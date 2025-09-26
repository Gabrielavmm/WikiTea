# WikiTEA
Este projeto consiste em um chatbot inteligente voltado para o autismo, com o objetivo de fornecer informações acessíveis, confiáveis e atualizadas para pessoas diagnosticadas e para qualquer pessoa interessada no tema.
O sistema responde perguntas com base em documentos científicos e institucionais relacionados às áreas de saúde, educação e leis.

A aplicação foi desenvolvida utilizando a técnica de RAG (Retrieval-Augmented Generation), que combina recuperação de informações com geração de linguagem natural, permitindo que o chatbot consulte documentos relevantes antes de formular uma resposta.

-Tecnologias utilizadas:

LangChain: para orquestrar os fluxos de RAG e integrar módulos de busca, parsing de documentos e geração de respostas.

LangGraph: para modelar e controlar o fluxo de decisão do chatbot em múltiplos nós, possibilitando lógica condicional e comportamentos dinâmicos.

OpenAI GPT-4 (ou GPT-3.5): como modelo de linguagem base para gerar respostas em linguagem natural, com alto nível de precisão e contextualização.

Streamlit: para a interface simples e interativa com o usuário final.

Essa arquitetura permite que o chatbot ofereça respostas mais precisas e contextualizadas, reduzindo o risco de alucinações e aumentando a confiabilidade, especialmente em um tema sensível como o autismo.

Link para slide: https://www.canva.com/design/DAGzvPQ5PXY/yzQOlrwilyliMHws7NVCKQ/view?utm_content=DAGzvPQ5PXY&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h087e5e6c0c

Para executar o projeto localmente, siga os passos abaixo:

Primeiramente, certifique-se de ter o Python 3.8 ou superior instalado. Clone o repositório e, dentro da pasta do projeto, crie um ambiente virtual com o comando python3 -m venv .venv. Em seguida, ative o ambiente virtual utilizando source .venv/bin/activate em sistemas Unix (Linux/macOS). No Windows, o comando equivalente é .\.venv\Scripts\activate.

Com o ambiente virtual ativado, instale as dependências do projeto executando pip install -r requirements.txt.

Após instalar as dependências, realize a ingestão dos documentos no banco de dados executando o script python3 ingest/autism_docs.py.

Por fim, para iniciar a aplicação e visualizar os dados por meio da interface do Streamlit, execute o comando streamlit run streamlit_app.py.

#Arquitetura#
Usuário → Pergunta via Streamlit

 ↓

Supervisor → Análise de intenção e classificação de domínio

 Identifica palavras-chave (educação/saúde/direito)

 Determina necessidade de retrieval

 Roteia para agente apropriado

 ↓

Retriever → Busca especializada

 🎓 Educação: MEC + inclusão + pedagogia

 🏥 Saúde: SUS + terapias + direcionamentos

 ⚖️ Direito: Leis + benefícios + direitos

 🌐 Geral: Busca ampla em todos os documentos

 ↓

Answerer → Geração de resposta

 Contexto dos documentos recuperados

 Prompt especializado por domínio

 Geração com GPT-40-mini
