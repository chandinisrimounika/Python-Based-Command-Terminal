from flask import Flask, request, jsonify, render_template, send_from_directory
from terminal import CommandTerminal
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
terminal = CommandTerminal()

@app.route("/")
def index():
    
    return render_template("index.html")

@app.route("/api/exec", methods=["POST"])
def exec_cmd():
    data = request.get_json(silent=True) or {}
    cmd = data.get("cmd", "")
    output = terminal.execute(cmd)
    return jsonify({"output": output})


@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
