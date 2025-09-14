"""
Grafo principal LangGraph para orquestração dos agentes RAG
Sistema de assistente sobre autismo com citações e anti-alucinação
"""

from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.runnables import RunnableLambda
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGState:
    """Estado compartilhado entre os agentes"""
    def __init__(self):
        self.messages: List[BaseMessage] = []
        self.query: str = ""
        self.retrieved_docs: List[Dict] = []
        self.answer: str = ""
        self.citations: List[Dict] = []
        self.needs_retrieval: bool = False
        self.safety_check_passed: bool = False
        self.self_check_passed: bool = False
        self.final_response: str = ""
        self.disclaimer: str = ""
        self.confidence_score: float = 0.0

def supervisor_node(state: RAGState) -> Dict[str, Any]:
    """
    Agente Supervisor - Decide o fluxo baseado na consulta
    """
    logger.info("🤖 Supervisor: Analisando consulta...")
    
    if not state.messages:
        return {"final_response": "Erro: Nenhuma mensagem recebida", "messages": state.messages}
    
    last_message = state.messages[-1]
    if isinstance(last_message, HumanMessage):
        query = last_message.content
        state.query = query
        
        # Análise simples para decidir se precisa de retrieval
        medical_keywords = ["autismo", "tea", "transtorno", "espectro", "sintomas", "tratamento", 
                           "diagnóstico", "terapia", "comportamento", "desenvolvimento"]
        
        state.needs_retrieval = any(keyword in query.lower() for keyword in medical_keywords)
        
        logger.info(f"🔍 Consulta: {query}")
        logger.info(f"📚 Precisa de retrieval: {state.needs_retrieval}")
        
        return {
            "query": query,
            "needs_retrieval": state.needs_retrieval,
            "messages": state.messages
        }
    
    return {"messages": state.messages}

def retriever_node(state: RAGState) -> Dict[str, Any]:
    """
    Agente Retriever - Busca documentos relevantes no vector store
    """
    logger.info("🔍 Retriever: Buscando documentos...")
    
    if not state.needs_retrieval:
        logger.info("⏭️ Retriever: Pulando retrieval - não necessário")
        return {"retrieved_docs": [], "messages": state.messages}
    
    try:
        # Importar aqui para evitar problemas de dependência circular
        from src.tools.vector_search import VectorSearchTool
        
        vector_tool = VectorSearchTool()
        docs = vector_tool.search(state.query, k=5)
        
        state.retrieved_docs = docs
        logger.info(f"📄 Retriever: Encontrados {len(docs)} documentos")
        
        return {"retrieved_docs": docs, "messages": state.messages}
        
    except Exception as e:
        logger.error(f"❌ Erro no retriever: {e}")
        return {"retrieved_docs": [], "messages": state.messages}

def answerer_node(state: RAGState) -> Dict[str, Any]:
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
        
        for i, doc in enumerate(state.retrieved_docs):
            context += f"\n\nDocumento {i+1}:\n{doc.get('content', '')}"
            citations.append({
                "source": doc.get('source', 'Fonte não identificada'),
                "content": doc.get('content', '')[:200] + "...",
                "relevance": doc.get('score', 0.0)
            })
        
        # Gerar resposta
        prompt = f"""
        Você é um assistente especializado em autismo (TEA - Transtorno do Espectro Autista).
        
        Pergunta do usuário: {state.query}
        
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
        state.answer = response
        state.citations = citations
        
        logger.info(f"✅ Answerer: Resposta gerada com {len(citations)} citações")
        
        return {
            "answer": response,
            "citations": citations,
            "messages": state.messages
        }
        
    except Exception as e:
        logger.error(f"❌ Erro no answerer: {e}")
        return {
            "answer": "Desculpe, ocorreu um erro ao gerar a resposta.",
            "citations": [],
            "messages": state.messages
        }

def self_check_node(state: RAGState) -> Dict[str, Any]:
    """
    Agente Self-Check - Valida se a resposta tem evidências suficientes
    """
    logger.info("🔍 Self-Check: Validando resposta...")
    
    try:
        # Verificações básicas
        has_citations = len(state.citations) > 0
        has_content = len(state.answer) > 50
        mentions_sources = "fonte" in state.answer.lower() or "documento" in state.answer.lower()
        
        # Score de confiança baseado nas verificações
        confidence = 0.0
        if has_citations:
            confidence += 0.4
        if has_content:
            confidence += 0.3
        if mentions_sources:
            confidence += 0.3
        
        state.confidence_score = confidence
        state.self_check_passed = confidence >= 0.6
        
        logger.info(f"📊 Self-Check: Confiança {confidence:.2f}, Passou: {state.self_check_passed}")
        
        return {
            "confidence_score": confidence,
            "self_check_passed": state.self_check_passed,
            "messages": state.messages
        }
        
    except Exception as e:
        logger.error(f"❌ Erro no self-check: {e}")
        return {
            "confidence_score": 0.0,
            "self_check_passed": False,
            "messages": state.messages
        }

def safety_node(state: RAGState) -> Dict[str, Any]:
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
        dangerous_words = ["diagnóstico", "trate", "medicamento", "dose", "prescreva"]
        contains_dangerous = any(word in state.answer.lower() for word in dangerous_words)
        
        if contains_dangerous:
            disclaimer += "\n\n🚨 Esta resposta contém informações que requerem supervisão profissional."
        
        state.disclaimer = disclaimer
        state.safety_check_passed = True
        
        logger.info("✅ Safety: Verificação concluída")
        
        return {
            "disclaimer": disclaimer,
            "safety_check_passed": True,
            "messages": state.messages
        }
        
    except Exception as e:
        logger.error(f"❌ Erro no safety: {e}")
        return {
            "disclaimer": "⚠️ Erro na verificação de segurança.",
            "safety_check_passed": False,
            "messages": state.messages
        }

def final_response_node(state: RAGState) -> Dict[str, Any]:
    """
    Nó final - Compila a resposta final
    """
    logger.info("📝 Finalizando resposta...")
    
    try:
        # Compilar resposta final
        final_response = f"{state.answer}\n\n"
        
        # Adicionar citações se existirem
        if state.citations:
            final_response += "📚 **Fontes consultadas:**\n"
            for i, citation in enumerate(state.citations, 1):
                final_response += f"{i}. {citation['source']} (relevância: {citation['relevance']:.2f})\n"
        
        # Adicionar disclaimer
        final_response += f"\n{state.disclaimer}"
        
        # Adicionar score de confiança
        final_response += f"\n\n📊 Confiança da resposta: {state.confidence_score:.1%}"
        
        state.final_response = final_response
        
        # Adicionar resposta ao histórico de mensagens
        ai_message = AIMessage(content=final_response)
        state.messages.append(ai_message)
        
        logger.info("✅ Resposta final compilada")
        
        return {
            "final_response": final_response,
            "messages": state.messages
        }
        
    except Exception as e:
        logger.error(f"❌ Erro na resposta final: {e}")
        error_response = "Desculpe, ocorreu um erro ao processar sua pergunta."
        return {
            "final_response": error_response,
            "messages": state.messages
        }

def should_continue(state: RAGState) -> str:
    """
    Função de decisão para o fluxo do grafo
    """
    if not state.needs_retrieval:
        return "answerer"
    else:
        return "retriever"

class RAGGraph:
    """Classe principal do grafo RAG"""
    
    def __init__(self):
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Constrói o grafo LangGraph"""
        
        # Criar grafo
        workflow = StateGraph(RAGState)
        
        # Adicionar nós
        workflow.add_node("supervisor", supervisor_node)
        workflow.add_node("retriever", retriever_node)
        workflow.add_node("answerer", answerer_node)
        workflow.add_node("self_check", self_check_node)
        workflow.add_node("safety", safety_node)
        workflow.add_node("final_response", final_response_node)
        
        # Definir fluxo
        workflow.set_entry_point("supervisor")
        
        # Fluxo condicional
        workflow.add_conditional_edges(
            "supervisor",
            should_continue,
            {
                "retriever": "retriever",
                "answerer": "answerer"
            }
        )
        
        # Fluxo sequencial
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
            state = RAGState()
            state.messages = [HumanMessage(content=query)]
            
            # Executar grafo
            result = self.graph.invoke(state)
            
            return result.final_response
            
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