import requests
import json
import time
import numpy as np
from jsonschema import validate, ValidationError


class LLMService:
    def __init__(self, api_key, model_url="https://api.deepseek.com/v1/chat/completions"):
        self.api_key = api_key
        self.model_url = model_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def call_model(self, messages, temperature=0.7, max_tokens=1024, stream=False):
        """调用大语言模型并返回结果"""
        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }

        try:
            response = requests.post(
                self.model_url,
                headers=self.headers,
                data=json.dumps(payload)
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"模型调用错误: {e}")
            return None