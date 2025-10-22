# 🚀 Migração para Google Gemini API (Direto)

## ✅ O que mudou?

**ANTES:** OpenRouter como único provider (com erros 404)
**AGORA:** Google Gemini API (direto) como PRIMARY + OpenRouter como FALLBACK opcional

### Benefícios
- ✅ **GRATUITO**: Google AI Studio oferece tier gratuito generoso
- ✅ **CONFIÁVEL**: API oficial do Google, sem intermediários
- ✅ **RÁPIDO**: Latência menor, sem proxy
- ✅ **FALLBACK**: OpenRouter continua disponível se Google falhar

---

## 📋 Passo a Passo

### 1️⃣ Obtenha sua chave Google AI (GRÁTIS)

1. Acesse: **https://aistudio.google.com/apikey**
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. Copie a chave gerada

### 2️⃣ Configure as variáveis de ambiente

Edite `backend/.env`:

```bash
# PRIMARY - Google Gemini API (Direct)
GOOGLE_API_KEY=AIzaSy...your-key-here
GOOGLE_MODEL=gemini-2.0-flash-exp

# SECONDARY (FALLBACK) - OpenRouter API (opcional)
OPENROUTER_API_KEY=sk-or-v1-...  # Mantém a chave existente
OPENROUTER_MODEL=google/gemini-flash-1.5
```

### 3️⃣ Instale as dependências

Com o venv ativo:

```bash
# Ative o venv (se não estiver ativo)
source .venv/bin/activate

# Rode o script de setup
./scripts/setup-google-gemini.sh
```

**OU manualmente:**

```bash
cd backend
poetry add google-generativeai
```

### 4️⃣ Teste localmente

```bash
cd backend
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Abra outro terminal e teste:

```bash
# Health check
curl http://localhost:8000/health

# API info (mostra providers ativos)
curl http://localhost:8000/api/info
```

---

## 🔄 Como funciona o Fallback?

O `LLMService` tenta os providers nesta ordem:

1. **Google Gemini** (se `GOOGLE_API_KEY` configurada)
2. **OpenRouter** (se Google falhar OU se `GOOGLE_API_KEY` não configurada)

Logs mostram qual provider foi usado:

```
✅ Google Gemini provider initialized (PRIMARY)
✅ OpenRouter provider initialized (FALLBACK)
LLMService ready with 2 provider(s)
```

Se uma chamada falhar:

```
⚠️ GoogleGeminiProvider failed: <erro>
🔄 Falling back to next provider...
✅ OpenRouter response: ...
```

---

## 🧪 Testando só o Google (sem fallback)

Se quiser **forçar** apenas Google (sem OpenRouter como fallback), deixe `OPENROUTER_API_KEY` vazia:

```bash
# backend/.env
GOOGLE_API_KEY=AIzaSy...
GOOGLE_MODEL=gemini-2.0-flash-exp

# Comente ou remova:
# OPENROUTER_API_KEY=
# OPENROUTER_MODEL=
```

---

## 🐳 Docker

O Dockerfile já foi atualizado para instalar `google-generativeai`. Para rebuild:

```bash
docker-compose down
docker-compose up --build
```

Edite `backend/.env` antes de rodar (adicione `GOOGLE_API_KEY`).

---

## 📚 Modelos disponíveis

Google Gemini oferece vários modelos gratuitos:

| Modelo | Descrição | Velocidade | Contexto |
|--------|-----------|------------|----------|
| `gemini-2.0-flash-exp` | **Mais recente** (experimental) | ⚡ Muito rápido | 1M tokens |
| `gemini-1.5-flash` | Estável e rápido | ⚡ Rápido | 1M tokens |
| `gemini-1.5-pro` | Mais poderoso | 🐢 Lento | 2M tokens |

Recomendado para dev: **`gemini-2.0-flash-exp`**

---

## ❓ Troubleshooting

### Erro: "GOOGLE_API_KEY not set"

```
⚠️ GOOGLE_API_KEY not set - Google Gemini unavailable
✅ OpenRouter provider initialized (FALLBACK)
```

**Solução:** Adicione `GOOGLE_API_KEY` no `backend/.env`

---

### Erro: "google.generativeai could not be resolved"

```
ImportError: No module named 'google.generativeai'
```

**Solução:** Instale o pacote:

```bash
cd backend
poetry install  # ou poetry add google-generativeai
```

---

### OpenRouter ainda retornando 404?

Agora isso **não é mais um problema**! O Google Gemini será usado como primário, e o erro 404 do OpenRouter será ignorado (fallback).

Se você quiser **remover completamente** o OpenRouter:

1. Remova `OPENROUTER_API_KEY` do `.env`
2. O LLMService usará apenas Google

---

## 🎉 Conclusão

Pronto! Agora você está usando a API oficial do Google Gemini, com:

- ✅ Tier gratuito generoso
- ✅ Latência menor
- ✅ Mais confiável
- ✅ Fallback automático para OpenRouter se necessário

**Próximo passo:** Rode `./scripts/setup-google-gemini.sh` e adicione sua `GOOGLE_API_KEY`! 🚀
