# Publicacao no GitHub

Data de preparacao: 2026-05-28.

## Objetivo do Repositorio

Publicar a `QualidadeAmbiental API` como projeto backend profissional de portfolio, demonstrando arquitetura em camadas, FastAPI, SQL Server, endpoints read-only, contratos REST, testes automatizados, documentacao tecnica e evolucao incremental.

Esta etapa prepara o projeto para publicacao. O push para o repositorio remoto deve ser executado em uma etapa separada, apos confirmacao da URL do repositorio.

## Estado Tecnico

| Item | Status |
| ---- | ------ |
| FastAPI | Implementado |
| SQL Server real | Validado |
| API read-only | Confirmada |
| OpenAPI/Swagger | Validado |
| Testes automatizados | 73 passed |
| Cobertura automatizada | 65% com `pytest-cov` |
| Tratamento padronizado de erro | Implementado |
| Logging basico | Implementado |
| Documentacao tecnica | Consolidada |
| Git | Limpo antes da publicacao |
| CI remoto | Aprovado em 2026-05-29 |
| Release inicial | Publicada em 2026-05-29 |

## Tecnologias

- Python 3.12
- FastAPI
- SQLAlchemy
- pyodbc
- SQL Server
- Pydantic
- pytest
- pytest-cov
- Uvicorn

## Pre-requisitos

- Python 3.12+
- SQL Server acessivel
- Driver ODBC para SQL Server
- Ambiente virtual `.venv`
- Arquivo `.env` local criado a partir de `.env.example`

## Seguranca

Antes da publicacao, foram auditados:

- `.gitignore`;
- arquivos rastreados pelo Git;
- `.env.example`;
- README;
- documentacao tecnica;
- codigo-fonte;
- testes.

Regras confirmadas:

- `.env` nao deve ser versionado;
- `.venv/` nao deve ser versionado;
- snapshots `.zip` em `backup/` nao devem ser versionados;
- logs e caches nao devem ser versionados;
- credenciais reais nao devem aparecer em README, docs, codigo ou testes;
- connection strings reais nao devem ser expostas.

## Como Executar Localmente

Criar ambiente virtual:

```powershell
python -m venv .venv
```

Instalar dependencias:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Criar `.env` local:

```powershell
copy .env.example .env
```

Executar API:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Executar testes:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Executar cobertura:

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=app --cov-report=term-missing
```

## URLs Locais

| Servico | URL |
| ------- | --- |
| Health | `http://127.0.0.1:8000/health` |
| Swagger | `http://127.0.0.1:8000/docs` |
| ReDoc | `http://127.0.0.1:8000/redoc` |

## Estrutura

```text
app/
  core/
  routers/
  services/
  repositories/
  schemas/
  models/
  utils/
docs/
tests/
backup/
```

## Politica de Contribuicoes Futuras

Contribuicoes futuras devem respeitar:

- arquitetura `router -> service -> repository`;
- API read-only ate decisao tecnica formal;
- nenhum SQL em routers;
- nenhum segredo versionado;
- testes automatizados para mudancas funcionais;
- documentacao atualizada junto com alteracoes relevantes;
- snapshots locais apenas em `backup/`, sem versionar arquivos compactados.

## Checklist de Publicacao

- [x] `.gitignore` auditado.
- [x] `.env` ignorado pelo Git.
- [x] Arquivos rastreados auditados com `git ls-files`.
- [x] Busca por possiveis segredos executada.
- [x] `.env.example` sanitizado.
- [x] README revisado como produto GitHub.
- [x] Testes executados com sucesso.
- [x] Snapshot de preparacao criado.
- [x] URL do repositorio remoto confirmada.
- [x] Remote GitHub configurado.
- [x] Push inicial executado.
- [x] GitHub Actions configurado para testes.
- [x] Badge de testes adicionado ao README.
- [x] Tag/release inicial avaliada.
- [x] CI remoto validado com sucesso.
- [x] Release `v0.3.0-readonly-analytics` criada.

## Tag Sugerida

Tag recomendada para a primeira publicacao:

```text
v0.3.0-readonly-analytics
```

Motivo: o projeto esta maduro como API read-only analitica e ja possui CI de testes, mas ainda nao possui Docker, autenticacao ou deploy produtivo.

## CI com GitHub Actions

Workflow configurado:

```text
.github/workflows/tests.yml
```

O workflow executa em:

- `push`;
- `pull_request`.

Etapas:

- checkout do repositorio;
- Python 3.12;
- instalacao de `unixodbc-dev`;
- instalacao de dependencias do `requirements.txt`;
- execucao de `pytest` com cobertura via `pytest-cov`.

Os testes automatizados nao dependem do SQL Server real.

## Validacao do CI Remoto

Validado em 2026-05-29:

| Item | Resultado |
| ---- | --------- |
| Workflow | `Tests` |
| Branch | `master` |
| Tag | `v0.3.0-readonly-analytics` |
| Status | `success` |
| Job | `pytest` com cobertura |
| Dependencia de SQL Server real | Nao |

Observacao: o GitHub Actions apresentou apenas uma anotacao informativa sobre futura migracao de actions baseadas em Node.js 20 para Node.js 24. Essa anotacao nao bloqueou o CI.

## Release Inicial

Release criada em 2026-05-29:

| Item | Valor |
| ---- | ----- |
| Tag | `v0.3.0-readonly-analytics` |
| Titulo | `v0.3.0 - Read-only Analytics API` |
| URL | `https://github.com/engambientalucas-design/-QualidadeAmbiental-API/releases/tag/v0.3.0-readonly-analytics` |

Descricao:

```text
Primeira release versionada da QualidadeAmbiental API, com camada read-only e analitica consolidada, endpoints validados, documentacao tecnica, testes automatizados e CI com GitHub Actions.
```
