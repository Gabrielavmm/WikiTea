"""
Agente Educador - Especializado em Educação e Escolarização de Autistas
Gera respostas focadas em estratégias educacionais, inclusão escolar e aprendizagem
"""

import logging
from typing import Dict, Any
import re

logger = logging.getLogger(__name__)

def education_retriever_node(state) -> Dict[str, Any]:
    """
    Agente Educador - Busca documentos específicos sobre educação
    """
    logger.info("🎓 Agente Educação: Buscando documentos educacionais...")
    
    try:
        # Foco em termos educacionais
        education_keywords = [
            "educação", "escola", "ensino", "aprendizagem", "pedagogia",
            "inclusão", "sala de aula", "currículo", "adaptação", "TEA escola",
            "professor", "educador", "escolarização", "material didático", "MEC",
            "ensino fundamental", "ensino médio", "universidade", "faculdade"
        ]
        
        # Verificar se é uma consulta educacional
        query = state.query.lower()
        is_education_query = any(keyword in query for keyword in education_keywords)
        
        if not is_education_query:
            logger.info("⏭️ Educação: Consulta não relacionada à educação")
            return {"retrieved_docs": [], "messages": state.messages}
        
        # Buscar documentos específicos de educação
        from src.tools.vector_search import VectorSearchTool
        
        vector_tool = VectorSearchTool()
        
        # Adicionar termos específicos de educação à busca
        education_query = f"{state.query} educação escolar inclusão autista TEA MEC"
        
        # Buscar mais documentos para depois filtrar
        docs = vector_tool.search(education_query, k=10)
        
        # Filtrar documentos por conteúdo/relevância educacional
        education_docs = []
        for doc in docs:
            content = doc.get('content', '').lower()
            source = doc.get('source', '').lower()
            
            # Verificar se é um documento educacional
            is_education_doc = (
                any(edu_keyword in content for edu_keyword in education_keywords) or
                'mec' in source or 'educação' in source or 'escola' in source or
                'gov.br' in source  # Fontes governamentais geralmente são confiáveis
            )
            
            if is_education_doc:
                education_docs.append(doc)
        
        # Manter apenas os top 5 documentos educacionais
        education_docs = education_docs[:5]
        
        state.retrieved_docs = education_docs
        logger.info(f"📚 Educação: Filtrados {len(education_docs)} documentos educacionais")
        
        return {"retrieved_docs": education_docs, "messages": state.messages}
        
    except Exception as e:
        logger.error(f"❌ Erro no agente educação: {e}")
        return {"retrieved_docs": [], "messages": state.messages}