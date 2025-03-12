"""
DeepSeek 联网搜索示例
~~~~~~~~~~~~~~~~~

演示如何使用DeepSeek客户端的联网搜索功能。
"""

import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 加载环境变量
load_dotenv()

from deepseek.client import DeepSeekClient

def main():
    # 从环境变量获取API密钥
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("错误: 未设置DEEPSEEK_API_KEY环境变量")
        print("请在.env文件中设置DEEPSEEK_API_KEY或直接传入API密钥")
        return

    # 初始化客户端
    client = DeepSeekClient(api_key=api_key)
    
    print("DeepSeek 联网搜索示例")
    print("-" * 50)
    
    # 设置系统消息
    system_message = "你是DeepSeek AI助手，一个由DeepSeek开发的大型语言模型。请提供有帮助、安全和准确的回答。"
    
    # 准备一个需要最新信息的问题
    current_events_question = "最近有哪些重要的AI研究突破或技术进展？请提供具体的研究成果和发布时间。"
    
    print(f"问题: {current_events_question}")
    print("\n1. 普通模式回答 (仅基于训练数据):")
    
    # 普通模式回答
    try:
        response_normal = client.chat(current_events_question, system_message=system_message)
        print(f"\n{response_normal}")
    except Exception as e:
        print(f"\n错误: {str(e)}")
    
    # 清除对话历史
    client.clear_conversation()
    
    print("\n" + "-" * 50)
    print("\n2. 联网搜索模式回答 (可获取最新信息):")
    
    # 启用联网搜索模式
    client.enable_web_search()
    
    # 联网搜索模式回答
    try:
        response_web = client.chat(current_events_question, system_message=system_message)
        print(f"\n{response_web}")
    except Exception as e:
        print(f"\n错误: {str(e)}")
    
    print("\n" + "-" * 50)
    print("\n对比两种模式的回答，可以看出联网搜索模式能够提供更新、更准确的信息。")

if __name__ == "__main__":
    main() 