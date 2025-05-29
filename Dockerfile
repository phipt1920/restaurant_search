FROM python:3.10-slim

WORKDIR /app

# Cài gói cần thiết để apt hoạt động + hỗ trợ pandas/numpy
RUN apt-get update && apt-get install -y \
    build-essential \
    netcat-openbsd \
    curl \
    gnupg \
    libatlas-base-dev \
    libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy và cài requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy mã nguồn vào container
COPY . .

# Cho phép chạy file script chờ Elasticsearch
RUN chmod +x wait-for-it.sh

# Command mặc định để chạy app sau khi Elasticsearch sẵn sàng
CMD ["./wait-for-it.sh", "elasticsearch:9200", "--", "python", "app.py"]
