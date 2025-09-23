import json
import logging
from typing import List, Dict, Any
from datetime import datetime
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleRAGEvaluator:
    def __init__(self):
        self.rag_system = None
        self.evaluation_data = None
        
    def load_questions(self, questions_file: str = "eval/questions_and_answers.json"):
        try:
            with open(questions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.evaluation_data = data['evaluation_questions']
            logger.info(f"✅ Carregadas {len(self.evaluation_data)} perguntas de avaliação")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao carregar perguntas: {e}")
            return False
    
    def initialize_rag_system(self):
        try:
            from src.graph.rag_graph import create_rag_graph
            self.rag_system = create_rag_graph()
            logger.info("✅ Sistema RAG inicializado")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar sistema RAG: {e}")
            return False
    
    def generate_responses(self, max_questions: int = 10) -> List[Dict[str, Any]]:
        if not self.rag_system:
            logger.error("❌ Sistema RAG não inicializado")
            return []
        
        results = []
        questions_to_process = self.evaluation_data[:max_questions]
        
        logger.info(f"🚀 Gerando respostas para {len(questions_to_process)} perguntas...")
        
        for i, question_data in enumerate(questions_to_process, 1):
            try:
                logger.info(f"📝 Processando pergunta {i}/{len(questions_to_process)}: {question_data['question'][:50]}...")
                
                response = self.rag_system.process_query_simple(question_data['question'])
                
                result = {
                    "question": question_data['question'],
                    "answer": response,
                    "ground_truth": question_data['ground_truth'],
                    "question_id": question_data['id'],
                    "domain": question_data.get('domain', 'geral'),
                    "source": question_data.get('source', ''),
                    "expected_citations": question_data.get('expected_citations', [])
                }
                
                results.append(result)
                logger.info(f"✅ Pergunta {i} processada")
                
            except Exception as e:
                logger.error(f"❌ Erro ao processar pergunta {i}: {e}")
                results.append({
                    "question": question_data['question'],
                    "answer": f"Erro: {str(e)}",
                    "ground_truth": question_data['ground_truth'],
                    "question_id": question_data['id'],
                    "domain": question_data.get('domain', 'geral'),
                    "source": question_data.get('source', ''),
                    "expected_citations": question_data.get('expected_citations', [])
                })
        
        logger.info(f"✅ Respostas geradas para {len(results)} perguntas")
        return results
    
    def calculate_metrics(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_questions = len(responses)
        successful_responses = 0
        responses_with_citations = 0
        responses_with_disclaimers = 0
        responses_with_keywords = 0
        domain_accuracy = {"saúde": 0, "direito": 0, "educação": 0}
        domain_count = {"saúde": 0, "direito": 0, "educação": 0}
        
        for response in responses:
            answer = response["answer"].lower()
            
            if not response["answer"].startswith("Erro:"):
                successful_responses += 1
            
            if "fonte" in answer or "documento" in answer or "consulta" in answer:
                responses_with_citations += 1
            
            if "importante" in answer or "consulte" in answer or "não substitui" in answer:
                responses_with_disclaimers += 1
            
            expected_keywords = response["expected_citations"]
            if any(keyword.lower() in answer for keyword in expected_keywords):
                responses_with_keywords += 1
            
            domain = response["domain"]
            if domain in domain_count:
                domain_count[domain] += 1
                if not response["answer"].startswith("Erro:"):
                    domain_accuracy[domain] += 1
        
        success_rate = successful_responses / total_questions if total_questions > 0 else 0
        citation_rate = responses_with_citations / total_questions if total_questions > 0 else 0
        disclaimer_rate = responses_with_disclaimers / total_questions if total_questions > 0 else 0
        keyword_match_rate = responses_with_keywords / total_questions if total_questions > 0 else 0
        
        domain_precision = {}
        for domain in domain_accuracy:
            if domain_count[domain] > 0:
                domain_precision[domain] = domain_accuracy[domain] / domain_count[domain]
            else:
                domain_precision[domain] = 0.0
        
        return {
            "success_rate": success_rate,
            "citation_rate": citation_rate,
            "disclaimer_rate": disclaimer_rate,
            "keyword_match_rate": keyword_match_rate,
            "domain_accuracy": domain_precision,
            "total_questions": total_questions,
            "successful_responses": successful_responses,
            "responses_with_citations": responses_with_citations,
            "responses_with_disclaimers": responses_with_disclaimers,
            "responses_with_keywords": responses_with_keywords
        }
    
    def generate_simple_report(self, metrics: Dict[str, Any], responses: List[Dict[str, Any]]) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""# Relatório de Avaliação Simplificada - Sistema RAG Autismo

**Data da Avaliação:** {timestamp}
**Total de Perguntas:** {metrics['total_questions']}

## 📊 Resumo Executivo

### Métricas Principais
- **Taxa de Sucesso:** {metrics['success_rate']:.2%}
- **Taxa de Citações:** {metrics['citation_rate']:.2%}
- **Taxa de Disclaimers:** {metrics['disclaimer_rate']:.2%}
- **Taxa de Palavras-chave:** {metrics['keyword_match_rate']:.2%}

## 🎯 Análise por Domínio

"""
        
        for domain, accuracy in metrics['domain_accuracy'].items():
            count = sum(1 for r in responses if r['domain'] == domain)
            report += f"- **{domain.title()}:** {accuracy:.2%} ({count} perguntas)\n"
        
        report += f"""

## 📈 Detalhes das Métricas

### Taxa de Sucesso
- **Respostas Bem-sucedidas:** {metrics['successful_responses']}/{metrics['total_questions']}
- **Taxa:** {metrics['success_rate']:.2%}

### Qualidade das Respostas
- **Com Citações:** {metrics['responses_with_citations']}/{metrics['total_questions']} ({metrics['citation_rate']:.2%})
- **Com Disclaimers:** {metrics['responses_with_disclaimers']}/{metrics['total_questions']} ({metrics['disclaimer_rate']:.2%})
- **Com Palavras-chave:** {metrics['responses_with_keywords']}/{metrics['total_questions']} ({metrics['keyword_match_rate']:.2%})

## 🔍 Análise de Problemas

"""
        
        error_responses = [r for r in responses if r["answer"].startswith("Erro:")]
        
        if error_responses:
            report += f"### Respostas com Erro ({len(error_responses)})\n"
            for error in error_responses[:3]:
                report += f"- **Pergunta {error['question_id']}:** {error['question'][:50]}...\n"
        
        successful_responses = [r for r in responses if not r["answer"].startswith("Erro:")]
        if successful_responses:
            report += f"\n### Exemplos de Respostas Bem-sucedidas\n\n"
            for i, response in enumerate(successful_responses[:2], 1):
                report += f"**Exemplo {i}:**\n"
                report += f"- **Pergunta:** {response['question']}\n"
                report += f"- **Resposta:** {response['answer'][:200]}...\n\n"
        
        report += f"""

## 📋 Recomendações

1. **Melhorar Taxa de Sucesso:** Resolver erros de processamento
2. **Padronizar Citações:** Implementar formato consistente
3. **Garantir Disclaimers:** Adicionar em todas as respostas
4. **Aumentar Relevância:** Melhorar matching de palavras-chave
5. **Monitorar por Domínio:** Acompanhar performance específica

## 📊 Métricas Detalhadas

```json
{json.dumps(metrics, indent=2, ensure_ascii=False)}
```

---
*Relatório gerado pelo sistema de avaliação simplificada*
"""
        
        return report
    
    def save_results(self, metrics: Dict[str, Any], responses: List[Dict[str, Any]], report: str):
        os.makedirs("eval", exist_ok=True)
        
        with open("eval/simple_report.md", "w", encoding="utf-8") as f:
            f.write(report)
        
        results_data = {
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics,
            "responses": responses,
            "summary": {
                "total_questions": metrics['total_questions'],
                "success_rate": metrics['success_rate'],
                "citation_rate": metrics['citation_rate'],
                "disclaimer_rate": metrics['disclaimer_rate']
            }
        }
        
        with open("eval/simple_results.json", "w", encoding="utf-8") as f:
            json.dump(results_data, f, indent=2, ensure_ascii=False)
        
        logger.info("✅ Resultados salvos em eval/simple_report.md e eval/simple_results.json")

def main():
    logger.info("🚀 Iniciando avaliação simplificada do sistema RAG...")
    
    evaluator = SimpleRAGEvaluator()
    
    if not evaluator.load_questions():
        logger.error("❌ Falha ao carregar perguntas")
        return
    
    if not evaluator.initialize_rag_system():
        logger.error("❌ Falha ao inicializar sistema RAG")
        return
    
    responses = evaluator.generate_responses(max_questions=10)
    if not responses:
        logger.error("❌ Falha ao gerar respostas")
        return
    
    metrics = evaluator.calculate_metrics(responses)
    report = evaluator.generate_simple_report(metrics, responses)
    evaluator.save_results(metrics, responses, report)
    
    logger.info("=" * 50)
    logger.info("📊 RESUMO DA AVALIAÇÃO SIMPLIFICADA")
    logger.info("=" * 50)
    logger.info(f"Total de perguntas: {metrics['total_questions']}")
    logger.info(f"Taxa de sucesso: {metrics['success_rate']:.2%}")
    logger.info(f"Taxa de citações: {metrics['citation_rate']:.2%}")
    logger.info(f"Taxa de disclaimers: {metrics['disclaimer_rate']:.2%}")
    logger.info(f"Taxa de palavras-chave: {metrics['keyword_match_rate']:.2%}")
    logger.info("=" * 50)
    logger.info("✅ Avaliação simplificada concluída! Verifique eval/simple_report.md para detalhes.")

if __name__ == "__main__":
    main()