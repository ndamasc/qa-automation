# QA API Framework 🚀

API REST desenvolvida com **FastAPI + PostgreSQL + SQLAlchemy**, focada em **qualidade de software, testes automatizados e CI/CD**.

Este projeto foi criado como laboratório prático para demonstrar habilidades em:

- Testes de API
- Automação com Pytest
- E2E com Playwright
- Banco de dados relacional
- Arquitetura backend em Python
- Integração contínua com GitHub Actions
- Boas práticas de engenharia de software

---

# Visão Geral

A aplicação permite gerenciamento de usuários com operações CRUD:

- Criar usuário
- Listar usuários
- Buscar por ID
- Atualizar parcialmente
- Remover usuário

Toda a estrutura foi pensada para servir como base de testes automatizados profissionais.

---

# Stack Utilizada

## Backend

- Python 3.12
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- Uvicorn

## Testes

- Pytest
- Playwright
- Faker
- HTTPX

## DevOps

- Docker Compose
- GitHub Actions (CI)

---

# Como rodar

## Usando UV (recomendado)

Instale o UV:

```bash
pip install uv
```

Clone o repositório:

```bash
git clone https://github.com/ndamasc/qa-automation.git
cd qa-api-framework
```

Crie o ambiente virtual:

```bash
uv venv
```

Ative o ambiente virtual.

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
uv sync
```

---

## Executar testes

```bash
uv run pytest tests/ -vv
```

---

## Rodar a API

```bash
uv run uvicorn api.main:app --reload
```



---

# Arquitetura do Projeto

```text
qa-api-framework/
├── api/
│   ├── db/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── tests/
│   ├── fixtures/
│   ├── integration/
│   ├── e2e/
│   └── conftest.py
│
├── utils/
├── docker-compose.yml
├── pyproject.toml
└── README.md
```
