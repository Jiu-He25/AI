# # import asyncio
# # import argparse
# # import sys
# # from llm_service import LLMService
# # from processor import InputPreprocessor, SecurityException
# # from exception_handler import LLMExceptionHandler, LLMServiceException
# # from dotenv import load_dotenv
# # import os
# # from PyQt5.QtWidgets import QApplication
# # from ui.guiFrame import ChatForm
# # load_dotenv()
# import os
# import sys
# import asyncio
# import argparse
# from dotenv import load_dotenv

# # 本地模块导入（使用相对路径）
# from llm_service import LLMService
# from processor import InputPreprocessor, SecurityException
# from exception_handler import LLMExceptionHandler, LLMServiceException

# # GUI 相关导入（仅在 GUI 模式时加载）
# if not sys.argv[1:]:  # 无命令行参数时
#     from PyQt5.QtWidgets import QApplication
#     from ui.guiFrame import ChatForm

# # 输入输出JSON Schema定义
# INPUT_SCHEMA = {
#     "type": "object",
#     "required": ["prompt", "modality"],
#     "properties": {
#         "prompt": {
#             "type": "string",
#             "minLength": 1,
#             "description": "用户输入的文本提示"
#         },
#         "modality": {
#             "type": "string",
#             "enum": ["text", "image", "audio", "video"],
#             "description": "输入模态类型"
#         },
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "temperature": {
#                     "type": "number",
#                     "minimum": 0.0,
#                     "maximum": 2.0,
#                     "default": 0.7,
#                     "description": "模型输出随机性控制参数"
#                 },
#                 "max_tokens": {
#                     "type": "integer",
#                     "minimum": 1,
#                     "maximum": 4096,
#                     "default": 512,
#                     "description": "最大输出token数量"
#                 }
#             }
#         },
#         "context": {
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "required": ["role", "content"],
#                 "properties": {
#                     "role": {
#                         "type": "string",
#                         "enum": ["user", "assistant", "system"],
#                         "description": "对话角色"
#                     },
#                     "content": {
#                         "type": "string",
#                         "description": "对话内容"
#                     }
#                 }
#             },
#             "description": "对话历史上下文"
#         }
#     }
# }

# OUTPUT_SCHEMA = {
#     "type": "object",
#     "required": ["result", "model_info", "timestamp"],
#     "properties": {
#         "result": {
#             "type": "string",
#             "description": "模型输出结果"
#         },
#         "model_info": {
#             "type": "object",
#             "required": ["model_name", "parameters"],
#             "properties": {
#                 "model_name": {
#                     "type": "string",
#                     "description": "使用的模型名称"
#                 },
#                 "parameters": {
#                     "type": "object",
#                     "description": "模型调用参数"
#                 },
#                 "tokens_used": {
#                     "type": "integer",
#                     "description": "使用的token数量"
#                 }
#             }
#         },
#         "timestamp": {
#             "type": "string",
#             "format": "date-time",
#             "description": "响应时间戳"
#         },
#         "modality_output": {
#             "type": "object",
#             "description": "多模态输出内容（如图像URL、音频链接等）"
#         }
#     }
# }


# async def run_llm_application(input_data):
#     """运行大语言模型应用主流程"""
#     try:
#         # 1. 初始化模块
#         api_key = input_data.get("api_key", "")
#         model_url = input_data.get("model_url", "https://api.deepseek.com/v1/chat/completions")
#         llm_service = LLMService(api_key, model_url)
#         stream_handler = StreamHandler(llm_service)
#         preprocessor = InputPreprocessor()
#         exception_handler = LLMExceptionHandler(max_retries=3, retry_delay=2)

#         # 2. 输入预处理
#         preprocessed_data = preprocessor.preprocess_input(input_data)

#         # 转换为messages格式
#         messages = [{"role": "user", "content": preprocessed_data["prompt"]}]
#         if "context" in preprocessed_data:
#             messages = preprocessed_data["context"] + messages

#         params = preprocessed_data.get("parameters", {})

#         # 3. 参数调优（可选）
#         if input_data.get("tune_parameters", False):
#             tuner = ParameterTuner(llm_service)
#             params = tuner.recommend_parameters(messages[0]["content"], params)
#             print(f"调优后参数: {params}")

#         if params.get("stream", False):
#             # 流式响应处理
#             print("模型输出（流式）:")
#             full_response = ""
#             async for chunk in stream_handler.stream_response(messages, params):
#                 print(chunk, end="", flush=True)
#                 full_response += chunk
#             print("\n")

#             # 检查是否有错误信息
#             if full_response.startswith("[错误:"):
#                 raise LLMServiceException(full_response)

#             # 处理结构化输出
#             if input_data.get("expect_structured_output", False):
#                 structured_output = exception_handler.handle_structured_output_failure(
#                     full_response,
#                     OUTPUT_SCHEMA
#                 )
#                 print("结构化输出结果:")
#                 print(json.dumps(structured_output, ensure_ascii=False, indent=2))

#         else:
#             # 非流式处理
#             response = exception_handler.handle_api_failure(
#                 lambda: llm_service.call_model(messages, **params),
#                 params
#             )

#             if response and "choices" in response:
#                 output_text = response["choices"][0]["message"]["content"]
#                 print(f"模型输出: {output_text}")

#                 # 处理结构化输出
#                 if input_data.get("expect_structured_output", False):
#                     structured_output = exception_handler.handle_structured_output_failure(
#                         output_text,
#                         OUTPUT_SCHEMA
#                     )
#                     print("结构化输出结果:")
#                     print(json.dumps(structured_output, ensure_ascii=False, indent=2))
#             else:
#                 raise LLMServiceException(f"无效的模型响应: {response}")

#         return {"status": "success", "response": response if not params.get("stream") else full_response}


#     except SecurityException as se:
#         print(f"安全警告: {str(se)}")
#         return {"status": "error", "message": str(se)}
#     except LLMServiceException as lse:
#         print(f"模型服务异常: {str(lse)}")
#         return {"status": "error", "message": str(lse)}
#     except Exception as e:
#         print(f"应用运行错误: {str(e)}")
#         return {"status": "error", "message": str(e)}

# def run_cli_mode():
#     """命令行模式"""
#     parser = argparse.ArgumentParser(description="DeepSeek 模型调用工具")
#     parser.add_argument("--prompt", type=str, required=True, help="输入提示词")
#     parser.add_argument("--temperature", type=float, default=0.7, help="生成温度")
#     parser.add_argument("--stream", action="store_true", help="启用流式输出")
#     args = parser.parse_args()

#     input_data = {
#         "api_key": os.getenv("DEEPSEEK_API_KEY"),
#         "prompt": args.prompt,
#         "modality": "text",
#         "parameters": {
#             "temperature": args.temperature,
#             "stream": args.stream
#         }
#     }

#     # 异步调用核心逻辑
#     result = asyncio.run(run_llm_application(input_data))
#     print("\n最终结果:")
#     print(json.dumps(result, indent=2))

# def run_gui_mode():
#     """图形界面模式"""
#     app = QApplication(sys.argv)
#     window = ChatForm()
#     window.setWindowTitle("DeepSeek Chat")
#     window.show()
#     sys.exit(app.exec_())

# if __name__ == "__main__":

    # # 优化后的提示词（明确、无敏感词）
    # sample_input = {
    #     "api_key": os.getenv("DEEPSEEK_API_KEY"),
    #     "prompt": "what can you do?",
    #     "modality": "text",
    #     "parameters": {
    #         "temperature": 0.7,  # 降低随机性，使故事结构更紧凑
    #         "max_tokens": 800,  # 增加生成长度以包含完整情节
    #         "stream": True  # 启用流式输出
    #     },
    #     "tune_parameters": True,  # 启用参数调优
    #     "expect_structured_output": False
    # }

    # asyncio.run(run_llm_application(sample_input))
    # if len(sys.argv) > 1:
    #     run_cli_mode()  # 有参数时启动 CLI
    # else:
    #     run_gui_mode()  # 无参数时启动 GUI
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