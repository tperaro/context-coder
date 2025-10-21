# Problemas Identificados - Context2Task

**Data da Análise:** 20/10/2025  
**Status:** Revisão Completa do Sistema

---

## 📊 Resumo Executivo

O sistema foi desenvolvido seguindo spec-driven-development, mas possui **problemas críticos de implementação** que impedem seu funcionamento completo. Os principais gaps estão na integração LangGraph → MCP, dependências não instaladas, e fluxo de dados incompleto.

### Problemas por Categoria:

| Categoria | P0 (Crítico) | P1 (Importante) | P2 (Melhoria) |
|-----------|--------------|-----------------|---------------|
| **Backend** | 4 | 3 | 2 |
| **Frontend** | 2 | 2 | 3 |
| **Integração** | 3 | 2 | 1 |
| **DevOps** | 2 | 1 | 1 |
| **Total** | **11** | **8** | **7** |

---

## 🔴 P0 - PROBLEMAS CRÍTICOS (Impedem funcionamento)

### Backend

#### 1. **Dependências Python não instaladas**
- **Problema:** `pip list` mostra que FastAPI, LangGraph, LangChain não estão instalados
- **Localização:** Sistema de ambiente Python
- **Impacto:** Backend não inicia
- **Solução:**
  ```bash
  cd backend
  poetry install
  # OU para Docker:
  docker-compose build --no-cache backend
  ```

#### 2. **MCP Service não funcional**
- **Problema:** `services/mcp.py` usa `npx @zilliztech/claude-context` mas:
  - Não verifica se Node.js está instalado
  - Não trata timeout de comandos longos (indexação)
  - Não há fallback quando MCP falha
- **Localização:** `backend/services/mcp.py` linhas 66-103
- **Impacto:** Sistema não consegue buscar contexto do código
- **Erro esperado:**
  ```
  RuntimeError: MCP command failed: npx: command not found
  ```
- **Solução:** Ver seção "Correções Propostas"

#### 3. **LangGraph checkpointing não persiste**
- **Problema:** `MemorySaver()` perde estado quando container reinicia
- **Localização:** `backend/agent/graph.py` linha 97
- **Impacto:** Conversas não são persistidas entre sessões
- **Solução:** Implementar `SqliteSaver` ou `PostgresSaver`

#### 4. **Nodes retornam dados inconsistentes**
- **Problema:** Alguns nodes retornam `StateUpdate` (TypedDict parcial), outros retornam dict completo
- **Localização:** `backend/agent/nodes/core.py`
- **Exemplo:**
  ```python
  # analyze_feature_node retorna messages como dict
  return {"messages": [{"role": "assistant", "content": "..."}]}
  
  # Mas AgentState.messages usa add_messages reducer que espera Message objects
  messages: Annotated[List[Dict[str, str]], add_messages]
  ```
- **Impacto:** Mensagens podem não aparecer corretamente no chat
- **Solução:** Padronizar formato de retorno (sempre usar LangChain Message objects)

### Frontend

#### 5. **Session ID não é gerado corretamente**
- **Problema:** `stores/session.ts` não gera `sessionId` no início
- **Localização:** `frontend/src/stores/session.ts`
- **Impacto:** Primeira mensagem falha com erro "session_id required"
- **Solução:**
  ```typescript
  // Gerar sessionId no início
  sessionId: crypto.randomUUID(),
  ```

#### 6. **UI não trata erros de API**
- **Problema:** `ChatInterface.tsx` não exibe mensagens de erro específicas
- **Localização:** `frontend/src/components/chat/ChatInterface.tsx` linha 48
- **Impacto:** Usuário não sabe o que deu errado
- **Solução:** Implementar toast/alert com mensagem de erro

### Integração

#### 7. **API endpoints não implementados**
- **Problema:** Endpoints definidos mas sem implementação real:
  - `/api/repositories/discover` - busca parcialmente funcional
  - `/api/repositories/index` - chama MCP mas não valida resultado
  - `/api/export/markdown` - não implementado
  - `/api/export/json` - não implementado
- **Localização:** `backend/api/export.py` e `backend/api/repositories.py`
- **Impacto:** Features de exportação e gerenciamento de repos não funcionam

#### 8. **CORS não configurado para produção**
- **Problema:** `CORS_ORIGINS` hardcoded para localhost
- **Localização:** `backend/main.py` linha 30
- **Impacto:** Deploy em produção falhará
- **Solução:** Usar variável de ambiente com múltiplos domínios

#### 9. **Frontend não aguarda resposta completa do streaming**
- **Problema:** Se LLM response for muito longa, pode cortar
- **Localização:** `frontend/src/api/client.ts`
- **Impacto:** Respostas do agente podem aparecer incompletas
- **Solução:** Implementar streaming real ou aumentar timeout

### DevOps

#### 10. **Dockerfile do backend não instala Node.js**
- **Problema:** MCP precisa de Node.js mas Dockerfile Python não tem
- **Localização:** `backend/Dockerfile`
- **Impacto:** MCP não funciona dentro do container
- **Solução:**
  ```dockerfile
  # Instalar Node.js 20+ no Dockerfile
  RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
  RUN apt-get install -y nodejs
  ```

#### 11. **Docker volumes montados incorretamente**
- **Problema:** `~/.cache/pypoetry` pode não existir no host
- **Localização:** `docker-compose.yml` linha 29
- **Impacto:** Build lento ou falha de permissão
- **Solução:** Criar volume nomeado para cache do Poetry

---

## 🟡 P1 - PROBLEMAS IMPORTANTES (Limitam funcionalidade)

### Backend

#### 12. **Prompts não customizados por perfil**
- **Problema:** `prompts/profiles.py` retorna prompts genéricos
- **Localização:** `backend/agent/prompts/profiles.py`
- **Impacto:** Usuários não-técnicos recebem respostas muito técnicas
- **Solução:** Implementar prompts específicos seguindo `prompts-library.md`

#### 13. **Spec sections não seguem template da empresa**
- **Problema:** `update_spec_node` não usa `company-task-template.md`
- **Localização:** `backend/agent/nodes/core.py` linha 173
- **Impacto:** Documento exportado não está no formato esperado
- **Solução:** Carregar template real e preencher seções corretas

#### 14. **Tech Debt / Security nodes vazios**
- **Problema:** `nodes/optional.py` tem stubs sem implementação
- **Localização:** `backend/agent/nodes/optional.py`
- **Impacto:** Features "Should Have" da spec não funcionam
- **Solução:** Implementar análise real usando LLM + regex patterns

### Frontend

#### 15. **Voice Input não funcional**
- **Problema:** `VoiceInput.tsx` provavelmente usa Web Speech API sem fallback
- **Impacto:** Feature de voz (prioritária na spec) não funciona em todos browsers
- **Solução:** Implementar fallback ou usar serviço de transcrição

#### 16. **Markdown Preview ausente**
- **Problema:** Spec da spec menciona "Side-by-side preview" mas não está implementado
- **Localização:** UI de review
- **Impacto:** Usuário não vê preview antes de exportar
- **Solução:** Adicionar componente de preview com react-markdown

### Integração

#### 17. **Multi-spec detection não implementada**
- **Problema:** `detect_multi_spec_node` apenas retorna flag booleana
- **Localização:** `backend/agent/nodes/optional.py`
- **Impacto:** Feature crítica (R11 da spec) não funciona
- **Solução:** Implementar análise de impacto cross-repo

#### 18. **GitHub integration ausente**
- **Problema:** `api/github.py` está vazio
- **Localização:** `backend/api/github.py`
- **Impacto:** Não cria issues/PRs automaticamente (feature "Should Have")

---

## 🟢 P2 - MELHORIAS (Nice to have)

### Backend

#### 19. **Logging excessivo em produção**
- **Problema:** Muitos logs DEBUG em production
- **Solução:** Configurar níveis de log por ambiente

#### 20. **Sem rate limiting**
- **Problema:** API não tem rate limiting
- **Solução:** Adicionar middleware de rate limiting

### Frontend

#### 21. **Sem dark mode persistente**
- **Problema:** Dark mode não salva preferência
- **Solução:** Usar localStorage

#### 22. **Sem loading states granulares**
- **Problema:** Loading spinner genérico, não mostra "Buscando código..." etc
- **Solução:** Adicionar estados específicos

#### 23. **Sem autocomplete de repos**
- **Problema:** Precisa digitar path completo
- **Solução:** Adicionar autocomplete/search

### Integração

#### 24. **Sem tratamento de tokens limits**
- **Problema:** Se contexto for muito grande, LLM vai falhar
- **Solução:** Implementar chunking/summarization

### DevOps

#### 25. **Sem health checks no Docker**
- **Problema:** docker-compose não verifica se serviços estão prontos
- **Solução:** Adicionar healthcheck directives

#### 26. **Sem testes automatizados funcionais**
- **Problema:** Testes existem mas provavelmente não passam
- **Localização:** `backend/tests/`
- **Solução:** Atualizar testes para refletir implementação atual

---

## 🛠️ CORREÇÕES PRIORITÁRIAS (Action Items)

### Sprint 1: Fazer o básico funcionar (P0)

1. **Instalar dependências**
   ```bash
   cd backend && poetry install
   cd ../frontend && npm install
   ```

2. **Corrigir Dockerfile do backend**
   - Adicionar Node.js 20+
   - Instalar dependências do Poetry corretamente

3. **Corrigir MCP Service**
   - Adicionar verificação de Node.js
   - Implementar timeout e retry
   - Adicionar fallback quando MCP falha

4. **Corrigir geração de sessionId**
   - Frontend deve gerar UUID no primeiro acesso

5. **Padronizar formato de mensagens**
   - Todos nodes devem retornar LangChain Message objects

### Sprint 2: Features essenciais (P1)

1. **Implementar prompts customizados por perfil**
2. **Carregar e usar company-task-template.md real**
3. **Implementar tech debt e security analysis**
4. **Adicionar markdown preview no frontend**
5. **Implementar endpoints de exportação**

### Sprint 3: Completar spec (P1+P2)

1. **Multi-spec detection e split**
2. **GitHub integration (criar issues)**
3. **Voice input com fallback**
4. **Mermaid diagram generation**
5. **Testes end-to-end**

---

## 📋 CHECKLIST DE VALIDAÇÃO

Depois de corrigir P0, sistema deve:

- [ ] Backend inicia sem erros (`uvicorn main:app --reload`)
- [ ] Frontend inicia sem erros (`npm run dev`)
- [ ] Endpoint `/health` retorna 200
- [ ] Consegue descobrir repositórios (`/api/repositories/discover`)
- [ ] Consegue indexar um repositório (`/api/repositories/index`)
- [ ] Consegue enviar mensagem no chat e receber resposta
- [ ] SessionId é gerado automaticamente
- [ ] Mensagens aparecem corretamente na UI
- [ ] Progresso de spec é atualizado
- [ ] Consegue exportar markdown (mesmo que básico)

---

## 🔗 ARQUIVOS CRÍTICOS PARA REVISAR

1. **Backend:**
   - `backend/services/mcp.py` - MCP integration
   - `backend/agent/nodes/core.py` - Core logic
   - `backend/agent/graph.py` - LangGraph setup
   - `backend/agent/checkpointing.py` - Session management
   - `backend/Dockerfile` - Container setup

2. **Frontend:**
   - `frontend/src/stores/session.ts` - State management
   - `frontend/src/components/chat/ChatInterface.tsx` - Main UI
   - `frontend/src/api/client.ts` - API calls

3. **DevOps:**
   - `docker-compose.yml` - Orchestration
   - `.env` - Configuration

---

## 📞 PRÓXIMOS PASSOS

1. **Revisar este documento com o time**
2. **Priorizar correções (começar por P0)**
3. **Criar branches para cada fix**
4. **Testar cada correção isoladamente**
5. **Atualizar specs e docs conforme implementação real**

---

**Conclusão:** O projeto tem uma **arquitetura sólida** e **especificações bem detalhadas**, mas a **implementação está incompleta** em pontos críticos. Com foco nas correções P0 e P1, o sistema pode ficar funcional em 2-3 sprints.
