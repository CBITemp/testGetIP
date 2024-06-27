from flask import Flask, request
from flask import jsonify
import geocoder
from flask_cors import CORS
import requests




app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    # Get requester's IP address
    requester_ip = request.remote_addr

    # Use geocoder to get country based on IP address
    location = geocoder.ip(requester_ip)
    country = location.country if location else "Unknown"

    # Prepare response
    response = f"Requester IP: {requester_ip}<br>Country: {country}"

    return response

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    ip = request.access_route[-1]

    return jsonify({'ip': ip}), 200

@app.route("/test", methods=["GET"])
def test():
    # Define the API endpoint
    url = 'https://api.ipify.org/?format=json'

    # Send a GET request to the API
    response = requests.get(url)
    ip = response.json()

    return jsonify({'ip': ip}), 200
