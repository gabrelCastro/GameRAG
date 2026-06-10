#!/bin/sh
set -e

echo "Aguardando o banco de dados..."
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}
DB_NAME=${DB_NAME:-gamerag}
DB_USER=${DB_USER:-gamerag}
DB_PASSWORD=${DB_PASSWORD:-gamerag}

# Retry logic com timeout mais longo
RETRY_COUNT=0
MAX_RETRIES=30

until python -c "
import os, psycopg2, sys
try:
    psycopg2.connect(
        dbname='${DB_NAME}',
        user='${DB_USER}',
        password='${DB_PASSWORD}',
        host='${DB_HOST}',
        port='${DB_PORT}',
        connect_timeout=3
    )
    print('✅ Banco de dados pronto!', flush=True)
except Exception as e:
    print(f'❌ Erro: {e}', flush=True)
    sys.exit(1)
" 2>&1; do
  RETRY_COUNT=$((RETRY_COUNT + 1))
  if [ $RETRY_COUNT -gt $MAX_RETRIES ]; then
    echo "Máximo de tentativas ($MAX_RETRIES) atingido. Abortando."
    exit 1
  fi
  echo "  banco ainda não disponível, tentativa $RETRY_COUNT/$MAX_RETRIES..."
  sleep 2
done

python manage.py migrate --noinput

if [ -n "${ADMIN_USERNAME:-}" ] && [ -n "${ADMIN_PASSWORD:-}" ]; then
  echo "Garantindo usuário admin local..."
  python manage.py create_admin_user
fi


echo "Verificando dados existentes no banco..."
python - <<PY
import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GameRAG.settings')
import django
django.setup()
from django.db import connections
from django.db.utils import OperationalError
try:
    # Tenta consultar se já existem jogos na tabela
    from games.models import Game
    has_games = Game.objects.exists()
except OperationalError:
    # Se houver problema de conexão/initialização, assume que não há dados
    has_games = False

if has_games:
    print('Dados já presentes no banco — pulando seeds.')
else:
    print('Banco sem dados. Executando seeds...')
    # Executa o comando de seed via manage.py para garantir consistência
    from django.core.management import call_command
    call_command('seed_data')
PY

exec python manage.py runserver 0.0.0.0:8000
