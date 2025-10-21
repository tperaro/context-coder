# Context2Task

> **From codebase context to actionable tasks**

Uma plataforma AI que transforma ideias vagas de features em especificações detalhadas e acionáveis, usando contexto inteligente de repositórios de código.

---

## 📋 Visão Geral

**Context2Task** é uma aplicação web que ajuda equipes técnicas e não-técnicas a criar especificações de features de alta qualidade através de conversas guiadas por IA, enriquecidas com contexto real do codebase.

### 🎯 Problema que Resolve

- ⏰ **Tempo**: Reduz especificação de features de 2-3 horas para < 10 minutos
- 🧠 **Contexto**: Garante que features considerem a arquitetura existente
- 🤝 **Comunicação**: Facilita colaboração entre técnicos e não-técnicos
- 📝 **Qualidade**: Gera documentação estruturada e acionável

### 👥 Usuários

1. **Sócios não-técnicos** (Product Owners): Criam tasks com linguagem simplificada
2. **Sócios técnicos** (Devs/Tech Leads): Criam specs detalhadas para equipe
3. **Desenvolvedores**: Recebem documentação pronta para implementação

---

## 🏗️ Arquitetura

### Stack Tecnológica

**Frontend**:
- React 18+ com TypeScript
- shadcn/ui (Radix UI + Tailwind CSS)
- Vite como bundler

**Backend**:
- Python 3.10+ com FastAPI
- **LangGraph** para orquestração do agente (stateful workflows)
- Async/await para performance
- MCP client para integração com repositórios

**AI/ML**:
- LLM: Gemini 2.5 Pro via OpenRouter
- **Agent Framework**: LangGraph + LangChain
- Embeddings: OpenAI (text-embedding-3-small)
- Vector DB: Zilliz Cloud (Milvus Serverless)
- MCP: claude-context para indexação de código

**Infraestrutura**:
- Docker + Docker Compose
- Containerização completa
- Setup com 1 comando

---

## ✨ Features Principais

### Core (V1)
- ✅ Seleção de múltiplos repositórios
- ✅ Perfis adaptativos (técnico vs não-técnico)
- ✅ Chat contextual multi-turno
- ✅ Análise de tradeoffs técnicos
- ✅ Geração de tasks no formato da empresa
- ✅ Download/cópia de documentos
- ✅ Busca semântica em código

### Future (V2+)
- 📊 Histórico de conversas persistido
- 🔗 Integração com GitHub Projects
- 📈 Analytics e métricas de uso
- 🎨 Templates customizáveis
- 🌐 Análise de impacto cross-repo

---

## 📁 Estrutura de Documentação

```
specs/active/ai-feature-assistant-platform/
├── 📋 Core Documents
│   ├── spec.md                            # Especificação completa (347 linhas)
│   ├── plan.md                            # Plano técnico detalhado (1530 linhas)
│   ├── README.md                          # Este arquivo
│   └── NEXT_STEPS.md                      # ⭐ Próximos passos recomendados
│
├── 🎨 UX & Flows
│   ├── user-flows.md                      # Fluxos de usuário (629 linhas)
│   ├── interface-final-v2.md              # Interface redesenhada (521 linhas)
│   └── system-flow-diagram.md             # 11 diagramas Mermaid (980 linhas)
│
├── 🎯 Features
│   ├── priority-features-detail.md        # 9 features prioritárias (806 linhas)
│   ├── multi-spec-feature.md              # Feature multi-repo (500 linhas)
│   └── future-features-brainstorm.md      # 90+ features futuras (501 linhas)
│
├── 🔧 Implementation
│   ├── tasks.md                           # ⭐ 22 tarefas implementáveis
│   ├── tasks-cross-validation.md          # ⭐ CRÍTICO: Análise de gaps nas tasks
│   ├── todo-list.md                       # ⭐ Checklist executável
│   ├── implementation-roadmap.md          # ⭐ Roadmap Sprint-by-Sprint
│   ├── langgraph-architecture.md          # ⭐ Arquitetura do agente (LangGraph)
│   ├── cross-validation-analysis.md       # ⭐ Análise de gaps e edge cases
│   └── prompts-library.md                 # ⭐ Biblioteca de prompts especializados
│
├── 🔌 Integrations
│   ├── openrouter-integration-notes.md    # Guia OpenRouter + Gemini (194 linhas)
│   ├── mcp-integration-notes.md           # Guia MCP (318 linhas)
│   └── company-task-template.md           # Template oficial (110 linhas)
│
└── 📝 Archive
    └── naming-suggestions.md              # Processo de naming (histórico)
```

### Documentos-Chave para Implementação

**Comece por aqui (IMPLEMENTAÇÃO)**:
1. 🔴 **tasks-cross-validation.md** - LEIA PRIMEIRO! Análise de gaps críticos
2. 📍 **tasks.md** - 22 tarefas detalhadas
3. 📍 **todo-list.md** - Checklist executável com progresso
4. 📍 **NEXT_STEPS.md** - Ações imediatas

**Documentação técnica**:
- **plan.md** - Arquitetura e decisões técnicas
- **langgraph-architecture.md** - Arquitetura do agente e orquestração
- **implementation-roadmap.md** - Ordem de implementação

**Durante desenvolvimento**:
- **prompts-library.md** - Todos os prompts para a IA
- **system-flow-diagram.md** - Diagramas de referência
- **priority-features-detail.md** - Detalhes de cada feature

**Para troubleshooting**:
- **cross-validation-analysis.md** - Edge cases e validações
- **user-flows.md** - Comportamento esperado

---

## 🚀 Próximos Passos

### Status Atual
✅ **Especificação completa** - Todas decisões técnicas tomadas  
✅ **Planning completo** - Plano técnico detalhado criado  
✅ **Documentação expandida** - Análises, prompts e roadmap criados  
✅ **Tasks criadas** - 22 tarefas implementáveis, 15 dias estimados  
🚀 **Pronto para implementar** - Comece com TASK-001 (Docker Setup)

### Roadmap
1. ✅ **`/specify`**: Criar especificação
2. ✅ **`/plan`**: Criar plano técnico detalhado
3. ✅ **`/tasks`**: Quebrar em tarefas implementáveis (22 tasks)
4. ⏳ **Implementação**: Desenvolver MVP (15 dias, 5 fases)
5. ⏳ **Deploy**: Containerizar e documentar

### Ação Imediata
🚀 **Comece implementando**: Veja `tasks.md` e `todo-list.md`  
📍 **Primeira tarefa**: TASK-001 (Docker Infrastructure Setup)

---

## 📊 Métricas de Sucesso

- **Volume**: ~50 features/mês
- **Tempo**: < 10 min por spec (vs 2-3h manual)
- **Adoção**: 80% das features
- **Satisfação**: NPS > 8/10
- **Perfil não-técnico**: 70% de uso
- **Perfil técnico**: 90% de uso

---

## 🔗 Referências

- [OpenRouter Docs](https://openrouter.ai/docs)
- [claude-context GitHub](https://github.com/zilliztech/claude-context)
- [shadcn/ui](https://ui.shadcn.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Zilliz Cloud](https://cloud.zilliz.com/)

---

**Criado**: 2025-10-19  
**Última Atualização**: 2025-10-19 (Cross-Validation Complete)  
**Status**: ⚠️ Tasks Require Corrections (see tasks-cross-validation.md)  
**Prioridade**: P0  
**Documentos Totais**: 20 arquivos, ~12,000 linhas  
**Tasks**: 22 tarefas (+4 gaps críticos identificados), 15 dias estimados

