FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    curl unzip gcc \
    && rm -rf /var/lib/apt/lists/*

# Node es requerido por Reflex para compilar el frontend
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Inicializa reflex (descarga bun y arma .web)
RUN reflex init

EXPOSE 3000 8001

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]
