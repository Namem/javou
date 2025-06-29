FROM python:3.12-slim

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y netcat-openbsd

# Copia o arquivo de dependências primeiro para otimizar o cache do Docker
COPY ./requirements.txt /app/requirements.txt

# Instala as dependências do Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia todo o resto do projeto para o container
COPY . /app

# Garante que o script de entrypoint seja executável
RUN chmod +x /app/entrypoint.sh

# Expõe a porta que o Gunicorn irá usar
EXPOSE 8000

# ===================================================================
# INÍCIO DA MODIFICAÇÃO: Define nosso script como o ponto de entrada
# ===================================================================
# Agora, toda vez que o container iniciar, ele executará este script primeiro.
ENTRYPOINT ["/app/entrypoint.sh"]
# ===================================================================
# FIM DA MODIFICAÇÃO
# ===================================================================

# O comando padrão que o entrypoint.sh irá executar no final (com exec "$@")
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]