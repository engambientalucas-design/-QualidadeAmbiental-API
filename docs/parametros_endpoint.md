# Endpoint de Parametros

## Objetivo

Documentar o endpoint read-only da Fase 2.2:

```http
GET /api/v1/parametros
```

O endpoint lista parametros ambientais cadastrados no banco `QualidadeAmbiental`, com filtros simples e paginacao segura.

## Fluxo arquitetural

```text
Cliente
   ↓
Router: app/routers/parametros.py
   ↓
Service: app/services/parametros_service.py
   ↓
Repository: app/repositories/parametros_repository.py
   ↓
SQL Server: Tbl_Parametros
   ↓
Schema: app/schemas/parametros.py
   ↓
Resposta JSON padronizada
```

## Fonte de dados

Tabela principal:

```text
Tbl_Parametros
```

Campos mapeados para a API:

| Banco | API |
| ----- | --- |
| `IdParametro` | `id_parametro` |
| `NomeParametro` | `nome_parametro` |
| `UnidadeMedida` | `unidade_medida` |
| `Categoria` | `categoria` |
| `Descricao` | `descricao` |
| `Ativo` | `ativo` |

## Filtros

| Parametro | Tipo | Obrigatorio | Descricao |
| --------- | ---- | ----------- | --------- |
| `categoria` | `string` | Nao | Filtra por categoria do parametro. |
| `ativo` | `boolean` | Nao | Filtra parametros ativos ou inativos. |

Os filtros sao aplicados por igualdade simples e parametrizados no repository.

## Paginacao

| Parametro | Padrao | Limite |
| --------- | ------ | ------ |
| `page` | `1` | minimo `1` |
| `page_size` | `20` | minimo `1`, maximo `100` |

A paginacao usa `COUNT(1)` para totalizacao e `OFFSET/FETCH` para limitar o retorno.

## Exemplo de request

```http
GET /api/v1/parametros?categoria=Fisico-quimico&ativo=true&page=1&page_size=20
```

## Exemplo de response

```json
{
  "success": true,
  "message": "Consulta realizada com sucesso.",
  "data": [
    {
      "id_parametro": 1,
      "nome_parametro": "pH",
      "unidade_medida": null,
      "categoria": "Fisico-quimico",
      "descricao": "Potencial hidrogenionico da amostra.",
      "ativo": true
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 12
  }
}
```

## Indices e constraints relevantes

- `PK_Tbl_Parametros` em `IdParametro`.
- `UQ_Tbl_Parametros_NomeParametro` em `NomeParametro`.
- Default `DF_Tbl_Parametros_Ativo` = `1`.

## Status de validacao

- Contrato automatizado validado com `pytest`.
- OpenAPI validado com endpoint, filtros e respostas esperadas.
- Validacao real com SQL Server concluida em 2026-05-28.

Resultados da validacao real:

| Item | Resultado |
| ---- | --------- |
| Banco | `QualidadeAmbiental` |
| Tabela | `Tbl_Parametros` |
| Total real | 12 registros |
| `GET /api/v1/parametros` | HTTP 200 |
| `page=1&page_size=2` | 2 itens em `data`, `total=12` |
| `ativo=true` | 12 registros |
| `ativo=false` | 0 registros |
| `categoria=Fisico-quimico` | 5 registros |
| Filtro sem resultado | `data=[]`, `total=0` |
| `page_size=101` | HTTP 422 |

Categorias observadas:

| Categoria | Total |
| --------- | ----: |
| `Desinfeccao` | 1 |
| `Fisico-quimico` | 5 |
| `Materia organica` | 2 |
| `Microbiologico` | 1 |
| `Nutrientes` | 2 |
| `Solidos` | 1 |

## Melhorias futuras

- Adicionar endpoint individual `GET /api/v1/parametros/{id}`.
- Avaliar busca parcial por nome do parametro.
- Avaliar ordenacao controlada por parametros seguros.
- Criar testes de integracao separados para SQL Server real.
