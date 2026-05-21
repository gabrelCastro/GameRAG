# Backend — GameRAG

API REST construída com Django + Django REST Framework, seguindo arquitetura DDD pragmático.

---

## Stack

| Tecnologia | Versão | Papel |
|---|---|---|
| Python | 3.12 | Linguagem |
| Django | 6.0.5 | Framework web |
| Django REST Framework | 3.17.1 | Camada REST |
| PostgreSQL | 17 | Banco de dados |
| pgvector | 0.4.2 | Busca vetorial (embeddings) |
| psycopg2-binary | 2.9.12 | Adapter PostgreSQL |
| django-cors-headers | 4.9.0 | CORS para o frontend |
| openai | 2.36.0 | SDK OpenAI — geração de embeddings |
| python-dotenv | 1.2.2 | Carregamento de variáveis de ambiente |

---

## Como rodar

### Pré-requisitos

- Docker
- Chave de API da OpenAI

### 1. Configurar variáveis de ambiente

Copie o arquivo de exemplo e preencha sua chave da OpenAI:

```bash
cp backend/.env.example backend/.env
```

`.env`:
```
SECRET_KEY=uma-chave-segura-para-desenvolvimento
DEBUG=true
OPENAI_API_KEY=sk-...
```

### 2. Subir a aplicação

```bash
docker compose up --build
```

O Compose sobe o PostgreSQL com pgvector, instala as dependências do backend, aplica as migrations no entrypoint e inicia o servidor Django em `http://localhost:8000`.

### 3. Criar superusuário (opcional)

```bash
docker compose exec backend python manage.py createsuperuser
```

Se você quiser deixar isso repetível para o ambiente local, também pode definir `ADMIN_USERNAME` e `ADMIN_PASSWORD` em `backend/.env`. Quando esses valores estiverem presentes, o `entrypoint.sh` cria ou promove automaticamente o usuário admin ao subir o container.

---

## Arquitetura — DDD Pragmático

O projeto segue DDD pragmático: os models do Django servem como entidades, sem camada de entidades separada. Cada funcionalidade é organizada em um **bounded context** (app Django), dividido em quatro camadas:

```
<contexto>/
├── models.py              # Entidades (ORM Django)
├── admin.py               # Registro no Django Admin
├── domain/
│   └── services.py        # Lógica de domínio pura
├── application/
│   ├── game_service.py             # Orquestra operações de jogos
│   ├── recommendation_service.py   # Lógica de recomendação
│   └── user_game_service.py        # Interações do usuário com jogos
├── infrastructure/
│   └── repositories.py    # Encapsulamento do ORM (futuro)
└── interfaces/
    ├── views.py           # ViewSets — contrato HTTP
    ├── serializers.py     # Serialização e validação
    └── urls.py            # Rotas do contexto
```

### Fluxo de uma requisição

```
HTTP Request
    → interfaces/views.py      (recebe, valida via serializer)
    → application/*_service.py (aplica regras de negócio)
    → models.py                (persistência via ORM)
    → HTTP Response
```

### Bounded contexts atuais

| Contexto | Prefixo de rota | Responsabilidade |
|---|---|---|
| `games` | `/api/games/` | Catálogo, recomendações, avaliações, favoritos e biblioteca do usuário |
| `users` | `/api/auth/` | Registro, login e autenticação |

---

## Banco de dados

- **Engine:** PostgreSQL 17 via Docker
- **Extensão:** `pgvector` — ativada automaticamente na migration inicial do app `games`
- **Conexão padrão (dev):**

```
host:     localhost
porta:    5432
banco:    gamerag
usuário:  gamerag
senha:    gamerag
```

### Tabelas da aplicação

O app `games` possui uma única migration inicial (`backend/games/migrations/0001_initial.py`) e cria quatro tabelas próprias:

| Tabela | Model | Uso |
|---|---|---|
| `games_game` | `Game` | Catálogo de jogos e base dos embeddings |
| `games_gamereview` | `GameReview` | Avaliações e comentários dos usuários |
| `games_gamefavorite` | `GameFavorite` | Jogos favoritados pelo usuário |
| `games_gamelibraryentry` | `GameLibraryEntry` | Status do jogo na biblioteca do usuário |

---

## Bounded Context: games

### Model — `Game`

Arquivo: `backend/games/models.py`

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | `BigAutoField` | Chave primária |
| `title` | `CharField(255)` | Título do jogo |
| `description` | `TextField` | Descrição |
| `genre` | `CharField(100)` | Gênero |
| `platform` | `CharField(100)` | Plataforma |
| `price` | `DecimalField` | Preço (≥ 0) |
| `developer` | `CharField(255)` | Desenvolvedora |
| `publisher` | `CharField(255)` | Publicadora |
| `release_date` | `DateField` | Data de lançamento |
| `tags` | `JSONField` | Lista de tags |
| `rating` | `DecimalField` | Nota (0–10) |
| `embedding` | `VectorField(1536)` | Embedding OpenAI text-embedding-3-small |
| `created_at` | `DateTimeField` | Criação (auto) |
| `updated_at` | `DateTimeField` | Atualização (auto) |

### Model — `GameReview`

Representa a avaliação de um usuário para um jogo.

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | `BigAutoField` | Chave primária |
| `game` | `ForeignKey(Game)` | Jogo avaliado |
| `user` | `ForeignKey(User)` | Usuário que avaliou |
| `rating` | `PositiveSmallIntegerField` | Nota de 1 a 10 |
| `comment` | `TextField` | Comentário opcional |
| `created_at` | `DateTimeField` | Criação (auto) |

Restrição: um usuário só pode ter uma avaliação por jogo (`unique_together = game, user`).

### Model — `GameFavorite`

Representa um jogo favoritado pelo usuário.

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | `BigAutoField` | Chave primária |
| `game` | `ForeignKey(Game)` | Jogo favoritado |
| `user` | `ForeignKey(User)` | Usuário dono do favorito |
| `created_at` | `DateTimeField` | Criação (auto) |

Restrição: um usuário só pode favoritar o mesmo jogo uma vez (`unique_together = game, user`).

### Model — `GameLibraryEntry`

Representa o estado de um jogo na biblioteca pessoal do usuário.

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | `BigAutoField` | Chave primária |
| `game` | `ForeignKey(Game)` | Jogo na biblioteca |
| `user` | `ForeignKey(User)` | Usuário dono da entrada |
| `status` | `CharField(20)` | Estado do jogo |
| `hours_played` | `DecimalField` | Horas jogadas (>= 0) |
| `created_at` | `DateTimeField` | Criação (auto) |
| `updated_at` | `DateTimeField` | Atualização (auto) |

Status aceitos:

| Valor | Significado |
|---|---|
| `want_to_play` | Quero jogar |
| `playing` | Jogando |
| `completed` | Concluído |
| `dropped` | Abandonado |

Restrição: um usuário só pode ter uma entrada de biblioteca por jogo (`unique_together = game, user`).

### Services

**`GameService`** — `backend/games/application/game_service.py`

| Método | Descrição |
|---|---|
| `get_queryset()` | Retorna todos os jogos |
| `get_by_id(id)` | Busca por ID — 404 automático se não encontrado |
| `create(serializer)` | Cria jogo — ponto de extensão para gerar embedding |
| `update(serializer)` | Atualiza jogo — ponto de extensão para regravar embedding |
| `delete(instance)` | Remove jogo |

**`RecommendationService`** — `backend/games/application/recommendation_service.py`

| Método | Descrição |
|---|---|
| `find_similar_games(embedding, limit)` | Busca jogos por distância de cosseno no espaço vetorial |
| `find_similar_to_game(game, limit)` | Busca similares a um jogo existente, excluindo ele mesmo |

**`UserGameService`** — `backend/games/application/user_game_service.py`

| Método | Descrição |
|---|---|
| `list_reviews(game)` | Lista avaliações de um jogo |
| `get_user_review(game, user)` | Busca a avaliação do usuário para um jogo |
| `save_review(serializer, game, user)` | Cria ou atualiza avaliação |
| `delete_review(game, user)` | Remove avaliação do usuário |
| `list_favorites(user)` | Lista favoritos do usuário |
| `add_favorite(game, user)` | Favorita um jogo |
| `remove_favorite(game, user)` | Remove favorito |
| `list_library(user)` | Lista biblioteca do usuário |
| `get_library_entry(game, user)` | Busca entrada de biblioteca do usuário |
| `save_library_entry(serializer, game, user)` | Cria ou atualiza entrada da biblioteca |
| `remove_library_entry(game, user)` | Remove entrada da biblioteca |

### Endpoints REST

Base URL: `http://localhost:8000/api/games/`

| Método | URL | Ação | Status |
|---|---|---|---|
| `GET` | `/api/games/` | Listar todos os jogos | 200 |
| `POST` | `/api/games/` | Cadastrar jogo | 201 |
| `GET` | `/api/games/{id}/` | Detalhar jogo | 200 / 404 |
| `PUT` | `/api/games/{id}/` | Atualizar completo | 200 / 404 |
| `PATCH` | `/api/games/{id}/` | Atualizar parcial | 200 / 404 |
| `DELETE` | `/api/games/{id}/` | Remover jogo | 204 / 404 |
| `GET` | `/api/games/{id}/similar/` | Jogos similares | 200 / 404 / 422 |
| `GET` | `/api/games/{id}/reviews/` | Listar avaliações do jogo | 200 / 404 |
| `POST` | `/api/games/{id}/reviews/` | Criar ou atualizar minha avaliação | 200 / 201 / 400 / 404 |
| `DELETE` | `/api/games/{id}/reviews/me/` | Remover minha avaliação | 204 / 404 |
| `POST` | `/api/games/{id}/favorite/` | Favoritar jogo | 200 / 201 / 404 |
| `DELETE` | `/api/games/{id}/favorite/` | Remover favorito | 204 / 404 |
| `GET` | `/api/games/favorites/` | Listar meus favoritos | 200 |
| `POST` | `/api/games/{id}/library/` | Adicionar jogo à minha biblioteca | 200 / 201 / 400 / 404 |
| `PATCH` | `/api/games/{id}/library/` | Atualizar status/horas na biblioteca | 200 / 201 / 400 / 404 |
| `DELETE` | `/api/games/{id}/library/` | Remover jogo da minha biblioteca | 204 / 404 |
| `GET` | `/api/games/library/` | Listar minha biblioteca | 200 |

#### Query params disponíveis

| Param | Exemplo | Descrição |
|---|---|---|
| `search` | `?search=zelda` | Busca em título, gênero, plataforma, dev e publisher |
| `ordering` | `?ordering=price` | Ordena por `title`, `price`, `rating` ou `release_date` |
| `ordering` (desc) | `?ordering=-rating` | Prefixo `-` para ordem decrescente |
| `limit` | `?limit=5` | Quantidade de similares retornados (máx 50, padrão 10) — só em `/similar/` |

#### Exemplo de payload (POST / PUT)

```json
{
  "title": "The Witcher 3",
  "description": "RPG de mundo aberto épico.",
  "genre": "RPG",
  "platform": "PC",
  "price": "99.90",
  "developer": "CD Projekt Red",
  "publisher": "CD Projekt",
  "release_date": "2015-05-19",
  "tags": ["RPG", "Open World", "Fantasy"],
  "rating": "9.8"
}
```

> O campo `embedding` é gerenciado internamente — não deve ser enviado pelo cliente.

#### Payload de avaliação

`POST /api/games/{id}/reviews/`

```json
{
  "rating": 9,
  "comment": "Excelente RPG, com boa progressão e mundo aberto."
}
```

Se o usuário já tiver avaliado o jogo, a requisição atualiza a avaliação existente.

#### Payload de biblioteca

`POST /api/games/{id}/library/` ou `PATCH /api/games/{id}/library/`

```json
{
  "status": "playing",
  "hours_played": "12.5"
}
```

O campo `status` aceita `want_to_play`, `playing`, `completed` ou `dropped`.

### Validações do serializer

| Campo | Regra |
|---|---|
| `rating` | Entre 0 e 10 |
| `price` | Maior ou igual a 0 |
| `tags` | Lista de strings |
| `GameReview.rating` | Entre 1 e 10 |
| `GameLibraryEntry.status` | Um dos status aceitos |
| `GameLibraryEntry.hours_played` | Maior ou igual a 0 |

---

## Autenticação

A API usa **JWT (JSON Web Token)** via `djangorestframework-simplejwt`. Toda requisição autenticada deve enviar o header:

```
Authorization: Bearer <access_token>
```

### Perfis

| Perfil | `is_staff` | Permissões |
|---|---|---|
| **Admin** | `True` | Acesso total — CRUD de jogos e todos os endpoints |
| **Usuário** | `False` | Registro, login, recomendações e interações pessoais com jogos |

### Endpoints de autenticação

Base URL: `http://localhost:8000/api/auth/`

| Método | URL | Ação | Auth |
|---|---|---|---|
| `POST` | `/api/auth/register/` | Cadastrar novo usuário | Público |
| `POST` | `/api/auth/login/` | Login — retorna `access` e `refresh` tokens | Público |
| `POST` | `/api/auth/token/refresh/` | Renovar o access token | Público |

#### Payload de registro

```json
{
  "username": "joao",
  "email": "joao@email.com",
  "password": "senha1234"
}
```

#### Payload de login

```json
{
  "username": "joao",
  "password": "senha1234"
}
```

#### Resposta do login

```json
{
  "access": "<token válido por 1h>",
  "refresh": "<token válido por 7 dias>"
}
```

### Configuração dos tokens

| Token | Validade |
|---|---|
| Access | 1 hora |
| Refresh | 7 dias |

### Matriz de permissões

| Endpoint | Sem token | Usuário | Admin |
|---|---|---|---|
| `POST /api/auth/register/` | ✅ | ✅ | ✅ |
| `POST /api/auth/login/` | ✅ | ✅ | ✅ |
| `GET /api/games/` | 401 | ✅ | ✅ |
| `GET /api/games/{id}/` | 401 | ✅ | ✅ |
| `POST /api/games/` | 401 | 403 | ✅ |
| `PUT/PATCH /api/games/{id}/` | 401 | 403 | ✅ |
| `DELETE /api/games/{id}/` | 401 | 403 | ✅ |
| `GET /api/games/{id}/similar/` | 401 | ✅ | ✅ |
| `GET /api/games/{id}/reviews/` | 401 | ✅ | ✅ |
| `POST /api/games/{id}/reviews/` | 401 | ✅ | ✅ |
| `DELETE /api/games/{id}/reviews/me/` | 401 | ✅ | ✅ |
| `POST/DELETE /api/games/{id}/favorite/` | 401 | ✅ | ✅ |
| `GET /api/games/favorites/` | 401 | ✅ | ✅ |
| `POST/PATCH/DELETE /api/games/{id}/library/` | 401 | ✅ | ✅ |
| `GET /api/games/library/` | 401 | ✅ | ✅ |

---

## Integração OpenAI — Embeddings

### Como funciona

Ao **criar** ou **atualizar** um jogo via API, o backend gera automaticamente um embedding vetorial usando o modelo `text-embedding-3-small` da OpenAI (1536 dimensões) e o armazena no campo `embedding` do model `Game`.

O texto enviado para a API é montado a partir dos campos do jogo:

```
{title}. {description}. Gênero: {genre}. Plataforma: {platform}. Desenvolvedor: {developer}. Tags: {tags}.
```

### Arquivos envolvidos

| Arquivo | Responsabilidade |
|---|---|
| `games/infrastructure/embedding_client.py` | Encapsula a chamada à API da OpenAI |
| `games/application/game_service.py` | Chama o client após salvar o jogo |
| `backend/.env` | Contém a `OPENAI_API_KEY` (não versionado) |
| `backend/GameRAG/settings.py` | Expõe `OPENAI_API_KEY` via `os.environ` |

### Variável de ambiente

```
OPENAI_API_KEY=sk-...
```

Configurada em `backend/.env`, carregada automaticamente via `python-dotenv` no início do `settings.py`.

### Resiliência

Se a geração de embedding falhar (chave inválida, timeout, etc.), o jogo **é salvo normalmente** sem embedding. O erro é registrado no log com o ID do jogo. O campo `embedding` permanece `null` e pode ser regerado futuramente.

---

## CORS

Origens permitidas em desenvolvimento:

```
http://localhost:3000   (React / Next.js)
http://localhost:5173   (Vite)
```

Para adicionar uma nova origem, edite `CORS_ALLOWED_ORIGINS` em `backend/GameRAG/settings.py`.

---

## Django Admin

Disponível em `http://localhost:8000/admin/`.

Interface administrativa com o tema **Jazzmin** (`django-jazzmin`).

### `Game`

| Configuração | Valor |
|---|---|
| `list_display` | title, genre, platform, developer, price, rating, release_date |
| `list_filter` | genre, platform |
| `search_fields` | title, developer, publisher |
| `ordering` | title |
| `inlines` | `GameReviewInline`, `GameFavoriteInline`, `GameLibraryEntryInline` |

### `GameReview`

| Configuração | Valor |
|---|---|
| `list_display` | game, user, rating, created_at |
| `list_filter` | rating |
| `search_fields` | game__title, user__username |

### `GameFavorite`

| Configuração | Valor |
|---|---|
| `list_display` | game, user, created_at |
| `search_fields` | game__title, user__username |

### `GameLibraryEntry`

| Configuração | Valor |
|---|---|
| `list_display` | game, user, status, hours_played, updated_at |
| `list_filter` | status |
| `search_fields` | game__title, user__username |

### `User`

| Configuração | Valor |
|---|---|
| `list_display` | username, email, first_name, last_name, is_staff, is_active, date_joined |
| `list_filter` | is_staff, is_active, is_superuser |
| `search_fields` | username, email, first_name, last_name |
