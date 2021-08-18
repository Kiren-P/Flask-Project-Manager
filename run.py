from flask import Flask
from flask import render_template

app = Flask(__name__)

#add dummy data and make cards


@app.route("/")
def hello_world():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)