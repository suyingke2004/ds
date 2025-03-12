"""
DeepSeek 配置管理
~~~~~~~~~~~~~~

管理DeepSeek客户端的配置选项，包括API密钥、基础URL、模型选择等。
"""

import os
from typing import Optional
from dotenv import load_dotenv

# 尝试加载.env文件中的环境变量
load_dotenv()


class DeepSeekConfig:
    """DeepSeek客户端配置类"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: Optional[int] = None,
        deep_thinking: Optional[bool] = None,
        web_search: Optional[bool] = None,
    ):
        """
        初始化DeepSeek配置

        Args:
            api_key: DeepSeek API密钥
            base_url: API基础URL
            model: 使用的模型名称
            timeout: API请求超时时间（秒）
            deep_thinking: 是否启用深度思考
            web_search: 是否启用联网搜索
        """
        # 优先使用传入的参数，其次使用环境变量，最后使用默认值
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("API密钥未提供。请通过参数传入或在环境变量中设置DEEPSEEK_API_KEY。")

        self.base_url = base_url or os.getenv("DEEPSEEK_API_BASE_URL", "https://api.deepseek.com")
        self.model = model or os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        
        # 转换timeout为整数
        timeout_str = os.getenv("API_TIMEOUT", "30") if timeout is None else str(timeout)
        try:
            self.timeout = int(timeout_str)
        except ValueError:
            self.timeout = 30
            
        # 转换布尔值配置
        self.deep_thinking = self._parse_bool(deep_thinking, "DEEP_THINKING_ENABLED", False)
        self.web_search = self._parse_bool(web_search, "WEB_SEARCH_ENABLED", False)

    def _parse_bool(self, value: Optional[bool], env_var: str, default: bool) -> bool:
        """
        解析布尔值配置，优先使用传入的参数，其次使用环境变量，最后使用默认值

        Args:
            value: 传入的布尔值
            env_var: 环境变量名
            default: 默认值

        Returns:
            解析后的布尔值
        """
        if value is not None:
            return value
            
        env_value = os.getenv(env_var)
        if env_value is not None:
            return env_value.lower() in ("true", "1", "yes", "y", "t")
            
        return default

    def to_dict(self) -> dict:
        """
        将配置转换为字典

        Returns:
            包含配置的字典
        """
        return {
            "api_key": self.api_key,
            "base_url": self.base_url,
            "model": self.model,
            "timeout": self.timeout,
            "deep_thinking": self.deep_thinking,
            "web_search": self.web_search,
        }

    def __repr__(self) -> str:
        """返回配置的字符串表示，隐藏API密钥"""
        config_dict = self.to_dict()
        # 隐藏API密钥
        if config_dict["api_key"]:
            config_dict["api_key"] = f"{config_dict['api_key'][:4]}...{config_dict['api_key'][-4:]}"
        return f"DeepSeekConfig({config_dict})" 