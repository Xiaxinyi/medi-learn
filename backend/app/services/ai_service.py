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

        return await AIService._call_ai(system_prompt, user_prompt)

    @staticmethod
    async def generate_question_info(topic: str) -> dict:
        """根据题目主题调用AI生成完整试题"""
        if not settings.OPENAI_API_KEY:
            raise ValueError("AI服务未配置，请设置 OPENAI_API_KEY")

        system_prompt = (
            "你是一位中医考试命题专家。请根据给定的知识点主题，生成一道高质量的中医考试题目。"
            "必须以JSON格式返回，不要包含任何其他说明文字。"
        )

        user_prompt = (
            f'请为主题"{topic}"生成一道中医考试题。以JSON格式返回，字段要求如下：\n'
            f'- content: 题目内容（字符串，清晰的题干）\n'
            f'- type: 题型，"single"（单选）或"multiple"（多选）\n'
            f'- options: 选项数组，固定4个选项，每个选项包含：\n'
            f'  - option_key: 选项标识，依次为 "A"、"B"、"C"、"D"\n'
            f'  - content: 选项内容（字符串）\n'
            f'  - is_correct: 是否正确（布尔值）\n'
            f'  - sort_order: 排序，依次为 0、1、2、3\n'
            f'- explanation: 答案解析（字符串，详细说明为什么选这个答案）\n'
            f'- difficulty: 难度，从 "easy"（简单）、"medium"（中等）、"hard"（困难）中选择\n'
            f'- tags: 标签数组（字符串数组，如 ["解表药","清热药"]）\n'
            f'\n要求：\n'
            f'1. 单选题必须有且仅有1个正确答案\n'
            f'2. 多选题必须有2-3个正确答案\n'
            f'3. 选项内容要有区分度，不能过于简单\n'
            f'4. 解析要专业、详细\n'
            f'\n只返回纯JSON对象，不要markdown代码块，不要其他说明。'
        )

        return await AIService._call_ai(system_prompt, user_prompt)

    @staticmethod
    async def _call_ai(system_prompt: str, user_prompt: str) -> dict:
        """调用AI API的通用方法"""
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
