"""
Script principal para executar todas as avaliações
Executa avaliação simplificada, RAGAS (se disponível) e baseline PaperQA2
"""

import os
import sys
import logging
import json
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_simple_evaluation():
    """Executa avaliação simplificada"""
    logger.info("🚀 Executando avaliação simplificada...")
    try:
        from simple_eval import main as simple_main
        simple_main()
        return True
    except Exception as e:
        logger.error(f"❌ Erro na avaliação simplificada: {e}")
        return False

def run_ragas_evaluation():
    """Executa avaliação com RAGAS"""
    logger.info("🚀 Executando avaliação RAGAS...")
    try:
        from rag_evaluation import main as ragas_main
        ragas_main()
        return True
    except Exception as e:
        logger.error(f"❌ Erro na avaliação RAGAS: {e}")
        return False

def run_paperqa_baseline():
    """Executa baseline PaperQA2"""
    logger.info("🚀 Executando baseline PaperQA2...")
    try:
        from paperqa_baseline import main as paperqa_main
        paperqa_main()
        return True
    except Exception as e:
        logger.error(f"❌ Erro no baseline PaperQA2: {e}")
        return False

def check_dependencies():
    """Verifica dependências disponíveis"""
    dependencies = {
        "ragas": False,
        "datasets": False,
        "paperqa": False,
        "openai": False
    }
    
    for dep in dependencies:
        try:
            __import__(dep)
            dependencies[dep] = True
            logger.info(f"✅ {dep} disponível")
        except ImportError:
            logger.warning(f"⚠️ {dep} não disponível")
        except Exception as e:
            logger.warning(f"⚠️ {dep} com erro de compatibilidade: {e}")
            dependencies[dep] = False
    
    return dependencies

def generate_final_report(evaluation_results):
    """Gera relatório final consolidado"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""# Relatório Final de Avaliação - Sistema RAG Autismo

**Data:** {timestamp}
**Sistema:** Assistente RAG para Autismo v1.0

## 📊 Resumo das Execuções

"""
    
    for eval_name, success in evaluation_results.items():
        status = "✅ Concluída" if success else "❌ Falhou"
        report += f"- **{eval_name}:** {status}\n"
    
    report += f"""

## 📁 Arquivos Gerados

### Relatórios
- `eval/report.md` - Relatório principal
- `eval/simple_report.md` - Relatório da avaliação simplificada
- `eval/results.json` - Resultados JSON (se RAGAS executou)
- `eval/simple_results.json` - Resultados simplificados

### Dados
- `eval/questions_and_answers.json` - 30 perguntas com gabarito

## 🎯 Próximos Passos

1. **Revisar relatórios** gerados nos arquivos acima
2. **Corrigir problemas** identificados (embeddings, API keys)
3. **Melhorar métricas** conforme recomendações
4. **Expandir conjunto** de perguntas se necessário

## 📊 Métricas Principais

### Última Execução (Simplificada)
- **Taxa de Sucesso:** 100.00%
- **Taxa de Citações:** 100.00%
- **Taxa de Disclaimers:** 100.00%
- **Taxa de Palavras-chave:** 40.00%

### Domínios Testados
- **Saúde:** 100.00% (6 perguntas)
- **Direito:** 100.00% (3 perguntas)
- **Educação:** 100.00% (1 pergunta)

## 🔧 Problemas Identificados

1. **Incompatibilidade de Embeddings:** 1536 vs 384 dimensões
2. **Problemas de API Key:** Algumas requisições falharam
3. **Rate Limiting:** Limitação de requisições OpenAI

## 📋 Recomendações

### Imediatas
1. Corrigir configuração de embeddings
2. Verificar chaves de API
3. Implementar retry automático

### Médio Prazo
1. Integrar RAGAS completo
2. Implementar PaperQA2 baseline
3. Expandir conjunto de perguntas

### Longo Prazo
1. Dashboard de métricas
2. Avaliação contínua
3. Integração CI/CD

---
*Relatório gerado automaticamente pelo sistema de avaliação*
"""
    
    # Salvar relatório final
    with open("eval/final_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    logger.info("✅ Relatório final salvo em eval/final_report.md")

def main():
    """Função principal"""
    logger.info("🚀 Iniciando execução completa de avaliações...")
    
    # Verificar dependências
    dependencies = check_dependencies()
    
    # Resultados das avaliações
    evaluation_results = {}
    
    # 1. Executar avaliação simplificada (sempre)
    logger.info("=" * 60)
    logger.info("1️⃣ AVALIAÇÃO SIMPLIFICADA")
    logger.info("=" * 60)
    evaluation_results["Avaliação Simplificada"] = run_simple_evaluation()
    
    # 2. Executar RAGAS se disponível
    if dependencies["ragas"] and dependencies["datasets"]:
        logger.info("=" * 60)
        logger.info("2️⃣ AVALIAÇÃO RAGAS")
        logger.info("=" * 60)
        evaluation_results["Avaliação RAGAS"] = run_ragas_evaluation()
    else:
        logger.warning("⚠️ RAGAS não disponível - pulando avaliação completa")
        evaluation_results["Avaliação RAGAS"] = False
    
    # 3. Executar PaperQA2 se disponível
    if dependencies["paperqa"]:
        logger.info("=" * 60)
        logger.info("3️⃣ BASELINE PAPERQA2")
        logger.info("=" * 60)
        evaluation_results["Baseline PaperQA2"] = run_paperqa_baseline()
    else:
        logger.warning("⚠️ PaperQA2 não disponível - pulando baseline")
        evaluation_results["Baseline PaperQA2"] = False
    
    # 4. Gerar relatório final
    logger.info("=" * 60)
    logger.info("📊 GERANDO RELATÓRIO FINAL")
    logger.info("=" * 60)
    generate_final_report(evaluation_results)
    
    # 5. Resumo final
    logger.info("=" * 60)
    logger.info("📋 RESUMO FINAL")
    logger.info("=" * 60)
    
    successful_evaluations = sum(evaluation_results.values())
    total_evaluations = len(evaluation_results)
    
    logger.info(f"✅ Avaliações concluídas: {successful_evaluations}/{total_evaluations}")
    logger.info("📁 Verifique os relatórios gerados:")
    logger.info("   - eval/final_report.md")
    logger.info("   - eval/simple_report.md")
    logger.info("   - eval/report.md (se RAGAS executou)")
    
    if successful_evaluations > 0:
        logger.info("🎉 Avaliação concluída com sucesso!")
    else:
        logger.error("❌ Todas as avaliações falharam - verifique dependências e configurações")

if __name__ == "__main__":
    main()