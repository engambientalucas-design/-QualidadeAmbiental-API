# Decisoes Tecnicas

Este documento registra decisoes de arquitetura e tecnologia do projeto `QualidadeAmbiental_API_FastAPI`.

## Python 3.12

O projeto usa Python 3.12 por ser uma versao estavel, madura e amplamente suportada pelo ecossistema atual de backend Python.

## Evitar Python 3.14 nesta fase

Python 3.14 ainda nao e a escolha mais conservadora para este projeto. Como a API depende de bibliotecas como FastAPI, SQLAlchemy, pyodbc e drivers ODBC, a prioridade e compatibilidade e estabilidade, nao adotar a versao mais nova possivel.

## FastAPI

FastAPI foi escolhido por oferecer:

- alta produtividade;
- documentacao automatica em `/docs` e `/redoc`;
- boa integracao com Pydantic;
- tipagem clara;
- bom desempenho para APIs REST.

## SQLAlchemy

SQLAlchemy sera usado como camada de acesso ao banco e base para futura modelagem ORM. Ele permite organizar conexao, sessoes e consultas com mais controle do que SQL espalhado diretamente nas rotas.

## pyodbc

pyodbc e usado como driver de comunicacao com SQL Server via ODBC. A combinacao `SQLAlchemy + pyodbc` e uma abordagem comum para aplicacoes Python que acessam SQL Server.

## Arquitetura em camadas

A estrutura separa responsabilidades:

- `routers`: entrada HTTP;
- `schemas`: contratos de entrada e saida;
- `services`: regras de negocio e orquestracao;
- `repositories`: acesso a dados;
- `models`: representacao das entidades do banco;
- `core`: configuracao e infraestrutura;
- `utils`: funcoes auxiliares.

Essa separacao evita que regras de banco, HTTP e negocio fiquem misturadas.

## API read-only inicialmente

A primeira versao da API sera somente leitura. Isso reduz risco operacional, protege o banco e permite validar consultas, filtros e contratos antes de qualquer operacao de escrita.

## Prefixo QA_API_

As variaveis de ambiente usam o prefixo `QA_API_` para evitar conflito com variaveis globais do sistema ou de outros projetos.

Exemplos:

```text
QA_API_DB_SERVER
QA_API_DB_NAME
QA_API_DEBUG
```

## Separacao routers/repositories/services

A API nao deve consultar banco diretamente dentro dos routers, exceto em endpoints tecnicos muito simples. A regra geral sera:

```text
router -> service -> repository -> banco
```

## Validar banco real antes do ORM

Antes de criar models definitivos, o schema real do SQL Server deve ser inspecionado. Isso evita modelagem baseada em suposicoes e reduz retrabalho.

Devem ser confirmados:

- tabelas reais;
- colunas;
- chaves primarias;
- chaves estrangeiras;
- tipos de dados;
- indices;
- views existentes;
- volume esperado de dados.
