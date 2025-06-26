# cli.py
import argparse
import asyncio
from core import run_llm_application

def main():
    parser = argparse.ArgumentParser(description="DeepSeek CLI")
    parser.add_argument("--prompt", required=True)
    args = parser.parse_args()

    input_data = {
        "prompt": args.prompt,
        "parameters": {"temperature": 0.7}
    }

    result = asyncio.run(run_llm_application(input_data))
    print(result)

if __name__ == "__main__":
    main()