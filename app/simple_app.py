"""
Interface Simples para o Assistente RAG sobre Autismo
Versão básica e funcional
"""

import streamlit as st
import sys
from pathlib import Path

# Adicionar src ao path para imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    from src.graph.rag_graph import create_rag_graph
except ImportError as e:
    st.error(f"Erro de import: {e}")
    st.stop()

# Configuração da página
st.set_page_config(
    page_title="Assistente RAG - Autismo",
    page_icon="🧠",
    layout="centered"
)

# Título
st.title("🧠 Assistente RAG sobre Autismo")
st.markdown("**Sistema de perguntas e respostas sobre Transtorno do Espectro Autista**")

# Inicializar o sistema
@st.cache_resource
def load_rag_system():
    """Carrega o sistema RAG uma vez"""
    try:
        with st.spinner("Carregando sistema..."):
            rag = create_rag_graph()
            st.success("✅ Sistema carregado!")
            return rag
    except Exception as e:
        st.error(f"❌ Erro ao carregar sistema: {e}")
        return None

# Carregar sistema
rag_system = load_rag_system()

if rag_system is None:
    st.stop()

# Interface principal
st.markdown("---")

# Input do usuário
user_question = st.text_input(
    "🤔 Faça sua pergunta sobre autismo:",
    placeholder="Ex: O que é autismo? Quais são os sintomas?",
    key="user_input"
)

# Botão de envio
if st.button("🔍 Buscar Resposta", type="primary"):
    if user_question.strip():
        with st.spinner("Processando sua pergunta..."):
            try:
                # Processar pergunta
                response = rag_system.process_query(user_question)
                
                # Mostrar resposta
                st.markdown("### 📝 Resposta:")
                st.markdown(response)
                
            except Exception as e:
                st.error(f"❌ Erro ao processar pergunta: {e}")
    else:
        st.warning("⚠️ Por favor, digite uma pergunta.")

# Exemplos de perguntas
st.markdown("---")
st.markdown("### 💡 Exemplos de perguntas:")
examples = [
    "O que é autismo?",
    "Quais são os sintomas do TEA?",
    "Como funciona o diagnóstico?",
    "Quais são as terapias disponíveis?",
    "Como ajudar uma criança com autismo?"
]

for example in examples:
    if st.button(f"❓ {example}", key=f"example_{example}"):
        st.session_state.user_input = example
        st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
        ⚠️ <strong>Importante:</strong> Este sistema é apenas informativo e não substitui consulta médica profissional.
    </div>
    """, 
    unsafe_allow_html=True
)