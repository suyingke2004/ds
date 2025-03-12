"""
DeepSeek 对话管理
~~~~~~~~~~~~~

管理与DeepSeek的对话，包括消息历史记录和上下文处理。
"""

from typing import Dict, Any, Optional, List, Union


class Conversation:
    """DeepSeek对话管理类"""

    def __init__(self, system_message: Optional[str] = None):
        """
        初始化对话

        Args:
            system_message: 系统消息，用于设置对话的上下文和指导模型行为
        """
        self.messages = []
        if system_message:
            self.add_system_message(system_message)

    def add_system_message(self, content: str) -> None:
        """
        添加系统消息

        Args:
            content: 消息内容
        """
        # 检查是否已有系统消息
        for i, message in enumerate(self.messages):
            if message["role"] == "system":
                # 更新现有的系统消息
                self.messages[i] = {"role": "system", "content": content}
                return

        # 如果没有系统消息，添加一个
        self.messages.insert(0, {"role": "system", "content": content})

    def add_user_message(self, content: str) -> None:
        """
        添加用户消息

        Args:
            content: 消息内容
        """
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str) -> None:
        """
        添加助手消息

        Args:
            content: 消息内容
        """
        self.messages.append({"role": "assistant", "content": content})

    def get_messages(self) -> List[Dict[str, str]]:
        """
        获取所有消息

        Returns:
            消息列表
        """
        return self.messages

    def clear_messages(self, keep_system_message: bool = True) -> None:
        """
        清除消息历史

        Args:
            keep_system_message: 是否保留系统消息
        """
        if keep_system_message:
            # 保留系统消息
            system_messages = [m for m in self.messages if m["role"] == "system"]
            self.messages = system_messages
        else:
            # 清除所有消息
            self.messages = []

    def get_last_user_message(self) -> Optional[str]:
        """
        获取最后一条用户消息

        Returns:
            最后一条用户消息的内容，如果没有则返回None
        """
        for message in reversed(self.messages):
            if message["role"] == "user":
                return message["content"]
        return None

    def get_last_assistant_message(self) -> Optional[str]:
        """
        获取最后一条助手消息

        Returns:
            最后一条助手消息的内容，如果没有则返回None
        """
        for message in reversed(self.messages):
            if message["role"] == "assistant":
                return message["content"]
        return None

    def truncate_messages(self, max_messages: int = 10) -> None:
        """
        截断消息历史，保留最近的消息

        Args:
            max_messages: 保留的最大消息数量
        """
        if len(self.messages) <= max_messages:
            return

        # 保留系统消息
        system_messages = [m for m in self.messages if m["role"] == "system"]
        
        # 获取非系统消息
        non_system_messages = [m for m in self.messages if m["role"] != "system"]
        
        # 保留最近的非系统消息
        recent_non_system_messages = non_system_messages[-max_messages + len(system_messages):]
        
        # 合并系统消息和最近的非系统消息
        self.messages = system_messages + recent_non_system_messages 