# Context2Task - Interface Final (V2 - Ajustada)

## 🎯 Ajustes Baseados em Feedback

### ✅ Mudanças Aplicadas

1. **Sidebar**: Dropdown para organizar (não abarrotar)
2. **Multi-Spec**: Seletor compacto (bem menorzinho)
3. **Preview MD**: SÓ NO FINAL (não side-by-side durante chat)
4. **Review Mode**: Página separada (após aprovar feature)

---

## 🖥️ INTERFACE FINAL SIMPLIFICADA

```
┌─────────────────────────────────────────────────────────────────┐
│ Context2Task                    [🎤 Voice] [👤] [⚙️]             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│ ┌──────────────┐  ┌───────────────────────────────────────────┐│
│ │ SIDEBAR      │  │ CHAT AREA (100% - Foco Total!)            ││
│ │ (Compacta)   │  │                                            ││
│ │              │  │ 💬 Conversa com IA                         ││
│ │ 📁 Repos ▼   │  │                                            ││
│ │ ☑ backend    │  │ IA: "Qual a prioridade desta feature?"    ││
│ │ ☑ frontend   │  │                                            ││
│ │ ☐ mobile     │  │ User: "Alta, sprint atual"                ││
│ │              │  │                                            ││
│ │ 🎯 Perfil ▼  │  │ IA: "Perfeito! Vou adicionar..."          ││
│ │ ● Técnico    │  │                                            ││
│ │              │  │                                            ││
│ │ 📑 Actions ▼ │  │ [Histórico de conversa scrollável]        ││
│ │ • Nova       │  │                                            ││
│ │ • Histórico  │  │                                            ││
│ │ • Templates  │  │                                            ││
│ │              │  │ ┌────────────────────────────────────────┐││
│ │ 🔢 Multi ▼   │  │ │ [🎤] Digite ou fale sua feature...     │││
│ │ Backend (90%)│  │ │ [Enviar →]                             │││
│ │ Frontend(85%)│  │ └────────────────────────────────────────┘││
│ │ Mobile (80%) │  │                                            ││
│ └──────────────┘  └───────────────────────────────────────────┘│
│                                                                   │
│ [Progress: 85% ████████▓░░░]    [💾 Auto-save: 2s ago]         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📐 COMPONENTES DETALHADOS

### 1. Sidebar Compacta (com Dropdowns)

```
┌──────────────────┐
│ 📁 Repositórios ▼│ ← Dropdown fechado
├──────────────────┤
│ 🎯 Perfil       ▼│
├──────────────────┤
│ 📑 Actions      ▼│
├──────────────────┤
│ 🔢 Multi-Spec   ▼│
└──────────────────┘

Quando clica [📁 Repositórios ▼]:
┌──────────────────┐
│ 📁 Repositórios ▲│ ← Dropdown expandido
├──────────────────┤
│ ☑ backend-api    │
│ ☑ frontend-web   │
│ ☐ mobile-app     │
│ ☐ shared-lib     │
├──────────────────┤
│ [+ Indexar Novo] │
└──────────────────┘

Quando clica [🎯 Perfil ▼]:
┌──────────────────┐
│ 🎯 Perfil       ▲│
├──────────────────┤
│ ● Técnico        │
│ ○ Não-técnico    │
└──────────────────┘

Quando clica [📑 Actions ▼]:
┌──────────────────┐
│ 📑 Actions      ▲│
├──────────────────┤
│ ✨ Nova Spec     │
│ 📋 Histórico     │
│ 📑 Templates     │
│ ⚙️ Configurações │
└──────────────────┘

Quando clica [🔢 Multi-Spec ▼]:
┌──────────────────┐
│ 🔢 Multi-Spec   ▲│
├──────────────────┤
│ [Backend] 90%    │
│ ████████▓░       │
│                  │
│ [Frontend] 85%   │
│ ████████░░       │
│                  │
│ [Mobile] 80%     │
│ ███████░░░       │
└──────────────────┘
```

**Vantagens**:
- ✅ Limpo e organizado
- ✅ Não abarrota visualmente
- ✅ Fácil de expandir/colapsar
- ✅ Mostra apenas o essencial

---

### 2. Multi-Spec Compacto (Bem Menorzinho)

**Opção A: Mini Tabs no Topo do Chat**
```
┌───────────────────────────────────────────────────────────┐
│ CHAT AREA                                                  │
├───────────────────────────────────────────────────────────┤
│ Specs: [Backend 🔴] [Frontend 🟡] [Mobile ⚪]  ← Tabs mini│
├───────────────────────────────────────────────────────────┤
│                                                            │
│ 💬 Conversando sobre: Backend                             │
│                                                            │
│ IA: "Para o backend, preciso saber..."                    │
└───────────────────────────────────────────────────────────┘
```

**Opção B: Dropdown no Input**
```
┌──────────────────────────────────────────────────┐
│ [Spec atual: Backend ▼] [🎤] Digite...          │
└──────────────────────────────────────────────────┘

Clica dropdown:
┌──────────────────┐
│ Spec atual      ▲│
├──────────────────┤
│ ● Backend (90%)  │
│ ○ Frontend (85%) │
│ ○ Mobile (80%)   │
└──────────────────┘
```

**Recomendação**: Opção A (mini tabs) é mais visual e fácil de alternar!

---

### 3. Preview MD - SÓ NO FINAL! 🎯

**Durante Conversa**: NÃO TEM PREVIEW
```
┌─────────────────────────────────────────────────────────┐
│ CHAT AREA (100% - Tela cheia!)                          │
│                                                           │
│ 💬 IA conversa normalmente...                            │
│                                                           │
│ [Sem preview, foco total na conversa]                    │
└─────────────────────────────────────────────────────────┘
```

**Ao Final da Conversa**: Botão aparece
```
┌─────────────────────────────────────────────────────────┐
│ ✅ Conversa Completa!                                    │
│                                                           │
│ Seu documento está pronto com 9/10 seções preenchidas.  │
│                                                           │
│ [👁️ Visualizar Documento MD] ← Botão aparece aqui      │
│                                                           │
│ [Continuar editando] [Análises opcionais ▼]             │
└─────────────────────────────────────────────────────────┘
```

**Quando Clica [👁️ Visualizar Documento MD]**:
```
┌─────────────────────────────────────────────────────────┐
│ 📄 Preview do Documento                    [✕ Fechar]   │
├─────────────────────────────────────────────────────────┤
│                                                           │
│ ## 📌 Descrição / Contexto                              │
│ Implementar sistema de notificações push via Firebase... │
│                                                           │
│ ## 👤 User Story                                         │
│ Como paciente, quero receber notificações...            │
│                                                           │
│ ## 📋 Resultado Esperado                                 │
│ - Backend configurado com Firebase                       │
│ - Endpoints de registro de devices                       │
│                                                           │
│ [... resto do documento scrollável ...]                  │
│                                                           │
├─────────────────────────────────────────────────────────┤
│ [✏️ Editar] [📥 Download] [📋 Copy] [🚀 Export]        │
└─────────────────────────────────────────────────────────┘
```

**Modal/Overlay fullscreen** com o MD renderizado!

---

### 4. Review Mode - Página Separada

**Fluxo**:
```
1. Spec completa
   ↓
2. [✅ Enviar para Aprovação]
   ↓
3. Redireciona para: /reviews/spec-123
   ↓
4. PÁGINA SEPARADA de Review
```

**Página de Review** (Rota diferente):
```
┌─────────────────────────────────────────────────────────┐
│ ← Voltar   📄 Review: Sistema de Notificações          │
├─────────────────────────────────────────────────────────┤
│                                                           │
│ 👥 Reviewers (3)                Status: 👀 In Review    │
│ ├─ @maria (Tech Lead)     ⏳ Pending                    │
│ ├─ @joao (Backend)        ✅ Approved                   │
│ └─ @pedro (Frontend)      💬 Commented                  │
│                                                           │
├─────────────────────────────────────────────────────────┤
│                                                           │
│ [Documento com comentários inline]                       │
│                                                           │
│ ## 📌 Descrição                                          │
│ Implementar sistema de...                                │
│                                                           │
│ 💬 @pedro (2h atrás): "E notificações de email?"        │
│    └─ [Responder] [Resolver]                            │
│                                                           │
├─────────────────────────────────────────────────────────┤
│ [✅ Aprovar] [❌ Rejeitar] [💬 Comentar]                │
└─────────────────────────────────────────────────────────┘
```

**Navegação**:
```
Main App: /
└─ Nova Spec: /new
└─ Histórico: /history
└─ Reviews: /reviews  ← Lista de specs em review
    └─ /reviews/123   ← Review específica (página separada!)
```

---

## 🔄 FLUXO COMPLETO ATUALIZADO

### Fluxo 1: Spec Simples (1 Repo)

```
1. Usuário abre Context2Task (/)
   
2. Sidebar: Seleciona [☑ backend]
   
3. [🎤] ou digita: "Adicionar cache Redis no SIGTAP"
   
4. CHAT 100% - Foco total na conversa
   ├─ IA faz perguntas
   ├─ Usuário responde
   └─ [Sem preview durante conversa!]
   
5. Conversa termina
   └─> "✅ Conversa Completa!"
   
6. Botões aparecem:
   ├─ [👁️ Visualizar Documento MD]
   ├─ [⚠️ Tech Debt] [🔒 Security] [📊 Diagram]
   └─ [📥 Download] [🚀 Export]
   
7. [👁️ Visualizar] → Modal fullscreen com MD
   
8. [📥 Download] → Baixa .md

FIM!
```

---

### Fluxo 2: Multi-Spec (3 Repos)

```
1. Sidebar: Seleciona 3 repos
   ☑ backend
   ☑ frontend
   ☑ mobile
   
2. Digita: "Sistema de Notificações Push"
   
3. IA detecta multi-spec:
   "Esta feature impacta 3 repositórios!
    Vou criar 3 documentos separados."
   
4. Mini tabs aparecem no topo do chat:
   [Backend 🔴] [Frontend 🟡] [Mobile ⚪]
   
5. Chat foca em [Backend] primeiro
   └─ Conversa específica do backend
   
6. Usuário alterna para [Frontend]
   └─ Chat muda para conversa do frontend
   
7. Sidebar mostra progresso:
   🔢 Multi-Spec ▼
   ├─ Backend: 90%
   ├─ Frontend: 85%
   └─ Mobile: 80%
   
8. Quando TODAS specs completas:
   "✅ 3 Specs Prontas!"
   
9. [👁️ Visualizar] mostra LISTA:
   ┌──────────────────────────┐
   │ 📄 Specs Geradas (3)     │
   ├──────────────────────────┤
   │ [Backend] 90%            │
   │ [Frontend] 85%           │
   │ [Mobile] 80%             │
   │                          │
   │ [Ver Backend]            │
   │ [Ver Frontend]           │
   │ [Ver Mobile]             │
   │ [Baixar Todas (.zip)]    │
   └──────────────────────────┘

FIM!
```

---

### Fluxo 3: Voice Input

```
1. Durante chat, clica [🎤]
   
2. Input expande verticalmente:
   ┌──────────────────────────────┐
   │ 🔴 Gravando... (00:45)       │
   │ ▁▂▃▅▆▇█ Waveform            │
   │                              │
   │ "Quero adicionar cache..."   │ ← Transcrição real-time
   │                              │
   │ [⏸️] [⏹️] [✅]              │
   └──────────────────────────────┘
   
3. Clica [✅ Confirmar]
   
4. Input volta ao normal
   
5. IA processa e responde

FIM!
```

---

### Fluxo 4: Com Review

```
1. Spec completa → [✅ Enviar para Aprovação]
   
2. Modal:
   ┌────────────────────────────┐
   │ Enviar para Review         │
   │                            │
   │ Reviewers:                 │
   │ [@maria] [@joao] [@pedro]  │
   │                            │
   │ [Enviar]                   │
   └────────────────────────────┘
   
3. Redireciona para: /reviews/123
   
4. PÁGINA SEPARADA de Review abre
   
5. Reviewers acessam /reviews/123
   
6. Comentam e aprovam
   
7. Quando aprovada, volta para main app

FIM!
```

---

## 🎨 COMPONENTES VISUAIS FINAIS

### Input com Voice

**Estado Normal**:
```
┌──────────────────────────────────────┐
│ [🎤] Digite ou fale sua feature...   │
│ [Enviar →]                           │
└──────────────────────────────────────┘
```

**Estado Gravando** (expande pra baixo):
```
┌──────────────────────────────────────┐
│ 🔴 Gravando... (00:45 / 05:00)       │
│ ▁▂▃▅▆▇█▇▆▅▃▂▁ Volume visual         │
│                                       │
│ 📝 Transcrição:                       │
│ "Quero adicionar um sistema de       │
│  notificações push para avisar..."   │
│                                       │
│ [⏸️ Pausar] [⏹️ Parar] [✅ OK]       │
└──────────────────────────────────────┘
```

---

### Análises Pré-Export

**Quando conversa termina**:
```
┌─────────────────────────────────────────────────┐
│ ✅ Documento Pronto! (9/10 seções)             │
├─────────────────────────────────────────────────┤
│                                                  │
│ 🔍 Análises Opcionais (Recomendamos!)          │
│                                                  │
│ [⚠️ Verificar Tech Debt]    ⏳ Não executado   │
│ [🔒 Security Checklist]     ⏳ Não executado   │
│ [📊 Gerar Diagrama Mermaid] ⏳ Não executado   │
│                                                  │
│ [🚀 Executar Todas] [⏭️ Pular]                 │
│                                                  │
├─────────────────────────────────────────────────┤
│ [👁️ Visualizar MD] [📥 Download] [📋 Copy]    │
└─────────────────────────────────────────────────┘
```

**Após executar análises**:
```
┌─────────────────────────────────────────────────┐
│ ✅ Análises Completas!                          │
├─────────────────────────────────────────────────┤
│                                                  │
│ [⚠️ Tech Debt]    ✅ 7 itens encontrados       │
│    └─> [Ver Detalhes]                           │
│                                                  │
│ [🔒 Security]     ⚠️ 3 alertas críticos        │
│    └─> [Ver Checklist]                          │
│                                                  │
│ [📊 Diagram]      ✅ Gerado com sucesso        │
│    └─> [Ver Diagrama]                           │
│                                                  │
├─────────────────────────────────────────────────┤
│ [👁️ Visualizar MD] [📥 Download] [📋 Copy]    │
└─────────────────────────────────────────────────┘
```

---

## 📊 RESUMO DAS MUDANÇAS

| Feature | Antes (complexo) | Agora (simplificado) |
|---------|------------------|---------------------|
| **Sidebar** | Tudo sempre visível | ✅ Dropdowns organizados |
| **Multi-Spec** | Tabs grandes | ✅ Mini tabs compactas ou dropdown |
| **Preview MD** | Side-by-side sempre | ✅ SÓ NO FINAL (modal) |
| **Review Mode** | Integrado | ✅ Página separada (/reviews) |
| **Chat** | Dividido com preview | ✅ 100% tela cheia durante conversa |
| **UX** | Complexo, muita coisa | ✅ Simples, focado, progressivo |

---

## ✅ VANTAGENS DA INTERFACE SIMPLIFICADA

1. **Foco Total no Chat** 🎯
   - 100% da tela para conversa
   - Sem distrações visuais
   - Preview só quando necessário

2. **Sidebar Organizada** 📂
   - Dropdowns evitam poluição
   - Tudo acessível mas não visível
   - Clean e profissional

3. **Multi-Spec Compacto** 🔢
   - Mini tabs não atrapalham
   - Progress na sidebar
   - Fácil alternar

4. **Preview Inteligente** 👁️
   - Aparece só quando faz sentido
   - Modal fullscreen = máxima legibilidade
   - Não divide atenção durante chat

5. **Review Separado** ✅
   - Workflow isolado e claro
   - Não confunde com criação
   - Página dedicada = melhor UX

---

## 🚀 PRÓXIMOS PASSOS

1. ✅ Interface simplificada aprovada
2. Criar wireframes no Figma
3. Protótipo clicável
4. Implementar com shadcn/ui

---

**Esta é a interface final otimizada! Simples, focada e escalável.** 🎨✨

