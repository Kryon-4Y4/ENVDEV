"""环境配置 —— 从 .env 文件加载 LLM API 密钥等敏感信息。

用法：
    from envdev.config import settings

    # 获取 API key
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    # 如果 key 未设置，settings 会抛出清晰的错误提示
"""

import os
from functools import lru_cache

from dotenv import load_dotenv

# 加载 .env → os.environ，后续 os.getenv 可直接读取
load_dotenv()


class Settings:
    """应用配置，从环境变量 / .env 文件读取。"""

    # --- Anthropic Claude ---
    ANTHROPIC_API_KEY: str | None = os.getenv("ANTHROPIC_API_KEY")
    ANTHROPIC_BASE_URL: str | None = os.getenv("ANTHROPIC_BASE_URL")

    # --- OpenAI ---
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    OPENAI_BASE_URL: str | None = os.getenv("OPENAI_BASE_URL")

    # --- DeepSeek ---
    DEEPSEEK_API_KEY: str | None = os.getenv("DEEPSEEK_API_KEY")

    # --- 通用配置 ---
    LLM_MODEL: str = os.getenv("LLM_MODEL", "deepseek-chat")

    def require(self, key: str) -> str:
        """获取必填配置，缺失时抛出清晰错误。"""
        value = getattr(self, key, None)
        if not value:
            raise ValueError(
                f"缺少 {key}，请在 .env 文件中设置（参考 .env.example）"
            )
        return value


@lru_cache
def get_settings() -> Settings:
    """获取单例配置对象（lru_cache 保证只创建一次）。"""
    return Settings()


# 模块级单例 —— 项目各处统一引用 settings 即可
settings = get_settings()