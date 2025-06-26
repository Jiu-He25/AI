import aiohttp
import json
import asyncio


class StreamHandler:
    def __init__(self, llm_service):
        self.llm_service = llm_service

    async def stream_response(self, messages, params):
        """实现流式响应处理"""
        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": params.get("temperature", 0.7),
            "max_tokens": params.get("max_tokens", 512),
            "stream": True  # 启用流式输出
        }

        try:
            # 异步请求
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        self.llm_service.model_url,
                        headers=self.llm_service.headers,
                        json=payload
                ) as response:

                    if response.status == 200:
                        # 逐块解析流式输出
                        async for line in response.content:
                            line = line.decode('utf-8').strip()
                            if line.startswith("data: ") and not line.startswith("data: [DONE]"):
                                data = line[6:]
                                try:
                                    parsed = json.loads(data)
                                    content = parsed["choices"][0]["delta"].get("content", "")
                                    if content:
                                        yield content  # 逐块生成内容
                                        await asyncio.sleep(0.01)  # 控制输出速度
                                except json.JSONDecodeError:
                                    continue
                    else:
                        error_text = await response.text()
                        yield f"[错误: {response.status}] {error_text}"

        except Exception as e:
            yield f"[错误: {str(e)}]"