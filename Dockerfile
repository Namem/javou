FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-openbsd

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

# Garante que o script seja executável DENTRO do container
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

# Define nosso script como o ponto de entrada oficial
ENTRYPOINT ["/app/entrypoint.sh"]

# Define o comando padrão que o entrypoint irá executar no final com "$@"
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]