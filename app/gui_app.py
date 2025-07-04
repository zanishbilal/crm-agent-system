from flask import Flask, request, render_template
from app.agents.orchestrator_agent import run_orchestrator
import os  # Add this

app = Flask(__name__, template_folder="app/templates")

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
    port = int(os.environ.get("PORT", 5000))  # Use Railway's PORT or default to 5000
    app.run(host="0.0.0.0", port=port)  # Dynamically bind to PORT