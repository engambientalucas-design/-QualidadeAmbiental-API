# Checklist Operacional

Use este checklist antes de evoluir o projeto ou executar mudancas criticas.

## Ambiente local

- [x] Ambiente virtual `.venv` criado.
- [x] Python 3.12.10 validado.
- [x] `pip` validado.
- [x] Dependencias instaladas com `pip install -r requirements.txt`.
- [x] Imports principais validados.
- [ ] Arquivo `.env` criado a partir de `.env.example` quando a validacao de banco for necessaria.
- [ ] Variaveis `QA_API_` conferidas quando a validacao de banco for necessaria.

## Banco de dados

- [ ] SQL Server acessivel.
- [ ] Banco `QualidadeAmbiental` disponivel.
- [ ] Usuario de banco com permissao adequada.
- [ ] Credenciais reais mantidas fora do Git.

## API

- [x] Aplicacao inicia com `uvicorn app.main:app --reload`.
- [x] Comando oficial validado: `.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload`.
- [x] Endpoint `/health` validado manualmente.
- [x] Endpoint `/health` validado por teste automatizado.
- [x] Swagger `/docs` acessivel.
- [x] ReDoc `/redoc` acessivel.
- [x] OpenAPI `/openapi.json` acessivel.
- [x] Encoding UTF-8 revisado nos arquivos do projeto.

## Testes

- [x] `tests/test_health.py` criado.
- [x] `pytest` executado.
- [x] Suite atual aprovada: 2 testes.

## Governanca

- [x] `.gitignore` revisado.
- [x] `.env` ignorado pelo Git.
- [x] `.venv/` ignorado pelo Git.
- [x] Logs ignorados pelo Git.
- [x] Snapshot da Fase 1 gerado.
- [x] Snapshot da Fase 1.3 gerado em 2026-05-27.
- [x] `git status` revisado antes de commit.
- [x] Commit realizado antes de mudancas criticas.

## Antes da Fase 2.0

- [x] Base inicial commitada.
- [x] Documentacao de versionamento revisada.
- [x] Decisoes tecnicas registradas.
- [x] Checklist operacional revisado.
- [x] Nenhum endpoint de dominio criado fora do planejamento.
- [x] Nenhuma tabela SQL Server alterada.
- [x] API local validada.
- [x] Swagger e ReDoc validados.
- [x] Teste automatizado minimo criado.

## Fase 2.0 - Inspecao do banco

- [x] Tabelas base identificadas.
- [x] Views identificadas.
- [x] Chaves primarias documentadas.
- [x] Chaves estrangeiras documentadas.
- [x] Indices principais documentados.
- [x] Constraints relevantes documentadas.
- [x] Triggers de auditoria documentadas.
- [x] Volumes iniciais documentados.
- [x] Contratos planejados da Fase 2 criados.
- [x] Nenhuma alteracao realizada no SQL Server.
