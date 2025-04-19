import os
import subprocess
from datetime import datetime

def clone_repo(repo_path, repo_name, repo_owner, github_token):
    repo_url = f"https://{github_token}@github.com/{repo_owner}/{repo_name}.git"
    if not os.path.exists(repo_path):
        subprocess.run(
            ["git", "clone", repo_url, repo_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

def run_git_blame(filepath, repo_path):
    result = subprocess.run(
        ["git", "blame", "--line-porcelain", filepath],
        cwd=repo_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8"
    )
    if result.returncode != 0:
        print(f"[!] Blame failed for {filepath}: {result.stderr}")
        return None
    return result.stdout


def extract_author_lines(blame_output, author_email, since, until):
    lines = []
    has_author_lines = False
    current_author = ""
    current_time = None

    for line in blame_output.splitlines():
        if line.startswith("author-mail "):
            current_author = line.split(" ")[1].strip("<>")
        elif line.startswith("author-time "):
            timestamp = int(line.split(" ")[1])
            current_time = datetime.utcfromtimestamp(timestamp)
        elif line.startswith("\t"):
            code_line = line[1:]
            if current_author == author_email and since <= current_time <= until:
                has_author_lines = True
                lines.append(f"// by {author_email} at {current_time}:\n{code_line}")
            else:
                lines.append(code_line)

    return lines if has_author_lines else None


def collect_blames_to_file(repo_path, author_email, since, until, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as out_file:
        for root, _, files in os.walk(repo_path):
            for filename in files:
                if filename.endswith(('.py', '.java', '.php')):
                    full_path = os.path.join(root, filename)
                    rel_path = os.path.relpath(full_path, repo_path)
                    blame_output = run_git_blame(rel_path, repo_path)
                    if blame_output:
                        relevant_lines = extract_author_lines(blame_output, author_email, since, until)
                        if relevant_lines:
                            out_file.write(f"====== FILE: {rel_path} ======\n")
                            out_file.write("\n".join(relevant_lines))
                            out_file.write("\n\n")