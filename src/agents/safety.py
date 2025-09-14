"""
Agente Safety - Verificação de Segurança
Adiciona disclaimers e verifica segurança das respostas
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def safety_node(state) -> Dict[str, Any]:
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