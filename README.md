# WikiTEA
Link para slide: https://www.canva.com/design/DAGzvPQ5PXY/yzQOlrwilyliMHws7NVCKQ/view?utm_content=DAGzvPQ5PXY&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h087e5e6c0c

Para executar o projeto localmente, siga os passos abaixo:

Primeiramente, certifique-se de ter o Python 3.8 ou superior instalado. Clone o repositório e, dentro da pasta do projeto, crie um ambiente virtual com o comando python3 -m venv .venv. Em seguida, ative o ambiente virtual utilizando source .venv/bin/activate em sistemas Unix (Linux/macOS). No Windows, o comando equivalente é .\.venv\Scripts\activate.

Com o ambiente virtual ativado, instale as dependências do projeto executando pip install -r requirements.txt.

Após instalar as dependências, realize a ingestão dos documentos no banco de dados executando o script python3 ingest/autism_docs.py.

Por fim, para iniciar a aplicação e visualizar os dados por meio da interface do Streamlit, execute o comando streamlit run streamlit_app.py.
