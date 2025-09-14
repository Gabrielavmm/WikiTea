"""
Interface Streamlit para o Assistente RAG sobre Autismo
"""

import streamlit as st
import sys
from pathlib import Path

# Adicionar src ao path para imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    from src.graph.rag_graph import create_rag_graph
    from src.tools.vector_search import create_vector_search_tool
except ImportError as e:
    print(f"Erro de import: {e}")
    print("Tentando import direto...")
    # Fallback para imports diretos
    sys.path.append(str(Path(__file__).parent.parent / "src"))
    from graph.rag_graph import create_rag_graph
    from tools.vector_search import create_vector_search_tool
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração da página
st.set_page_config(
    page_title="Assistente RAG - Autismo",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Inicializa o estado da sessão"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "rag_graph" not in st.session_state:
        with st.spinner("Inicializando sistema..."):
            try:
                st.session_state.rag_graph = create_rag_graph()
                st.session_state.vector_tool = create_vector_search_tool()
                st.session_state.system_ready = True
            except Exception as e:
                st.error(f"Erro ao inicializar sistema: {e}")
                st.session_state.system_ready = False

def display_sidebar():
    """Exibe a barra lateral com informações"""
    with st.sidebar:
        st.title("🧠 Assistente RAG - Autismo")
        
        st.markdown("""
        ### Sobre este sistema
        
        Este é um assistente baseado em RAG (Retrieval-Augmented Generation) 
        especializado em informações sobre autismo (TEA).
        
        **Características:**
        - ✅ Citações das fontes
        - ✅ Verificação de evidências
        - ✅ Disclaimers de segurança
        - ✅ Múltiplas fontes de dados
        
        **⚠️ Importante:**
        Este sistema é apenas informativo e não substitui 
        consulta médica ou psicológica profissional.
        """)
        
        # Informações do sistema
        if st.session_state.get("system_ready", False):
            st.success("✅ Sistema inicializado")
            
            # Mostrar estatísticas do banco vetorial
            try:
                stats = st.session_state.vector_tool.get_collection_info()
                st.info(f"📊 Documentos indexados: {stats.get('document_count', 'N/A')}")
            except:
                pass
        else:
            st.error("❌ Sistema não inicializado")
        
        # Limpar histórico
        if st.button("🗑️ Limpar Histórico"):
            st.session_state.messages = []
            st.rerun()

def display_chat():
    """Exibe a interface de chat"""
    st.title("💬 Chat com o Assistente")
    
    # Exibir histórico de mensagens
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input do usuário
    if prompt := st.chat_input("Faça sua pergunta sobre autismo..."):
        # Adicionar mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Processar com o sistema RAG
        if st.session_state.get("system_ready", False):
            with st.chat_message("assistant"):
                with st.spinner("Processando sua pergunta..."):
                    try:
                        # Processar consulta
                        response = st.session_state.rag_graph.process_query(prompt)
                        
                        # Exibir resposta
                        st.markdown(response)
                        
                        # Adicionar ao histórico
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        
                    except Exception as e:
                        error_msg = f"❌ Erro ao processar pergunta: {e}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        else:
            error_msg = "❌ Sistema não está pronto. Tente recarregar a página."
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

def display_examples():
    """Exibe exemplos de perguntas"""
    st.subheader("💡 Exemplos de Perguntas")
    
    examples = [
        "O que é autismo?",
        "Quais são os sinais do TEA?",
        "Como funciona o diagnóstico?",
        "Quais são as terapias disponíveis?",
        "Quais são os direitos das pessoas com autismo?",
        "Como apoiar uma criança com autismo?",
        "O que é ABA?",
        "Como funciona a inclusão escolar?"
    ]
    
    cols = st.columns(2)
    for i, example in enumerate(examples):
        col = cols[i % 2]
        if col.button(f"❓ {example}", key=f"example_{i}"):
            st.session_state.messages.append({"role": "user", "content": example})
            st.rerun()

def display_footer():
    """Exibe rodapé com informações importantes"""
    st.markdown("---")
    
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
        <p><strong>⚠️ Disclaimer Importante:</strong></p>
        <p>Este sistema é apenas informativo e educacional. As informações fornecidas 
        não substituem consulta médica, psicológica ou de outros profissionais qualificados.</p>
        <p>Para diagnóstico, tratamento ou orientações específicas, sempre consulte 
        profissionais de saúde especializados.</p>
        <br>
        <p>Desenvolvido como projeto acadêmico - Sistema RAG + Agentes LangGraph</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Função principal da aplicação"""
    # Inicializar estado da sessão
    initialize_session_state()
    
    # Layout principal
    display_sidebar()
    
    # Conteúdo principal
    tab1, tab2 = st.tabs(["💬 Chat", "ℹ️ Sobre"])
    
    with tab1:
        display_chat()
        display_examples()
    
    with tab2:
        st.subheader("📋 Sobre o Sistema")
        
        st.markdown("""
        ### 🏗️ Arquitetura
        
        Este sistema utiliza uma arquitetura de agentes baseada em LangGraph:
        
        **🤖 Agentes:**
        - **Supervisor**: Decide o fluxo baseado na consulta
        - **Retriever**: Busca documentos relevantes no banco vetorial
        - **Answerer**: Gera resposta com base nos documentos encontrados
        - **Self-Check**: Valida se a resposta tem evidências suficientes
        - **Safety**: Adiciona disclaimers e verifica segurança
        
        **🔧 Tecnologias:**
        - **LangGraph**: Orquestração de agentes
        - **ChromaDB**: Banco vetorial para documentos
        - **HuggingFace Embeddings**: Modelos de embedding
        - **Streamlit**: Interface web
        - **Ollama/LLM**: Geração de respostas
        
        ### 📊 Métricas de Qualidade
        
        O sistema implementa várias verificações:
        - **Citações obrigatórias**: Todas as respostas devem ter fontes
        - **Score de confiança**: Avaliação da qualidade da resposta
        - **Verificação de evidências**: Garantia de que há suporte documental
        - **Disclaimers de segurança**: Alertas sobre limitações médicas
        
        ### 🎯 Fontes de Dados
        
        - Wikipedia sobre autismo
        - Informações oficiais do SUS
        - Documentos educacionais sobre TEA
        - Diretrizes e protocolos públicos
        """)
        
        # Mostrar configurações se disponível
        if st.session_state.get("system_ready", False):
            st.subheader("⚙️ Configurações do Sistema")
            
            try:
                vector_stats = st.session_state.vector_tool.get_collection_info()
                st.json(vector_stats)
            except:
                st.info("Informações do sistema não disponíveis")
    
    display_footer()

if __name__ == "__main__":
    main()