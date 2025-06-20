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
python src/server.py
```

### 3. Start the example Client
```bash
python example/client.py
```

*Now, pdf files under folder [./example/pdfs](./example/pdfs/) will be processed in parallel. Assuming you have 2 gpus, if you change the `workers_per_device` to `2`, 4 pdf files will be processed at the same time!*


## Docker

### Build Image

```
docker build -t mineru-api:v2.0 .
```
*Builds the Docker image for MinerU API.*

### Run Container
```
docker run -d --gpus all \
    -p 24008:24008 \
    -v mineru-api:/app/output \
    mineru-api:v2.0
```
*Runs the container, exposing port 24008 and mounting a named volume for output.*


## API Endpoints

### /predict

This endpoint is used to submit PDF files for processing.

```
POST /predict
```

**Request Body Example:**
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

**Example `jq` command:**
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

This endpoint allows retrieval of processed files.

```
GET /download/{file_key}/all.zip
GET /download/{file_key}/file.md
```

Replace `{file_key}` with the identifier returned by the `/predict` endpoint or a custom `file_key` provided in the request.

## Parsed File Retrieval

You can visit `/download/` route to retrieve the output files. You might want to specify `file_key` in the client otherwise a random UUID would be returned by the server.

### Using curl to retrieve files

```bash
FILE_KEY=my_document_key

# Download all output as a zip file
curl -O http://127.0.0.1:8000/download/${FILE_KEY}/all.zip

# Retrieve only the text content as a markdown file
curl -O http://127.0.0.1:8000/download/${FILE_KEY}/file.md
```

*Generated files are currently hard coded to be removed in 7 days.*
