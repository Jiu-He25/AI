# 输入输出逻辑处理，统一模型调用
from deepseek_api import call_deepseek
from schema import validate_input
from config import TEMPERATURES

def process_input(data: dict):
    validate_input(data)
    prompt = data["user_input"]
    results = {}
    for temp in TEMPERATURES:
        output = call_deepseek(prompt, temp)
        results[temp] = output
    return results
