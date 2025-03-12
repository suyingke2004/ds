"""
DeepSeek 文件上传示例
~~~~~~~~~~~~~~~~~

演示如何使用DeepSeek客户端上传文件并基于文件内容进行对话。
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
    
    print("DeepSeek 文件上传示例")
    print("-" * 50)
    
    # 设置系统消息
    system_message = "你是DeepSeek AI助手，一个由DeepSeek开发的大型语言模型。请提供有帮助、安全和准确的回答。"
    
    # 获取文件路径
    file_path = input("请输入要上传的文件路径: ")
    
    if not os.path.exists(file_path):
        print(f"错误: 文件不存在: {file_path}")
        return
        
    print(f"\n正在上传文件: {file_path}")
    
    try:
        # 上传文件
        file_id = client.upload_file(file_path)
        print(f"文件上传成功，ID: {file_id}")
        
        # 获取文件信息
        file_info = client.get_file(file_id)
        print(f"\n文件信息:")
        print(f"- 名称: {file_info.get('filename', 'N/A')}")
        print(f"- 大小: {file_info.get('bytes', 0)} 字节")
        print(f"- 类型: {file_info.get('purpose', 'N/A')}")
        print(f"- 创建时间: {file_info.get('created_at', 'N/A')}")
        
        # 基于文件内容提问
        print("\n现在您可以基于上传的文件内容提问")
        
        while True:
            # 获取用户输入
            user_input = input("\n问题 (输入'exit'退出): ")
            
            # 检查是否退出
            if user_input.lower() in ["exit", "quit", "退出"]:
                break
                
            # 发送消息到DeepSeek，包含文件引用
            try:
                response = client.chat(
                    user_input,
                    system_message=system_message,
                    file_ids=[file_id]
                )
                print(f"\nDeepSeek: {response}")
            except Exception as e:
                print(f"\n错误: {str(e)}")
        
        # 询问是否删除文件
        delete_file = input("\n是否删除上传的文件? (y/n): ")
        if delete_file.lower() in ["y", "yes"]:
            client.delete_file(file_id)
            print(f"文件已删除: {file_id}")
        
    except Exception as e:
        print(f"\n错误: {str(e)}")

if __name__ == "__main__":
    main() 