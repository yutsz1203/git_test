from urllib.parse import quote_plus

from flask import Flask, json, jsonify, request
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
password = quote_plus("myu@2024")
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://mervin:{password}@192.168.28.144/exe2024_mervin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_detail = db.Column(db.Text, nullable=False)

    def __str__(self):
        return f'{self.task_id} {self.task_detail}'


def todo_serializer(todo):
    return {
        'task_id': todo.task_id,
        'task_detail': todo.task_detail
    }


@app.route('/api/task', methods=['GET'])
@cross_origin()
def get_tasks():
    return jsonify([*map(todo_serializer,
                         Todo.query.order_by(Todo.task_id).all())])


@app.route('/api/task', methods=['POST'])
# create
def create_task():
    request_data = json.loads(request.data)
    todo = Todo(task_detail=request_data['task_detail'])

    with app.app_context():
        db.session.add(todo)
        db.session.commit()

    return jsonify({'task': "Inserted new task"}), 200


@app.route('/api/task/<int:task_id>', methods=['PATCH'])
# update
def update_task(task_id):
    todo = Todo.query.get(task_id)
    data = request.json
    todo.task_detail = data['task_detail']

    db.session.commit()

    return jsonify({'task': f'Task {task_id} updated'}), 200

@app.route('/api/task/<int:task_id>', methods=['DELETE'])
def delete(task_id):
    Todo.query.filter(Todo.task_id == task_id).delete()
    db.session.commit()

    return jsonify({'message': f'Task {task_id} deleted'}), 200


if __name__ == '__main__':
    app.run(debug=True)
