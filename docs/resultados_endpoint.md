# Endpoint de Resultados Consolidados

## Objetivo

Documentar o endpoint read-only da Fase 2.4:

```http
GET /api/v1/resultados
```

O endpoint lista resultados analiticos consolidados a partir da view `VW_ConformidadeResultados`.

## Fonte de dados

Fonte oficial:

```text
VW_ConformidadeResultados
```

A view ja consolida resultados, amostras, pontos de coleta, tipos, responsaveis, status, parametros, limites e classificacao de conformidade.

## Por que usar a view

A API nao recalcula conformidade em Python. A classificacao vem diretamente da view por meio dos campos:

- `ClassificacaoResultado`;
- `PossuiLimiteReferencia`;
- `IndicadorNaoConforme`.

Isso evita divergencia entre regra do banco e regra da API.

## Campos publicos

| View | API |
| ---- | --- |
| `IdResultado` | `id_resultado` |
| `IdAmostra` | `id_amostra` |
| `CodigoAmostra` | `codigo_amostra` |
| `DataColeta` | `data_coleta` |
| `HoraColeta` | `hora_coleta` |
| `IdTipoAmostra` | `id_tipo_amostra` |
| `NomeTipoAmostra` | `nome_tipo_amostra` |
| `IdPontoColeta` | `id_ponto_coleta` |
| `NomePonto` | `nome_ponto` |
| `TipoPonto` | `tipo_ponto` |
| `Municipio` | `municipio` |
| `Estado` | `estado` |
| `IdResponsavel` | `id_responsavel` |
| `NomeResponsavel` | `nome_responsavel` |
| `IdStatus` | `id_status` |
| `NomeStatus` | `nome_status` |
| `IdParametro` | `id_parametro` |
| `NomeParametro` | `nome_parametro` |
| `Categoria` | `categoria` |
| `ValorResultado` | `valor_resultado` |
| `UnidadeMedida` | `unidade_medida` |
| `DataAnalise` | `data_analise` |
| `MetodoAnalise` | `metodo_analise` |
| `IdLimite` | `id_limite` |
| `ValorMinimo` | `valor_minimo` |
| `ValorMaximo` | `valor_maximo` |
| `ReferenciaNormativa` | `referencia_normativa` |
| `ClassificacaoResultado` | `classificacao_resultado` |
| `PossuiLimiteReferencia` | `possui_limite_referencia` |
| `IndicadorNaoConforme` | `indicador_nao_conforme` |

## Conversao de tipos

- `ValorResultado`, `ValorMinimo` e `ValorMaximo`: `Decimal` no banco, numero JSON na API.
- `PossuiLimiteReferencia`: `int` na view, `boolean` na API.
- `IndicadorNaoConforme`: `int` ou `NULL` na view, `boolean | null` na API.
- `DataColeta` e `DataAnalise`: `date`.
- `HoraColeta`: `time | null`.

## Filtros

| Parametro | Tipo | Obrigatorio | Descricao |
| --------- | ---- | ----------- | --------- |
| `data_inicio` | `date` | Nao | Filtra coletas a partir desta data. |
| `data_fim` | `date` | Nao | Filtra coletas ate esta data. |
| `id_amostra` | `integer` | Nao | Filtra por amostra. |
| `codigo_amostra` | `string` | Nao | Filtra por codigo da amostra. |
| `id_ponto_coleta` | `integer` | Nao | Filtra por ponto de coleta. |
| `municipio` | `string` | Nao | Filtra por municipio. |
| `id_parametro` | `integer` | Nao | Filtra por parametro. |
| `categoria` | `string` | Nao | Filtra por categoria do parametro. |
| `classificacao_resultado` | `string` | Nao | Filtra pela classificacao produzida pela view. |
| `possui_limite_referencia` | `boolean` | Nao | Filtra resultados com ou sem limite. |
| `indicador_nao_conforme` | `boolean` | Nao | Filtra resultados conformes ou nao conformes quando ha limite. |

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
GET /api/v1/resultados?municipio=Cuiaba&categoria=Fisico-quimico&page=1&page_size=20
```

## Exemplo de response

```json
{
  "success": true,
  "message": "Consulta realizada com sucesso.",
  "data": [
    {
      "id_resultado": 72,
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
      "id_parametro": 12,
      "nome_parametro": "Cloro Residual Livre",
      "categoria": "Desinfeccao",
      "valor_resultado": 0.8,
      "unidade_medida": "mg/L",
      "data_analise": "2026-04-09",
      "metodo_analise": "Metodo didatico",
      "id_limite": 19,
      "valor_minimo": 0.2,
      "valor_maximo": 2.0,
      "referencia_normativa": "Limite didatico do projeto",
      "classificacao_resultado": "Conforme",
      "possui_limite_referencia": true,
      "indicador_nao_conforme": false
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 72
  }
}
```

## Validacao real

Validacao com SQL Server real concluida em 2026-05-28.

| Cenario | Resultado |
| ------- | --------- |
| `GET /api/v1/resultados` | 72 registros |
| `page=1&page_size=2` | 2 itens, `total=72` |
| `municipio=Cuiaba` | 48 registros |
| `id_parametro=11` | 6 registros |
| `categoria=Fisico-quimico` | 30 registros |
| `classificacao_resultado=Conforme` | 50 registros |
| `indicador_nao_conforme=true` | 7 registros |
| `indicador_nao_conforme=false` | 50 registros |
| `possui_limite_referencia=false` | 15 registros |
| `possui_limite_referencia=true` | 57 registros |
| `codigo_amostra=QA-2026-006` | 12 registros |
| `id_amostra=6` | 12 registros |
| `id_ponto_coleta=6` | 12 registros |
| `data_inicio=2026-04-01&data_fim=2026-04-03` | 72 registros |
| Filtro sem resultado | `data=[]`, `total=0` |
| `page_size=101` | HTTP 422 |
| `data_inicio > data_fim` | HTTP 422 |

## Riscos e melhorias futuras

- Criar endpoint especifico para nao conformidades usando `VW_ResultadosForaDoPadrao`.
- Criar endpoint especifico para resultados sem limite de referencia.
- Criar endpoint de resumo mensal usando `VW_ConformidadeMensal`.
- Criar endpoint de ranking de parametros criticos.
- Avaliar ordenacao controlada por parametros seguros.
- Criar testes de integracao separados para SQL Server real.
