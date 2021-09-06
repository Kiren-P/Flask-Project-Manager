from enum import unique
from flask import Flask
from flask import render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)

#find a way to implement tasks

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)
    manager = db.Column(db.String, nullable=False)
    #tasks

    def __repr__(self):
        return f"Project('{self.id}', '{self.title}', '{self.description}', '{self.manager}')"


@app.route("/", methods=["GET", "POST"] )
def homePage():
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")
        manager = request.form.get("manager")
        new_project = Project(title=title, description=desc, manager=manager)
        db.session.add(new_project)
        db.session.commit()
    projects_all = Project.query.all()
    return render_template("home.html", projects=projects_all)

@app.route("/NewProject", methods=["GET", "POST"])
def newProject():
    return render_template("new_project.html")


@app.route("/project/<project_title>")
def projectPage(project_title):
    project = Project.query.filter_by(title=str(project_title)).first()
    return render_template("project.html", project=project)

if __name__ == "__main__":
    app.run(debug=True)