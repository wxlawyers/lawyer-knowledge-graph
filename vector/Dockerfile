FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖（text2vec 需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9998

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "9998"]
