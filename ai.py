import os
import openai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configurar la API de OpenAI
openai.api_key = OPENAI_API_KEY

# Contexto para preguntas bancarias
BANKING_CONTEXT = """
Eres un asistente bancario inteligente. Responde preguntas sobre servicios bancarios con información precisa.
La entidad para la que trabajas ofrece:

Tarjetas de crédito:
- Visa Classic: Límite de $200,000, 3 cuotas sin interés
- Visa Gold: Límite de $500,000, 6 cuotas sin interés, seguro de viaje
- Mastercard Platinum: Límite de $1,000,000, 12 cuotas sin interés, acceso a salas VIP

Plazos fijos:
- Plazo fijo tradicional: Tasa nominal anual del 43% a 30 días
- Plazo fijo UVA: Inflación + 1% anual, mínimo 90 días

Préstamos personales:
- Tasa para clientes: 55% TEA
- Monto máximo: $5,000,000
- Plazo máximo: 60 meses

Da respuestas concisas y claras. Si no estás seguro de algo, indica que consultarán con un asesor.
"""


async def get_ai_response(user_message):
    """
    Obtiene una respuesta de la API de OpenAI para consultas bancarias

    Args:
        user_message: Mensaje del usuario

    Returns:
        str: Respuesta del asistente
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": BANKING_CONTEXT},
                {"role": "user", "content": user_message}
            ],
            max_tokens=200,
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error con OpenAI: {e}")
        return "Lo siento, no puedo responder esa consulta en este momento. Por favor, intenta más tarde."


async def detect_intent(message):
    """
    Detecta la intención del usuario basada en su mensaje

    Args:
        message: Mensaje del usuario

    Returns:
        str: Intención detectada
    """
    message = message.lower()

    # Detectar intenciones relacionadas con saldo
    if any(word in message for word in ['saldo', 'tengo', 'cuánto', 'cuenta', 'disponible']):
        return "saldo"

    # Detectar intenciones relacionadas con movimientos
    if any(word in message for word in ['movimientos', 'transacciones', 'gastos', 'últimos', 'recientes']):
        return "movimientos"

    # Detectar intenciones relacionadas con préstamos
    if any(word in message for word in ['préstamo', 'crédito', 'solicitar', 'pedir', 'necesito dinero']):
        return "prestamo"

    # Si no se detecta una intención específica, usar la IA
    return "general"


async def get_ai(user_message):
    """Función principal para procesar mensajes con IA"""
    intent = await detect_intent(user_message)

    if intent == "general":
        return await get_ai_response(user_message)

    return intent
