import logging
from typing import Dict, Any
import re

logger = logging.getLogger(__name__)

def legal_retriever_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agente Direito - Busca documentos específicos sobre legislação
    """
    logger.info("⚖️ Agente Direito: Buscando documentos jurídicos...")
    
    try:
        from src.tools.vector_search import VectorSearchTool
        vector_tool = VectorSearchTool()
        
        legal_query = f"{state['query']} direito lei legislação autista TEA"
        docs = vector_tool.search(legal_query, k=10)
        
        # Filtrar documentos jurídicos
        legal_docs = []
        legal_keywords = ["direito", "lei", "legal", "jurídico", "legislação"]
        
        for doc in docs:
            content = doc.get('content', '').lower()
            source = doc.get('source', '').lower()
            
            is_legal_doc = (
                any(keyword in content for keyword in legal_keywords) or
                any(keyword in source for keyword in ['jus', 'tribunal', 'lei', 'direito'])
            )
            
            if is_legal_doc:
                legal_docs.append(doc)
        
        legal_docs = legal_docs[:5]
        logger.info(f"📜 Direito: Encontrados {len(legal_docs)} documentos jurídicos")
        
        return {"retrieved_docs": legal_docs, "messages": state.get("messages", [])}
        
    except Exception as e:
        logger.error(f"❌ Erro no agente direito: {e}")
        return {"retrieved_docs": [], "messages": state.get("messages", [])}