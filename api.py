from flask import Flask, request, render_template, jsonify
import json
import os

app = Flask(__name__)
endpoints = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api', methods=['GET'])
def get_endpoints():
    return jsonify({'endpoints': list(endpoints.keys())})

@app.route('/api', methods=['POST'])
def add_endpoint():
    endpoint = request.form.get('endpoint')
    if endpoint:
        endpoints[endpoint] = {}
        create_data_file(endpoint)
        return {'message': 'Endpoint added successfully'}
    else:
        return {'message': 'Invalid request'}, 400

@app.route('/api/<endpoint>', methods=['GET'])
def get_data(endpoint):
    data = read_data_file(endpoint)
    if data:
        return jsonify(data)
    else:
        return {'message': 'Endpoint not found'}, 404

@app.route('/api/<endpoint>', methods=['POST'])
def add_data(endpoint):
    data = request.json
    if validate_data(endpoint, data):
        update_data_file(endpoint, data)
        return {'message': 'Data added successfully'}
    else:
        return {'message': 'Invalid data structure'}, 400

def create_data_file(endpoint):
    filename = endpoint + '.json'
    with open(filename, 'w') as file:
        json.dump([], file)

def read_data_file(endpoint):
    filename = endpoint + '.json'
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            return data
    else:
        return None

def update_data_file(endpoint, data):
    filename = endpoint + '.json'
    with open(filename, 'w') as file:
        json.dump(data, file)

def validate_data(endpoint, data):
    if endpoint in endpoints:
        structure = endpoints[endpoint]
        if len(structure) == 0:
            endpoints[endpoint] = determine_structure(data)
            return True
        else:
            return validate_structure(structure, data)
    else:
        return False

def determine_structure(data):
    structure = {}
    for key, value in data.items():
        structure[key] = type(value).__name__
    return structure

def validate_structure(structure, data):
    for key, value in structure.items():
        if key not in data or type(data[key]).__name__ != value:
            return False
    return True

if __name__ == '__main__':
    app.run()
