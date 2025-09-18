"""
Agente Supervisor - Router de Intents
Decide o fluxo baseado na consulta do usuário
"""

import logging
from typing import Dict, Any
from langchain_core.messages import HumanMessage

logger = logging.getLogger(__name__)

def supervisor_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agente Supervisor - Decide o fluxo baseado na consulta e identifica o domínio
    """
    logger.info("🤖 Supervisor: Analisando consulta...")
    
    if not state.get("messages", []):
        return {"final_response": "Erro: Nenhuma mensagem recebida", "messages": state.get("messages", [])}
    
    last_message = state["messages"][-1]
    if isinstance(last_message, HumanMessage):
        query = last_message.content.lower()
        state["query"] = query
        
        # Identificar domínio da consulta
        education_keywords = [
            "educação", "escola", "ensino", "aprendizagem", "pedagogia",
            "inclusão", "sala de aula", "currículo", "adaptação", "TEA escola",
            "professor", "educador", "escolarização", "material didático", "MEC",
            "ensino fundamental", "ensino médio", "universidade", "faculdade"
        ]
        
        health_keywords = [
            "saúde", "médico", "tratamento", "terapia", "diagnóstico",
            "sintomas", "intervenção", "medicamento", "psiquiatra", 
            "neurologista", "psicólogo", "fonoaudiólogo", "terapeuta"
        ]
        
        legal_keywords = [
            "direito", "legal", "lei", "jurídico", "legislação",
            "inclusão", "acessibilidade", "deficiência", "educação especial",
            "saúde pública", "SUS", "benefício", "aposentadoria", "LOAS"
        ]
        
        # Determinar domínio
        domain = "geral"
        if any(keyword in query for keyword in education_keywords):
            domain = "educação"
        elif any(keyword in query for keyword in health_keywords):
            domain = "saúde"
        elif any(keyword in query for keyword in legal_keywords):
            domain = "direito"
        
        # Decidir se precisa de retrieval
        needs_retrieval = any(keyword in query for keyword in 
                            education_keywords + health_keywords + legal_keywords + 
                            ["autismo", "tea", "transtorno", "espectro"])
        
        logger.info(f"🔍 Consulta: {query}")
        logger.info(f"🎯 Domínio identificado: {domain}")
        logger.info(f"📚 Precisa de retrieval: {needs_retrieval}")
        
        return {
            "query": query,
            "domain": domain,
            "needs_retrieval": needs_retrieval,
            "messages": state["messages"]
        }
    
    return {"messages": state.get("messages", [])}