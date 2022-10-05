"""Teacher views tests."""

# run these tests like:
#
# FLASK_ENV=production python -m unittest test_teacher_view.py

import os
from unittest import TestCase
from models import db, connect_db, Teacher, Assignment

os.environ['DATABASE_URL'] = "postgresql:///gradebook_db_test"

from app import app

db.create_all()
app.config['WTF_CSRF_ENABLED'] = False


class TeacherViewTestCase(TestCase):
    """."""

    def setUp(self):
        """"""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        teacher1 = Teacher.register(id=1, email='testemail1@gmail.com', password='password', first_name='John', last_name='Smith')

        teacher2 = Teacher.register(id=2, email='testemail2@gmail.com', password='password', first_name='Jane', last_name='Johnson')
        teacher2.id = 2      

        db.session.commit()

        self.teacher1 = teacher1
        self.teacher1.id = teacher1.id

        self.teacher2 = teacher2
        self.teacher2.id = teacher2.id

        db.session.commit()


    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp


    def test_teacher_dashboard(self):
        self.setUp()

        with self.client as client:
            with client.session_transaction() as sess:
                sess['id'] = self.teacher2.id

            resp = client.get(f'/teachers/{self.teacher2.id}')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2 class="display-4">Assignments</h2>', str(resp.data))

    def test_assignment_info(self):
        self.setUp()
        test_assignment = Assignment(id=1, name='Test Assignment', teacher_id=self.teacher1.id)
        db.session.add(test_assignment)
        db.session.commit()

        with self.client as client:
            with client.session_transaction() as sess:
                sess['id'] = test_assignment.id

            resp = client.get('assignments/1')

            self.assertIn('Test Assignment', str(resp.data))


    def test_logged_out_teacher(self):
        self.setUp()

        with self.client as client:

            resp = client.get(f'/teachers/{self.teacher2.id}', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Please login first!", str(resp.data))


    def test_add_assignment(self):
        """"""
        self.setUp()
        test_assignment = Assignment(id=1, name='Test Assignment', teacher_id=self.teacher1.id)
        db.session.add(test_assignment)
        db.session.commit()

        with self.client as client:

            with client.session_transaction() as sess:
                sess['teacher_id'] = self.teacher1.id

            resp = client.post("/assignments/add", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

            assignment = Assignment.query.get(1)
            self.assertIsNotNone(assignment)
            self.assertEqual(assignment.name, "Test Assignment")
            

    def test_delete_assignment(self):
        self.setUp()
        test_assignment = Assignment(id=1, name='Test Assignment', teacher_id=self.teacher1.id)
        db.session.add(test_assignment)
        db.session.commit()

        with self.client as client:
            with client.session_transaction() as sess:
                sess['teacher_id'] = self.teacher1.id

            resp = client.post('/assignments/1/delete', follow_redirects=True)
           
            self.assertEqual(resp.status_code, 200)

            test_assignment = Assignment.query.get(1)
            self.assertIsNone(test_assignment)


    def test_logged_out_add_assignment(self):
        self.setUp()

        with self.client as client:
            resp = client.post('/assignments/add', data={"name": "Assignment"}, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Please login first!", str(resp.data))


    def test_logged_out_delete_assignment(self):
        self.setUp()
        test_assignment = Assignment(id=1, name='Test Assignment', teacher_id=self.teacher1.id)
        db.session.add(test_assignment)
        db.session.commit()

        with self.client as client:
            resp = client.post('/assignments/1/delete', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Please login first!", str(resp.data))

            test_assignment = Assignment.query.get(1)
            self.assertIsNotNone(test_assignment)


    def wrong_user_add_assignment(self):
        self.setUp()
        with self.client as client:
            with client.session_transaction() as sess:
                sess['teacher_id'] = self.teacher1.id

            resp = client.post("/assignments/add", data={"name": "Assignment", "teacher_id": self.teacher2.id}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Please login first!", str(resp.data))


    def test_wrong_user_delete_assignment(self):
        self.setUp()
        test_assignment = Assignment(id=1, name='Test Assignment', teacher_id=self.teacher1.id)
        db.session.add(test_assignment)
        db.session.commit()

        with self.client as client:
            with client.session_transaction() as sess:
                sess['teacher_id'] = self.teacher2.id

            resp = client.post("/assignments/1/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
      
            assignment = Assignment.query.get(1)
            self.assertIsNotNone(assignment)
    

