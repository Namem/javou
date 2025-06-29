#!/bin/sh

set -e

echo "Aplicando migrações do banco de dados..."
python manage.py migrate --noinput

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# ===================================================================
# INÍCIO DA MODIFICAÇÃO: Usar nosso novo comando não-interativo
# ===================================================================
echo "Verificando/Criando superusuário..."
python manage.py createsuperuser_if_needed
# ===================================================================
# FIM DA MODIFICAÇÃO
# ===================================================================

exec "$@"