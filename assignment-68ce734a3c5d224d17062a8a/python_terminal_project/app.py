from flask import Flask, request, jsonify, send_from_directory
from terminal import CommandTerminal
import os

app = Flask(__name__)
terminal = CommandTerminal()

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/api/exec", methods=["POST"])
def exec_cmd():
    data = request.get_json()
    cmd = data.get("cmd", "")
    output = terminal.execute(cmd)
    return jsonify({"output": output})

if __name__ == "__main__":
    app.run(debug=True)
