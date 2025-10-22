# Nota sobre o Frontend

## 📦 Frontend Movido para Repositório Separado

O frontend do Context-Coder foi movido para um repositório dedicado:

🔗 **https://github.com/tperaro/context-coder-front**

---

## 🚀 Como Usar

### 1. Execute o Backend (este repositório)

```bash
# Configure o ambiente
cp .env.example .env
# Edite .env com suas API keys

# Inicie o backend
docker-compose up --build

# Backend rodando em: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### 2. Execute o Frontend (repositório separado)

```bash
# Clone o repositório do frontend
git clone https://github.com/tperaro/context-coder-front.git
cd context-coder-front

# Siga as instruções do README
# Frontend rodará em: http://localhost:5173
```

---

## 🎯 Por que separamos?

- ✅ **Deploy independente** - Frontend e backend podem ser deployados separadamente
- ✅ **Desenvolvimento mais rápido** - Times podem trabalhar independentemente
- ✅ **CI/CD simplificado** - Pipelines separados e mais rápidos
- ✅ **Versionamento claro** - Cada parte tem sua própria versão
- ✅ **Escalabilidade** - Podem ser escalados independentemente

---

## 🔗 Integração

O frontend se comunica com este backend via:

- **API REST**: `http://localhost:8000/api/`
- **Docs**: `http://localhost:8000/docs`

### Configuração necessária:

**No Backend (.env):**
```bash
CORS_ORIGINS=http://localhost:5173
```

**No Frontend (.env):**
```bash
VITE_API_URL=http://localhost:8000
```

---

Para mais informações, consulte:
- [README do Backend](./README.md)
- [README do Frontend](https://github.com/tperaro/context-coder-front/blob/main/README.md)
