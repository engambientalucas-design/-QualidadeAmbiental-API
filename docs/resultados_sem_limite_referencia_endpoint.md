# Endpoint de Resultados Sem Limite de Referencia

## Objetivo

Documentar o endpoint read-only da Fase 2.6:

```http
GET /api/v1/resultados/sem-limite-referencia
```

O endpoint lista resultados que nao possuem limite de referencia cadastrado.

## Fonte de dados

Fonte principal do recorte:

```text
VW_ResultadosSemLimiteReferencia
```

Como a view possui um conjunto reduzido de colunas, o endpoint junta por `IdResultado` com:

```text
VW_ConformidadeResultados
```

Assim, a API mantem o mesmo contrato publico de `GET /api/v1/resultados` sem recalcular conformidade em Python.

## Comportamento esperado

Todos os registros retornados devem apresentar:

- `possui_limite_referencia=false`;
- `indicador_nao_conforme=null`;
- `classificacao_resultado=Sem limite de referencia`.

## Filtros

| Parametro | Tipo | Obrigatorio | Descricao |
| --------- | ---- | ----------- | --------- |
| `data_inicio` | `date` | Nao | Filtra coletas a partir desta data. |
| `data_fim` | `date` | Nao | Filtra coletas ate esta data. |
| `municipio` | `string` | Nao | Filtra por municipio. |
| `id_ponto_coleta` | `integer` | Nao | Filtra por ponto de coleta. |
| `id_parametro` | `integer` | Nao | Filtra por parametro. |
| `categoria` | `string` | Nao | Filtra por categoria do parametro. |
| `codigo_amostra` | `string` | Nao | Filtra por codigo da amostra. |
| `id_amostra` | `integer` | Nao | Filtra por amostra. |

`data_inicio` deve ser menor ou igual a `data_fim`. Caso contrario, a API retorna HTTP 422.

## Paginacao

| Parametro | Padrao | Limite |
| --------- | ------ | ------ |
| `page` | `1` | minimo `1` |
| `page_size` | `20` | minimo `1`, maximo `100` |

## Ordenacao

```sql
ORDER BY DataColeta DESC, IdAmostra DESC, IdResultado DESC
```

## Exemplo de request

```http
GET /api/v1/resultados/sem-limite-referencia?municipio=Cuiaba&page=1&page_size=20
```

## Exemplo de response

```json
{
  "success": true,
  "message": "Consulta realizada com sucesso.",
  "data": [
    {
      "id_resultado": 64,
      "id_amostra": 6,
      "codigo_amostra": "QA-2026-006",
      "data_coleta": "2026-04-03",
      "hora_coleta": "11:15:00",
      "id_tipo_amostra": 2,
      "nome_tipo_amostra": "Agua Tratada",
      "id_ponto_coleta": 6,
      "nome_ponto": "Reservatorio Bairro Leste",
      "tipo_ponto": "Reservatorio",
      "municipio": "Cuiaba",
      "estado": "MT",
      "id_responsavel": 4,
      "nome_responsavel": "Joao Pereira",
      "id_status": 3,
      "nome_status": "Concluida",
      "id_parametro": 4,
      "nome_parametro": "DBO",
      "categoria": "Materia organica",
      "valor_resultado": 2.0,
      "unidade_medida": "mg/L",
      "data_analise": "2026-04-09",
      "metodo_analise": "Metodo didatico",
      "id_limite": null,
      "valor_minimo": null,
      "valor_maximo": null,
      "referencia_normativa": null,
      "classificacao_resultado": "Sem limite de referencia",
      "possui_limite_referencia": false,
      "indicador_nao_conforme": null
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 15
  }
}
```

## Validacao real

Validacao com SQL Server real concluida em 2026-05-28.

| Cenario | Resultado |
| ------- | --------- |
| `GET /api/v1/resultados/sem-limite-referencia` | 15 registros |
| `page=1&page_size=2` | 2 itens, `total=15` |
| `municipio=Cuiaba` | 9 registros |
| `categoria=Fisico-quimico` | 5 registros |
| `id_parametro=4` | 2 registros |
| `id_ponto_coleta=6` | 2 registros |
| `codigo_amostra=QA-2026-006` | 2 registros |
| `id_amostra=6` | 2 registros |
| `data_inicio=2026-04-01&data_fim=2026-04-03` | 15 registros |
| Filtro sem resultado | `data=[]`, `total=0` |
| `page_size=101` | HTTP 422 |
| `data_inicio > data_fim` | HTTP 422 |

## Riscos e melhorias futuras

- Avaliar endpoint especifico para cadastro/qualidade de limites de referencia.
- Criar endpoint de resumo mensal usando `VW_ConformidadeMensal`.
- Criar endpoint de ranking de parametros criticos.
- Criar testes de integracao separados para SQL Server real.
