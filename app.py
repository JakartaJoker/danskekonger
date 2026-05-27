from flask import Flask, render_template, request, Response
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
@app.route("/danskekonger")
def danskekonger():
    return render_template("index.html")


@app.route("/stream", methods=["POST"])
def stream():
    question = request.form.get("question", "").strip()

    if not question:
        return Response("Skriv først et spørgsmål.", mimetype="text/plain")

    def generate():
        try:
            stream = client.responses.create(
                model="gpt-4o-mini",
                stream=True,
                input=f"""
Du er en ekspert i Danmarks kongerække og dansk historie.

Regler:
- Svar altid på dansk.
- Svar kun på spørgsmål om danske konger og relateret dansk kongehistorie.
- Hvis spørgsmålet handler om noget andet, så forklar venligt at systemet kun handler om danske konger.
- Brug årstal når det er relevant.
- Vær faktuel og historisk præcis.
- Hvis historikere er uenige eller noget er usikkert, så sig det tydeligt.
- Skriv i et klart og pædagogisk sprog.
- Brug korte afsnit.
- Brug gerne punktlister ved længere svar.

Spørgsmål:
{question}
"""
            )

            for event in stream:
                if event.type == "response.output_text.delta":
                    yield event.delta

        except Exception as e:
            yield f"\n\nDer opstod en fejl: {str(e)}"

    return Response(generate(), mimetype="text/plain")


if __name__ == "__main__":
    app.run(debug=True)
