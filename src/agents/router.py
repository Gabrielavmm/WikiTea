"""
Router - Direciona para os agentes especializados
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def router_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Router - Decide qual agente de retrieval usar baseado no domínio
    """
    domain = state.get("domain", "geral")
    needs_retrieval = state.get("needs_retrieval", False)
    
    logger.info(f"🔄 Router: Domínio {domain}, Retrieval necessário: {needs_retrieval}")
    
    # Se não precisa de retrieval, vai direto para o answerer
    if not needs_retrieval:
        logger.info("⏭️ Router: Pulando retrieval - não necessário")
        return {"retrieved_docs": [], "messages": state.get("messages", [])}
    
    # Importar os agentes especializados
    try:
        if domain == "educação":
            from src.agents.educador import education_retriever_node
            return education_retriever_node(state)
        elif domain == "saúde":
            from src.agents.saude import health_retriever_node
            return health_retriever_node(state)
        elif domain == "direito":
            from src.agents.direito import legal_retriever_node
            return legal_retriever_node(state)
        else:
            # Domínio geral - usa o retriever padrão
            from src.agents.retriever import retriever_node
            return retriever_node(state)
            
    except ImportError as e:
        logger.error(f"❌ Erro ao importar agente especializado: {e}")
        # Fallback para retriever padrão
        from src.agents.retriever import retriever_node
        return retriever_node(state)