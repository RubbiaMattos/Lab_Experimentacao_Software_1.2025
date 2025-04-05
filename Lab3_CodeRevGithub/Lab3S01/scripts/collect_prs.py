from github import Github
import os
import time
import pandas as pd
import requests
from tqdm import tqdm
import random
import sys
import shutil
import contextlib
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from config_token import configurar_token

EXACT_REQUIRED_PRS = 100

BASE_DIR = os.path.join("Lab3_CodeRevGithub", "Lab3S01")
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

repo_file = os.path.join(DATA_DIR, "selected_repos.csv")
collected_file = os.path.join(DATA_DIR, "collected_prs.csv")

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
            print(f"📦 Pycache movido para: {destino}")

def handle_error_and_rate_limit(g, error=None, fallback_wait=600, max_wait=1800):
    import traceback
    wait_seconds = None
    status_info = ""
    handled = False

    try:
        if isinstance(error, Exception):
            status_info = f"{type(error).__name__} — {error}"

            # Verifica se é uma exceção do PyGithub com headers
            if hasattr(error, 'status') or hasattr(error, 'status_code'):
                status_code = getattr(error, 'status', None) or getattr(error, 'status_code', None)
                if status_code == 403:
                    try:
                        core = g.get_rate_limit().core
                        remaining = core.remaining
                        reset_timestamp = core.reset.timestamp()
                        now = time.time()



                        if remaining == 0:
                            wait_seconds = max(int(reset_timestamp - now + 10), 10)
                        else:
                            wait_seconds = random.randint(fallback_wait, max_wait)

                        handled = True
                    except Exception as fallback_check:
                        status_info += f" | Erro ao checar rate limit: {fallback_check}"
                        wait_seconds = random.randint(fallback_wait, max_wait)
                        handled = True


            # Trata timeout, conexão recusada, e erros comuns de rede
            elif isinstance(error, (
                ConnectionError,
                TimeoutError,
                OSError,
                requests.exceptions.RequestException,
                requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError,
                requests.exceptions.Timeout,
                requests.exceptions.TooManyRedirects,
            )):
                wait_seconds = random.randint(60, 180)
                handled = True


            # Catch-all para outros erros — imprime stacktrace para depuração
            else:
                wait_seconds = random.randint(fallback_wait, max_wait)
                handled = True

    except Exception as e:
        status_info = f"Erro ao lidar com erro: {type(e).__name__} — {e}"
        wait_seconds = random.randint(fallback_wait, max_wait)
        handled = True

    if wait_seconds and handled:
        if wait_seconds > max_wait:
            wait_seconds = random.randint(fallback_wait, max_wait)

        tqdm.write(f"\n⚠️ Erro: {status_info}")
        tqdm.write(f"🚦 Limite de requisições da API atingido ou outro erro - Iniciando pausa temporária..")
        tqdm.write(f"⏳ Estimativa de espera: {wait_seconds} segundos até a liberação de novas requisições...\n")
        time.sleep(wait_seconds)
        return True  # Pausou

    return False  # Não pausou (não foi erro esperado)

def collect_prs_from_repo(g, repo_name, min_prs=100, max_prs=100):
    collected = []
    try:
        repo = g.get_repo(repo_name)
        pulls = repo.get_pulls(state="closed", sort="created", direction="desc")
        pulls_list = list(pulls)
        collected_count = 0
        attempts = 0
        max_attempts = 10

        with tqdm(total=max_prs, ncols=120, bar_format="    ⏳{l_bar}{bar}| {n:03d}/{total:03d} {percentage:3.0f}% {remaining}", leave=True) as pbar:
            while collected_count < max_prs and attempts < max_attempts:
                for pr in pulls_list:
                    if collected_count >= max_prs:
                        break

                    try:
                        while True:
                            try:
                                with contextlib.redirect_stdout(io.StringIO()):
                                    reviews = list(pr.get_reviews())    
                                break
                            except Exception as e:
                                if handle_error_and_rate_limit(g, error=e):
                                    continue
                                else:
                                    raise e

                        if not pr.closed_at:
                            continue

                        time_diff = pr.closed_at - pr.created_at
                        if time_diff.total_seconds() < 3600:
                            continue

                        participants = set()
                        if pr.user and pr.user.login:
                            participants.add(pr.user.login)

                        for review in reviews:
                            if review.user and review.user.login:
                                participants.add(review.user.login)

                        while True:
                            try:
                                with contextlib.redirect_stdout(io.StringIO()):
                                    try:
                                        comments = list(pr.get_issue_comments())
                                    except Exception:
                                        comments = list(pr.get_comments())
                                break
                            except Exception as e:
                                if handle_error_and_rate_limit(g, error=e):
                                    continue
                                else:
                                    raise e

                        for comment in comments:
                            if comment.user and comment.user.login:
                                participants.add(comment.user.login)

                        if len(reviews) == 0 and len(comments) == 0:
                            continue

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
                            "participant_count": len(participants)
                        })

                        collected_count += 1
                        pbar.update(1)

                    except Exception as e:
                        if handle_error_and_rate_limit(g, error=e):
                            continue
                        else:
                            raise e

                if collected_count < max_prs:
                    tqdm.write(f"⏳ Coletados {collected_count}/{max_prs} PRs — aguardando antes de tentar novamente...")
                    time.sleep(60)
                    attempts += 1

        if collected_count < min_prs:
            print(f"⚠️ Apenas {collected_count} PRs válidos coletados de '{repo_name}' — abaixo do mínimo ({min_prs}).")
            return []

        return collected

    except Exception as e:
        if handle_error_and_rate_limit(g, error=e):
            return []
        else:
            raise e


# Função para salvar PRs coletados em CSV
def save_prs_to_csv(prs, output_file):
    if prs:
        df = pd.DataFrame(prs)

        # Garantir que o diretório existe antes de salvar
        directory = os.path.dirname(output_file)
        if not os.path.exists(directory):
            print(f"🚧 Diretório {directory} não encontrado. Criando diretório...")
            os.makedirs(directory, exist_ok=True)

        # Agora salvar o arquivo
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"✅ {len(prs)} PRs salvos em {output_file}")
    else:
        print("🔴 Nenhum PR para salvar. Nada foi feito.")


# Função para carregar repositórios do arquivo CSV ou criar arquivo vazio, se necessário
def load_repos(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        print(f"🔴 Arquivo {file_path} não encontrado. Criando arquivo CSV vazio...")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        empty_df = pd.DataFrame(columns=[
            "repo_name", "pr_number", "title", "body", "body_length", "state",
            "merged", "created_at", "closed_at", "merged_at", "review_count",
            "files_changed", "additions", "deletions", "comments",
            "review_comments", "time_to_close_hours", "participant_count"
        ])
        empty_df.to_csv(file_path, index=False)
        return empty_df


def repo_has_valid_prs(collected_prs_df, repo_name, exact_prs=100):
    repo_data = collected_prs_df[collected_prs_df['repo_name'] == repo_name]
    valid_prs = repo_data.dropna(subset=["pr_number", "title", "body", "state", "created_at", "closed_at"])
    return valid_prs.shape[0] == exact_prs

def compare_repositories(selected_repos_df, collected_prs_df, g):
    selected_repos = selected_repos_df['full_name'].tolist()
    collected_repos = collected_prs_df['repo_name'].unique().tolist()

    valid_repos = []
    invalid_repos = []

    print("    🔍 Verificando Repositórios Selecionados...")
    with tqdm(total=len(selected_repos), ncols=120, bar_format="    ⏳ {l_bar}{bar}| {n:03d}/{total:03d} {percentage:3.0f}% {remaining}", leave=True, position=0) as pbar:
        for repo_name in selected_repos:
            try:
                g.get_repo(repo_name)
                valid_repos.append(repo_name)
            except Exception:
                invalid_repos.append(repo_name)
            pbar.update(1)

    removed_repos = [repo for repo in collected_repos if repo not in selected_repos]
    collected_in_selected = [repo for repo in collected_repos if repo in selected_repos]

    complete_repos = []
    incomplete_repos = []
    for repo in collected_in_selected:
        if repo_has_valid_prs(collected_prs_df, repo, exact_prs=EXACT_REQUIRED_PRS):
            complete_repos.append(repo)
        else:
            incomplete_repos.append(repo)

    remaining_to_collect_or_complete = len(selected_repos) - len(complete_repos)

    return complete_repos, incomplete_repos, len(removed_repos), len(collected_repos), len(collected_in_selected), remaining_to_collect_or_complete, valid_repos, invalid_repos, removed_repos

def filter_remaining_repos(selected_repos_df, collected_repos_df):
    selected_repos = selected_repos_df['full_name'].tolist()
    collected_repos = collected_repos_df['repo_name'].unique().tolist()

    # Repositórios que precisam ser coletados (não estão na lista de coletados)
    remaining_repos = [repo for repo in selected_repos if repo not in collected_repos]

    return remaining_repos


from statistics import mean, median

def main():
    # Configurar o token do GitHub
    g = Github(configurar_token())

    base_dir = os.path.join("Lab3_CodeRevGithub", "Lab3S01")
    data_dir = os.path.join(base_dir, "data")

    repo_file = os.path.join(data_dir, "selected_repos.csv")
    collected_file = os.path.join(data_dir, "collected_prs.csv")

    print(f"📁 O caminho para o arquivo de repositórios selecionados é: {repo_file}")
    print(f"📁 O caminho para salvar os PRs coletados é: {collected_file}\n")
    print("-" * 120 + "\n")

    selected_repos_df = load_repos(repo_file)
    collected_prs_df = load_repos(collected_file)

    complete_repos, incomplete_repos, removed_repos_count, total_collected_repos, collected_in_selected_count, _, valid_repos, invalid_repos, removed_repos = compare_repositories(selected_repos_df, collected_prs_df, g)

    selected_set = set(selected_repos_df['full_name'])
    collected_set = set(collected_prs_df['repo_name'])
    completos_set = set(complete_repos)
    incompletos_set = set(incomplete_repos)
    removidos_set = collected_set - selected_set

    # Pendentes = selecionados que não estão nem completos nem incompletos
    repos_pendentes_set = selected_set - completos_set - incompletos_set
    remaining_to_collect_count = len(repos_pendentes_set)

    total_check = len(completos_set) + len(incompletos_set) + len(repos_pendentes_set)
    assert total_check == len(selected_set), f"Soma de estados incorreta: {total_check} != {len(selected_set)}"

    print("\n📊 Resumo da Coleta de PRs\n")
    print(f"   📋 Repositórios selecionados: {len(selected_repos_df)}")
    print(f"   📋 Repositórios processados: {total_collected_repos}")
    print(f"   📋 Repositórios com PRs completos: {len(complete_repos)}")
    print(f"   📋 Repositórios com PRs incompletos: {len(incomplete_repos)}")
    print(f"   🗑️  Repositórios anteriormente coletados, mas removidos da lista atual: {len(removidos_set)}")
    print(f"\n   📋 Repositórios pendentes de coleta: {remaining_to_collect_count}\n")
    print("-" * 120 + "\n")

    # 🧹 Limpa os PRs de repositórios que não estão mais nos selecionados
    if not collected_prs_df.empty and len(removidos_set) > 0:
        before = len(collected_prs_df)
        collected_prs_df = collected_prs_df[~collected_prs_df["repo_name"].isin(removidos_set)].reset_index(drop=True)
        after = len(collected_prs_df)

        if before != after:
            collected_prs_df.to_csv(collected_file, index=False, encoding='utf-8')

    # Repositórios que ainda precisam ser coletados (não estão no arquivo ou estão incompletos)
    remaining_repos = list(repos_pendentes_set)
    if incomplete_repos:
        print(f"🔁 Incluindo {len(incomplete_repos)} repositórios incompletos na nova rodada de coleta...")
        remaining_repos += incomplete_repos
        remaining_repos = list(set(remaining_repos))

    if remaining_repos:
        print(f"\n📄 Coletando PRs dos repositórios restantes ({len(remaining_repos)})...")

        total_prs_collected = 0
        repo_times = {}

        if os.path.exists(collected_file):
            collected_df = pd.read_csv(collected_file)
        else:
            collected_df = pd.DataFrame()

        for idx, repo_name in enumerate(remaining_repos):
            tqdm.write(f"\n🔄 {str(idx + 1).zfill(2)}/{len(remaining_repos)} Coletando PRs de repositório: {repo_name}")
            inicio = time.time()
            prs = collect_prs_from_repo(g, repo_name)
            fim = time.time()
            tempo = fim - inicio
            repo_times[repo_name] = tempo
            tempo_str = format_seconds(tempo)

            if prs:
                total_prs_collected += len(prs)
                print(f"   📦 PRs coletados do repositório '{repo_name}': {len(prs)} PRs ⏱️ Tempo: {tempo_str}")

                new_df = pd.DataFrame(prs)
                collected_df = pd.concat([collected_df, new_df], ignore_index=True)
                collected_df.to_csv(collected_file, index=False, encoding='utf-8')
                print(f"   📅 PRs salvos no arquivo: {collected_file}")
            else:
                print(f"   ⚠️ Repositório '{repo_name}' ignorado — menos de 500 PRs válidos. ⏱️ Tempo: {tempo_str}")

        print(f"\n📊 Total acumulado de PRs coletados nesta execução: {total_prs_collected}")

        tempos = list(repo_times.values())
        if tempos:
            media_tempo = mean(tempos)
            mediana_tempo = median(tempos)
            tempo_total = sum(tempos)

            print(f"\n⏱️ Estatísticas de Tempo da Coleta:")
            print(f"   🔹 Tempo total: {format_seconds(tempo_total)}")
            print(f"   🔹 Tempo médio por repositório: {format_seconds(media_tempo)}")
            print(f"   🔹 Tempo mediano por repositório: {format_seconds(mediana_tempo)}")

    else:
        print("🔴 Não há repositórios restantes para coletar.")

if __name__ == "__main__":
    main()
    mover_pycache()