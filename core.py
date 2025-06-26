# core.py
import asyncio
from llm_service import LLMService
from processor import InputPreprocessor, SecurityException
from exception_handler import LLMExceptionHandler, LLMServiceException
from parameter_tuner import ParameterTuner
from stream_handler import StreamHandler
import json

# 修改run_llm_application为同步函数
def run_llm_application(input_data):
    try:
        # 同步实现（原异步逻辑改为同步）
        llm_service = LLMService(input_data.get("api_key", ""))
        response = llm_service.call_model(
            [{"role": "user", "content": input_data["prompt"]}],
            **input_data.get("parameters", {})
        )
        return {"status": "success", "response": response}
    except Exception as e:
        return {"status": "error", "message": str(e)}