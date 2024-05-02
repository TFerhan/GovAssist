from flask import Flask, request, jsonify
import threading, time
from flask_cors import CORS, cross_origin
from gradio_client import Client
import os
hf_token = os.environ.get('hf_token')
client = Client("tferhan/data_gov_ma", hf_token=hf_token)

#get hf token from env variables
hf_token = os.environ.get('hf_token')
app = Flask(__name__)

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def home():
    return 'Hello World!' 


@app.route('/api', methods=['POST'])
@cross_origin()
def api():
    message = request.json.get('message')
    if message is None:
        return jsonify({"error": "Message not found in request"}), 400

    result = client.predict(
        message,    
        api_name="/chat"
    ) 
    return jsonify(result)  


def keep_alive():
    while True:
        try:
            predict = client.predict(
                "Bonjour",
                api_name="/chat"
            )
            time.sleep(86400)
        except:
            pass


threading.Thread(target=keep_alive).start()


