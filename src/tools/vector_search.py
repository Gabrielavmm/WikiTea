"""
Ferramenta de busca vetorial para recuperação de documentos
"""

import os
from typing import List, Dict, Any
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import logging

logger = logging.getLogger(__name__)

class VectorSearchTool:
    """Ferramenta para busca no banco vetorial ChromaDB"""
    
    def __init__(self, persist_directory: str = "./chroma_db", collection_name: str = "autismo"):
        """
        Inicializa a ferramenta de busca vetorial
        
        Args:
            persist_directory: Diretório onde está o ChromaDB
            collection_name: Nome da coleção no ChromaDB
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.vectorstore = None
        self.embeddings = None
        self._initialize_vectorstore()
    
    def _initialize_vectorstore(self):
        """Inicializa o vectorstore e embeddings"""
        try:
            # Verificar se o diretório existe
            if not os.path.exists(self.persist_directory):
                raise FileNotFoundError(f"Diretório {self.persist_directory} não encontrado")
            
            # Inicializar embeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            
            # Carregar vectorstore existente
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
                collection_name=self.collection_name
            )
            
            logger.info(f"✅ VectorStore carregado de {self.persist_directory}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar VectorStore: {e}")
            raise
    
    def search(self, query: str, k: int = 5, score_threshold: float = 0.0) -> List[Dict[str, Any]]:
        """
        Busca documentos similares à consulta
        
        Args:
            query: Consulta do usuário
            k: Número de documentos a retornar
            score_threshold: Limiar mínimo de similaridade
            
        Returns:
            Lista de documentos com metadados
        """
        try:
            if not self.vectorstore:
                raise RuntimeError("VectorStore não foi inicializado")
            
            # Buscar documentos similares
            docs_with_scores = self.vectorstore.similarity_search_with_score(
                query, k=k
            )
            
            # Processar resultados
            results = []
            for doc, score in docs_with_scores:
                # Converter score de distância para similaridade (0-1)
                similarity = 1 / (1 + score)
                
                if similarity >= score_threshold:
                    result = {
                        "content": doc.page_content,
                        "metadata": doc.metadata,
                        "score": similarity,
                        "source": doc.metadata.get("source", "Fonte não identificada")
                    }
                    results.append(result)
            
            logger.info(f"🔍 Busca realizada: {len(results)} documentos encontrados para '{query}'")
            return results
            
        except Exception as e:
            logger.error(f"❌ Erro na busca: {e}")
            return []
    
    def search_with_filters(self, query: str, filters: Dict[str, Any], k: int = 5) -> List[Dict[str, Any]]:
        """
        Busca com filtros específicos nos metadados
        
        Args:
            query: Consulta do usuário
            filters: Filtros para aplicar nos metadados
            k: Número de documentos a retornar
            
        Returns:
            Lista de documentos filtrados
        """
        try:
            if not self.vectorstore:
                raise RuntimeError("VectorStore não foi inicializado")
            
            # Buscar com filtros
            docs = self.vectorstore.similarity_search(
                query, k=k, filter=filters
            )
            
            # Processar resultados
            results = []
            for doc in docs:
                result = {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "source": doc.metadata.get("source", "Fonte não identificada")
                }
                results.append(result)
            
            logger.info(f"🔍 Busca filtrada: {len(results)} documentos encontrados")
            return results
            
        except Exception as e:
            logger.error(f"❌ Erro na busca filtrada: {e}")
            return []
    
    def get_collection_info(self) -> Dict[str, Any]:
        """
        Retorna informações sobre a coleção
        
        Returns:
            Dicionário com informações da coleção
        """
        try:
            if not self.vectorstore:
                return {"error": "VectorStore não inicializado"}
            
            # Contar documentos
            count = self.vectorstore._collection.count()
            
            return {
                "collection_name": self.collection_name,
                "document_count": count,
                "persist_directory": self.persist_directory,
                "embedding_model": "sentence-transformers/all-MiniLM-L6-v2"
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao obter info da coleção: {e}")
            return {"error": str(e)}

# Função de conveniência
def create_vector_search_tool() -> VectorSearchTool:
    """Cria e retorna uma instância da ferramenta de busca vetorial"""
    return VectorSearchTool()

if __name__ == "__main__":
    # Teste básico
    tool = create_vector_search_tool()
    info = tool.get_collection_info()
    print(f"Informações da coleção: {info}")
    
    # Teste de busca
    results = tool.search("O que é autismo?", k=3)
    for i, result in enumerate(results, 1):
        print(f"\nDocumento {i}:")
        print(f"Fonte: {result['source']}")
        print(f"Similaridade: {result['score']:.3f}")
        print(f"Conteúdo: {result['content'][:200]}...")