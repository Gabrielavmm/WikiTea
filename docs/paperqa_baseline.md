# PaperQA Baseline Module

## Visão Geral

O módulo `paperqa_baseline.py` implementa um sistema de baseline usando PaperQA2 para comparação de precisão com o sistema RAG atual. PaperQA2 é reconhecido por sua alta precisão em documentos científicos PDF, servindo como referência para avaliação de qualidade.

## Arquitetura

### Classe Principal: PaperQABaseline

A classe `PaperQABaseline` gerencia a configuração e execução do sistema PaperQA2 para comparação com o sistema RAG principal.

#### Métodos Principais

##### `__init__()`
Inicializa o baseline com variáveis de estado para gerenciamento de documentos e sistema.

##### `install_paperqa() -> bool`
Instala automaticamente a biblioteca PaperQA se não estiver disponível.

**Retorno:** `True` se instalado ou já disponível, `False` em caso de erro

##### `initialize_system() -> bool`
Inicializa o sistema PaperQA com configurações otimizadas para documentos sobre autismo.

**Configurações:**
- `llm`: "gpt-3.5-turbo"
- `embeddings`: "text-embedding-ada-002"
- `max_sources`: 10
- `max_tokens`: 4000
- `chunk_size`: 1000
- `chunk_overlap`: 200

**Retorno:** `True` se inicializado com sucesso, `False` caso contrário

##### `add_autism_documents(document_paths: List[str]) -> bool`
Adiciona documentos sobre autismo ao sistema PaperQA.

**Parâmetros:**
- `document_paths`: Lista de caminhos para documentos (PDF, TXT, etc.)

**Retorno:** `True` se documentos adicionados com sucesso, `False` caso contrário

##### `query_system(question: str) -> Dict[str, Any]`
Executa uma consulta no sistema PaperQA.

**Parâmetros:**
- `question`: Pergunta a ser processada

**Retorno:** Dicionário contendo:
- `question`: Pergunta original
- `answer`: Resposta gerada
- `sources`: Lista de fontes utilizadas
- `confidence`: Score de confiança
- `citations`: Número de citações
- `method`: "PaperQA2"

##### `compare_with_rag(questions: List[str], rag_responses: List[Dict[str, Any]]) -> Dict[str, Any]`
Compara respostas do PaperQA com o sistema RAG atual.

**Parâmetros:**
- `questions`: Lista de perguntas
- `rag_responses`: Respostas do sistema RAG

**Retorno:** Dicionário com resultados da comparação:
- `paperqa_responses`: Respostas do PaperQA
- `rag_responses`: Respostas do RAG
- `comparison_metrics`: Métricas de comparação por pergunta
- `summary`: Resumo agregado das métricas

## Dependências

### Obrigatórias
- `paperqa`: Framework PaperQA2
- `openai`: Cliente OpenAI
- `os`: Operações do sistema
- `sys`: Sistema e caminhos
- `logging`: Sistema de logs

### Opcionais
- `subprocess`: Instalação automática de dependências

## Uso

### Execução Direta
```bash
python3 eval/paperqa_baseline.py
```

### Importação como Módulo
```python
from eval.paperqa_baseline import PaperQABaseline

baseline = PaperQABaseline()
baseline.initialize_system()
baseline.add_autism_documents(["doc1.pdf", "doc2.pdf"])
result = baseline.query_system("O que é autismo?")
```

### Comparação com RAG
```python
questions = ["Pergunta 1", "Pergunta 2"]
rag_responses = [...]  # Respostas do sistema RAG
comparison = baseline.compare_with_rag(questions, rag_responses)
```

## Configuração

### Variáveis de Ambiente
- `OPENAI_API_KEY`: Chave da API OpenAI (obrigatória)

### Documentos Suportados
- PDF: Documentos científicos e técnicos
- TXT: Textos simples
- Outros formatos suportados pelo PaperQA

### Configurações Recomendadas
- **Chunk Size**: 1000 tokens (balance entre contexto e precisão)
- **Chunk Overlap**: 200 tokens (continuidade de contexto)
- **Max Sources**: 10 (variedade de fontes)
- **Max Tokens**: 4000 (respostas completas)

## Métricas de Comparação

### Implementadas
- **Taxa de Sucesso**: Comparação de respostas válidas
- **Número de Citações**: Quantidade de fontes utilizadas
- **Confiança**: Score de confiança do PaperQA
- **Comprimento**: Comparação do tamanho das respostas

### Calculadas
- **PaperQA Success Rate**: Taxa de sucesso do PaperQA
- **RAG Success Rate**: Taxa de sucesso do RAG
- **Average Citations**: Média de citações por sistema
- **Performance Gap**: Diferença de performance

## Algoritmos de Comparação

### Detecção de Resposta Válida
```python
paperqa_valid = "answer" in result and not result.get("error")
rag_valid = not response.get("answer", "").startswith("Erro:")
```

### Contagem de Citações
```python
paperqa_citations = result.get("citations", 0)
rag_citations = 1 if "fonte" in response.get("answer", "").lower() else 0
```

### Cálculo de Métricas
```python
success_rate = valid_responses / total_questions
avg_citations = sum(citations) / total_questions
```

## Tratamento de Erros

### Tipos de Erro
1. **Instalação**: Falha na instalação do PaperQA
2. **Inicialização**: Erro na configuração do sistema
3. **Documentos**: Problemas na adição de documentos
4. **Consultas**: Falhas no processamento de perguntas
5. **Comparação**: Erros na análise comparativa

### Estratégias de Recuperação
- Instalação automática de dependências
- Criação de documento de exemplo
- Logging detalhado de erros
- Fallback para funcionalidades básicas

## Logs

### Níveis de Log
- `INFO`: Progresso normal e resultados
- `WARNING`: Avisos sobre problemas não críticos
- `ERROR`: Erros que impedem funcionamento

### Informações Registradas
- Instalação de dependências
- Inicialização do sistema
- Adição de documentos
- Processamento de consultas
- Resultados de comparação

## Saídas

### Console
- Logs de progresso
- Resultados de consultas
- Métricas de comparação
- Mensagens de erro

### Arquivos
- Documento de exemplo criado automaticamente
- Logs de execução (se configurado)

## Vantagens do PaperQA2

### Precisão
- Alta precisão em documentos científicos
- Algoritmos otimizados para PDF
- Métricas de confiança integradas

### Funcionalidades
- Suporte a múltiplos formatos
- Chunking inteligente
- Citações automáticas
- Configuração flexível

### Robustez
- Tratamento de erros robusto
- Fallbacks automáticos
- Logging detalhado

## Limitações

### Dependências
- Requer instalação do PaperQA
- Dependente de APIs externas
- Recursos computacionais elevados

### Funcionalidades
- Limitado a documentos específicos
- Configuração complexa
- Latência de processamento

## Casos de Uso

### Ideal Para
- Comparação com sistemas RAG
- Avaliação de precisão
- Baseline de qualidade
- Análise de documentos científicos

### Não Ideal Para
- Produção em tempo real
- Sistemas com recursos limitados
- Ambientes sem dependências externas
- Aplicações de baixa latência

## Comparação com Sistema RAG

| Aspecto | PaperQA2 | Sistema RAG |
|---------|----------|-------------|
| Precisão | Alta | Média |
| Latência | Alta | Baixa |
| Dependências | Muitas | Poucas |
| Configuração | Complexa | Simples |
| Citações | Automáticas | Manuais |
| Domínios | Científico | Geral |

## Manutenção

### Atualizações Recomendadas
- Atualizar versão do PaperQA
- Revisar configurações de chunking
- Otimizar parâmetros de embedding
- Melhorar tratamento de erros

### Monitoramento
- Performance de consultas
- Qualidade das citações
- Taxa de sucesso
- Uso de recursos

## Troubleshooting

### Problemas Comuns
1. **Instalação do PaperQA**: Verificar compatibilidade Python
2. **Chaves de API**: Validar OPENAI_API_KEY
3. **Documentos**: Verificar formatos suportados
4. **Memória**: Monitorar uso de RAM

### Soluções
- Reinstalar dependências
- Verificar variáveis de ambiente
- Converter documentos para formatos suportados
- Ajustar parâmetros de chunking

## Versionamento

- **v1.0**: Implementação inicial
- **v1.1**: Adição de comparação automática
- **v1.2**: Melhoria no tratamento de erros
- **v1.3**: Otimização de configurações

## Integração

### Com Sistema RAG
```python
from eval.simple_eval import SimpleRAGEvaluator
from eval.paperqa_baseline import PaperQABaseline

rag_evaluator = SimpleRAGEvaluator()
rag_responses = rag_evaluator.generate_responses()

baseline = PaperQABaseline()
baseline.initialize_system()
comparison = baseline.compare_with_rag(questions, rag_responses)
```

### Com RAGAS
```python
from eval.rag_evaluation import RAGEvaluator

ragas_evaluator = RAGEvaluator()
ragas_results = ragas_evaluator.evaluate_with_ragas(responses)

baseline = PaperQABaseline()
paperqa_results = baseline.query_system(question)
```

## Contribuição

Para contribuir com melhorias:
1. Manter compatibilidade com PaperQA
2. Adicionar testes de comparação
3. Documentar novas funcionalidades
4. Validar performance

---

*Documentação gerada automaticamente - Sistema RAG Autismo v1.0*