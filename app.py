from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, swag_from  # I added Swagger for API docs

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"
app.config['SWAGGER'] = {
    'title': 'Students Management API',
    'uiversion': 3
}
db = SQLAlchemy(app)
swagger = Swagger(app) #I added Swagger instance

class Students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))

    def __init__(self, name, city, addr, pin):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin

# WEB ROUTES
@app.route('/')
def show_all():
    return render_template('show_all.html', students=Students.query.all())

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            student = Students(
                request.form['name'],
                request.form['city'],
                request.form['addr'],
                request.form['pin']
            )
            db.session.add(student)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new.html')

# # I add REST API ROUTES below

@app.route('/api/students', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'List of all students',
            'examples': {
                'application/json': [
                    {'id': 1, 'name': 'Althea', 'city': 'Puerto', 'addr': 'Palumco Street', 'pin': '12345'}
                ]
            }
        }
    }
})
def get_students():
    students = Students.query.all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'city': s.city,
        'addr': s.addr,
        'pin': s.pin
    } for s in students]), 200

@app.route('/api/students/<int:id>', methods=['GET'])
@swag_from({
    'parameters': [{'name': 'id', 'in': 'path', 'type': 'integer', 'required': True}],
    'responses': {
        200: {'description': 'Student data found'},
        404: {'description': 'Student not found'}
    }
})
def get_student(id):
    student = db.session.get(Students, id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify({
        'id': student.id,
        'name': student.name,
        'city': student.city,
        'addr': student.addr,
        'pin': student.pin
    }), 200

@app.route('/api/students', methods=['POST'])
@swag_from({
    'parameters': [{
        'name': 'student',
        'in': 'body',
        'schema': {
            'type': 'object',
            'properties': {
                'name': {'type': 'string'},
                'city': {'type': 'string'},
                'addr': {'type': 'string'},
                'pin': {'type': 'string'}
            },
            'required': ['name', 'city', 'addr']
        }
    }],
    'responses': {
        201: {'description': 'Student created successfully'},
        400: {'description': 'Invalid input'}
    }
})
def create_student():
    data = request.get_json()
    if not data or not all(k in data for k in ('name', 'city', 'addr')):
        return jsonify({'error': 'Invalid input'}), 400

    new_student = Students(data['name'], data['city'], data['addr'], data.get('pin', ''))
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'message': 'Student created successfully'}), 201

@app.route('/api/students/<int:id>', methods=['PUT'])
@swag_from({
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True},
        {'name': 'student', 'in': 'body', 'schema': {
            'type': 'object',
            'properties': {
                'name': {'type': 'string'},
                'city': {'type': 'string'},
                'addr': {'type': 'string'},
                'pin': {'type': 'string'}
            }
        }}
    ],
    'responses': {
        200: {'description': 'Student updated successfully'},
        404: {'description': 'Student not found'}
    }
})
def update_student(id):
    student = db.session.get(Students, id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    data = request.get_json()
    student.name = data.get('name', student.name)
    student.city = data.get('city', student.city)
    student.addr = data.get('addr', student.addr)
    student.pin = data.get('pin', student.pin)

    db.session.commit()
    return jsonify({'message': 'Student updated successfully'}), 200

@app.route('/api/students/<int:id>', methods=['DELETE'])
@swag_from({
    'parameters': [{'name': 'id', 'in': 'path', 'type': 'integer', 'required': True}],
    'responses': {
        200: {'description': 'Student deleted successfully'},
        404: {'description': 'Student not found'}
    }
})
def delete_student(id):
    student = db.session.get(Students, id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted successfully'}), 200

# I added swagger UI location: http://127.0.0.1:5000/apidocs

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



