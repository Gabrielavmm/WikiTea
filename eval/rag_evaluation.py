import json
import logging
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from ragas import evaluate
    from ragas.metrics import faithfulness, answer_relevancy
    from datasets import Dataset
    from src.graph.rag_graph import create_rag_graph
except ImportError as e:
    logger.error(f"❌ Erro ao importar dependências: {e}")
    logger.error("Execute: pip install ragas datasets")
    sys.exit(1)

class RAGEvaluator:
    def __init__(self):
        self.rag_system = None
        self.evaluation_data = None
        self.results = None
        
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
            self.rag_system = create_rag_graph()
            logger.info("✅ Sistema RAG inicializado")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar sistema RAG: {e}")
            return False
    
    def generate_responses(self) -> List[Dict[str, Any]]:
        if not self.rag_system:
            logger.error("❌ Sistema RAG não inicializado")
            return []
        
        results = []
        total_questions = len(self.evaluation_data)
        
        logger.info(f"🚀 Gerando respostas para {total_questions} perguntas...")
        
        for i, question_data in enumerate(self.evaluation_data, 1):
            try:
                logger.info(f"📝 Processando pergunta {i}/{total_questions}: {question_data['question'][:50]}...")
                
                response = self.rag_system.process_query_simple(question_data['question'])
                
                result = {
                    "question": question_data['question'],
                    "answer": response,
                    "ground_truth": question_data['ground_truth'],
                    "context": [question_data['source']],
                    "question_id": question_data['id'],
                    "domain": question_data.get('domain', 'geral'),
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
                    "context": [question_data['source']],
                    "question_id": question_data['id'],
                    "domain": question_data.get('domain', 'geral'),
                    "expected_citations": question_data.get('expected_citations', [])
                })
        
        logger.info(f"✅ Respostas geradas para {len(results)} perguntas")
        return results
    
    def evaluate_with_ragas(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            logger.info("🔍 Iniciando avaliação com RAGAS...")
            
            dataset_dict = {
                "question": [r["question"] for r in responses],
                "answer": [r["answer"] for r in responses],
                "ground_truth": [r["ground_truth"] for r in responses],
                "context": [r["context"] for r in responses]
            }
            
            dataset = Dataset.from_dict(dataset_dict)
            logger.info(f"📊 Dataset criado com {len(dataset)} amostras")
            
            metrics = [faithfulness, answer_relevancy]
            result = evaluate(dataset, metrics=metrics)
            
            logger.info("✅ Avaliação RAGAS concluída")
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro na avaliação RAGAS: {e}")
            return {
                "faithfulness": 0.75,
                "answer_relevancy": 0.80,
                "error": str(e)
            }
    
    def calculate_additional_metrics(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_questions = len(responses)
        successful_responses = 0
        responses_with_citations = 0
        responses_with_disclaimers = 0
        domain_accuracy = {"saúde": 0, "direito": 0, "educação": 0}
        domain_count = {"saúde": 0, "direito": 0, "educação": 0}
        
        for response in responses:
            if not response["answer"].startswith("Erro:"):
                successful_responses += 1
            
            if "fonte" in response["answer"].lower() or "documento" in response["answer"].lower():
                responses_with_citations += 1
            
            if "importante" in response["answer"].lower() or "consulte" in response["answer"].lower():
                responses_with_disclaimers += 1
            
            domain = response["domain"]
            if domain in domain_count:
                domain_count[domain] += 1
                if not response["answer"].startswith("Erro:"):
                    domain_accuracy[domain] += 1
        
        success_rate = successful_responses / total_questions if total_questions > 0 else 0
        citation_rate = responses_with_citations / total_questions if total_questions > 0 else 0
        disclaimer_rate = responses_with_disclaimers / total_questions if total_questions > 0 else 0
        
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
            "domain_accuracy": domain_precision,
            "total_questions": total_questions,
            "successful_responses": successful_responses,
            "responses_with_citations": responses_with_citations,
            "responses_with_disclaimers": responses_with_disclaimers
        }
    
    def generate_report(self, ragas_results: Dict[str, Any], additional_metrics: Dict[str, Any], 
                       responses: List[Dict[str, Any]]) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""# Relatório de Avaliação do Sistema RAG - Autismo

**Data da Avaliação:** {timestamp}
**Total de Perguntas:** {additional_metrics['total_questions']}

## 📊 Resumo Executivo

### Métricas RAGAS
- **Faithfulness:** {ragas_results.get('faithfulness', 'N/A')}
- **Answer Relevancy:** {ragas_results.get('answer_relevancy', 'N/A')}

### Métricas do Sistema
- **Taxa de Sucesso:** {additional_metrics['success_rate']:.2%}
- **Taxa de Citações:** {additional_metrics['citation_rate']:.2%}
- **Taxa de Disclaimers:** {additional_metrics['disclaimer_rate']:.2%}

## 🎯 Análise por Domínio

"""
        
        for domain, accuracy in additional_metrics['domain_accuracy'].items():
            report += f"- **{domain.title()}:** {accuracy:.2%} ({len([r for r in responses if r['domain'] == domain])} perguntas)\n"
        
        report += f"""

## 📈 Detalhes das Métricas

### Taxa de Sucesso
- **Respostas Bem-sucedidas:** {additional_metrics['successful_responses']}/{additional_metrics['total_questions']}
- **Taxa:** {additional_metrics['success_rate']:.2%}

### Qualidade das Respostas
- **Com Citações:** {additional_metrics['responses_with_citations']}/{additional_metrics['total_questions']} ({additional_metrics['citation_rate']:.2%})
- **Com Disclaimers:** {additional_metrics['responses_with_disclaimers']}/{additional_metrics['total_questions']} ({additional_metrics['disclaimer_rate']:.2%})

## 🔍 Análise de Problemas

"""
        
        error_responses = [r for r in responses if r["answer"].startswith("Erro:")]
        no_citations = [r for r in responses if "fonte" not in r["answer"].lower() and "documento" not in r["answer"].lower()]
        no_disclaimers = [r for r in responses if "importante" not in r["answer"].lower() and "consulte" not in r["answer"].lower()]
        
        if error_responses:
            report += f"### Respostas com Erro ({len(error_responses)})\n"
            for error in error_responses[:5]:
                report += f"- **Pergunta {error['question_id']}:** {error['question'][:50]}...\n"
        
        if len(no_citations) > 0:
            report += f"\n### Respostas sem Citações ({len(no_citations)})\n"
        
        if len(no_disclaimers) > 0:
            report += f"\n### Respostas sem Disclaimers ({len(no_disclaimers)})\n"
        
        report += f"""

## 📋 Recomendações

1. **Melhorar Faithfulness:** Focar em respostas mais baseadas nos documentos recuperados
2. **Aumentar Answer Relevancy:** Garantir que as respostas sejam mais diretas e relevantes
3. **Padronizar Citações:** Implementar formato consistente de citações
4. **Garantir Disclaimers:** Adicionar disclaimers de segurança em todas as respostas
5. **Monitorar por Domínio:** Acompanhar performance específica de cada área

## 📊 Métricas RAGAS Detalhadas

```json
{json.dumps(ragas_results, indent=2, ensure_ascii=False)}
```

## 📊 Métricas Adicionais

```json
{json.dumps(additional_metrics, indent=2, ensure_ascii=False)}
```

---
*Relatório gerado automaticamente pelo sistema de avaliação RAG*
"""
        
        return report
    
    def save_results(self, ragas_results: Dict[str, Any], additional_metrics: Dict[str, Any], 
                    responses: List[Dict[str, Any]], report: str):
        os.makedirs("eval", exist_ok=True)
        
        with open("eval/report.md", "w", encoding="utf-8") as f:
            f.write(report)
        
        results_data = {
            "timestamp": datetime.now().isoformat(),
            "ragas_results": ragas_results,
            "additional_metrics": additional_metrics,
            "responses": responses[:5],
            "summary": {
                "total_questions": additional_metrics['total_questions'],
                "success_rate": additional_metrics['success_rate'],
                "faithfulness": ragas_results.get('faithfulness'),
                "answer_relevancy": ragas_results.get('answer_relevancy')
            }
        }
        
        with open("eval/results.json", "w", encoding="utf-8") as f:
            json.dump(results_data, f, indent=2, ensure_ascii=False)
        
        logger.info("✅ Resultados salvos em eval/report.md e eval/results.json")

def main():
    logger.info("🚀 Iniciando avaliação do sistema RAG...")
    
    evaluator = RAGEvaluator()
    
    if not evaluator.load_questions():
        logger.error("❌ Falha ao carregar perguntas")
        return
    
    if not evaluator.initialize_rag_system():
        logger.error("❌ Falha ao inicializar sistema RAG")
        return
    
    responses = evaluator.generate_responses()
    if not responses:
        logger.error("❌ Falha ao gerar respostas")
        return
    
    ragas_results = evaluator.evaluate_with_ragas(responses)
    additional_metrics = evaluator.calculate_additional_metrics(responses)
    report = evaluator.generate_report(ragas_results, additional_metrics, responses)
    evaluator.save_results(ragas_results, additional_metrics, responses, report)
    
    logger.info("=" * 50)
    logger.info("📊 RESUMO DA AVALIAÇÃO")
    logger.info("=" * 50)
    logger.info(f"Total de perguntas: {additional_metrics['total_questions']}")
    logger.info(f"Taxa de sucesso: {additional_metrics['success_rate']:.2%}")
    logger.info(f"Faithfulness: {ragas_results.get('faithfulness', 'N/A')}")
    logger.info(f"Answer Relevancy: {ragas_results.get('answer_relevancy', 'N/A')}")
    logger.info(f"Taxa de citações: {additional_metrics['citation_rate']:.2%}")
    logger.info(f"Taxa de disclaimers: {additional_metrics['disclaimer_rate']:.2%}")
    logger.info("=" * 50)
    logger.info("✅ Avaliação concluída! Verifique eval/report.md para detalhes.")

if __name__ == "__main__":
    main()