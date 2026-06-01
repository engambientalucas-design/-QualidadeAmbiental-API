# Dockerizacao Local

Data de criacao: 2026-05-29.

## Objetivo

Permitir a execucao local da `QualidadeAmbiental API` em container Docker, mantendo a API read-only e a conexao com SQL Server configuravel por variaveis de ambiente.

Esta fase containeriza apenas a API. O SQL Server nao e containerizado nesta etapa.

## Pre-requisitos

- Docker Desktop instalado e em execucao.
- Docker Compose disponivel via `docker compose`.
- Arquivo `.env` local criado a partir de `.env.example`.
- SQL Server acessivel a partir do host ou da rede usada pelo container.

## Arquivos Criados

| Arquivo | Objetivo |
| ------- | -------- |
| `Dockerfile` | Cria imagem Python 3.12 slim com dependencias da API e Microsoft ODBC Driver 18. |
| `.dockerignore` | Evita copiar credenciais, caches, backups, logs, `.venv` e relatorios para a imagem. |
| `docker-compose.yml` | Sobe o servico `qualidadeambiental-api` na porta 8000. |

## Variaveis de Ambiente

O container usa as mesmas variaveis `QA_API_` da aplicacao local:

```text
QA_API_DB_SERVER=host.docker.internal
QA_API_DB_PORT=1433
QA_API_DB_NAME=QualidadeAmbiental
QA_API_DB_USER=
QA_API_DB_PASSWORD=
QA_API_DB_DRIVER=ODBC Driver 18 for SQL Server
QA_API_DB_ENCRYPT=no
QA_API_DB_TRUST_SERVER_CERTIFICATE=true
```

Importante: em Docker no Windows, `localhost` dentro do container aponta para o proprio container. Quando o SQL Server estiver rodando na maquina host, use:

```text
QA_API_DB_SERVER=host.docker.internal
```

## Build

```powershell
docker compose build --no-cache
```

## Execucao

```powershell
docker compose up -d
```

Ou:

```powershell
docker compose up -d --build
```

## Acessos Locais

| Servico | URL |
| ------- | --- |
| Health | `http://127.0.0.1:8000/health` |
| Swagger | `http://127.0.0.1:8000/docs` |
| ReDoc | `http://127.0.0.1:8000/redoc` |
| OpenAPI | `http://127.0.0.1:8000/openapi.json` |

## Validacoes Esperadas

Com o container em execucao:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Validar tambem o contrato OpenAPI gerado:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/openapi.json
```

Se o SQL Server host estiver acessivel:

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/api/v1/pontos-coleta?page=1&page_size=2"
```

## Status da Validacao Local

Tentativa realizada em 2026-05-29:

| Item | Resultado |
| ---- | --------- |
| `docker --version` | Nao disponivel no PATH |
| `docker compose version` | Nao disponivel no PATH |
| Instalacao via `winget` | Falhou no instalador com exit code 1 por necessidade de UAC/admin |
| Instalacao elevada/interativa | Retornou sem erro no PowerShell, mas Docker Desktop nao apareceu instalado |
| Build da imagem | Pendente |
| Subida do container | Pendente |
| `/health` em container | Pendente |
| Endpoint com SQL Server via container | Pendente |

Pendencia:

- instalar/abrir Docker Desktop manualmente com permissao de administrador;
- garantir que `docker --version` e `docker compose version` funcionem em novo terminal;
- repetir `docker compose build` e `docker compose up`.

### Tentativa de validacao em 2026-06-01

| Item | Resultado |
| ---- | --------- |
| `docker --version` | Falhou: comando `docker` nao reconhecido no PowerShell |
| `docker compose version` | Falhou: comando `docker` nao reconhecido no PowerShell |
| Docker Engine (`docker info`) | Nao executado porque o CLI Docker nao esta disponivel |
| Docker Context (`docker context ls`) | Nao executado porque o CLI Docker nao esta disponivel |
| `docker compose build --no-cache` | Nao executado |
| `docker compose up -d` | Nao executado |
| `/health` em container | Nao validado |
| `/docs` em container | Nao validado |
| `/redoc` em container | Nao validado |
| `/openapi.json` em container | Nao validado |
| Endpoint com SQL Server via container | Nao validado |

Conclusao: a Fase 3.3.1 permanece bloqueada ate o Docker Desktop estar instalado, aberto e disponivel no PATH do terminal.

Quando o Docker estiver disponivel, a validacao deve ser retomada nesta ordem:

```powershell
docker --version
docker compose version
docker info
docker context ls
docker compose build --no-cache
docker compose up -d
docker compose ps
docker compose logs --tail=100
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-RestMethod http://127.0.0.1:8000/openapi.json
```

Para SQL Server rodando no host Windows, confirmar antes da validacao de endpoint:

```text
QA_API_DB_SERVER=host.docker.internal
```

Se a conexao local usar autenticacao integrada do Windows, a validacao do banco a partir de container Linux pode falhar mesmo com rede correta. Nesse caso, a pendencia deve ser registrada explicitamente. A solucao tecnica recomendada para Docker e usar um SQL Login configurado por variaveis `QA_API_DB_USER` e `QA_API_DB_PASSWORD`, sem versionar credenciais reais.

## Limitacoes da Fase Atual

- SQL Server nao e containerizado.
- CI do GitHub Actions continua executando testes Python com cobertura, sem build Docker.
- Validacao real com banco em container depende de conectividade entre container e SQL Server host.
- Credenciais reais continuam fora do Git.

## Evolucao Futura

Possiveis proximas melhorias:

- validar build Docker no GitHub Actions;
- criar profile opcional para testes de integracao;
- avaliar SQL Server containerizado apenas se fizer sentido para testes automatizados;
- publicar imagem em registry somente em fase de release/deploy.
