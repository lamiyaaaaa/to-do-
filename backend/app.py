from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import csv
import os

app = Flask(__name__, static_folder='../frontend/static', static_url_path='/static')
CORS(app)

TASKS_FILE = 'tasks.csv'

def read_tasks():
    tasks = []
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                tasks.append(row)
    return tasks

def write_tasks(tasks):
    with open(TASKS_FILE, mode='w', newline='') as file:
        fieldnames = ['id', 'task']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for task in tasks:
            writer.writerow(task)

@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(read_tasks())

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    tasks = read_tasks()
    new_id = str(len(tasks) + 1)
    task = {'id': new_id, 'task': data['task']}
    tasks.append(task)
    write_tasks(tasks)
    return jsonify(task), 201

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = read_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    write_tasks(tasks)
    return jsonify({'message': 'Task deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
