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

Now, pdf files under folder [demo](../../demo/) will be processed in parallel. Assuming you have 2 gpus, if you change the `workers_per_device` to `2`, 4 pdf files will be processed at the same time!

## Parsed File Retrival

Visit `http://127.0.0.1:8000/download/{file_key}/all.zip` to download output from MinerU 2.0. If you are only interested in the text, visit `http://127.0.0.1:8000/download/{file_key}/file.md`. You might want to specify `file_key` in the client otherwise a random UUID would be returned by the server.

Generated files are currently hard coded to be removed in 7 days.