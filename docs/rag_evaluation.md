# RAG Evaluation Module

## Visão Geral

O módulo `rag_evaluation.py` implementa um sistema completo de avaliação para o assistente RAG especializado em autismo, utilizando métricas RAGAS (faithfulness e answer relevancy) e métricas customizadas.

## Arquitetura

### Classe Principal: RAGEvaluator

A classe `RAGEvaluator` é responsável por coordenar todo o processo de avaliação do sistema RAG.

#### Métodos Principais

##### `__init__()`
Inicializa o avaliador com variáveis de estado vazias.

##### `load_questions(questions_file: str) -> bool`
Carrega o conjunto de perguntas de avaliação a partir de um arquivo JSON.

**Parâmetros:**
- `questions_file`: Caminho para o arquivo JSON contendo as perguntas (padrão: "eval/questions_and_answers.json")

**Retorno:** `True` se carregado com sucesso, `False` caso contrário

##### `initialize_rag_system() -> bool`
Inicializa o sistema RAG para processamento das perguntas.

**Retorno:** `True` se inicializado com sucesso, `False` caso contrário

##### `generate_responses() -> List[Dict[str, Any]]`
Gera respostas para todas as perguntas usando o sistema RAG.

**Retorno:** Lista de dicionários contendo:
- `question`: Texto da pergunta
- `answer`: Resposta gerada pelo sistema
- `ground_truth`: Resposta esperada
- `context`: Contexto usado
- `question_id`: ID da pergunta
- `domain`: Domínio da pergunta
- `expected_citations`: Citações esperadas

##### `evaluate_with_ragas(responses: List[Dict[str, Any]]) -> Dict[str, Any]`
Avalia as respostas usando métricas RAGAS.

**Parâmetros:**
- `responses`: Lista de respostas geradas

**Retorno:** Dicionário com métricas RAGAS:
- `faithfulness`: Score de fidelidade (0-1)
- `answer_relevancy`: Score de relevância (0-1)

##### `calculate_additional_metrics(responses: List[Dict[str, Any]]) -> Dict[str, Any]`
Calcula métricas adicionais específicas do sistema.

**Parâmetros:**
- `responses`: Lista de respostas geradas

**Retorno:** Dicionário com métricas customizadas:
- `success_rate`: Taxa de sucesso
- `citation_rate`: Taxa de citações
- `disclaimer_rate`: Taxa de disclaimers
- `domain_accuracy`: Precisão por domínio

##### `generate_report(ragas_results: Dict[str, Any], additional_metrics: Dict[str, Any], responses: List[Dict[str, Any]]) -> str`
Gera relatório em Markdown com os resultados da avaliação.

**Parâmetros:**
- `ragas_results`: Resultados das métricas RAGAS
- `additional_metrics`: Métricas adicionais
- `responses`: Respostas geradas

**Retorno:** String contendo o relatório em Markdown

##### `save_results(ragas_results: Dict[str, Any], additional_metrics: Dict[str, Any], responses: List[Dict[str, Any]], report: str)`
Salva os resultados em arquivos.

**Arquivos gerados:**
- `eval/report.md`: Relatório principal
- `eval/results.json`: Resultados em JSON

## Dependências

### Obrigatórias
- `ragas>=0.1.0`: Framework de avaliação RAG
- `datasets>=2.14.0`: Manipulação de datasets
- `openai>=1.3.0`: Cliente OpenAI
- `langchain>=0.3.0`: Framework LangChain
- `chromadb>=1.0.0`: Banco vetorial
- `sentence-transformers>=2.2.0`: Modelos de embedding

### Internas
- `src.graph.rag_graph`: Sistema RAG principal
- `json`: Manipulação de arquivos JSON
- `logging`: Sistema de logs
- `datetime`: Manipulação de datas
- `os`: Operações do sistema
- `sys`: Sistema e caminhos

## Uso

### Execução Direta
```bash
python3 eval/rag_evaluation.py
```

### Importação como Módulo
```python
from eval.rag_evaluation import RAGEvaluator

evaluator = RAGEvaluator()
evaluator.load_questions()
evaluator.initialize_rag_system()
responses = evaluator.generate_responses()
```

## Métricas Implementadas

### RAGAS
- **Faithfulness**: Mede se a resposta é baseada nos documentos recuperados
- **Answer Relevancy**: Mede se a resposta é relevante para a pergunta

### Customizadas
- **Taxa de Sucesso**: Percentual de respostas bem-sucedidas
- **Taxa de Citações**: Percentual de respostas com fontes
- **Taxa de Disclaimers**: Percentual de respostas com alertas médicos
- **Precisão por Domínio**: Performance por área (saúde, direito, educação)

## Tratamento de Erros

O módulo implementa tratamento robusto de erros:
- Falhas na importação de dependências
- Erros na inicialização do sistema RAG
- Falhas no processamento de perguntas individuais
- Problemas na avaliação RAGAS

## Logs

O sistema utiliza logging estruturado com níveis:
- `INFO`: Informações gerais de progresso
- `ERROR`: Erros críticos que impedem execução
- `WARNING`: Avisos sobre problemas não críticos

## Configuração

### Variáveis de Ambiente
- `OPENAI_API_KEY`: Chave da API OpenAI
- `HUGGINGFACE_API_KEY`: Chave da API HuggingFace (opcional)

### Arquivos de Configuração
- `eval/questions_and_answers.json`: Conjunto de perguntas de avaliação
- `.env`: Variáveis de ambiente (opcional)

## Saídas

### Arquivos Gerados
1. **eval/report.md**: Relatório principal em Markdown
2. **eval/results.json**: Resultados estruturados em JSON

### Console
- Logs de progresso durante execução
- Resumo final das métricas
- Mensagens de erro e avisos

## Limitações

1. **Dependência do RAGAS**: Requer instalação de dependências específicas
2. **API Externa**: Dependente de APIs externas (OpenAI)
3. **Recursos Computacionais**: Pode ser intensivo em CPU/memória
4. **Latência**: Processamento pode ser lento para grandes conjuntos

## Manutenção

### Atualizações Recomendadas
- Atualizar versões das dependências regularmente
- Revisar métricas RAGAS conforme evolução do framework
- Expandir conjunto de perguntas de avaliação
- Otimizar performance para grandes volumes

### Troubleshooting
- Verificar instalação das dependências
- Validar chaves de API
- Revisar logs de erro para diagnóstico
- Testar com conjunto menor de perguntas

## Versionamento

- **v1.0**: Implementação inicial com RAGAS básico
- **v1.1**: Adição de métricas customizadas
- **v1.2**: Melhoria no tratamento de erros
- **v1.3**: Otimização de performance

## Contribuição

Para contribuir com melhorias:
1. Seguir padrões de código existentes
2. Adicionar testes para novas funcionalidades
3. Atualizar documentação
4. Validar compatibilidade com dependências

---

*Documentação gerada automaticamente - Sistema RAG Autismo v1.0*