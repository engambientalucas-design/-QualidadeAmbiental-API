# Proposta Inicial do Modelo de Banco

Banco fonte: `QualidadeAmbiental`.

Esta documentacao registra a visao inicial de dominio. O mapeamento final dos
models SQLAlchemy deve ser feito somente apos inspecao do schema real no SQL
Server, incluindo nomes de tabelas, colunas, chaves primarias, chaves
estrangeiras, tipos, indices e views existentes.

## Entidades no escopo inicial

### Pontos de coleta

Representam locais onde amostras ambientais sao coletadas.

Campos esperados para validacao:

- Identificador do ponto.
- Nome ou codigo do ponto.
- Municipio.
- Coordenadas, quando existirem.
- Status ou situacao cadastral.

### Parametros

Representam variaveis ambientais analisadas.

Campos esperados para validacao:

- Identificador do parametro.
- Nome do parametro.
- Unidade de medida.
- Limite de referencia, quando aplicavel.
- Grupo ou classificacao do parametro.

### Amostras

Representam eventos de coleta.

Campos esperados para validacao:

- Identificador da amostra.
- Ponto de coleta relacionado.
- Data da coleta.
- Tipo de amostra.
- Responsavel ou origem, quando disponivel.

### Resultados

Representam valores medidos para parametros em amostras.

Campos esperados para validacao:

- Identificador do resultado.
- Amostra relacionada.
- Parametro relacionado.
- Valor medido.
- Unidade.
- Limite aplicavel.
- Situacao de conformidade.

## Premissas de DBA

- A API deve respeitar o modelo existente, sem criar tabelas nesta etapa.
- Consultas iniciais devem ser read-only.
- Relacionamentos devem ser confirmados no banco antes de implementar joins.
- Filtros por data, ponto, parametro, municipio e situacao devem considerar indices existentes.
- Nomes em portugues na API podem ser diferentes dos nomes fisicos do banco, desde que o mapeamento fique documentado.

## Validacoes pendentes

- Listar schemas e tabelas reais.
- Identificar chaves primarias e estrangeiras.
- Confirmar se existem views consolidadas para resultados e nao conformidades.
- Avaliar volume de dados para estrategia de paginacao.
- Avaliar indices para filtros mais frequentes.
- Confirmar politica de acesso ao SQL Server e usuario read-only.
