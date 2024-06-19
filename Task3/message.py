from urllib.parse import quote_plus

from flask import Flask, json, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
password = quote_plus("myu@2024")
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://mervin:{password}@192.168.28.144/exe2024_mervin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Msg(db.Model):
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message_body = db.Column(db.Text, nullable=False)

    def __str__(self):
        return f'{self.message_id} {self.message_body}'


def message_serializer(message):
    return {
        'message': message.message_body
    }


@app.route('/api/message', methods=['GET'])
def get_message():
    message = Msg.query.order_by(Msg.message_id.desc()).first()
    return message_serializer(message)
                         


@app.route('/api/message', methods=['POST'])
# create
def create():
    request_data = json.loads(request.data)
    message = Msg(message_body=request_data['message'])

    with app.app_context():
        db.session.add(message)
        db.session.commit()

    return jsonify({'message': "Inserted new message"}), 200


@app.route('/api/message/<int:message_id>', methods=['PATCH'])
# update
def update(message_id):
    message = Msg.query.get(message_id)
    data = request.json
    message.message_body = data['message']

    db.session.commit()

    return jsonify({'message': f'Message {message_id} updated'}), 200

@app.route('/api/message/<int:message_id>', methods=['DELETE'])
def delete(message_id):
    Msg.query.filter(Msg.message_id == message_id).delete()
    db.session.commit()

    return jsonify({'message': f'Message {message_id} deleted'}), 200


if __name__ == '__main__':
    app.run(debug=True)