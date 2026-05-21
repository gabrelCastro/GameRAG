# GameRAG

API REST para catálogo e recomendação de jogos com Django, PostgreSQL, pgvector e embeddings da OpenAI.

## Admin

O projeto já expõe o Django Admin em `/admin/`, protegido por login e senha.

Para criar um usuário admin local de forma repetível, preencha `ADMIN_USERNAME` e `ADMIN_PASSWORD` em `backend/.env` e suba o backend, ou execute:

```bash
# Ir no diretório de backend.
cd backend

# Instalar as depêndencias necessárias.
pip install -r requirements.txt

# Iniciar ambiente virtual
# Linux
source .venv/bin/activate

# Windows
source .venv/Scripts/activate

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

## Documentação

- Backend: [docs/backend.md](docs/backend.md)
- Collection Postman: [docs/GameRAG.postman_collection.json](docs/GameRAG.postman_collection.json)
