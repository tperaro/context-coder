# MCP Integration Notes

## Configuração Atual do MCP

### Setup do Usuario
```json
{
  "claude-context": {
    "command": "npx",
    "args": ["-y", "@zilliz/claude-context-mcp@latest"],
    "env": {
      "OPENAI_API_KEY": "sk-proj-...",
      "MILVUS_ADDRESS": "https://in03-1d4be7cd0fd6b0a.serverless.gcp-us-west1.cloud.zilliz.com",
      "MILVUS_TOKEN": "092c834ce630c1dc413971534cf7861938585653d5653c2504c782436c6d7dd0190a4a383c4e3e47f9950dc0843ed8c4565ffe2c"
    }
  }
}
```

### Arquitetura
- **MCP Server**: Local (executa via npx)
- **Comunicação**: Stdio (stdin/stdout)
- **Vector DB**: Zilliz Cloud Serverless (Milvus gerenciado)
- **Embeddings**: OpenAI (`text-embedding-3-small` por padrão)
- **Protocolo**: Model Context Protocol (MCP)

## Opções de Integração para Backend Python

### Opção 1: MCP Client Python (Recomendada)
Usar biblioteca oficial MCP para Python

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Inicializar MCP client
server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@zilliz/claude-context-mcp@latest"],
    env={
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "MILVUS_ADDRESS": os.getenv("MILVUS_ADDRESS"),
        "MILVUS_TOKEN": os.getenv("MILVUS_TOKEN")
    }
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        # Inicializar
        await session.initialize()
        
        # Listar tools disponíveis
        tools = await session.list_tools()
        
        # Chamar tool (ex: search_code)
        result = await session.call_tool(
            "search_code",
            arguments={
                "path": "/path/to/codebase",
                "query": "authentication implementation",
                "limit": 10
            }
        )
        
        print(result)
```

### Opção 2: Subprocess + JSON-RPC
Executar MCP como subprocess e comunicar via JSON-RPC

```python
import asyncio
import json
from typing import Dict, Any

class MCPClient:
    def __init__(self):
        self.process = None
        self.request_id = 0
        
    async def start(self):
        self.process = await asyncio.create_subprocess_exec(
            "npx", "-y", "@zilliz/claude-context-mcp@latest",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env={
                "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
                "MILVUS_ADDRESS": os.getenv("MILVUS_ADDRESS"),
                "MILVUS_TOKEN": os.getenv("MILVUS_TOKEN")
            }
        )
        
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]):
        self.request_id += 1
        
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        # Enviar request
        self.process.stdin.write(json.dumps(request).encode() + b'\n')
        await self.process.stdin.drain()
        
        # Ler response
        response_line = await self.process.stdout.readline()
        response = json.loads(response_line.decode())
        
        return response.get("result")
        
    async def stop(self):
        if self.process:
            self.process.terminate()
            await self.process.wait()
```

### Opção 3: Usar Core Library Diretamente (Node.js microservice)
Criar microservice Node.js que usa `@zilliz/claude-context-core`

```javascript
// mcp-service/index.js
import express from 'express';
import { Context, MilvusVectorDatabase, OpenAIEmbedding } from '@zilliz/claude-context-core';

const app = express();
app.use(express.json());

const embedding = new OpenAIEmbedding({
    apiKey: process.env.OPENAI_API_KEY,
    model: 'text-embedding-3-small'
});

const vectorDatabase = new MilvusVectorDatabase({
    address: process.env.MILVUS_ADDRESS,
    token: process.env.MILVUS_TOKEN
});

const context = new Context({ embedding, vectorDatabase });

app.post('/search', async (req, res) => {
    try {
        const { path, query, limit } = req.body;
        const results = await context.semanticSearch(path, query, limit);
        res.json({ results });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/index', async (req, res) => {
    try {
        const { path } = req.body;
        const stats = await context.indexCodebase(path, (progress) => {
            console.log(`${progress.phase} - ${progress.percentage}%`);
        });
        res.json({ stats });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.listen(3001, () => console.log('MCP service running on port 3001'));
```

## Decisão de Arquitetura

### Recomendação: Opção 1 (MCP Client Python)
**Vantagens**:
- ✅ Usa protocolo MCP oficial
- ✅ Mantém compatibilidade futura
- ✅ Menos overhead (sem HTTP)
- ✅ Tudo em Python (exceto subprocess Node)

**Desvantagens**:
- ⚠️ Precisa spawnar processo Node.js
- ⚠️ Comunicação via stdio (menos flexível)

### Alternativa: Opção 3 (Microservice Node.js)
**Vantagens**:
- ✅ HTTP REST API (mais familiar)
- ✅ Escalável (pode rodar separado)
- ✅ Mais fácil debug e teste
- ✅ Pode adicionar cache/rate limiting

**Desvantagens**:
- ⚠️ Mais uma peça na arquitetura
- ⚠️ Overhead HTTP
- ⚠️ Precisa gerenciar porta/health check

## Tools Disponíveis

### 1. index_codebase
Indexa um diretório de código

```python
result = await mcp_client.call_tool(
    "index_codebase",
    {
        "path": "/absolute/path/to/codebase",
        "force": False,  # Re-indexar se já indexado
        "splitter": "ast",  # ou "langchain"
        "customExtensions": [".vue", ".svelte"],  # opcional
        "ignorePatterns": ["*.tmp", "private/**"]  # opcional
    }
)
```

### 2. search_code
Busca semântica no código indexado

```python
result = await mcp_client.call_tool(
    "search_code",
    {
        "path": "/absolute/path/to/codebase",
        "query": "user authentication with JWT tokens",
        "limit": 10,
        "extensionFilter": [".py", ".js"]  # opcional
    }
)

# Resultado
{
    "results": [
        {
            "relativePath": "backend/auth/jwt.py",
            "startLine": 45,
            "endLine": 78,
            "content": "def validate_jwt_token(token: str):\n    ...",
            "score": 0.92
        }
    ]
}
```

### 3. clear_index
Limpa índice de um codebase

```python
result = await mcp_client.call_tool(
    "clear_index",
    {
        "path": "/absolute/path/to/codebase"
    }
)
```

### 4. get_indexing_status
Verifica status da indexação

```python
result = await mcp_client.call_tool(
    "get_indexing_status",
    {
        "path": "/absolute/path/to/codebase"
    }
)

# Resultado
{
    "status": "indexing",  # ou "completed"
    "percentage": 65,
    "filesProcessed": 325,
    "totalFiles": 500
}
```

## Variáveis de Ambiente

```bash
# OpenAI (para embeddings)
OPENAI_API_KEY=sk-proj-...

# Zilliz Cloud (Milvus Serverless)
MILVUS_ADDRESS=https://in03-xxx.serverless.gcp-us-west1.cloud.zilliz.com
MILVUS_TOKEN=092c834ce630...

# MCP Config (opcional)
MCP_TIMEOUT=30000  # ms
MCP_MAX_RETRIES=3
```

## Error Handling

```python
try:
    result = await mcp_client.call_tool("search_code", {...})
except MCPError as e:
    if e.code == "CODEBASE_NOT_INDEXED":
        # Indexar primeiro
        await mcp_client.call_tool("index_codebase", {...})
        result = await mcp_client.call_tool("search_code", {...})
    elif e.code == "TIMEOUT":
        # Retry ou fallback
        pass
    else:
        raise
```

## Performance Considerations

- **Indexação**: Pode levar minutos para codebases grandes (progress callback importante)
- **Busca**: < 1s para maioria das queries
- **Cache**: MCP faz caching automático de chunks já indexados
- **Rate Limits**: Respeitar limites do OpenAI (embeddings) e Zilliz Cloud

## Referências
- [claude-context GitHub](https://github.com/zilliztech/claude-context)
- [MCP Protocol Spec](https://modelcontextprotocol.io/)
- [Zilliz Cloud Docs](https://docs.zilliz.com/)

