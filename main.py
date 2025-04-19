import os
import argparse
from datetime import datetime
import json

from config import GITHUB_TOKEN, OPENAI_API_KEY, OPENAI_API_BASE
from git_utils import clone_repo, collect_blames_to_file
from llm_utils import run_code_review
from report_utils import generate_pdf_from_json
from prompts import BASE_PROMPT


def parse_arguments():
    parser = argparse.ArgumentParser(description="Github Code Quality Reporter")
    parser.add_argument("--repo", required=True, help="Repository name, e.g., 'user/repo'")
    parser.add_argument("--author", required=True, help="Author email")
    parser.add_argument("--start-date", required=True, help="Start date in YYYY-MM-DD format")
    parser.add_argument("--end-date", required=True, help="End date in YYYY-MM-DD format")
    parser.add_argument("--output-dir", default="output", help="Output directory (default: ./output)")
    return parser.parse_args()


def main():
    args = parse_arguments()

    try:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
    except ValueError as e:
        print(f"Неверный формат даты: {e}")
        return

    repo_owner, repo_name = args.repo.split('/')
    tmp_dir = os.path.abspath("./tmp")
    local_repo_path = os.path.join(tmp_dir, repo_name)
    author_code_file = os.path.join(tmp_dir, f"{args.author}.txt")

    clone_repo(local_repo_path, repo_name, repo_owner, GITHUB_TOKEN)
    collect_blames_to_file(local_repo_path, args.author, start_date, end_date, author_code_file)

    with open(author_code_file, 'r', encoding='utf-8') as file:
        code = file.read()

    prompt = BASE_PROMPT.format(
        author_email=args.author,
        code=code
    )

    try:
        response = run_code_review(prompt, OPENAI_API_KEY, OPENAI_API_BASE)
    except Exception as e:
        print(f"Ошибка во время запроса к LLM: {e}")

    fixed_str = response.content.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
    parsed_json = json.loads(fixed_str)
    generate_pdf_from_json(parsed_json, args.author, start_date, end_date)


if __name__ == "__main__":
    main()
