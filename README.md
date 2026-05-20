# GameRAG

API REST para catálogo e recomendação de jogos com Django, PostgreSQL, pgvector e embeddings da OpenAI.

## Como rodar

Configure o arquivo de ambiente do backend:

```bash
cp backend/.env.example backend/.env
```

Preencha `OPENAI_API_KEY` em `backend/.env` e suba a aplicação:

```bash
docker compose up --build
```

A API ficará disponível em:

```text
http://localhost:8000
```

## Documentação

- Backend: [docs/backend.md](docs/backend.md)
- Collection Postman: [docs/GameRAG.postman_collection.json](docs/GameRAG.postman_collection.json)
