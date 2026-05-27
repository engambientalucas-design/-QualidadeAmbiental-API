# Versionamento e Backup

## Objetivo

Este documento define a estrategia de versionamento, backup e recuperacao do projeto `QualidadeAmbiental_API_FastAPI` antes da evolucao para endpoints reais e modelagem ORM.

A regra principal desta fase e simples: qualquer mudanca estrutural deve ser rastreavel, reversivel e segura para credenciais.

## Estrategia de versionamento

O projeto usa Git como ferramenta principal de controle de versao. O Git deve registrar a evolucao do codigo, documentacao e configuracoes de exemplo.

Devem ser versionados:

- codigo fonte em `app/`;
- documentacao em `docs/`;
- testes em `tests/`;
- `README.md`;
- `requirements.txt`;
- `.env.example`;
- `.gitignore`.

Nao devem ser versionados:

- `.env`;
- `.venv/`;
- caches Python;
- logs;
- snapshots ZIP;
- credenciais reais.

## Politica de commits

Commits devem ser pequenos, claros e ligados a uma mudanca objetiva. Evitar commits grandes misturando documentacao, refatoracao e funcionalidade.

Convencao adotada:

- `feat:` nova funcionalidade;
- `fix:` correcao de bug;
- `refactor:` melhoria interna sem alterar comportamento esperado;
- `docs:` alteracoes de documentacao;
- `test:` criacao ou ajuste de testes;
- `chore:` tarefas de manutencao, configuracao ou governanca.

Exemplos:

```text
feat: adiciona endpoint de pontos de coleta
docs: atualiza documentacao da Fase 1.2
fix: corrige carregamento de variaveis QA_API_
chore: registra base validada das fases 0 e 1
```

## Estrategia de snapshots

Snapshots sao backups compactados para recuperacao manual rapida. Eles complementam o Git, mas nao substituem o Git.

Local padrao:

```text
backup/
```

Padrao de nome:

```text
backup/QualidadeAmbiental_API_FastAPI_Fase1_2026-05-27.zip
```

Snapshots devem ser gerados antes de:

- refatoracoes relevantes;
- alteracoes de conexao SQL Server;
- criacao de endpoints reais;
- alteracoes em models;
- mudancas estruturais de pastas;
- mudancas de dependencias relevantes.

Snapshots nunca devem conter:

- `.env`;
- `.venv/`;
- `.git/`;
- `__pycache__/`;
- `*.pyc`;
- `*.log`;
- `.pytest_cache/`;
- arquivos ZIP antigos dentro de `backup/`.

## Git x backup ZIP

Git registra historico incremental do projeto e permite comparar, revisar e reverter mudancas.

Backup ZIP e uma copia manual de recuperacao rapida em um ponto especifico. Ele e util antes de mudancas criticas, mas nao oferece historico detalhado como o Git.

## Politica de rollback

Rollback preferencial:

1. verificar `git status`;
2. identificar o commit estavel;
3. revisar o diff;
4. reverter de forma controlada.

Snapshots ZIP devem ser usados somente quando o repositorio local estiver indisponivel, corrompido ou quando for necessario recuperar uma copia isolada rapidamente.

## Cuidados com credenciais

O arquivo `.env` deve existir apenas localmente. O repositorio deve conter somente `.env.example`.

Nunca registrar em Git:

- usuario real do SQL Server;
- senha real;
- strings de conexao com segredo;
- tokens;
- certificados privados.

## Checklist antes de mudancas criticas

- `git status` revisado;
- commit estavel existente;
- `.env` fora do Git;
- `.venv` fora do Git;
- snapshot gerado quando a mudanca for estrutural;
- README e docs atualizados quando houver decisao tecnica nova.
