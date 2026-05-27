# Modelo Real do Banco SQL Server

Banco fonte: `QualidadeAmbiental`.

Inspecao realizada em 2026-05-27, somente leitura, sem alteracao de schema, dados, tabelas, views, indices ou triggers.

## Resumo executivo

O banco possui um modelo relacional simples e bem separado para qualidade ambiental:

- cadastro de pontos de coleta;
- cadastro de parametros analisados;
- cadastro de tipos e status de amostra;
- cadastro de responsaveis;
- registro de amostras;
- registro de resultados analiticos;
- limites de referencia por parametro e tipo de amostra;
- auditoria de alteracoes;
- views consolidadas para conformidade, nao conformidade, eficiencia e ranking.

A API deve iniciar a Fase 2 usando consultas read-only e respeitando o modelo existente.

## Objetos encontrados

### Tabelas base

| Tabela | Papel | Linhas atuais |
|---|---|---:|
| `Tbl_PontosColeta` | Cadastro dos locais de coleta | 6 |
| `Tbl_Parametros` | Cadastro dos parametros ambientais | 12 |
| `Tbl_TiposAmostra` | Dominio de tipos de amostra | 5 |
| `Tbl_StatusAmostra` | Dominio de status da amostra | 5 |
| `Tbl_Responsaveis` | Cadastro dos responsaveis | 4 |
| `Tbl_Amostras` | Eventos de coleta | 6 |
| `Tbl_ResultadosAnalise` | Valores medidos por amostra e parametro | 72 |
| `Tbl_LimitesReferencia` | Limites por parametro e tipo de amostra | 47 |
| `Tbl_AuditoriaAlteracoes` | Auditoria de alteracoes | 8 |

### Views

| View | Uso sugerido na API |
|---|---|
| `VW_ConformidadeResultados` | Base consolidada para resultados com classificacao de conformidade. |
| `VW_ResultadosForaDoPadrao` | Endpoint de nao conformidades. |
| `VW_ResultadosSemLimiteReferencia` | Endpoint ou filtro para resultados sem limite cadastrado. |
| `VW_ConformidadeMensal` | Resumo mensal de conformidade. |
| `VW_RankingParametrosCriticos` | Ranking de parametros com maior nao conformidade. |
| `VW_EficienciaRemocaoETE` | Indicador de eficiencia de remocao em ETE. |

## Relacionamentos confirmados

| Origem | Coluna | Destino | Coluna destino |
|---|---|---|---|
| `Tbl_Amostras` | `IdPontoColeta` | `Tbl_PontosColeta` | `IdPontoColeta` |
| `Tbl_Amostras` | `IdResponsavel` | `Tbl_Responsaveis` | `IdResponsavel` |
| `Tbl_Amostras` | `IdStatus` | `Tbl_StatusAmostra` | `IdStatus` |
| `Tbl_Amostras` | `IdTipoAmostra` | `Tbl_TiposAmostra` | `IdTipoAmostra` |
| `Tbl_ResultadosAnalise` | `IdAmostra` | `Tbl_Amostras` | `IdAmostra` |
| `Tbl_ResultadosAnalise` | `IdParametro` | `Tbl_Parametros` | `IdParametro` |
| `Tbl_LimitesReferencia` | `IdParametro` | `Tbl_Parametros` | `IdParametro` |
| `Tbl_LimitesReferencia` | `IdTipoAmostra` | `Tbl_TiposAmostra` | `IdTipoAmostra` |

Todas as FKs inspecionadas usam `NO_ACTION` para delete e update.

## Tabelas principais

### Tbl_PontosColeta

Chave primaria: `IdPontoColeta`.

Colunas:

| Coluna | Tipo | Nulo | Observacao |
|---|---|---|---|
| `IdPontoColeta` | `int` | nao | PK. |
| `NomePonto` | `varchar(100)` | nao | Nome do ponto. |
| `TipoPonto` | `varchar(80)` | nao | Tipo operacional do ponto. |
| `Municipio` | `varchar(100)` | nao | Municipio. |
| `Estado` | `char(2)` | nao | UF. |
| `Latitude` | `decimal(9,6)` | sim | Check entre -90 e 90. |
| `Longitude` | `decimal(9,6)` | sim | Check entre -180 e 180. |
| `Observacao` | `varchar(255)` | sim | Texto livre. |

Indices e constraints relevantes:

- `PK_Tbl_PontosColeta` em `IdPontoColeta`.
- `UQ_Tbl_PontosColeta_NomeMunicipioEstado` em `NomePonto`, `Municipio`, `Estado`.
- `CK_Tbl_PontosColeta_Latitude`.
- `CK_Tbl_PontosColeta_Longitude`.

### Tbl_Parametros

Chave primaria: `IdParametro`.

Colunas:

| Coluna | Tipo | Nulo | Observacao |
|---|---|---|---|
| `IdParametro` | `int` | nao | PK. |
| `NomeParametro` | `varchar(120)` | nao | Nome unico. |
| `UnidadeMedida` | `varchar(30)` | sim | Unidade padrao. |
| `Categoria` | `varchar(80)` | sim | Grupo do parametro. |
| `Descricao` | `varchar(255)` | sim | Descricao textual. |
| `Ativo` | `bit` | nao | Default `1`. |

Indices e constraints relevantes:

- `PK_Tbl_Parametros` em `IdParametro`.
- `UQ_Tbl_Parametros_NomeParametro` em `NomeParametro`.
- Default `DF_Tbl_Parametros_Ativo` = `1`.

### Tbl_Amostras

Chave primaria: `IdAmostra`.

Colunas:

| Coluna | Tipo | Nulo | Observacao |
|---|---|---|---|
| `IdAmostra` | `int` | nao | PK. |
| `CodigoAmostra` | `varchar(50)` | nao | Codigo unico. |
| `IdPontoColeta` | `int` | nao | FK para ponto. |
| `IdTipoAmostra` | `int` | nao | FK para tipo. |
| `IdResponsavel` | `int` | nao | FK para responsavel. |
| `IdStatus` | `int` | nao | FK para status. |
| `DataColeta` | `date` | nao | Data da coleta. |
| `HoraColeta` | `time` | sim | Hora da coleta. |
| `Observacao` | `varchar(255)` | sim | Texto livre. |

Indices e constraints relevantes:

- `PK_Tbl_Amostras` em `IdAmostra`.
- `UQ_Tbl_Amostras_CodigoAmostra` em `CodigoAmostra`.
- `IX_Tbl_Amostras_DataColeta_Tipo_Ponto` em `DataColeta`, `IdTipoAmostra`, `IdPontoColeta`, com includes `CodigoAmostra`, `IdResponsavel`, `IdStatus`.

### Tbl_ResultadosAnalise

Chave primaria: `IdResultado`.

Colunas:

| Coluna | Tipo | Nulo | Observacao |
|---|---|---|---|
| `IdResultado` | `int` | nao | PK. |
| `IdAmostra` | `int` | nao | FK para amostra. |
| `IdParametro` | `int` | nao | FK para parametro. |
| `ValorResultado` | `decimal(18,4)` | nao | Valor medido. |
| `UnidadeMedida` | `varchar(30)` | sim | Unidade informada no resultado. |
| `DataAnalise` | `date` | nao | Data da analise. |
| `MetodoAnalise` | `varchar(100)` | sim | Metodo usado. |
| `Observacao` | `varchar(255)` | sim | Texto livre. |

Indices e constraints relevantes:

- `PK_Tbl_ResultadosAnalise` em `IdResultado`.
- `UQ_Tbl_ResultadosAnalise_AmostraParametro` em `IdAmostra`, `IdParametro`.
- `IX_Tbl_ResultadosAnalise_Parametro_Amostra` em `IdParametro`, `IdAmostra`, com includes `ValorResultado`, `UnidadeMedida`, `DataAnalise`, `MetodoAnalise`.

### Tbl_LimitesReferencia

Chave primaria: `IdLimite`.

Colunas:

| Coluna | Tipo | Nulo | Observacao |
|---|---|---|---|
| `IdLimite` | `int` | nao | PK. |
| `IdParametro` | `int` | nao | FK para parametro. |
| `IdTipoAmostra` | `int` | nao | FK para tipo de amostra. |
| `ValorMinimo` | `decimal(18,4)` | sim | Limite minimo. |
| `ValorMaximo` | `decimal(18,4)` | sim | Limite maximo. |
| `UnidadeMedida` | `varchar(30)` | sim | Unidade do limite. |
| `ReferenciaNormativa` | `varchar(150)` | sim | Referencia. |
| `Observacao` | `varchar(255)` | sim | Texto livre. |

Indices e constraints relevantes:

- `PK_Tbl_LimitesReferencia` em `IdLimite`.
- `UQ_Tbl_LimitesReferencia_ParametroTipoAmostra` em `IdParametro`, `IdTipoAmostra`.
- `CK_Tbl_LimitesReferencia_LimiteInformado`: exige minimo ou maximo informado.
- `CK_Tbl_LimitesReferencia_MinimoMenorOuIgualMaximo`.

## Tabelas de dominio

### Tbl_TiposAmostra

Valores atuais:

- Agua Bruta;
- Agua Tratada;
- Esgoto Bruto;
- Esgoto Tratado;
- Corpo Hidrico.

Chaves e constraints:

- PK `IdTipoAmostra`.
- Unique `NomeTipoAmostra`.

### Tbl_StatusAmostra

Valores atuais:

- Coletada;
- Em Analise;
- Concluida;
- Reprovada;
- Pendente.

Chaves e constraints:

- PK `IdStatus`.
- Unique `NomeStatus`.

### Tbl_Responsaveis

Contem responsaveis operacionais com nome, cargo, email e telefone.

Chaves e constraints:

- PK `IdResponsavel`.

## Auditoria

A tabela `Tbl_AuditoriaAlteracoes` registra alteracoes com:

- tabela afetada;
- id do registro afetado;
- operacao;
- data/hora;
- usuario SQL;
- host;
- aplicacao;
- valores anteriores e novos.

Triggers de auditoria encontradas:

| Tabela | Trigger | Timing |
|---|---|---|
| `Tbl_Amostras` | `TRG_Tbl_Amostras_Auditoria` | AFTER |
| `Tbl_LimitesReferencia` | `TRG_Tbl_LimitesReferencia_Auditoria` | AFTER |
| `Tbl_ResultadosAnalise` | `TRG_Tbl_ResultadosAnalise_Auditoria` | AFTER |

Para a API read-only inicial, auditoria deve ser apenas documentada. Nao ha necessidade de expor endpoints de auditoria na primeira entrega.

## Views consolidadas

### VW_ConformidadeResultados

View central para resultados consolidados. Junta resultados, amostras, pontos, responsaveis, status, parametros e limites.

Campos relevantes:

- identificadores de resultado, amostra, ponto, tipo, responsavel, status e parametro;
- codigo e data da amostra;
- ponto, municipio e UF;
- parametro, categoria, valor e unidade;
- limite minimo e maximo;
- `ClassificacaoResultado`;
- `PossuiLimiteReferencia`;
- `IndicadorNaoConforme`.

Classificacoes observadas:

- `Conforme`;
- `Acima do limite maximo`;
- `Abaixo do limite minimo`;
- `Sem limite de referencia`.

Esta deve ser a principal base para endpoints de resultados na Fase 2.

### VW_ResultadosForaDoPadrao

Filtra resultados classificados como acima ou abaixo do limite. Boa candidata para endpoint:

```text
GET /api/v1/resultados/nao-conformidades
```

### VW_ResultadosSemLimiteReferencia

Filtra resultados sem limite de referencia. Pode virar endpoint posterior ou filtro em resultados.

### VW_ConformidadeMensal

Resumo mensal observado para abril de 2026:

- total de resultados: 72;
- resultados com limite: 57;
- resultados sem limite: 15;
- resultados conformes com limite: 50;
- resultados nao conformes com limite: 7;
- percentual de conformidade com limite: 87.72%.

Boa candidata para endpoint de resumo:

```text
GET /api/v1/resultados/resumo-mensal
```

### VW_RankingParametrosCriticos

Ranking de parametros por nao conformidade. Turbidez aparece como parametro com maior total de nao conformidades no conjunto atual.

### VW_EficienciaRemocaoETE

Calcula eficiencia de remocao comparando esgoto bruto e tratado para parametros como DBO, DQO, Solidos Totais, Nitrogenio Amoniacal e Fosforo Total.

## Implicacoes para a API

### Primeiros endpoints recomendados

1. `GET /api/v1/pontos-coleta`
2. `GET /api/v1/parametros`
3. `GET /api/v1/amostras`
4. `GET /api/v1/resultados`
5. `GET /api/v1/resultados/nao-conformidades`
6. `GET /api/v1/resultados/resumo-mensal`
7. `GET /api/v1/resultados/parametros-criticos`

### Estrategia tecnica recomendada

- Usar tabelas base para cadastros simples: pontos, parametros, tipos, status e responsaveis.
- Usar `VW_ConformidadeResultados` para resultados consolidados.
- Usar views especificas para agregacoes e nao conformidades quando o contrato da API coincidir com a view.
- Manter API read-only na Fase 2.
- Nao criar migrations.
- Nao alterar schema do banco.

## Pendencias antes de implementar endpoints

- Definir contratos Pydantic de resposta.
- Decidir nomes publicos dos campos na API: portugues fisico do banco vs nomes padronizados em snake_case.
- Definir padrao de paginacao para listas.
- Definir filtros iniciais por endpoint.
- Decidir se endpoints devem expor IDs internos e nomes juntos.
- Confirmar se `Tbl_AuditoriaAlteracoes` ficara fora do escopo da primeira versao publica.
