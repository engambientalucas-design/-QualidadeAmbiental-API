# Inspecao da View VW_ConformidadeMensal

Data da inspecao: 2026-05-28.

## Objetivo

Registrar a inspecao read-only da view `VW_ConformidadeMensal` antes da implementacao do endpoint `GET /api/v1/resultados/resumo-mensal`.

Esta etapa confirma o contrato real da view e evita que a API recalcule indicadores ja consolidados no SQL Server.

## Fonte

- Banco: `QualidadeAmbiental`
- View: `VW_ConformidadeMensal`
- Modo de acesso: read-only
- Alteracoes no SQL Server: nenhuma

## Colunas Confirmadas

| Coluna | Tipo SQL Server | Nullable | Campo publico |
| ------ | --------------- | -------- | ------------- |
| `AnoColeta` | `int` | YES | `ano_coleta` |
| `MesColeta` | `int` | YES | `mes_coleta` |
| `TotalResultados` | `int` | YES | `total_resultados` |
| `ResultadosComLimite` | `int` | YES | `resultados_com_limite` |
| `ResultadosSemLimite` | `int` | YES | `resultados_sem_limite` |
| `ResultadosConformesComLimite` | `int` | YES | `resultados_conformes_com_limite` |
| `ResultadosNaoConformesComLimite` | `int` | YES | `resultados_nao_conformes_com_limite` |
| `PercentualConformidadeComLimite` | `decimal` | YES | `percentual_conformidade_com_limite` |

## Volume e Periodo

| Item | Valor |
| ---- | ----- |
| Total de registros | 1 |
| Ano minimo | 2026 |
| Mes minimo | 4 |
| Ano maximo | 2026 |
| Mes maximo | 4 |

## Amostra Real

```json
{
  "AnoColeta": 2026,
  "MesColeta": 4,
  "TotalResultados": 72,
  "ResultadosComLimite": 57,
  "ResultadosSemLimite": 15,
  "ResultadosConformesComLimite": 50,
  "ResultadosNaoConformesComLimite": 7,
  "PercentualConformidadeComLimite": "87.72"
}
```

## Granularidade

A view possui granularidade mensal por `AnoColeta` e `MesColeta`.

Como a view nao possui campos de municipio, categoria, ponto de coleta ou parametro, a API nao deve expor filtros desse tipo neste endpoint.

## Indicadores

Os indicadores sao retornados diretamente pela view:

- total de resultados;
- resultados com limite;
- resultados sem limite;
- resultados conformes com limite;
- resultados nao conformes com limite;
- percentual de conformidade considerando somente resultados com limite.

A API nao recalcula nenhum desses indicadores em Python.

## Conversao de Tipos

- Campos `int` sao expostos como `int | null`.
- `PercentualConformidadeComLimite` vem como `Decimal` e deve ser serializado como numero JSON.

## Filtros Possiveis

Filtros confirmados pela granularidade real:

- `ano`
- `mes`
- `page`
- `page_size`

## Conclusao Tecnica

A view esta adequada para o endpoint analitico `GET /api/v1/resultados/resumo-mensal`.

O contrato publico deve respeitar a granularidade real da view e evitar filtros inexistentes na fonte.
