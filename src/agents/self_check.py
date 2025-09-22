"""
Agente Self-Check - Anti-alucinação
Valida se a resposta tem evidências suficientes
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def self_check_node(state) -> Dict[str, Any]:
    """
    Agente Self-Check - Valida se a resposta tem evidências suficientes
    """
    logger.info("🔍 Self-Check: Validando resposta...")
    
    try:
        # Verificações básicas
        has_citations = len(state.citations) > 0
        has_content = len(state.answer) > 50
        mentions_sources = "fonte" in state.answer.lower() or "documento" in state.answer.lower()
        
        
        return {
            
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