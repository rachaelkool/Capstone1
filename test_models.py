"""Models tests."""

# run these tests like:
#
# FLASK_ENV=production python -m unittest test_models.py

import os
from unittest import TestCase
from models import db, connect_db, Student, Teacher, Assignment, StudentAssignment

os.environ['DATABASE_URL'] = "postgresql:///gradebook_db_test"

from app import app

db.create_all()
app.config['WTF_CSRF_ENABLED'] = False


class StudentModelTestCase(TestCase):
    '''Tests for student model.'''
    def setUp(self):
        '''Create test client, add sample data.'''
        db.drop_all()
        db.create_all()
        
        self.client = app.test_client()

        student1 = Student.register(id=3000, email='testemail1@gmail.com', password='password', first_name='John', last_name='Smith', grade=9)
        student2 = Student.register(id=4000, email='testemail2@gmail.com', password='password', first_name='Jane', last_name='Johnson', grade=11)

        db.session.commit()

        student1 = Student.query.get(student1.id)
        student2 = Student.query.get(student2.id)


        self.student1 = student1
        self.student1.id = student1.id

        self.student2 = student2
        self.student2.id = student2.id

        db.session.commit()


    def tearDown(self):
        '''Run after each test.'''
        res = super().tearDown()
        db.session.rollback()
        return res


    def test_student_model(self):
        '''Tests if basic student model works.'''
        student = Student(
            id=5050,
            email="test@test.com",
            password="HASHED_PASSWORD",
            first_name="James",
            last_name="Johnson",
            grade=10
        )

        db.session.add(student)
        db.session.commit()

        self.assertEqual(student.id, 5050)


    def test_student_authentication(self):
        '''Tests student login.'''
        student = Student.authenticate(self.student1.email, 'password')
        self.assertEqual(student.id, self.student1.id)


    def test_invalid_student_email(self):
        '''Tests invalid student email when logging in.'''
        self.assertFalse(Student.authenticate('bademail', 'password'))


    def test_invalid_student_password(self):
        '''Tests invalid student password when logging in.'''
        self.assertFalse(Student.authenticate(self.student1.email, 'dumbpassword'))


class TeacherModelTestCase(TestCase):
    '''Tests for student model.'''
    def setUp(self):
        '''Create test client, add sample data.'''
        db.drop_all()
        db.create_all()
        
        self.client = app.test_client()

        teacher1 = Teacher.register(id=5000, email='testemail@gmail.com', password='password', first_name='John', last_name='Smith')

        db.session.commit()

        teacher1 = Teacher.query.get(teacher1.id)

        self.teacher1 = teacher1
        self.teacher1.id = teacher1.id

        db.session.commit()


    def tearDown(self):
        '''Run after each test.'''
        res = super().tearDown()
        db.session.rollback()
        return res


    def test_teacher_model(self):
        '''Tests if basic teacher model works.'''
        teacher= Teacher(
            id=5051,
            email="test@test.com",
            password="HASHED_PASSWORD",
            first_name="James",
            last_name="Johnson"
        )

        db.session.add(teacher)
        db.session.commit()

        self.assertEqual(teacher.id, 5051)


    def test_teacher_authentication(self):
        '''Tests teacher login.'''
        teacher = Teacher.authenticate(self.teacher1.email, 'password')
        self.assertEqual(teacher.id, self.teacher1.id)


    def test_invalid_teacher_email(self):
        '''Tests invalid teacher email when logging in.'''
        self.assertFalse(Teacher.authenticate('bademail', 'password'))


    def test_invalid_teacher_password(self):
        '''Tests invalid teacher password when logging in.'''
        self.assertFalse(Teacher.authenticate(self.teacher1.email, 'dumbpassword'))


class AssignmentModelTestCase(TestCase):
    '''Tests for assignment model.'''
    def setUp(self):
        '''Create test client, add sample data.'''
        db.drop_all()
        db.create_all()
        
        self.client = app.test_client()

        teacher1 = Teacher.register(id=5000, email='testemail@gmail.com', password='password', first_name='John', last_name='Smith')

        db.session.commit()

        teacher1 = Teacher.query.get(teacher1.id)

        self.teacher1 = teacher1
        self.teacher1.id = teacher1.id

        db.session.commit()


    def tearDown(self):
        '''Run after each test.'''
        res = super().tearDown()
        db.session.rollback()
        return res


    def test_assignment_model(self):
        '''Tests if basic assignment model works.'''
        assignment = Assignment(id=2, 
        name='Test Assignment', 
        due_date='2022-09-25', 
        teacher_id=self.teacher1.id
        )

        db.session.add(assignment)
        db.session.commit()

        self.assertEqual(assignment.name, 'Test Assignment')


class StudentAssignmentModelTestCase(TestCase):
    '''Tests for student assignment model.'''
    def setUp(self):
        '''Create test client, add sample data.'''
        db.drop_all()
        db.create_all()
        
        self.client = app.test_client()

        teacher1 = Teacher.register(id=5000, email='testemail@gmail.com', password='password', first_name='John', last_name='Smith')
        student1 = Student.register(id=3000, email='testemail1@gmail.com', password='password', first_name='John', last_name='Smith', grade=9)

        db.session.commit()

        teacher1 = Teacher.query.get(teacher1.id)
        student1 = Student.query.get(student1.id)


        self.teacher1 = teacher1
        self.teacher1.id = teacher1.id

        self.student1 = student1
        self.student1.id = student1.id

        db.session.commit()


    def tearDown(self):        
        '''Run after each test.'''
        res = super().tearDown()
        db.session.rollback()
        return res


    def test_student_assignment_model(self):
        '''Tests if basic student assignment model works.'''
        assignment = Assignment(id=2, 
        name='Test Assignment', 
        due_date='2022-09-25', 
        teacher_id=self.teacher1.id
        )

        db.session.add(assignment)
        db.session.commit()

        student_assignment = StudentAssignment(id=2, 
        student_id=self.student1.id,
        assignment_id=assignment.id,
        score=88,
        passed=True
        )

        db.session.add(student_assignment)
        db.session.commit()

        self.assertEqual(student_assignment.score, 88)





