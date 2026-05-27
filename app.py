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

if __name__ == "__main__":
    app.run(debug=True)
