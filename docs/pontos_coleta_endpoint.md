# Endpoint de Pontos de Coleta

## Objetivo

Documentar o primeiro endpoint read-only profissional da Fase 2.1:

```http
GET /api/v1/pontos-coleta
```

O endpoint lista pontos de coleta cadastrados no banco `QualidadeAmbiental`, com filtros simples e paginação segura.

## Fluxo arquitetural

```text
Cliente
   ↓
Router: app/routers/pontos_coleta.py
   ↓
Service: app/services/pontos_coleta_service.py
   ↓
Repository: app/repositories/pontos_coleta_repository.py
   ↓
SQL Server: Tbl_PontosColeta
   ↓
Schema: app/schemas/pontos_coleta.py
   ↓
Resposta JSON padronizada
```

## Fonte de dados

Tabela principal:

```text
Tbl_PontosColeta
```

Campos mapeados para a API:

| Banco | API |
| ----- | --- |
| `IdPontoColeta` | `id_ponto_coleta` |
| `NomePonto` | `nome_ponto` |
| `TipoPonto` | `tipo_ponto` |
| `Municipio` | `municipio` |
| `Estado` | `estado` |
| `Latitude` | `latitude` |
| `Longitude` | `longitude` |
| `Observacao` | `observacao` |

## Filtros

| Parâmetro | Tipo | Obrigatório | Descrição |
| --------- | ---- | ----------- | --------- |
| `municipio` | `string` | Não | Filtra por município. |
| `estado` | `string` | Não | Filtra por UF com 2 caracteres. |
| `tipo_ponto` | `string` | Não | Filtra por tipo do ponto de coleta. |

Os filtros são aplicados por igualdade simples e parametrizados no repository.

## Paginação

| Parâmetro | Padrão | Limite |
| --------- | ------ | ------ |
| `page` | `1` | mínimo `1` |
| `page_size` | `20` | mínimo `1`, máximo `100` |

A paginação usa `COUNT(1)` para totalização e `OFFSET/FETCH` para limitar o retorno.

## Exemplo de request

```http
GET /api/v1/pontos-coleta?municipio=Cuiaba&estado=MT&page=1&page_size=20
```

## Exemplo de response

```json
{
  "success": true,
  "message": "Consulta realizada com sucesso.",
  "data": [
    {
      "id_ponto_coleta": 1,
      "nome_ponto": "Rio Cuiaba - Ponto 01",
      "tipo_ponto": "Corpo Hidrico",
      "municipio": "Cuiaba",
      "estado": "MT",
      "latitude": -15.601234,
      "longitude": -56.097891,
      "observacao": "Ponto de monitoramento ambiental."
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 6
  }
}
```

## Índices e constraints relevantes

- `PK_Tbl_PontosColeta` em `IdPontoColeta`.
- `UQ_Tbl_PontosColeta_NomeMunicipioEstado` em `NomePonto`, `Municipio`, `Estado`.
- `CK_Tbl_PontosColeta_Latitude`.
- `CK_Tbl_PontosColeta_Longitude`.

## Melhorias futuras

- Adicionar endpoint individual `GET /api/v1/pontos-coleta/{id}`.
- Avaliar busca parcial por nome do ponto.
- Avaliar ordenação controlada por parâmetros seguros.
- Criar testes de integração separados para SQL Server real.

## Status de validação

- Contrato automatizado validado com `pytest`.
- OpenAPI validado com endpoint, filtros e respostas esperadas.
- Validação real com SQL Server pendente no workspace atual por ausência de `.env` configurado.
