# Inspecao da View VW_ResultadosSemLimiteReferencia

Inspecao read-only realizada em 2026-05-28 antes da implementacao do endpoint:

```http
GET /api/v1/resultados/sem-limite-referencia
```

## Objetivo

Confirmar estrutura, totais e filtros reais da view `VW_ResultadosSemLimiteReferencia`.

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
| 13 | `ClassificacaoResultado` | `varchar` | nao |

## Implicacao para a implementacao

A view especifica possui shape reduzido. Para manter contrato publico compativel com `GET /api/v1/resultados`, o endpoint usa:

```text
VW_ResultadosSemLimiteReferencia -> define o recorte de resultados sem limite
VW_ConformidadeResultados -> fornece os campos consolidados completos por IdResultado
```

Essa estrategia nao recalcula conformidade em Python e nao duplica regra da view.

## Distribuicoes observadas

Total geral:

| Item | Total |
| ---- | ----: |
| Registros | 15 |

Periodo:

| Data minima | Data maxima |
| ----------- | ----------- |
| `2026-04-01` | `2026-04-03` |

Municipios:

| Municipio | Total |
| --------- | ----: |
| `Cuiaba` | 9 |
| `Varzea Grande` | 6 |

Categorias:

| Categoria | Total |
| --------- | ----: |
| `Fisico-quimico` | 5 |
| `Desinfeccao` | 4 |
| `Materia organica` | 2 |
| `Microbiologico` | 2 |
| `Nutrientes` | 2 |

Classificacao:

| Classificacao | Total |
| ------------- | ----: |
| `Sem limite de referencia` | 15 |

## Filtros reais validados

| Filtro | Total |
| ------ | ----: |
| `municipio=Cuiaba` | 9 |
| `categoria=Fisico-quimico` | 5 |
| `id_parametro=4` | 2 |
| `id_ponto_coleta=6` | 2 |
| `codigo_amostra=QA-2026-006` | 2 |
| `id_amostra=6` | 2 |
| `data_inicio=2026-04-01&data_fim=2026-04-03` | 15 |

## Comportamento confirmado no contrato completo

Ao cruzar com `VW_ConformidadeResultados`, os registros retornam:

- `possui_limite_referencia=false`;
- `indicador_nao_conforme=null`;
- `classificacao_resultado=Sem limite de referencia`.

## Proximo passo

Implementar `GET /api/v1/resultados/sem-limite-referencia` consumindo `VW_ResultadosSemLimiteReferencia` como recorte oficial de resultados sem limite.
