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

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    questions = [
        {
            "question": "Hvilken konge forbindes især med Rundetårn?",
            "options": ["Christian 4.", "Frederik 7.", "Harald Blåtand"],
            "answer": "Christian 4.",
            "explanation": "Christian 4. lod Rundetårn opføre i København. Tårnet stod færdigt i 1642."
        },
        {
            "question": "Hvilken konge gav Danmark grundloven i 1849?",
            "options": ["Christian 8.", "Frederik 7.", "Christian 9."],
            "answer": "Frederik 7.",
            "explanation": "Frederik 7. underskrev Danmarks Grundlov den 5. juni 1849."
        },
        {
            "question": "Hvilken konge er kendt for Jellingstenen?",
            "options": ["Gorm den Gamle", "Harald Blåtand", "Svend Tveskæg"],
            "answer": "Harald Blåtand",
            "explanation": "Harald Blåtand lod Jellingstenen rejse og omtales ofte som den konge, der samlede Danmark."
        },
        {
            "question": "Hvem var Danmarks konge under besættelsen 1940-1945?",
            "options": ["Christian 10.", "Frederik 9.", "Christian 9."],
            "answer": "Christian 10.",
            "explanation": "Christian 10. var konge under den tyske besættelse af Danmark fra 1940 til 1945."
        },
        {
            "question": "Hvilken konge blev kaldt Europas svigerfar?",
            "options": ["Frederik 6.", "Christian 9.", "Frederik 8."],
            "answer": "Christian 9.",
            "explanation": "Christian 9. blev kaldt Europas svigerfar, fordi hans børn blev gift ind i flere europæiske kongehuse."
        }
    ]

    score = None

    if request.method == "POST":
        score = 0
        for i, q in enumerate(questions):
            user_answer = request.form.get(f"q{i}")
            if user_answer == q["answer"]:
                score += 1

    return render_template("quiz.html", questions=questions, score=score)

if __name__ == "__main__":
    app.run(debug=True)
