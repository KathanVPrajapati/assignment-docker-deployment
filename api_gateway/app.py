from flask import Flask, request, jsonify
import requests
import json
import random
import logging

app = Flask(__name__)

USER_SERVICE_V1 = 'http://localhost:5001'
USER_SERVICE_V2 = 'http://localhost:5002'
ORDER_SERVICE = 'http://localhost:5003'

def load_config():
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            return config.get('v1_percentage', 100)  # Default to 100% for v1 if not specified
    except FileNotFoundError:
        print("Config file not found. Using default v1_percentage = 100.")
        return 100

def decide_user_service():
    v1_percentage = load_config()
    if random.random() * 100 < v1_percentage:
        app.logger.debug("Routing to User Service v1")
        return USER_SERVICE_V1
    else:
        app.logger.debug("Routing to User Service v2")
        return USER_SERVICE_V2

@app.route('/user', methods=['POST', 'PUT'])
def user():
    # version = request.args.get('version', 'v1')  # default to 'v1'
    # user_service_url = USER_SERVICE_V1 if version == 'v1' else USER_SERVICE_V2
    # response = requests.request(request.method, f"{user_service_url}/user", json=request.json)
    # return jsonify(response.json()), response.status_code

    user_service_url = decide_user_service()
    app.logger.debug(f"Routing request to: {user_service_url}")
    response = requests.request(request.method, f"{user_service_url}/user", json=request.json)
    return jsonify(response.json()), response.status_code

@app.route('/order', methods=['GET', 'POST', 'PUT'])
def order():
    # response = requests.request(request.method, f"{ORDER_SERVICE}/order", json=request.json)
    # return jsonify(response.json()), response.status_code

    response = requests.request(request.method, f"{ORDER_SERVICE}/order", json=request.json)
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(port=5000)
