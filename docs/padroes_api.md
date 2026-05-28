# Padroes Internos da API

Data de criacao: 2026-05-28.

## Objetivo

Documentar os padroes internos adotados na Fase 3.0 para respostas, erros, paginacao, validacoes, logging e organizacao arquitetural.

## Envelope de Sucesso

Listagens devem manter o contrato ja validado na Fase 2:

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

Regras:

- nao alterar campos publicos sem decisao tecnica;
- manter `success`, `message`, `data` e `pagination` nas respostas paginadas;
- usar `success_response()` ou `paginated_response()` para montar envelopes.

## Envelope de Erro

A partir da Fase 3.0, erros devem seguir o contrato:

```json
{
  "success": false,
  "message": "Erro de validacao na requisicao.",
  "error": {
    "code": "VALIDATION_ERROR",
    "details": "Verifique os parametros enviados na requisicao."
  }
}
```

Codigos iniciais:

| Codigo | Uso |
| ------ | --- |
| `VALIDATION_ERROR` | Erros de validacao de request, como query params invalidos |
| `HTTP_ERROR` | Erros HTTP controlados pela aplicacao |
| `INTERNAL_SERVER_ERROR` | Erros inesperados |

Regras:

- nao expor stacktrace;
- nao expor credenciais;
- nao expor connection string;
- nao expor detalhes sensiveis do SQL Server;
- logar detalhes internos de erros inesperados.

## Paginacao

Padrao publico:

| Campo | Padrao | Limite |
| ----- | ------ | ------ |
| `page` | 1 | minimo 1 |
| `page_size` | 20 | minimo 1, maximo 100 |

Constantes internas:

- `DEFAULT_PAGE = 1`
- `DEFAULT_PAGE_SIZE = 20`
- `MAX_PAGE_SIZE = 100`

Metadados:

```json
{
  "page": 1,
  "page_size": 20,
  "total": 0
}
```

## Validacao de Datas

Endpoints com filtros `data_inicio` e `data_fim` devem usar:

```python
validate_date_range(data_inicio, data_fim)
```

Regra:

- `data_inicio` deve ser menor ou igual a `data_fim`;
- erro controlado retorna HTTP 422 no envelope padrao.

Aplicavel a:

- `GET /api/v1/amostras`;
- `GET /api/v1/resultados`;
- `GET /api/v1/resultados/nao-conformidades`;
- `GET /api/v1/resultados/sem-limite-referencia`.

Nao aplicavel a:

- `GET /api/v1/resultados/resumo-mensal`;
- `GET /api/v1/resultados/parametros-criticos`.

## Arquitetura

Fluxo padrao:

```text
router -> service -> repository -> SQL Server
```

Regras:

- routers recebem parametros HTTP e delegam para services;
- services orquestram fluxo e validacoes leves;
- repositories concentram SQL parametrizado;
- schemas Pydantic definem contratos publicos;
- SQL nao deve ser colocado em routers.

## Views Oficiais

Quando houver view oficial no SQL Server para indicadores analiticos:

- consumir a view diretamente;
- nao recalcular indicadores em Python;
- converter tipos tecnicos para contrato publico quando necessario;
- documentar a origem dos campos.

## Logging

Logging basico foi configurado em `app/core/logging.py`.

Regras:

- registrar erros controlados em nivel informativo;
- registrar erros inesperados com stacktrace apenas no log interno;
- nao retornar stacktrace para consumidores externos;
- nao registrar senha, token, connection string ou credenciais.

## Handlers Globais

Handlers registrados em `app/core/exception_handlers.py`:

- `RequestValidationError`;
- `HTTPException`;
- `Exception`.

Objetivo:

- padronizar erros;
- preservar status codes;
- evitar vazamento de informacoes sensiveis;
- preparar a API para observabilidade futura.
