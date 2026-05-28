# Divida Tecnica

Data de abertura: 2026-05-28.

## Objetivo

Registrar oportunidades de melhoria identificadas no fechamento da Fase 2, sem implementar refatoracoes nesta etapa.

## Duplicacoes Identificadas

| Item | Observacao | Recomendacao |
| ---- | ---------- | ------------ |
| `PaginationResponse` | Repetido em schemas de pontos de coleta, parametros, amostras e resultados. | Centralizar em schema comum na Fase 3. |
| Validacao de intervalo de datas | Repetida em services de amostras e resultados. | Criar helper reutilizavel para validacao `data_inicio <= data_fim`. |
| Montagem de filtros SQL | Padrao repetido nos repositories. | Avaliar builder interno simples, mantendo SQL claro e parametrizado. |
| Envelope de resposta | Padrao aplicado via `success_response`, mas schemas repetem estrutura. | Avaliar schemas genericos ou base classes com cautela. |

## Arquitetura e Codigo

- `app/repositories/resultados_repository.py` concentra varios endpoints analiticos e tende a crescer.
- Services ainda retornam `HTTPException` diretamente para validacoes de aplicacao.
- `app/utils/pagination.py` possui `PaginationParams` com nomes `pagina` e `tamanho_pagina`, diferentes do contrato publico `page` e `page_size`.
- Models SQLAlchemy existem, mas a implementacao atual usa queries SQL textuais por aderencia ao banco real.

## OpenAPI

- Melhorar exemplos de response para cada endpoint.
- Documentar responses de erro HTTP 422 e possiveis erros de banco de forma padronizada.
- Avaliar tags especificas para analiticos, como `resultados-analiticos`, sem quebrar compatibilidade de docs.
- Corrigir textos com encoding inconsistente em descricoes antigas.

## Testes

- Ampliar testes de services e repositories com stubs mais especificos.
- Adicionar testes para helpers comuns quando forem criados.
- Adicionar testes de contrato OpenAPI cobrindo todos os endpoints em um unico teste parametrizado.
- Avaliar testes de integracao reais opcionais, separados dos testes unitarios, para SQL Server local.

## Observabilidade e Logging

- Criar logging estruturado basico para inicializacao da API e erros inesperados.
- Registrar request id/correlation id em fase futura.
- Evitar logs com credenciais ou connection string.
- Criar politica de nivel de log por ambiente.

## Padronizacao de Erros

- Criar handlers globais para `HTTPException`, `RequestValidationError` e erros inesperados.
- Definir envelope padrao para erros.
- Garantir que erros de banco sejam tratados sem expor detalhes sensiveis.

## Documentacao

- Revisar encoding de README e alguns textos antigos.
- Consolidar indice de documentos tecnicos.
- Separar contratos planejados de contratos implementados em uma futura reorganizacao documental.

## Prioridade Recomendada

1. Padronizacao de erros.
2. Centralizacao de paginacao.
3. Logging estruturado basico.
4. Testes OpenAPI parametrizados.
5. Refatoracao gradual do repository de resultados.
