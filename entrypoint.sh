#!/bin/sh

# O script irá parar se qualquer comando falhar
set -e

# 1. Espera o banco de dados ficar disponível
#    As variáveis de ambiente vêm do Render ou do seu .env local
echo "Aguardando o banco de dados..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "Banco de dados disponível."

# 2. Executa os comandos de setup do Django
echo "Aplicando migrações do banco de dados..."
python manage.py migrate --noinput

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# 3. Inicia o processo principal (o comando que foi passado para o container, ex: gunicorn)
#    O "$@" executa o comando que está no "command" do seu docker-compose.yml ou no Start Command do Render.
exec "$@"