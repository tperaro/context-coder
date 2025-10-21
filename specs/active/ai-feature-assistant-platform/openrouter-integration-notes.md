# OpenRouter Integration Notes

## Modelo Padrão
- **Model ID**: `google/gemini-2.5-pro`
- **Provider**: OpenRouter
- **Endpoint**: `https://openrouter.ai/api/v1/chat/completions`

## Autenticação

### Python com OpenAI SDK
```python
from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="<OPENROUTER_API_KEY>",
)

completion = client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "<APP_URL>",  # Para ranking no openrouter.ai
    "X-Title": "<APP_NAME>",       # Para ranking no openrouter.ai
  },
  model="google/gemini-2.5-pro",
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ]
)

print(completion.choices[0].message.content)
```

### Python com requests direto
```python
import requests

response = requests.post(
    'https://openrouter.ai/api/v1/chat/completions',
    headers={
        'Authorization': 'Bearer <OPENROUTER_API_KEY>',
        'Content-Type': 'application/json',
        'HTTP-Referer': '<APP_URL>',
        'X-Title': '<APP_NAME>',
    },
    json={
        'model': 'google/gemini-2.5-pro',
        'messages': [
            {
                'role': 'user',
                'content': 'Hello!'
            }
        ]
    }
)

result = response.json()
print(result['choices'][0]['message']['content'])
```

## Features Importantes

### 1. Prompt Caching (Gemini)
Para otimizar custos com contextos grandes (código do repositório):

```json
{
  "messages": [
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "You are a feature specification assistant. Below is the codebase context:"
        },
        {
          "type": "text",
          "text": "LARGE CODEBASE CONTEXT HERE",
          "cache_control": {
            "type": "ephemeral"
          }
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Help me specify this feature: [user input]"
        }
      ]
    }
  ]
}
```

### 2. Model Fallback
```python
completion = client.chat.completions.create(
    model="google/gemini-2.5-pro",
    extra_body={
        "models": [
            "anthropic/claude-3.5-sonnet",
            "openai/gpt-4o"
        ],
    },
    messages=[...]
)
```

### 3. Multi-turn Conversations
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Tell me about Python"},
    {"role": "assistant", "content": "Python is a programming language..."},
    {"role": "user", "content": "What about FastAPI?"}
]

completion = client.chat.completions.create(
    model="google/gemini-2.5-pro",
    messages=messages
)
```

## Variáveis de Ambiente Necessárias

```bash
# OpenRouter
OPENROUTER_API_KEY=sk-or-v1-xxxxx
DEFAULT_LLM_MODEL=google/gemini-2.5-pro
FALLBACK_MODELS=anthropic/claude-3.5-sonnet,openai/gpt-4o

# App Info (para ranking no OpenRouter)
APP_NAME=AI Feature Assistant Platform
APP_URL=http://localhost:3000

# Rate Limits (opcional)
MAX_TOKENS=8000
TEMPERATURE=0.7
```

## Custos e Limites

### Gemini 2.5 Pro via OpenRouter
- **Input**: ~$X por 1M tokens (verificar pricing atual)
- **Output**: ~$Y por 1M tokens
- **Caching**: Reduz custos significativamente para contextos reutilizados
- **Rate Limits**: Verificar limites do OpenRouter (geralmente generosos)

## Error Handling

```python
from openai import OpenAI, RateLimitError, APIError

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

try:
    completion = client.chat.completions.create(...)
except RateLimitError:
    # Rate limit atingido - implementar backoff
    print("Rate limit reached, waiting...")
except APIError as e:
    # Erro da API - tentar fallback model
    print(f"API error: {e}")
except Exception as e:
    # Outros erros
    print(f"Unexpected error: {e}")
```

## Streaming Support

```python
completion = client.chat.completions.create(
    model="google/gemini-2.5-pro",
    messages=[...],
    stream=True
)

for chunk in completion:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='')
```

## Referências
- [OpenRouter Docs](https://openrouter.ai/docs)
- [Gemini Models](https://openrouter.ai/docs/models#google-gemini)
- [Prompt Caching](https://openrouter.ai/docs/features/prompt-caching)
- [Model Routing](https://openrouter.ai/docs/features/model-routing)

