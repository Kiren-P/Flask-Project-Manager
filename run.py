from enum import unique
from flask import Flask
from flask import render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)

#make  tasks page and display tasks

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)
    manager = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", backref="task", lazy=True)

    def __repr__(self):
        return f"Project('{self.id}', '{self.title}', '{self.description}', '{self.manager}')"

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)

    def __repr__(self):
        return f"Task('{self.title}', '{self.description}')"


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


@app.route("/project/<project_title>", methods=["POST", "GET"])
def projectPage(project_title):
    project = Project.query.filter_by(title=str(project_title)).first()
    if request.method == "POST":
        task_title = request.form.get("task_title")
        task_desc = request.form.get("task_desc")
        projectID = project.id
        new_task = Task(title=task_title, description=task_desc, project_id=projectID)
        db.session.add(new_task)
        db.session.commit()
    tasks = project.tasks
    return render_template("project.html", project=project, tasks=tasks)

@app.route("/<project_title>/AddTask")
def addTask(project_title):
    project = Project.query.filter_by(title=str(project_title)).first()
    return render_template("add_task.html", project=project)

@app.route("/project/<project_title>/tasks", methods=["POST", "GET"])
def taskPage(project_title):
    #use this to create project page with tasks properly displayed
    return render_template("tasks.html")



if __name__ == "__main__":
    app.run(debug=True)