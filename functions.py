from datetime import datetime
import psycopg2
import os
from groq import Groq
from variables import config


def bbdd(pregunta, respuesta):
    conn = psycopg2.connect(**config)
    cursor = conn.cursor()
    query = "INSERT INTO preguntas_respuestas(preguntas, respuestas, fechas) VALUES (%s, %s, %s)"
    cursor.execute(query, (pregunta, respuesta, datetime.now()))
    conn.commit()
    cursor.close()
    conn.close()
    return "ok"




def llm(pregunta):
    client = Groq(
        api_key=os.environ.get("KEY_GROQ"),
    )

    chat_completion = client.chat.completions.create(
        messages = [
            {
                "role": "system",
                "content": """
                    Eres un tutor altamente experimentado en programación, ciencia de datos, SQL, Data Engineering y Data Analysis.  
                    Debes responder siempre en el mismo idioma en que se formule la pregunta. (Si la pregunta fue en ingles, responde en ingles, en espanol y cualquier otra lengua haga lo mismo)
                    Tu misión es ayudar al usuario a comprender conceptos, resolver problemas y aprender buenas prácticas en estos temas.  
                    Si alguien pregunta sobre otro tema, indícale educadamente que solo puedes ayudar con programación y anima a que haga otra pregunta relevante.  
                    Incluye ejemplos de código cuando sea posible.
                    Siempre que sea útil, proporciona consejos de buenas prácticas o alternativas para resolver problemas.
                    """
            },

            {
                "role":"user",
                "content":pregunta
            }
        ],
        model="openai/gpt-oss-20b",
        stream=False,
    )

    return (chat_completion.choices[0].message.content)

