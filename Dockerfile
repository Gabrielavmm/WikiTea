# Dockerfile para o Sistema RAG de Autismo
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fonte
COPY src/ ./src/
COPY app/ ./app/
COPY ingest/ ./ingest/

# Criar diretórios necessários
RUN mkdir -p chroma_db data

# Expor porta do Streamlit
EXPOSE 8501

# Comando para executar a aplicação
CMD ["streamlit", "run", "app/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]