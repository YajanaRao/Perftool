from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world','updated':'true'}

api.add_resource(HelloWorld, '/')

def start_server():
    app.run(debug=True)

if __name__ == '__main__':
    start_server()
