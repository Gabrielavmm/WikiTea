"""
Agente Supervisor - Router de Intents
Decide o fluxo baseado na consulta do usuário
"""

import logging
from typing import Dict, Any
from langchain_core.messages import HumanMessage

logger = logging.getLogger(__name__)

def supervisor_node(state) -> Dict[str, Any]:
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