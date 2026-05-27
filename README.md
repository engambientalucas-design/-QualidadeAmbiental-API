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

Fase atual: Fase 1.3 - Validação Local Completa concluída.

Validações realizadas em 2026-05-27:

- Python 3.12.10 validado na `.venv`.
- `pip` validado.
- Imports principais validados: FastAPI, SQLAlchemy, pyodbc, Pydantic, Uvicorn, httpx e pytest.
- API iniciada com o comando oficial:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

- `GET /health` validado com HTTP 200.
- Swagger `/docs` validado com HTTP 200.
- ReDoc `/redoc` validado com HTTP 200.
- OpenAPI `/openapi.json` validado com HTTP 200.
- Teste automatizado mínimo criado para `/health`.
- `pytest` executado com sucesso: 2 testes aprovados.

Próxima etapa: Fase 2.0 - inspeção real do banco SQL Server antes de criar endpoints de domínio.

Ainda não devem ser criados CRUD, autenticação, migrations, Docker, deploy ou endpoints reais sem a inspeção e documentação do schema do banco.
