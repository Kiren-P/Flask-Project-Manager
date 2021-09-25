from enum import unique
from flask import Flask
from flask import render_template, redirect, url_for, request
from flask.templating import render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)
    manager = db.Column(db.String, nullable=False) #person who manages the project
    tasks = db.relationship("Task", backref="task", lazy=True)

    def __repr__(self):
        return f"Project('{self.id}', '{self.title}', '{self.description}', '{self.manager}')"

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=False, nullable=False)
    description = db.Column(db.String)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)

    def __repr__(self):
        return f"Task('{self.title}', '{self.description}')"


@app.route("/", methods=["GET", "POST"] )
def homePage():
    projects_all = Project.query.all()
    return render_template("home.html", projects=projects_all)

@app.route("/NewProject", methods=["GET", "POST"])
def newProject():
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")
        manager = request.form.get("manager")
        new_project = Project(title=title, description=desc, manager=manager)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for("homePage"))
    return render_template("new_project.html")

@app.route("/project/<project_title>", methods=["POST", "GET"])
def projectPage(project_title):
    project = Project.query.filter_by(title=str(project_title)).first()
    tasks = project.tasks
    return render_template("project.html", project=project, tasks=tasks)

@app.route("/edit/<project_title>", methods=["POST", "GET"])
def editProject(project_title):
    project = Project.query.filter_by(title=project_title).first()
    if request.method == "POST":
        new_title = request.form.get("project_title")
        new_desc = request.form.get("project_desc")
        project.title = new_title
        project.description = new_desc
        db.session.commit()
        return redirect(url_for("projectPage", project_title=project.title))
    return render_template("edit_project.html", project=project)

@app.route("/delete/<project_title>", methods=["POST"])
def deleteProject(project_title):
    if request.method == "POST":
        project = Project.query.filter_by(title=project_title).first()
        tasks = project.tasks
        for task in tasks:
            db.session.delete(task)
        Project.query.filter_by(title=project_title).delete()
        db.session.commit()
        return redirect(url_for("homePage"))

@app.route("/<project_title>/AddTask", methods=["POST", "GET"])
def addTask(project_title):
    project = Project.query.filter_by(title=str(project_title)).first()
    if request.method == "POST":
        task_title = request.form.get("task_title")
        task_desc = request.form.get("task_desc")
        projectID = project.id
        new_task = Task(title=task_title, description=task_desc, project_id=projectID)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("projectPage", project_title=project_title))
    return render_template("add_task.html", project=project)

@app.route("/project/<project_title>/<task_title>", methods=["POST", "GET"])
def taskPage(project_title, task_title):
    project = Project.query.filter_by(title=str(project_title)).first()
    tasks = project.tasks
    for i in tasks:
        title = i.title
        if task_title == title:
            task = i
    return render_template("tasks.html", task=task, project=project)

@app.route("/edit/<project_title>/<task_title>", methods=["POST", "GET"])
def editTask(project_title, task_title):
    project = Project.query.filter_by(title=str(project_title)).first()
    tasks = project.tasks
    for i in tasks:
        title = i.title
        if task_title == title:
            task = i 
    if request.method == "POST":
        new_task_title = request.form.get("task_title")
        new_task_desc = request.form.get("task_desc")
        task.title = new_task_title
        task.description = new_task_desc
        db.session.commit()
        return redirect(url_for("taskPage", project_title=project.title, task_title=task.title))
    return render_template("edit_tasks.html", project=project, task=task)

@app.route("/delete/<project_title>/<task_title>", methods=["POST"])
def deleteTask(project_title, task_title):
    project = Project.query.filter_by(title=str(project_title)).first()
    tasks = project.tasks
    for i in tasks:
        title = i.title
        if title == task_title:
            task = i
    if request.method == "POST":
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for("projectPage", project_title=project.title))
        
if __name__ == "__main__":
    app.run()