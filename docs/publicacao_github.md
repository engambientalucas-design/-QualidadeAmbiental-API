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
| Testes automatizados | 41 passed |
| Tratamento padronizado de erro | Implementado |
| Logging basico | Implementado |
| Documentacao tecnica | Consolidada |
| Git | Limpo antes da publicacao |

## Tecnologias

- Python 3.12
- FastAPI
- SQLAlchemy
- pyodbc
- SQL Server
- Pydantic
- pytest
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
- [ ] URL do repositorio remoto confirmada.
- [ ] Remote GitHub configurado.
- [ ] Push inicial executado.
- [ ] Tag/release inicial avaliada.

## Tag Sugerida

Tag recomendada para a primeira publicacao:

```text
v0.3.0-readonly-analytics
```

Motivo: o projeto esta maduro como API read-only analitica, mas ainda nao possui CI/CD, Docker, autenticacao ou release produtiva.
