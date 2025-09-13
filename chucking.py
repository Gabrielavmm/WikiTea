# STEP 1
import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


# URL da página 
URL_BASE = "https://pt.wikipedia.org/wiki/Autismo"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Inicialize web_paths antes do try/except
web_paths = []

try:
    response = requests.get(URL_BASE, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Se você quiser continuar com a Wikipédia, a lógica de busca de links
    # precisa ser ajustada, pois o conteúdo não está em tags <h2> com a classe 'entry-title'.
    # Para simplificar, vamos carregar a página inteira diretamente.
    web_paths.append(URL_BASE)

    print(f"Links encontrados: {len(web_paths)}")
    for path in web_paths:
        print(path)

except requests.exceptions.RequestException as e:
    print(f"Erro ao acessar a URL: {e}")
except Exception as e:
    print(f"Ocorreu um erro: {e}")

# Se web_paths estiver vazia, não prosseguimos com o carregamento
if not web_paths:
    print("Nenhum link para carregar. Encerrando o programa.")
else:
    # STEP 2 recuperar o chucking e indexar a pagina
    print("Buscando conteúdo...")
    loader = WebBaseLoader(web_paths)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # STEP 3 Salvar no disco
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),
        persist_directory="./chroma_db",
        collection_name="autismo"
    )