# Divida Tecnica

Data de abertura: 2026-05-28.

## Objetivo

Registrar oportunidades de melhoria identificadas no fechamento da Fase 2, sem implementar refatoracoes nesta etapa.

## Duplicacoes Identificadas

| Item | Observacao | Recomendacao |
| ---- | ---------- | ------------ |
| `PaginationResponse` | Repetido em schemas de pontos de coleta, parametros, amostras e resultados. | Centralizar em schema comum na Fase 3. |
| Validacao de intervalo de datas | Resolvida parcialmente na Fase 3.0 com `validate_date_range`. | Manter helper e ampliar apenas se surgirem novas regras. |
| Montagem de filtros SQL | Padrao repetido nos repositories. | Avaliar builder interno simples, mantendo SQL claro e parametrizado. |
| Envelope de resposta | Padrao aplicado via `success_response`, mas schemas repetem estrutura. | Avaliar schemas genericos ou base classes com cautela. |

## Arquitetura e Codigo

- `app/repositories/resultados_repository.py` concentra varios endpoints analiticos e tende a crescer.
- Services usam helper reutilizavel para validacao de intervalo de datas, mas ainda podem evoluir para excecoes de dominio no futuro.
- `app/utils/pagination.py` foi alinhado ao contrato publico `page` e `page_size` na Fase 3.0.
- Models SQLAlchemy existem, mas a implementacao atual usa queries SQL textuais por aderencia ao banco real.

## OpenAPI

- Melhorar exemplos de response para cada endpoint.
- Documentar responses de erro HTTP 422 e possiveis erros de banco no OpenAPI de forma mais completa.
- Avaliar tags especificas para analiticos, como `resultados-analiticos`, sem quebrar compatibilidade de docs.
- Corrigir textos com encoding inconsistente em descricoes antigas.

## Testes

- Ampliar testes de services e repositories com stubs mais especificos.
- Adicionar testes para helpers comuns quando forem criados.
- Adicionar testes de contrato OpenAPI cobrindo todos os endpoints em um unico teste parametrizado.
- Avaliar testes de integracao reais opcionais, separados dos testes unitarios, para SQL Server local.

## Observabilidade e Logging

- Logging basico criado na Fase 3.0; evoluir para request id/correlation id futuramente.
- Registrar request id/correlation id em fase futura.
- Evitar logs com credenciais ou connection string.
- Criar politica de nivel de log por ambiente.

## Padronizacao de Erros

- Handlers globais para `HTTPException`, `RequestValidationError` e erros inesperados criados na Fase 3.0.
- Envelope padrao de erro definido na Fase 3.0.
- Garantir que erros de banco sejam tratados sem expor detalhes sensiveis.

## Documentacao

- Revisar encoding de README e alguns textos antigos.
- Consolidar indice de documentos tecnicos.
- Separar contratos planejados de contratos implementados em uma futura reorganizacao documental.

## Prioridade Recomendada

1. Centralizar `PaginationResponse` em schema comum.
2. Documentar responses de erro no OpenAPI.
3. Testes OpenAPI parametrizados.
4. Evoluir logging com correlation id.
5. Refatoracao gradual do repository de resultados.
