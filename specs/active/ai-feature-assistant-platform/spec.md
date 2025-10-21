# Context2Task Spec

**Nome oficial da plataforma**: Context2Task  
**Tagline**: "From codebase context to actionable tasks"

## What & Why

- **Problem**: Desenvolvedores e product managers precisam transformar ideias vagas de features em especificações detalhadas e acionáveis, mas isso requer muito tempo e conhecimento profundo do codebase existente. Atualmente não há uma ferramenta que automatize esse processo usando contexto do repositório existente.

- **Users**: 
  - **Sócios não-técnicos** (Product Owners): Criam tasks para desenvolvedores sem conhecimento técnico profundo
  - **Sócios técnicos** (Tech Leads/Devs): Criam tasks detalhadas para equipe de desenvolvimento
  - **Equipes de desenvolvimento**: Recebem documentação estruturada para implementação
  
  **Requisito crítico**: O agente deve adaptar sua linguagem e profundidade técnica baseado no perfil do usuário

- **Value**: 
  - Reduz tempo de especificação de features de horas para minutos
  - Garante que features sejam pensadas considerando a arquitetura existente
  - Melhora a qualidade das especificações através de conversas guiadas
  - Facilita a comunicação entre stakeholders técnicos e não-técnicos
  - Gera documentação pronta para uso em ferramentas de gestão de projetos

## Requirements

### Must Have
- **R1: Seleção de repositório(s) alvo** → Interface permite selecionar um ou mais repositórios indexados, combinando contexto de múltiplas bases de código
- **R2: Perfis de usuário adaptativos** → Sistema detecta/permite seleção de perfil (não-técnico vs técnico) e adapta linguagem e profundidade das respostas
- **R3: Interface de chat com histórico multi-turno** → O usuário pode manter conversas contextuais onde cada mensagem se baseia nas anteriores
- **R4: Integração com MCP (Model Context Protocol)** → Sistema deve consumir contexto de repositórios já indexados via MCP
- **R5: Enriquecimento de prompt com contexto multi-repo** → Sistema analisa o prompt inicial e busca contexto relevante nos repositórios selecionados
- **R6: Apresentação de tradeoffs técnicos** → Agente apresenta múltiplas abordagens de implementação com prós e contras (adaptado ao perfil do usuário)
- **R7: Geração de documento markdown final** → Sistema gera spec.md estruturado baseado na conversa seguindo template da empresa
- **R8: Download e cópia de documento** → Interface permite baixar arquivo .md e copiar conteúdo para clipboard
- **R9: Containerização completa** → Frontend e backend devem rodar com um único comando (docker-compose)
- **R10: Seleção iterativa de abordagens** → Usuário pode escolher entre opções apresentadas e refinar progressivamente
- **R11: Geração multi-spec automática** → Quando feature impacta múltiplos repos, sistema gera uma spec separada para cada repositório (automático para não-técnicos, manual para técnicos)

### Should Have  
- Interface web moderna e responsiva (shadcn/ui + Tailwind CSS)
- Visualização de trechos de código relevantes dos repositórios
- **Markdown Preview Side-by-Side** (editor + preview em tempo real)
- **Voice Input** 🎤 (essencial - fala feature, IA transcreve e estrutura)
- **Interactive Tutorial** (walkthrough guiado na primeira vez)
- **Tech Debt Detector** ⚠️ (botão antes de exportar - analisa TODOs/dívidas no código)
- **Security Checklist** 🛡️ (baseado em critérios da empresa - LGPD, OWASP)
- **Review Mode + @Mentions** ✅ (workflow Draft → Review → Approved com assignments)
- **Template Sharing** 📑 (compartilha templates entre times)
- **Mermaid Diagrams** 📐 (opcional - gera diagramas de arquitetura sob demanda)
- Histórico de conversas persistido (opcional - v2)
- Templates de documentos customizáveis por perfil
- Exportação em múltiplos formatos (Markdown, JSON, YAML)
- Integração direta com GitHub Projects API
- Sistema de tags e categorização de features
- Análise de impacto cross-repo (quando múltiplos repos selecionados)
- **Split automático de specs por repositório** (gera task separada para backend, frontend, etc.)
- Linking entre specs relacionadas (tasks conectadas)
- Sugestão de testes baseada na feature
- Estimativa de complexidade adaptada ao perfil
- Glossário técnico para usuários não-técnicos

### Could Have
- **Dependency Graph** 🕸️ (visualização de features dependentes - menor prioridade)
- Integração com Jira, Linear, etc.
- Comparação de features similares já implementadas
- Sugestão de reviewer baseado em ownership de código
- Modo colaborativo multi-usuário tempo real
- Versionamento de especificações (Git-like)

### Won't Have (Out of Scope)
- Implementação automática de código
- Gestão completa de projetos
- Sistema de CI/CD integrado
- Code review automatizado
- Deploy automático

## User Stories

### US1: Especificação Rápida de Feature
**Como desenvolvedor**, quero inserir uma ideia de feature e receber um documento detalhado → para reduzir tempo de planejamento
- **AC**: 
  - Sistema aceita prompt de texto livre
  - Busca contexto relevante no repositório indexado
  - Gera documento markdown com especificação completa
  - Processo completo em < 5 minutos
- **Priority**: P0 (Crítico) | **Effort**: 8 pontos

### US2: Exploração de Tradeoffs
**Como tech lead**, quero ver diferentes abordagens técnicas com prós e contras → para tomar decisões informadas
- **AC**:
  - Sistema apresenta pelo menos 2-3 abordagens diferentes
  - Cada abordagem lista tradeoffs claros (performance, manutenibilidade, complexidade)
  - Considera arquitetura atual do projeto
  - Permite comparação lado a lado
- **Priority**: P0 (Crítico) | **Effort**: 13 pontos

### US3: Conversa Contextual
**Como product manager**, quero refinar a especificação através de conversas → para chegar na melhor solução
- **AC**:
  - Chat mantém contexto de mensagens anteriores
  - Pode fazer perguntas de esclarecimento
  - Ajusta a especificação baseado em feedback
  - Histórico navegável da conversa
- **Priority**: P0 (Crítico) | **Effort**: 8 pontos

### US4: Exportação para GitHub Projects
**Como desenvolvedor**, quero copiar/baixar o documento final → para adicionar no GitHub Projects sem retrabalho
- **AC**:
  - Botão de download gera arquivo .md
  - Botão de copy copia formatação markdown para clipboard
  - Documento segue formato compatível com GitHub Projects
  - Inclui metadados (labels, estimates, etc.)
- **Priority**: P0 (Crítico) | **Effort**: 3 pontos

### US5: Setup Simplificado
**Como usuário**, quero rodar a aplicação com 1 comando → para começar a usar rapidamente
- **AC**:
  - `docker-compose up` inicia frontend e backend
  - Não requer configuração manual complexa
  - Variáveis de ambiente documentadas
  - Healthcheck automático
- **Priority**: P0 (Crítico) | **Effort**: 5 pontos

### US6: Análise de Impacto
**Como desenvolvedor**, quero ver que partes do código serão afetadas → para estimar melhor o esforço
- **AC**:
  - Sistema identifica módulos/arquivos impactados
  - Mostra dependencies afetadas
  - Sugere áreas que precisam de testes
  - Estima complexidade da mudança
- **Priority**: P1 (Alto) | **Effort**: 13 pontos

## Success Metrics

### Métricas de Adoção
- **Volume esperado**: ~50 features especificadas/mês
- **Tempo médio de especificação**: < 10 minutos (vs. 2-3 horas manual)
- **Taxa de uso**: 80% das novas features passam pela ferramenta
- **NPS (Net Promoter Score)**: > 8/10
- **Taxa de uso por perfil**: 70% dos não-técnicos + 90% dos técnicos

### Métricas de Qualidade
- **Completude de specs**: 95% das specs geradas incluem todos os campos obrigatórios
- **Taxa de retrabalho**: < 15% das specs precisam de revisão significativa
- **Acurácia de contexto**: 90% do contexto buscado é relevante

### Métricas Técnicas
- **Tempo de resposta**: < 3s para enriquecimento de contexto
- **Uptime**: 99%+
- **Tempo de setup**: < 2 minutos do clone ao primeiro uso

## Technical Considerations

### Arquitetura Definida
- **Frontend**: React + TypeScript com **shadcn/ui** (Radix UI + Tailwind CSS)
  - Trust Score: 10/10
  - Copy-paste components (não dependência npm pesada)
  - Totalmente customizável e type-safe
  - Acessibilidade nativa via Radix UI
- **Backend**: Python (FastAPI recomendado para performance e async)
- **LLM Provider**: OpenRouter API (Gemini 2.5 Pro como padrão)
- **MCP**: claude-context da Zilliz (local via npx + Zilliz Cloud)
- **Storage**: In-memory (sessão) - V1 sem persistência entre restarts
- **Containerização**: Docker + Docker Compose
- **Ambiente**: Ubuntu 22.04 Linux

### Integrações
- **MCP Tools Disponíveis**:
  - `index_codebase`: Indexação com hybrid search (BM25 + dense vector)
  - `search_code`: Busca semântica com linguagem natural
  - `clear_index`: Limpeza de índice
  - `get_indexing_status`: Status de progresso da indexação
- **LLM API**: OpenRouter (suporta múltiplos modelos - Claude, GPT-4, etc.)
- **Docker**: Frontend (Node + React) + Backend (Python + FastAPI) + Nginx (opcional)

### Desafios Técnicos
1. **Gerenciamento de contexto**: Como otimizar buscas no MCP sem explodir tokens do OpenRouter
2. **Qualidade de tradeoffs**: Como garantir que análises sejam relevantes e não genéricas
3. **Persistência de estado**: Manter conversas em memória durante sessão (sem DB)
4. **Latência**: Balancear qualidade de resposta com tempo de resposta (Zilliz Cloud + OpenRouter)
5. **Segurança de dados**: Garantir que dados sensíveis não vazem em logs ou requests LLM
6. **Gestão de sessões**: Como identificar e manter múltiplas conversas simultâneas (in-memory)
7. **Integração MCP**: Backend Python precisa se comunicar com MCP Node.js (subprocess ou porta HTTP)

## Dependencies

### Técnicas
- **claude-context MCP Server** (Zilliz) - já configurado e remoto
- **OpenRouter API Key** - acesso a LLMs
- **Docker e Docker Compose** - instalados em Ubuntu 22.04
- **Node.js** (para build do React) - dentro do container
- **Python 3.10+** - dentro do container
- **MCP Client Library** - para comunicação com claude-context

### Conhecimento/Recursos
- Documentação do claude-context MCP: https://github.com/zilliztech/claude-context
- Documentação OpenRouter API: https://openrouter.ai/docs
- **Template de Task da Empresa**: Ver `company-task-template.md` neste diretório
- Guia de boas práticas de especificação da empresa

### Configuração Necessária
- `.env` com variáveis:
  - `OPENROUTER_API_KEY`: chave do OpenRouter
  - `DEFAULT_LLM_MODEL`: `google/gemini-2.5-pro`
  - `FALLBACK_MODELS`: lista de modelos backup (opcional)
  - `OPENAI_API_KEY`: para embeddings do MCP (claude-context)
  - `MILVUS_ADDRESS`: endpoint do Zilliz Cloud Serverless
  - `MILVUS_TOKEN`: token de autenticação do Milvus
  - `ALLOWED_ORIGINS`: CORS config
  - `APP_NAME`: "Context2Task" (para X-Title header OpenRouter)
  - `APP_URL`: URL da aplicação (para HTTP-Referer header)

## Out of Scope

- **Implementação de código**: Sistema não gera código, apenas especificações
- **Code review automatizado**: Não analisa qualidade de código existente
- **Gestão de projeto completa**: Não substitui ferramentas como Jira/GitHub Projects
- **Deploy e CI/CD**: Não gerencia pipelines de deploy
- **Autenticação avançada**: V1 pode usar auth simples, SSO fica para depois
- **Modo offline**: Requer conexão para acessar LLM APIs
- **Multi-repositório**: V1 funciona com um repositório por vez
- **Análise de código em tempo real**: Usa apenas índice MCP, não faz parse dinâmico

## Edge Cases & Error Handling

### Casos de Borda
1. **Repositório muito grande**: Como lidar quando contexto excede limites de tokens?
2. **Feature muito vaga**: Como guiar usuário quando prompt inicial é insuficiente?
3. **Múltiplas features relacionadas**: Como lidar quando feature depende de outras não implementadas?
4. **Conflitos arquiteturais**: Como alertar quando feature viola padrões existentes?

### Tratamento de Erros
- **MCP Server indisponível**: Fallback para modo sem contexto + alerta ao usuário
- **LLM API rate limit**: Queue de requisições + retry com backoff
- **Timeout em conversas longas**: Auto-save periódico do estado
- **Documento malformado**: Validação antes de permitir download

## Open Questions

### ✅ Resolvidas
- ~~Stack Tecnológica~~ → React + Python (FastAPI) + sem DB
- ~~Integração MCP~~ → claude-context (Zilliz) remoto com hybrid search
- ~~LLM~~ → OpenRouter API
- ~~Deployment~~ → Local, Ubuntu 22.04
- ~~Autenticação~~ → Não precisa para V1
- ~~Formato de documento~~ → Template da empresa com 10 seções estruturadas
- ~~Modelo LLM~~ → Gemini 2.5 Pro via OpenRouter
- ~~Configuração MCP~~ → Local via npx + Zilliz Cloud Serverless

### ⚠️ Pendentes - CRÍTICO

#### 1. Formato do Documento Final ✅ **RESOLVIDO**
**Template da empresa recebido e salvo em `company-task-template.md`**

O documento final gerado pela plataforma deve seguir a estrutura:
1. 📌 **Descrição / Contexto**: Objetivo geral e contexto técnico/negócio
2. 👤 **User Story**: Como [perfil], quero [ação], para que [benefício]
3. 📋 **Resultado Esperado**: Artefatos, scripts, funcionalidades esperadas
4. ⚙️ **Detalhes Técnicos / Escopo**: O que deve ser feito tecnicamente
5. 📌 **Checklist de Tarefas**: Subtarefas marcáveis
6. ✅ **Critérios de Aceite**: Condições para aceitar a task
7. 📦 **Definição de Done**: Estado esperado ao encerrar
8. 🔍 **Observações Adicionais**: Notas, sugestões, decisões
9. 🔗 **Referências / Links Úteis** (opcional)
10. ⚠️ **Riscos ou Limitações** (opcional)

**Formato**: Markdown puro, sem frontmatter YAML/JSON, com emojis para seções

#### 2. Segurança de Dados Sensíveis
Você mencionou que há **dados sensíveis** no repositório:
- **Que tipo de dados?** (secrets, PII, código proprietário crítico?)
- **Precisa filtrar/sanitizar** antes de enviar ao OpenRouter?
- **Logging**: posso logar contexto buscado ou precisa ser anonimizado?
- **Retenção**: quanto tempo manter conversas em memória? (limpar após X minutos de inatividade?)

#### 3. Modelo LLM Padrão ✅ **RESOLVIDO**
**Modelo configurado: `google/gemini-2.5-pro` via OpenRouter**

Configuração:
- **Modelo principal**: `google/gemini-2.5-pro` (através do OpenRouter)
- **Autenticação**: Bearer token no header `Authorization`
- **Endpoint**: `https://openrouter.ai/api/v1/chat/completions`
- **Features disponíveis**:
  - Prompt caching (otimização de custos para contextos grandes)
  - Multi-turn conversations
  - System messages para instruções
  - Support para tool calling (se necessário no futuro)
- **Fallback**: Pode ser configurado via `extra_body.models` array (ex: anthropic/claude-3.5-sonnet)
- **Headers opcionais**: `HTTP-Referer` e `X-Title` para ranking no OpenRouter

#### 4. Configuração do MCP ✅ **RESOLVIDO**
**MCP local via npx + Zilliz Cloud (Milvus Serverless)**

Configuração identificada:
- **Tipo**: Local MCP server (executa via `npx @zilliz/claude-context-mcp@latest`)
- **Comunicação**: Stdio (não HTTP) - processo local
- **Backend**: Zilliz Cloud Serverless (`in03-1d4be7cd0fd6b0a.serverless.gcp-us-west1.cloud.zilliz.com`)
- **Embeddings**: OpenAI API (`text-embedding-3-small` provavelmente)
- **Autenticação MCP**: Não necessária (processo local)
- **Autenticação Milvus**: Via `MILVUS_TOKEN` (já configurado)
- **Tools disponíveis**: `index_codebase`, `search_code`, `clear_index`, `get_indexing_status`

**Implicações para a plataforma**:
- Backend Python precisa executar subprocess do MCP ou usar biblioteca MCP client
- Alternativa: Usar diretamente `@zilliz/claude-context-core` (Node) ou implementar cliente Python
- Precisa das mesmas credenciais (OPENAI_API_KEY, MILVUS_ADDRESS, MILVUS_TOKEN)

---

## Next Steps

### Antes de `/plan`
1. ✅ Definir stack tecnológica
2. ✅ Confirmar integrações (MCP, LLM)
3. ✅ Receber template de task da empresa
4. ✅ Definir modelo LLM padrão (Gemini 2.5 Pro)
5. ✅ Confirmar configuração MCP (local via npx + Zilliz Cloud)
6. ⏳ Esclarecer requisitos de segurança de dados (assumir defaults seguros)

### Após receber informações pendentes
1. ✅ Executar `/plan` para criar arquitetura técnica detalhada
2. ✅ Executar `/tasks` para quebrar em tarefas implementáveis
3. ⏳ Começar implementação do MVP (22 tarefas, 15 dias estimados)

---

**Status**: ✅ Tasks Created - Ready to Implement  
**Owner**: TBD  
**Created**: 2025-10-19  
**Last Updated**: 2025-10-19  
**Priority**: P0 (Alta prioridade para início de desenvolvimento)

**Stack Tecnológica Confirmada**:
- Frontend: React + TypeScript + shadcn/ui (Radix UI + Tailwind)
- Backend: Python (FastAPI)
- LLM: Gemini 2.5 Pro via OpenRouter
- MCP: claude-context (local + Zilliz Cloud)
- Storage: In-memory (V1)
- Deploy: Docker Compose local (Ubuntu 22)
- UI Library: shadcn/ui (Trust Score 10/10, copy-paste components)

**Features Críticas Adicionadas**:
- Multi-repositório: Seleção e combinação de múltiplos repos
- Multi-perfil: Usuários técnicos vs não-técnicos com adaptação de linguagem
- Volume: ~50 features/mês

