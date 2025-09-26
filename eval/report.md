# Relatório Final de Avaliação RAGAS - Sistema RAG Autismo

**Data da Avaliação:** 2025-09-26 00:20:19
**Total de Perguntas:** 5

## 📊 Métricas RAGAS (Finais)

### Faithfulness
- **Score:** 0.352
- **Interpretação:** 35.2% de fidelidade às fontes recuperadas
- **Status:** ❌ Precisa melhorar

### Answer Relevancy  
- **Score:** 0.579
- **Interpretação:** 57.9% de relevância para as perguntas
- **Status:** ❌ Precisa melhorar

### Context Precision
- **Score:** 0.422
- **Interpretação:** 42.2% de precisão dos contextos recuperados
- **Status:** ❌ Precisa melhorar

### Context Recall
- **Score:** 0.582
- **Interpretação:** 58.2% de recall dos contextos relevantes
- **Status:** ❌ Precisa melhorar

## 🎯 Análise de Contextos Recuperados

### Estatísticas
- **Total de perguntas:** 5
- **Respostas bem-sucedidas:** 5
- **Com contextos recuperados:** 5
- **Média de contextos por pergunta:** 3.0

## 📋 Recomendações

### Para Melhorar Faithfulness
1. **Aumentar número de documentos recuperados** (atualmente k=3)
2. **Melhorar qualidade dos embeddings** 
3. **Implementar reranking** dos documentos
4. **Refinar prompts** para maior fidelidade às fontes

### Para Melhorar Answer Relevancy
1. **Otimizar retrieval** para documentos mais relevantes
2. **Implementar filtros** por domínio
3. **Melhorar chunking** dos documentos
4. **Adicionar mais fontes** de qualidade

### Para Melhorar Context Precision
1. **Implementar reranking** dos documentos recuperados
2. **Ajustar threshold** de relevância
3. **Melhorar embeddings** para maior precisão
4. **Filtrar contextos** de baixa qualidade

### Para Melhorar Context Recall
1. **Aumentar k** de documentos recuperados
2. **Expandir base de conhecimento** com mais fontes
3. **Melhorar estratégia de chunking**
4. **Implementar busca híbrida** (semântica + lexical)

## 📊 Métricas Detalhadas

```json
{
  "timestamp": "2025-09-26T00:20:19.348425",
  "ragas_results": {
    "faithfulness": 0.3515151515151515,
    "answer_relevancy": 0.5788321057091834,
    "context_precision": 0.422,
    "context_recall": 0.582
  },
  "total_questions": 5,
  "successful_responses": 5,
  "responses_with_contexts": 5,
  "average_contexts_per_question": 3.0,
  "sample_responses": [
    {
      "question": "O que é o Transtorno do Espectro Autista (TEA)?",
      "answer": "O Transtorno do Espectro Autista (TEA) é um distúrbio caracterizado pela alteração das funções do neurodesenvolvimento, afetando a capacidade de comunicação, linguagem, interação social e comportamento. O TEA pode ser diagnosticado precocemente, o que permite o desenvolvimento de estímulos para a independência e qualidade de vida das crianças com autismo.\n\nSegundo o Ministério da Saúde, no Brasil foram realizados 9,6 milhões de atendimentos em ambulatórios para pessoas com autismo em 2021, sendo 4,1 milhões para o público infantil com até 9 anos de idade. O Sistema Único de Saúde (SUS) conta com uma rede de apoio e assistência para pacientes com TEA, visando proporcionar o melhor suporte possível.\n\nAlém disso, a Política Nacional de Proteção dos Direitos da Pessoa com Transtorno do Espectro Autista considera a pessoa com TEA como pessoa com deficiência para todos os efeitos legais. Isso significa que os estudantes autistas são considerados público-alvo da educação especial inclusiva, de acordo com a Política Nacional de Educação Especial na Perspectiva da Educação Inclusiva.\n\nÉ importante destacar que o TEA é uma condição complexa e variável, sendo fundamental o acompanhamento de profissionais de saúde especializados. A Linha de Cuidado desenvolvida pelo Ministério da Saúde, com o apoio de especialistas nacionais e internacionais, é uma ferramenta importante para orientar os profissionais de saúde no atendimento de crianças com TEA.\n\nFontes:\n- Ministério da Saúde\n- Política Nacional de Proteção dos Direitos da Pessoa com Transtorno do Espectro Autista\n- Linha de Cuidado - Transtorno do Espectro Autista (TEA) na criança\n\n📚 **Fontes consultadas:**\n1. https://linhasdecuidado.saude.gov.br/portal/transtorno-do-espectro-autista/ (relevância: 0.71)\n2. https://www.gov.br/saude/pt-br/assuntos/noticias/2022/abril/tea-saiba-o-que-e-o-transtorno-do-espectro-autista-e-como-o-sus-tem-dado-assistencia-a-pacientes-e-familiares (relevância: 0.64)\n3. https://www.gov.br/saude/pt-br/assuntos/noticias/2022/abril/tea-saiba-o-que-e-o-transtorno-do-espectro-autista-e-como-o-sus-tem-dado-assistencia-a-pacientes-e-familiares (relevância: 0.62)\n4. https://www.gov.br/mec/pt-br/assuntos/noticias/2025/abril/acoes-do-mec-buscam-a-inclusao-dos-estudantes-autistas (relevância: 0.61)\n5. https://linhasdecuidado.saude.gov.br/portal/transtorno-do-espectro-autista/ (relevância: 0.60)\n\n\n        ⚠️ IMPORTANTE: Esta é uma resposta informativa baseada em documentos públicos. \n        Não substitui consulta médica, psicológica ou de outros profissionais qualificados. \n        Sempre consulte profissionais de saúde para diagnóstico e tratamento.\n        ",
      "ground_truth": "O Transtorno do Espectro Autista (TEA) é uma condição do desenvolvimento neurológico caracterizada por dificuldades persistentes na comunicação social e interação social, bem como padrões restritos e repetitivos de comportamento, interesses ou atividades.",
      "context": [
        "Organização Pan-Americana da Saúde (OPAS/OMS) - Guia para Famílias sobre TEA"
      ],
      "retrieved_contexts": [
        "Linhas de Cuidado - Transtorno do Espectro Autista (TEA) na criança\n\n\n\n\n Linhas de Cuidado \n\n\n\n\n\nPortalTranstorno do Espectro Autista (TEA) na criança",
        "TEA: saiba o que é o Transtorno do Espectro Autista e como o SUS tem dado assistência a pacientes e familiares — Ministério da Saúde\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nIr para o\n      Conteúdo\n      1\n\n\nIr para a\n      Página Inicial\n      2\n\n\nIr para o menu de\n      Navegação\n      3\n\n\nIr para a\n      Busca\n      4\n\n\nIr para o\n      Mapa do site\n      5\n\n\n\n\nAtenção!\nSeu navegador não pode executar javascript. Alguns recursos podem não funcionar corretamente.\n\n\n\n\n\n\n\n\n\n\n\nAbrir menu principal de navegação\n\n\n\n\n\n\nMinistério da Saúde\n\n\n\n\n\n                        Termos mais buscados\n                    \n\n\n\n\n                                   imposto de renda\n                                \n\n\n\n\n                                   inss\n                                \n\n\n\n\n                                   assinatura\n                                \n\n\n\n\n                                   cnh social",
        "Neste 2 de abril, para celebrar o Dia Mundial de Conscientização sobre o Autismo, o Ministério da Saúde chama a atenção para um assunto importante: o Transtorno do Espectro Autista (TEA). Dados do Sistema de Informações Ambulatoriais (SIA) mostram que o Brasil realizou, em 2021, 9,6 milhões de atendimentos em ambulatórios, a pessoas com autismo, sendo 4,1 milhões ao público infantil com até 9 anos de idade.\nO TEA é um distúrbio caracterizado pela alteração das funções do neurodesenvolvimento do indivíduo, interferindo na capacidade de comunicação, linguagem, interação social e comportamento. Mesmo assim, o diagnóstico precoce permite o desenvolvimento de estímulos para independência e qualidade de vida das crianças. Para isso, o Sistema Único de Saúde (SUS) conta com uma rede de apoio e assistência a pacientes com essa condição."
      ]
    },
    {
      "question": "Quais são os sinais precoces de autismo em bebês?",
      "answer": "Os sinais precoces de autismo em bebês podem variar, mas alguns dos sinais comuns incluem dificuldade em fazer contato visual, falta de sorrisos sociais, atraso no desenvolvimento da linguagem, dificuldade em responder ao seu nome, movimentos repetitivos e dificuldade em interagir socialmente com outras pessoas.\n\nSegundo o Ministério da Saúde, o diagnóstico precoce é fundamental para o desenvolvimento de estímulos que podem ajudar na independência e qualidade de vida das crianças com autismo. Por isso, é importante estar atento a esses sinais e, se houver alguma preocupação, buscar orientação de profissionais de saúde.\n\nAlém disso, o Ministério da Saúde oferece capacitações e cursos sobre autismo, tanto para profissionais de saúde quanto para familiares, cuidadores e educadores, visando oferecer mais conhecimento e informação sobre o TEA.\n\nSe você suspeitar que seu bebê possa estar apresentando sinais de autismo, é importante procurar um profissional de saúde para uma avaliação adequada e um possível encaminhamento para um diagnóstico mais detalhado e intervenções específicas, se necessário. A rede de apoio do Sistema Único de Saúde (SUS) também pode oferecer suporte e assistência a pacientes com autismo.\n\nFonte:\n- Ministério da Saúde.\n\n📚 **Fontes consultadas:**\n1. https://www.gov.br/saude/pt-br/assuntos/noticias/2022/abril/tea-saiba-o-que-e-o-transtorno-do-espectro-autista-e-como-o-sus-tem-dado-assistencia-a-pacientes-e-familiares (relevância: 0.59)\n2. https://linhasdecuidado.saude.gov.br/portal/transtorno-do-espectro-autista/ (relevância: 0.57)\n3. https://www.gov.br/mec/pt-br/assuntos/noticias/2025/abril/acoes-do-mec-buscam-a-inclusao-dos-estudantes-autistas (relevância: 0.57)\n4. https://www.gov.br/mec/pt-br/assuntos/noticias/2025/abril/acoes-do-mec-buscam-a-inclusao-dos-estudantes-autistas (relevância: 0.57)\n5. https://www.gov.br/saude/pt-br/assuntos/noticias/2022/abril/tea-saiba-o-que-e-o-transtorno-do-espectro-autista-e-como-o-sus-tem-dado-assistencia-a-pacientes-e-familiares (relevância: 0.57)\n\n\n        ⚠️ IMPORTANTE: Esta é uma resposta informativa baseada em documentos públicos. \n        Não substitui consulta médica, psicológica ou de outros profissionais qualificados. \n        Sempre consulte profissionais de saúde para diagnóstico e tratamento.\n        ",
      "ground_truth": "Os sinais precoces incluem: falta de contato visual, não responder ao nome, não apontar objetos, atraso na fala, movimentos repetitivos, falta de sorriso social, e não imitar gestos simples.",
      "context": [
        "Ministério da Saúde do Brasil - Linha de Cuidado para TEA"
      ],
      "retrieved_contexts": [
        "Capacitação sobre Autismo\nE para oferecer mais acolhimento, conhecimento e informação para familiares de pacientes, cuidadores, educadores e profissionais de saúde o Ministério da Saúde também está ofertando quatro cursos sobre a temática do Autismo. Os materiais estão disponíveis no Ambiente Virtual de Aprendizagem do SUS (AVA-SUS) e na plataforma da Universidade Aberta do Sistema Único de Saúde (UNA-SUS).\nAlém disso, é ofertada uma capacitação profissional para uso da Caderneta da Criança, que vai possibilitar a compreensão da importância da caderneta como instrumento de vigilância do crescimento e desenvolvimento infantil. A capacitação é gratuita, em formato Educação a Distância (EAD) e não tem limitação de vagas. As inscrições podem ser feitas por meio da plataforma UNASUS/UFMA.\nFran Martins\nMinistério da Saúde",
        "Elyse Matos (ICO Project) \n                    Dr. Ami Klin (Emory University, Centro de Autismo de Marcus Children's Healthcare of Atlanta) \n                    Dr. Cíntia Guilardi (PUC-SP) \n                    Dra. Paula Gioia (PUC-SP) \n                    Psi. Eduardo Cassanho (Secretaria Municipal de Saúde de Curitiba/PR, Master Trainer do Programa de Treinamento de Pais e Cuidadores da OMS no Brasil) \n                    Dra. Cristiana Maragon (Secretaria Municipal de Saúde de Curitiba/PR) \n                    O grupo ainda contou com as valiosas contribuições de Willian Chimura, pessoa Autista, presidente da AUTINC (autistas pela inclusão), programador, youtuber e mestrando em Informática para Educação pelo IFRS, de  Nicolas Brito, pessoa com autismo, palestrante, escritor e fotógrafo premiado internacionalmente e sua mãe Anita Brito.",
        "Ações do MEC buscam a inclusão dos estudantes autistas — Ministério da Educação\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nIr para o\n      Conteúdo\n      1\n\n\nIr para a\n      Página Inicial\n      2\n\n\nIr para o menu de\n      Navegação\n      3\n\n\nIr para a\n      Busca\n      4\n\n\nIr para o\n      Mapa do site\n      5\n\n\n\n\nAtenção!\nSeu navegador não pode executar javascript. Alguns recursos podem não funcionar corretamente.\n\n\n\n\n\n\n\n\n\n\n\nAbrir menu principal de navegação\n\n\n\n\n\n\nMinistério da Educação\n\n\n\n\n\n                        Termos mais buscados\n                    \n\n\n\n\n                                   imposto de renda\n                                \n\n\n\n\n                                   inss\n                                \n\n\n\n\n                                   assinatura\n                                \n\n\n\n\n                                   cnh social"
      ]
    }
  ]
}
```

---
*Relatório gerado pelo sistema de avaliação RAGAS corrigida*