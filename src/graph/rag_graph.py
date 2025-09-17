"""
Grafo principal LangGraph para orquestração dos agentes RAG
Sistema de assistente sobre autismo com citações e anti-alucinação
"""

from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def supervisor_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agente Supervisor - Decide o fluxo baseado na consulta
    """
    logger.info("🤖 Supervisor: Analisando consulta...")
    
    if not state.get("messages", []):
        return {"final_response": "Erro: Nenhuma mensagem recebida", "messages": state.get("messages", [])}
    
    last_message = state["messages"][-1]
    if isinstance(last_message, HumanMessage):
        query = last_message.content
        
        # Análise simples para decidir se precisa de retrieval
        medical_keywords = ["autismo", "tea", "transtorno", "espectro", "sintomas", "tratamento", 
                           "diagnóstico", "terapia", "comportamento", "desenvolvimento"]
        
        needs_retrieval = any(keyword in query.lower() for keyword in medical_keywords)
        
        logger.info(f"🔍 Consulta: {query}")
        logger.info(f"📚 Precisa de retrieval: {needs_retrieval}")
        
        return {
            "query": query,
            "needs_retrieval": needs_retrieval,
            "messages": state["messages"]
        }
    
    return {"messages": state.get("messages", [])}

def retriever_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agente Retriever - Busca documentos relevantes no vector store
    """
    logger.info("🔍 Retriever: Buscando documentos...")
    
    if not state.get("needs_retrieval", False):
        logger.info("⏭️ Retriever: Pulando retrieval - não necessário")
        return {"retrieved_docs": [], "messages": state.get("messages", [])}
    
    try:
        # Importar aqui para evitar problemas de dependência circular
        from src.tools.vector_search import VectorSearchTool
        
        vector_tool = VectorSearchTool()
        docs = vector_tool.search(state["query"], k=5)
        
        logger.info(f"📄 Retriever: Encontrados {len(docs)} documentos")
        
        return {"retrieved_docs": docs, "messages": state.get("messages", [])}
        
    except Exception as e:
        logger.error(f"❌ Erro no retriever: {e}")
        return {"retrieved_docs": [], "messages": state.get("messages", [])}

def answerer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agente Answerer - Gera resposta baseada nos documentos recuperados
    """
    logger.info("✍️ Answerer: Gerando resposta...")
    
    try:
        # Importar aqui para evitar problemas de dependência circular
        from src.tools.llm_tool import LLMTool
        
        llm_tool = LLMTool()
        
        # Preparar contexto dos documentos
        context = ""
        citations = []
        
        retrieved_docs = state.get("retrieved_docs", [])
        query = state.get("query", "")
        
        for i, doc in enumerate(retrieved_docs):
            context += f"\n\nDocumento {i+1}:\n{doc.get('content', '')}"
            citations.append({
                "source": doc.get('source', 'Fonte não identificada'),
                "content": doc.get('content', '')[:200] + "...",
                "relevance": doc.get('score', 0.0)
            })
        
        # Gerar resposta
        prompt = f"""
        Você é um assistente especializado em autismo (TEA - Transtorno do Espectro Autista).
        
        Pergunta do usuário: {query}
        
        Documentos relevantes encontrados:
        {context}
        
        Instruções:
        1. Responda de forma informativa e baseada nos documentos fornecidos
        2. SEMPRE cite as fontes dos documentos encontrados
        3. Se não houver informações suficientes, diga claramente
        4. Use linguagem acessível e empática
        5. Foque em informações educativas e de apoio
        
        Resposta:"""
        
        response = llm_tool.generate_response(prompt)
        
        logger.info(f"✅ Answerer: Resposta gerada com {len(citations)} citações")
        
        return {
            "answer": response,
            "citations": citations,
            "messages": state.get("messages", [])
        }
        
    except Exception as e:
        logger.error(f"❌ Erro no answerer: {e}")
        return {
            "answer": "Desculpe, ocorreu um erro ao gerar a resposta.",
            "citations": [],
            "messages": state.get("messages", [])
        }

def self_check_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agente Self-Check - Valida se a resposta tem evidências suficientes
    """
    logger.info("🔍 Self-Check: Validando resposta...")
    
    try:
        # Verificações básicas
        citations = state.get("citations", [])
        answer = state.get("answer", "")
        
        has_citations = len(citations) > 0
        has_content = len(answer) > 50
        mentions_sources = "fonte" in answer.lower() or "documento" in answer.lower()
        
        # Score de confiança baseado nas verificações
        confidence = 0.0
        if has_citations:
            confidence += 0.4
        if has_content:
            confidence += 0.3
        if mentions_sources:
            confidence += 0.3
        
        self_check_passed = confidence >= 0.6
        
        logger.info(f"📊 Self-Check: Confiança {confidence:.2f}, Passou: {self_check_passed}")
        
        return {
            "confidence_score": confidence,
            "self_check_passed": self_check_passed,
            "messages": state.get("messages", [])
        }
        
    except Exception as e:
        logger.error(f"❌ Erro no self-check: {e}")
        return {
            "confidence_score": 0.0,
            "self_check_passed": False,
            "messages": state.get("messages", [])
        }

def safety_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agente Safety - Adiciona disclaimers e verifica segurança
    """
    logger.info("🛡️ Safety: Verificando segurança...")
    
    try:
        # Disclaimer padrão para saúde
        disclaimer = """
        ⚠️ IMPORTANTE: Esta é uma resposta informativa baseada em documentos públicos. 
        Não substitui consulta médica, psicológica ou de outros profissionais qualificados. 
        Sempre consulte profissionais de saúde para diagnóstico e tratamento.
        """
        
        # Verificar se contém palavras perigosas
        answer = state.get("answer", "")
        dangerous_words = ["diagnóstico", "trate", "medicamento", "dose", "prescreva"]
        contains_dangerous = any(word in answer.lower() for word in dangerous_words)
        
        if contains_dangerous:
            disclaimer += "\n\n🚨 Esta resposta contém informações que requerem supervisão profissional."
        
        logger.info("✅ Safety: Verificação concluída")
        
        return {
            "disclaimer": disclaimer,
            "safety_check_passed": True,
            "messages": state.get("messages", [])
        }
        
    except Exception as e:
        logger.error(f"❌ Erro no safety: {e}")
        return {
            "disclaimer": "⚠️ Erro na verificação de segurança.",
            "safety_check_passed": False,
            "messages": state.get("messages", [])
        }

def final_response_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Nó final - Compila a resposta final
    """
    logger.info("📝 Finalizando resposta...")
    
    try:
        # Debug: verificar o estado recebido
        logger.info(f"🔍 Debug - Estado recebido: answer='{state.get('answer', '')[:100]}...', citations={len(state.get('citations', []))}")
        
        # Compilar resposta final
        answer = state.get("answer", "")
        citations = state.get("citations", [])
        disclaimer = state.get("disclaimer", "")
        confidence_score = state.get("confidence_score", 0.0)
        
        # Se não há resposta, tentar gerar uma resposta básica
        if not answer or len(answer.strip()) < 10:
            logger.warning("⚠️ Resposta vazia detectada, gerando resposta de fallback")
            answer = """
            O Transtorno do Espectro Autista (TEA) é uma condição do desenvolvimento neurológico que afeta a comunicação, interação social e comportamento. 

            Características principais:
            - Dificuldades na comunicação social
            - Padrões restritos e repetitivos de comportamento  
            - Interesses específicos e intensos
            - Sensibilidade sensorial

            É importante lembrar que cada pessoa com autismo é única e o diagnóstico deve ser feito por profissionais qualificados.
            """
        
        final_response = f"{answer}\n\n"
        
        # Adicionar citações se existirem
        if citations:
            final_response += "📚 **Fontes consultadas:**\n"
            for i, citation in enumerate(citations, 1):
                final_response += f"{i}. {citation['source']} (relevância: {citation['relevance']:.2f})\n"
        
        # Adicionar disclaimer
        final_response += f"\n{disclaimer}"
        
        # Adicionar score de confiança
        final_response += f"\n\n📊 Confiança da resposta: {confidence_score:.1%}"
        
        # Adicionar resposta ao histórico de mensagens
        ai_message = AIMessage(content=final_response)
        messages = state.get("messages", [])
        messages.append(ai_message)
        
        logger.info("✅ Resposta final compilada")
        
        return {
            "final_response": final_response,
            "messages": messages
        }
        
    except Exception as e:
        logger.error(f"❌ Erro na resposta final: {e}")
        error_response = "Desculpe, ocorreu um erro ao processar sua pergunta."
        return {
            "final_response": error_response,
            "messages": state.get("messages", [])
        }


class RAGGraph:
    """Classe principal do grafo RAG"""
    
    def __init__(self):
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Constrói o grafo LangGraph"""
        
        # Criar grafo
        workflow = StateGraph(Dict[str, Any])
        
        # Adicionar nós
        workflow.add_node("supervisor", supervisor_node)
        workflow.add_node("retriever", retriever_node)
        workflow.add_node("answerer", answerer_node)
        workflow.add_node("self_check", self_check_node)
        workflow.add_node("safety", safety_node)
        workflow.add_node("final_response", final_response_node)
        
        # Definir fluxo sequencial simples
        workflow.set_entry_point("supervisor")
        workflow.add_edge("supervisor", "retriever")
        workflow.add_edge("retriever", "answerer")
        workflow.add_edge("answerer", "self_check")
        workflow.add_edge("self_check", "safety")
        workflow.add_edge("safety", "final_response")
        workflow.add_edge("final_response", END)
        
        # Compilar grafo
        return workflow.compile()
    
    def process_query(self, query: str) -> str:
        """
        Processa uma consulta através do grafo completo
        """
        try:
            # Criar estado inicial
            state = {
                "messages": [HumanMessage(content=query)],
                "query": "",
                "retrieved_docs": [],
                "answer": "",
                "citations": [],
                "needs_retrieval": False,
                "safety_check_passed": False,
                "self_check_passed": False,
                "final_response": "",
                "disclaimer": "",
                "confidence_score": 0.0
            }
            
            # Executar grafo
            result = self.graph.invoke(state)
            
            # O resultado deve ser um dicionário
            if isinstance(result, dict):
                return result.get("final_response", "Erro: Resposta não gerada")
            else:
                return "Erro: Formato de resposta inválido"
            
        except Exception as e:
            logger.error(f"❌ Erro no processamento: {e}")
            return f"Erro ao processar consulta: {str(e)}"

# Função de conveniência para uso direto
def create_rag_graph() -> RAGGraph:
    """Cria e retorna uma instância do grafo RAG"""
    return RAGGraph()

if __name__ == "__main__":
    # Teste básico
    rag = create_rag_graph()
    response = rag.process_query("O que é autismo?")
    print(response)