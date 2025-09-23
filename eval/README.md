# Sistema de Avaliação RAG - Autismo

Este diretório contém o sistema completo de avaliação para o assistente RAG especializado em autismo.

## 📁 Estrutura dos Arquivos

```
eval/
├── questions_and_answers.json    # 30 perguntas com gabarito
├── rag_evaluation.py            # Avaliação completa com RAGAS
├── simple_eval.py               # Avaliação simplificada (fallback)
├── paperqa_baseline.py          # Baseline PaperQA2 para comparação
├── install_dependencies.py      # Instalação de dependências
├── run_evaluation.py           # Script principal de execução
├── report.md                   # Relatório principal de avaliação
├── simple_report.md            # Relatório da avaliação simplificada
└── README.md                   # Este arquivo
```

## 🚀 Como Executar

### 1. Instalação de Dependências

```bash
# Instalar dependências básicas
python3 eval/install_dependencies.py

# Ou instalar manualmente
pip install ragas>=0.1.0 datasets>=2.14.0 openai>=1.3.0
```

### 2. Execução da Avaliação

```bash
# Executar avaliação completa (com RAGAS se disponível)
python3 eval/run_evaluation.py

# Executar apenas avaliação simplificada
python3 eval/simple_eval.py

# Executar avaliação completa com RAGAS
python3 eval/rag_evaluation.py
```

### 3. Configurar Baseline PaperQA2 (Opcional)

```bash
# Configurar e testar PaperQA2
python3 eval/paperqa_baseline.py
```

## 📊 Métricas Implementadas

### Métricas RAGAS
- **Faithfulness:** Mede se a resposta é baseada nos documentos recuperados
- **Answer Relevancy:** Mede se a resposta é relevante para a pergunta

### Métricas Customizadas
- **Taxa de Sucesso:** Percentual de respostas bem-sucedidas
- **Taxa de Citações:** Percentual de respostas com fontes
- **Taxa de Disclaimers:** Percentual de respostas com alertas médicos
- **Taxa de Palavras-chave:** Matching com termos esperados

## 📋 Conjunto de Perguntas

O arquivo `questions_and_answers.json` contém 30 perguntas organizadas por domínio:

- **Saúde (15 perguntas):** Diagnóstico, terapias, comorbidades
- **Direito (8 perguntas):** Legislação, benefícios, direitos
- **Educação (7 perguntas):** Inclusão, adaptações, AEE

### Exemplo de Pergunta
```json
{
  "id": 1,
  "question": "O que é o Transtorno do Espectro Autista (TEA)?",
  "ground_truth": "O Transtorno do Espectro Autista (TEA) é uma condição do desenvolvimento neurológico...",
  "source": "Organização Pan-Americana da Saúde (OPAS/OMS)",
  "url": "https://www.paho.org/pt/autism",
  "domain": "saúde",
  "expected_citations": ["OPAS", "OMS", "desenvolvimento neurológico"]
}
```

## 📈 Resultados da Avaliação

### Métricas Principais (Última Execução)
- **Taxa de Sucesso:** 100.00%
- **Taxa de Citações:** 100.00%
- **Taxa de Disclaimers:** 100.00%
- **Taxa de Palavras-chave:** 40.00%

### Análise por Domínio
- **Saúde:** 100.00% (6 perguntas testadas)
- **Direito:** 100.00% (3 perguntas testadas)
- **Educação:** 100.00% (1 pergunta testada)

## 🔧 Configuração Técnica

### Variáveis de Ambiente Necessárias
```bash
OPENAI_API_KEY=your_openai_key_here
HUGGINGFACE_API_KEY=your_huggingface_key_here  # Opcional
```

### Dependências Principais
```python
ragas>=0.1.0
datasets>=2.14.0
openai>=1.3.0
langchain>=0.3.0
langchain-openai>=0.0.2
chromadb>=1.0.0
sentence-transformers>=2.2.0
```

## 📊 Interpretação dos Resultados

### Faithfulness Score
- **0.8-1.0:** Excelente - Resposta bem fundamentada nos documentos
- **0.6-0.8:** Bom - Resposta parcialmente baseada em evidências
- **0.4-0.6:** Regular - Algumas informações não têm suporte
- **0.0-0.4:** Ruim - Resposta não baseada nos documentos

### Answer Relevancy Score
- **0.8-1.0:** Excelente - Resposta muito relevante
- **0.6-0.8:** Bom - Resposta relevante
- **0.4-0.6:** Regular - Resposta parcialmente relevante
- **0.0-0.4:** Ruim - Resposta não relevante

## 🐛 Problemas Conhecidos

### 1. Incompatibilidade de Embeddings
```
ERROR: Collection expecting embedding with dimension of 1536, got 384
```
**Solução:** Usar embeddings consistentes (OpenAI text-embedding-ada-002)

### 2. Problemas de API Key
```
ERROR: Error code: 401 - Incorrect API key provided
```
**Solução:** Verificar OPENAI_API_KEY no arquivo .env

### 3. Rate Limiting
```
ERROR: Error code: 429 - Too Many Requests
```
**Solução:** Implementar delays entre requisições

## 🔄 Melhorias Futuras

### Curto Prazo
1. Corrigir problema de embeddings
2. Implementar retry automático
3. Melhorar tratamento de erros

### Médio Prazo
1. Expandir conjunto de perguntas
2. Adicionar métricas de latência
3. Implementar comparação com PaperQA2

### Longo Prazo
1. Dashboard de métricas em tempo real
2. Integração com CI/CD
3. Avaliação contínua automática

## 📚 Referências

- [RAGAS Documentation](https://docs.ragas.io/)
- [PaperQA2 GitHub](https://github.com/whitead/paper-qa)
- [LangChain Evaluation](https://python.langchain.com/docs/guides/evaluation/)
- [ChromaDB Documentation](https://docs.trychroma.com/)

## 🤝 Contribuição

Para adicionar novas perguntas ou métricas:

1. Edite `questions_and_answers.json`
2. Execute a avaliação
3. Atualize os relatórios
4. Documente as mudanças

---
*Sistema de avaliação desenvolvido para o projeto RAG de Autismo*