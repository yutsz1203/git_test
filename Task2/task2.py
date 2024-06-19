from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/api/message', methods=['GET'])
def get_tasks():
    return jsonify({"message": "Hello, World!"})


if __name__ == '__main__':
    app.run(debug=True)