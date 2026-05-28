# Checklist de Entrada da Fase 3

Data de criacao: 2026-05-28.

## Objetivo

Definir criterios e trilha de trabalho para iniciar a Fase 3 com seguranca, sem perder a estabilidade conquistada na Fase 2.

## Go/No-Go

| Criterio | Status |
| -------- | ------ |
| Fase 2 encerrada e documentada | Go |
| Testes automatizados aprovados | Go |
| SQL Server real validado | Go |
| Git limpo | Go |
| Nenhum endpoint novo pendente da camada analitica inicial | Go |
| Divida tecnica registrada | Go |

## Escopo Recomendado da Fase 3

- Padronizacao profissional de erros.
- Contrato padrao de resposta de erro.
- Centralizacao de paginacao.
- Validacoes reutilizaveis.
- Logging estruturado basico.
- Observabilidade leve.
- Testes de erro e OpenAPI mais abrangentes.
- Revisao incremental de duplicacoes.

## Fora do Escopo Inicial da Fase 3

- CRUD.
- Autenticacao/JWT.
- Docker.
- Deploy.
- Migrations.
- Alteracoes no SQL Server.
- Reescrita completa da arquitetura.

## Checklist Tecnico

- [ ] Criar handlers globais de erro.
- [ ] Definir schema padrao de erro.
- [ ] Padronizar respostas de validacao.
- [ ] Centralizar schema de paginacao.
- [ ] Alinhar `PaginationParams` com `page` e `page_size`.
- [ ] Criar helper de validacao de intervalo de datas.
- [ ] Criar testes parametrizados de OpenAPI.
- [ ] Criar testes para erros HTTP 422.
- [ ] Adicionar logging estruturado basico.
- [ ] Garantir que logs nao exponham credenciais.
- [ ] Documentar politica de erro e logging.

## Cuidado com Contratos Publicos

- Nao renomear campos publicos sem justificativa e versionamento.
- Nao alterar filtros existentes sem registrar impacto.
- Nao alterar formato de sucesso ja validado.
- Introduzir envelope de erro de forma consistente e documentada.

## Resultado Esperado da Fase 3

Ao final da Fase 3, a API deve manter os contratos funcionais da Fase 2 e adicionar maior previsibilidade operacional por meio de erros padronizados, logs basicos e reducao controlada de duplicacoes.
