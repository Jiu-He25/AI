import argparse
from schema import validate_input
from deepseek_api import call_deepseek_model

def main():
    parser = argparse.ArgumentParser(description="调用 DeepSeek API 进行文本生成")
    parser.add_argument("--prompt", type=str, required=True, help="输入提示词")
    parser.add_argument("--temperature", type=float, default=0.7, help="生成温度（影响创造力）")
    args = parser.parse_args()

    # 构造输入数据
    input_data = {
        "user_input": args.prompt
    }

    # 校验输入格式
    try:
        validate_input(input_data)
    except ValueError as e:
        print(f"[输入错误] {e}")
        return

    # 调用模型
    try:
        print(f"\n[模型调用中] prompt: {args.prompt} | temperature: {args.temperature}")
        output = call_deepseek_model(prompt=args.prompt, temperature=args.temperature)
        print("\n[模型输出]")
        print(output)
    except Exception as e:
        print(f"[错误] 模型调用失败：{e}")


if __name__ == "__main__":
    main()