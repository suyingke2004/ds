# DeepSeek Python 客户端

一个用于访问DeepSeek API的Python客户端，具有结构清晰、易于维护和良好的可扩展性。

## 功能特点

- **深度思考模式**：激活DeepSeek的深度思考能力，获得更深入的分析和回答
- **联网搜索**：允许DeepSeek在回答问题时搜索互联网获取最新信息
- **常规对话**：与DeepSeek进行自然对话交互
- **文件上传**：支持向DeepSeek提交文件以供分析和处理

## 项目结构

```
deepseek-client/
├── deepseek/                  # 主包目录
│   ├── __init__.py            # 包初始化
│   ├── client.py              # 核心客户端
│   ├── config.py              # 配置管理
│   ├── conversation.py        # 对话管理
│   ├── files.py               # 文件处理
│   └── features/              # 功能模块
│       ├── __init__.py
│       ├── deep_thinking.py   # 深度思考功能
│       └── web_search.py      # 联网搜索功能
├── examples/                  # 使用示例
│   ├── basic_conversation.py
│   ├── deep_thinking_demo.py
│   ├── web_search_demo.py
│   └── file_upload_demo.py
├── tests/                     # 测试目录
│   ├── __init__.py
│   ├── test_client.py
│   ├── test_conversation.py
│   └── test_features.py
├── .env.example               # 环境变量示例
├── requirements.txt           # 项目依赖
├── setup.py                   # 安装脚本
└── README.md                  # 项目文档
```

## 安装方法

1. 克隆此仓库:
```bash
git clone [repository-url]
cd deepseek-client
```

2. 安装依赖:
```bash
pip install -r requirements.txt
```

3. 配置API密钥:
```bash
cp .env.example .env
# 编辑.env文件，添加你的DeepSeek API密钥
```

## 使用示例

### 基本对话

```python
from deepseek.client import DeepSeekClient

# 初始化客户端
client = DeepSeekClient(api_key="your-api-key")

# 进行对话
response = client.chat("你好，请介绍一下自己")
print(response)
```

### 开启深度思考模式

```python
from deepseek.client import DeepSeekClient

client = DeepSeekClient(api_key="your-api-key")

# 启用深度思考
client.enable_deep_thinking()

# 提出需要深入思考的问题
response = client.chat("请分析人工智能对未来就业市场的影响")
print(response)
```

### 使用联网搜索

```python
from deepseek.client import DeepSeekClient

client = DeepSeekClient(api_key="your-api-key")

# 启用网络搜索
client.enable_web_search()

# 提出需要最新信息的问题
response = client.chat("最近有哪些重要的AI研究突破？")
print(response)
```

### 上传文件

```python
from deepseek.client import DeepSeekClient

client = DeepSeekClient(api_key="your-api-key")

# 上传文件并获取分析
file_id = client.upload_file("path/to/document.pdf")
response = client.chat("请总结这份文档的主要内容", file_ids=[file_id])
print(response)
```

## 配置选项

在创建客户端时可以设置以下配置选项:

```python
client = DeepSeekClient(
    api_key="your-api-key",
    base_url="https://api.deepseek.com",  # 可选，默认为DeepSeek官方API
    model="deepseek-chat",                # 可选，指定使用的模型
    timeout=30,                           # 可选，请求超时时间(秒)
    deep_thinking=False,                  # 可选，默认不启用深度思考
    web_search=False                      # 可选，默认不启用网络搜索
)
```

## 开发计划

- [ ] 流式响应支持
- [ ] 批量文件处理
- [ ] 多模态输入支持
- [ ] 对话历史管理
- [ ] Web界面

## 贡献指南

欢迎提交问题和拉取请求来改进此项目。请确保在提交前运行测试并遵循现有的代码风格。

## 许可证

[MIT](LICENSE) 