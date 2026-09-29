import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# --------------------------------------------------------------------
# DATABASE CONFIG
# By default this app uses SQLite (students.db) — zero setup needed.
#
# To use Render's PostgreSQL instead, just set an environment variable
# called DATABASE_URL to your Render Postgres "External/Internal
# Database URL". The app will automatically detect it and switch.
# --------------------------------------------------------------------
database_url = os.environ.get('DATABASE_URL', '')

if database_url:
    # Render (and most hosts) give URLs starting with postgres://
    # SQLAlchemy needs postgresql:// — fix it automatically.
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'students.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# --------------------------------------------------------------------
# MODEL
# --------------------------------------------------------------------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    dob = db.Column(db.String(20), nullable=False)          # stored as YYYY-MM-DD
    gender = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(300), nullable=False)
    course = db.Column(db.String(120), nullable=True)
    year = db.Column(db.String(20), nullable=False)          # study year (1st, 2nd, ...)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'dob': self.dob,
            'gender': self.gender,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'course': self.course,
            'year': self.year,
            'created_at': self.created_at.strftime('%d-%m-%Y %H:%M') if self.created_at else ''
        }


with app.app_context():
    db.create_all()


# --------------------------------------------------------------------
# ROUTES
# --------------------------------------------------------------------
@app.route('/')
def index():
    students = Student.query.order_by(Student.id.desc()).all()
    return render_template('index.html', students=students)


@app.route('/add', methods=['POST'])
def add_student():
    try:
        name = request.form.get('name', '').strip()
        age = request.form.get('age', '').strip()
        dob = request.form.get('dob', '').strip()
        gender = request.form.get('gender', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        course = request.form.get('course', '').strip()
        year = request.form.get('year', '').strip()

        if not name or not age or not dob or not address or not year:
            flash('Please fill all required fields.', 'error')
            return redirect(url_for('index'))

        student = Student(
            name=name,
            age=int(age),
            dob=dob,
            gender=gender,
            email=email,
            phone=phone,
            address=address,
            course=course,
            year=year
        )
        db.session.add(student)
        db.session.commit()
        flash(f'Student "{name}" registered successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error registering student: {str(e)}', 'error')

    return redirect(url_for('index'))


@app.route('/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash(f'Student "{student.name}" removed.', 'success')
    return redirect(url_for('index'))


@app.route('/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        try:
            student.name = request.form.get('name', '').strip()
            student.age = int(request.form.get('age', '').strip())
            student.dob = request.form.get('dob', '').strip()
            student.gender = request.form.get('gender', '').strip()
            student.email = request.form.get('email', '').strip()
            student.phone = request.form.get('phone', '').strip()
            student.address = request.form.get('address', '').strip()
            student.course = request.form.get('course', '').strip()
            student.year = request.form.get('year', '').strip()

            db.session.commit()
            flash(f'Student "{student.name}" updated successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating student: {str(e)}', 'error')

    return render_template('edit.html', student=student)


@app.route('/api/students')
def api_students():
    students = Student.query.order_by(Student.id.desc()).all()
    return jsonify([s.to_dict() for s in students])


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
