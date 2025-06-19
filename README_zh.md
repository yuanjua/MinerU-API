# MinerU v2.0 多GPU服务器

[English](README.md)

这是一个精简的多GPU服务器实现。

## 快速开始

### 1. 安装 MinerU

```bash
pip install --upgrade pip
pip install uv
uv pip install -r requirements.txt
```

### 2. 启动服务器

```bash
python server.py
```

### 3. 启动客户端

```bash
python client.py
```

现在，`[demo](../../demo/)` 文件夹下的PDF文件将并行处理。假设您有2个GPU，如果您将 `workers_per_device` 更改为 `2`，则可以同时处理4个PDF文件！

## 检索已解析文件

访问 `http://127.0.0.1:8000/download/{file_key}/all.zip` 下载 MinerU 2.0 的输出。如果您只对文本感兴趣，请访问 `http://127.0.0.1:8000/download/{file_key}/file.md`。您可能需要在客户端指定 `file_key`，否则服务端会生成一个随机的 UUID。

生成的文件目前被硬编码为在 7 天后删除。
