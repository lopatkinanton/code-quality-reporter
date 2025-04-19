from langchain_openai import ChatOpenAI

def run_code_review(prompt, api_key, api_base):
    llm = ChatOpenAI(
        model="qwen/qwen-2.5-coder-32b-instruct:free",
        temperature=0,
        openai_api_key=api_key,
        openai_api_base=api_base,
        request_timeout=60
    )

    return llm.invoke(prompt)
