import os
import argparse
import json
from datetime import datetime

from config import GITHUB_TOKEN, OPENAI_API_KEY, OPENAI_API_BASE
from git_utils import clone_github_repo, collect_blames_to_file
from llm_utils import invoke_review_llm
from report_utils import generate_pdf_report
from prompts import BASE_PROMPT



def parse_arguments():
    parser = argparse.ArgumentParser(description="Github Code Quality Reporter")
    parser.add_argument("--repo", required=True, help="Repository name, e.g., 'user/repo'")
    parser.add_argument("--author", required=True, help="Author email")
    parser.add_argument("--start-date", required=True, help="Start date in YYYY-MM-DD format")
    parser.add_argument("--end-date", required=True, help="End date in YYYY-MM-DD format")
    parser.add_argument("--output-dir", default=".\output", help="Output directory (default: .\output)")
    return parser.parse_args()


def main():
    args = parse_arguments()

    try:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
    except ValueError as e:
        print(f"Неверный формат даты: {e}")
        return
         
    try:
        repo_owner, repo_name = args.repo.split('/')
    except ValueError:
        print("Неверный формат репозитория. Ожидается 'user/repo'.")
        return

    tmp_dir = os.path.abspath("./tmp")
    local_repo_path = os.path.join(tmp_dir, repo_name)
    author_code_file = os.path.join(tmp_dir, f"{args.author}.txt")

    clone_github_repo(local_repo_path, repo_name, repo_owner, GITHUB_TOKEN)
    collect_blames_to_file(local_repo_path, args.author, start_date, end_date, author_code_file)

    with open(author_code_file, 'r', encoding='utf-8') as file:
        code = file.read()

    prompt = BASE_PROMPT.format(
        author_email=args.author,
        code=code
    )

    response = invoke_review_llm(prompt, OPENAI_API_KEY, OPENAI_API_BASE) 
    cleaned_response = response.content.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
    parsed_json = json.loads(cleaned_response)

    os.makedirs(args.output_dir, exist_ok=True)
    output_pdf_path = os.path.join(args.output_dir, "report.pdf")
    generate_pdf_report(parsed_json, args.author, args.repo, start_date, end_date, output_pdf_path)


if __name__ == "__main__":
    main()
