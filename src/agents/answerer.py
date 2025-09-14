"""
Agente Answerer - Gerador de Respostas
Gera respostas baseadas nos documentos recuperados com citações
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def answerer_node(state) -> Dict[str, Any]:
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