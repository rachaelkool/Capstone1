from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    '''Connect to database.'''
    db.app = app
    db.init_app(app)


class Teacher(db.Model):
    '''Teacher'''
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    assignments = db.relationship('Assignment', backref='teacher')

    @classmethod
    def register(cls, id, email, password, first_name, last_name):
        '''Register a teacher account.

        Hashes password and adds teacher to system.'''
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        teacher = cls(
            id=id,
            email=email,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name
        )

        db.session.add(teacher)
        return teacher

    @classmethod
    def authenticate(cls, email, password):
        '''Find teacher with `email` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.'''
        teacher = Teacher.query.filter_by(email=email).first()

        if teacher and bcrypt.check_password_hash(teacher.password, password):
            return teacher
        else:
            return False


class Student(db.Model):
    '''Student'''
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    grade = db.Column(db.Text, nullable=False)

    scores = db.relationship('StudentAssignment')

    @classmethod
    def register(cls, id, email, password, first_name, last_name, grade):
        '''Register a student account.

        Hashes password and adds student to system.'''
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        student = cls(
            id=id,
            email=email,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name,
            grade=grade
        )

        db.session.add(student)
        return student

    @classmethod
    def authenticate(cls, email, password):
        '''Find student with `email` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.'''
        student = Student.query.filter_by(email=email).first()

        if student and bcrypt.check_password_hash(student.password, password):
            return student
        else:
            return False


class Assignment(db.Model):
    '''Assignment made by teacher.'''
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    due_date = db.Column(db.Date, default=2022-12-31)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    
    scores = db.relationship('StudentAssignment')


class StudentAssignment(db.Model):
    '''Student scores and if they passed on assignments.'''
    __tablename__ = 'students_assignments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'))
    score = db.Column(db.Integer)
    passed = db.Column(db.Boolean)

    students = db.relationship('Student')
    assignments = db.relationship('Assignment')

    __table_args__ = (UniqueConstraint('student_id', 'assignment_id', name='student_assignment_uc'),)


















