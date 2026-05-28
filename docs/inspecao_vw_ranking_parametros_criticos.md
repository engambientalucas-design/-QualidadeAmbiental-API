# Inspecao da View VW_RankingParametrosCriticos

Data da inspecao: 2026-05-28.

## Objetivo

Registrar a inspecao read-only da view `VW_RankingParametrosCriticos` antes da implementacao do endpoint `GET /api/v1/resultados/parametros-criticos`.

Esta etapa confirma o contrato real da view e evita que a API recalcule indicadores ja consolidados no SQL Server.

## Fonte

- Banco: `QualidadeAmbiental`
- View: `VW_RankingParametrosCriticos`
- Modo de acesso: read-only
- Alteracoes no SQL Server: nenhuma

## Colunas Confirmadas

| Coluna | Tipo SQL Server | Nullable | Campo publico |
| ------ | --------------- | -------- | ------------- |
| `IdParametro` | `int` | NO | `id_parametro` |
| `NomeParametro` | `varchar` | NO | `nome_parametro` |
| `Categoria` | `varchar` | YES | `categoria` |
| `TotalResultados` | `int` | YES | `total_resultados` |
| `ResultadosComLimite` | `int` | YES | `resultados_com_limite` |
| `ResultadosSemLimite` | `int` | YES | `resultados_sem_limite` |
| `TotalNaoConformidades` | `int` | YES | `total_nao_conformidades` |
| `PercentualNaoConformidadeComLimite` | `decimal` | YES | `percentual_nao_conformidade_com_limite` |

## Volume

| Item | Valor |
| ---- | ----- |
| Total de registros | 12 |
| Categorias distintas | 6 |

## Distribuicao por Categoria

| Categoria | Quantidade |
| --------- | ---------- |
| Fisico-quimico | 5 |
| Materia organica | 2 |
| Nutrientes | 2 |
| Desinfeccao | 1 |
| Microbiologico | 1 |
| Solidos | 1 |

## Amostra Ordenada

Ordenacao aplicada pela API:

```sql
TotalNaoConformidades DESC,
PercentualNaoConformidadeComLimite DESC,
IdParametro ASC
```

Top 3 observado:

| Ranking | Parametro | Categoria | Nao conformidades | Percentual |
| ------- | --------- | --------- | ----------------- | ---------- |
| 1 | Turbidez | Fisico-quimico | 2 | 40.00 |
| 2 | Cloro Residual Livre | Desinfeccao | 1 | 50.00 |
| 3 | Oxigenio Dissolvido | Fisico-quimico | 1 | 33.33 |

## Indicadores

- `TotalResultados`: quantidade total de resultados associados ao parametro.
- `ResultadosComLimite`: quantidade de resultados com limite de referencia.
- `ResultadosSemLimite`: quantidade de resultados sem limite de referencia.
- `TotalNaoConformidades`: quantidade de resultados nao conformes com limite.
- `PercentualNaoConformidadeComLimite`: percentual de nao conformidade considerando resultados com limite.

A API nao recalcula esses indicadores em Python.

## Ranking

A view nao possui coluna fisica `Ranking`.

Para expor um campo publico `ranking`, a API calcula a posicao no SQL usando `ROW_NUMBER()` sobre os indicadores oficiais da view. Isso cria uma ordenacao estavel sem recalcular os indicadores de negocio.

## Filtros Possiveis

Filtros confirmados:

- `categoria`
- `limit`
- `page`
- `page_size`

O parametro `limit` foi mantido porque representa o recorte Top N, comum em ranking analitico. A paginacao continua disponivel para manter o contrato padronizado.

## Conclusao Tecnica

A view esta adequada para o endpoint analitico `GET /api/v1/resultados/parametros-criticos`.

O contrato publico deve usar `percentual_nao_conformidade_com_limite` para deixar claro que o denominador considera somente resultados com limite de referencia.
