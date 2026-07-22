FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖（torch/transformers 编译需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ git && \
    rm -rf /var/lib/apt/lists/*

# 先装 CPU 版 torch（避免装 CUDA 版导致镜像 5GB+）
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9998

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "9998"]
