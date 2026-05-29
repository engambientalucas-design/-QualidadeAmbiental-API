# Qualidade de Testes e Cobertura

Data de criacao: 2026-05-29.

## Objetivo

Registrar a medicao objetiva de cobertura automatizada da API a partir da Fase 3.2.

A cobertura nao substitui a validacao real com SQL Server. Ela mede quanto do codigo Python e exercitado pela suite automatizada local e pelo GitHub Actions.

## Ferramenta

A Fase 3.2 adicionou:

- `pytest-cov==6.0.0`;
- configuracao `pytest.ini`;
- cobertura no workflow `.github/workflows/tests.yml`.

## Comandos Locais

Executar suite padrao:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Executar cobertura no terminal:

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=app --cov-report=term-missing
```

Gerar relatorio HTML local:

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=app --cov-report=html
```

O relatorio HTML e gerado em `htmlcov/` e nao deve ser versionado.

## Resultado Atual

Validacao local em 2026-05-29:

| Item | Resultado |
| ---- | --------- |
| Testes | 73 passed |
| Cobertura geral | 65% |
| Relatorio terminal | `--cov-report=term-missing` |
| Relatorio HTML | Gerado em `htmlcov/` |
| SQL Server real no CI | Nao requerido |

## Modulos com Alta Cobertura

| Area | Observacao |
| ---- | ---------- |
| Routers | 100% nos routers principais |
| Schemas | 100% nos schemas de resposta |
| Middleware | 100% no middleware de request logging |
| Main | 100% na criacao da aplicacao |
| Validators | 100% na validacao de intervalo de datas |
| Database | 100% nas funcoes carregadas pelos testes |

## Modulos com Baixa Cobertura

| Modulo | Cobertura | Motivo principal |
| ------ | --------- | ---------------- |
| `app/repositories/resultados_repository.py` | 14% | Concentra SQL parametrizado e consultas sobre views reais |
| `app/repositories/amostras_repository.py` | 22% | Depende de queries SQL e sessao real |
| `app/repositories/pontos_coleta_repository.py` | 27% | Depende de queries SQL e sessao real |
| `app/repositories/parametros_repository.py` | 30% | Depende de queries SQL e sessao real |
| `app/utils/responses.py` | 50% | Helpers parcialmente exercitados pelos services |
| `app/services/resultados_service.py` | 58% | Fluxos cobertos por routers com mocks, nao por service unit direto |

## Riscos Conhecidos

- A cobertura dos repositories e baixa porque os testes de CI nao dependem do SQL Server real.
- Os testes atuais validam contratos HTTP, parametros, erros, OpenAPI e observabilidade, mas nao substituem testes de integracao com banco.
- A cobertura geral de 65% e um marco inicial, nao uma garantia completa de qualidade.
- Os endpoints ja foram validados manualmente contra SQL Server real em fases anteriores, mas essa validacao ainda nao roda automaticamente no CI.

## Decisao Tecnica

Nao foi definido limite minimo de cobertura nesta fase.

Motivo:

- evitar meta artificial antes de separar melhor testes unitarios, contratos e integracao;
- preservar CI independente do SQL Server real;
- usar a primeira medicao como baseline honesto.

## Metas Futuras

Recomendacoes:

- criar testes unitarios especificos para services;
- criar testes de repositories com stubs/fakes de `Session.execute`, quando o custo compensar;
- criar uma suite opcional de integracao local com SQL Server real;
- avaliar meta minima de cobertura apenas depois da Fase 3.3 ou 3.4;
- considerar `coverage.xml` para integracao futura com badges ou ferramentas externas.
