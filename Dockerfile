FROM lmsysorg/sglang:v0.4.7-cu124

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
    apscheduler \
    --break-system-packages && \
    mineru-models-download -s $MODEL_SOURCE -m all

ENV MINERU_MODEL_SOURCE=local
ENV PYTHONPATH=/app
EXPOSE 24008

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

ENTRYPOINT ["python3", "server.py", "--port", "24008"]