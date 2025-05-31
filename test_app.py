
import unittest
import json
from app import app, db, Students

class StudentApiTestCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    #Here are positive test cases
    def test_create_student_success(self):
        response = self.app.post('/api/students', 
                                 json={'name': 'Alice', 'city': 'Wonderland', 'addr': '123 Fantasy Rd', 'pin': '11111'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Student created successfully', response.get_data(as_text=True))

    def test_get_all_students_empty(self):
        response = self.app.get('/api/students')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)

    def test_get_all_students_with_data(self):
        with app.app_context():
            student = Students('Bob', 'BuilderCity', '456 Work St', '22222')
            db.session.add(student)
            db.session.commit()

        response = self.app.get('/api/students')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Bob')

    def test_get_student_by_id_success(self):
        with app.app_context():
            student = Students('Charlie', 'Chocolate', '789 Sweet Ave', '33333')
            db.session.add(student)
            db.session.commit()
            sid = student.id

        response = self.app.get(f'/api/students/{sid}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Charlie')

    def test_update_student_success(self):
        with app.app_context():
            student = Students('Diana', 'Themyscira', '000 Amazon Ln', '44444')
            db.session.add(student)
            db.session.commit()
            sid = student.id

        response = self.app.put(f'/api/students/{sid}', json={'city': 'New City'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Student updated successfully', response.get_data(as_text=True))

        # Check if updated
        with app.app_context():
            updated_student = Students.query.get(sid)
            self.assertEqual(updated_student.city, 'New City')

    def test_delete_student_success(self):
        with app.app_context():
            student = Students('Eve', 'Garden', '123 Paradise', '55555')
            db.session.add(student)
            db.session.commit()
            sid = student.id

        response = self.app.delete(f'/api/students/{sid}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Student deleted successfully', response.get_data(as_text=True))

    # Here are negative test cases
    def test_create_student_missing_fields(self):
        response = self.app.post('/api/students', json={'city': 'NoNameCity'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid input', response.get_data(as_text=True))

    def test_get_student_by_id_not_found(self):
        response = self.app.get('/api/students/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Student not found', response.get_data(as_text=True))

    def test_update_student_not_found(self):
        response = self.app.put('/api/students/999', json={'city': 'Nowhere'})
        self.assertEqual(response.status_code, 404)
        self.assertIn('Student not found', response.get_data(as_text=True))

    def test_delete_student_not_found(self):
        response = self.app.delete('/api/students/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Student not found', response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
