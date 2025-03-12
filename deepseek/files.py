"""
DeepSeek 文件处理
~~~~~~~~~~~~~

处理文件上传和管理，支持向DeepSeek API提交文件以供分析。
"""

import os
import mimetypes
from typing import Dict, Any, Optional, List, Union, BinaryIO
import requests
from tqdm import tqdm


class FileManager:
    """DeepSeek文件管理类"""

    def __init__(self, api_key: str, base_url: str, timeout: int = 30):
        """
        初始化文件管理器

        Args:
            api_key: DeepSeek API密钥
            base_url: API基础URL
            timeout: 请求超时时间（秒）
        """
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.files_endpoint = f"{self.base_url}/v1/files"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

    def upload_file(self, file_path: str, purpose: str = "assistants") -> str:
        """
        上传文件到DeepSeek API

        Args:
            file_path: 文件路径
            purpose: 文件用途，默认为"assistants"

        Returns:
            上传成功后的文件ID
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")

        # 获取文件大小和MIME类型
        file_size = os.path.getsize(file_path)
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = "application/octet-stream"

        # 打开文件并上传
        with open(file_path, "rb") as file:
            # 使用tqdm显示上传进度
            with tqdm(total=file_size, unit="B", unit_scale=True, desc=f"上传 {os.path.basename(file_path)}") as pbar:
                # 创建一个包装器来跟踪上传进度
                file_wrapper = self._create_file_wrapper(file, pbar)
                
                # 准备上传请求
                files = {
                    "file": (os.path.basename(file_path), file_wrapper, mime_type)
                }
                data = {
                    "purpose": purpose
                }
                
                # 发送上传请求
                response = requests.post(
                    self.files_endpoint,
                    headers=self.headers,
                    files=files,
                    data=data,
                    timeout=self.timeout
                )
                
                # 检查响应
                if response.status_code != 200:
                    error_msg = f"文件上传失败: {response.status_code} - {response.text}"
                    raise Exception(error_msg)
                
                # 解析响应获取文件ID
                response_data = response.json()
                file_id = response_data.get("id")
                if not file_id:
                    raise Exception("上传成功但未返回文件ID")
                
                return file_id

    def _create_file_wrapper(self, file: BinaryIO, progress_bar: tqdm) -> BinaryIO:
        """
        创建一个文件包装器来跟踪上传进度

        Args:
            file: 原始文件对象
            progress_bar: 进度条对象

        Returns:
            包装后的文件对象
        """
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        # 创建一个包装器类
        class FileWrapper:
            def __init__(self, file, progress_bar):
                self.file = file
                self.progress_bar = progress_bar
                self.bytes_read = 0
                
            def read(self, size=-1):
                data = self.file.read(size)
                self.bytes_read += len(data)
                self.progress_bar.update(len(data))
                return data
                
            def __getattr__(self, attr):
                return getattr(self.file, attr)
        
        return FileWrapper(file, progress_bar)

    def list_files(self) -> List[Dict[str, Any]]:
        """
        列出所有上传的文件

        Returns:
            文件列表
        """
        response = requests.get(
            self.files_endpoint,
            headers=self.headers,
            timeout=self.timeout
        )
        
        if response.status_code != 200:
            error_msg = f"获取文件列表失败: {response.status_code} - {response.text}"
            raise Exception(error_msg)
        
        response_data = response.json()
        return response_data.get("data", [])

    def get_file(self, file_id: str) -> Dict[str, Any]:
        """
        获取文件信息

        Args:
            file_id: 文件ID

        Returns:
            文件信息
        """
        response = requests.get(
            f"{self.files_endpoint}/{file_id}",
            headers=self.headers,
            timeout=self.timeout
        )
        
        if response.status_code != 200:
            error_msg = f"获取文件信息失败: {response.status_code} - {response.text}"
            raise Exception(error_msg)
        
        return response.json()

    def delete_file(self, file_id: str) -> bool:
        """
        删除文件

        Args:
            file_id: 文件ID

        Returns:
            是否删除成功
        """
        response = requests.delete(
            f"{self.files_endpoint}/{file_id}",
            headers=self.headers,
            timeout=self.timeout
        )
        
        if response.status_code != 200:
            error_msg = f"删除文件失败: {response.status_code} - {response.text}"
            raise Exception(error_msg)
        
        return True 