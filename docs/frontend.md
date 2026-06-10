# Frontend — GameRAG

Interface de usuário construída com **Vue 3**, **Vite**, **Tailwind CSS** e **Pinia**.

---

## Stack

| Tecnologia | Versão | Papel |
|---|---|---|
| Vue | 3.5.13 | Framework reativo |
| Vite | 6.0.5 | Build tool e dev server |
| Tailwind CSS | 3.4.17 | Utility-first CSS |
| Pinia | 2.2.6 | State management |
| Vue Router | 4.5.0 | Client-side routing |
| Axios | 1.7.7 | HTTP client |

---

## Estrutura de Pastas

```
frontend/
├── index.html              # Ponto de entrada HTML
├── package.json            # Dependências e scripts
├── vite.config.js          # Configuração do Vite
├── tailwind.config.js      # Configuração do Tailwind
├── postcss.config.js       # Configuração do PostCSS
└── src/
    ├── main.js             # Inicialização da aplicação
    ├── App.vue             # Componente raiz
    ├── components/         # Componentes reutilizáveis
    │   ├── Header.vue      # Cabeçalho com navegação
    │   ├── GameCard.vue    # Card de jogo com modal de detalhes
    │   └── ThemeToggle.vue # Alternador de tema dark/light
    ├── views/              # Páginas da aplicação
    │   ├── LoginView.vue   # Autenticação (login e registro)
    │   ├── PesquisaView.vue   # Busca e listagem de jogos
    │   ├── PerfilView.vue  # Perfil e jogos favoritos
    │   └── ConfiguracoesView.vue # Gerenciar conta e senha
    ├── router/
    │   └── index.js        # Definição de rotas
    ├── stores/             # Pinia stores (state)
    │   ├── auth.js         # Estado de autenticação
    │   └── theme.js        # Estado do tema
    └── services/
        └── api.js          # Cliente HTTP com interceptadores
```

---

## Como Rodar

### Desenvolvimento

```bash
cd frontend
npm install
npm run dev
```

Acesse em `http://localhost:5173`.

### Build para Produção

```bash
npm run build
npm run preview
```

---

## Rotas

| Rota | Nome | Componente | Auth | Descrição |
|------|------|-----------|------|-----------|
| `/` | login | LoginView | Guest Only | Tela de login e registro |
| `/pesquisa` | pesquisa | PesquisaView | Required | Busca e listagem de jogos |
| `/perfil` | perfil | PerfilView | Required | Perfil e jogos favoritos |
| `/configuracoes` | configuracoes | ConfiguracoesView | Required | Gerenciar conta |

**Guards:**
- `requiresAuth` — Redireciona para login se não autenticado
- `guestOnly` — Redireciona para pesquisa se já autenticado

---

## Estado (Pinia)

### `useAuthStore()` — `stores/auth.js`

Gerencia autenticação e dados do usuário.

| Estado | Tipo | Descrição |
|--------|------|-----------|
| `access` | String | JWT access token |
| `refresh` | String | JWT refresh token |
| `username` | String | Username do usuário logado |

| Método | Descrição |
|--------|-----------|
| `login(credentials)` | Faz login com username/password |
| `register(data)` | Registra novo usuário |
| `logout()` | Limpa tokens e desloga |
| `isAuthenticated` | Computed — retorna se há token |

### `useThemeStore()` — `stores/theme.js`

Gerencia tema escuro/claro.

| Estado | Tipo | Descrição |
|--------|------|-----------|
| `isDark` | Boolean | True se tema dark ativo |

| Método | Descrição |
|--------|-----------|
| `toggle()` | Alterna entre dark/light |
| `setDark(value)` | Define tema explicitamente |

---

## Componentes

### `Header.vue`

Cabeçalho navegável presente em todas as páginas autenticadas.

**Props:**
- `username: String` — Nome do usuário logado

**Eventos:**
- `@profile-click` — Clique em "Perfil"
- `@settings-click` — Clique em "Configurações"
- `@logout` — Clique em "Sair"
- `@pesquisa` — Clique no logo (volta para pesquisa)

---

### `GameCard.vue`

Card interativo de jogo com modal de detalhes.

**Props:**
- `game: Object` — Dados do jogo
  - `id, title, description, genre, platform, price, developer, publisher, release_date, rating, tags`
- `showPrice: Boolean` (default `true`) — Exibir preço no card
- `showPlatformBadge: Boolean` (default `true`) — Exibir plataforma no card

**Funcionalidades:**
- ✅ Modal com detalhes completos do jogo
- ✅ Sistema de avaliações (criar, atualizar, deletar)
- ✅ Favoritar/desfavoritar jogo
- ✅ Exibir média de avaliações
- ✅ Fechar modal com ESC ou clique fora

**Estado Interno:**
- `isDetailsOpen` — Modal aberto/fechado
- `reviews` — Lista de avaliações
- `userReview` — Avaliação do usuário logado
- `isFavorited` — Jogo está favoritado
- `newRating, newComment` — Dados do formulário de avaliação

---

### `ThemeToggle.vue`

Botão simples para alternar tema.

---

## Serviços

### `api.js` — Cliente HTTP

Baseado em Axios com interceptadores automáticos.

**Funcionalidades:**
- ✅ Base URL configurável via `VITE_API_BASE_URL`
- ✅ Injeta token JWT em toda requisição
- ✅ Atualiza access token automaticamente quando expira (refresh token)
- ✅ Remove tokens e desloga se refresh token expirar

**Headers automáticos:**
```javascript
Authorization: Bearer <access_token>
```

**Variáveis de Ambiente:**
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

---

## Fluxos Principais

### 1. **Autenticação**

```
LoginView
  → auth.register() ou auth.login()
    → POST /auth/register/ ou /auth/login/
      ← access + refresh tokens
  → localStorage (tokens + username)
  → Redireciona para /pesquisa
```

### 2. **Busca de Jogos**

```
PesquisaView
  → input busca
    → api.get('/games/', { params: { search: termo } })
      ← lista de jogos
  → Renderiza GameCard para cada jogo
```

### 3. **Detalhes e Avaliação**

```
GameCard (click)
  → openDetails()
    → api.get(/games/{id}/reviews/)
    → api.get(/games/favorites/) → checkFavorited()
    → Modal abre
  
Usuário avalia jogo
  → saveReview()
    → POST /games/{id}/reviews/ { rating, comment }
    → loadReviews() (atualiza lista)
```

### 4. **Favoritos**

```
GameCard (botão favorito)
  → toggleFavorite()
    → POST ou DELETE /games/{id}/favorite/
    → isFavorited = !isFavorited
```

### 5. **Perfil**

```
PerfilView (onMounted)
  → Promise.all([
      api.get('/auth/me/'),
      api.get('/games/favorites/')
    ])
  → Exibe dados do usuário + favoritos
```

### 6. **Mudar Senha**

```
ConfiguracoesView
  → changePassword()
    → POST /auth/change-password/
      { current_password, new_password, confirm_password }
    → Sucesso: exibe mensagem e limpa inputs
    → Erro: exibe mensagem de erro
```

---

## Estilo e Temas

### Tailwind CSS

Toda a estilização usa Tailwind com configuração de dark mode.

**Convenção de cores:**
- **Primário:** `sky-*` (azul claro) — botões, links, destaques
- **Gradiente:** `from-purple-* to-indigo-*` — hero, logos
- **Fundo:** `bg-white dark:bg-slate-950`
- **Texto:** `text-slate-900 dark:text-slate-100`

### Dark Mode

Ativado via classe `dark` no `<html>`. Persistência:

```javascript
// localStorage → theme.isDark
if (isDark) document.documentElement.classList.add('dark')
else document.documentElement.classList.remove('dark')
```

---

## Validações e Erros

### Client-side (Vue)

- Email validation — `<input type="email">`
- Password confirmation — `if (signup.password !== signup.confirm)`
- Senha mínima — `minlength="8"` no input

### Server-side (Django)

Erros retornam em `err.response.data`:
- `detail` — Mensagem geral
- Campo específico — Array de erros para cada campo

**Tratamento:**
```javascript
const fieldErrors = Object.values(data).flat().join(' ')
const message = data?.detail || fieldErrors || 'Erro padrão'
```

---

## Performance e Otimizações

✅ **Lazy loading de rotas** — Components carregados via `() => import()`
✅ **Computed properties** — Memoização automática (formattedPrice, averageRating, etc)
✅ **Pinia stores** — State compartilhado sem prop drilling
✅ **Interceptadores** — Refresh automático de token evita logouts inesperados

⚠️ **Possíveis melhorias:**
- [ ] Skeleton screens no loading de GameCard
- [ ] Virtualização em listas longas
- [ ] Service workers para cache offline
- [ ] Testes unitários (Vue Test Utils)

---

## Variáveis de Ambiente

### `.env.local` (desenvolvimento)

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

### `.env.production` (produção)

```env
VITE_API_BASE_URL=https://api.gamerag.com/api
```

---

## Troubleshooting

| Problema | Causa | Solução |
|----------|-------|--------|
| CORS error | Backend não permite origem | Adicionar origem em `CORS_ALLOWED_ORIGINS` |
| 401 Unauthorized | Token expirado/inválido | Fazer logout e login novamente |
| API não responde | Backend offline | Verificar `VITE_API_BASE_URL` |
| Dark mode não persiste | localStorage bloqueado | Usar private browsing ou checar permissões |
| Modal do jogo não abre | Erro ao carregar reviews | Verificar console — pode ser permissão |

---

## Próximas Features

- [ ] **Biblioteca de Jogos** — Status (want_to_play, playing, completed, dropped) + horas jogadas
- [ ] **Busca Vetorial/RAG** — Integrar endpoint `/games/{id}/similar/`
- [ ] **Chat/Assistant** — Interface para busca conversacional de recomendações
- [ ] **Exportar Perfil** — Download de dados em JSON/CSV
- [ ] **Avatar e Bio** — Customização de perfil
