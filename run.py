from flask import Flask
from flask import render_template

app = Flask(__name__)

#learn how to work with grrids in css
projetcs = [
    {"title":"test project",
    "description":"This is the first project",
    "manager":"Kiren Panchoe"
    },
    {"title":"test project 2",
    "description":"This is the second project",
    "manager":"Kiren Panchoe"
    }

    ]



@app.route("/")
def hello_world():
    return render_template("home.html", projects=projetcs)

if __name__ == "__main__":
    app.run(debug=True)