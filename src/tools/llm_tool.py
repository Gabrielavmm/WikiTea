"""
Ferramenta para interação com modelos de linguagem
"""

import os
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class LLMTool:
    """Ferramenta para interação com LLMs"""
    
    def __init__(self, model_type: str = "ollama", model_name: str = "llama3.1:8b"):
        """
        Inicializa a ferramenta LLM
        
        Args:
            model_type: Tipo do modelo ("ollama", "openai", "huggingface")
            model_name: Nome do modelo
        """
        self.model_type = model_type
        self.model_name = model_name
        self.llm = None
        self._initialize_llm()
    
    def _initialize_llm(self):
        """Inicializa o modelo de linguagem"""
        try:
            if self.model_type == "ollama":
                self._init_ollama()
            elif self.model_type == "openai":
                self._init_openai()
            elif self.model_type == "huggingface":
                self._init_huggingface()
            else:
                raise ValueError(f"Tipo de modelo não suportado: {self.model_type}")
                
            logger.info(f"✅ LLM inicializado: {self.model_name}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar LLM: {e}")
            # Fallback para um modelo simples
            self._init_fallback()
    
    def _init_ollama(self):
        """Inicializa Ollama"""
        try:
            from langchain_community.llms import Ollama
            
            self.llm = Ollama(
                model=self.model_name,
                temperature=0.7,
                top_p=0.9,
                num_ctx=4096
            )
            
        except ImportError:
            logger.warning("Ollama não disponível, usando fallback")
            raise
        except Exception as e:
            logger.error(f"Erro ao inicializar Ollama: {e}")
            raise
    
    def _init_openai(self):
        """Inicializa OpenAI"""
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
            
            # Configurar parâmetros se necessário
            if max_tokens and hasattr(self.llm, 'max_tokens'):
                self.llm.max_tokens = max_tokens
            
            # Gerar resposta
            response = self.llm.invoke(prompt)
            
            # Processar resposta baseado no tipo
            if hasattr(response, 'content'):
                return response.content
            elif isinstance(response, str):
                return response
            else:
                return str(response)
                
        except Exception as e:
            logger.error(f"❌ Erro ao gerar resposta: {e}")
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
            "tratamento": "O tratamento do autismo geralmente envolve terapias multidisciplinares, incluindo terapia comportamental, fonoaudiologia e acompanhamento médico. Cada caso é único e requer plano individualizado."
        }
    
    def invoke(self, prompt: str) -> str:
        """Gera resposta baseada em palavras-chave"""
        prompt_lower = prompt.lower()
        
        # Buscar palavra-chave mais relevante
        for keyword, response in self.responses.items():
            if keyword in prompt_lower:
                return response
        
        # Resposta genérica
        return """
        Esta é uma resposta informativa sobre autismo. 
        Para informações mais específicas, recomendo consultar:
        - Profissionais de saúde qualificados
        - Associações especializadas em autismo
        - Materiais oficiais do Ministério da Saúde
        
        ⚠️ Esta resposta não substitui consulta médica ou psicológica profissional.
        """

# Função de conveniência
def create_llm_tool(model_type: str = "ollama", model_name: str = "llama3.1:8b") -> LLMTool:
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