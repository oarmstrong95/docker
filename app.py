from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def hello_world():
    data = request.json
    name = data.get('name', 'World')
    return f'Thank you, {name}!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
