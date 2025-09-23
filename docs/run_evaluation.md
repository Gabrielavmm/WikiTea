# Run Evaluation Module

## Visão Geral

O módulo `run_evaluation.py` é um script de execução principal que coordena diferentes tipos de avaliação do sistema RAG, incluindo detecção automática de dependências e fallback para métodos alternativos.

## Funcionalidades

### Detecção Automática de Dependências
O script verifica automaticamente se as dependências necessárias para avaliação completa (RAGAS) estão disponíveis.

### Execução Adaptativa
Baseado na disponibilidade de dependências, executa:
- **Avaliação Completa**: Se RAGAS estiver disponível
- **Avaliação Simplificada**: Como fallback se RAGAS não estiver disponível

### Tratamento de Erros
Implementa fallback automático em caso de falhas na avaliação completa.

## Arquitetura

### Funções Principais

#### `check_ragas_availability() -> bool`
Verifica se as dependências RAGAS estão disponíveis.

**Verificações:**
- `ragas`: Framework principal
- `datasets`: Manipulação de datasets

**Retorno:** `True` se disponível, `False` caso contrário

#### `main()`
Função principal que coordena a execução da avaliação.

**Fluxo:**
1. Verifica disponibilidade do RAGAS
2. Executa avaliação apropriada
3. Implementa fallback em caso de erro

#### `run_simple_evaluation()`
Executa avaliação simplificada como fallback.

**Funcionalidades:**
- Importa e executa `simple_eval.py`
- Trata erros de execução
- Fornece feedback sobre falhas

## Dependências

### Condicionais
- `ragas`: Para avaliação completa (opcional)
- `datasets`: Para avaliação completa (opcional)

### Obrigatórias
- `os`: Operações do sistema
- `sys`: Sistema e caminhos
- `logging`: Sistema de logs

### Internas
- `rag_evaluation`: Módulo de avaliação completa
- `simple_eval`: Módulo de avaliação simplificada

## Uso

### Execução Direta
```bash
python3 eval/run_evaluation.py
```

### Integração
```python
from eval.run_evaluation import main

main()
```

## Fluxo de Execução

### 1. Verificação de Dependências
```python
if check_ragas_availability():
    # Executar avaliação completa
else:
    # Executar avaliação simplificada
```

### 2. Execução de Avaliação
- **Com RAGAS**: Chama `rag_evaluation.main()`
- **Sem RAGAS**: Chama `simple_eval.main()`

### 3. Tratamento de Erros
- Falha na avaliação completa → Fallback para simplificada
- Falha na avaliação simplificada → Relatório de erro

## Logs

### Mensagens de Informação
- Status de disponibilidade do RAGAS
- Tipo de avaliação sendo executada
- Instruções de instalação

### Mensagens de Erro
- Falhas na importação de módulos
- Erros de execução
- Falhas completas de avaliação

## Casos de Uso

### Cenário 1: RAGAS Disponível
```
INFO: ✅ RAGAS disponível - executando avaliação completa
INFO: 🚀 Iniciando avaliação do sistema RAG...
```

### Cenário 2: RAGAS Não Disponível
```
WARNING: ⚠️ RAGAS não disponível - executando avaliação simplificada
INFO: 💡 Para instalar RAGAS: python eval/install_dependencies.py
INFO: 🚀 Iniciando avaliação simplificada do sistema RAG...
```

### Cenário 3: Falha na Avaliação Completa
```
ERROR: ❌ Erro na avaliação RAGAS: [erro]
INFO: 🔄 Fallback para avaliação simplificada...
```

## Vantagens

### Flexibilidade
- Adaptação automática às dependências disponíveis
- Fallback robusto para métodos alternativos
- Execução sem configuração manual

### Robustez
- Tratamento de erros abrangente
- Múltiplos níveis de fallback
- Feedback claro sobre problemas

### Facilidade de Uso
- Execução simples com um comando
- Detecção automática de ambiente
- Instruções claras de resolução

## Limitações

### Dependências
- Requer módulos de avaliação internos
- Dependente de estrutura de diretórios
- Limitações dos módulos subjacentes

### Funcionalidades
- Não implementa avaliação própria
- Dependente de outros módulos
- Limitado aos métodos disponíveis

## Configuração

### Variáveis de Ambiente
- `OPENAI_API_KEY`: Para sistema RAG subjacente
- `HUGGINGFACE_API_KEY`: Para embeddings (opcional)

### Estrutura de Diretórios
```
eval/
├── run_evaluation.py
├── rag_evaluation.py
├── simple_eval.py
└── questions_and_answers.json
```

## Troubleshooting

### Problemas Comuns

#### 1. Módulos Não Encontrados
```
ModuleNotFoundError: No module named 'rag_evaluation'
```
**Solução:** Verificar estrutura de diretórios

#### 2. Falha na Importação RAGAS
```
ImportError: No module named 'ragas'
```
**Solução:** Instalar dependências ou usar avaliação simplificada

#### 3. Erro no Sistema RAG
```
ERROR: ❌ Erro na avaliação simplificada
```
**Solução:** Verificar configuração do sistema RAG

### Diagnóstico
1. Verificar logs de erro
2. Validar dependências
3. Testar módulos individuais
4. Verificar configuração

## Integração

### Com Scripts de Instalação
```bash
python eval/install_dependencies.py
python eval/run_evaluation.py
```

### Com CI/CD
```yaml
- name: Run RAG Evaluation
  run: python eval/run_evaluation.py
```

### Com Outros Módulos
```python
from eval.run_evaluation import check_ragas_availability

if check_ragas_availability():
    # Executar avaliação completa
    pass
else:
    # Usar métodos alternativos
    pass
```

## Manutenção

### Atualizações Recomendadas
- Verificar compatibilidade com novos módulos
- Atualizar mensagens de erro
- Melhorar detecção de dependências
- Expandir opções de fallback

### Monitoramento
- Taxa de sucesso das avaliações
- Frequência de fallbacks
- Tempo de execução
- Erros mais comuns

## Versionamento

- **v1.0**: Implementação inicial com detecção básica
- **v1.1**: Melhoria no tratamento de erros
- **v1.2**: Adição de logs informativos
- **v1.3**: Otimização de fallbacks

## Contribuição

Para contribuir com melhorias:
1. Manter compatibilidade com módulos existentes
2. Adicionar testes para diferentes cenários
3. Documentar novos casos de uso
4. Validar fallbacks

---

*Documentação gerada automaticamente - Sistema RAG Autismo v1.0*