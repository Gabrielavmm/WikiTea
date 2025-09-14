# 🧠 Assistente RAG para Autismo

Sistema de assistente inteligente baseado em RAG (Retrieval-Augmented Generation) e agentes LangGraph, especializado em informações sobre autismo (TEA - Transtorno do Espectro Autista).

## 🎯 Objetivo

Este projeto é uma prova de conceito (PoC) de um assistente com RAG + agentes que resolve um problema em **saúde**, especificamente fornecendo informações educativas sobre autismo com:

- ✅ **Citações obrigatórias** das fontes consultadas
- ✅ **Mecanismo anti-alucinação** com self-check
- ✅ **Orquestração de agentes** via LangGraph
- ✅ **Disclaimers de segurança** para questões de saúde
- ✅ **Interface web** com Streamlit

## 🏗️ Arquitetura

### Fluxo dos Agentes LangGraph

```
[Streamlit UI] 
   ↕
[LangGraph Supervisor] ← src/graph/rag_graph.py
   ├─(tool) RetrieverAgent  ← src/agents/retriever.py
   ├─(tool) AnswerAgent     ← src/agents/answerer.py  
   ├─(tool) SelfCheckAgent  ← src/agents/self_check.py
   └─(tool) SafetyAgent     ← src/agents/safety.py
```

### Estrutura do Projeto

```
AtividadeLLM/
├── src/                    # Código principal dos agentes
│   ├── agents/            # Agentes individuais
│   ├── graph/             # Orquestração LangGraph
│   ├── tools/             # Ferramentas (vector search, LLM)
│   └── config/            # Configurações
├── app/                   # Interface Streamlit
├── ingest/                # Scripts de ingestão de dados
├── eval/                  # Avaliação e métricas
├── tests/                 # Testes
├── data/                  # Dados brutos
├── chroma_db/             # Banco vetorial ChromaDB
├── requirements.txt       # Dependências
├── Dockerfile            # Containerização
└── README.md             # Esta documentação
```

## 🚀 Como Executar

### Pré-requisitos

- Python 3.11+
- Git

### 1. Clonar e Configurar

```bash
git clone <seu-repositorio>
cd AtividadeLLM
```

### 2. Verificar Python e Dependências

```bash
# Verificar versão do Python
python3.10 --version

# Verificar se as dependências estão instaladas
python3.10 -c "import langchain, streamlit, chromadb; print('✅ Dependências OK')"
```

### 3. Instalar Dependências (se necessário)

```bash
# Se alguma dependência estiver faltando:
pip3.10 install langchain langchain-community langchain-chroma langgraph streamlit sentence-transformers
```

### 4. Executar Ingestão de Dados

```bash
python3.10 ingest/autism_docs.py
```

### 5. Executar Interface

```bash
python3.10 -m streamlit run app/streamlit_app.py
```

### 6. Acessar no Navegador

Abra http://localhost:8501

## 🐳 Executar com Docker

```bash
# Construir imagem
docker build -t autism-rag .

# Executar container
docker run -p 8501:8501 autism-rag
```

## 🤖 Agentes Implementados

### 1. **Supervisor** (Router de Intents)
- Analisa a consulta do usuário
- Decide se precisa de retrieval de documentos
- Roteia para os agentes apropriados

### 2. **Retriever** (Busca Vetorial)
- Busca documentos relevantes no ChromaDB
- Usa embeddings HuggingFace (sentence-transformers)
- Retorna documentos com scores de similaridade

### 3. **Answerer** (Gerador de Respostas)
- Gera respostas baseadas nos documentos recuperados
- **SEMPRE inclui citações** das fontes
- Usa LLM (Ollama/Llama3.1 por padrão)

### 4. **Self-Check** (Anti-alucinação)
- Valida se a resposta tem evidências suficientes
- Calcula score de confiança (0-1)
- Rejeita respostas sem citações adequadas

### 5. **Safety** (Verificação de Segurança)
- Adiciona disclaimers médicos obrigatórios
- Verifica palavras perigosas
- Garante que não há aconselhamento médico direto

## 📊 Métricas de Qualidade

O sistema implementa várias verificações:

- **Context Precision/Recall**: Baseado na relevância dos documentos recuperados
- **Faithfulness**: Verificação se a resposta é baseada nas evidências
- **Answer Relevancy**: Relevância da resposta para a pergunta
- **Confidence Score**: Score de confiança (0-1) baseado em evidências
- **Citation Coverage**: Percentual de sentenças com citações

## 📚 Fontes de Dados

- **Wikipedia**: Informações gerais sobre autismo
- **SUS**: Protocolos oficiais do Ministério da Saúde
- **OMS**: Diretrizes internacionais
- **Documentos educacionais**: Material sobre TEA, direitos, terapias

## ⚠️ Limitações e Disclaimers

### **Ética & Segurança**
- ❌ **NÃO faz diagnósticos** médicos ou psicológicos
- ❌ **NÃO fornece aconselhamento** de tratamento
- ❌ **NÃO substitui** consulta profissional
- ✅ **APENAS informativo** com fontes citadas
- ✅ **SEMPRE** inclui disclaimers de segurança

### **Limitações Técnicas**
- Baseado em documentos públicos disponíveis
- Depende da qualidade dos embeddings
- LLM pode ter limitações de conhecimento atual
- Requer conexão com internet para algumas fontes

## 🧪 Avaliação

### Teste Manual
- Conjunto de 20+ perguntas sobre autismo
- Verificação manual de citações
- Análise de relevância das respostas

### Métricas Automatizadas
- **Faithfulness**: RAGAS para verificar se respostas são baseadas em evidências
- **Answer Relevancy**: Relevância das respostas para as perguntas
- **Context Precision/Recall**: Qualidade da recuperação de documentos

## 🔧 Configurações

### Variáveis de Ambiente

```bash
# LLM
export LLM_MODEL_TYPE="ollama"  # ollama, openai, huggingface
export LLM_MODEL_NAME="llama3.1:8b"

# Vector Store
export VECTOR_STORE_DIR="./chroma_db"
export VECTOR_STORE_COLLECTION="autismo"

# Embeddings
export EMBEDDING_MODEL="sentence-transformers/all-MiniLM-L6-v2"
```

## 📈 Próximos Passos

- [ ] Adicionar mais fontes de dados (protocolos SUS, pesquisas)
- [ ] Implementar reranking de documentos
- [ ] Melhorar métricas de avaliação com RAGAS
- [ ] Adicionar suporte a PDFs e documentos offline
- [ ] Implementar cache de respostas
- [ ] Adicionar logs de auditoria

## 🤝 Contribuição

Este é um projeto acadêmico. Para contribuições:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## 📞 Contato

Desenvolvido como projeto final da disciplina de LLM.

---

**⚠️ IMPORTANTE**: Este sistema é apenas educacional e informativo. Não substitui consulta médica, psicológica ou de outros profissionais qualificados. Sempre consulte profissionais de saúde para diagnóstico e tratamento.