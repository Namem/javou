#!/bin/sh

# O script irá parar se qualquer comando falhar
set -e

# 1. Espera o banco de dados ficar disponível
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

# 3. Inicia o processo principal (Gunicorn)
exec "$@"