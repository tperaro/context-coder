# Context2Task - Fluxos de Usuário

## 🎬 Visão Geral da Interface

```
┌─────────────────────────────────────────────────────────────────┐
│  Context2Task                    [👤 Perfil] [⚙️ Config]         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌───────────────────┐  ┌─────────────────────────────────┐    │
│  │   SIDEBAR         │  │   CHAT AREA                      │    │
│  │                   │  │                                   │    │
│  │ 📁 Repositórios   │  │  💬 Conversa com AI              │    │
│  │ ☐ backend-api     │  │  📝 Preview do documento         │    │
│  │ ☐ frontend-app    │  │                                   │    │
│  │ ☐ shared-lib      │  │                                   │    │
│  │                   │  │                                   │    │
│  │ 📋 Histórico      │  │                                   │    │
│  │ • Task anterior 1 │  │                                   │    │
│  │ • Task anterior 2 │  │                                   │    │
│  │                   │  │                                   │    │
│  │ 🎯 Perfil         │  │  [Digite sua ideia de feature]   │    │
│  │ ○ Não-técnico    │  │  [Enviar] [Anexar código]         │    │
│  │ ● Técnico        │  │                                   │    │
│  └───────────────────┘  └─────────────────────────────────┘    │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Fluxo 1: Setup Inicial (Primeira Vez)

### Passo a Passo

```
1. Usuário abre Context2Task
   │
   ├─> [Tela de Boas-Vindas]
   │   "Bem-vindo ao Context2Task!"
   │   "Vamos configurar seus repositórios"
   │
2. Sistema mostra lista de repos disponíveis
   │
   ├─> [Lista de Repositórios Indexados]
   │   ☐ empresa/backend-multiagente (1.2M LOC, indexado)
   │   ☐ empresa/frontend-dashboard (450K LOC, indexado)
   │   ☐ empresa/shared-utils (80K LOC, indexado)
   │   [➕ Adicionar novo repositório]
   │
3. Usuário seleciona perfil
   │
   ├─> [Seleção de Perfil]
   │   ○ 🎨 Não-técnico (Product Owner)
   │   ○ 💻 Técnico (Developer/Tech Lead)
   │   
   │   Explicação:
   │   "Seu perfil ajusta a profundidade técnica
   │    das respostas e sugestões do assistente"
   │
4. Sistema está pronto
   │
   └─> [Dashboard Principal]
```

---

## 🚀 Fluxo 2: Criação de Task (Usuário Não-Técnico)

### Cenário: Sócio não-técnico quer criar feature de notificações

```
┌─────────────────────────────────────────────────────────────────┐
│ PASSO 1: Input Inicial                                           │
└─────────────────────────────────────────────────────────────────┘

Usuário digita:
"Quero adicionar notificações push no app quando houver uma nova 
mensagem do médico"

Sistema:
├─> Detecta perfil: Não-técnico
├─> Seleciona repos: backend-multiagente, frontend-dashboard
└─> Busca contexto relevante no MCP


┌─────────────────────────────────────────────────────────────────┐
│ PASSO 2: Enriquecimento Automático                               │
└─────────────────────────────────────────────────────────────────┘

[Loading] "Analisando contexto do código..."

Sistema faz automaticamente:
1. MCP search: "notification system push messages"
2. MCP search: "message handling doctor patient"
3. Encontra:
   ├─> backend/services/notification_service.py (já existe!)
   ├─> backend/models/message.py
   └─> frontend/components/NotificationCenter.tsx

[✓] Contexto encontrado: 3 arquivos relevantes


┌─────────────────────────────────────────────────────────────────┐
│ PASSO 3: Primeira Resposta do Assistente (Linguagem Simples)    │
└─────────────────────────────────────────────────────────────────┘

AI:
"Entendi! Você quer que os usuários recebam notificações quando 
médicos enviarem mensagens. 

Descobri que vocês JÁ TÊM um sistema de notificações! 
Isso facilita bastante. 

Algumas perguntas para entender melhor:

1. 📱 Tipo de Notificação
   - Notificação no navegador (quando app está aberto)?
   - Notificação push no celular (mesmo app fechado)?
   - Ambos?

2. 🔔 Quando notificar
   - Sempre que houver mensagem nova?
   - Só mensagens de certos tipos de médicos?
   - Apenas em horário específico?

3. 👥 Quem recebe
   - Todos os usuários?
   - Só pacientes ativos?
   - Configurável por usuário?

[Mostrar código] [Continuar sem detalhes]"


┌─────────────────────────────────────────────────────────────────┐
│ PASSO 4: Usuário Responde                                        │
└─────────────────────────────────────────────────────────────────┘

Usuário:
"Notificação push no celular, sempre que médico enviar mensagem,
todos os pacientes"

AI:
"Perfeito! Vou te mostrar 3 formas de fazer isso:

╔══════════════════════════════════════════════════════════════╗
║ OPÇÃO 1: Usar Serviço Externo (RECOMENDADO)                 ║
╠══════════════════════════════════════════════════════════════╣
║ ✅ Mais rápido de implementar (1-2 dias)                     ║
║ ✅ Confiável (99.9% uptime)                                  ║
║ ✅ Suporta iOS + Android automaticamente                     ║
║ ⚠️ Custo: ~$50/mês para 10k notificações                    ║
║                                                               ║
║ Serviços: Firebase Cloud Messaging (FCM) ou OneSignal       ║
╚══════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════╗
║ OPÇÃO 2: Integrar com Sistema Atual                         ║
╠══════════════════════════════════════════════════════════════╣
║ ✅ Sem custo adicional                                       ║
║ ✅ Controle total                                            ║
║ ⚠️ Mais trabalho (3-5 dias)                                  ║
║ ⚠️ Precisa configurar iOS e Android separadamente           ║
║                                                               ║
║ Modificar: backend/services/notification_service.py         ║
╚══════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════╗
║ OPÇÃO 3: Começar Simples (MVP)                              ║
╠══════════════════════════════════════════════════════════════╣
║ ✅ Rápido (1 dia)                                            ║
║ ✅ Valida se usuários realmente usam                         ║
║ ⚠️ Só funciona com app aberto                               ║
║                                                               ║
║ Usar: Web Notifications API (já suportado no código)        ║
╚══════════════════════════════════════════════════════════════╝

Qual opção faz mais sentido para vocês?"


┌─────────────────────────────────────────────────────────────────┐
│ PASSO 5: Iteração e Refinamento                                  │
└─────────────────────────────────────────────────────────────────┘

Usuário: "Opção 1, Firebase"

AI:
"Ótima escolha! Vou estruturar a task. 

Mais algumas perguntas rápidas:

🔐 Segurança e Privacidade
   - As mensagens podem conter dados sensíveis (diagnósticos)?
   - Devemos mostrar o CONTEÚDO da mensagem na notificação,
     ou só avisar "Você tem 1 nova mensagem"?

⏰ Prioridade
   - Essa feature é urgente (sprint atual)?
   - Ou pode esperar próxima sprint?

👨‍💻 Time
   - Vocês têm desenvolvedor com experiência em Firebase?
   - Ou prefere que eu detalhe mais na documentação?"


┌─────────────────────────────────────────────────────────────────┐
│ PASSO 6: Preview do Documento em Tempo Real                      │
└─────────────────────────────────────────────────────────────────┘

[Sidebar direita mostra preview sendo construído]

## 📌 Descrição / Contexto
Implementar notificações push mobile usando Firebase Cloud 
Messaging (FCM) para alertar pacientes quando médicos enviarem 
novas mensagens...

## 👤 User Story
Como paciente, quero receber notificações push no meu celular 
quando um médico me enviar mensagem, para que eu possa responder 
rapidamente...

[Preview continua se atualizando conforme conversa]


┌─────────────────────────────────────────────────────────────────┐
│ PASSO 7: Geração Final                                           │
└─────────────────────────────────────────────────────────────────┘

AI:
"Pronto! Sua task está completa. 

📊 Resumo:
   • Complexidade: Média (3-5 dias)
   • Arquivos impactados: 4 arquivos
   • Dependências: Firebase SDK, configuração iOS/Android
   • Custo estimado: $50/mês

[📥 Baixar .md] [📋 Copiar] [✏️ Editar] [🔄 Refazer]"
```

---

## 💻 Fluxo 3: Criação de Task (Usuário Técnico)

### Cenário: Dev Tech Lead quer criar feature de cache distribuído

```
┌─────────────────────────────────────────────────────────────────┐
│ PASSO 1: Input Inicial                                           │
└─────────────────────────────────────────────────────────────────┘

Usuário digita:
"Implementar cache distribuído Redis para reduzir latência nas 
queries do SIGTAP"

Sistema:
├─> Detecta perfil: Técnico
├─> Busca contexto: "SIGTAP queries database performance"
└─> Resposta com DETALHES TÉCNICOS


┌─────────────────────────────────────────────────────────────────┐
│ PASSO 2: Resposta Técnica Detalhada                              │
└─────────────────────────────────────────────────────────────────┘

AI:
"Analisando a base de código atual:

📁 Contexto Encontrado:
   backend/services/sigtap_service.py (linha 45-230)
   ├─> get_procedures(): 1.2s avg latency
   ├─> search_by_code(): 800ms avg
   └─> get_enriched_descriptions(): 2.1s avg

   backend/models/sigtap.py
   └─> Database: PostgreSQL 14.2, ~5M registros

🎯 Oportunidades de Cache Identificadas:

1. Query Patterns (últimas 1000 requests):
   • 67% - Buscas repetidas por código (alta cardinalidade)
   • 23% - Listagens paginadas (baixa cardinalidade)
   • 10% - Full-text search (dinâmica)

2. Arquitetura Atual:
   ┌─────────┐     ┌──────────┐     ┌────────────┐
   │ FastAPI │────▶│PostgreSQL│────▶│   SIGTAP   │
   └─────────┘     └──────────┘     └────────────┘
                      1.2s avg          5M rows

⚠️ DECISÕES TÉCNICAS CRÍTICAS:

╔══════════════════════════════════════════════════════════════╗
║ OPÇÃO A: Redis + Cache-Aside Pattern                        ║
╠══════════════════════════════════════════════════════════════╣
║ Arquitetura:                                                 ║
║    ┌────────┐    ┌────────┐    ┌──────────┐               ║
║    │FastAPI │───▶│ Redis  │───▶│PostgreSQL │              ║
║    └────────┘    └────────┘    └──────────┘               ║
║       │              │                                       ║
║       └──────Cache Miss────────┘                           ║
║                                                              ║
║ ✅ Pros:                                                     ║
║   • Controle fino do que cachear                            ║
║   • Fallback automático se Redis cair                       ║
║   • Latência: ~5-10ms (vs 1200ms)                          ║
║                                                              ║
║ ⚠️ Contras:                                                  ║
║   • Invalidação manual necessária                           ║
║   • Cache stampede em cold start                            ║
║   • Código mais complexo                                    ║
║                                                              ║
║ 📝 Implementação:                                            ║
║   • redis-py + async support                                ║
║   • TTL: 1h para procedures, 5min para search              ║
║   • Serialização: JSON ou MessagePack                       ║
╚══════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════╗
║ OPÇÃO B: Redis + Read-Through Pattern                       ║
╠══════════════════════════════════════════════════════════════╣
║ ✅ Pros:                                                     ║
║   • Código mais simples (abstração)                         ║
║   • Cache population automático                             ║
║                                                              ║
║ ⚠️ Contras:                                                  ║
║   • Menos flexível                                          ║
║   • Performance hit no primeiro acesso                      ║
║   • Lock contention em queries populares                    ║
╚══════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════╗
║ OPÇÃO C: PostgreSQL + pg_prewarm (Hybrid)                   ║
╠══════════════════════════════════════════════════════════════╣
║ ✅ Pros:                                                     ║
║   • Zero código novo                                        ║
║   • Sem Redis (menos infra)                                 ║
║   • Latência: ~50-100ms (vs 1200ms)                        ║
║                                                              ║
║ ⚠️ Contras:                                                  ║
║   • Ainda dependente do DB                                  ║
║   • Não escalável horizontalmente                           ║
║   • Ganho menor (~10x vs ~200x com Redis)                  ║
╚══════════════════════════════════════════════════════════════╝

🔍 ANÁLISE DE IMPACTO:

Arquivos que DEVEM ser modificados:
1. backend/services/sigtap_service.py
   └─> Adicionar cache layer (50-80 LOC)

2. backend/config.py
   └─> Redis connection config (10-15 LOC)

3. backend/dependencies.py
   └─> Redis dependency injection (20 LOC)

4. docker-compose.yml
   └─> Adicionar serviço Redis

Arquivos OPCIONAIS (se quiser invalidação):
5. backend/api/admin/sigtap.py
   └─> Endpoints de invalidação manual

⚡ PERFORMANCE ESTIMADA:

                 Atual    Cache-Aside    Improvement
get_procedures    1.2s       5-10ms        120-240x
search_by_code   800ms       5-10ms        80-160x
full_text         2.1s      100-200ms      10-20x (partial)

💰 CUSTOS:
• Redis Cloud: $0 (free tier até 30MB) ou $5/mês (250MB)
• Development: 3-5 dias (c/ testes e monitoring)
• Ops overhead: Minimal (Redis é stateless-ish)

🚨 RISCOS:

1. Cache Inconsistency
   └─> Mitigação: TTL curto + invalidação on-demand

2. Redis Single Point of Failure
   └─> Mitigação: Fallback to DB se Redis falhar

3. Memory Eviction
   └─> Mitigação: LRU policy + monitoring de hit rate

Qual arquitetura prefere? Posso detalhar mais qualquer uma."
```

---

## 🔀 Fluxo 4: Multi-Repositório

### Cenário: Feature que impacta múltiplos repos

```
┌─────────────────────────────────────────────────────────────────┐
│ SELEÇÃO DE REPOSITÓRIOS                                          │
└─────────────────────────────────────────────────────────────────┘

Usuário quer criar: "API de autenticação unificada"

[Sidebar - Seleção de Repos]
☑ backend-api (principal)
☑ frontend-dashboard (usa a API)
☑ mobile-app (também usa)
☐ data-pipeline (não relevante)

Sistema:
├─> Busca em TODOS repos selecionados simultaneamente
├─> Encontra código de auth em cada um
└─> Identifica inconsistências entre repos!


AI:
"⚠️ ATENÇÃO: Detectei 3 implementações DIFERENTES de auth:

1. backend-api: JWT com refresh tokens (padrão atual)
   └─> backend/auth/jwt_handler.py

2. frontend-dashboard: Session-based auth (legacy!)
   └─> src/utils/auth.ts (usando cookies)

3. mobile-app: OAuth2 + JWT (correto)
   └─> lib/services/auth_service.dart

💡 RECOMENDAÇÃO:
Antes de criar API unificada, vocês têm uma dívida técnica:
O frontend está usando autenticação antiga!

Sugestão: Incluir migração do frontend na task?
[✓] Sim, incluir migração
[ ] Não, criar task separada
[ ] Ignorar por enquanto"
```

---

## 📝 Fluxo 5: Visualização de Código Relevante

```
┌─────────────────────────────────────────────────────────────────┐
│ EXPANDIR CONTEXTO DE CÓDIGO                                      │
└─────────────────────────────────────────────────────────────────┘

Durante conversa, AI menciona:
"Encontrei notification_service.py que já implementa parte disso"

[Botão: 👁️ Mostrar código]

Usuario clica ▼

┌───────────────────────────────────────────────────────┐
│ 📄 backend/services/notification_service.py           │
│ Linhas 45-78 (relevância: 92%)                        │
├───────────────────────────────────────────────────────┤
│                                                        │
│  45 │ class NotificationService:                      │
│  46 │     def __init__(self, db: Database):           │
│  47 │         self.db = db                            │
│  48 │         self.providers = []                     │
│  49 │                                                  │
│  50 │     async def send_notification(              │
│  51 │         user_id: str,                          │
│  52 │         message: str,                          │
│  53 │         type: NotificationType                 │
│  54 │     ):                                         │
│  55 │         """Send notification to user"""        │
│  56 │         # TODO: Add push notification support  │ ← RELEVANTE!
│  57 │         await self._send_email(user_id,...)    │
│  58 │                                                  │
│  ...                                                   │
│                                                        │
│ [📋 Copiar] [🔗 Abrir no GitHub] [💬 Discutir]      │
└───────────────────────────────────────────────────────┘

AI:
"Viu a linha 56? Já tem um TODO exatamente para isso! 
Vamos aproveitar essa estrutura."
```

---

## 📊 Fluxo 6: Preview e Export

```
┌─────────────────────────────────────────────────────────────────┐
│ PREVIEW EM TEMPO REAL                                            │
└─────────────────────────────────────────────────────────────────┘

[Split View - 50% Chat / 50% Preview]

Chat (esquerda):              Preview (direita):
┌──────────────────────┐     ┌────────────────────────┐
│ AI: "Qual prioridade?"│     │ ## 📌 Descrição        │
│                       │     │ Implementar sistema... │
│ User: "Alta, sprint   │     │                         │
│ atual"                │     │ ## 👤 User Story       │
│                       │ ───▶│ Como paciente...       │
│ AI: "Entendido..."    │     │ [AUTO-UPDATING]        │
│                       │     │                         │
│                       │     │ ## ⚙️ Detalhes          │
│                       │     │ 1. Configurar Firebase │
│                       │     │ 2. Modificar backend.. │
└──────────────────────┘     └────────────────────────┘

[Botão flutuante no preview]
✓ Documento Completo (8/10 seções preenchidas)
[📥 Baixar] [📋 Copiar] [✏️ Editar Manualmente]
```

---

## 🎯 Fluxo 7: Finalização

```
┌─────────────────────────────────────────────────────────────────┐
│ OPÇÕES DE EXPORT                                                 │
└─────────────────────────────────────────────────────────────────┘

[Modal de Export]

📄 Formato
   ● Markdown (.md) - Para GitHub Projects
   ○ JSON - Para APIs/automação
   ○ YAML - Para GitLab/Jira

🎨 Template
   ● Formato da Empresa (padrão)
   ○ Formato Técnico Detalhado
   ○ Formato Executivo Resumido

🏷️ Metadados
   Priority: [High ▼]
   Labels: [feature] [backend] [firebase]
   Assignee: [Selecionar dev ▼]
   Sprint: [Sprint 23 ▼]

🎯 GitHub Project (se selecionado)
   Project: [Backlog ▼]
   ○ Backlog
   ○ Sprint Atual
   ○ Roadmap

[Cancelar] [📥 Baixar] [📋 Copiar] [🚀 Criar Card no GitHub Project]
```

---

## 🔄 Funcionalidades Adicionais

### 1. **Histórico de Conversas**
```
[Sidebar]
📋 Tarefas Anteriores
├─ 🟢 Push Notifications (completa)
│  └─ Criada há 2 dias, por João
├─ 🟡 Redis Cache (em edição)
│  └─ Criada há 1 hora, por você
└─ 🔴 Auth API (rascunho)
   └─ Criada há 5 min, por você

[Click em qualquer uma retoma conversa]
```

### 2. **Sugestões Proativas**
```
AI (durante conversa):
"💡 Lembrete: Vocês têm uma task similar de 2 meses atrás:
'Email Notifications' que também usou o notification_service.py

Quer que eu busque detalhes de como foi implementada?"
[Ver Task Anterior] [Ignorar]
```

### 3. **Validação Pré-Export**
```
⚠️ Checklist Antes de Finalizar:

☑ Descrição clara
☑ User story definida
☑ Critérios de aceite
☐ Riscos identificados (recomendado)
☐ Links de referência (opcional)

[Finalizar Mesmo Assim] [Completar Checklist]
```

---

## 🎨 Diferenças por Perfil

### Perfil NÃO-TÉCNICO
- ✅ Linguagem simples, sem jargões
- ✅ Analogias e exemplos do dia-a-dia
- ✅ Foco em benefícios de negócio
- ✅ Esconde detalhes de implementação (mostra se pedir)
- ✅ Estimativas em dias, não story points

### Perfil TÉCNICO
- ✅ Termos técnicos precisos
- ✅ Arquitetura e padrões de design
- ✅ Tradeoffs técnicos detalhados
- ✅ Performance metrics
- ✅ Trechos de código relevantes inline
- ✅ Análise de complexidade

---

## 🚀 Resumo das Funcionalidades

1. ✅ **Seleção Multi-Repo**: Combina contexto de vários projetos
2. ✅ **Chat Contextual**: IA busca código relevante automaticamente
3. ✅ **Perfis Adaptativos**: Linguagem técnica ou simples
4. ✅ **Análise de Tradeoffs**: Múltiplas opções com prós/contras
5. ✅ **Preview em Tempo Real**: Vê documento sendo construído
6. ✅ **Detecção de Código**: Encontra implementações existentes
7. ✅ **Sugestões Proativas**: IA sugere melhorias baseadas no contexto
8. ✅ **Export Flexível**: .md, JSON, YAML, direto para GitHub Projects
9. ✅ **Histórico**: Retoma conversas anteriores
10. ✅ **Validação**: Checklists antes de finalizar
11. ✅ **Split Multi-Spec**: Gera spec separada por repositório automaticamente

---

Esses são os fluxos principais! Quer que eu detalhe mais algum? Ou ajustar alguma parte?

