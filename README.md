# bailian2openai

阿里百炼 API 转 OpenAI API 格式的适配服务，支持将 OpenAI 格式的请求转发到阿里百炼 API。

## 功能特点

- 支持 OpenAI chat completions API 格式
- 支持多轮对话（通过 session_id）
- 自动处理认证和格式转换
- 兼容现有的 OpenAI 客户端代码

## 安装

1. 克隆仓库：

   ```bash
   git clone https://github.com/yourusername/bailian2openai.git
   cd bailian2openai
   ```

2. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

3. 配置环境变量：

   创建 `.env` 文件并添加以下配置：

   ```plaintext
   DASHSCOPE_API_KEY=your_api_key_here
   DASHSCOPE_APP_ID=your_app_id_here
   ```

## 运行服务

启动服务器：

```bash
python main.py
```

服务将在 `http://localhost:8000` 上运行。

## API 使用

### 发送聊天请求

使用以下命令发送聊天请求：

```bash
curl -X POST "http://localhost:8000/chat/completions" \
     -H "Content-Type: application/json" \
     -H "X-Task-Id: your_task_id_here" \
     -H "X-Request-Id: your_request_id_here" \
     -d '{"messages": [{"role": "user", "content": "Hello, how are you?"}]}'
```



## 环境变量说明

- `DASHSCOPE_API_KEY`: 阿里百炼 API 密钥
- `DASHSCOPE_APP_ID`: 阿里百炼应用 ID

## 注意事项

1. 请确保已获取阿里百炼的 API 密钥和应用 ID。
2. 服务默认监听所有网络接口（0.0.0.0），如需更改请修改 `main.py`。
3. 默认端口为 8000，可以通过修改 `main.py` 更改。

## License

MIT
