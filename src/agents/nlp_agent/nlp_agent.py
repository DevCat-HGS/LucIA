from transformers import pipeline
import torch
from typing import Dict, List, Optional
from loguru import logger
from ..core.config.nlp_config import NLPConfig

class NLPAgent:
    def __init__(self, config: Optional[NLPConfig] = None):
        self.config = config or NLPConfig()
        self._initialize_model()
        self.conversation_history = []
        
    def _initialize_model(self):
        """Inicializa el modelo y tokenizer"""
        try:
            logger.info(f"Cargando modelo {self.config.MODEL_NAME}")
            device = "cuda" if torch.cuda.is_available() else "cpu"
            
            # Usar pipeline de generación de texto
            self.generator = pipeline(
                "text-generation",
                model=self.config.MODEL_NAME,
                device=device
            )
            logger.info(f"Modelo cargado exitosamente en dispositivo: {device}")
        except Exception as e:
            logger.error(f"Error al cargar el modelo: {e}")
            raise

    def process_input(self, text: str, language: str = None) -> str:
        """Procesa el texto de entrada y genera una respuesta"""
        try:
            language = language or self.config.DEFAULT_LANGUAGE
            
            # Preparar el contexto con el historial de conversación
            context = self._prepare_conversation_context(text)
            
            # Generar respuesta
            response = self.generator(
                context,
                max_length=self.config.MAX_LENGTH,
                min_length=self.config.MIN_LENGTH,
                temperature=self.config.TEMPERATURE,
                top_k=self.config.TOP_K,
                top_p=self.config.TOP_P,
                do_sample=True,
                num_return_sequences=1
            )
            
            # Extraer la respuesta generada
            generated_text = response[0]['generated_text']
            # Limpiar la respuesta para obtener solo la última parte (la respuesta del asistente)
            assistant_response = self._extract_assistant_response(generated_text, text)
            
            # Agregar la interacción al historial
            self.conversation_history.append({"role": "user", "content": text})
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response
            
        except Exception as e:
            logger.error(f"Error al procesar entrada: {e}")
            return "Lo siento, hubo un error al procesar tu mensaje."

    def _prepare_conversation_context(self, new_message: str) -> str:
        """Prepara el contexto de la conversación para el modelo"""
        context = "La siguiente es una conversación amigable entre un humano y un asistente de IA llamado LucIA.\n\n"
        
        # Agregar las últimas 3 interacciones del historial
        for message in self.conversation_history[-6:]:  # Últimas 3 interacciones (6 mensajes)
            prefix = "Humano: " if message["role"] == "user" else "LucIA: "
            context += prefix + message["content"] + "\n"
            
        # Agregar el nuevo mensaje
        context += "Humano: " + new_message + "\nLucIA:"
        return context

    def _extract_assistant_response(self, generated_text: str, original_input: str) -> str:
        """Extrae la respuesta del asistente del texto generado"""
        # Encontrar la última ocurrencia de "LucIA:" en el texto
        parts = generated_text.split("LucIA:")
        if len(parts) > 1:
            response = parts[-1].strip()
        else:
            # Si no se encuentra "LucIA:", tomar el texto después del input
            response = generated_text.split(original_input)[-1].strip()
        
        return response

    def clear_history(self):
        """Limpia el historial de conversación"""
        self.conversation_history = []

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Retorna el historial de conversación"""
        return self.conversation_history