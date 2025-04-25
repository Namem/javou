FROM python:3.12-slim

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto para dentro do container
COPY . /app

# Instala dependências
RUN apt-get update && apt-get install -y netcat-openbsd \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


# Expõe a porta padrão do Django
EXPOSE 8000

# Comando de entrada padrão (usado via docker-compose override)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

