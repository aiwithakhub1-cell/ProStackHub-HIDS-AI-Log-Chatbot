from flask import (
    Flask,
    render_template,
    request,
    jsonify
)

from database import (
    initialize_database,
    get_alerts,
    get_alert_summary
)

from ai_chatbot import ask_ai
from log_watcher import start_log_watcher


app = Flask(__name__)


initialize_database()

observer = start_log_watcher()


@app.route("/")
def dashboard():

    alerts = get_alerts()

    summary = get_alert_summary()

    return render_template(
        "dashboard.html",
        alerts=alerts,
        summary=summary
    )


@app.route("/api/alerts")
def api_alerts():

    return jsonify({
        "alerts": get_alerts(),
        "summary": get_alert_summary()
    })


@app.route("/chat", methods=["POST"])
def chat():
    try:
        question = request.form.get("question", "").strip()

        if not question:
            return jsonify({
                "answer": "Please enter a question."
            }), 400

        answer = ask_ai(question)

        return jsonify({
            "answer": answer
        })

    except Exception as error:
        print(f"Chat error: {error}")

        return jsonify({
            "answer": f"Chat error: {error}"
        }), 500


if __name__ == "__main__":

    try:

        app.run(
            host="127.0.0.1",
            port=5001,
            debug=False
        )

    finally:

        observer.stop()
        observer.join()