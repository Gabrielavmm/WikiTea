"""
Ferramenta para interação com modelos de linguagem
"""

import os
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class LLMTool:
    """Ferramenta para interação com LLMs"""
    
    def __init__(self, model_type: str = None, model_name: str = None):
        """
        Inicializa a ferramenta LLM
        
        Args:
            model_type: Tipo do modelo ("openai", "huggingface")
            model_name: Nome do modelo
        """
        # Usar configurações do settings.py se não especificado
        if model_type is None or model_name is None:
            from src.config.settings import settings
            self.model_type = model_type or settings.LLM["model_type"]
            self.model_name = model_name or settings.LLM["model_name"]
        else:
            self.model_type = model_type
            self.model_name = model_name
            
        self.llm = None
        self._initialize_llm()
    
    def _initialize_llm(self):
        """Inicializa o modelo de linguagem"""
        try:
            if self.model_type == "openai":
                self._init_openai()
            elif self.model_type == "huggingface":
                self._init_huggingface()
            else:
                raise ValueError(f"Tipo de modelo não suportado: {self.model_type}. Suportado: 'openai', 'huggingface'")
                
            logger.info(f"✅ LLM inicializado: {self.model_name}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar LLM: {e}")
            # Fallback para um modelo simples
            self._init_fallback()
    
    
    def _init_openai(self):
        """Inicializa OpenAI"""
        try:
            # Tentar usar langchain_openai primeiro
            try:
                from langchain_openai import ChatOpenAI
                
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    raise ValueError("OPENAI_API_KEY não encontrada")
                
                self.llm = ChatOpenAI(
                    model=self.model_name,
                    temperature=0.7,
                    max_tokens=2048
                )
            except ImportError:
                # Fallback para openai direto
                import openai
                
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    raise ValueError("OPENAI_API_KEY não encontrada")
                
                # Configurar cliente OpenAI
                openai.api_key = api_key
                self.llm = "openai_direct"  # Marcador para usar método direto
            
        except ImportError:
            logger.warning("OpenAI não disponível, usando fallback")
            raise
        except Exception as e:
            logger.error(f"Erro ao inicializar OpenAI: {e}")
            raise
    
    def _init_huggingface(self):
        """Inicializa HuggingFace"""
        try:
            from langchain_community.llms import HuggingFacePipeline
            from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
            
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
            pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_length=512,
                temperature=0.7,
                do_sample=True
            )
            
            self.llm = HuggingFacePipeline(pipeline=pipe)
            
        except ImportError:
            logger.warning("HuggingFace não disponível, usando fallback")
            raise
        except Exception as e:
            logger.error(f"Erro ao inicializar HuggingFace: {e}")
            raise
    
    def _init_fallback(self):
        """Inicializa um modelo fallback simples"""
        logger.warning("Usando modelo fallback simples")
        self.llm = SimpleFallbackLLM()
    
    def generate_response(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """
        Gera uma resposta baseada no prompt
        
        Args:
            prompt: Prompt para o modelo
            max_tokens: Número máximo de tokens (se suportado)
            
        Returns:
            Resposta gerada pelo modelo
        """
        try:
            if not self.llm:
                raise RuntimeError("LLM não foi inicializado")
            
            # Se usando OpenAI direto
            if self.llm == "openai_direct":
                return self._generate_openai_direct(prompt, max_tokens)
            
            # Configurar parâmetros se necessário
            if max_tokens and hasattr(self.llm, 'max_tokens'):
                self.llm.max_tokens = max_tokens
            
            # Gerar resposta
            response = self.llm.invoke(prompt)
            logger.debug(f"🔍 Resposta bruta do LLM: {response!r}")

            
            # Processar resposta baseado no tipo
            if hasattr(response, 'content') and response.content:
                
                return response.content.strip()
            if isinstance(response, str) and response.strip():
                return response.strip()
            logger.debug(f"🔍 Conteúdo final extraído: {response.content if hasattr(response,'content') else response}")
            return str(response.strip)
                
        except Exception as e:
            logger.error(f"❌ Erro ao gerar resposta: {e}")
            return self._get_error_response()
    
    def _generate_openai_direct(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """Gera resposta usando OpenAI diretamente"""
        try:
            import openai
            
            response = openai.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=max_tokens or 2048
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"❌ Erro na API OpenAI direta: {e}")
            return self._get_error_response()
    
    def _get_error_response(self) -> str:
        """Resposta de erro quando o LLM falha"""
        return """
        Desculpe, ocorreu um erro ao processar sua pergunta. 
        Por favor, tente novamente ou reformule sua pergunta.
        """
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Retorna informações sobre o modelo
        
        Returns:
            Dicionário com informações do modelo
        """
        return {
            "model_type": self.model_type,
            "model_name": self.model_name,
            "initialized": self.llm is not None
        }

class SimpleFallbackLLM:
    """LLM fallback simples para quando outros modelos não estão disponíveis"""
    
    def __init__(self):
        self.responses = {
            "autismo": "O Transtorno do Espectro Autista (TEA) é uma condição do desenvolvimento neurológico que afeta a comunicação, interação social e comportamento. É importante consultar profissionais qualificados para diagnóstico e tratamento adequado.",
            "tea": "TEA (Transtorno do Espectro Autista) é caracterizado por dificuldades na comunicação social e padrões restritos de comportamento. Cada pessoa com TEA é única e pode apresentar diferentes características.",
            "sintomas": "Os sintomas do autismo podem incluir dificuldades na comunicação social, interesses restritos, comportamentos repetitivos e sensibilidade sensorial. É importante buscar avaliação profissional.",
            "tratamento": "O tratamento do autismo geralmente envolve terapias multidisciplinares, incluindo terapia comportamental, fonoaudiologia e acompanhamento médico. Cada caso é único e requer plano individualizado.",
            "diagnóstico": "O diagnóstico de TEA é feito por profissionais especializados através de avaliação clínica e testes padronizados. É importante buscar avaliação precoce para intervenção adequada.",
            "terapia": "As terapias para autismo incluem ABA (Análise do Comportamento Aplicada), terapia ocupacional, fonoaudiologia e intervenções educacionais especializadas.",
            "inclusão": "A inclusão de pessoas com autismo na escola e sociedade é fundamental. Requer adaptações, apoio especializado e compreensão das necessidades individuais.",
            "direitos": "Pessoas com autismo têm direitos garantidos por lei, incluindo acesso à educação, saúde e inclusão social. A Lei Brasileira de Inclusão protege esses direitos.",
            "família": "Famílias de pessoas com autismo precisam de apoio, informação e recursos. Existem associações e grupos de apoio que podem ajudar.",
            "desenvolvimento": "O desenvolvimento de pessoas com autismo é único. Com apoio adequado, podem desenvolver habilidades e ter uma vida plena."
        }
    
    def invoke(self, prompt: str) -> str:
        """Gera resposta baseada em palavras-chave"""
        prompt_lower = prompt.lower()
        
        # Buscar palavra-chave mais relevante
        best_match = None
        best_score = 0
        
        for keyword, response in self.responses.items():
            if keyword in prompt_lower:
                # Dar prioridade para correspondências exatas
                score = len(keyword) if keyword in prompt_lower else 0
                if score > best_score:
                    best_score = score
                    best_match = response
        
        if best_match:
            return best_match
        
        # Se não encontrou correspondência específica, tentar palavras relacionadas
        related_keywords = {
            "o que é": "autismo",
            "como funciona": "desenvolvimento", 
            "quais são": "sintomas",
            "como tratar": "tratamento",
            "como diagnosticar": "diagnóstico",
            "escola": "inclusão",
            "lei": "direitos",
            "pais": "família"
        }
        
        for question_word, keyword in related_keywords.items():
            if question_word in prompt_lower:
                return self.responses[keyword]
        
        # Resposta genérica mais informativa
        return """
        O Transtorno do Espectro Autista (TEA) é uma condição do desenvolvimento neurológico que afeta a comunicação, interação social e comportamento. 

        Características principais:
        - Dificuldades na comunicação social
        - Padrões restritos e repetitivos de comportamento
        - Interesses específicos e intensos
        - Sensibilidade sensorial

        É importante lembrar que:
        - Cada pessoa com autismo é única
        - O diagnóstico deve ser feito por profissionais qualificados
        - Existem diversas terapias e intervenções disponíveis
        - A inclusão social e educacional é fundamental

        Para informações mais específicas, recomendo consultar:
        - Profissionais de saúde qualificados (médicos, psicólogos, fonoaudiólogos)
        - Associações especializadas em autismo
        - Materiais oficiais do Ministério da Saúde
        - Centros de referência em TEA

        ⚠️ IMPORTANTE: Esta resposta é apenas informativa e não substitui consulta médica ou psicológica profissional.
        """

# Função de conveniência
def create_llm_tool(model_type: str = "openai", model_name: str = "gpt-3.5-turbo") -> LLMTool:
    """Cria e retorna uma instância da ferramenta LLM"""
    return LLMTool(model_type=model_type, model_name=model_name)

if __name__ == "__main__":
    # Teste básico
    llm = create_llm_tool()
    info = llm.get_model_info()
    print(f"Informações do modelo: {info}")
    
    # Teste de geração
    response = llm.generate_response("O que é autismo?")
    print(f"Resposta: {response}")