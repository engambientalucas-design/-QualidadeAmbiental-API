# Inspecao da View VW_ConformidadeResultados

Inspecao read-only realizada em 2026-05-28 antes da implementacao do endpoint:

```http
GET /api/v1/resultados
```

## Objetivo

Confirmar nomes, tipos, distribuicoes e filtros reais da view `VW_ConformidadeResultados`, evitando implementar o contrato publico com suposicoes.

## Colunas confirmadas

| Ordem | Coluna | Tipo | Nulo |
| ----: | ------ | ---- | ---- |
| 1 | `IdResultado` | `int` | nao |
| 2 | `IdAmostra` | `int` | nao |
| 3 | `CodigoAmostra` | `varchar` | nao |
| 4 | `DataColeta` | `date` | nao |
| 5 | `HoraColeta` | `time` | sim |
| 6 | `IdTipoAmostra` | `int` | nao |
| 7 | `NomeTipoAmostra` | `varchar` | nao |
| 8 | `IdPontoColeta` | `int` | nao |
| 9 | `NomePonto` | `varchar` | nao |
| 10 | `TipoPonto` | `varchar` | nao |
| 11 | `Municipio` | `varchar` | nao |
| 12 | `Estado` | `char` | nao |
| 13 | `IdResponsavel` | `int` | nao |
| 14 | `NomeResponsavel` | `varchar` | nao |
| 15 | `IdStatus` | `int` | nao |
| 16 | `NomeStatus` | `varchar` | nao |
| 17 | `IdParametro` | `int` | nao |
| 18 | `NomeParametro` | `varchar` | nao |
| 19 | `Categoria` | `varchar` | sim |
| 20 | `ValorResultado` | `decimal` | nao |
| 21 | `UnidadeMedida` | `varchar` | sim |
| 22 | `DataAnalise` | `date` | nao |
| 23 | `MetodoAnalise` | `varchar` | sim |
| 24 | `IdLimite` | `int` | sim |
| 25 | `ValorMinimo` | `decimal` | sim |
| 26 | `ValorMaximo` | `decimal` | sim |
| 27 | `ReferenciaNormativa` | `varchar` | sim |
| 28 | `ClassificacaoResultado` | `varchar` | nao |
| 29 | `PossuiLimiteReferencia` | `int` | nao |
| 30 | `IndicadorNaoConforme` | `int` | sim |

## Implicacoes para o contrato publico

- `ValorResultado`, `ValorMinimo` e `ValorMaximo` devem ser expostos como numeros JSON.
- `PossuiLimiteReferencia` deve ser exposto como booleano.
- `IndicadorNaoConforme` deve ser exposto como `boolean | null`, pois a view retorna `NULL` para resultados sem limite de referencia.
- O endpoint deve usar a view como fonte da classificacao, sem recalcular conformidade em Python.

## Distribuicoes observadas

Total geral:

| Item | Total |
| ---- | ----: |
| Registros | 72 |

Periodo:

| Data minima | Data maxima |
| ----------- | ----------- |
| `2026-04-01` | `2026-04-03` |

Municipios:

| Municipio | Total |
| --------- | ----: |
| `Cuiaba` | 48 |
| `Varzea Grande` | 24 |

Categorias:

| Categoria | Total |
| --------- | ----: |
| `Fisico-quimico` | 30 |
| `Materia organica` | 12 |
| `Nutrientes` | 12 |
| `Desinfeccao` | 6 |
| `Microbiologico` | 6 |
| `Solidos` | 6 |

Classificacoes:

| Classificacao | Total |
| ------------- | ----: |
| `Conforme` | 50 |
| `Sem limite de referencia` | 15 |
| `Acima do limite maximo` | 5 |
| `Abaixo do limite minimo` | 2 |

Limite de referencia:

| Possui limite | Total |
| ------------- | ----: |
| `false` | 15 |
| `true` | 57 |

Nao conformidade:

| Indicador | Total |
| --------- | ----: |
| `null` | 15 |
| `false` | 50 |
| `true` | 7 |

## Filtros reais validados

| Filtro | Total |
| ------ | ----: |
| `municipio=Cuiaba` | 48 |
| `id_parametro=11` | 6 |
| `categoria=Fisico-quimico` | 30 |
| `classificacao_resultado=Conforme` | 50 |
| `indicador_nao_conforme=true` | 7 |
| `indicador_nao_conforme=false` | 50 |
| `possui_limite_referencia=false` | 15 |
| `possui_limite_referencia=true` | 57 |
| `data_inicio=2026-04-01&data_fim=2026-04-03` | 72 |
| `codigo_amostra=QA-2026-006` | 12 |
| `id_amostra=6` | 12 |
| `id_ponto_coleta=6` | 12 |

## Proximo passo

Implementar `GET /api/v1/resultados` consumindo `VW_ConformidadeResultados` em modo read-only, com filtros parametrizados, paginacao e sem recalculo de conformidade em Python.
