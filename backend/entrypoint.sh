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
