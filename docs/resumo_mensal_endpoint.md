# Endpoint GET /api/v1/resultados/resumo-mensal

## Objetivo

Expor o resumo mensal de conformidade dos resultados ambientais, consumindo diretamente a view `VW_ConformidadeMensal`.

Este endpoint faz parte da Fase 2.7 e representa o primeiro endpoint analitico agregado mensal da API.

## Fonte de Dados

- Banco: `QualidadeAmbiental`
- Fonte oficial: `VW_ConformidadeMensal`
- Modo: read-only

A API nao recalcula indicadores em Python. Todos os totais e percentuais sao retornados pela view.

## Fluxo Arquitetural

```text
Cliente
   ->
Router
   ->
Service
   ->
Repository
   ->
VW_ConformidadeMensal
   ->
Schema Pydantic
   ->
Resposta JSON
```

## Campos Publicos

| Campo | Tipo | Origem |
| ----- | ---- | ------ |
| `ano_coleta` | `int | null` | `AnoColeta` |
| `mes_coleta` | `int | null` | `MesColeta` |
| `total_resultados` | `int | null` | `TotalResultados` |
| `resultados_com_limite` | `int | null` | `ResultadosComLimite` |
| `resultados_sem_limite` | `int | null` | `ResultadosSemLimite` |
| `resultados_conformes_com_limite` | `int | null` | `ResultadosConformesComLimite` |
| `resultados_nao_conformes_com_limite` | `int | null` | `ResultadosNaoConformesComLimite` |
| `percentual_conformidade_com_limite` | `float | null` | `PercentualConformidadeComLimite` |

## Filtros

| Parametro | Tipo | Regra |
| --------- | ---- | ----- |
| `ano` | `int` | Opcional, entre 2000 e 2100 |
| `mes` | `int` | Opcional, entre 1 e 12 |
| `page` | `int` | Padrao 1, minimo 1 |
| `page_size` | `int` | Padrao 20, minimo 1, maximo 100 |

Filtros por municipio, categoria, ponto de coleta ou parametro nao foram implementados porque a view mensal nao possui essa granularidade.

## Paginacao

Resposta padronizada:

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

## Exemplos

Consulta geral:

```http
GET /api/v1/resultados/resumo-mensal
```

Consulta por ano e mes:

```http
GET /api/v1/resultados/resumo-mensal?ano=2026&mes=4
```

Consulta paginada:

```http
GET /api/v1/resultados/resumo-mensal?page=1&page_size=2
```

## Exemplo de Resposta

```json
{
  "success": true,
  "message": "Consulta realizada com sucesso.",
  "data": [
    {
      "ano_coleta": 2026,
      "mes_coleta": 4,
      "total_resultados": 72,
      "resultados_com_limite": 57,
      "resultados_sem_limite": 15,
      "resultados_conformes_com_limite": 50,
      "resultados_nao_conformes_com_limite": 7,
      "percentual_conformidade_com_limite": 87.72
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 1
  }
}
```

## Ordenacao

A ordenacao padrao e:

```sql
AnoColeta DESC, MesColeta DESC
```

## Validacao Real

Validado em 2026-05-28 contra SQL Server real:

| Cenario | Resultado |
| ------- | --------- |
| `GET /api/v1/resultados/resumo-mensal` | total 1 |
| `page=1&page_size=2` | 1 item, total 1 |
| `ano=2026` | total 1 |
| `mes=4` | total 1 |
| `ano=2026&mes=4` | total 1 |
| `ano=2099` | `data=[]`, total 0 |
| `page_size=101` | HTTP 422 |
| `mes=13` | HTTP 422 |

## Riscos e Melhorias Futuras

- Se a view evoluir para incluir municipio, categoria ou parametro, novos filtros podem ser adicionados.
- Para dashboards, pode ser util adicionar endpoint de serie temporal com granularidade anual ou por municipio, desde que a fonte SQL Server forneca essa agregacao.
- O percentual deve continuar vindo da view para preservar a regra oficial de conformidade.
