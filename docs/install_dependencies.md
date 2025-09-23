# Install Dependencies Module

## Visão Geral

O módulo `install_dependencies.py` automatiza a instalação das dependências necessárias para execução completa do sistema de avaliação RAG, incluindo RAGAS e outras bibliotecas essenciais.

## Funcionalidades

### Instalação Automática
Instala automaticamente todas as dependências necessárias para avaliação completa.

### Verificação de Sucesso
Monitora o processo de instalação e relata o status de cada pacote.

### Feedback Detalhado
Fornece feedback claro sobre sucessos e falhas na instalação.

## Arquitetura

### Funções Principais

#### `install_package(package: str) -> bool`
Instala um pacote Python específico usando pip.

**Parâmetros:**
- `package`: Nome e versão do pacote a ser instalado

**Retorno:** `True` se instalado com sucesso, `False` caso contrário

**Funcionalidades:**
- Execução via subprocess
- Captura de erros
- Feedback visual

#### `main()`
Função principal que coordena a instalação de todos os pacotes.

**Fluxo:**
1. Lista pacotes necessários
2. Instala cada pacote individualmente
3. Conta sucessos e falhas
4. Fornece relatório final

## Dependências Instaladas

### Principais
- **ragas>=0.1.0**: Framework de avaliação RAG
- **datasets>=2.14.0**: Manipulação de datasets
- **openai>=1.3.0**: Cliente OpenAI

### LangChain
- **langchain>=0.3.0**: Framework principal
- **langchain-openai>=0.0.2**: Integração OpenAI

### Vector Store e Embeddings
- **chromadb>=1.0.0**: Banco vetorial
- **sentence-transformers>=2.2.0**: Modelos de embedding

## Uso

### Execução Direta
```bash
python3 eval/install_dependencies.py
```

### Integração
```python
from eval.install_dependencies import install_package

success = install_package("ragas>=0.1.0")
```

## Fluxo de Execução

### 1. Inicialização
```python
print("🚀 Instalando dependências para avaliação RAGAS...")
```

### 2. Instalação de Pacotes
```python
for package in packages:
    if install_package(package):
        success_count += 1
```

### 3. Relatório Final
```python
print(f"📊 Resultado: {success_count}/{len(packages)} pacotes instalados")
```

## Logs e Feedback

### Mensagens de Sucesso
```
✅ ragas>=0.1.0 instalado com sucesso
✅ datasets>=2.14.0 instalado com sucesso
```

### Mensagens de Erro
```
❌ Erro ao instalar ragas>=0.1.0: CalledProcessError
```

### Relatório Final
```
📊 Resultado: 6/7 pacotes instalados
✅ Todas as dependências foram instaladas com sucesso!
Execute: python eval/rag_evaluation.py
```

## Tratamento de Erros

### Tipos de Erro
1. **CalledProcessError**: Falha na execução do pip
2. **NetworkError**: Problemas de conectividade
3. **PermissionError**: Falta de permissões
4. **VersionConflict**: Conflitos de versão

### Estratégias
- Captura individual de erros por pacote
- Continuação da instalação após falhas
- Relatório detalhado de problemas
- Instruções de resolução

## Vantagens

### Automação
- Instalação sem intervenção manual
- Processo padronizado e reproduzível
- Verificação automática de sucesso

### Robustez
- Tratamento de erros por pacote
- Continuidade após falhas
- Feedback claro sobre problemas

### Facilidade de Uso
- Execução simples
- Instruções claras
- Integração com outros módulos

## Limitações

### Dependências do Sistema
- Requer Python e pip funcionais
- Dependente de conectividade de rede
- Pode precisar de permissões elevadas

### Compatibilidade
- Versões específicas de pacotes
- Possíveis conflitos de dependências
- Dependência de ambientes Python

## Configuração

### Pré-requisitos
- Python 3.8+ instalado
- pip funcional
- Conectividade de rede
- Permissões de instalação

### Variáveis de Ambiente
- `PIP_INDEX_URL`: URL do índice pip (opcional)
- `PIP_TRUSTED_HOST`: Hosts confiáveis (opcional)

## Casos de Uso

### Desenvolvimento
```bash
# Instalar dependências para desenvolvimento
python eval/install_dependencies.py
```

### CI/CD
```yaml
- name: Install Dependencies
  run: python eval/install_dependencies.py
```

### Produção
```bash
# Verificar e instalar dependências
python eval/install_dependencies.py
python eval/rag_evaluation.py
```

## Troubleshooting

### Problemas Comuns

#### 1. Falha na Instalação do RAGAS
```
❌ Erro ao instalar ragas>=0.1.0
```
**Solução:** Verificar conectividade e permissões

#### 2. Conflitos de Versão
```
ERROR: pip's dependency resolver does not support
```
**Solução:** Atualizar pip ou usar ambientes virtuais

#### 3. Permissões Insuficientes
```
PermissionError: [Errno 13] Permission denied
```
**Solução:** Usar `--user` ou ambiente virtual

### Diagnóstico
1. Verificar versão do Python
2. Validar funcionamento do pip
3. Testar conectividade de rede
4. Verificar permissões

## Integração

### Com Scripts de Avaliação
```bash
python eval/install_dependencies.py
python eval/run_evaluation.py
```

### Com Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate
python eval/install_dependencies.py
```

### Com Docker
```dockerfile
RUN python eval/install_dependencies.py
```

## Manutenção

### Atualizações Recomendadas
- Revisar versões dos pacotes
- Atualizar lista de dependências
- Melhorar tratamento de erros
- Adicionar validações

### Monitoramento
- Taxa de sucesso de instalação
- Erros mais comuns
- Tempo de instalação
- Conflitos de dependências

## Versionamento

- **v1.0**: Implementação inicial básica
- **v1.1**: Melhoria no tratamento de erros
- **v1.2**: Adição de feedback detalhado
- **v1.3**: Otimização de pacotes

## Alternativas

### Instalação Manual
```bash
pip install ragas>=0.1.0
pip install datasets>=2.14.0
pip install openai>=1.3.0
```

### Requirements.txt
```bash
pip install -r requirements.txt
```

### Conda
```bash
conda install -c conda-forge ragas
```

## Contribuição

Para contribuir com melhorias:
1. Manter compatibilidade com Python 3.8+
2. Adicionar novos pacotes conforme necessário
3. Melhorar tratamento de erros
4. Documentar novos casos de uso

---

*Documentação gerada automaticamente - Sistema RAG Autismo v1.0*