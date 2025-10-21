# Template de Task da Empresa

## 📌 Descrição / Contexto  
> **Objetivo geral da tarefa**  
> Explique o problema ou necessidade que essa issue busca resolver.  
> Forneça contexto técnico, regulatório ou de negócio, se necessário.

**Exemplo:**
Precisamos enriquecer as descrições dos procedimentos da tabela SIGTAP usando LLMs. Isso vai ajudar os codificadores a entenderem melhor os procedimentos e melhorar a precisão do faturamento.

---

## 👤 User Story  
> Use o formato:  
> *Como [perfil de usuário]*, quero [ação desejada], para que [benefício de negócio]*.

**Exemplo:**  
Como integrante do time de Faturamento, quero que as descrições dos procedimentos sejam limpas e enriquecidas automaticamente, para que o processo de codificação seja mais preciso.

---

## 📋 Resultado Esperado  
> Quais artefatos, scripts, relatórios ou funcionalidades devem estar prontos ao final da tarefa?

**Exemplo:**  
- Script que limpa e trata dados do SIGTAP  
- Script assíncrono que enriquece as descrições via API da OpenAI com cache  
- CSV final ou entrada no banco com os dados enriquecidos

---

## ⚙️ Detalhes Técnicos / Escopo  
> Detalhar o que deve ser feito tecnicamente.  
> Pode usar subtópicos e bullets.

**Exemplo:**  
1. Ler arquivo CSV com Polars  
2. Limpar dados inconsistentes e colunas desnecessárias  
3. Criar pipeline assíncrona com cache para OpenAI  
4. Validar volume (ex: 5k registros) com bom desempenho  
5. Gerar saída formatada para ingestão futura

---

## 📌 Checklist de Tarefas  
> Lista de subtarefas que podem ser marcadas conforme concluídas.

**Exemplo:** 
- [ ] Configurar ambiente e dependências (Polars, OpenAI API, etc.)  
- [ ] Implementar script de limpeza  
- [ ] Criar pipeline de chamadas assíncronas à LLM  
- [ ] Implementar caching e estratégia JIT  
- [ ] Validar enriquecimento com amostra  
- [ ] Gerar saída em CSV ou inserir no banco  
- [ ] Testar e revisar performance  
- [ ] Documentar uso e dependências  
- [ ] Submeter PR com revisores

---

## ✅ Critérios de Aceite  
> O que precisa estar funcionando ou disponível para que a issue seja aceita?

**Exemplo:**  
- Todas as descrições processadas com sucesso  
- Caching implementado  
- Limpeza eficaz de dados ruins  
- Processamento em menos de X minutos para 5k linhas

---

## 📦 Definição de Done  
> Estado esperado da tarefa ao ser encerrada.

**Exemplo:**  
- Código mergeado em `develop`  
- Documentação atualizada no README  
- Página no MKDocs com exemplo de uso  
- Nenhum erro crítico na execução (tratamento de exceções feito)

---

## 🔍 Observações Adicionais  
> Notas soltas, sugestões, decisões, ou informações úteis que não se encaixam nas outras seções.

**Exemplo:**  
- Avaliar se compensa armazenar múltiplas versões da tabela SIGTAP no banco  
- Futuramente, criar um painel de comparação entre versões  
- Lidar com possíveis timeouts da OpenAI com `backoff` e retries

---

## 🔗 Referências / Links Úteis (opcional)  
> Links para documentação externa, APIs, RFCs, páginas de referência, etc.

**Exemplo:** 
- [OpenAI API Docs](https://platform.openai.com/docs)  
- [Polars Docs](https://pola-rs.github.io/polars/)  

---

## ⚠️ Riscos ou Limitações (opcional)  
> Quais fatores podem impactar o andamento ou sucesso dessa tarefa?

**Exemplo:**  
- Instabilidade da API da OpenAI  
- Custo elevado com requisições se caching falhar  
- Inconsistência nos dados históricos do SIGTAP

