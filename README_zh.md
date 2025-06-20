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
python example/client.py
```

*现在，[./example/pdfs](./example/pdfs/) 文件夹下的PDF文件将并行处理。假设您有2个GPU，如果您将 `workers_per_device` 更改为 `2`，则可以同时处理4个PDF文件！*


## Docker

### 构建镜像

```bash
docker build -t mineru-api:v2.0 .
```
*构建 MinerU API Docker 镜像。*

### 运行容器
```bash
docker run -d --gpus all \
    -p 24008:24008 \
    -v mineru-api:/app/output \
    mineru-api:v2.0
```
*运行容器，暴露 24008 端口并挂载一个命名卷用于输出。*


## API 端点

### /predict

此端点用于提交PDF文件进行处理。

```
POST /predict
```

**请求体示例:**
```json
{
    "file": "base64_encoded_pdf_content",
    "options": {
        "backend": "pipeline",
        "lang": "en",
        "method": "auto",
        "formula_enable": true,
        "table_enable": true
    },
    "file_key": "optional_unique_file_identifier"
}
```

**示例 `jq` 请求:**
```bash
jq -n \
   --arg file_key "my_document_key" \
   --argjson options '{"backend": "pipeline", "lang": "en", "method": "auto", "formula_enable": true, "table_enable": true}' \
   --rawfile file_data ./example/pdfs/demo1.pdf \
   '{
      "file": ($file_data | @base64),
      "options": $options,
      "file_key": $file_key
    }' | curl -X POST http://127.0.0.1:24008/predict \
              -H "Content-Type: application/json" \
              -d @-
```

### /download

此端点允许检索已处理的文件。

```
GET /download/{file_key}/all.zip
GET /download/{file_key}/file.md
```

将 `{file_key}` 替换为 `/predict` 端点返回的标识符，或在请求中提供的自定义 `file_key`。

## 检索已解析文件

您可以访问 `/download/` 路由来检索输出文件。您可能需要在客户端指定 `file_key`，否则服务端会生成一个随机的 UUID。

### 使用 curl 检索文件

```bash
FILE_KEY=my_document_key

# 将所有输出下载为 zip 文件
curl -O http://127.0.0.1:8000/download/${FILE_KEY}/all.zip

# 仅将文本内容检索为 markdown 文件
curl -O http://127.0.0.1:8000/download/${FILE_KEY}/file.md
```

*生成的文件目前被硬编码为在 7 天后删除。*
