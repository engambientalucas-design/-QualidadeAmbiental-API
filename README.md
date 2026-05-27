# QualidadeAmbiental API FastAPI

API REST em Python com FastAPI para consultar, organizar e futuramente manipular dados de qualidade ambiental a partir do banco SQL Server `QualidadeAmbiental`.

## Objetivo

Nesta primeira etapa, a API sera read-only e servira como ponte entre o banco `QualidadeAmbiental` e consumidores externos como dashboards, frontends, Power BI e outros sistemas.

## Tecnologias

- Python 3.12
- FastAPI
- SQLAlchemy
- pyodbc
- Pydantic
- SQL Server
- pytest

## Estrutura

```text
app/
  core/           Configuracoes, variaveis de ambiente e conexao
  models/         Modelos SQLAlchemy do banco
  repositories/   Consultas SQL/ORM
  routers/        Rotas HTTP
  schemas/        Schemas Pydantic
  services/       Regras de negocio e orquestracao
  utils/          Respostas, paginacao e utilitarios
backup/           Snapshots locais ignorados pelo Git
docs/             Documentacao tecnica do projeto
tests/            Testes automatizados
```

## Rotas iniciais

- `GET /health`
- Swagger: `/docs`
- ReDoc: `/redoc`

Rotas de dominio previstas para a Fase 2:

- `GET /api/v1/pontos-coleta`
- `GET /api/v1/parametros`
- `GET /api/v1/amostras`
- `GET /api/v1/resultados`

## Configuracao local

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual no Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependencias:

```bash
pip install -r requirements.txt
```

Copie o arquivo de exemplo de ambiente:

```bash
copy .env.example .env
```

Edite o `.env` com os dados reais do SQL Server.

As variaveis da aplicacao usam o prefixo `QA_API_` para evitar conflito com variaveis globais do sistema, por exemplo `QA_API_DEBUG` e `QA_API_DB_SERVER`.

Execute a API:

```bash
uvicorn app.main:app --reload
```

Acesse:

- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## Versionamento

O projeto usa Git para rastrear codigo, documentacao e configuracoes de exemplo.

Fluxo recomendado:

```bash
git status
git add .
git commit -m "chore: descreve a mudanca"
```

Convencao de commits:

- `feat:` nova funcionalidade;
- `fix:` correcao;
- `refactor:` melhoria interna;
- `docs:` documentacao;
- `test:` testes;
- `chore:` manutencao, configuracao ou governanca.

## Seguranca de credenciais

O arquivo `.env` nunca deve ser versionado. O repositorio deve conter somente `.env.example` com valores de exemplo.

Antes de qualquer commit, confirme:

```bash
git status --short
```

Arquivos como `.env`, `.venv/`, logs e caches nao devem aparecer para commit.

## Snapshots

Snapshots compactados devem ser gerados antes de mudancas criticas, como refatoracoes, alteracoes na conexao SQL Server, criacao de endpoints reais ou mudancas estruturais.

Padrao de nome:

```text
backup/QualidadeAmbiental_API_FastAPI_Fase1_2026-05-27.zip
```

Os arquivos `.zip` em `backup/` sao locais e ignorados pelo Git.

## Documentacao tecnica

- `docs/fases.md`: fases de evolucao do projeto.
- `docs/modelo_banco.md`: visao inicial do dominio e premissas sobre o banco.
- `docs/versionamento_backup.md`: politica de Git, backup e rollback.
- `docs/decisoes_tecnicas.md`: decisoes de arquitetura e tecnologia.
- `docs/checklist_operacional.md`: checklist antes de mudancas criticas.

## Padrao de resposta

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

## Status

Fase atual: Fase 2.0 - Inspecao Real do Banco SQL Server documentada.

Validações e inspecoes realizadas:

- Fase 1.3 concluida com API local validada.
- `/health`, `/docs`, `/redoc` e `/openapi.json` validados.
- `pytest` aprovado com 2 testes.
- Banco `QualidadeAmbiental` inspecionado em modo read-only.
- 9 tabelas base identificadas.
- 6 views consolidadas identificadas.
- Relacionamentos principais confirmados.
- Indices, constraints, triggers e volumes iniciais documentados.
- Contratos planejados da Fase 2 registrados antes de implementacao.

Documentos principais:

- `docs/modelo_banco.md`
- `docs/contratos_api_fase2.md`
- `docs/fases.md`
- `docs/checklist_operacional.md`

Proxima etapa recomendada: Fase 2.1 - implementar o primeiro endpoint read-only `GET /api/v1/pontos-coleta`, usando o fluxo completo `router -> service -> repository -> banco`.

Ainda nao devem ser criados CRUD, autenticacao, migrations, Docker, deploy ou alteracoes no SQL Server.
