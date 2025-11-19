# Create a Python task management web application using Flask
# Requirements:
# - Use Flask framework for the web server
# - Implement CRUD operations (Create, Read, Update, Delete) for tasks
# - Each task should have: id, title, description, status (pending/in-progress/completed), created_date, due_date
# - Use SQLite database with SQLAlchemy ORM for data persistence
# - Create RESTful API endpoints:
#   - GET /tasks - retrieve all tasks
#   - GET /tasks/<id> - retrieve a specific task
#   - POST /tasks - create a new task
#   - PUT /tasks/<id> - update a task
#   - DELETE /tasks/<id> - delete a task
# - Include basic error handling and input validation
# - Add HTML templates with Bootstrap for a simple UI
# - Implement task filtering by status
# - Add search functionality for tasks by title or description

from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    status = db.Column(db.String(50), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)

# Create the database tables
with app.app_context():
    db.create_all()

# Home page - display all tasks
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

# Get a specific task
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify(task.to_dict())

# Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    new_task = Task(
        title=data['title'],
        description=data.get('description', ''),
        status=data['status'],
        due_date=datetime.strptime(data['due_date'], '%Y-%m-%d') if 'due_date' in data else None
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

# Update a task
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.json
    task.title = data['title']
    task.description = data.get('description', task.description)
    task.status = data['status']
    task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d') if 'due_date' in data else task.due_date
    db.session.commit()
    return jsonify(task.to_dict())

# Delete a task
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return '', 204

# Error handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
