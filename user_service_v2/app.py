from flask import Flask, request, jsonify
from pymongo import MongoClient
import json
import pika
from urllib.parse import quote_plus 

app = Flask(__name__)
username = quote_plus("kvp2001") 
password = quote_plus("Kathan@123")
client = MongoClient(f"mongodb+srv://{username}:{password}@mongoworkshop.mkqov.mongodb.net/Sample?retryWrites=true&w=majority", serverSelectionTimeoutMS=5000)

db = client['user_db_v2'] 

# def send_event(data):
#     connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
#     channel = connection.channel()
#     channel.queue_declare(queue='sync_queue')
#     channel.basic_publish(exchange='', routing_key='sync_queue', body=str(data))
#     connection.close()

def send_event(data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='sync_queue')
    # Use json.dumps() instead of str(data) to ensure proper JSON formatting
    channel.basic_publish(exchange='', routing_key='sync_queue', body=json.dumps(data))
    connection.close()


@app.route('/user', methods=['POST', 'PUT'])
def manage_user():
    data = request.json
    if request.method == 'POST':
        db.users.insert_one(data)
        return jsonify({"msg": "User created in v2"}), 201
    elif request.method == 'PUT':
        db.users.update_one({'account_id': data['account_id']}, {"$set": data})
        send_event(data)  # Trigger event for sync
        return jsonify({"msg": "User updated in v2"}), 200

if __name__ == '__main__':
    app.run(port=5002)
