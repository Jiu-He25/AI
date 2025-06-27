import asyncio
from llm_service import LLMService
from input_processor import InputPreprocessor, SecurityException
from stream_handler import StreamHandler
from parameter_tuner import ParameterTuner
from exception_handler import LLMExceptionHandler, LLMServiceException
from dotenv import load_dotenv
import os
import json 
import logging
import jsonschema
from jsonschema import validate, ValidationError
from typing import Dict,Any

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
# 输入输出JSON Schema定义
INPUT_SCHEMA = {
    "type": "object",
    "required": ["prompt", "modality"],
    "properties": {
        "prompt": {
            "type": "string",
            "minLength": 1,
            "description": "用户输入的文本提示"
        },
        "modality": {
            "type": "string",
            "enum": ["text", "image", "audio", "video"],
            "description": "输入模态类型"
        },
        "parameters": {
            "type": "object",
            "properties": {
                "temperature": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 2.0,
                    "default": 0.7,
                    "description": "模型输出随机性控制参数"
                },
                "max_tokens": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 4096,
                    "default": 512,
                    "description": "最大输出token数量"
                }
            }
        },
        "context": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["role", "content"],
                "properties": {
                    "role": {
                        "type": "string",
                        "enum": ["user", "assistant", "system"],
                        "description": "对话角色"
                    },
                    "content": {
                        "type": "string",
                        "description": "对话内容"
                    }
                }
            },
            "description": "对话历史上下文"
        }
    }
}

OUTPUT_SCHEMA = {
    "type": "object",
    "required": ["result", "model_info", "timestamp"],
    "properties": {
        "result": {
            "type": "string",
            "description": "模型输出结果"
        },
        "model_info": {
            "type": "object",
            "required": ["model_name", "parameters"],
            "properties": {
                "model_name": {
                    "type": "string",
                    "description": "使用的模型名称"
                },
                "parameters": {
                    "type": "object",
                    "description": "模型调用参数"
                },
                "tokens_used": {
                    "type": "integer",
                    "description": "使用的token数量"
                }
            }
        },
        "timestamp": {
            "type": "string",
            "format": "date-time",
            "description": "响应时间戳"
        },
        "modality_output": {
            "type": "object",
            "description": "多模态输出内容（如图像URL、音频链接等）"
        }
    }
}

# 异常类定义
class LLMException(Exception):
    """LLM应用基础异常类"""
    def __init__(self, message: str, code: int = 500):
        super().__init__(message)
        self.message = message
        self.code = code

    def to_dict(self):
        return {"error": {"message": self.message, "code": self.code}}

class SecurityException(LLMException):
    """安全相关异常"""
    def __init__(self, message: str):
        super().__init__(message, 403)

class LLMServiceException(LLMException):
    """LLM服务异常"""
    def __init__(self, message: str, code: int = 500):
        super().__init__(message, code)

class ConfigurationException(LLMException):
    """配置异常"""
    def __init__(self, message: str):
        super().__init__(message, 500)

class ValidationException(LLMException):
    """验证异常"""
    def __init__(self, message: str):
        super().__init__(message, 400)

# 输入输出验证器
class Validator:
    """输入输出验证工具类"""
    @staticmethod
    def validate_input(data: Dict[str, Any]) -> None:
        """验证输入数据是否符合INPUT_SCHEMA"""
        try:
            validate(instance=data, schema=INPUT_SCHEMA)
            logger.info("输入数据格式验证通过")
        except ValidationError as e:
            logger.error(f"输入数据格式错误: {e}")
            raise ValidationException(f"输入格式错误: {e.message}")
    
    @staticmethod
    def validate_output(data: Dict[str, Any]) -> None:
        """验证输出数据是否符合OUTPUT_SCHEMA"""
        try:
            validate(instance=data, schema=OUTPUT_SCHEMA)
            logger.info("输出数据格式验证通过")
        except ValidationError as e:
            logger.warning(f"输出数据格式不符合规范: {e}")
            # 这里选择记录警告而不是抛出异常，因为可能需要处理非结构化输出

    @staticmethod
    def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
        """清理和规范化输入数据"""
        sanitized = data.copy()
        # 处理参数默认值
        if "parameters" in sanitized:
            params = sanitized["parameters"]
            params.setdefault("temperature", 0.7)
            params.setdefault("max_tokens", 512)
            params.setdefault("stream", False)
            sanitized["parameters"] = params
        return sanitized

async def run_llm_application(input_data):
    """运行大语言模型应用主流程，直接返回模型回复文本"""
    try:
        # 1. 初始化模块
        api_key = input_data.get("api_key", "")
        model_url = input_data.get("model_url", "https://api.deepseek.com/v1/chat/completions")
        llm_service = LLMService(api_key, model_url)
        stream_handler = StreamHandler(llm_service)
        preprocessor = InputPreprocessor()
        exception_handler = LLMExceptionHandler(max_retries=3, retry_delay=2)

        # 2. 输入预处理
        preprocessed_data = preprocessor.preprocess_input(input_data)

        # 转换为messages格式
        messages = [{"role": "user", "content": preprocessed_data["prompt"]}]
        if "context" in preprocessed_data:
            messages = preprocessed_data["context"] + messages

        params = preprocessed_data.get("parameters", {})

        # 3. 参数调优（可选）
        if input_data.get("tune_parameters", False):
            tuner = ParameterTuner(llm_service)
            params = tuner.recommend_parameters(messages[0]["content"], params)

        if params.get("stream", False):
            # 流式响应处理
            full_response = ""
            async for chunk in stream_handler.stream_response(messages, params):
                full_response += chunk
            # 直接返回流式拼接的完整回复
            return full_response.strip()
        else:
            # 非流式处理
            response = exception_handler.handle_api_failure(
                lambda: llm_service.call_model(messages, **params),
                params
            )
            # 直接返回模型回复内容
            return response["choices"][0]["message"]["content"].strip()

    except SecurityException as se:
        return f"安全警告: {str(se)}"
    except LLMServiceException as lse:
        return f"模型服务异常: {str(lse)}"
    except Exception as e:
        return f"应用运行错误: {str(e)}"

#测试的部分
async def main():
    sample_input = {
        "api_key": 'sk-32b705ff866949f788a2fde04f9d0fb0',
        "prompt": "what can you do?",
        "modality": "text",
        "parameters": {
            "temperature": 0.7,
            "max_tokens": 800,
            "stream": True
        }
    }
    response_text = await run_llm_application(sample_input)  # ✅ 正确：在async函数内使用await
    print(response_text)

if __name__ == "__main__":
    asyncio.run(main())  # 启动异步主函数
