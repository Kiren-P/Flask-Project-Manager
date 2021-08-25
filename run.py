from flask import Flask
from flask import render_template, url_for

app = Flask(__name__)

#rebuild frontend with bootstrap

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
    },
    {"title":"test project 3",
    "description":"This is the thirdf project",
    "manager":"Kiren Panchoe",
    "id":"2"
    },
    {"title":"test project 4",
    "description":"This is the fourth project",
    "manager":"Kiren Panchoe",
    "id":"2"
    },
    {"title":"test project 5",
    "description":"This is the five project",
    "manager":"Kiren Panchoe",
    "id":"2"
    },
    {"title":"test project 6",
    "description":"This is the five project",
    "manager":"Kiren Panchoe",
    "id":"2"
    },
    {"title":"test project 7",
    "description":"This is the five project",
    "manager":"Kiren Panchoe",
    "id":"2"
    },
    {"title":"test project 8",
    "description":"This is the five project",
    "manager":"Kiren Panchoe",
    "id":"2"
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