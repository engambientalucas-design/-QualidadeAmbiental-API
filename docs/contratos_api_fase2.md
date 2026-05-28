# Contratos Planejados da API - Fase 2

Este documento planeja os primeiros contratos read-only da API antes da implementacao.

A Fase 2 ainda deve respeitar a arquitetura:

```text
router -> service -> repository -> banco
```

Nao colocar SQL diretamente nos routers.

## Padrao geral de resposta

Listas devem seguir o envelope ja documentado:

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

Recursos individuais podem usar o mesmo envelope sem `pagination`.

## GET /api/v1/pontos-coleta

Status: implementado e validado.

Objetivo: listar pontos de coleta.

Fonte primaria: `Tbl_PontosColeta`.

Filtros iniciais:

- `municipio`;
- `estado`;
- `tipo_ponto`;
- `page`;
- `page_size`.

Campos sugeridos:

- `id_ponto_coleta`;
- `nome_ponto`;
- `tipo_ponto`;
- `municipio`;
- `estado`;
- `latitude`;
- `longitude`;
- `observacao`.

## GET /api/v1/parametros

Status: implementado e validado.

Objetivo: listar parametros ambientais.

Fonte primaria: `Tbl_Parametros`.

Filtros iniciais:

- `categoria`;
- `ativo`;
- `page`;
- `page_size`.

Campos sugeridos:

- `id_parametro`;
- `nome_parametro`;
- `unidade_medida`;
- `categoria`;
- `descricao`;
- `ativo`.

## GET /api/v1/amostras

Status: implementado e validado.

Objetivo: listar amostras com dados de ponto, tipo, status e responsavel.

Fonte primaria: `Tbl_Amostras` com joins nas tabelas de dominio.

Filtros iniciais:

- `data_inicio`;
- `data_fim`;
- `id_ponto_coleta`;
- `municipio`;
- `id_tipo_amostra`;
- `id_status`;
- `page`;
- `page_size`.

Campos sugeridos:

- `id_amostra`;
- `codigo_amostra`;
- `data_coleta`;
- `hora_coleta`;
- `id_ponto_coleta`;
- `nome_ponto`;
- `municipio`;
- `estado`;
- `id_tipo_amostra`;
- `nome_tipo_amostra`;
- `id_status`;
- `nome_status`;
- `id_responsavel`;
- `nome_responsavel`;
- `observacao`.

## GET /api/v1/resultados

Status: implementado e validado.

Objetivo: listar resultados analiticos consolidados.

Fonte recomendada: `VW_ConformidadeResultados`.

Filtros iniciais:

- `data_inicio`;
- `data_fim`;
- `id_amostra`;
- `codigo_amostra`;
- `id_ponto_coleta`;
- `municipio`;
- `id_parametro`;
- `categoria`;
- `classificacao_resultado`;
- `possui_limite_referencia`;
- `indicador_nao_conforme`;
- `page`;
- `page_size`.

Campos sugeridos:

- `id_resultado`;
- `id_amostra`;
- `codigo_amostra`;
- `data_coleta`;
- `nome_tipo_amostra`;
- `nome_ponto`;
- `municipio`;
- `estado`;
- `nome_parametro`;
- `categoria`;
- `valor_resultado`;
- `unidade_medida`;
- `valor_minimo`;
- `valor_maximo`;
- `classificacao_resultado`;
- `possui_limite_referencia`;
- `indicador_nao_conforme`.

## GET /api/v1/resultados/nao-conformidades

Status: implementado e validado.

Objetivo: listar resultados fora do padrao.

Fonte recomendada: `VW_ResultadosForaDoPadrao`.

Filtros iniciais:

- `data_inicio`;
- `data_fim`;
- `municipio`;
- `id_ponto_coleta`;
- `id_parametro`;
- `categoria`;
- `classificacao_resultado`;
- `page`;
- `page_size`.

## GET /api/v1/resultados/sem-limite-referencia

Status: implementado e validado.

Objetivo: listar resultados sem limite de referencia cadastrado.

Fonte recomendada: `VW_ResultadosSemLimiteReferencia`.

Filtros iniciais:

- `data_inicio`;
- `data_fim`;
- `municipio`;
- `id_ponto_coleta`;
- `id_parametro`;
- `categoria`;
- `codigo_amostra`;
- `id_amostra`;
- `page`;
- `page_size`.

## GET /api/v1/resultados/resumo-mensal

Status: implementado e validado.

Objetivo: expor resumo mensal de conformidade.

Fonte recomendada: `VW_ConformidadeMensal`.

Filtros iniciais:

- `ano`;
- `mes`;
- `page`;
- `page_size`.

Campos sugeridos:

- `ano_coleta`;
- `mes_coleta`;
- `total_resultados`;
- `resultados_com_limite`;
- `resultados_sem_limite`;
- `resultados_conformes_com_limite`;
- `resultados_nao_conformes_com_limite`;
- `percentual_conformidade_com_limite`.

Observacao: filtros por municipio, categoria, ponto de coleta ou parametro nao foram implementados porque a view mensal possui granularidade apenas por ano e mes.

## GET /api/v1/resultados/parametros-criticos

Status: implementado e validado.

Objetivo: ranking de parametros por nao conformidade.

Fonte recomendada: `VW_RankingParametrosCriticos`.

Filtros iniciais:

- `categoria`;
- `limit`;
- `page`;
- `page_size`.

Campos publicos:

- `ranking`;
- `id_parametro`;
- `nome_parametro`;
- `categoria`;
- `total_resultados`;
- `resultados_com_limite`;
- `resultados_sem_limite`;
- `total_nao_conformidades`;
- `percentual_nao_conformidade_com_limite`.

Observacao: a view nao possui coluna fisica de ranking. A API calcula a posicao em SQL com `ROW_NUMBER()` usando indicadores oficiais da view, sem recalcular indicadores de negocio em Python.

## Fora do escopo imediato

- CRUD;
- autenticacao/JWT;
- migrations;
- alteracao de schema SQL Server;
- endpoints de auditoria;
- Docker;
- deploy;
- frontend.

## Fechamento da Fase 2

Status: contratos da Fase 2 implementados e validados em SQL Server real.

Proximo passo recomendado: iniciar a Fase 3 com foco em padronizacao de erros, reducao de duplicacoes, observabilidade leve e melhoria incremental dos testes.
