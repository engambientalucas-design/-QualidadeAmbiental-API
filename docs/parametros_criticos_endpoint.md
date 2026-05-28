# Endpoint GET /api/v1/resultados/parametros-criticos

## Objetivo

Expor ranking de parametros criticos com base nas nao conformidades consolidadas pela view `VW_RankingParametrosCriticos`.

Este endpoint faz parte da Fase 2.8 e conclui a camada analitica inicial da API.

## Fonte de Dados

- Banco: `QualidadeAmbiental`
- Fonte oficial: `VW_RankingParametrosCriticos`
- Modo: read-only

A API nao recalcula indicadores em Python. Totais e percentuais sao retornados pela view.

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
VW_RankingParametrosCriticos
   ->
Schema Pydantic
   ->
Resposta JSON
```

## Campos Publicos

| Campo | Tipo | Origem |
| ----- | ---- | ------ |
| `ranking` | `int` | Posicao calculada em SQL com `ROW_NUMBER()` |
| `id_parametro` | `int` | `IdParametro` |
| `nome_parametro` | `str` | `NomeParametro` |
| `categoria` | `str | null` | `Categoria` |
| `total_resultados` | `int | null` | `TotalResultados` |
| `resultados_com_limite` | `int | null` | `ResultadosComLimite` |
| `resultados_sem_limite` | `int | null` | `ResultadosSemLimite` |
| `total_nao_conformidades` | `int | null` | `TotalNaoConformidades` |
| `percentual_nao_conformidade_com_limite` | `float | null` | `PercentualNaoConformidadeComLimite` |

## Filtros

| Parametro | Tipo | Regra |
| --------- | ---- | ----- |
| `categoria` | `str` | Opcional, filtra por categoria do parametro |
| `limit` | `int` | Opcional, Top N entre 1 e 100 |
| `page` | `int` | Padrao 1, minimo 1 |
| `page_size` | `int` | Padrao 20, minimo 1, maximo 100 |

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

Quando `limit` e usado, `pagination.total` representa o total apos o recorte Top N.

## Ordenacao

Ordenacao padrao:

```sql
TotalNaoConformidades DESC,
PercentualNaoConformidadeComLimite DESC,
IdParametro ASC
```

## Exemplos

Consulta geral:

```http
GET /api/v1/resultados/parametros-criticos
```

Top 3:

```http
GET /api/v1/resultados/parametros-criticos?limit=3
```

Filtro por categoria:

```http
GET /api/v1/resultados/parametros-criticos?categoria=Fisico-quimico
```

## Exemplo de Resposta

```json
{
  "success": true,
  "message": "Consulta realizada com sucesso.",
  "data": [
    {
      "ranking": 1,
      "id_parametro": 2,
      "nome_parametro": "Turbidez",
      "categoria": "Fisico-quimico",
      "total_resultados": 6,
      "resultados_com_limite": 5,
      "resultados_sem_limite": 1,
      "total_nao_conformidades": 2,
      "percentual_nao_conformidade_com_limite": 40.0
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 12
  }
}
```

## Validacao Real

Validado em 2026-05-28 contra SQL Server real:

| Cenario | Resultado |
| ------- | --------- |
| `GET /api/v1/resultados/parametros-criticos` | total 12 |
| `page=1&page_size=2` | 2 itens, total 12 |
| `categoria=Fisico-quimico` | total 5 |
| `limit=3` | 3 itens, total 3 |
| `limit=3&page=1&page_size=2` | 2 itens, total 3 |
| `categoria=CategoriaInexistente` | `data=[]`, total 0 |
| `page_size=101` | HTTP 422 |
| `limit=101` | HTTP 422 |

Ranking 1 observado: `Turbidez`, com 2 nao conformidades e 40.0% de nao conformidade com limite.

## Riscos e Melhorias Futuras

- Se a view passar a expor uma coluna fisica de ranking, o repository pode consumir essa coluna diretamente.
- Novos filtros so devem ser adicionados se existirem na fonte oficial ou em uma view analitica especifica.
- O percentual deve continuar vindo da view para preservar a regra oficial do banco.
