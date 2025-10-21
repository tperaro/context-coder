# Context2Task - Diagrama de Fluxo do Sistema

## 🎯 Visão Geral

Este documento contém os diagramas Mermaid que representam toda a arquitetura e fluxos da plataforma Context2Task.

### 📑 Índice de Diagramas

1. **Casos de Uso Principais** - Visão geral de usuários, features e integrações
2. **Fluxo Completo de Criação de Spec** - Do input até export final
3. **Arquitetura Técnica** - Stack e componentes do sistema
4. **Fluxo Multi-Spec** - Feature que impacta múltiplos repositórios
5. **Voice Input Flow** - Sequência de gravação e transcrição
6. **Security & Tech Debt Analysis** - Análises opcionais pré-export
7. **Review Mode Workflow** - Estados de aprovação
8. **Data Flow & Integration** - Fluxo de dados entre componentes
9. **Casos de Uso por Perfil** - Separado por técnico vs não-técnico
10. **Tech Debt Detector Inteligente** 🧠 **NOVO** - Análise via IA (não grep/regex)
11. **GitHub Projects Integration** ⭐ **NOVO** - Export para GitHub Projects (não Issues)

---

## 📊 Diagrama 1: Casos de Uso Principais

```mermaid
graph TB
    subgraph "Usuários"
        NT[👔 Não-Técnico<br/>Product Owner]
        TEC[💻 Técnico<br/>Tech Lead/Dev]
    end
    
    subgraph "Context2Task Platform"
        subgraph "Core Features"
            SEL[📁 Seleção Multi-Repo]
            CHAT[💬 Chat Contextual]
            VOICE[🎤 Voice Input]
            AI[🤖 AI Assistant<br/>Gemini 2.5 Pro]
            PREVIEW[👁️ Preview MD]
        end
        
        subgraph "Analysis Features"
            TD[⚠️ Tech Debt Detector]
            SEC[🔒 Security Checklist]
            DIAG[📊 Mermaid Diagrams]
        end
        
        subgraph "Collaboration"
            REV[✅ Review Mode]
            TEMP[📑 Templates]
            MULTI[🔢 Multi-Spec Generator]
        end
        
        subgraph "Export"
            DOWN[📥 Download MD]
            COPY[📋 Copy]
            GH[🚀 GitHub Projects Card]
        end
    end
    
    subgraph "Integrations"
        MCP[🔍 MCP claude-context<br/>Zilliz Cloud + OpenAI]
        LLM[🧠 OpenRouter API<br/>Gemini 2.5 Pro]
        REPOS[📦 Repositories<br/>Backend/Frontend/Mobile]
    end
    
    NT -->|"Descreve feature<br/>(linguagem simples)"| SEL
    TEC -->|"Descreve feature<br/>(linguagem técnica)"| SEL
    
    SEL --> CHAT
    VOICE -->|"Transcrição"| CHAT
    CHAT --> AI
    
    AI <-->|"Busca contexto"| MCP
    AI <-->|"Gera respostas"| LLM
    MCP <--> REPOS
    
    AI --> PREVIEW
    PREVIEW --> TD
    PREVIEW --> SEC
    PREVIEW --> DIAG
    
    TD --> MULTI
    SEC --> MULTI
    DIAG --> MULTI
    
    MULTI -->|"1 ou N specs"| DOWN
    MULTI --> COPY
    MULTI --> GH
    
    DOWN --> REV
    COPY --> REV
    REV --> TEMP
    
    style NT fill:#e1f5ff
    style TEC fill:#ffe1f5
    style AI fill:#fff4e1
    style MULTI fill:#e1ffe1
```

---

## 🔄 Diagrama 2: Fluxo Completo de Criação de Spec

```mermaid
flowchart TD
    START([👤 Usuário Acessa]) --> PROFILE{Seleciona Perfil}
    
    PROFILE -->|Não-Técnico| NT_MODE[🎨 Modo Simplificado]
    PROFILE -->|Técnico| TEC_MODE[💻 Modo Detalhado]
    
    NT_MODE --> SEL_REPO[📁 Seleciona Repositórios]
    TEC_MODE --> SEL_REPO
    
    SEL_REPO --> INPUT_METHOD{Como descrever?}
    
    INPUT_METHOD -->|Texto| TEXT_INPUT[⌨️ Digita Feature]
    INPUT_METHOD -->|Voz| VOICE_INPUT[🎤 Grava Áudio]
    
    VOICE_INPUT -->|Whisper API| TRANSCRIBE[📝 Transcrição]
    TRANSCRIBE --> TEXT_INPUT
    
    TEXT_INPUT --> MCP_SEARCH[🔍 Busca Contexto MCP]
    
    MCP_SEARCH --> ANALYZE{Quantos repos<br/>impactados?}
    
    ANALYZE -->|1 Repo| SINGLE_CHAT[💬 Chat Single]
    ANALYZE -->|2+ Repos| MULTI_DETECT{Perfil?}
    
    MULTI_DETECT -->|Não-Técnico| AUTO_SPLIT[🤖 Split Automático]
    MULTI_DETECT -->|Técnico| MANUAL_SPLIT[⚙️ Split Manual]
    
    AUTO_SPLIT --> MULTI_CHAT[💬 Chat Multi-Repo<br/>Mini Tabs]
    MANUAL_SPLIT --> MULTI_CHAT
    
    SINGLE_CHAT --> AI_CONV[🤖 Conversa IA]
    MULTI_CHAT --> AI_CONV
    
    AI_CONV -->|"Perguntas<br/>Tradeoffs<br/>Refinamento"| ITERATE{Continuar<br/>refinando?}
    
    ITERATE -->|Sim| AI_CONV
    ITERATE -->|Não| PREVIEW_READY[👁️ Preview Pronto]
    
    PREVIEW_READY --> OPTIONAL{Análises<br/>Opcionais?}
    
    OPTIONAL -->|Sim| RUN_ANALYSIS[⚡ Executar Análises]
    OPTIONAL -->|Não| EXPORT_READY
    
    RUN_ANALYSIS --> TD_CHECK[⚠️ Tech Debt]
    RUN_ANALYSIS --> SEC_CHECK[🔒 Security]
    RUN_ANALYSIS --> DIAG_GEN[📊 Diagrams]
    
    TD_CHECK --> ANALYSIS_DONE[✅ Análises Completas]
    SEC_CHECK --> ANALYSIS_DONE
    DIAG_GEN --> ANALYSIS_DONE
    
    ANALYSIS_DONE --> ADD_TO_SPEC{Adicionar<br/>à spec?}
    
    ADD_TO_SPEC -->|Sim| UPDATE_SPEC[📝 Atualiza Documento]
    ADD_TO_SPEC -->|Não| EXPORT_READY
    UPDATE_SPEC --> EXPORT_READY
    
    EXPORT_READY[📄 Documento Final] --> EXPORT_CHOICE{Como exportar?}
    
    EXPORT_CHOICE -->|Download| DOWNLOAD[📥 Baixar .md]
    EXPORT_CHOICE -->|Copy| CLIPBOARD[📋 Copiar]
    EXPORT_CHOICE -->|Review| REVIEW_MODE[✅ Enviar p/ Review]
    EXPORT_CHOICE -->|GitHub| GITHUB_PROJECT[🚀 Criar Card no Project]
    
    GITHUB_PROJECT --> SELECT_PROJECT{Qual Project?}
    SELECT_PROJECT -->|Backlog| CREATE_BACKLOG[📋 Card no Backlog]
    SELECT_PROJECT -->|Sprint Atual| CREATE_SPRINT[⚡ Card no Sprint]
    SELECT_PROJECT -->|Roadmap| CREATE_ROADMAP[🗺️ Card no Roadmap]
    
    CREATE_BACKLOG --> GITHUB_DONE[✅ Card criado]
    CREATE_SPRINT --> GITHUB_DONE
    CREATE_ROADMAP --> GITHUB_DONE
    
    REVIEW_MODE --> ASSIGN[👥 Assign Reviewers]
    ASSIGN --> NOTIFY[📧 Notificar]
    NOTIFY --> FEEDBACK_LOOP{Aprovado?}
    
    FEEDBACK_LOOP -->|Comentários| AI_CONV
    FEEDBACK_LOOP -->|Aprovado| DOWNLOAD
    FEEDBACK_LOOP -->|Rejeitado| AI_CONV
    
    DOWNLOAD --> END([✅ Concluído])
    CLIPBOARD --> END
    GITHUB_DONE --> END
    
    style START fill:#e1f5ff
    style END fill:#e1ffe1
    style AUTO_SPLIT fill:#ffe1e1
    style MANUAL_SPLIT fill:#fff4e1
    style EXPORT_READY fill:#f0e1ff
```

---

## 🏗️ Diagrama 3: Arquitetura Técnica

```mermaid
graph TB
    subgraph "Frontend Container"
        UI[React + TypeScript<br/>shadcn/ui + Tailwind]
        COMP[Components]
        STATE[State Management]
        UI --> COMP
        COMP --> STATE
    end
    
    subgraph "Backend Container"
        API[FastAPI<br/>Python 3.10+]
        MCP_CLIENT[MCP Client<br/>Stdio/Subprocess]
        CACHE[In-Memory Cache<br/>Sessions]
        
        API --> MCP_CLIENT
        API --> CACHE
    end
    
    subgraph "External Services"
        OR[OpenRouter API<br/>Gemini 2.5 Pro]
        MCP_SERVER[claude-context MCP<br/>npx @zilliz/claude-context-mcp]
        ZILLIZ[Zilliz Cloud<br/>Milvus Serverless]
        OAI[OpenAI API<br/>Embeddings]
        
        MCP_SERVER --> ZILLIZ
        MCP_SERVER --> OAI
    end
    
    subgraph "Repositories"
        BE[Backend Repo]
        FE[Frontend Repo]
        MOB[Mobile Repo]
    end
    
    UI <-->|HTTP/WS| API
    API <-->|REST| OR
    MCP_CLIENT <-->|Stdio/JSON-RPC| MCP_SERVER
    
    MCP_SERVER <-->|Index/Search| BE
    MCP_SERVER <-->|Index/Search| FE
    MCP_SERVER <-->|Index/Search| MOB
    
    ZILLIZ -.->|Vector Search| MCP_SERVER
    OAI -.->|Generate Embeddings| MCP_SERVER
    
    style UI fill:#61dafb
    style API fill:#009688
    style OR fill:#ff6b6b
    style MCP_SERVER fill:#4ecdc4
    style ZILLIZ fill:#95e1d3
```

---

## 🎭 Diagrama 4: Fluxo Multi-Spec (Feature Complexa)

```mermaid
flowchart TD
    START([Feature: Push Notifications]) --> DETECT[🔍 IA Detecta Impacto]
    
    DETECT --> SCAN_REPOS{Escaneia<br/>Repositórios}
    
    SCAN_REPOS -->|Backend| BE_IMPACT[✅ Backend<br/>90% impacto]
    SCAN_REPOS -->|Frontend| FE_IMPACT[✅ Frontend<br/>85% impacto]
    SCAN_REPOS -->|Mobile| MOB_IMPACT[✅ Mobile<br/>80% impacto]
    
    BE_IMPACT --> COUNT{Quantos repos<br/>impactados?}
    FE_IMPACT --> COUNT
    MOB_IMPACT --> COUNT
    
    COUNT -->|3 repos| PROFILE_CHECK{Perfil?}
    
    PROFILE_CHECK -->|Não-Técnico| AUTO_MSG["🤖 Detectei impacto em 3 repos!<br/>Vou criar 3 specs automaticamente"]
    PROFILE_CHECK -->|Técnico| MANUAL_MSG["💻 Detectei impacto em 3 repos.<br/>Deseja criar specs separadas?"]
    
    AUTO_MSG --> CREATE_TABS
    MANUAL_MSG --> USER_CHOICE{Usuário<br/>confirma?}
    
    USER_CHOICE -->|Sim| CREATE_TABS
    USER_CHOICE -->|Não| SINGLE_SPEC[📄 Spec Única]
    
    CREATE_TABS[📑 Cria 3 Tabs] --> TAB_BE[Backend 🔴]
    CREATE_TABS --> TAB_FE[Frontend 🟡]
    CREATE_TABS --> TAB_MOB[Mobile ⚪]
    
    TAB_BE --> CONV_BE[💬 Conversa Backend]
    TAB_FE --> CONV_FE[💬 Conversa Frontend]
    TAB_MOB --> CONV_MOB[💬 Conversa Mobile]
    
    CONV_BE -->|"API endpoints<br/>Firebase SDK<br/>Workers"| SPEC_BE[📄 Spec Backend]
    CONV_FE -->|"UI components<br/>SDK integration<br/>Permissions"| SPEC_FE[📄 Spec Frontend]
    CONV_MOB -->|"Native SDK<br/>Push handlers"| SPEC_MOB[📄 Spec Mobile]
    
    SPEC_BE --> LINK{Linkar specs?}
    SPEC_FE --> LINK
    SPEC_MOB --> LINK
    
    LINK -->|Sim| ADD_REFS[🔗 Adiciona Seção<br/>'Tasks Relacionadas']
    
    ADD_REFS --> FINAL_BE[📄 Backend Spec Final<br/>+ Links para FE/MOB]
    ADD_REFS --> FINAL_FE[📄 Frontend Spec Final<br/>+ Links para BE/MOB]
    ADD_REFS --> FINAL_MOB[📄 Mobile Spec Final<br/>+ Links para BE/FE]
    
    FINAL_BE --> EXPORT_MULTI{Como exportar<br/>3 specs?}
    FINAL_FE --> EXPORT_MULTI
    FINAL_MOB --> EXPORT_MULTI
    
    EXPORT_MULTI -->|Separadas| THREE_FILES[3 arquivos .md]
    EXPORT_MULTI -->|ZIP| ZIP_FILE[arquivo .zip]
    EXPORT_MULTI -->|GitHub| THREE_CARDS[3 cards linkados<br/>no GitHub Project]
    
    THREE_FILES --> END([✅ Concluído])
    ZIP_FILE --> END
    THREE_CARDS --> END
    SINGLE_SPEC --> END
    
    style AUTO_MSG fill:#e1ffe1
    style MANUAL_MSG fill:#ffe1e1
    style FINAL_BE fill:#bbdefb
    style FINAL_FE fill:#c8e6c9
    style FINAL_MOB fill:#fff9c4
```

---

## 🎤 Diagrama 5: Voice Input Flow

```mermaid
sequenceDiagram
    actor User
    participant UI as Frontend UI
    participant Voice as Voice Module
    participant Whisper as Whisper API
    participant AI as AI Assistant
    participant Chat as Chat Engine
    
    User->>UI: Clica 🎤
    UI->>Voice: Inicia gravação
    Voice-->>UI: Pede permissão mic
    User->>Voice: Concede permissão
    
    Voice->>Voice: 🔴 Gravando...
    Voice-->>UI: Mostra waveform
    Voice-->>UI: Timer (00:45)
    
    loop Transcrição Real-time (opcional)
        Voice->>Whisper: Stream de áudio
        Whisper-->>Voice: Texto parcial
        Voice-->>UI: Atualiza transcrição
    end
    
    User->>UI: Clica ⏹️ Parar
    Voice->>Whisper: Áudio completo
    Whisper->>Whisper: Processa
    Whisper-->>Voice: Transcrição final
    
    Voice->>Voice: Remove filler words
    Voice-->>UI: Texto limpo
    
    User->>UI: Clica ✅ Confirmar
    UI->>AI: Envia texto
    AI->>Chat: Processa feature
    Chat-->>AI: Contexto + análise
    AI-->>UI: Resposta estruturada
    
    UI-->>User: Mostra resultado
```

---

## 🔒 Diagrama 6: Security & Tech Debt Analysis Flow

```mermaid
flowchart TD
    START[📄 Spec 90% Completa] --> PRE_EXPORT{Antes de exportar}
    
    PRE_EXPORT --> SHOW_OPTIONS["🔍 Análises Opcionais:<br/>⚠️ Tech Debt<br/>🔒 Security<br/>📊 Diagrams"]
    
    SHOW_OPTIONS --> USER_SELECT{Usuário<br/>seleciona?}
    
    USER_SELECT -->|Tech Debt| TD_START[⚠️ Inicia Tech Debt]
    USER_SELECT -->|Security| SEC_START[🔒 Inicia Security]
    USER_SELECT -->|Diagrams| DIAG_START[📊 Inicia Diagrams]
    USER_SELECT -->|Pular| SKIP_TO_EXPORT
    
    TD_START --> TD_CONTEXT[🔍 MCP Busca<br/>Contexto Relacionado]
    TD_CONTEXT --> TD_AI_PROMPT["🤖 IA Analisa com<br/>Prompt Especializado:<br/>- Code smells<br/>- Duplicação<br/>- Complexidade<br/>- Anti-patterns<br/>- Performance issues<br/>- Acoplamento<br/>- Falta de testes"]
    TD_AI_PROMPT --> TD_AI_ANALYSIS[Gemini 2.5 Pro<br/>Analisa Código]
    TD_AI_ANALYSIS --> TD_RESULTS{Encontrou<br/>problemas?}
    
    TD_RESULTS -->|Sim| TD_SHOW["Mostra Relatório:<br/>🔴 3 críticos<br/>🟡 5 médios<br/>🟢 2 sugestões"]
    TD_RESULTS -->|Não| TD_EMPTY[✅ Código saudável<br/>Sem tech debt detectado]
    
    TD_SHOW --> TD_ACTION{Adicionar<br/>à spec?}
    TD_ACTION -->|Sim| TD_UPDATE[Atualiza Spec]
    TD_ACTION -->|Não| TD_DONE
    
    SEC_START --> SEC_RULES[Carrega Regras<br/>da Empresa]
    SEC_RULES --> SEC_CHECK_LGPD{Dados<br/>Sensíveis?}
    
    SEC_CHECK_LGPD -->|Sim| SEC_LGPD["🚨 Alerta LGPD:<br/>- Consentimento<br/>- Retenção<br/>- DPO"]
    SEC_CHECK_LGPD -->|Não| SEC_CHECK_OWASP
    
    SEC_CHECK_OWASP{API Externa?}
    SEC_CHECK_OWASP -->|Sim| SEC_OWASP["✅ Checklist OWASP:<br/>- Rate limiting<br/>- Auth JWT<br/>- Input validation"]
    SEC_CHECK_OWASP -->|Não| SEC_CHECK_COMPANY
    
    SEC_CHECK_COMPANY{Critérios<br/>Empresa?}
    SEC_CHECK_COMPANY -->|Healthcare| SEC_HEALTH["🏥 Healthcare:<br/>- Audit trail<br/>- Encryption<br/>- RBAC"]
    SEC_CHECK_COMPANY -->|Outro| SEC_DONE
    
    SEC_LGPD --> SEC_SCORE[📊 Score: 6/9]
    SEC_OWASP --> SEC_SCORE
    SEC_HEALTH --> SEC_SCORE
    
    SEC_SCORE --> SEC_SHOW{Críticos?}
    SEC_SHOW -->|Sim| SEC_ALERT[⚠️ 3 itens críticos!]
    SEC_SHOW -->|Não| SEC_OK[✅ Tudo OK]
    
    SEC_ALERT --> SEC_ACTION{Adicionar?}
    SEC_ACTION -->|Sim| SEC_UPDATE[Atualiza Spec]
    SEC_ACTION -->|Não| SEC_DONE
    
    DIAG_START --> DIAG_TYPE{Tipo de<br/>Diagrama?}
    DIAG_TYPE -->|Arquitetura| GEN_ARCH[Gera Architecture]
    DIAG_TYPE -->|Fluxo| GEN_FLOW[Gera Flow]
    DIAG_TYPE -->|Sequência| GEN_SEQ[Gera Sequence]
    DIAG_TYPE -->|ER| GEN_ER[Gera ER]
    
    GEN_ARCH --> DIAG_AI[🤖 IA Gera Mermaid]
    GEN_FLOW --> DIAG_AI
    GEN_SEQ --> DIAG_AI
    GEN_ER --> DIAG_AI
    
    DIAG_AI --> DIAG_RENDER[Renderiza Preview]
    DIAG_RENDER --> DIAG_ACTION{Incluir?}
    DIAG_ACTION -->|Sim| DIAG_UPDATE[Adiciona à Spec]
    DIAG_ACTION -->|Não| DIAG_DONE
    
    TD_UPDATE --> ANALYSIS_COMPLETE
    TD_DONE --> ANALYSIS_COMPLETE
    TD_EMPTY --> ANALYSIS_COMPLETE
    
    SEC_UPDATE --> ANALYSIS_COMPLETE
    SEC_DONE --> ANALYSIS_COMPLETE
    SEC_OK --> ANALYSIS_COMPLETE
    
    DIAG_UPDATE --> ANALYSIS_COMPLETE
    DIAG_DONE --> ANALYSIS_COMPLETE
    
    ANALYSIS_COMPLETE[✅ Análises Completas] --> SKIP_TO_EXPORT
    
    SKIP_TO_EXPORT[📤 Pronto para Export] --> EXPORT_OPTIONS
    
    EXPORT_OPTIONS[📥 Download / 📋 Copy / 🚀 GitHub]
    
    style TD_SHOW fill:#ffe1e1
    style SEC_ALERT fill:#ffcccb
    style DIAG_RENDER fill:#e1f5ff
    style ANALYSIS_COMPLETE fill:#e1ffe1
```

---

## 🔄 Diagrama 7: Review Mode Workflow

```mermaid
stateDiagram-v2
    [*] --> Draft: Spec Criada
    
    Draft --> InReview: Enviar para Review
    Draft --> Editing: Continuar Editando
    Editing --> Draft: Salvar
    
    InReview --> Reviewing: Assign Reviewers
    Reviewing --> Commented: Reviewer Comenta
    Reviewing --> Approved: Reviewer Aprova
    Reviewing --> Rejected: Reviewer Rejeita
    
    Commented --> Responding: Author Responde
    Responding --> Commented: Novo Comentário
    Responding --> Resolved: Resolve Thread
    
    Resolved --> Approved: Todos OK
    Rejected --> Draft: Volta para Draft
    
    Approved --> AllApproved: Todos Aprovaram?
    AllApproved --> Finalized: Sim
    AllApproved --> Reviewing: Não (aguarda)
    
    Finalized --> Exported: Export (MD/Copy/GitHub Projects)
    Exported --> [*]
    
    note right of InReview
        Notifica reviewers
        via email/Slack
    end note
    
    note right of Commented
        @mentions ativos
        Threads inline
    end note
    
    note right of Approved
        Pode ter aprovação
        parcial (por seção)
    end note
```

---

## 📊 Diagrama 8: Data Flow & Integration

```mermaid
graph LR
    subgraph "User Input"
        TEXT[Texto]
        VOICE[Voz]
    end
    
    subgraph "Frontend"
        UI[React UI]
        WS[WebSocket]
    end
    
    subgraph "Backend API"
        ROUTE[FastAPI Routes]
        SESS[Session Manager]
        ORCH[Orchestrator]
    end
    
    subgraph "AI Pipeline"
        PROMPT[Prompt Builder]
        LLM_CALL[LLM Client]
        PARSER[Response Parser]
    end
    
    subgraph "Context Engine"
        MCP_CLI[MCP Client]
        QUERY[Query Builder]
        RANK[Ranking Engine]
    end
    
    subgraph "External APIs"
        OR_API[OpenRouter<br/>Gemini 2.5 Pro]
        MCP_SRV[claude-context<br/>MCP Server]
        ZILLIZ_DB[(Zilliz Cloud<br/>Vector DB)]
    end
    
    subgraph "Output"
        MD[Markdown Generator]
        VALID[Validator]
        EXPORT[Export Module]
    end
    
    TEXT --> UI
    VOICE -->|Whisper| UI
    UI <--> WS
    WS <--> ROUTE
    
    ROUTE --> SESS
    SESS --> ORCH
    
    ORCH --> PROMPT
    ORCH --> MCP_CLI
    
    PROMPT --> LLM_CALL
    LLM_CALL <-->|REST| OR_API
    OR_API --> PARSER
    
    MCP_CLI --> QUERY
    QUERY <-->|Stdio/JSON-RPC| MCP_SRV
    MCP_SRV <-->|Hybrid Search| ZILLIZ_DB
    MCP_SRV --> RANK
    
    PARSER --> ORCH
    RANK --> ORCH
    
    ORCH --> MD
    MD --> VALID
    VALID --> EXPORT
    
    EXPORT -->|Download| UI
    EXPORT -->|GitHub Projects API| GH[GitHub Projects]
    
    style OR_API fill:#ff6b6b
    style MCP_SRV fill:#4ecdc4
    style ZILLIZ_DB fill:#95e1d3
    style EXPORT fill:#e1ffe1
```

---

## 🎯 Diagrama 9: Casos de Uso por Perfil

```mermaid
graph TB
    subgraph "Perfil Não-Técnico 👔"
        NT_UC1[UC1: Criar Spec Simples<br/>Linguagem natural]
        NT_UC2[UC2: Voice Input<br/>Falar feature]
        NT_UC3[UC3: Ver Preview<br/>Documento em tempo real]
        NT_UC4[UC4: Split Automático<br/>Multi-repo sem decisão]
        NT_UC5[UC5: Enviar para Dev<br/>Download/Copy]
    end
    
    subgraph "Perfil Técnico 💻"
        TEC_UC1[UC1: Spec Detalhada<br/>Análise técnica profunda]
        TEC_UC2[UC2: Explorar Tradeoffs<br/>Comparar arquiteturas]
        TEC_UC3[UC3: Ver Código<br/>Snippets relevantes]
        TEC_UC4[UC4: Split Manual<br/>Controle fino de repos]
        TEC_UC5[UC5: Tech Debt Analysis<br/>TODOs/FIXMEs]
        TEC_UC6[UC6: Security Check<br/>OWASP/LGPD]
        TEC_UC7[UC7: Gerar Diagramas<br/>Mermaid arquitetura]
    end
    
    subgraph "Casos de Uso Comuns"
        COM_UC1[UC8: Histórico<br/>Ver specs anteriores]
        COM_UC2[UC9: Templates<br/>Reutilizar padrões]
        COM_UC3[UC10: Review Mode<br/>Aprovar specs]
        COM_UC4[UC11: Export<br/>MD/JSON/GitHub Projects]
    end
    
    subgraph "Sistema"
        SYS[Context2Task]
    end
    
    NT_UC1 --> SYS
    NT_UC2 --> SYS
    NT_UC3 --> SYS
    NT_UC4 --> SYS
    NT_UC5 --> SYS
    
    TEC_UC1 --> SYS
    TEC_UC2 --> SYS
    TEC_UC3 --> SYS
    TEC_UC4 --> SYS
    TEC_UC5 --> SYS
    TEC_UC6 --> SYS
    TEC_UC7 --> SYS
    
    COM_UC1 --> SYS
    COM_UC2 --> SYS
    COM_UC3 --> SYS
    COM_UC4 --> SYS
    
    style NT_UC1 fill:#e1f5ff
    style NT_UC2 fill:#e1f5ff
    style NT_UC3 fill:#e1f5ff
    style NT_UC4 fill:#e1f5ff
    style NT_UC5 fill:#e1f5ff
    
    style TEC_UC1 fill:#ffe1f5
    style TEC_UC2 fill:#ffe1f5
    style TEC_UC3 fill:#ffe1f5
    style TEC_UC4 fill:#ffe1f5
    style TEC_UC5 fill:#ffe1f5
    style TEC_UC6 fill:#ffe1f5
    style TEC_UC7 fill:#ffe1f5
    
    style COM_UC1 fill:#fff4e1
    style COM_UC2 fill:#fff4e1
    style COM_UC3 fill:#fff4e1
    style COM_UC4 fill:#fff4e1
```

---

## 🧠 Diagrama 10: Tech Debt Detector Inteligente (IA)

```mermaid
flowchart TB
    START[🚀 Usuário clica<br/>Tech Debt Detector] --> FEATURE_CTX[📄 Pega contexto<br/>da Feature]
    
    FEATURE_CTX --> MCP_SEARCH[🔍 MCP Search]
    
    subgraph "Busca de Código Relevante"
        MCP_SEARCH -->|Query| SEARCH_1[Backend relacionado]
        MCP_SEARCH -->|Query| SEARCH_2[Frontend relacionado]
        MCP_SEARCH -->|Query| SEARCH_3[Shared/Utils relacionados]
        
        SEARCH_1 --> CODE_CTX[Código Contextual<br/>Top 20 arquivos]
        SEARCH_2 --> CODE_CTX
        SEARCH_3 --> CODE_CTX
    end
    
    CODE_CTX --> PROMPT_BUILD[🔨 Monta Prompt<br/>Especializado]
    
    subgraph "Prompt Template"
        PROMPT_BUILD --> PROMPT["Categorias de Análise:<br/>✓ Code Smells<br/>✓ Duplicação<br/>✓ Anti-patterns<br/>✓ Performance<br/>✓ Acoplamento<br/>✓ Testabilidade<br/>✓ Best Practices"]
    end
    
    PROMPT --> LLM[🤖 Gemini 2.5 Pro<br/>via OpenRouter]
    
    LLM --> AI_ANALYSIS[IA Analisa Código]
    
    subgraph "Análise Inteligente"
        AI_ANALYSIS --> DETECT_SMELLS[Detecta Code Smells]
        AI_ANALYSIS --> DETECT_DUP[Detecta Duplicação]
        AI_ANALYSIS --> DETECT_PERF[Detecta Performance Issues]
        AI_ANALYSIS --> DETECT_ARCH[Detecta Problemas Arquiteturais]
        
        DETECT_SMELLS --> CLASSIFY
        DETECT_DUP --> CLASSIFY
        DETECT_PERF --> CLASSIFY
        DETECT_ARCH --> CLASSIFY
    end
    
    CLASSIFY[Classifica por Severidade] --> JSON_OUTPUT
    
    subgraph "Output Estruturado"
        JSON_OUTPUT[JSON Response] --> CRITICAL[🔴 Críticos]
        JSON_OUTPUT --> MEDIUM[🟡 Médios]
        JSON_OUTPUT --> LOW[🟢 Baixos]
        
        CRITICAL --> EFFORT_CALC[Calcula Esforço Total]
        MEDIUM --> EFFORT_CALC
        LOW --> EFFORT_CALC
    end
    
    EFFORT_CALC --> RENDER[🎨 Renderiza UI]
    
    subgraph "Apresentação ao Usuário"
        RENDER --> SHOW_SUMMARY["📊 Resumo:<br/>8 problemas<br/>5.5h esforço"]
        RENDER --> SHOW_CRITICAL["🔴 3 Críticos<br/>+ sugestões<br/>+ esforço"]
        RENDER --> SHOW_MEDIUM["🟡 3 Médios<br/>+ sugestões<br/>+ esforço"]
        RENDER --> SHOW_LOW["🟢 2 Baixos<br/>+ sugestões"]
    end
    
    SHOW_SUMMARY --> USER_ACTION{Usuário decide}
    SHOW_CRITICAL --> USER_ACTION
    SHOW_MEDIUM --> USER_ACTION
    SHOW_LOW --> USER_ACTION
    
    USER_ACTION -->|Adicionar Todos| ADD_ALL[✅ Adiciona todos à Spec]
    USER_ACTION -->|Selecionar| SELECT_ITEMS[⚙️ Seleciona quais adicionar]
    USER_ACTION -->|Ver Código| VIEW_CODE[👁️ Abre arquivo no MCP]
    USER_ACTION -->|Ignorar| SKIP[⏭️ Pula análise]
    
    ADD_ALL --> UPDATE_SPEC[📝 Atualiza Documento]
    SELECT_ITEMS --> UPDATE_SPEC
    VIEW_CODE --> USER_ACTION
    
    UPDATE_SPEC --> DONE([✅ Completo])
    SKIP --> DONE
    
    style MCP_SEARCH fill:#4ecdc4
    style LLM fill:#ff6b6b
    style AI_ANALYSIS fill:#ffd93d
    style CRITICAL fill:#ffcccc
    style MEDIUM fill:#fff4cc
    style LOW fill:#ccffcc
    style UPDATE_SPEC fill:#e1ffe1
```

### Comparação: Abordagem Antiga vs Nova

```mermaid
graph LR
    subgraph "❌ Abordagem Antiga (grep/regex)"
        OLD_START[Feature] --> OLD_GREP[grep TODO/FIXME]
        OLD_GREP --> OLD_RESULT[Lista de comentários]
        OLD_RESULT --> OLD_ISSUE[Problema: Só acha comentários]
    end
    
    subgraph "✅ Abordagem Nova (IA)"
        NEW_START[Feature] --> NEW_MCP[MCP Search]
        NEW_MCP --> NEW_AI[IA Analisa Código]
        NEW_AI --> NEW_SMART[Detecta problemas reais:<br/>code smells, N+1, duplicação]
        NEW_SMART --> NEW_SUGGEST[+ Sugestões de fix<br/>+ Esforço estimado]
    end
    
    style OLD_ISSUE fill:#ffcccc
    style NEW_SUGGEST fill:#ccffcc
```

---

## 🎯 Diagrama 11: GitHub Projects Integration

```mermaid
flowchart LR
    START[📄 Spec Completa] --> EXPORT_BTN[🚀 Exportar para GitHub]
    
    EXPORT_BTN --> SELECT_PROJECT{Selecionar<br/>GitHub Project}
    
    SELECT_PROJECT -->|Backlog| BACKLOG[📋 Backlog Board]
    SELECT_PROJECT -->|Sprint Atual| SPRINT[⚡ Sprint Board]
    SELECT_PROJECT -->|Roadmap| ROADMAP[🗺️ Roadmap Board]
    
    BACKLOG --> CREATE_CARD[Cria Card via<br/>GitHub Projects API]
    SPRINT --> CREATE_CARD
    ROADMAP --> CREATE_CARD
    
    CREATE_CARD --> CARD_CREATED[✅ Card Criado]
    
    subgraph "Card no GitHub Projects"
        CARD_CREATED --> CARD_CONTENT["Card contém:<br/>• Título<br/>• Descrição completa MD<br/>• Labels<br/>• Assignee<br/>• Priority<br/>• Links (se multi-spec)"]
    end
    
    CARD_CONTENT --> WORKFLOW{Próximos<br/>passos?}
    
    WORKFLOW -->|PM prioriza| MOVE_CARD[Move card<br/>entre boards]
    WORKFLOW -->|Dev pega| CONVERT[Converte card<br/>em Issue]
    WORKFLOW -->|Ajustar| EDIT[Edita card<br/>no board]
    
    MOVE_CARD --> DONE([✅ Fluxo concluído])
    CONVERT --> DONE
    EDIT --> DONE
    
    style BACKLOG fill:#bbdefb
    style SPRINT fill:#ffccbc
    style ROADMAP fill:#c5e1a5
    style CARD_CREATED fill:#e1ffe1
```

### Exemplo: Multi-Spec → 3 Cards Linkados

```mermaid
graph TB
    subgraph "GitHub Projects - Backlog Board"
        CARD1["📋 Card 1: [Backend]<br/>Sistema de Notificações Push<br/><br/>🔗 Relacionado:<br/>→ Card 2 (Frontend)<br/>→ Card 3 (Mobile)"]
        
        CARD2["📋 Card 2: [Frontend]<br/>Interface de Notificações<br/><br/>🔗 Relacionado:<br/>→ Card 1 (Backend)<br/>→ Card 3 (Mobile)"]
        
        CARD3["📋 Card 3: [Mobile]<br/>Push Notifications Nativo<br/><br/>🔗 Relacionado:<br/>→ Card 1 (Backend)<br/>→ Card 2 (Frontend)"]
    end
    
    CARD1 -.->|Depende| CARD1
    CARD2 -.->|Depende| CARD1
    CARD3 -.->|Depende| CARD1
    
    style CARD1 fill:#bbdefb
    style CARD2 fill:#c8e6c9
    style CARD3 fill:#fff9c4
```

---

## 📝 Legenda e Notas

### Cores
- 🔵 **Azul claro**: Features não-técnicas
- 🟣 **Rosa claro**: Features técnicas
- 🟡 **Amarelo claro**: Features comuns
- 🟢 **Verde claro**: Estados finais/sucesso
- 🔴 **Vermelho claro**: Alertas/decisões críticas

### Símbolos
- 📁 Repositórios
- 💬 Chat/Conversa
- 🤖 IA/Automação
- 🔍 Busca/Análise
- 📄 Documentos
- ⚠️ Alertas/Tech Debt
- 🔒 Segurança
- 👤 Usuário
- 🎤 Voice Input
- ✅ Aprovação/Sucesso
- 🚀 Export/Deploy

### 📝 Notas Importantes

#### Tech Debt Detector Inteligente 🧠

A análise de tech debt **não usa grep/regex** para procurar TODOs/FIXMEs (abordagem ultrapassada). Ao invés disso, usa **IA com acesso ao código via MCP** para análise profunda:

**Fluxo de Análise**:
1. **MCP Search**: Busca código relacionado à feature nos repositórios selecionados
2. **Prompt Especializado**: Envia código para IA com prompt focado em detectar:
   - 🔴 **Code Smells**: Long methods, god classes, shotgun surgery
   - 🔴 **Duplicação**: Código repetido, falta de abstração
   - 🔴 **Complexidade Ciclomática**: Funções muito complexas (> 10)
   - 🔴 **Anti-patterns**: Singleton abuse, magic numbers, global state
   - 🟡 **Performance**: N+1 queries, loops desnecessários, alocações excessivas
   - 🟡 **Acoplamento**: Dependências circulares, tight coupling
   - 🟡 **Falta de Testes**: Coverage baixo, código não testável
   - 🟢 **Violações de Padrões**: Naming conventions, estrutura de pastas
   - 🟢 **Documentação**: Falta de docstrings, comentários obsoletos

**Prompt Example**:
```
Você é um arquiteto de software expert. Analise o código abaixo relacionado 
à feature "{feature_description}" e identifique tech debt nos seguintes aspectos:

1. Code Smells (complexidade, tamanho de métodos, god classes)
2. Duplicação de código
3. Anti-patterns (singleton abuse, magic numbers, etc.)
4. Performance issues (N+1, loops ineficientes)
5. Acoplamento excessivo
6. Falta de testes ou código não testável
7. Violações de best practices da stack ({stack_tech})

Para cada problema encontrado, forneça:
- Severidade (Crítico/Médio/Baixo)
- Localização (arquivo:linha)
- Descrição clara do problema
- Sugestão de refatoração
- Estimativa de esforço (horas)

Código a analisar:
{code_context_from_mcp}
```

**Output da IA**:
```json
{
  "tech_debt": [
    {
      "severity": "critical",
      "category": "code_smell",
      "file": "backend/services/notification_service.py",
      "line": 145,
      "issue": "Método send_notification() tem 85 linhas (máx recomendado: 20)",
      "suggestion": "Quebrar em métodos menores: _validate, _prepare, _send, _log",
      "effort_hours": 2
    },
    {
      "severity": "medium",
      "category": "performance",
      "file": "backend/api/routes.py",
      "line": 67,
      "issue": "N+1 query: loop carrega usuários um por um",
      "suggestion": "Usar select_related() ou prefetch_related()",
      "effort_hours": 0.5
    }
  ]
}
```

**Vantagens sobre grep de TODOs**:
- ✅ Detecta problemas reais no código (não apenas comentários)
- ✅ Analisa qualidade arquitetural
- ✅ Prioriza por severidade real
- ✅ Dá sugestões concretas de refatoração
- ✅ Estima esforço para correção

---

#### Integração GitHub Projects
A plataforma **não cria Issues diretamente**, mas sim **Cards no GitHub Projects**:

1. **Fluxo de Export para GitHub**:
   - Usuário clica em "🚀 Exportar para GitHub"
   - Sistema pergunta: "Qual Project?" (Backlog / Sprint Atual / Roadmap)
   - Cria card no board selecionado via GitHub Projects API
   - Cards podem depois ser convertidos em Issues pelos devs

2. **Multi-Spec → GitHub Projects**:
   - Quando há 3 specs (Backend/Frontend/Mobile)
   - Sistema cria **3 cards linkados** no mesmo Project
   - Cards referenciam uns aos outros (tasks relacionadas)
   - Permite paralelização do trabalho entre times

3. **Vantagens**:
   - ✅ Cards vão direto pro board de gestão (Backlog, Sprint, etc.)
   - ✅ Já aparecem organizados no fluxo de trabalho
   - ✅ Não poluem as Issues do repo antes da priorização
   - ✅ PMs podem mover cards entre boards antes de virar Issue

---

## 🔗 Documentos de Referência

Estes diagramas foram gerados a partir de:
- `spec.md` - Especificação completa
- `interface-final-v2.md` - Interface ajustada
- `user-flows.md` - Fluxos detalhados
- `multi-spec-feature.md` - Feature multi-repo
- `priority-features-detail.md` - Features prioritárias
- `mcp-integration-notes.md` - Integração MCP
- `openrouter-integration-notes.md` - Integração LLM

---

**Criado**: 2025-10-19  
**Status**: Documentação Completa  
**Plataforma**: Context2Task

