# SDD Features Index

## Navigation
- [📋 Project Overview](00-overview.md)
- [📖 Guidelines](../.sdd/guidelines.md)
- [⚙️ Configuration](../.sdd/config.json)

## Feature Status Dashboard

### Active Features (In Development)
- ⚠️ [Context2Task](active/ai-feature-assistant-platform/spec.md) - Plataforma AI que transforma contexto de repositórios em tasks acionáveis
  - **Status**: ⚠️ **Cross-Validation Complete → Gaps Identificados (62% cobertura)**
  - **Priority**: P0 (Crítico)
  - **Stack**: React + FastAPI + **LangGraph** + Gemini 2.5 Pro + MCP
  - **Tasks**: 22 tarefas (+4 gaps críticos), 15 dias + 3 dias para correções
  - **Documentação**: 20 arquivos, ~12,000 linhas
  - **CRÍTICO**: Leia [tasks-cross-validation.md](active/ai-feature-assistant-platform/tasks-cross-validation.md) ANTES de implementar
  - **Gaps**: LangGraph incompleto (38%), Prompts não integrados (0%), UI desalinhada (20%), Edge cases não testados (20%)

### Completed Features
Currently no completed features.

### Backlog Features
Currently no backlog features.

## Quick Actions
- 🆕 [Create New Feature](active/)
- 📊 [View All Features](.)
- 📝 [Update Guidelines](../.sdd/guidelines.md)
- ⚙️ [Modify Configuration](../.sdd/config.json)

## Statistics
- **Total Features**: 1
- **Active**: 1
- **Completed**: 0
- **Backlog**: 0
- **Documentation Lines**: ~12,000
- **Key Documents**: 20
- **Implementation Tasks**: 22 (+4 gaps críticos identificados)
- **Estimated Timeline**: 15 days MVP + 3 days corrections
- **Cross-Validation**: Complete (62% coverage → target 85%)

## Recent Activity
- 2025-10-19: ⚠️ **Cross-validation das tasks revelou gaps críticos**:
  - Cobertura geral: 62% (precisa melhorar para 85%)
  - **Gap crítico 1**: LangGraph (38% coberto) - TASK-006 muito superficial
  - **Gap crítico 2**: Prompts library (0% integrada) - Tasks não referenciam prompts especializados
  - **Gap crítico 3**: Interface UI (20% alinhada) - Não segue `interface-final-v2.md`
  - **Gap crítico 4**: Edge cases (20% testados) - Não cobre `cross-validation-analysis.md`
  - Recomendação: +3 dias para expandir TASK-006, integrar prompts, alinhar UI, adicionar TASK-023
  - Documento: `tasks-cross-validation.md` (2000+ linhas de análise detalhada)
- 2025-10-19: 🚀 **Tarefas de implementação criadas** (`/tasks`) para Context2Task:
  - 22 tarefas detalhadas e implementáveis
  - 5 fases: Foundation → Core → Advanced → Testing → Deployment
  - Estimativa: 15 dias para MVP
  - Critical path identificado: Docker → Backend → LangGraph → Chat → Export
  - Todo-list executável com checklists e milestones
  - Documentos: `tasks.md` (300+ linhas), `todo-list.md` (600+ linhas)
- 2025-10-19: ✅ **Definida arquitetura do agente com LangGraph** para Context2Task:
  - Framework: LangGraph para orquestração stateful
  - Design híbrido: IA + controle do usuário sobre fluxo do grafo
  - Nós modulares: analyze, search, tech_debt, security, diagram, export
  - Checkpointing: MemorySaver (V1) → PostgresSaver (V2)
  - Documento detalhado: `langgraph-architecture.md` (1500+ linhas)
- 2025-10-19: ✅ **Detalhamento pós-planning completo** para Context2Task:
  - Cross-validation analysis (gaps, edge cases, validações)
  - Biblioteca de prompts especializados (system, análise, multi-spec)
  - Roadmap de implementação detalhado (Sprint-by-Sprint)
  - NEXT_STEPS.md com ações imediatas
- 2025-10-19: ✅ Criado plano técnico detalhado para Context2Task (1530 linhas)
- 2025-10-19: ✅ Criada especificação completa para Context2Task (347 linhas)

---
Last updated: 2025-10-19
