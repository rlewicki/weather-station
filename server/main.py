from flask import Flask, request
from flask_restful import Resource, Api
import rsa
from base64 import b64decode

app = Flask(__name__)
api = Api(app)

todos = {}
private_key = None

class WeatherReading(Resource):
    def get(self):
        return "answer from the server to the get request"

    def put(self):
        data = request.form["data"]
        data = b64decode(data.encode("utf8"))
        message = rsa.decrypt(data, private_key).decode()
        print(message)
        return "received data"

api.add_resource(WeatherReading, "/reading/new")

if __name__ == '__main__':
    key_file = open("private.pem", "rb")
    key_data = key_file.read()
    key_file.close()
    private_key = rsa.PrivateKey.load_pkcs1(key_data)
    app.run(debug=True)
