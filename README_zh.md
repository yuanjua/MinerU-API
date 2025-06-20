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
python src/server.py
```

### 3. 启动客户端

```bash
python src/client.py
```

*现在，[pdfs](./pdfs/) 文件夹下的PDF文件将并行处理。假设您有2个GPU，如果您将 `workers_per_device` 更改为 `2`，则可以同时处理4个PDF文件！*

## 检索已解析文件

您可以访问 `/download/` 路由来检索输出文件。您可能需要在客户端指定 `file_key`，否则服务端会生成一个随机的 UUID。

### 使用 curl 检索文件

```bash
# 将所有输出下载为 zip 文件
curl -O http://127.0.0.1:8000/download/{file_key}/all.zip

# 仅将文本内容检索为 markdown 文件
curl -O http://127.0.0.1:8000/download/{file_key}/file.md
```

*生成的文件目前被硬编码为在 7 天后删除。*

## Docker

### 构建镜像

```bash
docker build -t mineru-api:v2.0 ./MinerU-API
```
*构建 MinerU API Docker 镜像。*

### 运行容器
```bash
docker run -d \
    -p 24008:24008 \
    -v mineru-api:/app/output \
    mineru-api:v2.0
```
*运行容器，暴露 24008 端口并挂载一个命名卷用于输出。*
