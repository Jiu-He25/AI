import time
import json
from jsonschema import validate, ValidationError


class LLMServiceException(Exception):
    pass


class LLMExceptionHandler:
    def __init__(self, max_retries=3, retry_delay=2, fallback_model="gpt-3.5-turbo"):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.fallback_model = fallback_model

    def handle_api_failure(self, call_function, original_params):
        """处理API调用失败（网络错误、限流等）"""
        retries = 0
        last_exception = None
        while retries < self.max_retries:
            try:
                print(f"API调用失败，重试 {retries + 1}/{self.max_retries}...")
                time.sleep(self.retry_delay * (2 ** retries))  # 指数退避

                # 可选：降级到备用模型
                if retries == self.max_retries - 1 and "model" in original_params:
                    original_params["model"] = self.fallback_model

                # 重新调用模型
                response = call_function()
                # 检查响应是否有效
                if not response or "choices" not in response:
                    raise LLMServiceException(f"无效的模型响应: {response}")

                return response

            except Exception as e:
                last_exception = e
                print(f"API调用失败: {str(e)}")
                retries += 1

                # 所有重试都失败
            if last_exception:
                raise LLMServiceException(f"所有重试失败: {str(last_exception)}") from last_exception
            else:
                raise LLMServiceException("API调用失败，原因未知")

    def handle_structured_output_failure(self, response_text, expected_schema):
        """处理结构化输出失败（如JSON解析错误）"""
        try:
            # 尝试解析结构化输出
            data = json.loads(response_text)
            # 验证是否符合预期Schema
            validate(instance=data, schema=expected_schema)
            return data
        except (json.JSONDecodeError, ValidationError) as e:
            # 结构化输出失败处理策略
            print(f"结构化输出解析失败: {str(e)}")

            # 策略1：提示模型重新生成结构化输出
            fixed_prompt = f"请重新生成符合以下JSON格式的响应: {json.dumps(expected_schema)}\n原响应: {response_text}"
            messages = [{"role": "user", "content": fixed_prompt}]

            # 假设llm_service已在上下文初始化
            from llm_service import LLMService
            # 这里简化处理，实际应从上下文获取llm_service实例
            llm_service = LLMService(api_key="temp_key")
            fixed_response = llm_service.call_model(messages, temperature=0.2)

            if fixed_response and "choices" in fixed_response:
                fixed_text = fixed_response["choices"][0]["message"]["content"]
                try:
                    # 再次尝试解析
                    return json.loads(fixed_text)
                except json.JSONDecodeError:
                    # 策略2：手动提取关键信息（保底方案）
                    return self._extract_info_manually(fixed_text, expected_schema)
            else:
                return {"error": "无法生成有效的结构化响应", "original_response": response_text}

    def _extract_info_manually(self, text, schema):
        """从非结构化文本中手动提取信息（保底方案）"""
        # 简单示例：提取文本中的数字和关键短语
        # 实际应用中应根据具体schema设计更复杂的提取逻辑
        extracted = {"extracted_info": text[:200]}  # 默认截取前200个字符
        return extracted