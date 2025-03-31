from agents.nlp_agent.nlp_agent import NLPAgent
from loguru import logger

def main():
    try:
        # Inicializar el agente NLP
        logger.info("Inicializando el agente NLP...")
        agent = NLPAgent()
        
        # Probar una conversación simple
        logger.info("Iniciando conversación de prueba...")
        
        # Primera interacción
        response = agent.process_input("Hola, ¿cómo estás?")
        print(f"\nUsuario: Hola, ¿cómo estás?")
        print(f"LucIA: {response}\n")
        
        # Segunda interacción
        response = agent.process_input("¿Cuál es tu propósito?")
        print(f"Usuario: ¿Cuál es tu propósito?")
        print(f"LucIA: {response}\n")
        
    except Exception as e:
        logger.error(f"Error durante la prueba: {e}")

if __name__ == "__main__":
    main()