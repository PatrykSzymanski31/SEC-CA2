from flask import Flask
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Secure Cloud Lab</h1>
    <p>Frontend app is running.</p>
    <p>Try <a href='/backend'>/backend</a> to call the internal API.</p>
    """

@app.route("/backend")
def backend():
    try:
        response = requests.get("http://internal-api:80", timeout=5)
        return f"<h1>Backend Response</h1><pre>{response.text}</pre>"
    except Exception as e:
        return f"<h1>Error reaching backend</h1><pre>{e}</pre>", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

