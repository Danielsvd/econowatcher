from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Botul este online."

app.run(host="0.0.0.0", port=3000)
