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

Status: concluida em 2026-05-28.

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
- Validacao real contra SQL Server concluida na Fase 2.1.1.
- Nenhum CRUD, migration, autenticacao, Docker, deploy ou alteracao no SQL Server foi criado.

## Fase 2.1.1 - Validacao Real do Endpoint com SQL Server

Status: concluida em 2026-05-28.

Objetivos:

- Configurar `.env` local sem versionar credenciais.
- Confirmar drivers ODBC para SQL Server.
- Validar carregamento das variaveis `QA_API_`.
- Validar API local com Uvicorn.
- Validar `/health`, `/docs`, `/redoc` e `/openapi.json`.
- Validar `GET /api/v1/pontos-coleta` contra o banco real.
- Validar paginacao, filtros e limite de `page_size`.

Resultados:

- Drivers identificados: `ODBC Driver 17 for SQL Server` e `ODBC Driver 18 for SQL Server`.
- Driver usado: `ODBC Driver 18 for SQL Server`.
- Ajuste configuravel criado: `QA_API_DB_ENCRYPT`.
- Banco validado: `QualidadeAmbiental`.
- Tabela validada: `Tbl_PontosColeta`.
- Total real retornado: 6 registros.
- Paginacao validada com `page=1&page_size=2`, retornando 2 itens e `total=6`.
- Filtro `estado=MT` retornou 6 registros.
- Filtro `municipio=Cuiaba` retornou 4 registros.
- Filtro `tipo_ponto=Captacao superficial` retornou 1 registro.
- Filtro sem resultado retornou `data=[]` e `total=0`.
- `page_size=101` retornou HTTP 422.
- Suite automatizada aprovada com 5 testes.
- Nenhuma credencial foi exposta ou versionada.
- Nenhuma alteracao realizada no SQL Server.

## Fase 2.2 - Endpoint Read-only de Parametros

Status: concluida em 2026-05-28.

Objetivos:

- Implementar `GET /api/v1/parametros`.
- Reaplicar o fluxo `router -> service -> repository -> banco`.
- Criar schema Pydantic de resposta.
- Criar repository read-only.
- Criar service dedicado.
- Implementar filtros `categoria` e `ativo`.
- Implementar paginacao `page` e `page_size`.
- Criar testes automatizados.
- Validar OpenAPI e SQL Server real.

Resultados:

- `GET /api/v1/parametros` implementado.
- Router registrado em `/api/v1`.
- Service dedicado criado em `app/services/parametros_service.py`.
- Repository read-only criado com `SELECT`, `COUNT(1)`, filtros parametrizados e paginacao por `OFFSET/FETCH`.
- Schema Pydantic criado para resposta individual, lista e paginacao.
- Campo publico `ativo` tratado como booleano.
- Filtros iniciais implementados: `categoria`, `ativo`.
- Paginacao implementada com `page` padrao `1`, `page_size` padrao `20` e maximo `100`.
- OpenAPI validado com endpoint, parametros e respostas esperadas.
- Suite automatizada aprovada com 8 testes.
- Validacao real contra SQL Server concluida.
- Total real retornado em `Tbl_Parametros`: 12 registros.
- Filtro `categoria=Fisico-quimico` retornou 5 registros.
- Filtro `ativo=true` retornou 12 registros.
- Filtro `ativo=false` retornou 0 registros.
- `page_size=101` retornou HTTP 422.
- Documentacao tecnica criada em `docs/parametros_endpoint.md`.
- Nenhum CRUD, migration, autenticacao, Docker, deploy ou alteracao no SQL Server foi criado.

## Fase 2.3 - Endpoint Read-only de Amostras

Status: concluida em 2026-05-28.

Objetivos:

- Implementar `GET /api/v1/amostras`.
- Validar a primeira consulta relacional com joins controlados.
- Criar schema Pydantic com campos de data e hora.
- Criar repository read-only com joins.
- Criar service dedicado com validacao leve de intervalo de datas.
- Implementar filtros `data_inicio`, `data_fim`, `id_ponto_coleta`, `municipio`, `id_tipo_amostra` e `id_status`.
- Implementar paginacao `page` e `page_size`.
- Criar testes automatizados.
- Validar OpenAPI e SQL Server real.

Resultados:

- `GET /api/v1/amostras` implementado.
- Router registrado em `/api/v1`.
- Service dedicado criado em `app/services/amostras_service.py`.
- Repository read-only criado com `SELECT`, `COUNT(1)`, joins parametrizados e paginacao por `OFFSET/FETCH`.
- Joins implementados com `Tbl_PontosColeta`, `Tbl_TiposAmostra`, `Tbl_StatusAmostra` e `Tbl_Responsaveis`.
- Schema Pydantic criado para resposta individual, lista e paginacao.
- Campos `data_coleta` e `hora_coleta` tratados com tipos nativos `date` e `time`.
- Validacao `data_inicio <= data_fim` implementada.
- Ordenacao padrao definida por `DataColeta DESC, IdAmostra DESC`.
- OpenAPI validado com endpoint, parametros e respostas esperadas.
- Suite automatizada aprovada com 13 testes.
- Validacao real contra SQL Server concluida.
- Total real retornado em `Tbl_Amostras`: 6 registros.
- Filtro `municipio=Cuiaba` retornou 4 registros.
- Filtro `id_tipo_amostra=1` retornou 1 registro.
- Filtro `id_status=3` retornou 6 registros.
- Intervalo `2026-04-01` a `2026-04-30` retornou 6 registros.
- `page_size=101` retornou HTTP 422.
- Intervalo invalido `data_inicio > data_fim` retornou HTTP 422.
- Documentacao tecnica criada em `docs/amostras_endpoint.md`.
- Nenhum CRUD, migration, autenticacao, Docker, deploy ou alteracao no SQL Server foi criado.

## Fase 2.4 - Endpoint Read-only de Resultados Consolidados

Status: concluida em 2026-05-28.

Resultados da inspecao previa:

- View fonte confirmada: `VW_ConformidadeResultados`.
- Total real observado: 72 registros.
- Periodo observado: `2026-04-01` a `2026-04-03`.
- `PossuiLimiteReferencia` retorna `int` e deve ser exposto como booleano.
- `IndicadorNaoConforme` retorna `int` ou `NULL`; o contrato publico deve permitir `boolean | null`.
- `ValorResultado`, `ValorMinimo` e `ValorMaximo` devem ser expostos como numeros JSON.
- Distribuicoes e filtros reais documentados em `docs/inspecao_vw_conformidade_resultados.md`.
- Nenhuma alteracao realizada no SQL Server.

Objetivos de implementacao:

- Implementar `GET /api/v1/resultados`.
- Consumir `VW_ConformidadeResultados` como fonte oficial.
- Nao recalcular conformidade em Python.
- Criar schema Pydantic com campos consolidados.
- Criar repository read-only com filtros parametrizados.
- Criar service dedicado com validacao leve de intervalo de datas.
- Implementar filtros analiticos e paginacao.
- Validar OpenAPI, testes automatizados e SQL Server real.

Resultados:

- `GET /api/v1/resultados` implementado.
- Router registrado em `/api/v1`.
- Service dedicado criado em `app/services/resultados_service.py`.
- Repository read-only criado sobre `VW_ConformidadeResultados`.
- Conformidade consumida diretamente da view.
- `PossuiLimiteReferencia` convertido para booleano publico.
- `IndicadorNaoConforme` convertido para `boolean | null`.
- Decimais convertidos para numeros JSON.
- Ordenacao padrao definida por `DataColeta DESC, IdAmostra DESC, IdResultado DESC`.
- Suite automatizada aprovada com 19 testes.
- Validacao real contra SQL Server concluida.
- Total real retornado: 72 registros.
- Filtros reais validados conforme `docs/resultados_endpoint.md`.
- Documentacao tecnica criada em `docs/resultados_endpoint.md`.
- Nenhum CRUD, migration, autenticacao, Docker, deploy ou alteracao no SQL Server foi criado.

## Fase 2.5 - Endpoint Read-only de Nao Conformidades

Status: concluida em 2026-05-28.

Objetivos:

- Implementar `GET /api/v1/resultados/nao-conformidades`.
- Consumir `VW_ResultadosForaDoPadrao` como fonte oficial do recorte.
- Manter contrato compativel com `GET /api/v1/resultados`.
- Nao recalcular conformidade em Python.
- Reaproveitar schema, service, repository e router de resultados quando adequado.
- Validar OpenAPI, testes automatizados e SQL Server real.

Resultados:

- View `VW_ResultadosForaDoPadrao` inspecionada em modo read-only.
- Shape reduzido da view documentado em `docs/inspecao_vw_resultados_fora_do_padrao.md`.
- Endpoint implementado no router de resultados.
- Repository consulta `VW_ResultadosForaDoPadrao` como recorte e junta com `VW_ConformidadeResultados` por `IdResultado` para preservar contrato completo.
- Conformidade consumida diretamente das views, sem recalculo em Python.
- Suite automatizada aprovada com 24 testes.
- Validacao real contra SQL Server concluida.
- Total real retornado: 7 registros.
- Todos os registros retornados apresentaram `indicador_nao_conforme=true`.
- Documentacao tecnica criada em `docs/resultados_nao_conformidades_endpoint.md`.
- Nenhum CRUD, migration, autenticacao, Docker, deploy ou alteracao no SQL Server foi criado.

## Fase 2.6 - Endpoint Read-only de Resultados Sem Limite de Referencia

Status: concluida em 2026-05-28.

Objetivos:

- Implementar `GET /api/v1/resultados/sem-limite-referencia`.
- Consumir `VW_ResultadosSemLimiteReferencia` como fonte oficial do recorte.
- Manter contrato compativel com `GET /api/v1/resultados`.
- Nao recalcular conformidade em Python.
- Reaproveitar schema, service, repository e router de resultados quando adequado.
- Validar OpenAPI, testes automatizados e SQL Server real.

Resultados:

- View `VW_ResultadosSemLimiteReferencia` inspecionada em modo read-only.
- Shape reduzido da view documentado em `docs/inspecao_vw_resultados_sem_limite_referencia.md`.
- Endpoint implementado no router de resultados.
- Repository consulta `VW_ResultadosSemLimiteReferencia` como recorte e junta com `VW_ConformidadeResultados` por `IdResultado` para preservar contrato completo.
- Conformidade consumida diretamente das views, sem recalculo em Python.
- Suite automatizada aprovada com 29 testes.
- Validacao real contra SQL Server concluida.
- Total real retornado: 15 registros.
- Todos os registros retornados apresentaram `possui_limite_referencia=false`, `indicador_nao_conforme=null` e `classificacao_resultado=Sem limite de referencia`.
- Documentacao tecnica criada em `docs/resultados_sem_limite_referencia_endpoint.md`.
- Nenhum CRUD, migration, autenticacao, Docker, deploy ou alteracao no SQL Server foi criado.

## Fase 2.7 - Endpoint Analitico Read-only de Resumo Mensal

Status: concluida em 2026-05-28.

Objetivos:

- Implementar `GET /api/v1/resultados/resumo-mensal`.
- Consumir `VW_ConformidadeMensal` como fonte oficial dos indicadores mensais.
- Nao recalcular indicadores em Python.
- Reaproveitar schema, service, repository e router da familia de resultados quando adequado.
- Validar OpenAPI, testes automatizados e SQL Server real.

Resultados:

- View `VW_ConformidadeMensal` inspecionada em modo read-only.
- Granularidade real confirmada por `AnoColeta` e `MesColeta`.
- Endpoint implementado no router de resultados.
- Repository de resultados ampliado com consulta read-only da view mensal.
- Percentual `Decimal` convertido para numero JSON.
- Filtros implementados conforme granularidade real: `ano` e `mes`.
- Paginacao `page` e `page_size` implementada.
- Limite maximo de `page_size` definido em 100.
- Suite automatizada aprovada com 34 testes.
- Validacao real contra SQL Server concluida.
- Total real validado: 1 registro mensal.
- Periodo real validado: abril de 2026.
- Documentacao tecnica criada em `docs/resumo_mensal_endpoint.md`.
- Nenhum CRUD, migration, autenticacao, Docker, deploy ou alteracao no SQL Server foi criado.

## Fase 2.8 - Endpoint Analitico Read-only de Ranking de Parametros Criticos

Status: concluida em 2026-05-28.

Objetivos:

- Implementar `GET /api/v1/resultados/parametros-criticos`.
- Consumir `VW_RankingParametrosCriticos` como fonte oficial dos indicadores.
- Nao recalcular indicadores em Python.
- Reaproveitar schema, service, repository e router da familia de resultados quando adequado.
- Validar OpenAPI, testes automatizados e SQL Server real.

Resultados:

- View `VW_RankingParametrosCriticos` inspecionada em modo read-only.
- Endpoint implementado no router de resultados.
- Repository de resultados ampliado com consulta read-only da view.
- Ranking publico calculado em SQL por `ROW_NUMBER()` sobre os indicadores oficiais da view.
- Percentual `Decimal` convertido para numero JSON.
- Filtros implementados: `categoria` e `limit`.
- Paginacao `page` e `page_size` implementada.
- Limite maximo de `page_size` e `limit` definido em 100.
- Suite automatizada aprovada com 39 testes.
- Validacao real contra SQL Server concluida.
- Total real validado: 12 parametros.
- Ranking 1 validado: `Turbidez`.
- Documentacao tecnica criada em `docs/parametros_criticos_endpoint.md`.
- Nenhum CRUD, migration, autenticacao, Docker, deploy ou alteracao no SQL Server foi criado.

## Fase 2.9 - Consolidacao e Fechamento Tecnico da Camada Read-only e Analitica

Status: concluida em 2026-05-28.

Objetivos:

- Auditar contratos publicos da Fase 2.
- Revisar filtros, paginacao, status codes e OpenAPI.
- Revisar arquitetura sem executar refatoracao profunda.
- Consolidar documentacao principal.
- Registrar divida tecnica.
- Criar checklist de entrada da Fase 3.

Resultados:

- Contratos publicos auditados e registrados em `docs/fechamento_fase2.md`.
- Tabela consolidada de filtros criada.
- OpenAPI revisado por inspecao automatizada leve.
- Documento `docs/divida_tecnica.md` criado.
- Documento `docs/checklist_fase3.md` criado.
- `docs/contratos_api_fase2.md` ajustado com correcoes documentais seguras.
- Suite automatizada aprovada com 39 testes.
- Nenhum endpoint novo criado.
- Nenhum contrato publico alterado.
- Nenhuma alteracao realizada no SQL Server.
- Fase 2 oficialmente encerrada.

## Fase 2 - Endpoints de Consulta

Status: concluida em 2026-05-28.

Escopo previsto:

- `GET /api/v1/pontos-coleta` (implementado na Fase 2.1)
- `GET /api/v1/pontos-coleta/{id}`
- `GET /api/v1/parametros` (implementado na Fase 2.2)
- `GET /api/v1/parametros/{id}`
- `GET /api/v1/amostras` (implementado na Fase 2.3)
- `GET /api/v1/amostras/{id}`
- `GET /api/v1/resultados` (implementado na Fase 2.4)
- `GET /api/v1/resultados/{id}`
- `GET /api/v1/resultados/resumo`
- `GET /api/v1/resultados/nao-conformidades` (implementado na Fase 2.5)
- `GET /api/v1/resultados/sem-limite-referencia` (implementado na Fase 2.6)
- `GET /api/v1/resultados/resumo-mensal` (implementado na Fase 2.7)
- `GET /api/v1/resultados/parametros-criticos` (implementado na Fase 2.8)

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

Status: em andamento.

Objetivos:

- Consolidar routers, schemas, models, repositories e services.
- Adicionar tratamento padronizado de erros.
- Adicionar paginacao e filtros.
- Revisar acoplamento e nomes de dominio.

## Fase 3.0 - Padronizacao de Erros, Paginacao e Validacoes

Status: concluida em 2026-05-28.

Objetivos:

- Padronizar respostas de erro.
- Centralizar constantes e metadados de paginacao.
- Criar validacao reutilizavel de intervalo de datas.
- Registrar handlers globais de erro.
- Configurar logging basico.
- Ampliar testes de erro.
- Documentar padroes internos da API.

Resultados:

- Schema de erro criado em `app/schemas/error.py`.
- Handlers globais criados em `app/core/exception_handlers.py`.
- Logging basico criado em `app/core/logging.py`.
- Utilitario de validacao criado em `app/utils/validators.py`.
- Utilitario de paginacao consolidado com `DEFAULT_PAGE`, `DEFAULT_PAGE_SIZE` e `MAX_PAGE_SIZE`.
- Contrato de sucesso preservado.
- Contrato de erro padronizado como novo contrato oficial da Fase 3.
- Validacao de data reutilizada em amostras e resultados.
- Testes de erro adicionados em `tests/test_error_handlers.py`.
- Suite automatizada aprovada com 41 testes.
- Documento `docs/padroes_api.md` criado.
- Nenhum endpoint de dominio criado.
- Nenhuma alteracao realizada no SQL Server.

## Fase 3.0.1 - Preparacao para Publicacao no GitHub

Status: concluida em 2026-05-28.

Objetivos:

- Auditar `.gitignore`.
- Auditar arquivos rastreados pelo Git.
- Verificar possiveis credenciais ou segredos.
- Revisar `.env.example`.
- Criar documentacao de publicacao.
- Validar testes antes do push.
- Preparar snapshot da etapa.

Resultados:

- `.gitignore` confirmado com exclusoes para `.env`, `.venv`, caches, logs e snapshots `.zip`.
- Arquivos rastreados auditados com `git ls-files`.
- Busca por possiveis segredos executada com `rg`.
- `.env.example` sanitizado com usuario e senha vazios.
- Documento `docs/publicacao_github.md` criado.
- Suite automatizada aprovada com 41 testes.
- Nenhum endpoint criado.
- Nenhum contrato publico alterado.
- Nenhuma alteracao realizada no SQL Server.
- Projeto pronto para configuracao de remote e push inicial.

## Fase 3.0.2 - Versionamento Inicial e CI com GitHub Actions

Status: concluida em 2026-05-29.

Objetivos:

- Configurar workflow de testes no GitHub Actions.
- Executar `pytest` automaticamente em `push` e `pull_request`.
- Usar Python 3.12 no CI.
- Garantir que o CI nao dependa do SQL Server real.
- Criar tag inicial do projeto.

Resultados:

- Workflow criado em `.github/workflows/tests.yml`.
- Dependencia de sistema `unixodbc-dev` instalada no CI para suporte ao `pyodbc`.
- Dependencias Python instaladas via `requirements.txt`.
- Suite automatizada executada com `pytest`.
- Badge de testes adicionado ao README.
- Tag inicial definida: `v0.3.0-readonly-analytics`.
- CI remoto validado com status `success`.
- Release inicial criada no GitHub: `v0.3.0 - Read-only Analytics API`.
- Nenhum endpoint criado.
- Nenhum contrato publico alterado.
- Nenhuma alteracao realizada no SQL Server.

## Fase 3.0.3 - Validacao do CI e Release Inicial

Status: concluida em 2026-05-29.

Objetivos:

- Validar autenticacao do GitHub CLI.
- Conferir workflows disponiveis.
- Validar execucoes recentes do GitHub Actions.
- Criar release inicial a partir da tag `v0.3.0-readonly-analytics`.
- Registrar status de CI e release na documentacao.

Resultados:

- GitHub CLI autenticado para a conta `engambientalucas-design`.
- Workflow `Tests` identificado e ativo.
- Run remoto do workflow `Tests` validado com status `success`.
- Job `pytest` validado no GitHub Actions.
- Release `v0.3.0 - Read-only Analytics API` criada.
- URL da release registrada em `docs/publicacao_github.md`.
- Nenhum endpoint criado.
- Nenhum contrato publico alterado.
- Nenhuma alteracao realizada no SQL Server.

## Fase 3.1 - Testes Avancados, OpenAPI e Observabilidade Leve

Status: concluida em 2026-05-29.

Objetivos:

- Ampliar testes parametrizados de validacao e contrato.
- Validar contratos de erro 422 de forma transversal.
- Documentar respostas de erro no OpenAPI.
- Adicionar middleware de logging de requisicao.
- Implementar suporte ao header `X-Request-ID`.
- Manter CI independente do SQL Server real.

Resultados:

- Middleware `RequestLoggingMiddleware` criado em `app/core/middleware.py`.
- Header `X-Request-ID` gerado ou preservado em respostas HTTP.
- Logs de requisicao registram metodo, path, status code, duracao e `request_id`.
- Routers documentam respostas padronizadas de erro 422 e 500 no OpenAPI.
- Testes parametrizados adicionados em `tests/test_api_contracts_phase3.py`.
- Testes de observabilidade adicionados em `tests/test_observability.py`.
- Suite automatizada aprovada com 73 testes.
- Documento `docs/observabilidade.md` criado.
- Nenhum endpoint de dominio criado.
- Nenhum contrato publico de sucesso alterado.
- Nenhuma alteracao realizada no SQL Server.

## Fase 3.2 - Cobertura de Testes com pytest-cov

Status: concluida em 2026-05-29.

Objetivos:

- Adicionar medicao objetiva de cobertura com `pytest-cov`.
- Padronizar execucao de testes via `pytest.ini`.
- Integrar cobertura ao GitHub Actions.
- Gerar relatorio HTML local ignorado pelo Git.
- Documentar riscos e metas futuras de qualidade.

Resultados:

- Dependencia `pytest-cov==6.0.0` adicionada ao `requirements.txt`.
- Arquivo `pytest.ini` criado com `testpaths`, `pythonpath` e `addopts`.
- Workflow `Tests` atualizado para executar `python -m pytest --cov=app --cov-report=term-missing`.
- Suite padrao aprovada com 73 testes.
- Cobertura local medida com 65% geral.
- Relatorio HTML gerado em `htmlcov/`.
- `htmlcov/`, `.coverage` e `coverage.xml` confirmados no `.gitignore`.
- Documento `docs/qualidade_testes.md` criado.
- Nenhum endpoint de dominio criado.
- Nenhum contrato publico de sucesso alterado.
- Nenhuma alteracao realizada no SQL Server.

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
