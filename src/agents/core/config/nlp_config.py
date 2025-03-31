from pydantic_settings import BaseSettings
from typing import Optional, List

class NLPConfig(BaseSettings):
    # Modelo base para el procesamiento de lenguaje natural
    MODEL_NAME: str = "microsoft/DialoGPT-small"  # Modelo más pequeño optimizado para diálogo
    
    # Configuración del modelo
    MAX_LENGTH: int = 128
    MIN_LENGTH: int = 10
    TEMPERATURE: float = 0.9
    TOP_K: int = 50
    TOP_P: float = 0.95
    
    # Configuración de la API
    API_TIMEOUT: int = 30
    BATCH_SIZE: int = 1
    
    # Paths
    MODEL_CACHE_DIR: str = "models/nlp/cache"
    
    # Idiomas soportados
    DEFAULT_LANGUAGE: str = "es"
    SUPPORTED_LANGUAGES: List[str] = ["es", "en"]
    
    class Config:
        env_file = ".env"