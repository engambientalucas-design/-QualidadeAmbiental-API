# Fechamento Tecnico da Fase 2

Data do fechamento: 2026-05-28.

## Objetivo

Consolidar a camada read-only e analitica inicial da `QualidadeAmbiental API`, auditando contratos, arquitetura, documentacao e estado operacional antes da entrada na Fase 3.

Esta fase nao criou novos endpoints, nao alterou o SQL Server e nao modificou contratos publicos existentes.

## Objetivos Alcancados

- Arquitetura `router -> service -> repository -> SQL Server` validada ponta a ponta.
- API REST read-only consolidada.
- SQL Server real validado.
- Swagger/OpenAPI validado.
- Endpoints operacionais, relacionais e analiticos implementados.
- Documentacao tecnica por endpoint criada.
- Inspecoes de views analiticas documentadas.
- Testes automatizados aprovados.
- Snapshots por fase gerados.
- Git mantido com commits tecnicos por etapa.

## Endpoints Implementados

| Endpoint | Fonte principal | Status |
| -------- | --------------- | ------ |
| `GET /health` | Aplicacao | Implementado |
| `GET /api/v1/pontos-coleta` | `Tbl_PontosColeta` | Implementado e validado |
| `GET /api/v1/parametros` | `Tbl_Parametros` | Implementado e validado |
| `GET /api/v1/amostras` | `Tbl_Amostras` + joins | Implementado e validado |
| `GET /api/v1/resultados` | `VW_ConformidadeResultados` | Implementado e validado |
| `GET /api/v1/resultados/nao-conformidades` | `VW_ResultadosForaDoPadrao` | Implementado e validado |
| `GET /api/v1/resultados/sem-limite-referencia` | `VW_ResultadosSemLimiteReferencia` | Implementado e validado |
| `GET /api/v1/resultados/resumo-mensal` | `VW_ConformidadeMensal` | Implementado e validado |
| `GET /api/v1/resultados/parametros-criticos` | `VW_RankingParametrosCriticos` | Implementado e validado |

## Views Consumidas

| View | Uso na API |
| ---- | ---------- |
| `VW_ConformidadeResultados` | Resultado analitico consolidado e complemento de recortes derivados |
| `VW_ResultadosForaDoPadrao` | Recorte oficial de nao conformidades |
| `VW_ResultadosSemLimiteReferencia` | Recorte oficial de resultados sem limite |
| `VW_ConformidadeMensal` | Resumo mensal de conformidade |
| `VW_RankingParametrosCriticos` | Ranking de parametros criticos |

## Contratos Publicos Auditados

Padroes confirmados:

- campos publicos em `snake_case`;
- resposta de listas com `success`, `message`, `data` e `pagination`;
- paginacao por `page` e `page_size`;
- limite maximo de `page_size=100`;
- erros de validacao retornando HTTP 422;
- SQL concentrado em repositories;
- routers sem acesso direto ao banco;
- services sem detalhes HTTP excessivos, exceto validacoes leves que retornam HTTP 422;
- endpoints analiticos consumindo views sem recalcular indicadores em Python.

## Tabela Consolidada de Filtros

| Endpoint | Filtros |
| -------- | ------- |
| `/api/v1/pontos-coleta` | `municipio`, `estado`, `tipo_ponto`, `page`, `page_size` |
| `/api/v1/parametros` | `categoria`, `ativo`, `page`, `page_size` |
| `/api/v1/amostras` | `data_inicio`, `data_fim`, `id_ponto_coleta`, `municipio`, `id_tipo_amostra`, `id_status`, `page`, `page_size` |
| `/api/v1/resultados` | `data_inicio`, `data_fim`, `id_amostra`, `codigo_amostra`, `id_ponto_coleta`, `municipio`, `id_parametro`, `categoria`, `classificacao_resultado`, `possui_limite_referencia`, `indicador_nao_conforme`, `page`, `page_size` |
| `/api/v1/resultados/nao-conformidades` | `data_inicio`, `data_fim`, `municipio`, `id_ponto_coleta`, `id_parametro`, `categoria`, `classificacao_resultado`, `page`, `page_size` |
| `/api/v1/resultados/sem-limite-referencia` | `data_inicio`, `data_fim`, `municipio`, `id_ponto_coleta`, `id_parametro`, `categoria`, `codigo_amostra`, `id_amostra`, `page`, `page_size` |
| `/api/v1/resultados/resumo-mensal` | `ano`, `mes`, `page`, `page_size` |
| `/api/v1/resultados/parametros-criticos` | `categoria`, `limit`, `page`, `page_size` |

## Revisao OpenAPI

Confirmado:

- todos os endpoints possuem `response_model`;
- query params aparecem no Swagger;
- tags estao presentes;
- endpoints de resultados estao agrupados na tag `resultados`;
- modelos Pydantic aparecem no schema OpenAPI.

Melhorias futuras:

- padronizar acentuacao e encoding das descricoes antigas;
- enriquecer exemplos de responses por endpoint;
- documentar respostas de erro padronizadas;
- avaliar tags mais granulares para endpoints analiticos.

## Decisoes Arquiteturais Confirmadas

- API permanece read-only.
- Nenhuma migration ou alteracao de schema SQL Server foi criada.
- Views do banco sao fontes oficiais para indicadores analiticos.
- Repositories concentram SQL parametrizado.
- Services orquestram fluxo e validacoes leves.
- Routers recebem query params e delegam para services.
- Schemas Pydantic definem contratos publicos.

## Riscos Conhecidos

- Repositories de resultados concentram bastante SQL e tendem a crescer.
- `PaginationResponse` esta duplicado em multiplos arquivos de schema.
- `PaginationParams` ainda usa nomenclatura antiga `pagina/tamanho_pagina` e nao esta alinhado ao contrato publico `page/page_size`.
- Tratamento de erro ainda depende majoritariamente do padrao FastAPI.
- Logging e observabilidade ainda sao minimos.
- Alguns textos antigos de documentacao/Swagger apresentam sinais de encoding inconsistente.

## Avisos Operacionais Conhecidos

- `pytest` pode emitir aviso de permissao em `.pytest_cache` no OneDrive, sem impedir a execucao dos testes.
- Git no Windows pode emitir aviso `LF will be replaced by CRLF`, sem impacto funcional.
- Validacoes reais contra SQL Server podem emitir `SAWarning` sobre versao do servidor, sem bloquear consultas.
- Operacoes de Git podem exigir permissao fora do sandbox para gravar em `.git/index.lock`.

## Criterios de Pronto da Fase 2

- [x] Endpoints read-only implementados.
- [x] Endpoints analiticos implementados.
- [x] SQL Server real validado.
- [x] OpenAPI validado.
- [x] Testes automatizados aprovados.
- [x] Documentacao tecnica criada.
- [x] Divida tecnica registrada.
- [x] Checklist de entrada da Fase 3 criado.
- [x] Nenhuma credencial versionada.
- [x] Nenhuma alteracao realizada no SQL Server.

## Recomendacoes para Fase 3

- Padronizar handlers globais de erro.
- Criar contrato padronizado de erro.
- Centralizar schemas de paginacao.
- Revisar duplicacoes em repositories.
- Adicionar logging estruturado basico.
- Adicionar testes de erro e de OpenAPI mais abrangentes.
- Revisar encoding dos arquivos de documentacao e descricoes Swagger.
