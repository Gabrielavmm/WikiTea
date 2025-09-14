"""
Agente Retriever - Busca Vetorial
Recupera documentos relevantes do banco vetorial
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def retriever_node(state) -> Dict[str, Any]:
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