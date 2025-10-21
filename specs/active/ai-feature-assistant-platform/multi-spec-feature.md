# Feature: Split Multi-Repo Specs

## 🎯 Visão Geral

Quando uma feature impacta múltiplos repositórios (ex: backend + frontend), o sistema gera **automaticamente uma spec separada para cada repositório**, permitindo que cada time trabalhe com documentação específica e focada.

---

## 🤔 Problema que Resolve

### Cenário Atual (Sem Split)
```
📄 Spec única: "Sistema de Notificações Push"
├─ Backend: configurar Firebase, API endpoints, workers...
├─ Frontend: componentes UI, integração SDK, permissões...
├─ Mobile: Firebase SDK, notificações nativas...
└─ Infra: configurar Firebase project, variáveis...

❌ Problemas:
   • Spec gigante e confusa
   • Backend dev precisa ler tudo pra achar sua parte
   • Frontend dev idem
   • Difícil dividir entre times
   • Estimativas não separadas
```

### Com Split Multi-Spec ✅
```
📄 Spec 1: [Backend] API de Notificações Push
   └─ Focada só no backend
   
📄 Spec 2: [Frontend] Interface de Notificações
   └─ Focada só no frontend
   
📄 Spec 3: [Mobile] Push Notifications
   └─ Focada só no mobile

✅ Benefícios:
   • Cada time recebe só sua parte
   • Specs menores e focadas
   • Estimativas por repo
   • Fácil de paralelizar
   • Linking entre specs relacionadas
```

---

## 🎭 Comportamento por Perfil

### 👔 Usuário NÃO-TÉCNICO: Split AUTOMÁTICO

```
Usuário: "Quero adicionar login com Google no app"

Sistema detecta automaticamente:
├─ backend-api: OAuth2 endpoints, user creation
├─ frontend-web: botão "Login com Google", callback
└─ mobile-app: Google Sign-In SDK integration

┌─────────────────────────────────────────────────────────────┐
│ 🤖 IA (Automático):                                          │
│                                                               │
│ "Detectei que essa feature impacta 3 repositórios:          │
│                                                               │
│ ✓ Backend API      (OAuth2 + autenticação)                  │
│ ✓ Frontend Web     (botão de login + integração)            │
│ ✓ Mobile App       (Google Sign-In nativo)                  │
│                                                               │
│ Vou criar 3 documentos separados automaticamente:           │
│                                                               │
│ 📄 Task 1: [Backend] Implementar OAuth2 Google              │
│ 📄 Task 2: [Frontend] Adicionar Login com Google            │
│ 📄 Task 3: [Mobile] Integrar Google Sign-In                 │
│                                                               │
│ Todas as tasks estarão linkadas e sincronizadas."           │
│                                                               │
│ [✓ Prosseguir] [⚙️ Ajustar divisão]                         │
└─────────────────────────────────────────────────────────────┘
```

**Comportamento:**
- ✅ Sistema decide AUTOMATICAMENTE quais repos impactar
- ✅ Mostra aviso mas NÃO pede confirmação (a não ser que clique "Ajustar")
- ✅ Gera todas as specs automaticamente
- ✅ Explica em linguagem simples o que cada time fará

---

### 💻 Usuário TÉCNICO: Split MANUAL (com Sugestão)

```
Usuário: "Implementar cache Redis no SIGTAP service"

Sistema analisa e sugere:

┌─────────────────────────────────────────────────────────────┐
│ 🤖 IA (Sugestão):                                            │
│                                                               │
│ "Analisando impacto nos repositórios selecionados:          │
│                                                               │
│ 🎯 IMPACTO DETECTADO:                                        │
│                                                               │
│ ☑ Backend API (PRIMARY)                                     │
│    ├─ backend/services/sigtap_service.py (modificar)        │
│    ├─ backend/config.py (adicionar Redis config)            │
│    └─ docker-compose.yml (adicionar serviço Redis)          │
│    Complexidade: Alta | 3-5 dias                            │
│                                                               │
│ ☐ Frontend Dashboard (OPCIONAL)                             │
│    └─ src/api/sigtap.ts (sem mudanças necessárias)          │
│    └─ API é backwards compatible                            │
│    Complexidade: Nenhuma | 0 dias                           │
│                                                               │
│ RECOMENDAÇÃO: Criar spec apenas para Backend                │
│                                                               │
│ Quer split em múltiplas specs?                              │
│ ○ Não, spec única (recomendado - só backend impactado)      │
│ ○ Sim, criar specs separadas                                │
│ ○ Deixa eu escolher manualmente                             │
└─────────────────────────────────────────────────────────────┘
```

**Comportamento:**
- ✅ Sistema SUGERE divisão mas pergunta primeiro
- ✅ Mostra análise técnica detalhada de impacto
- ✅ Dá opção de ajustar manualmente
- ✅ Explica por que recomenda determinada divisão
- ✅ Permite override total

---

## 🔄 Fluxo Completo: Split Multi-Spec

### Exemplo: "Sistema de Rating de Médicos"

```
┌──────────────────────────────────────────────────────────────┐
│ PASSO 1: Usuário descreve feature                            │
└──────────────────────────────────────────────────────────────┘

Usuário (não-técnico):
"Quero que pacientes possam dar nota de 1 a 5 estrelas para 
os médicos depois de cada consulta"

Repos selecionados:
☑ backend-api
☑ frontend-dashboard  
☑ mobile-app


┌──────────────────────────────────────────────────────────────┐
│ PASSO 2: IA analisa impacto                                  │
└──────────────────────────────────────────────────────────────┘

[Analisando repositórios...]

🔍 Análise de Impacto:

Backend (backend-api):
├─ Precisa criar: Model Rating, API endpoints
├─ Precisa modificar: Doctor model (avg_rating)
└─ Escopo: Alta complexidade (validações, anti-fraude)

Frontend (frontend-dashboard):
├─ Precisa criar: Componente StarRating
├─ Precisa criar: Modal de avaliação
└─ Escopo: Média complexidade (UI + integração)

Mobile (mobile-app):
├─ Precisa criar: Tela de rating pós-consulta
├─ Precisa integrar: com API de ratings
└─ Escopo: Média complexidade (UI nativa)


┌──────────────────────────────────────────────────────────────┐
│ PASSO 3: IA propõe split (AUTOMÁTICO para não-técnico)       │
└──────────────────────────────────────────────────────────────┘

🤖 IA:
"Essa feature precisa de trabalho em 3 repositórios diferentes!

Vou criar 3 documentos separados:

📄 Task 1: [Backend] Sistema de Ratings de Médicos
   └─ Para: Time de Backend
   └─ Tempo: 3-4 dias
   └─ Prioridade: DEVE SER FEITO PRIMEIRO ⚠️

📄 Task 2: [Frontend] Interface de Avaliação
   └─ Para: Time de Frontend  
   └─ Tempo: 2 dias
   └─ Depende: Task 1 (precisa da API pronta)

📄 Task 3: [Mobile] Tela de Rating Pós-Consulta
   └─ Para: Time Mobile
   └─ Tempo: 2-3 dias  
   └─ Depende: Task 1 (precisa da API pronta)

[Continuar com 3 conversas separadas]"


┌──────────────────────────────────────────────────────────────┐
│ PASSO 4: Conversas paralelas                                 │
└──────────────────────────────────────────────────────────────┘

Sistema cria 3 TABS na interface:

┌────────────────────────────────────────────────────────────┐
│ [Backend 🔴] [Frontend 🟡] [Mobile 🟡]                      │
├────────────────────────────────────────────────────────────┤
│                                                              │
│ 💬 Conversando sobre: Backend                               │
│                                                              │
│ IA: "Para o backend, preciso saber:                         │
│      1. Como prevenir fraude (múltiplos ratings)?           │
│      2. Paciente pode editar rating depois?                 │
│      3. Rating é anônimo ou identificado?"                  │
│                                                              │
│ [Esta conversa é específica do backend]                     │
└────────────────────────────────────────────────────────────┘

Usuário pode:
├─ Responder na tab Backend
├─ Alternar para tab Frontend e responder lá
└─ Ou deixar IA preencher com defaults e revisar depois


┌──────────────────────────────────────────────────────────────┐
│ PASSO 5: IA mantém CONTEXTO COMPARTILHADO                    │
└──────────────────────────────────────────────────────────────┘

Se usuário define algo no Backend:
"Rating não pode ser editado após 24h"

IA automaticamente aplica no Frontend e Mobile:
"[✓] Aplicado em todas as specs: Rating locked após 24h"

SYNC automático de decisões comuns!


┌──────────────────────────────────────────────────────────────┐
│ PASSO 6: Preview simultâneo                                  │
└──────────────────────────────────────────────────────────────┘

Interface mostra 3 previews:

┌──────────────────┬──────────────────┬──────────────────┐
│ 📄 Backend Spec  │ 📄 Frontend Spec │ 📄 Mobile Spec   │
├──────────────────┼──────────────────┼──────────────────┤
│ ## Descrição     │ ## Descrição     │ ## Descrição     │
│ Implementar API  │ Criar interface  │ Tela de rating   │
│ de ratings...    │ de rating...     │ pós-consulta...  │
│                  │                  │                  │
│ ## Escopo        │ ## Escopo        │ ## Escopo        │
│ • Model Rating   │ • StarRating     │ • Native stars   │
│ • POST /ratings  │ • RatingModal    │ • Rating screen  │
│ • GET /ratings   │ • Integration    │ • API calls      │
│                  │                  │                  │
│ [90% completo]   │ [85% completo]   │ [80% completo]   │
└──────────────────┴──────────────────┴──────────────────┘


┌──────────────────────────────────────────────────────────────┐
│ PASSO 7: Export coordenado                                   │
└──────────────────────────────────────────────────────────────┘

[Modal de Export]

📦 Você tem 3 specs prontas!

Como quer exportar?

○ Separadas (3 arquivos .md)
   └─ ratings-backend.md
   └─ ratings-frontend.md  
   └─ ratings-mobile.md

○ Pacote ZIP
   └─ ratings-feature.zip
       ├─ backend.md
       ├─ frontend.md
       └─ mobile.md

○ GitHub Projects (criar 3 cards linkados)
   └─ Seleciona Project: [Backlog / Sprint Atual / Roadmap]
   └─ Card #1 [Backend] + Card #2 [Frontend] + Card #3 [Mobile]
   └─ Todos linkados com "Related to Card #1"

○ Monorepo (1 arquivo com seções)
   └─ ratings-feature.md (com 3 seções separadas)

[Exportar]
```

---

## 📋 Estrutura dos Documentos Gerados

### Cada spec inclui SEÇÃO DE LINKING:

```markdown
## 📌 Descrição / Contexto
Implementar sistema de ratings de médicos (1-5 estrelas)...

## 🔗 Tasks Relacionadas
⚠️ Esta feature faz parte de um conjunto de 3 tasks:

1. ✅ [Backend] Sistema de Ratings de Médicos (ESTA TASK)
   └─ Prioridade: P0 - DEVE SER IMPLEMENTADA PRIMEIRO
   └─ Repo: backend-api
   └─ Arquivo: ratings-backend.md

2. ⏳ [Frontend] Interface de Avaliação  
   └─ Depende: Task 1
   └─ Repo: frontend-dashboard
   └─ Arquivo: ratings-frontend.md

3. ⏳ [Mobile] Tela de Rating Pós-Consulta
   └─ Depende: Task 1
   └─ Repo: mobile-app
   └─ Arquivo: ratings-mobile.md

⚠️ IMPORTANTE: Backend DEVE ser implementado primeiro!

## 👤 User Story
Como paciente, quero dar nota para médicos...
[resto da spec normal]
```

---

## 🧠 Lógica de Detecção Automática

### Para Usuário NÃO-TÉCNICO (Automático)

```python
# Pseudo-código da lógica

if user.profile == "non-technical":
    # Busca contexto em todos repos selecionados
    impact = analyze_repos(feature_description)
    
    # Detecta quais repos precisam mudanças
    affected_repos = []
    for repo in selected_repos:
        changes = mcp_search(repo, feature_description)
        if changes.confidence > 0.7:  # 70% de confiança
            affected_repos.append(repo)
    
    # Se múltiplos repos impactados
    if len(affected_repos) > 1:
        # DECIDE AUTOMATICAMENTE fazer split
        show_notification(
            f"Detectei impacto em {len(affected_repos)} repositórios. "
            f"Vou criar {len(affected_repos)} documentos separados."
        )
        
        # Cria conversas paralelas (uma por repo)
        for repo in affected_repos:
            create_parallel_conversation(repo)
    
    # Usuário NÃO precisa confirmar, é automático!
```

### Para Usuário TÉCNICO (Manual com Sugestão)

```python
if user.profile == "technical":
    # Análise mais profunda
    impact = analyze_repos_detailed(feature_description)
    
    # Mostra análise completa
    show_impact_analysis(impact)
    
    # PERGUNTA ao usuário
    decision = ask_user(
        "Detectei impacto em múltiplos repos. "
        "Quer criar specs separadas?",
        options=[
            "Sim, criar specs separadas (recomendado)",
            "Não, manter spec única", 
            "Deixa eu escolher manualmente quais repos"
        ]
    )
    
    if decision == "manual":
        # Permite usuário marcar/desmarcar repos
        selected = show_repo_selector(affected_repos)
        affected_repos = selected
    
    elif decision == "single":
        affected_repos = [primary_repo]  # Spec única
    
    # Só cria split se usuário concordar
```

---

## 🎨 Interface Visual

### Indicador de Multi-Spec

```
┌─────────────────────────────────────────────────────────────┐
│ Context2Task                           👤 Tech Lead         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ ┌───────────────┐                                            │
│ │ REPOSITÓRIOS  │   🔄 Multi-Spec Mode: 3 repos impactados  │
│ ├───────────────┤                                            │
│ │ ☑ backend-api │   ┌─────────────────────────────────────┐│
│ │ ☑ frontend    │   │ [Backend 🔴] [Frontend 🟡] [Mobile] ││
│ │ ☑ mobile-app  │   ├─────────────────────────────────────┤│
│ └───────────────┘   │                                       ││
│                     │ 💬 Conversando sobre: Backend...      ││
│ 📊 STATUS           │                                       ││
│ ├─ Backend   90%    │ [Preview sendo construído]            ││
│ ├─ Frontend  85%    │                                       ││
│ └─ Mobile    80%    │                                       ││
└─────────────────────────────────────────────────────────────┘
```

### Navegação entre Specs

```
[Tabs com progresso visual]

┌────────┬────────┬────────┐
│Backend │Frontend│Mobile  │
│   🔴   │   🟡   │   ⚪   │
│  90%   │  85%   │  80%   │
└────────┴────────┴────────┘

🔴 = Completo e revisado
🟡 = Em progresso  
⚪ = Iniciado
```

---

## ✅ Regras de Negócio

### 1. Detecção de Impacto
- **Threshold de confiança**: 70% para incluir repo automaticamente
- **Análise de código**: Busca por imports, APIs, modelos compartilhados
- **Histórico**: Considera features similares passadas

### 2. Ordem de Implementação
- Sistema sugere automaticamente ordem baseada em dependências
- Backend geralmente vem primeiro (APIs)
- Frontend/Mobile dependem de backend estar pronto

### 3. Sincronização de Decisões
- Decisões comuns (regras de negócio) são sincronizadas
- Decisões técnicas específicas ficam isoladas por repo

### 4. Validação
```
ANTES DE EXPORTAR, sistema valida:

✓ Todas as specs têm mínimo 80% de completude
✓ Dependências entre specs estão mapeadas
✓ Não há contradições entre specs
✓ Estimativas de tempo são coerentes
```

---

## 📊 Métricas de Sucesso

- **Taxa de split correto**: > 90% dos splits são úteis
- **Redução de tamanho**: Specs individuais 60-70% menores que spec única
- **Satisfação**: Devs preferem specs separadas (target: 85%+)
- **Paralelização**: Aumentar em 40% o número de tasks trabalhadas em paralelo

---

## 🚀 Benefícios

### Para Não-Técnicos
✅ Não precisa entender arquitetura de repositórios
✅ Sistema decide automaticamente
✅ Recebe múltiplos documentos prontos para distribuir

### Para Técnicos  
✅ Controle fino sobre divisão
✅ Pode ajustar sugestões
✅ Entende impacto técnico detalhado

### Para Times de Dev
✅ Cada time recebe APENAS sua parte
✅ Specs focadas e menores
✅ Estimativas mais precisas
✅ Trabalho pode ser paralelizado

---

Essa feature transforma o Context2Task em uma ferramenta ainda mais poderosa! Quer que eu adicione mais algum detalhe ou ajuste algo?

