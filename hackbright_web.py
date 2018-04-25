"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/")
def homepage():
	"""Rendering homepage"""

	return render_template("homepage.html")

@app.route("/student-search")
def get_student_form():
	"""Show form for searing for a student."""

	return render_template("student_search.html")


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    grades = hackbright.get_grades_by_github(github)

    html = render_template("student_info.html",
    						first=first,
    						last=last,
    						github=github,
    						grades=grades)

    return html


@app.route("/add-form")
def get_add_form():
	"""Show form for adding a student."""

	return render_template("student_add.html")


@app.route("/student-add", methods=['POST'])
def student_add():
	"""Add a student."""

	first = request.form.get("first_name")
	last = request.form.get("last_name")
	github = request.form.get("github")

	hackbright.make_new_student(first, last, github)

	return render_template("new_info.html", first=first, last=last, github=github)

@app.route("/get-project-title")
def get_project_title():
	"""Show form for project title"""

	return render_template("get_project_title.html")


@app.route("/get-project")
def get_project():
	"""Get project information based on title."""

	title = request.args.get("title")

	project = hackbright.get_project_by_title(title)

	student = hackbright.get_grades_by_title(title)

	return render_template("project_info.html", title=project[0], description=project[1],
							max_grade=project[2], students=student)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
