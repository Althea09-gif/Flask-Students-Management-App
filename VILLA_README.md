# Student Management System with REST API - Final Exam Project

This project is an enhanced version of a simple Flask-based student management system. It adds a RESTful API layer to the original web application, enabling full CRUD (Create, Read, Update, Delete) operations on student records via HTTP requests. The project also integrates Swagger UI for easy API documentation and interactive testing.

## Features

- Web-based student management with a UI for adding, viewing, updating, and deleting student records.
- REST API endpoints for full CRUD operations on students:
  - GET /api/students – Retrieve all students
  - GET /api/students/<id> – Retrieve a specific student by ID
  - POST /api/students – Create a new student
  - PUT /api/students/<id> – Update an existing student
  - DELETE /api/students/<id> – Delete a student
- Proper HTTP status codes and error handling
- Swagger UI documentation for interactive API testing

## Getting Started

### Clone the Project

This project is based on the original Flask student management system template by Qoslaye.  
You can find the original template here:  
https://github.com/Qoslaye/Flask-Students-Management-App.git

I cloned and extended this template by adding the REST API and Swagger UI features.

### Requirements

- Python 3.x  
- Flask  
- Flasgger (for Swagger UI)  
- SQLite (default for the project)

### Installation

1. Clone this repository:

   git clone https://github.com/Qoslaye/student-management-final.git  
   cd student-management-final

2. Install dependencies:

   pip install -r requirements.txt

3. Run the Flask application:

   python app.py

4. Open your browser and go to:

   http://127.0.0.1:5000

5. To view and test the API documentation, go to:

  http://127.0.0.1:5000/apidocs

## API Documentation

The API endpoints support full CRUD operations on the student records, accepting and returning JSON data.

You can interact with the API directly via Swagger UI at:  
http://127.0.0.1:5000/apidocs/

## Testing

Automated tests are included using Python's unittest framework to verify the correctness and robustness of the API endpoints.  
Run tests using:

python -m unittest test_app.py

## Author

Althea Lauren J. Villa  
2nd Year BSIT Student

## Youtube channel to watch [https://youtu.be/2TBCs9ufJmE?si=XdlhGsh-seQ9lwfb]

## Acknowledgements

- Original Flask student management system template by [Original Author]  
- Flask and Flasgger libraries for API development and documentation

## License

This project is for academic purposes only.
