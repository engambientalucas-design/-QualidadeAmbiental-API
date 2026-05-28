# Endpoint de Nao Conformidades

## Objetivo

Documentar o endpoint read-only da Fase 2.5:

```http
GET /api/v1/resultados/nao-conformidades
```

O endpoint lista resultados fora do padrao, usando a view `VW_ResultadosForaDoPadrao` como fonte do recorte de nao conformidade.

## Fonte de dados

Fonte principal do recorte:

```text
VW_ResultadosForaDoPadrao
```

Como a view possui um conjunto reduzido de colunas, o endpoint junta por `IdResultado` com:

```text
VW_ConformidadeResultados
```

Assim, a API mantem o mesmo contrato publico de `GET /api/v1/resultados` sem recalcular conformidade em Python.

## Campos publicos

O contrato de resposta reutiliza o schema de resultados consolidados:

- `id_resultado`
- `id_amostra`
- `codigo_amostra`
- `data_coleta`
- `hora_coleta`
- `id_tipo_amostra`
- `nome_tipo_amostra`
- `id_ponto_coleta`
- `nome_ponto`
- `tipo_ponto`
- `municipio`
- `estado`
- `id_responsavel`
- `nome_responsavel`
- `id_status`
- `nome_status`
- `id_parametro`
- `nome_parametro`
- `categoria`
- `valor_resultado`
- `unidade_medida`
- `data_analise`
- `metodo_analise`
- `id_limite`
- `valor_minimo`
- `valor_maximo`
- `referencia_normativa`
- `classificacao_resultado`
- `possui_limite_referencia`
- `indicador_nao_conforme`

## Filtros

| Parametro | Tipo | Obrigatorio | Descricao |
| --------- | ---- | ----------- | --------- |
| `data_inicio` | `date` | Nao | Filtra coletas a partir desta data. |
| `data_fim` | `date` | Nao | Filtra coletas ate esta data. |
| `municipio` | `string` | Nao | Filtra por municipio. |
| `id_ponto_coleta` | `integer` | Nao | Filtra por ponto de coleta. |
| `id_parametro` | `integer` | Nao | Filtra por parametro. |
| `categoria` | `string` | Nao | Filtra por categoria do parametro. |
| `classificacao_resultado` | `string` | Nao | Filtra pela classificacao produzida pela view. |

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
GET /api/v1/resultados/nao-conformidades?municipio=Cuiaba&page=1&page_size=20
```

## Exemplo de response

```json
{
  "success": true,
  "message": "Consulta realizada com sucesso.",
  "data": [
    {
      "id_resultado": 71,
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
      "id_parametro": 11,
      "nome_parametro": "Fosforo Total",
      "categoria": "Nutrientes",
      "valor_resultado": 0.2,
      "unidade_medida": "mg/L",
      "data_analise": "2026-04-09",
      "metodo_analise": "Metodo didatico",
      "id_limite": 18,
      "valor_minimo": null,
      "valor_maximo": 0.1,
      "referencia_normativa": "Limite didatico do projeto",
      "classificacao_resultado": "Acima do limite maximo",
      "possui_limite_referencia": true,
      "indicador_nao_conforme": true
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 7
  }
}
```

## Validacao real

Validacao com SQL Server real concluida em 2026-05-28.

| Cenario | Resultado |
| ------- | --------- |
| `GET /api/v1/resultados/nao-conformidades` | 7 registros |
| `page=1&page_size=2` | 2 itens, `total=7` |
| `municipio=Cuiaba` | 5 registros |
| `categoria=Fisico-quimico` | 3 registros |
| `classificacao_resultado=Acima do limite maximo` | 5 registros |
| `classificacao_resultado=Abaixo do limite minimo` | 2 registros |
| `id_parametro=11` | 1 registro |
| `id_ponto_coleta=6` | 2 registros |
| `data_inicio=2026-04-01&data_fim=2026-04-03` | 7 registros |
| Filtro sem resultado | `data=[]`, `total=0` |
| `page_size=101` | HTTP 422 |
| `data_inicio > data_fim` | HTTP 422 |

Todos os registros retornados apresentaram `indicador_nao_conforme=true` na validacao real.

## Riscos e melhorias futuras

- Criar endpoint especifico para resultados sem limite de referencia.
- Criar endpoint de resumo mensal usando `VW_ConformidadeMensal`.
- Criar endpoint de ranking de parametros criticos.
- Avaliar filtros adicionais como `codigo_amostra` caso o consumo externo demande.
- Criar testes de integracao separados para SQL Server real.
