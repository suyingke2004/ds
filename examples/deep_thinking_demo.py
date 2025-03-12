"""
DeepSeek 深度思考示例
~~~~~~~~~~~~~~~~~

演示如何使用DeepSeek客户端的深度思考功能。
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
    
    print("DeepSeek 深度思考示例")
    print("-" * 50)
    
    # 设置系统消息
    system_message = "你是DeepSeek AI助手，一个由DeepSeek开发的大型语言模型。请提供有帮助、安全和准确的回答。"
    
    # 准备一个需要深入思考的问题
    complex_question = "人工智能可能对未来社会产生哪些深远影响？请从经济、就业、教育、伦理等多个角度分析。"
    
    print(f"问题: {complex_question}")
    print("\n1. 普通模式回答:")
    
    # 普通模式回答
    try:
        response_normal = client.chat(complex_question, system_message=system_message)
        print(f"\n{response_normal}")
    except Exception as e:
        print(f"\n错误: {str(e)}")
    
    # 清除对话历史
    client.clear_conversation()
    
    print("\n" + "-" * 50)
    print("\n2. 深度思考模式回答:")
    
    # 启用深度思考模式
    client.enable_deep_thinking()
    
    # 深度思考模式回答
    try:
        response_deep = client.chat(complex_question, system_message=system_message)
        print(f"\n{response_deep}")
    except Exception as e:
        print(f"\n错误: {str(e)}")
    
    print("\n" + "-" * 50)
    print("\n对比两种模式的回答，可以看出深度思考模式提供了更全面、深入的分析。")

if __name__ == "__main__":
    main() 