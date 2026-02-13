# Case PicPay - Machine Learning Engineer Sênior

Um projeto desenvolvido como case técnico para a vaga de **Engenheiro de Machine Learning Sênior** no PicPay, composto por **2 etapas principais**.

## 📋 Sobre o Projeto

### Etapa 1: Pipeline de Extração e Processamento de Dados 📊
Implementação de um **pipeline assíncrono de ingestão de dados** que extrai informações da PokeAPI, realiza processamento em lote e persiste os dados em **Delta Lake no Databricks**. Utiliza requisições paralelas controladas, validação com Pydantic e streaming assincrono para garantir escalabilidade e eficiência.

📓 **Localização**: [`Case Machine Learning Engineer Sênior.ipynb`](Case%20Machine%20Engineer%20Sênior.ipynb)

**Tecnologias**: Python, AsyncIO, Pydantic, httpx, Databricks, Delta Lake, PySpark

### Etapa 2: API REST com Load Balancing 🚀
Uma **arquitetura escalável baseada em FastAPI** com integração de **processamento de linguagem natural (NLP)** utilizando Spacy, persistência de dados em **MongoDB** e um sistema de load balancing com **Nginx**. A aplicação é containerizada com Docker e pode ser facilmente escalonada para múltiplas instâncias de API.

📍 **Localização**: Este repositório (diretório `src/`)

## 🛠️ Tecnologias

### Etapa 1 - Pipeline de Dados
- **Python**: Processamento assíncrono
- **AsyncIO & httpx**: Requisições paralelas controladas
- **Pydantic**: Validação de dados e modelos
- **aiostream**: Processamento de streaming
- **Databricks & Delta Lake**: Data Lakehouse
- **PySpark**: Processamento distribuído

### Etapa 2 - API REST
- **Python**: 3.13.5+
- **FastAPI**: Framework web moderno e de alta performance
- **Spacy**: Biblioteca de NLP para processamento avançado de texto
- **MongoDB**: Banco de dados NoSQL escalável
- **Nginx**: Reverse proxy e load balancer
- **Docker & Docker Compose**: Containerização e orquestração
- **Pydantic**: Validação de dados e configurações
- **PyMongo**: Driver MongoDB para Python

## 📁 Estrutura do Projeto

```
.
├── Case Machine Learning Engineer Sênior.ipynb  # Etapa 1: Pipeline de ingestão
├── src/                            # Etapa 2: API REST
│   ├── main.py                     # Aplicação FastAPI principal
│   ├── models.py                   # Modelos Pydantic (LoadModelRequest, PredictRequest, etc)
│   ├── core/                       # Configurações centrais
│   ├── middlewares/                # Middlewares da aplicação
│   ├── routing/                    # Rotas e endpoints
│   ├── services/                   # Lógica de negócio e NLP
│   ├── repositories/               # Camada de acesso a dados (MongoDB)
│   └── __pycache__/                # Cache Python
├── tests/                          # Testes automatizados
│   ├── unit/                       # Testes unitários
│   ├── controller/                 # Testes de controller/endpoints
│   ├── mock/                       # Dados e fixtures para testes
│   ├── conftest.py                 # Configuração pytest
│   └── __init__.py
├── .github/workflows/
│   └── ci.yml                      # Pipeline CI/CD (Lint, Format, Type Check, Tests)
├── nginx/
│   └── nginx.conf                  # Configuração do reverse proxy
├── docker-compose.yml              # Orquestração de containers
├── Dockerfile                      # Build da imagem Docker
├── requirements.txt                # Dependências Python
├── pyproject.toml                  # Metadados do projeto
└── README.md                       # Este arquivo
```

## 🚀 Etapa 1: Pipeline de Ingestão de Dados

### Sobre

Este notebook implementa um pipeline **assíncrono e escalável** para:

1. **Extração de dados** da PokeAPI com requisições paralelas controladas
2. **Validação** de dados usando Pydantic models com regras de negócio
3. **Processamento em batches** para otimizar performance
4. **Ingestão em Delta Lake** no Databricks
5. **Suporte a rollback lógico** em caso de falhas

### Tecnologias Utilizadas

- **httpx**: Cliente HTTP assíncrono para requisições paralelas
- **asyncio & aiostream**: Processamento assíncrono e streaming
- **Pydantic**: Validação rigorosa de dados e modelos
- **PySpark SQL**: Transformações distribuídas
- **Delta Lake**: Garantias ACID e versionamento de dados

### Como Executar

1. Abrir o notebook: [`Case Machine Learning Engineer Sênior.ipynb`](Case%20Machine%20Engineer%20Sênior.ipynb)
2. Executar as células sequencialmente (requer acesso a cluster Databricks)
3. O notebook criará/atualizará tabelas Delta Lake automaticamente

---

## 🚀 Etapa 2: API REST

### Inicio Rápido - Etapa 2

#### Requisitos

- Docker e Docker Compose instalados
- Git

#### Instalação e Execução Local

Para executar o projeto localmente com 3 instâncias de API e load balancing automático via Nginx:

```bash
docker compose up --build --scale api=3 -d
```

Este comando irá:

1. **Build** da imagem Docker da aplicação
2. **Inicialização** do MongoDB como banco de dados
3. **Escalamento** de 3 instâncias paralelas da API FastAPI
4. **Configuração** do Nginx como load balancer
5. **Execução em background** (-d flag)

#### Acessando a Aplicação

Após a execução, a aplicação estará disponível em:

- **API**: `http://localhost:80`
- **Documentação Swagger (opcional)**: `http://localhost:80/docs`

#### Verificação da Saúde

```bash
curl http://localhost/health
```

Resposta esperada:
```json
{"status": "ok"}
```

## 📦 Endpoints Principais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/health` | Verifica o status da aplicação |
| POST | `/predict` | Realiza predição de entidades usando modelo Spacy |
| GET | `/history` | Retorna histórico de predições do MongoDB |
| POST | `/load` | Carrega um modelo Spacy específico |

## 📊 Modelos de Dados

### LoadModelRequest
```python
{
  "model": "pt_core_news_sm"
}
```

### PredictRequest
```python
{
  "model": "pt_core_news_sm",
  "text": "Quero transferir R$ 1000 para João em 25 de janeiro"
}
```

### PredictionModel (Resposta)
```python
{
  "_id": ObjectId,
  "model": "pt_core_news_sm",
  "text": "Quero transferir R$ 1000 para João em 25 de janeiro",
  "entities": {
    "money": 1000.0,
    "person": "João",
    "date": "25 de janeiro"
  },
  "timestamp": "2026-02-13T10:30:00"
}
```

## ⚙️ Configuração

As variáveis de ambiente são automaticamente configuradas via Docker Compose:

- `MONGO_URI`: `mongodb://mongo:27017/picpay`
- `HOST`: `0.0.0.0`
- `PORT`: `8000`

Para customizar, edite o arquivo `docker-compose.yml`.

## 🧪 Testes

Para executar os testes:

```bash
docker compose exec api pytest tests/
```

Ou localmente com Poetry:

```bash
poetry run pytest tests/ -v
```

### Estrutura de Testes

- **tests/unit/**: Testes unitários de serviços e lógica
- **tests/controller/**: Testes de endpoints e integração HTTP
- **tests/mock/**: Dados fictícios e fixtures para testes
- **tests/conftest.py**: Configuração e fixtures globais do pytest

Dependências de teste:
- pytest
- ruff (linting)
- mypy (type checking)

## 📊 Arquitetura - Etapa 2

```
        ┌─────────────┐
        │   Nginx     │  (Load Balancer)
        │  (Port 80)  │
        └──────┬──────┘
               │
    ┌───────┬──┴───┬───────┐
    │       │      │       │
┌───▼─┐  ┌──▼──┐ ┌─▼───┐ ┌─▼───┐
│API 1│  │API 2│ │API 3│ │API 4│
│:8000│  │:8000│ │:8000│ │:8000│
└───┬─┘  └──┬──┘ └─┬───┘ └─┬───┘
    │       │      │       │
    └───────┴───┬──┴───────┘
                │
         ┌──────▼───────┐
         │   MongoDB    │
         │  :27017      │
         └──────────────┘
```

## 🔄 Escalabilidade

A aplicação é horizontalmente escalável. Para ajustar o número de instâncias da API:

```bash
# 5 instâncias
docker compose up --build --scale api=5 -d

# 2 instâncias
docker compose up --build --scale api=2 -d
```

O Nginx distribuirá automaticamente as requisições entre as instâncias.

## 📝 Parar a Aplicação

```bash
docker compose down
```

Para remover também os dados persistidos:

```bash
docker compose down -v
```

## 👨‍💻 Desenvolvimento

### Estrutura Recomendada Para Novas Features

1. **Models** (`src/models.py`): Define dataclasses/Pydantic models centralizados
2. **Services** (`src/services/`): Implementa lógica de negócio e processamento NLP
3. **Repositories** (`src/repositories/`): Acesso a dados (MongoDB)
4. **Routing** (`src/routing/`): Define endpoints e rotas FastAPI
5. **Core** (`src/core/`): Configurações e inicializações centrais
6. **Middlewares** (`src/middlewares/`): Interceptadores de requisições

### Dependências de Desenvolvimento

Este projeto utiliza **Poetry** para gerenciamento de dependências.

#### 1. Instalar Poetry

Se ainda não possui Poetry instalado, execute:

```bash
python -m pip install poetry
```

#### 2. Instalar Dependências de Desenvolvimento

No diretório raiz do projeto, instale as dependências incluindo os grupos `dev` e `test`:

```bash
poetry install --with dev --with test
```

Isso irá instalar:
- **Dependências padrão**: FastAPI, Pydantic, PyMongo, Spacy, etc.
- **Dependências dev**: ipykernel (para Jupyter notebooks)
- **Dependências test**: pytest, ruff (linting), mypy (type checking)

#### 3. Executar Comandos no Ambiente Poetry

```bash
# Executar a aplicação
poetry run fastapi run src/main.py

# Executar testes
poetry run pytest tests/ -v --cov

# Executar linting
poetry run ruff check src/

# Executar formatação
poetry run ruff format src/

# Verificar tipos com mypy
poetry run mypy src/
```

### CI/CD - GitHub Actions

Este projeto possui um **pipeline de integração contínua** automatizado que executa:

- **Ruff Lint**: Validação de código e detecção de problemas
- **Ruff Format**: Verificação de formatação de código
- **MyPy**: Type checking para garantir tipagem correta
- **Pytest**: Execução de testes automatizados

O workflow é disparado automaticamente em:
- ✅ Push para `main` ou `develop`
- ✅ Pull Requests para `main`

📄 **Configuração**: [`.github/workflows/ci.yml`](.github/workflows/ci.yml)

## 📄 Licença

Projeto desenvolvido como case técnico.
