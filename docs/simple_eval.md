# Simple RAG Evaluation Module

## Visão Geral

O módulo `simple_eval.py` implementa um sistema de avaliação simplificado para o assistente RAG especializado em autismo, sem dependência de frameworks externos como RAGAS. É uma alternativa leve para casos onde as dependências completas não estão disponíveis.

## Arquitetura

### Classe Principal: SimpleRAGEvaluator

A classe `SimpleRAGEvaluator` fornece funcionalidades básicas de avaliação usando apenas bibliotecas padrão do Python.

#### Métodos Principais

##### `__init__()`
Inicializa o avaliador simplificado com variáveis de estado básicas.

##### `load_questions(questions_file: str) -> bool`
Carrega o conjunto de perguntas de avaliação a partir de um arquivo JSON.

**Parâmetros:**
- `questions_file`: Caminho para o arquivo JSON contendo as perguntas (padrão: "eval/questions_and_answers.json")

**Retorno:** `True` se carregado com sucesso, `False` caso contrário

##### `initialize_rag_system() -> bool`
Inicializa o sistema RAG para processamento das perguntas.

**Retorno:** `True` se inicializado com sucesso, `False` caso contrário

##### `generate_responses(max_questions: int) -> List[Dict[str, Any]]`
Gera respostas para um número limitado de perguntas usando o sistema RAG.

**Parâmetros:**
- `max_questions`: Número máximo de perguntas a processar (padrão: 10)

**Retorno:** Lista de dicionários contendo:
- `question`: Texto da pergunta
- `answer`: Resposta gerada pelo sistema
- `ground_truth`: Resposta esperada
- `question_id`: ID da pergunta
- `domain`: Domínio da pergunta
- `source`: Fonte da pergunta
- `expected_citations`: Citações esperadas

##### `calculate_metrics(responses: List[Dict[str, Any]]) -> Dict[str, Any]`
Calcula métricas básicas de avaliação sem dependências externas.

**Parâmetros:**
- `responses`: Lista de respostas geradas

**Retorno:** Dicionário com métricas:
- `success_rate`: Taxa de sucesso
- `citation_rate`: Taxa de citações
- `disclaimer_rate`: Taxa de disclaimers
- `keyword_match_rate`: Taxa de matching de palavras-chave
- `domain_accuracy`: Precisão por domínio

##### `generate_simple_report(metrics: Dict[str, Any], responses: List[Dict[str, Any]]) -> str`
Gera relatório simplificado em Markdown com os resultados da avaliação.

**Parâmetros:**
- `metrics`: Métricas calculadas
- `responses`: Respostas geradas

**Retorno:** String contendo o relatório em Markdown

##### `save_results(metrics: Dict[str, Any], responses: List[Dict[str, Any]], report: str)`
Salva os resultados em arquivos.

**Arquivos gerados:**
- `eval/simple_report.md`: Relatório simplificado
- `eval/simple_results.json`: Resultados em JSON

## Dependências

### Obrigatórias (Mínimas)
- `json`: Manipulação de arquivos JSON
- `logging`: Sistema de logs
- `datetime`: Manipulação de datas
- `os`: Operações do sistema
- `sys`: Sistema e caminhos

### Internas
- `src.graph.rag_graph`: Sistema RAG principal

### Não Obrigatórias
- `ragas`: Framework de avaliação RAG (não utilizado)
- `datasets`: Manipulação de datasets (não utilizado)

## Uso

### Execução Direta
```bash
python3 eval/simple_eval.py
```

### Importação como Módulo
```python
from eval.simple_eval import SimpleRAGEvaluator

evaluator = SimpleRAGEvaluator()
evaluator.load_questions()
evaluator.initialize_rag_system()
responses = evaluator.generate_responses(max_questions=5)
```

## Métricas Implementadas

### Básicas
- **Taxa de Sucesso**: Percentual de respostas bem-sucedidas
- **Taxa de Citações**: Percentual de respostas com fontes
- **Taxa de Disclaimers**: Percentual de respostas com alertas médicos
- **Taxa de Palavras-chave**: Matching com termos esperados

### Por Domínio
- **Saúde**: Precisão em perguntas médicas
- **Direito**: Precisão em perguntas legais
- **Educação**: Precisão em perguntas educacionais

## Algoritmos de Cálculo

### Taxa de Sucesso
```python
success_rate = successful_responses / total_questions
```

### Taxa de Citações
Detecta presença de palavras-chave relacionadas a fontes:
- "fonte"
- "documento"
- "consulta"

### Taxa de Disclaimers
Detecta presença de alertas de segurança:
- "importante"
- "consulte"
- "não substitui"

### Matching de Palavras-chave
Compara palavras-chave esperadas com o conteúdo da resposta usando busca case-insensitive.

## Tratamento de Erros

O módulo implementa tratamento básico de erros:
- Falhas na carregamento de perguntas
- Erros na inicialização do sistema RAG
- Falhas no processamento de perguntas individuais
- Problemas na geração de relatórios

## Logs

O sistema utiliza logging estruturado com níveis:
- `INFO`: Informações gerais de progresso
- `ERROR`: Erros críticos que impedem execução

## Configuração

### Variáveis de Ambiente
- `OPENAI_API_KEY`: Chave da API OpenAI (para sistema RAG)

### Arquivos de Configuração
- `eval/questions_and_answers.json`: Conjunto de perguntas de avaliação

## Saídas

### Arquivos Gerados
1. **eval/simple_report.md**: Relatório simplificado em Markdown
2. **eval/simple_results.json**: Resultados estruturados em JSON

### Console
- Logs de progresso durante execução
- Resumo final das métricas
- Mensagens de erro

## Vantagens

1. **Baixa Dependência**: Não requer frameworks externos pesados
2. **Execução Rápida**: Processamento mais leve
3. **Facilidade de Instalação**: Dependências mínimas
4. **Compatibilidade**: Funciona em ambientes restritivos

## Limitações

1. **Métricas Básicas**: Não implementa métricas avançadas como RAGAS
2. **Análise Limitada**: Análise de qualidade mais simples
3. **Sem Comparação**: Não compara com baselines externos
4. **Funcionalidades Reduzidas**: Menos recursos que versão completa

## Casos de Uso

### Ideal Para
- Ambientes com restrições de dependências
- Testes rápidos e desenvolvimento
- Sistemas com recursos limitados
- Validação básica de funcionamento

### Não Ideal Para
- Avaliação de produção completa
- Análise detalhada de qualidade
- Comparação com baselines
- Relatórios técnicos avançados

## Comparação com RAGAS

| Aspecto | Simple Eval | RAGAS |
|---------|-------------|-------|
| Dependências | Mínimas | Extensas |
| Métricas | Básicas | Avançadas |
| Performance | Rápida | Mais lenta |
| Precisão | Limitada | Alta |
| Instalação | Simples | Complexa |

## Manutenção

### Atualizações Recomendadas
- Revisar algoritmos de detecção de citações
- Melhorar matching de palavras-chave
- Expandir métricas básicas
- Otimizar geração de relatórios

### Troubleshooting
- Verificar sistema RAG principal
- Validar arquivo de perguntas
- Revisar logs de erro
- Testar com menos perguntas

## Versionamento

- **v1.0**: Implementação inicial básica
- **v1.1**: Adição de métricas por domínio
- **v1.2**: Melhoria no tratamento de erros
- **v1.3**: Otimização de performance

## Migração para RAGAS

Para migrar para avaliação completa:
1. Instalar dependências RAGAS
2. Usar `rag_evaluation.py`
3. Comparar resultados
4. Manter ambos os sistemas

## Contribuição

Para contribuir com melhorias:
1. Manter simplicidade e baixa dependência
2. Adicionar testes básicos
3. Documentar mudanças
4. Validar compatibilidade

---

*Documentação gerada automaticamente - Sistema RAG Autismo v1.0*