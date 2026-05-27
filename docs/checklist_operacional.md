# Checklist Operacional

Use este checklist antes de evoluir o projeto ou executar mudancas criticas.

## Ambiente local

- [ ] Ambiente virtual `.venv` criado.
- [ ] Ambiente virtual ativo.
- [ ] Dependencias instaladas com `pip install -r requirements.txt`.
- [ ] Arquivo `.env` criado a partir de `.env.example`.
- [ ] Variaveis `QA_API_` conferidas.

## Banco de dados

- [ ] SQL Server acessivel.
- [ ] Banco `QualidadeAmbiental` disponivel.
- [ ] Usuario de banco com permissao adequada.
- [ ] Credenciais reais mantidas fora do Git.

## API

- [ ] Aplicacao inicia com `uvicorn app.main:app --reload`.
- [ ] Endpoint `/health` validado.
- [ ] Swagger `/docs` acessivel.
- [ ] ReDoc `/redoc` acessivel.

## Governanca

- [ ] `.gitignore` revisado.
- [ ] `.env` ignorado pelo Git.
- [ ] `.venv/` ignorado pelo Git.
- [ ] Logs ignorados pelo Git.
- [ ] `git status` revisado antes de commit.
- [ ] Commit realizado antes de mudancas criticas.
- [ ] Snapshot gerado antes de refatoracoes ou alteracoes estruturais.

## Antes da Fase 2

- [ ] Base atual commitada.
- [ ] Documentacao de versionamento revisada.
- [ ] Decisoes tecnicas registradas.
- [ ] Checklist operacional revisado.
- [ ] Nenhum endpoint de dominio criado fora do planejamento.
- [ ] Nenhuma tabela SQL Server alterada.
