"""核心包 —— 再导出核心函数，各端统一写 from envdev.core import ... 即可。"""

from envdev.core.core import build_system_prompt, chat

__all__ = ["build_system_prompt", "chat"]
