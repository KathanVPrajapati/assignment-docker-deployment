from flask import Flask, request, jsonify
from pymongo import MongoClient
from urllib.parse import quote_plus 

app = Flask(__name__)
username = quote_plus("kvp2001") 
password = quote_plus("Kathan@123")
client = MongoClient(f"mongodb+srv://{username}:{password}@mongoworkshop.mkqov.mongodb.net/Sample?retryWrites=true&w=majority", serverSelectionTimeoutMS=5000)

db = client['order_db']

@app.route('/order', methods=['POST'])
def create_order():
    data = request.json
    db.orders.insert_one(data)
    return jsonify({"msg": "Order created"}), 201

@app.route('/order', methods=['PUT'])
def update_order():
    data = request.json
    db.orders.update_one({'order_id': data['order_id']}, {"$set": {"status": data['status']}})
    return jsonify({"msg": "Order status updated"}), 200

@app.route('/order', methods=['GET'])
def get_orders():
    state = request.args.get('state')
    orders = list(db.orders.find({"status": state}))
    return jsonify(orders), 200

@app.route('/order/sync', methods=['PUT'])
def sync_order():
    data = request.json
    db.orders.update_many({'user_email': data['email']}, {"$set": {"user_email": data['email'], "delivery_address": data['delivery_address']}})
    return jsonify({"msg": "Orders synchronized"}), 200

if __name__ == '__main__':
    app.run(port=5003)
