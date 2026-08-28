"""环境配置 —— 从 .env 文件加载 LLM API 密钥等敏感信息。

用法：
    from envdev.config import settings

    # 获取 API key
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    # 如果 key 未设置，settings 会抛出清晰的错误提示
"""

import os
import sys
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

# 加载 .env → os.environ，后续 os.getenv 可直接读取
# 打包模式：定位配置目录后读其中的 .env（双击启动时 cwd 不可控）；开发模式：默认从 cwd 查找，行为不变
def _config_dir() -> str:
    """配置目录定位：默认 = 可执行文件同目录；若身处 macOS .app 包内，跳到 .app 所在目录。"""
    base = Path(sys.executable).resolve().parent
    # 找出 .app 包目录（如 ENVDEV.app），跳到其所在目录（目录名以 .app 结尾）
    app_idx = next((i for i, p in enumerate(base.parts) if p.endswith(".app")), None)
    if app_idx is not None:
        base = Path(*base.parts[: app_idx + 1]).parent
    return str(base)


if getattr(sys, "frozen", False):
    load_dotenv(os.path.join(_config_dir(), ".env"))
else:
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