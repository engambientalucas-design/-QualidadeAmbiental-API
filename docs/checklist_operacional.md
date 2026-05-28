# Checklist Operacional

Use este checklist antes de evoluir o projeto ou executar mudancas criticas.

## Ambiente local

- [x] Ambiente virtual `.venv` criado.
- [x] Python 3.12.10 validado.
- [x] `pip` validado.
- [x] Dependencias instaladas com `pip install -r requirements.txt`.
- [x] Imports principais validados.
- [x] Arquivo `.env` criado a partir de `.env.example` quando a validacao de banco for necessaria.
- [x] Variaveis `QA_API_` conferidas quando a validacao de banco for necessaria.
- [x] VS Code configurado para usar `.venv`.
- [x] VS Code configurado para localizar `${workspaceFolder}/.env`.
- [x] VS Code configurado com `python.terminal.useEnvFile=true`.

## Banco de dados

- [x] SQL Server acessivel.
- [x] Banco `QualidadeAmbiental` disponivel.
- [x] Usuario de banco com permissao adequada.
- [x] Credenciais reais mantidas fora do Git.

## API

- [x] Aplicacao inicia com `uvicorn app.main:app --reload`.
- [x] Comando oficial validado: `.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload`.
- [x] Endpoint `/health` validado manualmente.
- [x] Endpoint `/health` validado por teste automatizado.
- [x] Endpoint `/api/v1/pontos-coleta` implementado.
- [x] Endpoint `/api/v1/pontos-coleta` validado por teste automatizado de contrato.
- [x] Endpoint `/api/v1/parametros` implementado.
- [x] Endpoint `/api/v1/parametros` validado por teste automatizado de contrato.
- [x] Endpoint `/api/v1/amostras` implementado.
- [x] Endpoint `/api/v1/amostras` validado por teste automatizado de contrato.
- [x] Endpoint `/api/v1/resultados` implementado.
- [x] Endpoint `/api/v1/resultados` validado por teste automatizado de contrato.
- [x] Endpoint `/api/v1/resultados/nao-conformidades` implementado.
- [x] Endpoint `/api/v1/resultados/nao-conformidades` validado por teste automatizado de contrato.
- [x] Endpoint `/api/v1/resultados/sem-limite-referencia` implementado.
- [x] Endpoint `/api/v1/resultados/sem-limite-referencia` validado por teste automatizado de contrato.
- [x] Endpoint `/api/v1/resultados/resumo-mensal` implementado.
- [x] Endpoint `/api/v1/resultados/resumo-mensal` validado por teste automatizado de contrato.
- [x] Endpoint `/api/v1/resultados/parametros-criticos` implementado.
- [x] Endpoint `/api/v1/resultados/parametros-criticos` validado por teste automatizado de contrato.
- [x] Swagger `/docs` acessivel.
- [x] ReDoc `/redoc` acessivel.
- [x] OpenAPI `/openapi.json` acessivel.
- [x] Encoding UTF-8 revisado nos arquivos do projeto.

## Testes

- [x] `tests/test_health.py` criado.
- [x] `tests/test_pontos_coleta.py` criado.
- [x] `tests/test_parametros.py` criado.
- [x] `tests/test_amostras.py` criado.
- [x] `tests/test_resultados.py` criado.
- [x] `tests/test_error_handlers.py` criado.
- [x] `pytest` executado.
- [x] Suite atual aprovada: 41 testes.

## Governanca

- [x] `.gitignore` revisado.
- [x] `.env` ignorado pelo Git.
- [x] `.venv/` ignorado pelo Git.
- [x] `.vscode/settings.json` liberado para versionamento seguro.
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

## Fase 2.1 - Primeiro endpoint read-only

- [x] Schema Pydantic de pontos de coleta criado.
- [x] Repository read-only de pontos de coleta criado.
- [x] Service de pontos de coleta criado.
- [x] Router `GET /api/v1/pontos-coleta` criado.
- [x] Router registrado na aplicacao.
- [x] Resposta padronizada implementada.
- [x] Paginacao `page` e `page_size` implementada.
- [x] Limite maximo de `page_size` definido em 100.
- [x] Filtros `municipio`, `estado` e `tipo_ponto` implementados.
- [x] Testes automatizados de contrato criados.
- [x] OpenAPI/Swagger validado por teste automatizado de importacao da aplicacao.
- [ ] Validacao real com SQL Server configurado via `.env`.
- [x] Documentacao tecnica do endpoint criada.
- [x] Nenhuma alteracao realizada no SQL Server.

## Fase 2.1.1 - Validacao real do endpoint com SQL Server

- [x] `.env` local criado/revisado a partir do `.env.example`.
- [x] `.env` confirmado fora do Git.
- [x] Variavel padronizada conferida: `QA_API_DB_TRUST_SERVER_CERTIFICATE`.
- [x] Drivers ODBC 17 e 18 identificados.
- [x] Imports principais validados.
- [x] Carregamento de configuracao validado sem imprimir senha.
- [x] Ajuste configuravel `QA_API_DB_ENCRYPT` criado.
- [x] Conexao real com `QualidadeAmbiental` validada.
- [x] Uvicorn iniciado localmente.
- [x] `/health` validado via HTTP.
- [x] `/docs` validado via HTTP 200.
- [x] `/redoc` validado via HTTP 200.
- [x] `/openapi.json` validado com `/api/v1/pontos-coleta`.
- [x] `GET /api/v1/pontos-coleta` validado contra SQL Server real.
- [x] Total real de `Tbl_PontosColeta` validado: 6 registros.
- [x] Paginacao validada com `page=1&page_size=2`.
- [x] Filtro `estado=MT` validado.
- [x] Filtro `municipio=Cuiaba` validado.
- [x] Filtro `tipo_ponto=Captacao superficial` validado.
- [x] Filtro sem resultado validado com `data=[]`.
- [x] `page_size=101` validado com HTTP 422.
- [x] `pytest` executado com 5 testes aprovados.
- [x] Nenhuma credencial exposta em documentacao ou Git.

## Ambiente VS Code

- [x] `.vscode/settings.json` criado.
- [x] `python.defaultInterpreterPath` aponta para `.venv\Scripts\python.exe`.
- [x] `python.envFile` aponta para `${workspaceFolder}/.env`.
- [x] `python.terminal.useEnvFile` habilitado.
- [x] `.env` permanece ignorado pelo Git.
- [x] Configuracao versionada nao contem credenciais.
- [ ] Validar `echo $env:QA_API_DB_NAME` em novo terminal integrado do VS Code.
- [ ] Validar `echo $env:QA_API_DB_DRIVER` em novo terminal integrado do VS Code.

Observacao: a aplicacao carrega `.env` diretamente via `pydantic-settings`; a configuracao do VS Code garante que o terminal integrado tambem receba as variaveis `QA_API_` ao abrir um novo terminal.

## Fase 2.2 - Endpoint read-only de parametros

- [x] Schema Pydantic de parametros criado.
- [x] Repository read-only de parametros criado.
- [x] Service de parametros criado.
- [x] Router `GET /api/v1/parametros` criado.
- [x] Router registrado na aplicacao.
- [x] Resposta padronizada implementada.
- [x] Paginacao `page` e `page_size` implementada.
- [x] Limite maximo de `page_size` definido em 100.
- [x] Filtros `categoria` e `ativo` implementados.
- [x] Campo `ativo` tratado como booleano na API publica.
- [x] Testes automatizados de contrato criados.
- [x] OpenAPI/Swagger validado com parametros do endpoint.
- [x] Validacao real com SQL Server concluida.
- [x] Total real de `Tbl_Parametros` validado: 12 registros.
- [x] Filtro `categoria=Fisico-quimico` validado.
- [x] Filtro `ativo=true` validado.
- [x] Filtro `ativo=false` validado.
- [x] Filtro sem resultado validado com `data=[]`.
- [x] `page_size=101` validado com HTTP 422.
- [x] `pytest` executado com 8 testes aprovados.
- [x] Documentacao tecnica do endpoint criada.
- [x] Nenhuma alteracao realizada no SQL Server.

## Fase 2.3 - Endpoint read-only de amostras

- [x] Schema Pydantic de amostras criado.
- [x] Repository read-only de amostras criado.
- [x] Service de amostras criado.
- [x] Router `GET /api/v1/amostras` criado.
- [x] Router registrado na aplicacao.
- [x] Resposta padronizada implementada.
- [x] Joins com pontos de coleta, tipos, status e responsaveis implementados.
- [x] Campos `data_coleta` e `hora_coleta` tipados como `date` e `time`.
- [x] Validacao `data_inicio <= data_fim` implementada.
- [x] Paginacao `page` e `page_size` implementada.
- [x] Limite maximo de `page_size` definido em 100.
- [x] Filtros `data_inicio`, `data_fim`, `id_ponto_coleta`, `municipio`, `id_tipo_amostra` e `id_status` implementados.
- [x] Testes automatizados de contrato criados.
- [x] OpenAPI/Swagger validado com parametros do endpoint.
- [x] Validacao real com SQL Server concluida.
- [x] Total real de `Tbl_Amostras` validado: 6 registros.
- [x] Filtro `municipio=Cuiaba` validado.
- [x] Filtro `id_tipo_amostra=1` validado.
- [x] Filtro `id_status=3` validado.
- [x] Intervalo `data_inicio=2026-04-01&data_fim=2026-04-30` validado.
- [x] Filtro sem resultado validado com `data=[]`.
- [x] `page_size=101` validado com HTTP 422.
- [x] Intervalo invalido `data_inicio > data_fim` validado com HTTP 422.
- [x] `pytest` executado com 13 testes aprovados.
- [x] Documentacao tecnica do endpoint criada.
- [x] Nenhuma alteracao realizada no SQL Server.

## Antes da Fase 2.4 - Inspecao da view de resultados

- [x] View `VW_ConformidadeResultados` inspecionada em modo read-only.
- [x] Colunas e tipos reais confirmados.
- [x] Total real de registros confirmado: 72.
- [x] Periodo real confirmado: `2026-04-01` a `2026-04-03`.
- [x] Distribuicoes por municipio, categoria e classificacao confirmadas.
- [x] Filtros booleanos reais confirmados.
- [x] `IndicadorNaoConforme` confirmado como campo que pode retornar `NULL`.
- [x] Documento `docs/inspecao_vw_conformidade_resultados.md` criado.
- [x] Nenhuma alteracao realizada no SQL Server.

## Fase 2.4 - Endpoint read-only de resultados consolidados

- [x] Schema Pydantic de resultados criado.
- [x] Repository read-only de resultados criado sobre `VW_ConformidadeResultados`.
- [x] Service de resultados criado.
- [x] Router `GET /api/v1/resultados` criado.
- [x] Router registrado na aplicacao.
- [x] Resposta padronizada implementada.
- [x] Conformidade consumida da view, sem recalculo em Python.
- [x] Decimais convertidos para numeros JSON.
- [x] `PossuiLimiteReferencia` convertido para booleano.
- [x] `IndicadorNaoConforme` tratado como `boolean | null`.
- [x] Validacao `data_inicio <= data_fim` implementada.
- [x] Paginacao `page` e `page_size` implementada.
- [x] Limite maximo de `page_size` definido em 100.
- [x] Testes automatizados de contrato criados.
- [x] OpenAPI/Swagger validado com parametros do endpoint.
- [x] Validacao real com SQL Server concluida.
- [x] Total real validado: 72 registros.
- [x] Filtros reais validados conforme `docs/resultados_endpoint.md`.
- [x] Filtro sem resultado validado com `data=[]`.
- [x] `page_size=101` validado com HTTP 422.
- [x] Intervalo invalido `data_inicio > data_fim` validado com HTTP 422.
- [x] `pytest` executado com 19 testes aprovados.
- [x] Documentacao tecnica do endpoint criada.
- [x] Nenhuma alteracao realizada no SQL Server.

## Fase 2.5 - Endpoint read-only de nao conformidades

- [x] View `VW_ResultadosForaDoPadrao` inspecionada em modo read-only.
- [x] Shape reduzido da view documentado.
- [x] Endpoint `GET /api/v1/resultados/nao-conformidades` criado.
- [x] Router de resultados reaproveitado.
- [x] Schema de resultados reaproveitado.
- [x] Repository de resultados ampliado com consulta read-only da view.
- [x] Service de resultados ampliado.
- [x] Conformidade consumida das views, sem recalculo em Python.
- [x] Paginacao `page` e `page_size` implementada.
- [x] Limite maximo de `page_size` definido em 100.
- [x] Testes automatizados de contrato criados.
- [x] OpenAPI/Swagger validado com parametros do endpoint.
- [x] Validacao real com SQL Server concluida.
- [x] Total real validado: 7 registros.
- [x] Filtros reais validados conforme `docs/resultados_nao_conformidades_endpoint.md`.
- [x] Filtro sem resultado validado com `data=[]`.
- [x] `page_size=101` validado com HTTP 422.
- [x] Intervalo invalido `data_inicio > data_fim` validado com HTTP 422.
- [x] `pytest` executado com 24 testes aprovados.
- [x] Documentacao tecnica do endpoint criada.
- [x] Nenhuma alteracao realizada no SQL Server.

## Fase 2.6 - Endpoint read-only de resultados sem limite

- [x] View `VW_ResultadosSemLimiteReferencia` inspecionada em modo read-only.
- [x] Shape reduzido da view documentado.
- [x] Endpoint `GET /api/v1/resultados/sem-limite-referencia` criado.
- [x] Router de resultados reaproveitado.
- [x] Schema de resultados reaproveitado.
- [x] Repository de resultados ampliado com consulta read-only da view.
- [x] Service de resultados ampliado.
- [x] Conformidade consumida das views, sem recalculo em Python.
- [x] Paginacao `page` e `page_size` implementada.
- [x] Limite maximo de `page_size` definido em 100.
- [x] Testes automatizados de contrato criados.
- [x] OpenAPI/Swagger validado com parametros do endpoint.
- [x] Validacao real com SQL Server concluida.
- [x] Total real validado: 15 registros.
- [x] Filtros reais validados conforme `docs/resultados_sem_limite_referencia_endpoint.md`.
- [x] Filtro sem resultado validado com `data=[]`.
- [x] `page_size=101` validado com HTTP 422.
- [x] Intervalo invalido `data_inicio > data_fim` validado com HTTP 422.
- [x] `pytest` executado com 29 testes aprovados.
- [x] Documentacao tecnica do endpoint criada.
- [x] Nenhuma alteracao realizada no SQL Server.

## Fase 2.7 - Endpoint analitico read-only de resumo mensal

- [x] View `VW_ConformidadeMensal` inspecionada em modo read-only.
- [x] Colunas e tipos reais confirmados.
- [x] Granularidade real confirmada por `AnoColeta` e `MesColeta`.
- [x] Endpoint `GET /api/v1/resultados/resumo-mensal` criado.
- [x] Router de resultados reaproveitado.
- [x] Schema de resumo mensal criado em `app/schemas/resultados.py`.
- [x] Repository de resultados ampliado com consulta read-only da view.
- [x] Service de resultados ampliado.
- [x] Indicadores consumidos da view, sem recalculo em Python.
- [x] Decimal convertido para numero JSON.
- [x] Paginacao `page` e `page_size` implementada.
- [x] Limite maximo de `page_size` definido em 100.
- [x] Filtros `ano` e `mes` implementados.
- [x] Testes automatizados de contrato criados.
- [x] OpenAPI/Swagger validado com parametros do endpoint.
- [x] Validacao real com SQL Server concluida.
- [x] Total real validado: 1 registro mensal.
- [x] Periodo real validado: abril de 2026.
- [x] Filtro sem resultado validado com `data=[]`.
- [x] `page_size=101` validado com HTTP 422.
- [x] `mes=13` validado com HTTP 422.
- [x] `pytest` executado com 34 testes aprovados.
- [x] Documentacao tecnica do endpoint criada.
- [x] Nenhuma alteracao realizada no SQL Server.

## Fase 2.8 - Endpoint analitico read-only de parametros criticos

- [x] View `VW_RankingParametrosCriticos` inspecionada em modo read-only.
- [x] Colunas e tipos reais confirmados.
- [x] Endpoint `GET /api/v1/resultados/parametros-criticos` criado.
- [x] Router de resultados reaproveitado.
- [x] Schema de parametros criticos criado em `app/schemas/resultados.py`.
- [x] Repository de resultados ampliado com consulta read-only da view.
- [x] Service de resultados ampliado.
- [x] Indicadores consumidos da view, sem recalculo em Python.
- [x] Ranking calculado em SQL com `ROW_NUMBER()` sobre indicadores oficiais.
- [x] Decimal convertido para numero JSON.
- [x] Paginacao `page` e `page_size` implementada.
- [x] Limite maximo de `page_size` definido em 100.
- [x] Filtros `categoria` e `limit` implementados.
- [x] Limite maximo de `limit` definido em 100.
- [x] Testes automatizados de contrato criados.
- [x] OpenAPI/Swagger validado com parametros do endpoint.
- [x] Validacao real com SQL Server concluida.
- [x] Total real validado: 12 parametros.
- [x] Ranking 1 validado: `Turbidez`.
- [x] Filtro sem resultado validado com `data=[]`.
- [x] `page_size=101` validado com HTTP 422.
- [x] `limit=101` validado com HTTP 422.
- [x] `pytest` executado com 39 testes aprovados.
- [x] Documentacao tecnica do endpoint criada.
- [x] Nenhuma alteracao realizada no SQL Server.

## Fase 3.0 - Padronizacao interna da API

- [x] Schema padrao de erro criado.
- [x] Handlers globais registrados.
- [x] Handler de `RequestValidationError` implementado.
- [x] Handler de `HTTPException` implementado.
- [x] Handler de erro inesperado implementado.
- [x] Logging basico configurado.
- [x] Constantes de paginacao centralizadas.
- [x] Helper de offset criado.
- [x] Validacao reutilizavel de intervalo de datas criada.
- [x] Services de amostras e resultados usando validacao reutilizavel.
- [x] Contrato de sucesso preservado.
- [x] Contrato de erro padronizado.
- [x] Testes de erro adicionados.
- [x] `pytest` executado com 41 testes aprovados.
- [x] Documento `docs/padroes_api.md` criado.
- [x] Nenhum endpoint de dominio criado.
- [x] Nenhuma alteracao realizada no SQL Server.

## Fase 3.0.1 - Preparacao para publicacao no GitHub

- [x] `.gitignore` auditado.
- [x] `.env` confirmado fora do Git.
- [x] `.env.example` revisado e sanitizado.
- [x] Arquivos rastreados auditados com `git ls-files`.
- [x] Busca por possiveis segredos executada.
- [x] README revisado como produto GitHub.
- [x] Documento `docs/publicacao_github.md` criado.
- [x] `pytest` executado com 41 testes aprovados.
- [x] Snapshot da Fase 3.0.1 gerado.
- [x] Nenhum endpoint criado.
- [x] Nenhuma alteracao realizada no SQL Server.
