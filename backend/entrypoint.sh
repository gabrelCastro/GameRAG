#!/bin/sh
set -e

echo "Aguardando o banco de dados..."
until python -c "
import os, psycopg2
psycopg2.connect(
    dbname=os.environ.get('DB_NAME', 'gamerag'),
    user=os.environ.get('DB_USER', 'gamerag'),
    password=os.environ.get('DB_PASSWORD', 'gamerag'),
    host=os.environ.get('DB_HOST', 'db'),
    port=os.environ.get('DB_PORT', '5432'),
)
" 2>/dev/null; do
  echo "  banco ainda não disponível, tentando novamente..."
  sleep 2
done
echo "Banco de dados pronto."

python manage.py migrate --noinput

if [ -n "${ADMIN_USERNAME:-}" ] && [ -n "${ADMIN_PASSWORD:-}" ]; then
  echo "Garantindo usuário admin local..."
  python manage.py create_admin_user
fi

exec python manage.py runserver 0.0.0.0:8000
