"""
DeepSeek 基本对话示例
~~~~~~~~~~~~~~~~~

演示如何使用DeepSeek客户端进行基本对话。
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
    
    print("DeepSeek 对话示例")
    print("输入'exit'或'quit'退出")
    print("-" * 50)
    
    # 设置系统消息
    system_message = "你是DeepSeek AI助手，一个由DeepSeek开发的大型语言模型。请提供有帮助、安全和准确的回答。"
    
    # 对话循环
    while True:
        # 获取用户输入
        user_input = input("\n你: ")
        
        # 检查是否退出
        if user_input.lower() in ["exit", "quit", "退出"]:
            print("\n再见！")
            break
            
        try:
            # 发送消息到DeepSeek
            if client.conversation.get_messages():
                # 如果已经有对话历史，直接发送用户消息
                response = client.chat(user_input)
            else:
                # 首次对话，设置系统消息
                response = client.chat(user_input, system_message=system_message)
                
            # 显示回答
            print(f"\nDeepSeek: {response}")
            
        except Exception as e:
            print(f"\n错误: {str(e)}")

if __name__ == "__main__":
    main() 