# Bot Bancario para Telegram 🏦

Bot conversacional para Telegram que implementa servicios típicos de una entidad bancaria con procesamiento de lenguaje natural e integración con IA.

## Funcionalidades 🚀

- **Autenticación**: Verificación de PIN (por defecto: 1234)
- **Consulta de saldo**: Obtener saldo actual de cuenta
- **Movimientos**: Los usuarios tienen 4 movimientos por defecto al crearse (depósito inicial, compra, transferencia y pago)
- **Simulación de préstamos**: Tasas personalizadas según interacciones del usuario (mejora con el uso)
- **Consultas generales mediante IA**: Respuestas vía OpenAI sobre productos bancarios
- **Persistencia**: Base de datos SQLite

## Requisitos técnicos 💻

- Python 3.10+
- Telegram Bot API Token
- OpenAI API Key (indispensable para las consultas generales bancarias)

## Instalación 🛠️

1. **Clonar el repositorio**

```bash
git clone https://github.com/tuusuario/bot-bancario.git
cd bot-bancario
```

2. **Configurar .env**

```bash
TELEGRAM_TOKEN=tu_token_aqui
OPENAI_API_KEY=tu_api_key_aqui  # Necesaria para responder consultas bancarias
```

3. **Instalar dependencias y ejecutar**

```bash
pip install -r requirements.txt
python main.py
```

## Uso con Docker 🐳

```bash
# Construir y ejecutar
docker build -t bot-bancario .
docker run -d --name bot-bancario -v $(pwd)/data:/app/data --env-file .env bot-bancario
```

## Estructura del proyecto 📁

```
├── main.py      # Código principal del bot
├── db.py        # Base de datos SQLite
├── logic.py     # Lógica de préstamos
├── ai.py        # Integración con OpenAI
├── Dockerfile   # Configuración Docker
└── README.md
```

## Comandos disponibles 📝

- `/start` - Iniciar y autenticarse
- `/saldo` - Consultar saldo
- `/movimientos` - Ver movimientos
- `/prestamo` - Simular préstamo
- `/cancelar` - Cancelar proceso
- `/ayuda` - Ver comandos

El bot también responde a lenguaje natural:

- "¿Cuánto tengo en mi cuenta?"
- "Necesito un préstamo"
- "¿Qué tarjetas ofrecen?"

## Valores por defecto 🔑

- **PIN de acceso**: 1234
- **Saldo inicial**: $9,000 (generado por los movimientos iniciales)
- **Tasa de préstamos**: 55% TEA base, con descuento según interacciones del usuario
- **Límite de préstamo**: $5,000,000
- **Plazo máximo**: 60 meses

## Notas sobre la implementación 🔍

Al recibir el correo con la prueba técnica, observé que el documento indicaba un tiempo estimado de 8 horas para completar la tarea. Sin embargo, no me quedo claro si ese tiempo era a partir de la recepción del correo o si debía gestionarlo de manera autónoma. Debido a esto, deduje que debía completar la prueba en un plazo de 8 horas desde el envío del correo, pero luego de algunos imprevistos personales, decidí enviarla a las 16:30, tras haber dedicado 5 horas al desarrollo. A pesar de no haber podido perfeccionarlo por completo, lo hago con la intención de entregar una solución funcional dentro del tiempo disponible, aunque reconozco que podría haber optimizado ciertos aspectos si hubiera tenido más tiempo.
Por otro lado, en cuanto a la implementación de la inteligencia artificial, el documento sugería su uso, por lo que decidí integrar OpenAI a través de ChatGPT. Durante el proceso, desarrollé toda la lógica para la integración, pero lamentablemente no pude probarla de manera exhaustiva, ya que no cuento con una API Key para OpenAI debido a que es un servicio pago. Me imaginé que, en un futuro, en caso de poder colaborar con ustedes, tendría acceso a las claves necesarias para probar y afinar la integración de manera correcta. Sin embargo, reconozco que no haber podido probarlo a fondo limita la verificación de su funcionamiento, y aunque creo que la implementación está bien planteada, podría haber algún error que sería necesario corregir.
Agradezco mucho la oportunidad de haber podido realizar esta prueba técnica y la comprensión frente a las limitaciones que pude haber tenido durante el proceso. Espero que la solución presentada sea de su agrado y que haya cumplido con las expectativas.
