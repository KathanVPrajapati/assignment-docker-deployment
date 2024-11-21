import pika
import json
import requests

def callback(ch, method, properties, body):
    try:
        # Try to decode the JSON message
        data = json.loads(body)
        
        # Assuming the sync endpoint on the order service
        sync_url = 'http://localhost:5003/order/sync'
        requests.put(sync_url, json={'email': data['email'], 'address': data['delivery_address']})
        # Send the data to the order service for synchronization
        response = requests.put(sync_url, json=data)
        
        # Log the successful synchronization
        print(f"Synchronized order data with updated user info: {data}")
    
    except json.JSONDecodeError as e:
        # Handle JSON decoding error
        print(f"Error decoding JSON: {e}")
        print(f"Received message: {body}")
    
    except requests.exceptions.RequestException as e:
        # Handle request errors
        print(f"Error sending request to order service: {e}")
    
    except Exception as e:
        # General exception handling
        print(f"An unexpected error occurred: {e}")

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))

channel = connection.channel()
channel.queue_declare(queue='sync_queue')
channel.basic_consume(queue='sync_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()
