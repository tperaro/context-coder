# LangSmith Integration - Context-Coder

## 📊 Visão Geral

O Context-Coder agora está integrado com o **LangSmith**, uma plataforma de observabilidade para aplicações LLM que permite:

- 🔍 **Rastreamento** de todas as execuções do LangGraph
- 🐛 **Debugging** de conversas e decisões do agente
- 📈 **Métricas** de performance e custos
- 🔗 **Visualização** do fluxo completo de execução dos nodes
- 🏷️ **Tags e Metadata** para organizar traces

## 🚀 Quick Start

### 1. Obter API Key (2 minutos)

1. Acesse [smith.langchain.com](https://smith.langchain.com/)
2. Crie uma conta gratuita ou faça login
3. Vá em **Settings** → **API Keys**
4. Clique em **Create API Key**
5. Copie a chave (começa com `lsv2_pt_...`)

### 2. Configurar (1 minuto)

Adicione ao seu arquivo `.env` no diretório `backend/`:

```bash
# Habilitar rastreamento
LANGCHAIN_TRACING_V2=true

# Sua API key do LangSmith
LANGCHAIN_API_KEY=lsv2_pt_sua_chave_aqui

# Nome do projeto (opcional)
LANGCHAIN_PROJECT=context-coder-dev

# Endpoint (opcional, padrão: US)
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

### 3. Instalar Dependência

```bash
cd backend
poetry install
# ou
pip install langsmith>=0.1.0
```

### 4. Iniciar a Aplicação

```bash
cd backend
poetry run uvicorn main:app --reload
```

Você verá no console:

```
✓ LangSmith configurado - Projeto: context-coder-dev, Endpoint: https://api.smith.langchain.com
```

### 5. Ver Traces em Tempo Real

1. Execute qualquer operação (criar uma spec, analisar feature, etc)
2. Acesse [smith.langchain.com](https://smith.langchain.com/)
3. Selecione seu projeto `context-coder-dev`
4. Veja os traces com:
   - Fluxo completo do agent (nodes)
   - Inputs e outputs de cada node
   - Chamadas LLM (prompts + respostas)
   - Performance e latência
   - Custos por execução

## 🏗️ Arquitetura

### Módulo Principal

`backend/services/langsmith.py` - Serviço centralizado com:

- **LangSmithConfig**: Configuração via variáveis de ambiente
- **@traceable**: Decorador para rastrear funções
- **trace_context**: Context manager para rastreamento customizado
- **create_run_config**: Helper para adicionar tags/metadata
- **hide_sensitive_data**: Ocultar dados sensíveis em traces

### Nodes Rastreados Automaticamente

Todos os nodes do agent estão instrumentados com `@traceable`:

#### Core Nodes (`agent/nodes/core.py`)
- ✅ `analyze_feature_node` - Análise inicial da feature
- ✅ `search_codebase_node` - Busca no codebase via MCP
- ✅ `llm_response_node` - Geração de resposta da IA
- ✅ `update_spec_node` - Atualização da especificação

#### Optional Nodes (`agent/nodes/optional.py`)
- ✅ `detect_multi_spec_node` - Detecção de multi-spec
- ✅ `tech_debt_node` - Análise de dívida técnica
- ✅ `security_check_node` - Checklist de segurança
- ✅ `generate_diagram_node` - Geração de diagramas Mermaid

### Tags Aplicadas

Cada node possui tags específicas para facilitar filtros:

```python
@traceable(name="analyze_feature", run_type="chain", tags=["agent", "analysis"])
@traceable(name="llm_response", run_type="llm", tags=["agent", "llm", "response"])
@traceable(name="tech_debt_analysis", run_type="chain", tags=["agent", "analysis", "tech-debt"])
```

## 💡 Uso Avançado

### Adicionar Metadata Customizada

```python
from services.langsmith import create_run_config

config = create_run_config(
    run_name="feature_spec_session_123",
    tags=["production", "feature_analysis"],
    metadata={
        "user_profile": "technical",
        "repository": "myrepo",
        "session_id": "abc-123"
    }
)

# Usar com o graph
result = await graph.invoke(inputs, config)
```

### Context Manager para Seções Específicas

```python
from services.langsmith import trace_context

with trace_context(
    tags=["production", "critical"],
    metadata={"environment": "prod"}
):
    # Seu código aqui
    result = await process_critical_operation()
```

### Decorador em Funções Customizadas

```python
from services.langsmith import traceable

@traceable(
    name="custom_analysis",
    run_type="chain",
    tags=["custom", "analysis"],
    metadata={"version": "2.0"}
)
async def analyze_custom_data(data: dict) -> dict:
    # Sua lógica aqui
    return result
```

### Ocultar Dados Sensíveis

```python
from services.langsmith import hide_sensitive_data

# Ocultar chaves específicas
safe_data = hide_sensitive_data(
    user_data,
    sensitive_keys=["email", "cpf", "token", "api_key"]
)

# Resultado: campos sensíveis são substituídos por "***HIDDEN***"
```

## 🔧 Configuração Avançada

### Variáveis de Ambiente Completas

```bash
# ===== LangSmith Configuration =====

# Habilitar tracing (true/false)
LANGCHAIN_TRACING_V2=true

# API Key (obrigatória)
LANGCHAIN_API_KEY=lsv2_pt_sua_chave_aqui

# Endpoint (opcional)
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
# Para EU: https://eu.api.smith.langchain.com

# Nome do projeto (opcional, padrão: "context-coder")
LANGCHAIN_PROJECT=context-coder-production

# Workspace ID (opcional, para API keys organizacionais)
# LANGSMITH_WORKSPACE_ID=your-workspace-id-here
```

### Desabilitar Temporariamente

```bash
# No .env
LANGCHAIN_TRACING_V2=false
```

Ou remova/comente a variável `LANGCHAIN_API_KEY`.

## 📊 Exemplos de Traces

### 1. Feature Analysis Flow

```
📊 Trace: feature_spec_session_123
  ├─ 🔍 analyze_feature (chain)
  │   └─ Input: "Implementar autenticação OAuth"
  │   └─ Output: goals, complexity, questions
  ├─ 🔎 search_codebase (retriever)
  │   └─ MCP queries: auth, oauth, implementation
  │   └─ Results: 15 code snippets
  ├─ 🤖 llm_response (llm)
  │   └─ Prompt: TECHNICAL_SYSTEM_PROMPT + context
  │   └─ Response: Detailed analysis
  └─ 📝 update_spec (chain)
      └─ Sections filled: 5/10
```

### 2. Tech Debt Analysis

```
📊 Trace: tech_debt_analysis_456
  ├─ 🔍 tech_debt_analysis (chain)
  │   └─ Categories: code_smells, performance, security
  │   └─ Code snippets: 12 files analyzed
  │   └─ Output: 8 issues found
  │       ├─ Critical: 2
  │       ├─ Medium: 4
  │       └─ Low: 2
```

## 🐛 Troubleshooting

### Traces não aparecem?

1. **Verificar configuração:**
   ```bash
   cd backend
   poetry run python -c "from services.langsmith import log_langsmith_status; log_langsmith_status()"
   ```

2. **Verificar variáveis de ambiente:**
   ```bash
   echo $LANGCHAIN_TRACING_V2
   echo $LANGCHAIN_API_KEY
   ```

3. **Logs da aplicação:**
   Procure por:
   - `✓ LangSmith configurado` (sucesso)
   - `✗ LangSmith não está configurado` (problema)

### API Key inválida?

- Confirme que copiou a chave completa
- A chave deve começar com `lsv2_pt_`
- Tente gerar uma nova chave no LangSmith

### Performance degradada?

O LangSmith adiciona overhead mínimo (~50-100ms por trace). Se necessário:

```bash
# Desabilitar temporariamente
LANGCHAIN_TRACING_V2=false
```

## 📚 Recursos

- 🔗 [LangSmith Documentation](https://docs.smith.langchain.com/)
- 🎥 [LangSmith Tutorials](https://docs.smith.langchain.com/tutorials)
- 💬 [Discord LangChain](https://discord.gg/langchain)
- 📖 [Best Practices](https://docs.smith.langchain.com/best-practices)

## 🎯 Benefícios para o Context-Coder

1. **Debug Rápido**: Veja exatamente onde o agent falhou ou tomou decisão errada
2. **Otimização de Prompts**: Compare diferentes versões de prompts e suas respostas
3. **Análise de Custos**: Monitore tokens e custos por execução
4. **Qualidade**: Identifique patterns de erro e melhore o sistema
5. **Compliance**: Audite todas as interações com o LLM
6. **Performance**: Identifique bottlenecks no fluxo do agent

## 🚦 Status da Implementação

- ✅ Módulo `services/langsmith.py` criado
- ✅ Inicialização no `main.py`
- ✅ Decoradores em todos os nodes principais
- ✅ Variáveis de ambiente no `.env.example`
- ✅ Dependência `langsmith>=0.1.0` adicionada
- ✅ Documentação completa

---

**Pronto!** O Context-Coder agora tem observabilidade completa com LangSmith! 🎉
