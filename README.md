# MinerU v2.0 Multi-GPU Server

[简体中文](README_zh.md)

A streamlined multi-GPU server implementation.

## Quick Start

### 1. install MinerU

```bash
pip install --upgrade pip
pip install uv
uv pip install -r requirements.txt
```

### 2. Start the Server
```bash
python server.py
```

### 3. Start the example Client
```bash
python client.py
```

*Now, pdf files under folder [pdfs](./pdfs/) will be processed in parallel. Assuming you have 2 gpus, if you change the `workers_per_device` to `2`, 4 pdf files will be processed at the same time!*

## Parsed File Retrival

You can visit `/download/` route to retrieve the output files. You might want to specify `file_key` in the client otherwise a random UUID would be returned by the server.

### Using curl to retrieve files

```bash
# Download all output as a zip file
curl -O http://127.0.0.1:8000/download/{file_key}/all.zip

# Retrieve only the text content as a markdown file
curl -O http://127.0.0.1:8000/download/{file_key}/file.md
```

*Generated files are currently hard coded to be removed in 7 days.*

## Docker

### Build Image

```
docker build -t mineru-api:v2.0 ./MinerU-API
```
*Builds the Docker image for MinerU API.*

### Run Container
```
docker run -d \
    -p 24008:24008 \
    -v mineru-api:/app/output \
    mineru-api:v2.0
```
*Runs the container, exposing port 24008 and mounting a named volume for output.*