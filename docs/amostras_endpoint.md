# Endpoint de Amostras

## Objetivo

Documentar o endpoint read-only da Fase 2.3:

```http
GET /api/v1/amostras
```

O endpoint lista amostras com dados consolidados de ponto de coleta, tipo de amostra, status e responsavel.

## Fluxo arquitetural

```text
Cliente
   ↓
Router: app/routers/amostras.py
   ↓
Service: app/services/amostras_service.py
   ↓
Repository: app/repositories/amostras_repository.py
   ↓
SQL Server: Tbl_Amostras + tabelas de dominio
   ↓
Schema: app/schemas/amostras.py
   ↓
Resposta JSON padronizada
```

## Fonte de dados

Tabela principal:

```text
Tbl_Amostras
```

Joins:

| Origem | Destino | Condicao |
| ------ | ------- | -------- |
| `Tbl_Amostras` | `Tbl_PontosColeta` | `IdPontoColeta` |
| `Tbl_Amostras` | `Tbl_TiposAmostra` | `IdTipoAmostra` |
| `Tbl_Amostras` | `Tbl_StatusAmostra` | `IdStatus` |
| `Tbl_Amostras` | `Tbl_Responsaveis` | `IdResponsavel` |

## Campos

| Banco | API |
| ----- | --- |
| `Tbl_Amostras.IdAmostra` | `id_amostra` |
| `Tbl_Amostras.CodigoAmostra` | `codigo_amostra` |
| `Tbl_Amostras.DataColeta` | `data_coleta` |
| `Tbl_Amostras.HoraColeta` | `hora_coleta` |
| `Tbl_Amostras.IdPontoColeta` | `id_ponto_coleta` |
| `Tbl_PontosColeta.NomePonto` | `nome_ponto` |
| `Tbl_PontosColeta.Municipio` | `municipio` |
| `Tbl_PontosColeta.Estado` | `estado` |
| `Tbl_Amostras.IdTipoAmostra` | `id_tipo_amostra` |
| `Tbl_TiposAmostra.NomeTipoAmostra` | `nome_tipo_amostra` |
| `Tbl_Amostras.IdStatus` | `id_status` |
| `Tbl_StatusAmostra.NomeStatus` | `nome_status` |
| `Tbl_Amostras.IdResponsavel` | `id_responsavel` |
| `Tbl_Responsaveis.NomeResponsavel` | `nome_responsavel` |
| `Tbl_Amostras.Observacao` | `observacao` |

## Filtros

| Parametro | Tipo | Obrigatorio | Descricao |
| --------- | ---- | ----------- | --------- |
| `data_inicio` | `date` | Nao | Filtra coletas a partir desta data. |
| `data_fim` | `date` | Nao | Filtra coletas ate esta data. |
| `id_ponto_coleta` | `integer` | Nao | Filtra por ponto de coleta. |
| `municipio` | `string` | Nao | Filtra por municipio do ponto. |
| `id_tipo_amostra` | `integer` | Nao | Filtra por tipo de amostra. |
| `id_status` | `integer` | Nao | Filtra por status da amostra. |

`data_inicio` deve ser menor ou igual a `data_fim`. Caso contrario, a API retorna HTTP 422.

## Paginacao

| Parametro | Padrao | Limite |
| --------- | ------ | ------ |
| `page` | `1` | minimo `1` |
| `page_size` | `20` | minimo `1`, maximo `100` |

A paginacao usa `COUNT(1)` com os mesmos joins/filtros e `OFFSET/FETCH` para limitar o retorno.

## Ordenacao

O retorno usa ordenacao padrao:

```sql
ORDER BY DataColeta DESC, IdAmostra DESC
```

Essa ordenacao prioriza as coletas mais recentes e garante estabilidade quando houver mais de uma amostra na mesma data.

## Exemplo de request

```http
GET /api/v1/amostras?municipio=Cuiaba&data_inicio=2026-04-01&data_fim=2026-04-30&page=1&page_size=20
```

## Exemplo de response

```json
{
  "success": true,
  "message": "Consulta realizada com sucesso.",
  "data": [
    {
      "id_amostra": 6,
      "codigo_amostra": "QA-2026-006",
      "data_coleta": "2026-04-03",
      "hora_coleta": "11:15:00",
      "id_ponto_coleta": 6,
      "nome_ponto": "Reservatorio Bairro Leste",
      "municipio": "Cuiaba",
      "estado": "MT",
      "id_tipo_amostra": 2,
      "nome_tipo_amostra": "Agua Tratada",
      "id_status": 3,
      "nome_status": "Concluida",
      "id_responsavel": 4,
      "nome_responsavel": "Joao Pereira",
      "observacao": "Segunda amostra didatica de agua tratada."
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 6
  }
}
```

## Indices e performance

Indices relevantes:

- `PK_Tbl_Amostras` em `IdAmostra`.
- `UQ_Tbl_Amostras_CodigoAmostra` em `CodigoAmostra`.
- `IX_Tbl_Amostras_DataColeta_Tipo_Ponto` em `DataColeta`, `IdTipoAmostra`, `IdPontoColeta`, com includes `CodigoAmostra`, `IdResponsavel`, `IdStatus`.

Observacoes:

- Filtros por data, tipo de amostra e ponto tendem a aproveitar melhor o indice documentado.
- Filtro por municipio depende do join com `Tbl_PontosColeta`.
- A consulta e read-only e nao altera tabelas, indices ou constraints.

## Status de validacao

- Contrato automatizado validado com `pytest`.
- OpenAPI validado com endpoint, filtros e respostas esperadas.
- Validacao real com SQL Server concluida em 2026-05-28.

Resultados da validacao real:

| Item | Resultado |
| ---- | --------- |
| Banco | `QualidadeAmbiental` |
| Tabela principal | `Tbl_Amostras` |
| Total real | 6 registros |
| `GET /api/v1/amostras` | HTTP 200 |
| `page=1&page_size=2` | 2 itens em `data`, `total=6` |
| `municipio=Cuiaba` | 4 registros |
| `id_tipo_amostra=1` | 1 registro |
| `id_status=3` | 6 registros |
| `data_inicio=2026-04-01&data_fim=2026-04-30` | 6 registros |
| Filtro sem resultado | `data=[]`, `total=0` |
| `page_size=101` | HTTP 422 |
| `data_inicio > data_fim` | HTTP 422 |

Observacao: `id_status=1` existe no dominio como `Coletada`, mas nao possui amostras no conjunto atual. O status com registros e `id_status=3` (`Concluida`).

## Melhorias futuras

- Adicionar endpoint individual `GET /api/v1/amostras/{id}`.
- Avaliar filtro por `codigo_amostra`.
- Avaliar ordenacao controlada por parametros seguros.
- Criar testes de integracao separados para SQL Server real.
