"""
DeepSeek 核心客户端
~~~~~~~~~~~~~~~

提供与DeepSeek API交互的核心功能，整合深度思考、联网搜索、对话和文件处理等功能。
"""

import json
from typing import Dict, Any, Optional, List, Union

import requests
from openai import OpenAI

from .config import DeepSeekConfig
from .conversation import Conversation
from .features.deep_thinking import DeepThinking
from .features.web_search import WebSearch
from .files import FileManager


class DeepSeekClient:
    """DeepSeek API客户端"""

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
        初始化DeepSeek客户端

        Args:
            api_key: DeepSeek API密钥
            base_url: API基础URL
            model: 使用的模型名称
            timeout: API请求超时时间（秒）
            deep_thinking: 是否启用深度思考
            web_search: 是否启用联网搜索
        """
        # 初始化配置
        self.config = DeepSeekConfig(
            api_key=api_key,
            base_url=base_url,
            model=model,
            timeout=timeout,
            deep_thinking=deep_thinking,
            web_search=web_search,
        )
        
        # 初始化功能模块
        self.deep_thinking = DeepThinking(enabled=self.config.deep_thinking)
        self.web_search = WebSearch(enabled=self.config.web_search)
        
        # 初始化对话管理
        self.conversation = Conversation()
        
        # 初始化文件管理
        self.file_manager = FileManager(
            api_key=self.config.api_key,
            base_url=self.config.base_url,
            timeout=self.config.timeout
        )
        
        # 初始化OpenAI兼容客户端
        self.client = OpenAI(
            api_key=self.config.api_key,
            base_url=self.config.base_url
        )

    def enable_deep_thinking(self) -> None:
        """启用深度思考功能"""
        self.deep_thinking.enable()

    def disable_deep_thinking(self) -> None:
        """禁用深度思考功能"""
        self.deep_thinking.disable()

    def enable_web_search(self) -> None:
        """启用联网搜索功能"""
        self.web_search.enable()

    def disable_web_search(self) -> None:
        """禁用联网搜索功能"""
        self.web_search.disable()

    def chat(
        self,
        message: str,
        system_message: Optional[str] = None,
        file_ids: Optional[List[str]] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> str:
        """
        与DeepSeek进行对话

        Args:
            message: 用户消息
            system_message: 系统消息，用于设置对话的上下文和指导模型行为
            file_ids: 文件ID列表，用于引用上传的文件
            temperature: 温度参数，控制回答的随机性
            max_tokens: 生成的最大token数
            stream: 是否使用流式响应
            **kwargs: 其他参数

        Returns:
            DeepSeek的回答
        """
        # 如果提供了系统消息，更新对话中的系统消息
        if system_message:
            self.conversation.add_system_message(system_message)
            
        # 添加用户消息到对话
        self.conversation.add_user_message(message)
        
        # 准备API调用参数
        params = {
            "model": self.config.model,
            "temperature": temperature,
            **kwargs
        }
        
        # 如果指定了max_tokens，添加到参数中
        if max_tokens:
            params["max_tokens"] = max_tokens
            
        # 如果提供了文件ID，添加到参数中
        if file_ids:
            params["file_ids"] = file_ids
            
        # 获取消息列表
        messages = self.conversation.get_messages()
        
        # 应用深度思考功能
        messages = self.deep_thinking.apply_to_messages(messages)
        params = self.deep_thinking.apply_to_params(params)
        
        # 应用联网搜索功能
        messages = self.web_search.apply_to_messages(messages)
        params = self.web_search.apply_to_params(params)
        
        # 调用API
        if stream:
            # 流式响应处理
            response_text = self._handle_streaming_response(messages, params)
        else:
            # 普通响应处理
            response_text = self._handle_normal_response(messages, params)
            
        # 添加助手回答到对话
        self.conversation.add_assistant_message(response_text)
        
        return response_text

    def _handle_normal_response(self, messages: List[Dict[str, str]], params: Dict[str, Any]) -> str:
        """
        处理普通（非流式）API响应

        Args:
            messages: 消息列表
            params: API参数

        Returns:
            模型回答的文本
        """
        try:
            response = self.client.chat.completions.create(
                messages=messages,
                **params
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            error_msg = f"API调用失败: {str(e)}"
            raise Exception(error_msg)

    def _handle_streaming_response(self, messages: List[Dict[str, str]], params: Dict[str, Any]) -> str:
        """
        处理流式API响应

        Args:
            messages: 消息列表
            params: API参数

        Returns:
            模型回答的文本
        """
        try:
            # 确保启用流式响应
            params["stream"] = True
            
            # 调用流式API
            response_stream = self.client.chat.completions.create(
                messages=messages,
                **params
            )
            
            # 收集流式响应的内容
            collected_content = ""
            for chunk in response_stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content_chunk = chunk.choices[0].delta.content
                    collected_content += content_chunk
                    # 可以在这里添加实时输出，例如：print(content_chunk, end="", flush=True)
                    
            return collected_content
        except Exception as e:
            error_msg = f"流式API调用失败: {str(e)}"
            raise Exception(error_msg)

    def upload_file(self, file_path: str, purpose: str = "assistants") -> str:
        """
        上传文件

        Args:
            file_path: 文件路径
            purpose: 文件用途

        Returns:
            文件ID
        """
        return self.file_manager.upload_file(file_path, purpose)

    def list_files(self) -> List[Dict[str, Any]]:
        """
        列出所有上传的文件

        Returns:
            文件列表
        """
        return self.file_manager.list_files()

    def get_file(self, file_id: str) -> Dict[str, Any]:
        """
        获取文件信息

        Args:
            file_id: 文件ID

        Returns:
            文件信息
        """
        return self.file_manager.get_file(file_id)

    def delete_file(self, file_id: str) -> bool:
        """
        删除文件

        Args:
            file_id: 文件ID

        Returns:
            是否删除成功
        """
        return self.file_manager.delete_file(file_id)

    def clear_conversation(self, keep_system_message: bool = True) -> None:
        """
        清除对话历史

        Args:
            keep_system_message: 是否保留系统消息
        """
        self.conversation.clear_messages(keep_system_message)

    def get_conversation_messages(self) -> List[Dict[str, str]]:
        """
        获取对话历史

        Returns:
            对话消息列表
        """
        return self.conversation.get_messages() 