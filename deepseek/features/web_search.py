"""
DeepSeek 联网搜索功能
~~~~~~~~~~~~~~~~~

实现DeepSeek的联网搜索功能，使模型能够获取互联网上的最新信息。
"""

from typing import Dict, Any, Optional, List


class WebSearch:
    """DeepSeek联网搜索功能类"""

    def __init__(self, enabled: bool = False):
        """
        初始化联网搜索功能

        Args:
            enabled: 是否启用联网搜索
        """
        self.enabled = enabled

    def enable(self):
        """启用联网搜索功能"""
        self.enabled = True

    def disable(self):
        """禁用联网搜索功能"""
        self.enabled = False

    def is_enabled(self) -> bool:
        """
        检查联网搜索功能是否启用

        Returns:
            是否启用联网搜索
        """
        return self.enabled

    def apply_to_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        将联网搜索功能应用到消息中

        Args:
            messages: 原始消息列表

        Returns:
            应用联网搜索后的消息列表
        """
        if not self.enabled:
            return messages

        # 联网搜索模式下，在系统消息中添加指令
        system_message_found = False
        web_search_instruction = (
            "你可以搜索互联网获取最新信息来回答问题。当需要事实性信息、"
            "最新数据或特定知识时，请主动使用搜索功能。在回答中，请引用"
            "你从搜索中获取的信息来源。"
        )

        modified_messages = []
        for message in messages:
            if message["role"] == "system":
                # 修改现有的系统消息
                system_message_found = True
                content = message["content"]
                if web_search_instruction not in content:
                    message["content"] = f"{content}\n\n{web_search_instruction}"
            modified_messages.append(message)

        # 如果没有系统消息，添加一个
        if not system_message_found:
            modified_messages.insert(0, {
                "role": "system",
                "content": web_search_instruction
            })

        return modified_messages

    def apply_to_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        将联网搜索功能应用到API参数中

        Args:
            params: 原始API参数

        Returns:
            应用联网搜索后的API参数
        """
        if not self.enabled:
            return params

        # 联网搜索模式下，添加相关参数
        modified_params = params.copy()
        
        # 添加web_search参数，告知API启用联网搜索
        modified_params["web_search"] = True
        
        # 可能需要其他特定参数，根据DeepSeek API的实际要求添加
        # 例如搜索引擎选择、搜索结果数量限制等
        
        return modified_params 