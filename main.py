# main.py
import os
import sys
import asyncio
import argparse
from dotenv import load_dotenv
from core import run_llm_application

load_dotenv()

def run_cli_mode():
    """命令行模式"""
    parser = argparse.ArgumentParser(description="DeepSeek CLI")
    parser.add_argument("--prompt", required=True, help="输入提示词")
    parser.add_argument("--temperature", type=float, default=0.7)
    args = parser.parse_args()

    input_data = {
        "api_key": os.getenv("DEEPSEEK_API_KEY"),
        "prompt": args.prompt,
        "parameters": {"temperature": args.temperature}
    }

    result = asyncio.run(run_llm_application(input_data))
    print(result)

def run_gui_mode():
    """图形界面模式"""
    from PyQt5.QtWidgets import QApplication
    from ui.guiFrame import ChatForm
    
    app = QApplication(sys.argv)
    window = ChatForm()
    window.setWindowTitle("DeepSeek Chat")
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_cli_mode()
    else:
        run_gui_mode()