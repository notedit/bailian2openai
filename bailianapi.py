

import aiohttp
from typing import List, Dict, Optional, Any


class BaiLianAdapter:
    def __init__(self, api_key: str, app_id: str):
        self.api_key = api_key
        self.app_id = app_id
        # fmt: off
        self.base_url = f"https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion"
        self.session_id: Optional[str] = None
        # fmt: on

    def _convert_messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """
        将 OpenAI 格式的消息转换为百炼的 prompt
        对于连续对话，我们只需要最后一条用户消息
        """
        # 获取最后一条用户消息
        for msg in reversed(messages):
            if msg["role"] == "user":
                return msg["content"]
        return ""

    async def create_chat_completion(
        self,
        messages: List[Dict[str, str]],
        session_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        模拟 OpenAI 的 create 方法
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # 构建请求体
        payload = {
            "input": {
                "prompt": self._convert_messages_to_prompt(messages)
            },
            "parameters": {},
            "debug": {}
        }

        # 如果存在 session_id，添加到请求中实现连续对话
        if session_id:
            payload["input"]["session_id"] = session_id

        # 发送请求
        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_url, headers=headers, json=payload) as response:
                result = await response.json()

                # 保存 session_id 用于后续对话
                if "output" in result and "session_id" in result["output"]:
                    self.session_id = result["output"]["session_id"]

                # 转换为 OpenAI 格式的响应
                return {
                    "choices": [{
                        "message": {
                            "role": "assistant",
                            "content": result.get("output", {}).get("text", "")
                        },
                        "finish_reason": result.get("output", {}).get("finish_reason", "stop")
                    }],
                    "usage": {
                        "total_tokens": sum(
                            model["input_tokens"] + model["output_tokens"]
                            for model in result.get("usage", {}).get("models", [])
                        ),
                        "prompt_tokens": sum(
                            model["input_tokens"]
                            for model in result.get("usage", {}).get("models", [])
                        ),
                        "completion_tokens": sum(
                            model["output_tokens"]
                            for model in result.get("usage", {}).get("models", [])
                        )
                    },
                    "id": result.get("request_id", ""),
                    "model": model
                }
