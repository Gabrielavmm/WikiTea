

import logging
from typing import Dict, Any
import re

logger = logging.getLogger(__name__)
def health_retriever_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agente Saúde - Busca documentos específicos sobre saúde
    """
    logger.info("🏥 Agente Saúde: Buscando documentos médicos...")
    
    try:
        from src.tools.vector_search import VectorSearchTool
        vector_tool = VectorSearchTool()
        
        health_query = f"{state['query']} saúde médico tratamento autista TEA"
        docs = vector_tool.search(health_query, k=10)
        
        # Filtrar documentos de saúde
        health_docs = []
        health_keywords = ["saúde", "médico", "tratamento", "terapia", "diagnóstico"]
        
        for doc in docs:
            content = doc.get('content', '').lower()
            source = doc.get('source', '').lower()
            
            is_health_doc = (
                any(keyword in content for keyword in health_keywords) or
                any(keyword in source for keyword in ['saúde', 'médico', 'hospital', 'sus'])
            )
            
            if is_health_doc:
                health_docs.append(doc)
        
        health_docs = health_docs[:5]
        logger.info(f"💊 Saúde: Encontrados {len(health_docs)} documentos médicos")
        
        return {"retrieved_docs": health_docs, "messages": state.get("messages", [])}
        
    except Exception as e:
        logger.error(f"❌ Erro no agente saúde: {e}")
        return {"retrieved_docs": [], "messages": state.get("messages", [])}