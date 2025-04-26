import json
import os
import time
from statistics import mean, median
import pandas as pd
from tqdm import tqdm
import sys
import shutil
import contextlib
import io
from datetime import datetime

start_time = datetime.now()
print(f"🕒 Início da execução: {start_time.strftime('%d/%m/%Y %H:%M:%S')}\n")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from config_token import configurar_token
from config_token_rotator import TokenRotator

tokens = configurar_token()
rotator = TokenRotator(tokens)

BASE_DIR = os.path.join("Lab3_CodeRevGithub", "Lab3S01")
DATA_DIR = os.path.join(BASE_DIR, "data")
REPO_FILE = os.path.join(DATA_DIR, "selected_repos.csv")
COLLECTED_FILE = os.path.join(DATA_DIR, "collected_prs.csv")
os.makedirs(DATA_DIR, exist_ok=True)

# Define margem de tolerância para pr_count
MARGIN = 5

def format_seconds(seconds):
    return time.strftime('%H:%M:%S', time.gmtime(seconds))

def mover_pycache(destino="Lab3_CodeRevGithub/Lab3S01/__pycache__"):
    for root, dirs, files in os.walk("."):
        if "__pycache__" in dirs:
            origem = os.path.join(root, "__pycache__")
            if os.path.abspath(origem) == os.path.abspath(destino):
                continue  # already in the right place
            os.makedirs(destino, exist_ok=True)
            for arquivo in os.listdir(origem):
                arquivo_destino = os.path.join(destino, arquivo)
                # Force overwrite by removing the existing file before moving
                if os.path.exists(arquivo_destino):
                    os.remove(arquivo_destino)
                shutil.move(os.path.join(origem, arquivo), destino)
            shutil.rmtree(origem)
            tqdm.write(f"📦 Pycache movido para: {destino}")

def handle_error_and_rate_limit(rotator, error=None, threshold=100, fallback_wait=60, max_wait=1800, retries=0):
    g = rotator.get()

    core = g.get_rate_limit().core
    if core.remaining <= threshold:
        tqdm.write(f"🔄 Token com apenas {core.remaining} requisições restantes. Alternando imediatamente para prevenir erro.")
        rotator.switch()
        g = rotator.get()  # Atualiza imediatamente o cliente GitHub após a troca
        return g

    return g

def collect_prs_from_repo(rotator, repo_name, min_valid_prs=100, max_valid_prs=None, max_pages=50):
    g = rotator.get()
    collected = []
    try:
        g = handle_error_and_rate_limit(rotator)
        repo = g.get_repo(repo_name)
        page = 0
        valid_count = 0
        analisados = 0

        total_prs_fechados = repo.get_pulls(state="closed").totalCount

        with tqdm(ncols=120, bar_format="   ⏳ {l_bar}{bar}| {n_fmt} PRs válidos coletados", leave=True, total=total_prs_fechados) as pbar:
            while page < max_pages:
                prs = repo.get_pulls(state="closed", sort="created", direction="desc").get_page(page)

                if not prs:
                    break

                for pr in prs:
                    if max_valid_prs and valid_count >= max_valid_prs:
                        break  # Limite máximo atingido

                    analisados += 1
                    try:
                        if not pr.closed_at:
                            continue

                        time_diff = pr.closed_at - pr.created_at
                        if time_diff.total_seconds() < 3600:
                            continue

                        with contextlib.redirect_stdout(io.StringIO()):
                            reviews = list(pr.get_reviews())
                        if not reviews or len(reviews) == 0:
                            continue

                        participants = set()
                        if pr.user and pr.user.login:
                            participants.add(pr.user.login)

                        try:
                            comments = list(pr.get_issue_comments())
                        except:
                            try:
                                comments = list(pr.get_comments())
                            except Exception as e:
                                if handle_error_and_rate_limit(rotator, error=e):
                                    g = rotator.get()
                                    continue
                                else:
                                    raise e

                        for comment in comments:
                            if comment.user and comment.user.login:
                                participants.add(comment.user.login)
                        for review in reviews:
                            if review.user and review.user.login:
                                participants.add(review.user.login)

                        collected.append({
                            "repo_name": repo_name,
                            "pr_number": pr.number,
                            "title": pr.title,
                            "body": pr.body or "",
                            "body_length": len(pr.body or ""),
                            "state": pr.state,
                            "merged": pr.merged,
                            "created_at": pr.created_at.isoformat(),
                            "closed_at": pr.closed_at.isoformat(),
                            "merged_at": pr.merged_at.isoformat() if pr.merged_at else None,
                            "review_count": len(reviews),
                            "files_changed": pr.changed_files,
                            "additions": pr.additions,
                            "deletions": pr.deletions,
                            "comments": pr.comments,
                            "review_comments": pr.review_comments,
                            "time_to_close_hours": time_diff.total_seconds() / 3600,
                            "participant_count": len(participants),
                            "language": repo.language   # <— adiciona o idioma do repositório
                        })

                        valid_count += 1
                        pbar.total = analisados
                        pbar.update(1)

                    except Exception as e:
                        if handle_error_and_rate_limit(rotator, error=e):
                            g = rotator.get()
                            continue
                        else:
                            raise e        
                time.sleep(1)

                if max_valid_prs and valid_count >= max_valid_prs:
                    break  # Limite máximo atingido

                page += 1

        tqdm.write(f"   🔍 {valid_count} PRs válidos encontrados entre {analisados} PRs avaliados em '{repo_name}'")

        #if valid_count < min_valid_prs:
           # tqdm.write(f"⚠️ Apenas {valid_count} PRs válidos encontrados em '{repo_name}' — abaixo do mínimo ({min_valid_prs}).")
           # return []

        return collected

    except Exception as e:
        if handle_error_and_rate_limit(rotator, error=e):
            return []
        else:
            raise e

# Função para salvar PRs coletados em CSV
def save_prs_to_files(prs, file_path):
    if not prs:
        print("🔴 Nenhum PR válido coletado. Arquivos não foram salvos.")
        return

    # Define colunas e ordem lógica
    selected = [
        "repo_name", "pr_number", "title", "body", "language",
        "created_at", "closed_at", "merged_at", "state", "merged",
        "review_count", "files_changed", "additions", "deletions",
        "comments", "review_comments", "time_to_close_hours", "participant_count"
    ]
    rows = [{k: r.get(k) for k in selected} for r in prs]
    df = pd.DataFrame(rows)

    # Limita o tamanho do body para facilitar leitura
    df["body"] = df["body"].apply(
        lambda x: (x[:300] + "...") if isinstance(x, str) and len(x) > 300 else x
    )

    print(f"\n   🧮 PRs consolidados atualmente: {len(prs)}")

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # 👉 Diferente do save_repos: aqui **não removemos arquivos antigos**

        # Salva CSV com separador ";"
        df.to_csv(file_path, index=False, sep=";", encoding="utf-8")
        print(f"       ✅ Arquivo CSV salvo em {file_path}")

        # Salva como JSON
        json_path = file_path.replace(".csv", ".json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(prs, f, indent=2, ensure_ascii=False)
        print(f"       ✅ Arquivo JSON salvo em {json_path}")

    except Exception as e:
        print(f"🔴 Erro ao salvar os arquivos de PRs: {e}\n")

def load_repos(file_path, required_columns=None):
    if required_columns is None:
        if "selected" in file_path:
            required_columns = ["full_name", "pr_count"]
        else:
            required_columns = [
                "repo_name", "pr_number", "title", "body", "state",
                "merged", "created_at", "closed_at", "merged_at",
                "review_count", "files_changed", "additions", "deletions",
                "comments", "review_comments", "time_to_close_hours", "participant_count"
            ]

    if os.path.exists(file_path):
        for sep in [";", ","]:
            try:
                df = pd.read_csv(file_path, sep=sep)
                check_columns = required_columns.copy()
                if "body_length" in check_columns:
                    check_columns.remove("body_length")
                if all(col in df.columns for col in check_columns):
                    return df
            except Exception:
                continue

    print(f"⚠️ Arquivo '{file_path}' inválido ou ausente. Criando novo com colunas padrão.")
    df = pd.DataFrame(columns=required_columns)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, index=False, sep=";")
    return df

def repo_has_valid_prs(collected_prs_df, repo_name, expected_total):
    repo_data = collected_prs_df[collected_prs_df['repo_name'] == repo_name]
    valid_prs = repo_data.dropna(subset=["pr_number", "title", "body", "state", "created_at", "closed_at"])
    return valid_prs.shape[0] >= expected_total

def compare_repositories(selected_repos_df, collected_prs_df):
    """
    Compara localmente o número de PRs válidos coletados vs esperado,
    exibindo tabela com colunas: #, Repositório, Esperado, Coletado, Completo, Remover.
    """
    # 1) Normaliza as listas de selecionados e coletados
    selected_repos  = selected_repos_df['full_name'].str.lower().str.strip().tolist()
    collected_repos = collected_prs_df['repo_name'].str.lower().str.strip().unique().tolist()

    # 2) Determina quais já não estão na lista atual (para coluna Remover)
    removed_repos          = [r for r in collected_repos if r not in selected_repos]
    collected_in_selected  = [r for r in collected_repos if r in selected_repos]
    len_removed            = len(removed_repos)
    total_collected        = len(collected_repos)
    total_in_selected      = len(collected_in_selected)

    complete_repos, incomplete_repos = [], []
    tabela_resultados = []

    tqdm.write("\n    🧮 Avaliando completude dos PRs coletados...\n")
    barra = tqdm(total=len(selected_repos), ncols=120,
                    bar_format="        ⏳ {l_bar}{bar}| {n_fmt}/{total_fmt} {percentage:3.0f}% {remaining}",
                    leave=True)

    # 4) Filtra apenas os PRs válidos localmente
    df = collected_prs_df.copy()
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['closed_at']  = pd.to_datetime(df['closed_at'])
    mask = (
        df['state'].str.lower().isin(['closed','merged']) &
        (df['review_count'].fillna(0).astype(int) > 0) &
        ((df['closed_at'] - df['created_at']).dt.total_seconds() > 3600)
    )
    valid_local_counts = df[mask] \
        .groupby(df['repo_name'].str.lower().str.strip()) \
        .size() \
        .to_dict()

    # 6) Monta o cabeçalho completo
    tqdm.write(f"{'#':^5} {'Repositório':<50} {'Esperado':^10} {'Coletado':^10} {'Completo':^10} {'Remover':^10}")

    # 7) Para cada selecionado, calcula esperado/coletado e sinaliza
    for idx, repo in enumerate(sorted(selected_repos, key=lambda r: r.lower()), start=1):
        exp = int(
            selected_repos_df.loc[
                selected_repos_df['full_name'].str.lower().str.strip() == repo,
                'pr_count'
            ].iloc[0]
        )
        loc = valid_local_counts.get(repo, 0)

        # completo?
        is_complete = (loc >= exp) or (loc >= exp - MARGIN)
        emoji_flag  = '✅' if is_complete else '❌'
        (complete_repos   if is_complete else incomplete_repos).append(repo)

        # remover?
        remover_emoji = '🗑️' if repo in removed_repos else '📌'

        # imprime linha
        tqdm.write(
            f"{str(idx).zfill(3):^5} {repo:<50}"
            f" {str(exp):^10} {str(loc):^10}"
            f" {emoji_flag:^10} {remover_emoji:^10}"
        )
        barra.update(1)

    barra.close()

    # 8) Retorna completos, incompletos e contagens
    return (
        complete_repos,
        incomplete_repos,
        len_removed,
        total_collected,
        total_in_selected,
        [],           # valid_repos (não usado)
        [],           # invalid_repos (não usado)
        removed_repos,
        valid_local_counts
    )

def show_initial_info():
    tqdm.write(f"📁 Caminho dos repositórios: {REPO_FILE}")
    tqdm.write(f"📁 Caminho dos PRs: {COLLECTED_FILE}\n")
    tqdm.write("-" * 120 + "\n")

def summarize_collection_results(
    selected_df, collected_df, complete_repos, incomplete_repos,
    missing_in_collected, extra_in_collected, output_file, valid_local_counts
):
    """
    Remove repositórios não selecionados, limita a 200, e escreve o resumo de completude.
    """
    # 🔥 Filtra PRs apenas dos repositórios selecionados
    if not collected_df.empty:
        selected_set = set(selected_df["full_name"].str.lower().str.strip())
        before = len(collected_df)
        collected_df = collected_df[collected_df["repo_name"].str.lower().str.strip().isin(selected_set)].reset_index(drop=True)
        if len(collected_df) != before:
            collected_df.to_csv(output_file, index=False, sep=";", encoding="utf-8")
            tqdm.write(f"🧹 {before - len(collected_df)} PRs removidos de repositórios não selecionados.")

    # 🔥 Limita a 200 repositórios
    unique_repos = collected_df["repo_name"].str.lower().str.strip().unique()
    if len(unique_repos) > 200:
        tqdm.write(f"⚠️ Mais de 200 repositórios detectados ({len(unique_repos)}). Mantendo apenas os 200 primeiros.")
        keep = list(selected_df["full_name"].str.lower().str.strip())[:200]
        before = len(collected_df)
        collected_df = collected_df[collected_df["repo_name"].str.lower().str.strip().isin(keep)].reset_index(drop=True)
        tqdm.write(f"✅ PRs filtrados para manter somente 200 repositórios ({before - len(collected_df)} removidos)")
        collected_df.to_csv(output_file, index=False, sep=";", encoding="utf-8")

    # ✅ Relatório da Coleta de PRs (corrigido)
    total_sel     = len(selected_df)
    # Conjunto de repos que realmente fizeram parte do DataFrame final
    processed_set = set(collected_df["repo_name"].str.lower().str.strip())
    total_proc    = len(processed_set)
    # Quantos não tiveram NENHUM PR coletado
    total_missing = len(missing_in_collected)
    # Dentre os processados, quantos ficaram completos/incompletos
    total_comp    = len([r for r in complete_repos   if r in processed_set])
    total_incmp   = len([r for r in incomplete_repos if r in processed_set])
    # Quantos foram removidos (extras)
    total_rmvd    = len(extra_in_collected)
    total_missing = len(missing_in_collected)

    tqdm.write("\n" + "-" * 120)
    tqdm.write("\n📈  Resumo da Coleta de PRs")
    tqdm.write(f"   📋  Repositórios selecionados: {total_sel}")
    tqdm.write(f"   🔄  Repositórios processados: {total_proc}")
    tqdm.write(f"   ✅  Repositórios com PRs completos: {total_comp}")
    tqdm.write(f"   ⚠️  Repositórios com PRs incompletos: {total_incmp}")
    tqdm.write(f"   🗑️  Repositórios removidos da lista atual: {total_rmvd}\n")
    tqdm.write(f"   🚫  Repositórios sem nenhum PR coletado: {total_missing}\n")
    tqdm.write("-" * 120 + "\n")

    collected_df.to_csv(output_file, index=False, sep=";", encoding="utf-8")
    return collected_df

def filter_collected_repositories(selected_repos_df, collected_prs_df, output_path) -> pd.DataFrame:
    selected_repos_set = set(selected_repos_df['full_name'].str.lower().str.strip())
    filtered_collected_repos_df = collected_prs_df[
        collected_prs_df['repo_name'].str.lower().str.strip().isin(selected_repos_set)
    ]
    filtered_collected_repos_df = filtered_collected_repos_df.drop_duplicates(subset=["repo_name"])
    filtered_collected_repos_df = filtered_collected_repos_df.head(200)
    filtered_collected_repos_df.to_csv(output_path, index=False, sep=";", encoding="utf-8")
    return filtered_collected_repos_df

def is_repo_complete(g, collected_df, repo_name, selected_df=None, save_path=None):
    """
    Verifica se um repositório está completo com base na contagem de PRs coletados.
    Considera completo se:
    - Número de PRs válidos localmente >= esperado remoto (cumpriu ou excedeu).
    - Ou número de PRs válidos localmente está dentro da margem de até 5 a menos do esperado.
    """
    repo_name_clean = repo_name.strip().lower()

    # Conta PRs válidos localmente (fechados e com comentários de revisão)
    local_valid = collected_df[
        (collected_df["repo_name"].str.strip().str.lower() == repo_name_clean) &
        (collected_df["state"].str.lower() == "closed") &
        (collected_df["review_comments"].fillna(0).astype(int) > 0)
    ].shape[0]

    # Obtém o pr_count remoto pré-calculado em selected_df, se disponível
    expected_remote = 0
    if selected_df is not None and "pr_count" in selected_df.columns:
        mask = selected_df["full_name"].str.strip().str.lower() == repo_name_clean
        if mask.any():
            expected_remote = int(selected_df.loc[mask, "pr_count"].iloc[0])

    # Marca como completo se exceder o esperado ou estiver dentro da margem inferior
    if local_valid >= expected_remote:
        completo = True
    elif local_valid >= expected_remote - MARGIN:
        completo = True
    else:
        completo = False

    # (Opcional) grava log de comparação
    if save_path:
        try:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "a", encoding="utf-8") as f:
                json.dump({
                    "repo": repo_name,
                    "esperado": expected_remote,
                    "coletado": local_valid
                }, f)
                f.write("\n")
        except Exception as e:
            tqdm.write(f"⚠️ Erro ao salvar log de comparação: {e}")

    return completo, expected_remote, local_valid

def coletar_prs_dos_repos(
    remaining_repos,
    missing_in_collected,
    collected_file,
    g,
    incomplete_repos,
    selected_repos_df,
    repo_to_idx    
):
    total_restantes = len(remaining_repos)
    tqdm.write(f"📄 Coletando PRs dos repositórios restantes ({total_restantes})...\n")

    total_prs_collected = 0
    repo_times = {}
    collected_df = load_repos(collected_file)

    for local_idx, repo_name in enumerate(remaining_repos, start=1):
        id_str = str(local_idx).zfill(3)
        idx = repo_to_idx.get(repo_name, 0)
        idx_str = str(idx).zfill(3)
        expected = int(
            selected_repos_df.loc[
                selected_repos_df["full_name"].str.lower().str.strip() == repo_name,
                "pr_count"
            ].iloc[0]
        )
        tipo = "\n   ♻️  RECOLETA" if repo_name in incomplete_repos else "\n   🆕  NOVO"
        tqdm.write(f"🔄 {id_str}/{total_restantes}   {tipo} ➜  {idx_str}  {repo_name} (esperado: {expected})")

        inicio = time.time()
        try:
            prs = collect_prs_from_repo(rotator, repo_name, min_valid_prs=100, max_valid_prs=None, max_pages=50)
        except Exception as e:
            tqdm.write(f"   ⚠️ Erro em {repo_name}: {e}")
            continue
        fim = time.time()
        tempo_str = format_seconds(fim - inicio)
        count = len(prs)
       # if count < 100:
           # tqdm.write(f"   ⚠️ Ignorado — menos de 100 PRs válidos. ⏱️ {tempo_str}")
           # continue

        total_prs_collected += count
        if prs:
            # concatena e deduplica
            new_df = pd.DataFrame(prs)
            collected_df = pd.concat([collected_df, new_df], ignore_index=True)
            before = collected_df.shape[0]
            collected_df.drop_duplicates(subset=["repo_name", "pr_number"], inplace=True)
            removed = before - collected_df.shape[0]
            collected_df.to_csv(collected_file, index=False, sep=";", encoding="utf-8")
            tqdm.write(f"   📊 Salvando coletado: {collected_df.shape[0]} PRs em {collected_file}")
        
        time.sleep(5)

        # ——— aqui atualiza o pr_count e grava os dois CSVs
        sel = pd.read_csv(REPO_FILE, sep=";")
        old = int(sel.loc[
            sel["full_name"].str.lower().str.strip() == repo_name,
            "pr_count"
        ].iloc[0])
        # total realmente coletado até agora
        total_local = collected_df[
            collected_df["repo_name"].str.lower().str.strip() == repo_name
        ].shape[0]

        if total_local < old - MARGIN:
            sel.loc[
            sel["full_name"].str.lower().str.strip() == repo_name,
                "pr_count"
            ] = total_local
            sel.to_csv(REPO_FILE, index=False, sep=";")
            tqdm.write(f"   🔄 Atualizando pr_count: {old} → {total_local}")

        print("\n")

    tqdm.write(f"\n📊 Total acumulado nesta execução: {total_prs_collected} PRs")

    tempos = list(repo_times.values())
    if tempos:
        media_tempo = mean(tempos)
        mediana_tempo = median(tempos)
        tempo_total = sum(tempos)

        tqdm.write(f"\n⏱️ Estatísticas de Tempo da Coleta:")
        tqdm.write(f"   🔹 Tempo total: {format_seconds(tempo_total)}")
        tqdm.write(f"   🔹 Tempo médio por repositório: {format_seconds(media_tempo)}")
        tqdm.write(f"   🔹 Tempo mediano por repositório: {format_seconds(mediana_tempo)}")


def main():
    # 1) Carrega DataFrames de selecionados e coletados
    selected_repos_df = load_repos(REPO_FILE)
    if selected_repos_df.empty or 'full_name' not in selected_repos_df.columns:
        tqdm.write("❌ Arquivo de repositórios selecionados está vazio ou mal formatado. Verifique o arquivo.")
        return

    collected_prs_df = load_repos(COLLECTED_FILE)
    collected_prs_df = collected_prs_df[
        collected_prs_df['repo_name'].str.lower().str.strip()
        .isin(selected_repos_df['full_name'].str.lower().str.strip())
    ].copy()
    collected_prs_df.to_csv(COLLECTED_FILE, index=False, sep=';', encoding='utf-8')

    # 2) Compara localmente os repositórios (sem API externa)
    complete_repos, incomplete_repos, len_removed, total_collected, total_in_selected, _, _, removed_repos, valid_local_counts = \
        compare_repositories(selected_repos_df, collected_prs_df)

    # 3) Calcula quais não tiveram NENHUM PR coletado
    selected_set  = set(selected_repos_df["full_name"].str.lower().str.strip())
    collected_set = set(collected_prs_df['repo_name'].str.lower().str.strip())
    missing_in_collected = list(selected_set - collected_set)

    # 4) Determina lista de repositórios a coletar (incompletos ∪ sem PR), exclui removidos
    pending = set(incomplete_repos) | set(missing_in_collected)
    remaining_repos = sorted(pending - set(removed_repos))

    # ⬇︎ Mapeia cada repo ao seu índice da listagem de comparação
    selected_repos = selected_repos_df['full_name'] \
        .str.lower().str.strip().tolist()
    repo_to_idx = {
        repo: idx
        for idx, repo in enumerate(
            sorted(selected_repos, key=lambda r: r.lower()),
            start=1
        )
    }

    # 5) Exibe e salva o resumo de completude
    collected_prs_df = summarize_collection_results(
        selected_repos_df,
        collected_prs_df,
        complete_repos,
        incomplete_repos,
        missing_in_collected,
        list(collected_set - selected_set),
        COLLECTED_FILE,
        valid_local_counts
    )

    # 6) Coleta PRs dos repositórios restantes
    if remaining_repos:
        coletar_prs_dos_repos(
            remaining_repos,
            missing_in_collected,
            COLLECTED_FILE,
            rotator,
            incomplete_repos,
            selected_repos_df,
            repo_to_idx        
        )
    else:
        tqdm.write("🔴 Não há repositórios restantes para coletar.")

    # 7) Exibe contagem final por repositório
    print("\n📋 PRs válidos por repositório (baseados na coleta via GraphQL):")
    print(f"{'Repositório':<50} | {'PRs válidos':^14}")
    print(f"{'-'*50} {'-'*14}")

    # Ordena alfabeticamente pelo nome completo do repositório
    filtered_final = sorted(
        filtered_final,
        key=lambda repo: repo.get("full_name", "").lower()
    )

    for repo in filtered_final:
        nome = repo.get("full_name", "").strip()
        pr_validos = repo.get("pr_count", 0)
        print(f"{nome:<50} {pr_validos:^14}")

    # Ajuste para usar a própria lista ordenada no total
    tqdm.write(f"\n📦 Total de repositórios no relatório final: {len(filtered_final)}")

    # 8) Finaliza
    end_time = datetime.now()
    duration = end_time - start_time
    print(f"\n🕔 Fim da execução: {end_time.strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"⏱️ Duração total: {duration}\n")

    # 9) Sobrescreve o arquivo de selecionados (caso tenha mudado)
    selected_repos_df.to_csv(REPO_FILE, index=False, sep=';', encoding='utf-8')

# === EXECUÇÃO PRINCIPAL ===
if __name__ == "__main__":
    main()
    mover_pycache()
