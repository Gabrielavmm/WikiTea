import os
import sys
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PaperQABaseline:
    def __init__(self):
        self.qa_system = None
        self.documents_added = []
        
    def install_paperqa(self):
        try:
            import paperqa
            logger.info("✅ PaperQA já está instalado")
            return True
        except ImportError:
            logger.info("📦 Instalando PaperQA...")
            try:
                import subprocess
                subprocess.check_call([sys.executable, "-m", "pip", "install", "paperqa"])
                logger.info("✅ PaperQA instalado com sucesso")
                return True
            except Exception as e:
                logger.error(f"❌ Erro ao instalar PaperQA: {e}")
                return False
    
    def initialize_system(self):
        try:
            if not self.install_paperqa():
                return False
                
            from paperqa import PaperQA
            
            self.qa_system = PaperQA(
                llm="gpt-3.5-turbo",
                embeddings="text-embedding-ada-002",
                max_sources=10,
                max_tokens=4000,
                chunk_size=1000,
                chunk_overlap=200
            )
            
            logger.info("✅ Sistema PaperQA inicializado")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar PaperQA: {e}")
            return False
    
    def add_autism_documents(self, document_paths: List[str]):
        if not self.qa_system:
            logger.error("❌ Sistema PaperQA não inicializado")
            return False
        
        try:
            for doc_path in document_paths:
                if os.path.exists(doc_path):
                    self.qa_system.add_paper(doc_path)
                    self.documents_added.append(doc_path)
                    logger.info(f"✅ Documento adicionado: {doc_path}")
                else:
                    logger.warning(f"⚠️ Documento não encontrado: {doc_path}")
            
            logger.info(f"✅ Total de documentos adicionados: {len(self.documents_added)}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao adicionar documentos: {e}")
            return False
    
    def query_system(self, question: str) -> Dict[str, Any]:
        if not self.qa_system:
            logger.error("❌ Sistema PaperQA não inicializado")
            return {"error": "Sistema não inicializado"}
        
        try:
            logger.info(f"🔍 PaperQA: Processando pergunta: {question[:50]}...")
            
            answer = self.qa_system.query(question)
            
            result = {
                "question": question,
                "answer": answer.answer,
                "sources": [source for source in answer.sources],
                "confidence": getattr(answer, 'confidence', 0.0),
                "citations": len(answer.sources),
                "method": "PaperQA2"
            }
            
            logger.info(f"✅ PaperQA: Resposta gerada com {len(answer.sources)} citações")
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro na consulta PaperQA: {e}")
            return {"error": str(e), "question": question}
    
    def compare_with_rag(self, questions: List[str], rag_responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not self.qa_system:
            logger.error("❌ Sistema PaperQA não inicializado")
            return {}
        
        logger.info(f"🔄 Comparando {len(questions)} perguntas...")
        
        paperqa_responses = []
        comparison_results = {
            "paperqa_responses": [],
            "rag_responses": rag_responses,
            "comparison_metrics": {},
            "total_questions": len(questions)
        }
        
        for i, question in enumerate(questions):
            try:
                paperqa_result = self.query_system(question)
                paperqa_responses.append(paperqa_result)
                
                if i < len(rag_responses):
                    rag_response = rag_responses[i]
                    
                    comparison = {
                        "question_id": i + 1,
                        "question": question,
                        "paperqa_has_answer": "answer" in paperqa_result and not paperqa_result.get("error"),
                        "rag_has_answer": not rag_response.get("answer", "").startswith("Erro:"),
                        "paperqa_citations": paperqa_result.get("citations", 0),
                        "rag_citations": 1 if "fonte" in rag_response.get("answer", "").lower() else 0,
                        "paperqa_confidence": paperqa_result.get("confidence", 0.0),
                        "length_comparison": {
                            "paperqa": len(paperqa_result.get("answer", "")),
                            "rag": len(rag_response.get("answer", ""))
                        }
                    }
                    
                    comparison_results["comparison_metrics"][f"question_{i+1}"] = comparison
                
            except Exception as e:
                logger.error(f"❌ Erro ao processar pergunta {i+1}: {e}")
        
        comparison_results["paperqa_responses"] = paperqa_responses
        
        total_questions = len(questions)
        paperqa_success = sum(1 for r in paperqa_responses if not r.get("error"))
        rag_success = sum(1 for r in rag_responses if not r.get("answer", "").startswith("Erro:"))
        
        comparison_results["summary"] = {
            "paperqa_success_rate": paperqa_success / total_questions if total_questions > 0 else 0,
            "rag_success_rate": rag_success / total_questions if total_questions > 0 else 0,
            "paperqa_avg_citations": sum(r.get("citations", 0) for r in paperqa_responses) / total_questions if total_questions > 0 else 0,
            "rag_avg_citations": sum(1 if "fonte" in r.get("answer", "").lower() else 0 for r in rag_responses) / total_questions if total_questions > 0 else 0
        }
        
        logger.info("✅ Comparação concluída")
        return comparison_results

def main():
    logger.info("🚀 Iniciando configuração do PaperQA baseline...")
    
    baseline = PaperQABaseline()
    
    if not baseline.initialize_system():
        logger.error("❌ Falha ao inicializar PaperQA")
        return
    
    document_paths = [
        "data/autism_documents.pdf",
        "data/autism_research.pdf",
        "data/autism_guidelines.pdf"
    ]
    
    available_docs = [doc for doc in document_paths if os.path.exists(doc)]
    if not available_docs:
        logger.warning("⚠️ Nenhum documento encontrado. Criando exemplo...")
        create_sample_document()
        available_docs = ["data/sample_autism_doc.txt"]
    
    baseline.add_autism_documents(available_docs)
    
    test_questions = [
        "O que é o Transtorno do Espectro Autista?",
        "Quais são os sinais precoces de autismo?",
        "Como funciona o diagnóstico de autismo?"
    ]
    
    logger.info("🧪 Testando PaperQA com perguntas de exemplo...")
    for question in test_questions:
        result = baseline.query_system(question)
        logger.info(f"Pergunta: {question}")
        logger.info(f"Resposta: {result.get('answer', 'Erro')[:100]}...")
        logger.info(f"Citações: {result.get('citations', 0)}")
        logger.info("-" * 50)
    
    logger.info("✅ Configuração do PaperQA baseline concluída!")

def create_sample_document():
    os.makedirs("data", exist_ok=True)
    
    sample_content = """
    Transtorno do Espectro Autista (TEA) - Documento de Referência
    
    O Transtorno do Espectro Autista (TEA) é uma condição do desenvolvimento neurológico 
    caracterizada por dificuldades persistentes na comunicação social e interação social, 
    bem como padrões restritos e repetitivos de comportamento, interesses ou atividades.
    
    Sinais Precoces:
    - Falta de contato visual
    - Não responder ao nome
    - Atraso na fala
    - Movimentos repetitivos
    
    Diagnóstico:
    - Realizado por equipe multidisciplinar
    - Baseado em critérios do DSM-5
    - Inclui instrumentos como ADOS-2
    
    Terapias:
    - Análise do Comportamento Aplicada (ABA)
    - Terapia Ocupacional
    - Fonoaudiologia
    
    Fonte: Organização Mundial da Saúde (OMS)
    """
    
    with open("data/sample_autism_doc.txt", "w", encoding="utf-8") as f:
        f.write(sample_content)
    
    logger.info("✅ Documento de exemplo criado em data/sample_autism_doc.txt")

if __name__ == "__main__":
    main()