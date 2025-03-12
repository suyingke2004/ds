"""
DeepSeek Python 客户端
~~~~~~~~~~~~~~~~~~~~~

一个用于访问DeepSeek API的Python客户端，具有结构清晰、易于维护和良好的可扩展性。

:copyright: (c) 2023 by DeepSeek Client Developer.
:license: MIT, see LICENSE for more details.
"""

from .client import DeepSeekClient
from .config import DeepSeekConfig

__version__ = '0.1.0'
__all__ = ['DeepSeekClient', 'DeepSeekConfig'] 