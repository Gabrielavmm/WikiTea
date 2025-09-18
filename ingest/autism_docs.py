"""
Sistema de ingestão de documentos sobre autismo
Carrega múltiplas fontes e cria banco vetorial
"""

import os
os.environ["OPENAI_API_KEY"] ="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"
import sys
import requests
import time
from typing import List, Dict, Any
from pathlib import Path

# Adicionar src ao path para imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AutismDocsIngester:
    """Classe para ingestão de documentos sobre autismo"""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        self.collection_name = "autismo"
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Fontes de dados sobre autismo
        self.data_sources = {
           "opas_oms_tea": {
                "url": "https://www.paho.org/pt/topicos/transtorno-espectro-autista",
                "description": "Transtorno do Espectro Autista"
            },
            "saude_gov_tea": {
                "url": "https://www.gov.br/saude/pt-br/assuntos/noticias/2022/abril/tea-saiba-o-que-e-o-transtorno-do-espectro-autista-e-como-o-sus-tem-dado-assistencia-a-pacientes-e-familiares",
                "description": "Ministério da Saúde - TEA e assistência do SUS"
            },
            "linhas_cuidado_tea": {
                "url": "https://linhasdecuidado.saude.gov.br/portal/transtorno-do-espectro-autista/",
                "description": "Ministério da Saúde - Linhas de cuidado para TEA"
            },
            "mec_inclusao_autistas": {
                "url": "https://www.gov.br/mec/pt-br/assuntos/noticias/2025/abril/acoes-do-mec-buscam-a-inclusao-dos-estudantes-autistas",
                "description": "Ações do MEC para inclusão de estudantes autistas"
            },
            "gov_lei_berenice_piana": {
                "url": "https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2012/lei/l12764.htm",
                "description": "Lei Berenice Piana - Política Nacional de TEA"
            },
            "fiocruz_autismo": {
                "url": "https://www.iff.fiocruz.br/index.php/8-noticias/673-autism",
                "description": "Fiocruz - Informações sobre autismo"
            }
        }
    
    def load_web_documents(self, urls: List[str]) -> List[Document]:
        """
        Carrega documentos de URLs web
        """
        logger.info(f"🌐 Carregando {len(urls)} URLs...")
        
        docs = []
        successful_urls = 0
        
        for url in urls:
            try:
                logger.info(f"📥 Tentando carregar: {url}")
                
                # Headers robustos para evitar bloqueio
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
                }
                
                loader = WebBaseLoader(
                    url, 
                    header_template=headers,
                    requests_kwargs={
                        'timeout': 15,
                        'verify': False,
                        'headers': headers
                    }
                )
                
                doc = loader.load()[0]
                
                doc.metadata.update({
                    "source_type": "web",
                    "topic": "autismo",
                    "language": "pt",
                    "url": url
                })
                
                docs.append(doc)
                successful_urls += 1
                logger.info(f"✅ Sucesso: {url}")
                
                # Pequeno delay entre requests
                time.sleep(1)
                
            except Exception as e:
                logger.warning(f"⚠️  Falha ao carregar {url}: {e}")
                continue
        
        logger.info(f"✅ {successful_urls}/{len(urls)} URLs carregadas com sucesso")
        return docs

    def load_sample_texts(self) -> List[Document]:
        """
        Carrega textos de exemplo sobre autismo (fallback)
        
        Returns:
            Lista de documentos de exemplo
        """
        logger.info("📝 Carregando textos de exemplo...")
        
        sample_texts = [
            {
                "content": """
                O Transtorno do Espectro Autista (TEA) é uma condição do desenvolvimento neurológico 
                que afeta a comunicação, interação social e comportamento. É caracterizado por padrões 
                restritos e repetitivos de comportamento, interesses ou atividades.
                
                O TEA pode ser diagnosticado em qualquer idade, mais os sintomas geralmente aparecem 
                nos primeiros dois anos de vida. Cada pessoa com TEA é única e pode apresentar 
                diferentes características e níveis de suporte necessários.
                
                As principais áreas afetadas incluem:
                - Comunicação social e interação social
                - Padrões restritos e repetitivos de comportamento
                - Interesses ou atividades
                - Resposta sensorial
                """,
                "source": "Informações Básicas sobre TEA",
                "topic": "definição"
            },
            {
                "content": """
                Sinais e sintomas do autismo podem incluir:
                
                Comunicação e Interação Social:
                - Dificuldade em iniciar ou manter conversas
                - Dificuldade em entender gestos e expressões faciais
                - Interesse limitado em compartilhar experiências
                - Dificuldade em fazer amigos
                
                Comportamentos Repetitivos e Restritos:
                - Movimentos repetitivos (balançar, bater palmas)
                - Rotinas rígidas e resistência a mudanças
                - Interesses intensos e restritos
                - Resposta incomum a estímulos sensoriais
                
                É importante notar que nem todas as pessoas com autismo apresentam todos esses 
                sinais, e a intensidade pode variar significativamente.
                """,
                "source": "Sinais e Sintomas do Autismo",
                "topic": "sintomas"
            },
            {
                "content": """
                Intervenções e apoios para pessoas com autismo:
                
                Terapias Comportamentales:
                - Análise do Comportamento Aplicada (ABA)
                - Treinamento de Habilidades Sociais
                - Terapia Cognitivo-Comportamental
                
                Terapias de Comunicação:
                - Fonoaudiologia
                - Sistemas de Comunicação Alternativa
                - Treinamento de Linguagem
                
                Apoios Educacionais:
                - Educação Especializada
                - Adaptações Curriculares
                - Suporte Individualizado
                
                Apoios Familiares:
                - Orientação e Treinamento para Famílias
                - Grupos de Apoio
                - Acesso a Recursos Comunitários
                
                O tratamento deve ser individualizado e multidisciplinar, envolvendo 
                profissionais de diferentes áreas e a família.
                """,
                "source": "Intervenções e Apoios para Autismo",
                "topic": "tratamento"
            },
            {
                "content": """
                Direitos das pessoas com autismo no Brasil:
                
                Legislação:
                - Lei 12.764/2012 (Lei Berenice Piana) - Política Nacional de Proteção dos Direitos da Pessoa com Transtorno do Espectro Autista
                - Lei 13.146/2015 (Lei Brasileira de Inclusão)
                
                Direitos Garantidos:
                - Acesso à educação em escolas regulares
                - Acesso à saúde e tratamentos
                - Acesso ao trabalho
                - Acesso à cultura, esporte, turismo e lazer
                - Acesso à moradia
                
                Benefícios:
                - BPC (Benefício de Prestação Continuada)
                - Passe livre no transporte público
                - Isenção de impostos para veículos adaptados
                
                É importante conhecer e exigir esses direitos para garantir uma vida digna 
                e inclusiva para pessoas com autismo.
                """,
                "source": "Direitos das Pessoas com Autismo",
                "topic": "direitos"
            }
        ]
        
        docs = []
        for text_data in sample_texts:
            doc = Document(
                page_content=text_data["content"].strip(),
                metadata={
                    "source": text_data["source"],
                    "source_type": "sample",
                    "topic": text_data["topic"],
                    "language": "pt"
                }
            )
            docs.append(doc)
        
        logger.info(f"✅ {len(docs)} documentos de exemplo carregados")
        return docs
    
    def create_chunks(self, documents: List[Document]) -> List[Document]:
        """
        Cria chunks dos documentos
        
        Args:
            documents: Lista de documentos originais
            
        Returns:
            Lista de chunks criados
        """
        logger.info("✂️ Criando chunks dos documentos...")
        
        try:
            chunks = self.text_splitter.split_documents(documents)
            
            # Adicionar metadados de chunk
            for i, chunk in enumerate(chunks):
                chunk.metadata.update({
                    "chunk_id": i,
                    "chunk_size": len(chunk.page_content)
                })
            
            logger.info(f"✅ {len(chunks)} chunks criados")
            return chunks
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar chunks: {e}")
            return []
    
    def create_vectorstore(self, chunks: List[Document]) -> Chroma:
        """
        Cria o banco vetorial
        
        Args:
            chunks: Lista de chunks para indexar
            
        Returns:
            Instância do ChromaDB
        """
        logger.info("🗄️ Criando banco vetorial...")
        
        try:
            # Inicializar embeddings
            embeddings = OpenAIEmbeddings(
             model="text-embedding-ada-002"
            )
            
            # Criar ou carregar vectorstore
            if os.path.exists(self.persist_directory):
                logger.info("📂 Carregando vectorstore existente...")
                vectorstore = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=embeddings,
                    collection_name=self.collection_name
                )
                
                # Adicionar novos chunks
                vectorstore.add_documents(chunks)
            else:
                logger.info("🆕 Criando novo vectorstore...")
                vectorstore = Chroma.from_documents(
                    documents=chunks,
                    embedding=embeddings,
                    persist_directory=self.persist_directory,
                    collection_name=self.collection_name
                )
            
            logger.info("✅ Banco vetorial criado/atualizado com sucesso")
            return vectorstore
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar vectorstore: {e}")
            raise
    
    
    def ingest_all(self) -> bool:
        """
        Executa o processo completo de ingestão
        """
        logger.info("🚀 Iniciando processo de ingestão...")
        
        try:
            # 1. Carregar documentos web
            urls = [source["url"] for source in self.data_sources.values()]
            web_docs = self.load_web_documents(urls)
            
            # 2. Se falhar no web, usar fallback para textos de exemplo
            if not web_docs:
                logger.warning("⚠️  Nenhum documento web carregado, usando textos de exemplo...")
                web_docs = self.load_sample_texts()
            
            # 3. Usar documentos disponíveis
            all_docs = web_docs
            
            if not all_docs:
                logger.error("❌ Nenhum documento disponível para ingestão")
                return False
            
            # 4. Criar chunks
            chunks = self.create_chunks(all_docs)
            
            if not chunks:
                logger.error("❌ Falha ao criar chunks")
                return False
            
            # 5. Criar vectorstore
            vectorstore = self.create_vectorstore(chunks)
            
            # 6. Verificar resultado
            count = vectorstore._collection.count()
            logger.info(f"✅ Ingestão concluída! Total de {count} documentos no banco vetorial")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro durante ingestão: {e}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas do banco vetorial
        
        Returns:
            Dicionário com estatísticas
        """
        try:
            if not os.path.exists(self.persist_directory):
                return {"error": "Banco vetorial não existe"}
            
            vectorstore = Chroma(
                persist_directory=self.persist_directory,
                collection_name=self.collection_name
            )
            
            count = vectorstore._collection.count()
            
            return {
                "total_documents": count,
                "persist_directory": self.persist_directory,
                "collection_name": self.collection_name,
                "embedding_model": "text-embedding-ada-002"  
            }
            
        except Exception as e:
            return {"error": str(e)}

def main():
    """Função principal para executar a ingestão"""
    logger.info("🎯 Iniciando ingestão de documentos sobre autismo")
    
    # Criar instância do ingester
    ingester = AutismDocsIngester()
    
    # Executar ingestão
    success = ingester.ingest_all()
    
    if success:
        # Mostrar estatísticas
        stats = ingester.get_stats()
        logger.info(f"📊 Estatísticas: {stats}")
        print("\n✅ Ingestão concluída com sucesso!")
        print(f"📊 Total de documentos: {stats.get('total_documents', 'N/A')}")
    else:
        print("\n❌ Falha na ingestão")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())