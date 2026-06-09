# GameRAG

API REST para catálogo e recomendação de jogos com Django, PostgreSQL, pgvector e embeddings da OpenAI.

## Stack de tecnologias

### Backend
- Python 3.12
- Django 6.0.5
- Django REST Framework 3.17.1
- PostgreSQL 17 com `pgvector`
- OpenAI embeddings via `openai` SDK
- JWT com `djangorestframework-simplejwt`
- CORS via `django-cors-headers`
- Admin customizado com `django-jazzmin`
- Configuração de ambiente com `python-dotenv`

### Frontend
- Vue 3
- Vite
- Tailwind CSS
- Pinia
- Vue Router
- Axios

### Infraestrutura
- Docker / Docker Compose
- PostgreSQL com extensão `pgvector`
- Backend em `http://localhost:8000`
- Frontend em `http://localhost:5173`

## Admin

O projeto já expõe o Django Admin em `/admin/`, protegido por login e senha.

Para criar um usuário admin local de forma repetível, preencha `ADMIN_USERNAME` e `ADMIN_PASSWORD` em `backend/.env` e suba o backend, ou execute:

```bash
# Ir no diretório de backend.
cd backend

# Criar um ambiente virtual .venv
python3 -m venv .venv

# Iniciar ambiente virtual
# Linux
source .venv/bin/activate

# Windows
source .venv/Scripts/activate

# Instalar as depêndencias necessárias.
pip install -r requirements.txt

# Criar um novo administrador
python manage.py create_admin_user
```

Se preferir, use o `createsuperuser` padrão do Django.

## Como rodar

Configure o arquivo de ambiente do backend:

```bash
cp backend/.env.example backend/.env
```

Preencha `OPENAI_API_KEY` em `backend/.env` e suba a aplicação:

```bash
docker compose up --build
```

A API ficará disponível em `http://localhost:8000`.

### Popular dados de exemplo

O backend já pode popular o banco de dados automaticamente ao iniciar, quando a variável `SEED_DATA` estiver definida como `true` em `backend/.env`.

No arquivo `backend/.env` ou em `backend/.env.example`, use:

```env
SEED_DATA=true
```

Isso faz com que o container execute `python manage.py seed_data` após aplicar as migrations.

Se preferir rodar manualmente, use:

```bash
docker compose exec backend python manage.py seed_data
```

Para criar apenas os jogos e não inserir usuários, avaliações, favoritos e biblioteca, use:

```bash
docker compose exec backend python manage.py seed_data --no-interactions
```

A página front-end é acessível em `http://localhost:5173`.

## Documentação

- Backend: [docs/backend.md](docs/backend.md)
- Collection Postman: [docs/GameRAG.postman_collection.json](docs/GameRAG.postman_collection.json)
