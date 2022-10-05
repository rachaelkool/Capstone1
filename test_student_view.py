"""Teacher views tests."""

# run these tests like:
#
# FLASK_ENV=production python -m unittest test_student_view.py

import os
from unittest import TestCase
from models import db, connect_db, Student, Assignment, StudentAssignment

os.environ['DATABASE_URL'] = "postgresql:///gradebook_db_test"

from app import app

db.create_all()
app.config['WTF_CSRF_ENABLED'] = False


class StudentViewTestCase(TestCase):
    """"""

    def setUp(self):
        """"""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        student1 = Student.register(id=3000, email='testemail1@gmail.com', password='password', first_name='John', last_name='Smith', grade=9)

        student2 = Student.register(id=4000, email='testemail2@gmail.com', password='password', first_name='Jane', last_name='Johnson', grade=11)

        db.session.commit()

        self.student1 = student1
        self.student1.id = student1.id

        self.student2 = student2
        self.student2.id = student2.id

        db.session.commit()


    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp


    def test_student_dashboard(self):
        self.setUp()
        test_assignment = Assignment(id=1, name='Test Assignment')
        db.session.add(test_assignment)
        db.session.commit()
        test_score = StudentAssignment(id=1, student_id=self.student2.id, assignment_id=1, score=22, passed=False)
        db.session.add(test_score)
        db.session.commit()

        with self.client as client:
            with client.session_transaction() as sess:
                sess['id'] = self.student2.id

            resp = client.get(f'/students/{self.student2.id}')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2 class="display-4">Assignments</h2>', str(resp.data))
            self.assertIn('22%', str(resp.data))
            self.assertIn('request another attempt', str(resp.data))


    def test_student_request(self):
            self.setUp()
            test_assignment = Assignment(id=1, name='Test Assignment')
            db.session.add(test_assignment)
            db.session.commit()
            test_score = StudentAssignment(id=3, student_id=self.student2.id, assignment_id=1, score=22, passed=False)
            db.session.add(test_score)
            db.session.commit()

            with self.client as client:
                with client.session_transaction() as sess:
                    sess['id'] = self.student2.id

                resp = client.get('/publish/attempt/3', follow_redirects=True)
                self.assertEqual(resp.status_code, 200)
                self.assertIn('Request sent.', str(resp.data))


    def test_logged_out_student(self):
        self.setUp()

        with self.client as client:

            resp = client.get(f'/students/{self.student2.id}', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Please login first!", str(resp.data))



    

