# 🌎 QualidadeAmbiental API

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-green)
![SQL Server](https://img.shields.io/badge/SQL_Server-Database-red)
![pytest](https://img.shields.io/badge/pytest-tests-yellow)
![Status](https://img.shields.io/badge/status-em_desenvolvimento-orange)
![License](https://img.shields.io/badge/license-TBD-lightgrey)

API REST profissional em Python com FastAPI para consulta, organização e exposição de dados de qualidade ambiental a partir do banco SQL Server `QualidadeAmbiental`.

O projeto está sendo desenvolvido de forma incremental, com foco em arquitetura limpa, governança técnica, documentação profissional e evolução segura para cenários reais de integração backend.

---

## 📌 Sobre o Projeto

A `QualidadeAmbiental API` tem como objetivo disponibilizar uma camada REST moderna para consumidores externos como dashboards, frontends, Power BI e outros sistemas que precisam acessar dados ambientais consolidados.

Nesta fase, a API é **read-only**. Isso significa que ela consulta o banco SQL Server sem alterar dados, preservando a integridade do ambiente e permitindo evolução controlada dos contratos de consulta.

Principais características:

✅ API REST profissional  
✅ FastAPI + SQL Server  
✅ Arquitetura em camadas  
✅ Swagger e ReDoc automáticos  
✅ Governança técnica documentada  
✅ Testes automatizados mínimos  
✅ Versionamento profissional com Git  
✅ Evolução incremental por fases  

---

## 🏗️ Arquitetura

O projeto segue uma arquitetura em camadas para separar responsabilidades e facilitar manutenção, testes e evolução dos endpoints.

```text
Cliente
   ↓
Router
   ↓
Service
   ↓
Repository
   ↓
SQL Server
```

| Camada | Responsabilidade |
| ------ | ---------------- |
| `Router` | Define rotas HTTP, parâmetros e contratos expostos pela API. |
| `Service` | Orquestra regras de consulta e coordena o fluxo da aplicação. |
| `Repository` | Centraliza o acesso read-only ao banco de dados. |
| `Schemas` | Define modelos Pydantic para entrada e saída de dados. |
| `Models` | Representa estruturas relacionadas ao banco via SQLAlchemy. |
| `Core` | Concentra configurações, variáveis de ambiente e conexão. |

---

## 🚀 Tecnologias

| Tecnologia | Objetivo |
| ---------- | -------- |
| Python 3.12 | Backend principal |
| FastAPI | Construção da API REST |
| SQLAlchemy | Camada de acesso ao banco |
| pyodbc | Driver de conexão com SQL Server |
| Pydantic | Validação e serialização de dados |
| SQL Server | Banco de dados relacional |
| pytest | Testes automatizados |
| Uvicorn | Servidor ASGI local |

---

## 📂 Estrutura do Projeto

```text
app/
├── core/
├── routers/
├── services/
├── repositories/
├── schemas/
├── models/
└── utils/

docs/
tests/
backup/
```

| Caminho | Objetivo |
| ------- | -------- |
| `app/core/` | Configurações, variáveis de ambiente e conexão com banco. |
| `app/routers/` | Rotas HTTP da API. |
| `app/services/` | Regras de aplicação e orquestração. |
| `app/repositories/` | Consultas e acesso read-only ao SQL Server. |
| `app/schemas/` | Schemas Pydantic de entrada e saída. |
| `app/models/` | Modelos relacionados às tabelas e views. |
| `app/utils/` | Utilitários de resposta, paginação e suporte. |
| `docs/` | Documentação técnica do projeto. |
| `tests/` | Testes automatizados. |
| `backup/` | Snapshots locais ignorados pelo Git. |

---

## 🗄️ Banco de Dados

A API utiliza o banco SQL Server `QualidadeAmbiental`, já inspecionado em modo read-only durante a Fase 2.0.

A inspeção real do banco confirmou tabelas base, views consolidadas, relacionamentos principais, índices, constraints, triggers e volumes iniciais. A partir disso, os contratos da Fase 2 foram planejados antes da implementação dos endpoints de domínio.

| Tipo | Quantidade |
| ---- | ---------- |
| Tabelas base | 9 |
| Views consolidadas | 6 |

Views relevantes para a evolução da API:

- `VW_ConformidadeResultados`
- `VW_ResultadosForaDoPadrao`
- `VW_ConformidadeMensal`

> A API não realiza alterações no SQL Server nesta etapa. O escopo atual é exclusivamente de leitura.

---

## 🔍 Endpoints

| Endpoint | Objetivo | Status |
| -------- | -------- | ------ |
| `GET /health` | Health check da aplicação | ✅ Implementado |
| `GET /api/v1/pontos-coleta` | Listagem de pontos de coleta | ✅ Implementado |
| `GET /api/v1/parametros` | Listagem de parâmetros ambientais | ✅ Implementado |
| `GET /api/v1/amostras` | Listagem de amostras | ✅ Implementado |
| `GET /api/v1/resultados` | Resultados analíticos consolidados | ✅ Implementado |
| `GET /api/v1/resultados/nao-conformidades` | Resultados fora do padrão | ✅ Implementado |
| `GET /api/v1/resultados/sem-limite-referencia` | Resultados sem limite de referência | ✅ Implementado |
| `GET /api/v1/resultados/resumo-mensal` | Resumo mensal de conformidade | ✅ Implementado |
| `GET /api/v1/resultados/parametros-criticos` | Ranking de parâmetros críticos | 📋 Planejado |

### Padrão de resposta

```json
{
  "success": true,
  "message": "Consulta realizada com sucesso.",
  "data": [],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 0
  }
}
```

---

## 🛠️ Execução Local

### Pré-requisitos

- Python 3.12+
- SQL Server acessível
- Driver ODBC compatível com SQL Server
- PowerShell ou terminal equivalente

### Ambiente virtual

```powershell
python -m venv .venv
```

```powershell
.\.venv\Scripts\Activate.ps1
```

### Instalação

```powershell
pip install -r requirements.txt
```

### Configuração `.env`

Copie o arquivo de exemplo:

```powershell
copy .env.example .env
```

Edite o `.env` com os dados reais do SQL Server.

As variáveis da aplicação usam o prefixo `QA_API_` para evitar conflito com variáveis globais do sistema, por exemplo:

```text
QA_API_DEBUG=true
QA_API_DB_SERVER=localhost
QA_API_DB_NAME=QualidadeAmbiental
QA_API_DB_ENCRYPT=no
```

### VS Code

O projeto versiona uma configuração segura em `.vscode/settings.json` para padronizar o ambiente local:

```json
{
  "python.defaultInterpreterPath": ".venv\\Scripts\\python.exe",
  "python.envFile": "${workspaceFolder}/.env",
  "python.terminal.useEnvFile": true
}
```

A aplicação já lê o `.env` diretamente via `pydantic-settings`. A configuração `python.terminal.useEnvFile` garante que o terminal integrado do VS Code também injete as variáveis `QA_API_` ao abrir um novo terminal.

Para validar no terminal integrado:

```powershell
echo $env:QA_API_DB_NAME
echo $env:QA_API_DB_DRIVER
```

### Execução

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

### Acessos locais

| Serviço | URL |
| ------- | --- |
| Health | http://127.0.0.1:8000/health |
| Swagger | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |

---

## 🧪 Testes

O projeto utiliza `pytest` para validação automatizada da API.

Execute:

```powershell
pytest
```

Status atual:

- ✅ 34 testes aprovados
- ✅ Endpoint `/health` validado
- ✅ Endpoint `/api/v1/pontos-coleta` validado por contrato
- ✅ Endpoint `/api/v1/parametros` validado por contrato
- ✅ Endpoint `/api/v1/amostras` validado por contrato
- ✅ Endpoint `/api/v1/resultados` validado por contrato
- ✅ Endpoint `/api/v1/resultados/nao-conformidades` validado por contrato
- ✅ Endpoint `/api/v1/resultados/sem-limite-referencia` validado por contrato
- ✅ Endpoint `/api/v1/resultados/resumo-mensal` validado por contrato
- ✅ Paginação e filtros básicos validados

---

## 🔐 Segurança

Medidas já aplicadas no projeto:

- `.env` fora do versionamento Git.
- `.env.example` mantido apenas com valores de exemplo.
- `.gitignore` configurado para ambiente virtual, logs, caches, snapshots e arquivos locais do VS Code.
- `.vscode/settings.json` versionado apenas com configurações seguras de ambiente.
- Snapshots locais compactados em `backup/`, sem versionar arquivos `.zip`.
- API read-only na fase atual.
- Nenhuma migration ou alteração de schema no SQL Server.
- Credenciais reais não devem ser expostas no repositório.

---

## 📘 Documentação Técnica

| Documento | Objetivo |
| --------- | -------- |
| `docs/fases.md` | Evolução do projeto por fases. |
| `docs/modelo_banco.md` | Modelo real inspecionado do banco. |
| `docs/contratos_api_fase2.md` | Contratos planejados para endpoints read-only. |
| `docs/pontos_coleta_endpoint.md` | Documentação técnica do primeiro endpoint read-only. |
| `docs/parametros_endpoint.md` | Documentação técnica do endpoint de parâmetros. |
| `docs/amostras_endpoint.md` | Documentação técnica do endpoint de amostras com joins. |
| `docs/resultados_endpoint.md` | Documentação técnica do endpoint de resultados consolidados. |
| `docs/resultados_nao_conformidades_endpoint.md` | Documentação técnica do endpoint de não conformidades. |
| `docs/resultados_sem_limite_referencia_endpoint.md` | Documentação técnica do endpoint de resultados sem limite. |
| `docs/resumo_mensal_endpoint.md` | Documentação técnica do endpoint de resumo mensal. |
| `docs/versionamento_backup.md` | Política de Git, snapshots e rollback. |
| `docs/decisoes_tecnicas.md` | Decisões arquiteturais e tecnológicas. |
| `docs/checklist_operacional.md` | Checklist antes de mudanças críticas. |

---

## 📈 Roadmap

- [x] Fase 0 - Planejamento e estruturação
- [x] Fase 1 - Base FastAPI
- [x] Fase 1.2 - Governança técnica, versionamento e backup
- [x] Fase 1.3 - Validação local completa
- [x] Fase 2.0 - Inspeção real do banco SQL Server
- [x] Fase 2.1 - Primeiro endpoint read-only: `GET /api/v1/pontos-coleta`
- [x] Fase 2.2 - Endpoint read-only: `GET /api/v1/parametros`
- [x] Fase 2.3 - Endpoint read-only com joins: `GET /api/v1/amostras`
- [x] Fase 2.4 - Endpoint read-only consolidado: `GET /api/v1/resultados`
- [x] Fase 2.5 - Endpoint read-only analítico: `GET /api/v1/resultados/nao-conformidades`
- [x] Fase 2.6 - Endpoint read-only analítico: `GET /api/v1/resultados/sem-limite-referencia`
- [x] Fase 2.7 - Endpoint read-only analítico: `GET /api/v1/resultados/resumo-mensal`
- [ ] Fase 2 - Endpoints de consulta do domínio
- [ ] Fase 3 - Organização profissional, paginação, filtros e erros
- [ ] Fase 4 - Evolução funcional controlada
- [ ] Fase 5 - Validação final e entrega

---

## 👨‍💻 Objetivo Profissional

Este projeto foi estruturado como um backend profissional de portfólio, com foco em demonstrar práticas reais de engenharia de software:

- arquitetura em camadas;
- integração entre FastAPI e SQL Server;
- separação entre documentação, configuração e código;
- governança técnica com Git, snapshots e checklist operacional;
- evolução incremental baseada em fases;
- contratos planejados antes da implementação;
- postura conservadora para banco de dados real.

A proposta é evoluir a API com qualidade, mantendo rastreabilidade técnica e clareza para qualquer pessoa que avalie ou dê manutenção ao projeto.

---

## 📍 Status Atual

| Item | Status |
| ---- | ------ |
| Fase atual | Fase 2.7 concluída |
| Próxima etapa | Fase 2.8 - Ranking de parâmetros críticos |
| API local | Validada |
| Swagger/ReDoc | Ativos |
| Banco SQL Server | Inspecionado em modo read-only |
| Primeiro endpoint de domínio | `GET /api/v1/pontos-coleta` implementado |
| Segundo endpoint de domínio | `GET /api/v1/parametros` implementado |
| Primeiro endpoint com joins | `GET /api/v1/amostras` implementado |
| Primeiro endpoint consolidado por view | `GET /api/v1/resultados` implementado |
| Primeiro endpoint analítico específico | `GET /api/v1/resultados/nao-conformidades` implementado |
| Segundo endpoint analítico específico | `GET /api/v1/resultados/sem-limite-referencia` implementado |
| Endpoint analítico mensal | `GET /api/v1/resultados/resumo-mensal` implementado |
| Validação SQL Server real | Concluída em 2026-05-28 |
| Testes | 34 testes aprovados |
| Workspace | Preparado para evolução dos endpoints |

Validação real do endpoint `GET /api/v1/pontos-coleta`:

- Banco: `QualidadeAmbiental`.
- Fonte: `Tbl_PontosColeta`.
- Total retornado: 6 registros.
- Paginação validada com `page=1&page_size=2`.
- Filtros validados: `estado=MT`, `municipio=Cuiaba`, `tipo_ponto=Captacao superficial`.
- Limite de `page_size=101` retorna HTTP 422.
- `.env` local configurado sem versionar credenciais.

Validação real do endpoint `GET /api/v1/parametros`:

- Banco: `QualidadeAmbiental`.
- Fonte: `Tbl_Parametros`.
- Total retornado: 12 registros.
- Paginação validada com `page=1&page_size=2`.
- Filtros validados: `ativo=true`, `ativo=false`, `categoria=Fisico-quimico`.
- Filtro sem resultado retorna `data=[]` e `total=0`.
- Limite de `page_size=101` retorna HTTP 422.

Validação real do endpoint `GET /api/v1/amostras`:

- Banco: `QualidadeAmbiental`.
- Fonte principal: `Tbl_Amostras`.
- Joins validados com pontos de coleta, tipos de amostra, status e responsáveis.
- Total retornado: 6 registros.
- Paginação validada com `page=1&page_size=2`.
- Filtros validados: `municipio=Cuiaba`, `id_tipo_amostra=1`, `id_status=3`, `data_inicio` e `data_fim`.
- Filtro sem resultado retorna `data=[]` e `total=0`.
- Limite de `page_size=101` retorna HTTP 422.
- Intervalo inválido `data_inicio > data_fim` retorna HTTP 422.

Validação real do endpoint `GET /api/v1/resultados`:

- Fonte oficial: `VW_ConformidadeResultados`.
- Total retornado: 72 registros.
- Paginação validada com `page=1&page_size=2`.
- Filtros validados: `municipio`, `id_parametro`, `categoria`, `classificacao_resultado`, `indicador_nao_conforme`, `possui_limite_referencia`, `codigo_amostra`, `id_amostra`, `id_ponto_coleta`, `data_inicio` e `data_fim`.
- `indicador_nao_conforme` aceita retorno `null` para resultados sem limite.
- Conformidade consumida diretamente da view, sem recalculo em Python.

Validação real do endpoint `GET /api/v1/resultados/nao-conformidades`:

- Fonte do recorte: `VW_ResultadosForaDoPadrao`.
- Total retornado: 7 registros.
- Paginação validada com `page=1&page_size=2`.
- Filtros validados: `municipio`, `categoria`, `classificacao_resultado`, `id_parametro`, `id_ponto_coleta`, `data_inicio` e `data_fim`.
- Todos os registros retornados apresentaram `indicador_nao_conforme=true`.
- Conformidade consumida diretamente das views, sem recalculo em Python.

Validação real do endpoint `GET /api/v1/resultados/sem-limite-referencia`:

- Fonte do recorte: `VW_ResultadosSemLimiteReferencia`.
- Total retornado: 15 registros.
- Paginação validada com `page=1&page_size=2`.
- Filtros validados: `municipio`, `categoria`, `id_parametro`, `id_ponto_coleta`, `codigo_amostra`, `id_amostra`, `data_inicio` e `data_fim`.
- Todos os registros retornados apresentaram `possui_limite_referencia=false`, `indicador_nao_conforme=null` e `classificacao_resultado=Sem limite de referencia`.

Validação real do endpoint `GET /api/v1/resultados/resumo-mensal`:

- Fonte oficial: `VW_ConformidadeMensal`.
- Total retornado: 1 registro mensal.
- Período disponível: abril de 2026.
- Indicadores retornados pela view: 72 resultados, 57 com limite, 15 sem limite, 50 conformes com limite e 7 não conformes com limite.
- Percentual de conformidade com limite: 87.72.
- Filtros validados: `ano` e `mes`.
- `page_size=101` retorna HTTP 422.
- `mes=13` retorna HTTP 422.
- Indicadores consumidos diretamente da view, sem recalculo em Python.

Ainda não fazem parte do escopo atual:

- CRUD;
- autenticação/JWT;
- migrations;
- Docker;
- deploy;
- alterações no SQL Server.
