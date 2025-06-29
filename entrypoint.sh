#!/bin/sh

# O script irá parar se qualquer comando falhar
set -e

# Executa os comandos de setup do Django
echo "Aplicando migrações do banco de dados..."
python manage.py migrate --noinput

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Inicia o processo principal (o comando que foi passado para o container, ex: gunicorn)
exec "$@"