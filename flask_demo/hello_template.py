from flask import Flask, render_template
import time
app = Flask(__name__)

@app.route("/")
def hello():
    now = str(time.time())
    templateData = {
        "title": "Hello, Flask!",
        "time": now
    }

    return render_template('./main.html', **templateData)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)