from flask import Flask, request, render_template
from app.agents.orchestrator_agent import run_orchestrator

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    hubspot_response = ""
    email_response = ""
    user_query = ""

    if request.method == "POST":
        user_query = request.form.get("query")
        result = run_orchestrator(user_query)

        hubspot_response = result.get("hubspot_response", "")
        email_response = result.get("email_response", "")

    return render_template("index.html", query=user_query, hubspot_response=hubspot_response, email_response=email_response)

if __name__ == "__main__":
    app.run(debug=True)
