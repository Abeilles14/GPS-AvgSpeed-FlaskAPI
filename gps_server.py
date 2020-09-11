# server for GPS coordinates

from flask import Flask, request
from flask_jsonpify import jsonify

app = Flask(__name__)

# create route at http://127.0.0.1:5000/coordinates
@app.route('/coordinates')
def get_all():
    with open('missionwaypoints.txt','r') as file:
        coordinates = file.readlines()

    file.close()
    return jsonify(coordinates)

if __name__ == '__main__':
    app.run(debug=True, port='5000')
