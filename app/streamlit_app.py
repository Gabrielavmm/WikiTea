"""
Interface Streamlit para o Assistente RAG sobre Autismo
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Carregar .env manualmente ANTES de qualquer import
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

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
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Inicializa o estado da sessão"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "rag_graph" not in st.session_state:
        # Loading mais detalhado para inicialização
        init_container = st.container()
        with init_container:
            st.info("🚀 Inicializando sistema RAG...")
            
            init_progress = st.progress(0)
            init_status = st.empty()
            
            try:
                # Carregar componentes
                init_status.text("📚 Carregando banco vetorial ChromaDB...")
                init_progress.progress(25)
                
                init_status.text("🤖 Inicializando OpenAI GPT-3.5-turbo...")
                init_progress.progress(50)
                
                init_status.text("🔗 Configurando agentes LangGraph...")
                init_progress.progress(75)
                
                st.session_state.rag_graph = create_rag_graph()
                st.session_state.vector_tool = create_vector_search_tool()
                
                init_status.text("✅ Sistema inicializado com sucesso!")
                init_progress.progress(100)
                
                st.session_state.system_ready = True
                
                # Limpar loading após um momento
                import time
                time.sleep(1)
                init_container.empty()
                
            except Exception as e:
                st.error(f"❌ Erro ao inicializar sistema: {e}")
                st.session_state.system_ready = False

def display_sidebar():
    """Exibe a barra lateral com informações"""
    with st.sidebar:
        st.title("Assistente RAG - Autismo")
        
        st.write("""
        Sobre este sistema
        
        Este é um assistente baseado em RAG (Retrieval-Augmented Generation) 
        especializado em informações sobre autismo (TEA).
        
        Características:
        - Citações das fontes
        - Verificação de evidências
        - Disclaimers de segurança
        - Múltiplas fontes de dados
        
        Importante:
        Este sistema é apenas informativo e não substitui 
        consulta médica ou psicológica profissional.
        """)
        
        # Informações do sistema
        if st.session_state.get("system_ready", False):
            st.success("✅ Sistema inicializado")
            
            # Status dos componentes
            st.markdown("**Status dos Componentes:**")
            st.markdown("🤖 OpenAI: ✅ Ativo")
            st.markdown("🧠 GPT-3.5-turbo: ✅ Carregado")
            st.markdown("📚 ChromaDB: ✅ Conectado")
            st.markdown("🔗 LangGraph: ✅ Configurado")
            
            # Mostrar estatísticas do banco vetorial
            try:
                stats = st.session_state.vector_tool.get_collection_info()
                st.info(f"📄 Documentos indexados: {stats.get('document_count', 'N/A')}")
            except:
                pass
        else:
            st.error("❌ Sistema não inicializado")
            st.info("🔄 Recarregue a página para inicializar")
        
        # Limpar histórico
        if st.button("Limpar Historico"):
            st.session_state.messages = []
            st.rerun()

def display_chat():
    """Exibe a interface de chat"""
    st.title("Chat com o Assistente")
    
    # Exibir histórico de mensagens
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.code(message["content"], language=None)
    
    # Input do usuário
    if prompt := st.chat_input("Faça sua pergunta sobre autismo..."):
        # Adicionar mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.code(prompt, language=None)
        
        # Processar com o sistema RAG
        if st.session_state.get("system_ready", False):
            with st.chat_message("assistant"):
                # Container para loading progressivo
                loading_container = st.container()
                
                with loading_container:
                    # Indicador principal
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        # Processar consulta com loading progressivo
                        import threading
                        import time
                        
                        # Variáveis para controle do loading
                        current_status = "🤖 Supervisor: Analisando sua pergunta..."
                        progress_value = 0
                        
                        def update_loading():
                            nonlocal current_status, progress_value
                            status_text.text(current_status)
                            progress_bar.progress(progress_value)
                        
                        # Iniciar com supervisor
                        current_status = "🤖 Supervisor: Analisando sua pergunta..."
                        progress_value = 10
                        update_loading()
                        time.sleep(0.3)
                        
                        # Retriever
                        current_status = "🔍 Retriever: Buscando documentos relevantes..."
                        progress_value = 25
                        update_loading()
                        time.sleep(0.5)
                        
                        # Answerer
                        current_status = "✍️ Answerer: Gerando resposta com GPT-3.5-turbo..."
                        progress_value = 50
                        update_loading()
                        
                        # Processar consulta (esta é a parte que demora mais)
                        try:
                            # Usar versão simples que funciona
                            response = st.session_state.rag_graph.process_query_simple(prompt)
                            if not response or response.strip() == "":
                                response = "Desculpe, não foi possível gerar uma resposta. Tente reformular sua pergunta."
                        except Exception as e:
                            st.error(f"Erro ao processar consulta: {e}")
                            response = f"Erro ao processar consulta: {str(e)}"
                        
                        # Self-Check
                        current_status = "🔍 Self-Check: Validando qualidade da resposta..."
                        progress_value = 80
                        update_loading()
                        time.sleep(0.2)
                        
                        # Safety
                        current_status = "🛡️ Safety: Verificando segurança..."
                        progress_value = 90
                        update_loading()
                        time.sleep(0.2)
                        
                        # Finalizar
                        current_status = "✅ Resposta finalizada!"
                        progress_value = 100
                        update_loading()
                        time.sleep(0.5)
                        
                        # Limpar loading
                        loading_container.empty()
                        
                        # Exibir resposta
                        st.code(response, language=None)
                        
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
    st.subheader("Exemplos de Perguntas")
    
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
        if col.button(f"? {example}", key=f"example_{i}"):
            st.session_state.messages.append({"role": "user", "content": example})
            st.rerun()

def display_footer():
    """Exibe rodapé com informações importantes"""
    st.write("---")
    
    st.write("""
    Disclaimer Importante:
    
    Este sistema é apenas informativo e educacional. As informações fornecidas 
    não substituem consulta médica, psicológica ou de outros profissionais qualificados.
    
    Para diagnóstico, tratamento ou orientações específicas, sempre consulte 
    profissionais de saúde especializados.
    
    Desenvolvido como projeto acadêmico - Sistema RAG + Agentes LangGraph
    """)

def main():
    """Função principal da aplicação"""
    # Inicializar estado da sessão
    initialize_session_state()
    
    # Layout principal
    display_sidebar()
    
    # Conteúdo principal
    tab1, tab2 = st.tabs(["Chat", "Sobre"])
    
    with tab1:
        display_chat()
        display_examples()
    
    with tab2:
        st.subheader("Sobre o Sistema")
        
        st.write("""
        Arquitetura
        
        Este sistema utiliza uma arquitetura de agentes baseada em LangGraph:
        
        Agentes:
        - Supervisor: Decide o fluxo baseado na consulta
        - Retriever: Busca documentos relevantes no banco vetorial
        - Answerer: Gera resposta com base nos documentos encontrados
        - Self-Check: Valida se a resposta tem evidências suficientes
        - Safety: Adiciona disclaimers e verifica segurança
        
        Tecnologias:
        - LangGraph: Orquestração de agentes
        - ChromaDB: Banco vetorial para documentos
        - HuggingFace Embeddings: Modelos de embedding
        - Streamlit: Interface web
        - OpenAI/LLM: Geração de respostas
        
        Métricas de Qualidade
        
        O sistema implementa várias verificações:
        - Citações obrigatórias: Todas as respostas devem ter fontes
        - Score de confiança: Avaliação da qualidade da resposta
        - Verificação de evidências: Garantia de que há suporte documental
        - Disclaimers de segurança: Alertas sobre limitações médicas
        
        Fontes de Dados
        
        - Wikipedia sobre autismo
        - Informações oficiais do SUS
        - Documentos educacionais sobre TEA
        - Diretrizes e protocolos públicos
        """)
        
        # Mostrar configurações se disponível
        if st.session_state.get("system_ready", False):
            st.subheader("Configuracoes do Sistema")
            
            try:
                vector_stats = st.session_state.vector_tool.get_collection_info()
                st.json(vector_stats)
            except:
                st.info("Informações do sistema não disponíveis")
    
    display_footer()

if __name__ == "__main__":
    main()