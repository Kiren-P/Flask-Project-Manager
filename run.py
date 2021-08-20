from flask import Flask
from flask import render_template, url_for

app = Flask(__name__)

#handle logic for project landing pages
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

@app.route("/project")
def projectPage():
    return render_template("project.html")

if __name__ == "__main__":
    app.run(debug=True)