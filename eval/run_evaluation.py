import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_ragas_availability():
    try:
        import ragas
        import datasets
        return True
    except ImportError:
        return False

def main():
    logger.info("🚀 Iniciando avaliação do sistema RAG...")
    
    if check_ragas_availability():
        logger.info("✅ RAGAS disponível - executando avaliação completa")
        try:
            from rag_evaluation import main as ragas_main
            ragas_main()
        except Exception as e:
            logger.error(f"❌ Erro na avaliação RAGAS: {e}")
            logger.info("🔄 Fallback para avaliação simplificada...")
            run_simple_evaluation()
    else:
        logger.warning("⚠️ RAGAS não disponível - executando avaliação simplificada")
        logger.info("💡 Para instalar RAGAS: python eval/install_dependencies.py")
        run_simple_evaluation()

def run_simple_evaluation():
    try:
        from simple_eval import main as simple_main
        simple_main()
    except Exception as e:
        logger.error(f"❌ Erro na avaliação simplificada: {e}")
        logger.error("❌ Falha completa na avaliação")

if __name__ == "__main__":
    main()