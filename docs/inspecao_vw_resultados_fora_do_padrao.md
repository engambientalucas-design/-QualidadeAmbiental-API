# Inspecao da View VW_ResultadosForaDoPadrao

Inspecao read-only realizada em 2026-05-28 antes da implementacao do endpoint:

```http
GET /api/v1/resultados/nao-conformidades
```

## Objetivo

Confirmar estrutura, totais e filtros reais da view `VW_ResultadosForaDoPadrao`.

## Colunas confirmadas

| Ordem | Coluna | Tipo | Nulo |
| ----: | ------ | ---- | ---- |
| 1 | `IdResultado` | `int` | nao |
| 2 | `IdAmostra` | `int` | nao |
| 3 | `CodigoAmostra` | `varchar` | nao |
| 4 | `DataColeta` | `date` | nao |
| 5 | `NomeTipoAmostra` | `varchar` | nao |
| 6 | `NomePonto` | `varchar` | nao |
| 7 | `Municipio` | `varchar` | nao |
| 8 | `Estado` | `char` | nao |
| 9 | `NomeParametro` | `varchar` | nao |
| 10 | `Categoria` | `varchar` | sim |
| 11 | `ValorResultado` | `decimal` | nao |
| 12 | `UnidadeMedida` | `varchar` | sim |
| 13 | `ValorMinimo` | `decimal` | sim |
| 14 | `ValorMaximo` | `decimal` | sim |
| 15 | `ClassificacaoResultado` | `varchar` | nao |

## Implicacao para a implementacao

A view especifica possui shape reduzido. Para manter contrato publico compativel com `GET /api/v1/resultados`, o endpoint usa:

```text
VW_ResultadosForaDoPadrao -> define o recorte de nao conformidades
VW_ConformidadeResultados -> fornece os campos consolidados completos por IdResultado
```

Essa estrategia nao recalcula conformidade em Python e nao duplica regra da view.

## Distribuicoes observadas

Total geral:

| Item | Total |
| ---- | ----: |
| Registros | 7 |

Periodo:

| Data minima | Data maxima |
| ----------- | ----------- |
| `2026-04-01` | `2026-04-03` |

Municipios:

| Municipio | Total |
| --------- | ----: |
| `Cuiaba` | 5 |
| `Varzea Grande` | 2 |

Categorias:

| Categoria | Total |
| --------- | ----: |
| `Fisico-quimico` | 3 |
| `Desinfeccao` | 1 |
| `Materia organica` | 1 |
| `Microbiologico` | 1 |
| `Nutrientes` | 1 |

Classificacoes:

| Classificacao | Total |
| ------------- | ----: |
| `Acima do limite maximo` | 5 |
| `Abaixo do limite minimo` | 2 |

## Filtros reais validados

| Filtro | Total |
| ------ | ----: |
| `municipio=Cuiaba` | 5 |
| `categoria=Fisico-quimico` | 3 |
| `classificacao_resultado=Acima do limite maximo` | 5 |
| `classificacao_resultado=Abaixo do limite minimo` | 2 |
| `id_parametro=11` | 1 |
| `id_ponto_coleta=6` | 2 |
| `data_inicio=2026-04-01&data_fim=2026-04-03` | 7 |

## Proximo passo

Implementar `GET /api/v1/resultados/nao-conformidades` consumindo `VW_ResultadosForaDoPadrao` como recorte oficial de nao conformidades.
