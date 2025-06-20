FROM pytorch/pytorch:2.7.1-cuda12.6-cudnn9-runtime

RUN apt-get update && apt-get install -y libgl1-mesa-glx \
    libsm6 libxext6 libxrender-dev libfontconfig1 libxft2 libfreetype6 libglib2.0-0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY src/server.py .
COPY src/_config_endpoint.py .
COPY src/_file_utils.py .
RUN mkdir -p output

RUN export MODEL_SOURCE=$(python3 _config_endpoint.py) && \
    if [ "$MODEL_SOURCE" = "modelscope" ]; then pip config set global.index-url https://mirrors.aliyun.com/pypi/simple; fi && \
    python3 -m pip install -U 'mineru[core]' \
    litserve \
    fastapi \
    uvicorn \
    loguru \
    aiohttp \
    apscheduler \
    --break-system-packages #&& \
    mineru-models-download -s $MODEL_SOURCE -m pipeline

ENV MINERU_MODEL_SOURCE=local
ENV PYTHONPATH=/app
EXPOSE 24008

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:24008/health || exit 1

ENTRYPOINT ["python3", "server.py", "--port", "24008"]