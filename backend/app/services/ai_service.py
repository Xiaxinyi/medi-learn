import httpx
import json
from app.config import settings


class AIService:
    @staticmethod
    async def generate_herb_info(name: str, categories: list[str]) -> dict:
        """根据草药名称调用AI生成详细信息"""
        if not settings.OPENAI_API_KEY:
            raise ValueError("AI服务未配置，请设置 OPENAI_API_KEY")

        system_prompt = (
            "你是一位中医专家。请根据给定的草药名称，生成该草药的详细信息。"
            "必须以JSON格式返回，不要包含任何其他说明文字。"
        )

        user_prompt = (
            f'请为草药"{name}"生成详细信息。以JSON格式返回，字段要求如下：\n'
            f'- latin_name: 拉丁学名（字符串）\n'
            f'- aliases: 别名列表（字符串数组，如["棒槌","地精"]）\n'
            f'- category: 分类，必须从以下列表中严格选择：{categories}\n'
            f'- efficacy: 功效（字符串，简要描述）\n'
            f'- indications: 主治（字符串，简要描述）\n'
            f'- dosage: 用量用法（字符串，如"3-9g，煎服"）\n'
            f'- contraindications: 禁忌（字符串，如"实热证忌用"，没有则填"暂无"）\n'
            f'- origin: 主要产地（字符串，如"吉林、辽宁"）\n'
            f'\n只返回纯JSON对象，不要markdown代码块，不要其他说明。'
        )

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{settings.OPENAI_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": settings.OPENAI_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": 0.3,
                },
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]

            # 清理可能的 markdown 代码块
            content = content.strip()
            if content.startswith("```"):
                content = content.split("\n", 1)[1] if "\n" in content else content
            if content.endswith("```"):
                content = content.rsplit("\n", 1)[0] if "\n" in content else content
            content = content.strip()

            result = json.loads(content)
            return result
