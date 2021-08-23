from flask import Flask
from flask import render_template, url_for

app = Flask(__name__)

#implement bootstrap and build out landing pages

projetcs = [
    {"title":"test project",
    "description":"This is the first project",
    "manager":"Kiren Panchoe",
    "id":"0"
    },
    {"title":"test project 2",
    "description":"This is the second project",
    "manager":"Kiren Panchoe",
    "id":"1"
    }

    ]



@app.route("/")
def homePage():
    return render_template("home.html", projects=projetcs)

#when implementing databases use project title
@app.route("/project/<project_id>")
def projectPage(project_id):
    project = projetcs[int(project_id)]
    return render_template("project.html", project=project)
if __name__ == "__main__":
    app.run(debug=True)