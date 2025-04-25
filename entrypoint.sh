#!/bin/sh

# Aguarda o banco de dados estar disponível
echo "Aguardando o banco de dados..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
  echo "Aguardando PostgreSQL em $POSTGRES_HOST:$POSTGRES_PORT..."
done

# Executa as migrations
echo "Aplicando migrations..."
python manage.py migrate

# Inicia o servidor
exec "$@"
