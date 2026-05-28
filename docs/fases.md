# Fases do Projeto

## Fase 0 - Planejamento e Estruturacao

Status: concluida para a base inicial.

Objetivos:

- Definir a API como servico REST read-only inicialmente.
- Validar o escopo inicial com as entidades pontos de coleta, parametros, amostras e resultados.
- Preparar a organizacao profissional em camadas.
- Definir padrao de resposta, filtros e versionamento em `/api/v1`.
- Documentar premissas sobre o banco `QualidadeAmbiental`.

Entregas desta fase:

- Estrutura de diretorios.
- Documentacao inicial.
- Definicao de dependencias.
- Configuracao inicial via variaveis de ambiente.

## Fase 1 - Criacao da Base do Projeto

Status: concluida para a base inicial.

Objetivos:

- Criar aplicacao FastAPI.
- Configurar carregamento de `.env`.
- Preparar conexao SQL Server com SQLAlchemy e pyodbc.
- Disponibilizar endpoint `GET /health`.
- Validar Swagger em `/docs` e ReDoc em `/redoc`.

## Fase 1.2 - Governanca Tecnica, Versionamento e Backup

Status: concluida.

Objetivos:

- Inicializar Git no projeto.
- Garantir `.gitignore` profissional.
- Proteger credenciais e arquivos locais.
- Documentar estrategia de versionamento, backup e rollback.
- Criar politica de snapshots.
- Registrar decisoes tecnicas.
- Criar checklist operacional.
- Gerar commit tecnico da base validada.
- Preparar o projeto para evolucao segura.

Regras desta fase:

- Nao criar endpoints de dominio.
- Nao implementar CRUD.
- Nao alterar tabelas do SQL Server.
- Nao criar migrations.
- Nao modificar logica da API.

## Fase 1.3 - Validacao Local Completa

Status: concluida em 2026-05-27.

Objetivos:

- Validar ambiente virtual.
- Validar execucao com `uvicorn app.main:app --reload`.
- Validar endpoint `/health`.
- Validar Swagger `/docs`.
- Validar ReDoc `/redoc`.
- Criar teste automatizado minimo.
- Rodar `pytest`.
- Revisar encoding dos arquivos.
- Atualizar documentacao da etapa.

Resultados:

- Python 3.12.10 validado.
- `pip` validado.
- Imports principais validados.
- API iniciou com o comando oficial.
- `/health`, `/docs`, `/redoc` e `/openapi.json` responderam HTTP 200.
- `tests/test_health.py` criado.
- `pytest` aprovado com 2 testes.

## Fase 2.0 - Inspecao Real do Banco SQL Server

Status: concluida em 2026-05-27.

Objetivos:

- Inspecionar schemas, tabelas, colunas, chaves primarias e chaves estrangeiras.
- Confirmar tipos de dados e relacionamentos reais.
- Verificar views existentes.
- Avaliar indices relevantes para filtros.
- Confirmar usuario e politica read-only.
- Atualizar `docs/modelo_banco.md` com o mapeamento real.
- Definir contratos dos primeiros endpoints antes de implementa-los.

Resultados:

- 9 tabelas base identificadas.
- 6 views consolidadas identificadas.
- Relacionamentos principais confirmados.
- Indices, constraints, triggers e volumes iniciais documentados.
- Contratos planejados da Fase 2 criados.
- Nenhuma alteracao realizada no SQL Server.

## Fase 2.1 - Primeiro Endpoint Read-only

Status: implementada em 2026-05-28; validacao real com SQL Server pendente no workspace atual por ausencia de `.env`.

Objetivos:

- Implementar `GET /api/v1/pontos-coleta`.
- Validar o fluxo `router -> service -> repository -> banco`.
- Criar schema Pydantic de resposta.
- Criar repository read-only.
- Criar service simples.
- Criar teste automatizado.
- Validar Swagger.

Resultados:

- `GET /api/v1/pontos-coleta` implementado.
- Router registrado em `/api/v1`.
- Service dedicado criado em `app/services/pontos_coleta_service.py`.
- Repository read-only criado com `SELECT`, `COUNT(1)`, filtros parametrizados e paginacao por `OFFSET/FETCH`.
- Schema Pydantic criado para resposta individual, lista e paginacao.
- Filtros iniciais implementados: `municipio`, `estado`, `tipo_ponto`.
- Paginacao implementada com `page` padrao `1`, `page_size` padrao `20` e maximo `100`.
- Testes automatizados criados em `tests/test_pontos_coleta.py`.
- Suite automatizada aprovada com 5 testes.
- Documentacao tecnica criada em `docs/pontos_coleta_endpoint.md`.
- OpenAPI validado com o endpoint, parametros e respostas esperadas.
- Validacao real contra SQL Server nao concluida neste workspace porque nao ha arquivo `.env` configurado e a aplicacao usou o fallback `localhost:1433`.
- Nenhum CRUD, migration, autenticacao, Docker, deploy ou alteracao no SQL Server foi criado.

## Fase 2 - Endpoints de Consulta

Status: em andamento.

Escopo previsto:

- `GET /api/v1/pontos-coleta` (implementado na Fase 2.1)
- `GET /api/v1/pontos-coleta/{id}`
- `GET /api/v1/parametros`
- `GET /api/v1/parametros/{id}`
- `GET /api/v1/amostras`
- `GET /api/v1/amostras/{id}`
- `GET /api/v1/resultados`
- `GET /api/v1/resultados/{id}`
- `GET /api/v1/resultados/resumo`
- `GET /api/v1/resultados/nao-conformidades`

Filtros previstos:

- `data_inicio`
- `data_fim`
- `ponto_coleta_id`
- `parametro_id`
- `municipio`
- `situacao`
- `limite`
- `pagina`
- `tamanho_pagina`

## Fase 3 - Organizacao Profissional

Status: pendente.

Objetivos:

- Consolidar routers, schemas, models, repositories e services.
- Adicionar tratamento padronizado de erros.
- Adicionar paginacao e filtros.
- Revisar acoplamento e nomes de dominio.

## Fase 4 - Evolucao Funcional

Status: pendente.

Objetivos:

- Avaliar endpoints de escrita.
- Definir autenticacao, autorizacao e logs.
- Ampliar testes automatizados.
- Melhorar documentacao tecnica.

## Fase 5 - Validacao Final e Entrega

Status: pendente.

Objetivos:

- Validar testes com pytest.
- Revisar README.
- Documentar exemplos de requisicoes.
- Validar `/docs` e `/redoc`.
- Criar checklist final de execucao local.
