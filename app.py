from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import flash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "secretkeey"

db = SQLAlchemy(app)

class students(db.Model):
	id = db.Column('student_id', db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	grade = db.Column(db.String(3))

def __init__(self, name, grade):
	self.name = name
	self.grade = grade

@app.route('/', methods=['GET', 'POST'])
def addstudent():
	if request.method == 'POST':
		if not request.form['name'] or not request.form['grade']:
			flash('Check both fields and try again', 'error')
		else:
			student = students(name=request.form['name'], grade=request.form['grade'])
			db.session.add(student)
			db.session.commit()

			return redirect(url_for('results', students=students.query.all()))
			
	return render_template('home.html')

@app.route('/results', methods=['GET', 'POST'])
def results():

	return render_template("results.html", students=students.query.all())

@app.route('/passed', methods=['GET', 'POST'])
def passed():

	return render_template("results.html", students=students.query.filter(students.grade>=85))

@app.route('/deleted', methods=['GET', 'POST'])
def deleteStudent():
	studentID = students(id=request.form['id'])
	deletedstudent = students.query.get(studentID)
	db.session.delete(deletedstudent)
	db.session.commit()

	return render_template("results.html", students=students.query.all())


if __name__ == '__main__':
	db.create_all()
	app.run(debug = True)