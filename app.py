from flask import Flask, render_template, request
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
@app.route("/danskekonger", methods=["GET", "POST"])
def danskekonger():
    answer = ""

    if request.method == "POST":
        question = request.form.get("question", "").strip()

        if not question:
            answer = "Skriv først et spørgsmål."
        else:
            try:
                response = client.responses.create(
                    model="gpt-4o-mini",
                    input=f"""
Du er en hjælpsom historielærer.

Brugeren må kun stille spørgsmål om danske konger.
Hvis spørgsmålet ikke handler om danske konger, skal du venligt forklare det.

Svar på dansk.

Spørgsmål:
{question}
"""
                )

                answer = response.output_text

            except Exception as e:
                answer = f"Der opstod en fejl: {str(e)}"

    return render_template("index.html", answer=answer)

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    questions = [
        {
            "question": "Hvilken konge forbindes især med Rundetårn?",
            "options": ["Christian 4.", "Frederik 7.", "Harald Blåtand"],
            "answer": "Christian 4."
        },
        {
            "question": "Hvilken konge gav Danmark grundloven i 1849?",
            "options": ["Christian 8.", "Frederik 7.", "Christian 9."],
            "answer": "Frederik 7."
        },
        {
            "question": "Hvilken konge er kendt for Jellingstenen?",
            "options": ["Gorm den Gamle", "Harald Blåtand", "Svend Tveskæg"],
            "answer": "Harald Blåtand"
        },
        {
            "question": "Hvem var Danmarks konge under besættelsen 1940-1945?",
            "options": ["Christian 10.", "Frederik 9.", "Christian 9."],
            "answer": "Christian 10."
        },
        {
            "question": "Hvilken konge blev kaldt Europas svigerfar?",
            "options": ["Frederik 6.", "Christian 9.", "Frederik 8."],
            "answer": "Christian 9."
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
