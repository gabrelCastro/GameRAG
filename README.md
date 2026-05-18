# 🎮 GameRAG - Sistema de Recomendação de Jogos com IA

**GameRAG** é uma API REST moderna para catálogo e recomendação de jogos que utiliza **busca semântica alimentada por inteligência artificial**. Usando embeddings do OpenAI e pgvector, o sistema encontra jogos similares não apenas por correspondência textual literal, mas por **significado semântico** — um usuário procurando por "ação rápida" também encontrará "jogos de reflexos" mesmo sem usar essas palavras exatas.

---

## ✨ Características Principais

- 🎯 **Busca Semântica Inteligente** — Embeddings OpenAI (text-embedding-3-small) com pgvector
- 👥 **Autenticação JWT** — Registro, login e refresh de tokens
- 📚 **CRUD Completo** — Gerenciamento de catálogo de jogos
- ⭐ **Sistema de Reviews** — Avaliações e comentários de usuários
- 🏗️ **Arquitetura DDD** — Domain-Driven Design pragmático com camadas bem definidas
- 🧪 **Testes Robustos** — 60+ testes unitários com cobertura completa
- 🐳 **Docker Ready** — Containerização com Docker Compose
- 📖 **Admin Django** — Interface Jazzmin para gerenciar dados
- 🌐 **CORS Habilitado** — Pronto para integração com frontend

---

## 🚀 Quick Start

### Com Docker (Recomendado)

```bash
# 1. Clonar repositório
git clone <repo>
cd GameRAG

# 2. Configurar variáveis de ambiente
cp backend/.env.example backend/.env
# Editar backend/.env e adicionar sua OPENAI_API_KEY

# 3. Levantar serviços
docker compose up -d

# 4. Verificar se está rodando
curl http://localhost:8000/api/games/
```

### Instalação Local

```bash
# 1. Criar ambiente virtual
cd backend
python3 -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar variáveis
cp .env.example .env
# Adicionar OPENAI_API_KEY em .env

# 4. Executar migrations
python manage.py migrate

# 5. Criar superuser (opcional)
python manage.py createsuperuser

# 6. Iniciar servidor
python manage.py runserver
```

Acesse: `http://localhost:8000`  
Admin: `http://localhost:8000/admin/`

---

## 📊 Stack Tecnológico

| Componente | Tecnologia | Versão |
|---|---|---|
| **Backend** | Python | 3.12 |
| **Framework** | Django | 6.0.5 |
| **API REST** | Django REST Framework | 3.17.1 |
| **Banco de Dados** | PostgreSQL | 17 |
| **Vetores** | pgvector | 0.4.2 |
| **IA/Embeddings** | OpenAI SDK | 2.36.0 |
| **Autenticação** | SimpleJWT | 5.5.1 |
| **Admin** | Django Jazzmin | 3.0.4 |
| **Containerização** | Docker + Docker Compose | Latest |
| **Frontend** | HTML5 + JavaScript + Tailwind CSS | Latest |

---

## 📁 Estrutura do Projeto

```
GameRAG/
├── backend/
│   ├── GameRAG/              # Configuração Django
│   │   ├── settings.py       # Configurações do projeto
│   │   ├── urls.py           # Rotas principais
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   ├── games/                # 🎮 App de Jogos (Catálogo + Recomendação)
│   │   ├── models.py         # Game, GameReview
│   │   ├── domain/
│   │   │   └── services.py
│   │   ├── application/
│   │   │   ├── game_service.py          # CRUD e embeddings
│   │   │   └── recommendation_service.py # Busca semântica
│   │   ├── infrastructure/
│   │   │   ├── embedding_client.py      # Cliente OpenAI
│   │   │   └── repositories.py
│   │   ├── interfaces/
│   │   │   ├── views.py      # GameViewSet REST
│   │   │   ├── serializers.py
│   │   │   └── urls.py
│   │   └── tests/            # Testes unitários
│   │
│   ├── users/                # 👤 App de Usuários (Autenticação)
│   │   ├── models.py
│   │   ├── application/
│   │   │   └── user_service.py
│   │   ├── interfaces/
│   │   │   ├── views.py      # RegisterView
│   │   │   ├── serializers.py
│   │   │   └── urls.py
│   │   └── tests/
│   │
│   ├── chat/                 # 💬 App de Chat (RAG - Em Desenvolvimento)
│   │   └── interfaces/
│   │       ├── views.py
│   │       └── urls.py
│   │
│   ├── templates/            # Frontend HTML
│   │   ├── telaInicial.html  # Login/Cadastro
│   │   ├── telaRAG.html      # Interface Principal
│   │   ├── scripts/
│   │   │   ├── telaInicial.js
│   │   │   └── telaRAG.js
│   │   └── styles/
│   │       ├── telaInicial.css
│   │       └── telaRAG.css
│   │
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── manage.py
│   ├── requirements.txt
│   └── .env.example
│
├── docker-compose.yml        # PostgreSQL + Backend
├── docs/
│   ├── backend.md           # Documentação detalhada
│   └── GameRAG.postman_collection.json
└── README.md               # Este arquivo
```

---

## 🔌 API REST - Principais Endpoints

### 🎮 **Jogos** (`/api/games/`)

#### Listar/Criar Jogos
```bash
GET /api/games/
POST /api/games/
```

**Query Parameters:**
- `search=zelda` — Busca por título, gênero, plataforma ou desenvolvedor
- `ordering=price` ou `ordering=-rating` — Ordenação (asc/desc)

**Request (POST):**
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

**Response (200):**
```json
{
  "id": 1,
  "title": "The Witcher 3",
  "description": "RPG de mundo aberto épico.",
  "genre": "RPG",
  "platform": "PC",
  "price": "99.90",
  "developer": "CD Projekt Red",
  "publisher": "CD Projekt",
  "release_date": "2015-05-19",
  "tags": ["RPG", "Open World", "Fantasy"],
  "rating": "9.8",
  "created_at": "2024-05-17T10:30:00Z",
  "updated_at": "2024-05-17T10:30:00Z"
}
```

#### Detalhes, Atualizar, Deletar
```bash
GET /api/games/{id}/
PUT /api/games/{id}/
PATCH /api/games/{id}/
DELETE /api/games/{id}/
```

#### 🔍 Busca Semântica - Jogos Similares
```bash
GET /api/games/{id}/similar/?limit=10
```

**Query Parameters:**
- `limit=10` — Quantidade de similares (1-50, padrão: 10)

**Response (200):**
```json
{
  "query_game": {
    "id": 1,
    "title": "The Witcher 3",
    ...
  },
  "similar_games": [
    {
      "id": 2,
      "title": "Baldur's Gate 3",
      "similarity_score": 0.92,
      ...
    },
    {
      "id": 3,
      "title": "Dragon's Dogma 2",
      "similarity_score": 0.87,
      ...
    }
  ]
}
```

### 👤 **Autenticação** (`/api/auth/`)

#### Registro
```bash
POST /api/auth/register/
```

**Request:**
```json
{
  "username": "joao_gamer",
  "email": "joao@example.com",
  "password": "senha_super_segura_123"
}
```

**Response (201):**
```json
{
  "id": 1,
  "username": "joao_gamer",
  "email": "joao@example.com"
}
```

#### Login
```bash
POST /api/auth/login/
```

**Request:**
```json
{
  "username": "joao_gamer",
  "password": "senha_super_segura_123"
}
```

**Response (200):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Renovar Token
```bash
POST /api/auth/token/refresh/
```

**Request:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 📝 **Headers Obrigatórios (Endpoints Autenticados)**

```bash
Authorization: Bearer <access_token>
Content-Type: application/json
```

---

## 🔐 Autenticação e Permissões

### Duração dos Tokens
- **Access Token:** 1 hora
- **Refresh Token:** 7 dias

### Matriz de Permissões
| Endpoint | Público | Usuário | Admin |
|---|---|---|---|
| POST /auth/register/ | ✅ | ✅ | ✅ |
| POST /auth/login/ | ✅ | ✅ | ✅ |
| GET /games/ | ❌ | ❌ | ✅ |
| POST /games/ | ❌ | ❌ | ✅ |
| GET /games/{id}/similar/ | ❌ | ✅ | ✅ |
| POST /chat/ | ❌ | ✅ | ✅ |

---

## 🗄️ Modelos de Dados

### Game
```python
- id (Integer) — Chave primária
- title (String) — Título do jogo
- description (Text) — Descrição detalhada
- genre (String) — Gênero
- platform (String) — Plataforma (PC, PS5, Xbox, Nintendo, etc.)
- price (Decimal) — Preço (validação: ≥ 0)
- developer (String) — Desenvolvedor
- publisher (String) — Publicadora
- release_date (Date) — Data de lançamento
- tags (JSON Array) — Tags descritivas
- rating (Decimal) — Nota de 1-10 (validação: 0-10)
- embedding (Vector) — Embedding OpenAI (1536 dimensões)
- created_at (DateTime) — Data de criação
- updated_at (DateTime) — Data de atualização
```

### GameReview
```python
- id (Integer)
- game (ForeignKey) → Game
- user (ForeignKey) → User
- rating (Integer) — 1-10
- comment (Text) — Comentário
- created_at (DateTime)
- Constraint: Um usuário só pode avaliar um jogo uma vez
```

### User (Django Built-in)
```python
- id (Integer)
- username (String) — Único
- email (Email) — Único no registro
- password (String) — Hasheada com PBKDF2
- is_staff (Boolean) — True = Admin, False = Usuário comum
```

---

## 🧪 Testes

O projeto possui **60+ testes unitários** cobrindo:

- ✅ Serviços de jogo (CRUD, embeddings)
- ✅ Serviço de recomendação (busca semântica)
- ✅ Views e serializers
- ✅ Autenticação e permissões
- ✅ Validações de entrada
- ✅ Tratamento de erros

### Executar Testes

```bash
# Todos os testes
python manage.py test

# App específico
python manage.py test games
python manage.py test users

# Test específico
python manage.py test games.tests.test_game_service.GameServiceTestCase.test_create_game

# Com verbosidade
python manage.py test --verbosity=2

# Com cobertura
coverage run --source='.' manage.py test
coverage report
```

---

## 🌍 Variáveis de Ambiente

Crie um arquivo `.env` na raiz de `backend/` com base em `.env.example`:

```env
# Django
DEBUG=True
SECRET_KEY=django-insecure-your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# OpenAI (CRÍTICO)
OPENAI_API_KEY=sk-proj-...                # Sua chave da OpenAI

# Database
DB_NAME=gamerag
DB_USER=gamerag
DB_PASSWORD=gamerag
DB_HOST=db                                # "db" com Docker, "localhost" local
DB_PORT=5432
```

**⚠️ Importante:** 
- Nunca commitar `.env` com credenciais reais
- Usar valores diferentes para produção
- Gerar nova `SECRET_KEY` antes de deploy

---

## 🏗️ Arquitetura - Domain-Driven Design

O projeto segue **DDD Pragmático** com 4 camadas bem definidas:

```
API Request (HTTP)
    ↓
[Interfaces] — Views REST (HTTP ↔ JSON)
    ↓
[Application] — Orquestração de lógica de negócio
    ↓
[Domain] — Lógica de domínio pura (services)
    ↓
[Infrastructure] — Persistência, APIs externas
    ↓
Database (PostgreSQL)
```

### Exemplo: Busca Semântica

1. **Interface** (`interfaces/views.py`): Recebe request HTTP
2. **Application** (`application/game_service.py`): Orquestra a busca
3. **Infrastructure** (`infrastructure/embedding_client.py`): Chama OpenAI
4. **Models** (`models.py`): Persiste embeddings
5. **Domain** (`domain/services.py`): Lógica pura (pgvector distance)

---

## 📦 Dependências Principais

```
Django==6.0.5
djangorestframework==3.17.1
djangorestframework-simplejwt==5.5.1
django-cors-headers==4.9.0
django-jazzmin==3.0.4
psycopg2-binary==2.9.12
pgvector==0.4.2
openai==2.36.0
python-dotenv==1.2.2
pydantic==2.13.4
```

Para lista completa, veja [requirements.txt](backend/requirements.txt)

---

## 🚀 Deploy em Produção

### Pré-requisitos
- Servidor com Docker e Docker Compose
- Domínio configurado
- Certificado SSL/TLS
- Variáveis de ambiente seguras

### Checklist
- [ ] `DEBUG=False` em `.env`
- [ ] `SECRET_KEY` aleatória e forte
- [ ] `ALLOWED_HOSTS` com seu domínio
- [ ] `CORS_ALLOWED_ORIGINS` com origem do frontend
- [ ] Banco de dados com backup automático
- [ ] HTTPS habilitado
- [ ] Logs centralizados
- [ ] Monitoramento ativo


---

## 📚 Documentação Adicional

- [Documentação Técnica Detalhada](docs/backend.md) — Análise profunda de cada componente
- [Coleção Postman](docs/GameRAG.postman_collection.json) — Testes de endpoints
- [Código-fonte](backend/) — Comentários inline

---

## 🛠️ Desenvolvimento

### Setup de Desenvolvimento

```bash
# Instalar dependências de dev
pip install -r requirements-dev.txt

# Rodar em modo watch
python manage.py runserver --reload

# Pre-commit hooks
pre-commit install
```

### Padrões de Código

- **Python**: PEP 8 (verificado com Flake8)
- **Nomes**: snake_case para funções/variáveis, PascalCase para classes
- **Docstrings**: Format Google
- **Testes**: Padrão `test_*.py` com unittest

### Git Workflow

```bash
# Feature branch
git checkout -b feature/sua-feature

# Commit mensagens significativas
git commit -m "feat: descrição da mudança"
git commit -m "fix: corrigir bug específico"
git commit -m "refactor: melhorar código"

# Push e abrir PR
git push origin feature/sua-feature
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Roadmap Futuro

- [ ] Chat RAG funcional (LLM + embeddings como contexto)
- [ ] Frontend integrado (React/Vue)
- [ ] Redis cache para buscas frequentes
- [ ] Celery para processamento assíncono de embeddings
- [ ] GraphQL API (alternativa REST)
- [ ] WebSocket para chat real-time
- [ ] Recomendação personalizada por usuário
- [ ] Analytics de uso

---

## 📝 Licença

Este projeto está sob licença MIT. Veja [LICENSE](LICENSE) para detalhes.

---

## 👨‍💻 Autor

Desenvolvido por Estevão, Gabriel, e Guilherme.

---

## 📧 Contato e Suporte

- **Issues**: [GitHub Issues](../../issues)
- **Discussões**: [GitHub Discussions](../../discussions)
- **Email**: seu.email@example.com

---

## 🙏 Agradecimentos

- OpenAI pela excelente API de embeddings
- Django e DRF pela framework robusta
- PostgreSQL + pgvector pela busca vetorial

---

**Última atualização:** Maio 2024  
**Status:** Em desenvolvimento ativo 🚀
