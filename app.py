from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
import openai
import os

app = Flask(__name__)

# Configura tu API key de OpenAI (puedes usar variables de entorno en Render)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    # Captura lo que dijo el usuario en la llamada
    user_text = request.form.get("SpeechResult", "")

    # Consulta a OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Eres un asistente de salud amable que agenda citas y responde dudas médicas simples."},
            {"role": "user", "content": user_text}
        ]
    )

    reply = response.choices[0].message.content.strip()

    # Crea la respuesta de voz en TwiML
    twiml = VoiceResponse()
    twiml.say(reply, voice="Polly.Lupe", language="es-MX")

    return str(twiml)

if __name__ == "__main__":
    app.run(debug=True)
