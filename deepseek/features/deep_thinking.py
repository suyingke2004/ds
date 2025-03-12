"""
DeepSeek 深度思考功能
~~~~~~~~~~~~~~~~~

实现DeepSeek的深度思考功能，使模型能够进行更深入的分析和推理。
"""

from typing import Dict, Any, Optional, List


class DeepThinking:
    """DeepSeek深度思考功能类"""

    def __init__(self, enabled: bool = False):
        """
        初始化深度思考功能

        Args:
            enabled: 是否启用深度思考
        """
        self.enabled = enabled

    def enable(self):
        """启用深度思考功能"""
        self.enabled = True

    def disable(self):
        """禁用深度思考功能"""
        self.enabled = False

    def is_enabled(self) -> bool:
        """
        检查深度思考功能是否启用

        Returns:
            是否启用深度思考
        """
        return self.enabled

    def apply_to_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        将深度思考功能应用到消息中

        Args:
            messages: 原始消息列表

        Returns:
            应用深度思考后的消息列表
        """
        if not self.enabled:
            return messages

        # 深度思考模式下，在系统消息中添加指令
        system_message_found = False
        deep_thinking_instruction = (
            "请进行深度思考，分析问题的各个方面，考虑不同的观点和可能性，"
            "提供深入的见解和全面的回答。在回答前，请先思考问题的本质、"
            "相关因素、潜在影响和可能的解决方案。"
        )

        modified_messages = []
        for message in messages:
            if message["role"] == "system":
                # 修改现有的系统消息
                system_message_found = True
                content = message["content"]
                if deep_thinking_instruction not in content:
                    message["content"] = f"{content}\n\n{deep_thinking_instruction}"
            modified_messages.append(message)

        # 如果没有系统消息，添加一个
        if not system_message_found:
            modified_messages.insert(0, {
                "role": "system",
                "content": deep_thinking_instruction
            })

        return modified_messages

    def apply_to_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        将深度思考功能应用到API参数中

        Args:
            params: 原始API参数

        Returns:
            应用深度思考后的API参数
        """
        if not self.enabled:
            return params

        # 深度思考模式下，可以调整模型参数
        modified_params = params.copy()
        
        # 增加temperature以鼓励更多样化的思考
        if "temperature" in modified_params:
            # 适度增加temperature，但不超过1.0
            modified_params["temperature"] = min(modified_params["temperature"] * 1.2, 1.0)
        else:
            modified_params["temperature"] = 0.8
            
        # 增加max_tokens以允许更长的回答
        if "max_tokens" in modified_params:
            # 增加max_tokens，但不超过模型限制
            modified_params["max_tokens"] = int(modified_params["max_tokens"] * 1.5)
        
        return modified_params 