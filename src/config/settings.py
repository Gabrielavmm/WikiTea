"""
Configurações do sistema RAG para Autismo
"""

import os
from typing import Dict, Any
from pathlib import Path

# Carregar variáveis de ambiente do arquivo .env manualmente
def load_env_manually():
    """Carrega variáveis do arquivo .env manualmente"""
    env_file = Path(__file__).parent.parent.parent / ".env"
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

# Carregar variáveis de ambiente
load_env_manually()

class Settings:
    """Configurações centralizadas do sistema"""
    
    # Configurações do Vector Store
    VECTOR_STORE = {
        "persist_directory": "./chroma_db",
        "collection_name": "autismo",
        "chunk_size": 1000,
        "chunk_overlap": 200
    }
    
    # Configurações de Embeddings
    EMBEDDINGS = {
        "model_name": "sentence-transformers/all-MiniLM-L6-v2",
        "device": "cpu",
        "normalize_embeddings": True
    }
    
    # Configurações do LLM
    LLM = {
        "model_type": "openai",  # openai, huggingface, fallback
        "model_name": "gpt-3.5-turbo",
        "temperature": 0.7,
        "max_tokens": 2048
    }
    
    # Configurações de Retrieval
    RETRIEVAL = {
        "k": 5,  # Número de documentos a recuperar
        "score_threshold": 0.0,  # Limiar mínimo de similaridade
        "rerank": False  # Se deve fazer reranking
    }
    
    # Configurações de Self-Check
    SELF_CHECK = {
        "min_confidence": 0.6,  # Confiança mínima para aceitar resposta
        "require_citations": True,  # Se citações são obrigatórias
        "min_citations": 1  # Número mínimo de citações
    }
    
    # Configurações de Safety
    SAFETY = {
        "add_disclaimer": True,
        "check_dangerous_words": True,
        "dangerous_words": [
            "diagnóstico", "trate", "medicamento", "dose", "prescreva",
            "cure", "tratamento médico", "medicação"
        ]
    }
    
    # Configurações de Logging
    LOGGING = {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    }
    
    # URLs de fontes de dados
    DATA_SOURCES = {
        "wikipedia_autismo": "https://pt.wikipedia.org/wiki/Autismo",
        "sus_teas": "https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/t/transtorno-do-espectro-autista",
        "oms_autismo": "https://www.who.int/news-room/fact-sheets/detail/autism-spectrum-disorders"
    }
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Retorna todas as configurações como dicionário"""
        return {
            "vector_store": cls.VECTOR_STORE,
            "embeddings": cls.EMBEDDINGS,
            "llm": cls.LLM,
            "retrieval": cls.RETRIEVAL,
            "self_check": cls.SELF_CHECK,
            "safety": cls.SAFETY,
            "logging": cls.LOGGING,
            "data_sources": cls.DATA_SOURCES
        }
    
    @classmethod
    def update_from_env(cls):
        """Atualiza configurações baseadas em variáveis de ambiente"""
        # LLM
        if os.getenv("LLM_MODEL_TYPE"):
            cls.LLM["model_type"] = os.getenv("LLM_MODEL_TYPE")
        if os.getenv("LLM_MODEL_NAME"):
            cls.LLM["model_name"] = os.getenv("LLM_MODEL_NAME")
        
        # Vector Store
        if os.getenv("VECTOR_STORE_DIR"):
            cls.VECTOR_STORE["persist_directory"] = os.getenv("VECTOR_STORE_DIR")
        if os.getenv("VECTOR_STORE_COLLECTION"):
            cls.VECTOR_STORE["collection_name"] = os.getenv("VECTOR_STORE_COLLECTION")
        
        # Embeddings
        if os.getenv("EMBEDDING_MODEL"):
            cls.EMBEDDINGS["model_name"] = os.getenv("EMBEDDING_MODEL")

# Instância global das configurações
settings = Settings()

# Atualizar configurações do ambiente
settings.update_from_env()