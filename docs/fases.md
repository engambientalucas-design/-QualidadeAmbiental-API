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

## Fase 2 - Endpoints de Consulta

Status: em andamento.

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
