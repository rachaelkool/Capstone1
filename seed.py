"""Seed database with sample data."""

from app import app
from models import db, Student, Assignment, Teacher, StudentAssignment


db.drop_all()
db.create_all()

t1 = Teacher(id=101, email="teacher@schoolemail.com", password="$2b$12$N8NwfZuxeemu0iJ.1vnYMeiEicrnJjVDnoOESo7sUCzfKs925IwdS", first_name="Bob", last_name="Smith")
db.session.add(t1)
db.session.commit()

s1 = Student(id=1001, email="student1001@schoolemail.com", password="$2b$12$N8NwfZuxeemu0iJ.1vnYMeiEicrnJjVDnoOESo7sUCzfKs925IwdS", first_name="John", last_name="Jenkins", grade="10")
s2 = Student(id=1002, email="student1002@schoolemail.com", password="$2b$12$N8NwfZuxeemu0iJ.1vnYMeiEicrnJjVDnoOESo7sUCzfKs925IwdS", first_name="Barbara", last_name="Jones", grade="10")
db.session.add_all([s1, s2])
db.session.commit()

a1 = Assignment(name="Chemistry Quiz", due_date="2022-09-25", teacher_id=101)
a2 = Assignment(name="Molecules Questions", due_date="2022-09-23", teacher_id=101)
a3 = Assignment(name="Bonding Lab", due_date="2022-09-24", teacher_id=101)
a4 = Assignment(name="Atoms Quiz", due_date="2022-09-18", teacher_id=101)
db.session.add_all([a1, a2, a3, a4])
db.session.commit()

sa1 = StudentAssignment(student_id=1001, assignment_id=1, score=22, passed=False)
sa3 = StudentAssignment(student_id=1002, assignment_id=1, score=56, passed=False)
sa2 = StudentAssignment(student_id=1001, assignment_id=2)
sa4 = StudentAssignment(student_id=1002, assignment_id=2, score=71, passed=True)
sa5 = StudentAssignment(student_id=1001, assignment_id=3, score=78, passed=True)
sa6 = StudentAssignment(student_id=1002, assignment_id=3, score=98, passed=True)
sa7 = StudentAssignment(student_id=1001, assignment_id=4, score=38, passed=False)
sa8 = StudentAssignment(student_id=1002, assignment_id=4)

db.session.add_all([sa1, sa2, sa3, sa4, sa5, sa6, sa7, sa8])
db.session.commit()
