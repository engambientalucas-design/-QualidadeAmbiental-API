# Observabilidade Leve

Data de criacao: 2026-05-29.

## Objetivo

Registrar o padrao de observabilidade leve adotado na Fase 3.1 para rastrear requisicoes HTTP sem expor dados sensiveis.

## Request ID

A API usa o header `X-Request-ID` para correlacionar requisicoes e logs.

Comportamento:

- se o cliente enviar `X-Request-ID`, a API preserva o valor;
- se o cliente nao enviar, a API gera um UUID;
- toda resposta retorna o header `X-Request-ID`;
- o valor e registrado nos logs da aplicacao.

Exemplo:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health -Headers @{"X-Request-ID"="qa-api-local-001"}
```

## Logging de Requisicao

O middleware `RequestLoggingMiddleware` registra:

- metodo HTTP;
- path sem query string;
- status code;
- tempo de resposta em milissegundos;
- `request_id`.

Exemplo de formato:

```text
request_completed request_id=... method=GET path=/health status_code=200 duration_ms=1.23
```

## Cuidados de Seguranca

Os logs nao devem registrar:

- body da requisicao;
- headers sensiveis;
- senha;
- token;
- connection string;
- valores completos de `.env`;
- query strings com possiveis credenciais.

## Testes

A Fase 3.1 adicionou testes para:

- resposta com `X-Request-ID` gerado;
- preservacao de `X-Request-ID` enviado pelo cliente;
- header `X-Request-ID` em respostas de erro 422;
- contrato de sucesso preservado.

## Escopo Futuro

Melhorias futuras recomendadas:

- correlacionar logs de erro com `request_id`;
- adicionar nivel de log configuravel por ambiente;
- avaliar metricas de latencia por rota;
- avaliar ferramenta externa de observabilidade apenas em fase posterior.
