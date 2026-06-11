# GameRAG

Sistema de catálogo e recomendação de jogos com busca semântica usando embeddings de IA. Combina Django REST API com Vue 3 frontend, PostgreSQL com pgvector para busca vetorial e OpenAI para geração de embeddings.

## 📋 Visão Geral

GameRAG é uma aplicação completa para:
- **Catálogo de Jogos**: Gerenciamento centralizado de jogos com múltiplos atributos
- **Busca Semântica**: Recomendações baseadas em embeddings de OpenAI
- **Sistema de Usuários**: Autenticação JWT, perfis, favoritos e histórico de interações
- **Chat**: Interface integrada para interação com o sistema

## 🛠️ Stack de Tecnologias

### Backend
- **Python 3.12** com **Django 6.0.5**
- **Django REST Framework 3.17.1** para API REST
- **PostgreSQL 17** com extensão `pgvector` para busca vetorial
- **OpenAI embeddings** via SDK oficial para geração de vetores
- **JWT** via `djangorestframework-simplejwt` para autenticação
- **CORS** via `django-cors-headers` para integração frontend
- **Django Admin customizado** com `django-jazzmin`
- **Gerenciamento de ambiente** com `python-dotenv`
- **Psycopg2** para driver PostgreSQL

### Frontend
- **Vue 3** (Composition API)
- **Vite** como bundler de aplicação
- **Tailwind CSS** para estilização
- **Pinia** para gerenciamento de estado
- **Vue Router** para roteamento
- **Axios** para requisições HTTP

### Infraestrutura
- **Docker & Docker Compose** para orquestração
- **PostgreSQL 17** com `pgvector` para embeddings
- **Volume persistente** para dados do banco de dados
- Portas padrão:
  - Backend: `http://localhost:8000`
  - Frontend: `http://localhost:5173`
  - Database: `localhost:5432`

## 📁 Estrutura do Projeto

```
GameRAG/
├── backend/                          # Django REST API
│   ├── GameRAG/                      # Configurações do projeto
│   │   ├── settings.py               # Configurações Django
│   │   ├── urls.py                   # URLs principais
│   │   ├── asgi.py & wsgi.py        # Aplicação ASGI/WSGI
│   ├── chat/                         # App de chat
│   │   ├── application/              # Lógica de negócios
│   │   ├── interfaces/               # ViewSets e Serializers
│   │   └── tests/                    # Testes unitários
│   ├── games/                        # App principal de jogos
│   │   ├── application/              # Serviços (recomendação, embeddings)
│   │   ├── infrastructure/           # Cliente de embeddings
│   │   ├── interfaces/               # ViewSets, Serializers e URLs
│   │   ├── management/commands/      # Comandos customizados (seed, embeddings)
│   │   └── tests/                    # Testes abrangentes
│   ├── users/                        # App de usuários
│   │   ├── application/              # Lógica de autenticação
│   │   ├── interfaces/               # ViewSets e Serializers
│   │   ├── management/commands/      # Criação de admin
│   │   └── tests/                    # Testes de usuários
│   ├── requirements.txt              # Dependências Python
│   ├── manage.py                     # CLI Django
│   ├── Dockerfile                    # Build do backend
│   └── .env.example                  # Exemplo de variáveis de ambiente
│
├── frontend/                         # Vue 3 + Vite SPA
│   ├── src/
│   │   ├── components/               # Componentes Vue reutilizáveis
│   │   │   ├── ChatWidget.vue        # Widget de chat
│   │   │   ├── GameCard.vue          # Card de jogo
│   │   │   ├── Header.vue            # Cabeçalho com navegação
│   │   │   └── ThemeToggle.vue       # Alternar tema claro/escuro
│   │   ├── views/                    # Páginas da aplicação
│   │   │   ├── LoginView.vue         # Autenticação
│   │   │   ├── PesquisaView.vue      # Busca e recomendação
│   │   │   ├── PerfilView.vue        # Perfil do usuário
│   │   │   └── ConfiguracoesView.vue # Configurações
│   │   ├── router/                   # Definição de rotas
│   │   ├── stores/                   # Pinia stores (auth, theme)
│   │   ├── services/                 # Cliente HTTP (Axios)
│   │   └── main.js                   # Entrada da aplicação
│   ├── package.json                  # Dependências Node.js
│   ├── vite.config.js                # Configuração Vite
│   ├── tailwind.config.js            # Configuração Tailwind
│   ├── Dockerfile                    # Build do frontend
│   └── index.html                    # Arquivo HTML raiz
│
├── docker-compose.yml                # Orquestração de containers
├── README.md                         # Este arquivo
└── docs/
    ├── backend.md                    # Documentação da API
    └── GameRAG.postman_collection.json # Collection Postman
```

## 🚀 Funcionalidades Principais

### Backend API
- **CRUD de Jogos**: Criação, leitura, atualização e deleção de jogos
- **Embeddings Vetoriais**: Geração automática de embeddings via OpenAI
- **Recomendações**: Motor de recomendação baseado em similaridade vetorial
- **Autenticação JWT**: Endpoints protegidos por token JWT
- **Gerenciamento de Usuários**: Registro, login, perfil, favoritos
- **Sistema de Interações**: Avaliações, histórico de visualizações
- **Admin Django Customizado**: Interface jazzmin para gerenciamento

### Frontend
- **Autenticação**: Login com persistência de token
- **Busca e Recomendação**: Interface para pesquisar jogos
- **Perfil Personalizado**: Gerenciamento de dados do usuário
- **Modo Claro/Escuro**: Tema toggleável
- **Chat Integrado**: Widget de chat para interações
- **Responsivo**: Designado para desktop e mobile

## 📋 Pré-requisitos

- **Docker e Docker Compose** (v20.10+)
- **OpenAI API Key** (obtenha em https://platform.openai.com)
- Git para clonar o repositório
- Porta 5432, 8000 e 5173 disponíveis localmente

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

## ⚡ Início Rápido

### 1. Configurar Variáveis de Ambiente

```bash
cd backend
cp .env.example .env
```

Edite `backend/.env` e preencha:
```env
OPENAI_API_KEY=sua_chave_openai_aqui
SEED_DATA=true              # Popula DB automaticamente ao iniciar
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

### 2. Iniciar a Aplicação

```bash
docker compose up --build
```

Aguarde até que todos os serviços estejam saudáveis:
- **PostgreSQL**: Pronto quando healthcheck passar
- **Backend**: API disponível em http://localhost:8000
- **Frontend**: Aplicação disponível em http://localhost:5173

### 3. Acessar o Sistema

- **Frontend**: http://localhost:5173
- **API**: http://localhost:8000/api
- **Django Admin**: http://localhost:8000/admin (credenciais definidas em .env)
- **API Docs**: http://localhost:8000/api/schema/swagger/ (caso disponível)

## 🔐 Admin Django

O projeto expõe Django Admin em `/admin/`, protegido por login e senha.

### Criar Administrador

#### Opção 1: Automática (Recomendado)
Configure em `backend/.env`:
```env
ADMIN_USERNAME=seu_usuario
ADMIN_PASSWORD=sua_senha
```

Ao iniciar o container, o usuário será criado automaticamente se não existir.

#### Opção 2: Manual via Terminal
```bash
# Com Docker Compose
docker compose exec backend python manage.py create_admin_user

# Ou localmente (após setup manual)
cd backend
python manage.py create_admin_user
```

#### Opção 3: Django createsuperuser Padrão
```bash
docker compose exec backend python manage.py createsuperuser
```

## 🏃 Como Rodar o Projeto

### Com Docker Compose (Recomendado)

```bash
# Build e inicia todos os serviços
docker compose up --build

# Apenas inicia os serviços (sem rebuild)
docker compose up

# Em modo background
docker compose up -d

# Parar os serviços
docker compose down

# Remover volumes (limpar dados)
docker compose down -v
```

### Executar Comandos no Backend

```bash
# Seed de dados
docker compose exec backend python manage.py seed_data

# Seed apenas de jogos (sem usuários/avaliações)
docker compose exec backend python manage.py seed_data --no-interactions

# Gerar embeddings para jogos existentes
docker compose exec backend python manage.py generate_embeddings

# Migrações de banco de dados
docker compose exec backend python manage.py migrate

# Criar superusuário
docker compose exec backend python manage.py createsuperuser
```

### Setup Local (Desenvolvimento sem Docker)

```bash
# Backend
cd backend
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py create_admin_user
python manage.py runserver

# Frontend (novo terminal)
cd frontend
npm install
npm run dev
```

## 📊 Popular Dados de Exemplo

O projeto pode popular automaticamente o banco de dados ao iniciar:

### Automático via Docker

Configure em `backend/.env`:
```env
SEED_DATA=true
```

O container executará `python manage.py seed_data` automaticamente após aplicar migrations.

### Manual

```bash
# Com Docker
docker compose exec backend python manage.py seed_data

# Localmente
python manage.py seed_data

# Apenas jogos (sem usuários/avaliações/favoritos)
python manage.py seed_data --no-interactions
```

Isso cria:
- ✅ 10+ jogos com metadados completos
- ✅ Embeddings via OpenAI
- ✅ Usuários de exemplo
- ✅ Avaliações e interações
- ✅ Dados de favoritos e biblioteca

## 📚 Documentação

- [Backend API Documentation](docs/backend.md) - Endpoints, autenticação e modelos
- [Postman Collection](docs/GameRAG.postman_collection.json) - Collection para testar API
- [Frontend Documentation](docs/frontend.md) - Componentes e estrutura

## 🔌 Principais Endpoints da API

### Autenticação
- `POST /api/users/login/` - Autenticação e obtenção de JWT
- `POST /api/users/register/` - Registro de novo usuário
- `POST /api/token/refresh/` - Renovar token JWT

### Jogos
- `GET /api/games/` - Listar todos os jogos
- `GET /api/games/{id}/` - Detalhes de um jogo
- `GET /api/games/recommendations/` - Obter recomendações
- `POST /api/games/{id}/rate/` - Avaliar um jogo
- `POST /api/games/{id}/favorite/` - Adicionar aos favoritos

### Usuários
- `GET /api/users/profile/` - Perfil do usuário autenticado
- `PUT /api/users/profile/` - Atualizar perfil
- `GET /api/users/favorites/` - Listar favoritos do usuário
- `GET /api/users/library/` - Biblioteca do usuário

### Chat
- `POST /api/chat/messages/` - Enviar mensagem ao chat
- `GET /api/chat/history/` - Histórico de chat

## 🐛 Troubleshooting

### Erro: "Permission denied" ao executar docker compose

```bash
# Adicione seu usuário ao grupo docker
sudo usermod -aG docker $USER
# Faça logout e login novamente, ou
newgrp docker
```

### Erro: "Port already in use"

```bash
# Verifique qual processo usa a porta
lsof -i :8000    # Backend
lsof -i :5173    # Frontend
lsof -i :5432    # Database

# Matando o processo (Linux/Mac)
kill -9 <PID>

# Ou use diferentes portas no docker-compose.yml
```

### PostgreSQL recusando conexão

```bash
# Verifique se o container está rodando
docker compose ps

# Veja os logs do database
docker compose logs db

# Recrie o volume
docker compose down -v
docker compose up --build
```

### "Invalid OpenAI API Key"

```bash
# Verifique se a chave está configurada
docker compose exec backend echo $OPENAI_API_KEY

# Atualize a chave em backend/.env e reinicie
docker compose restart backend
```

### Embeddings não são gerados

```bash
# Execute manualmente
docker compose exec backend python manage.py generate_embeddings

# Ou gere junto com seed
docker compose exec backend python manage.py seed_data
```

## 🛠️ Desenvolvimento

### Instalar Dependências Adicionais

```bash
# Backend
docker compose exec backend pip install novo_pacote

# Frontend
docker compose exec frontend npm install novo_pacote
```

### Executar Testes

```bash
# Testes do backend
docker compose exec backend python manage.py test

# Ou com coverage
docker compose exec backend coverage run -m manage test
docker compose exec backend coverage report
```

### Acessar o Shell Django

```bash
docker compose exec backend python manage.py shell
```

## 📦 Variáveis de Ambiente

### Backend (.env)

```env
# OpenAI
OPENAI_API_KEY=sk-...

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=gamerag
DB_USER=gamerag
DB_PASSWORD=gamerag
DB_HOST=db
DB_PORT=5432

# Admin
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# Seed
SEED_DATA=true

# Django
DEBUG=False
SECRET_KEY=sua-chave-secreta-aqui
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

### Frontend (Variáveis de Build)

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

## 🤝 Contribuindo

1. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
2. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
3. Push para a branch (`git push origin feature/AmazingFeature`)
4. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue no repositório.

---

**Última atualização**: Junho 2026
