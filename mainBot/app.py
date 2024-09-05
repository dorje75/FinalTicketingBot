from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Set your Rasa server URL and authentication token
RASA_URL = 'http://localhost:5005/webhooks/rest/webhook'
AUTH_TOKEN = 'autoMates'


@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['message']

    headers = {'Authorization': f'Bearer {AUTH_TOKEN}'}
    response = requests.post(RASA_URL, json={'message': user_message}, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Error communicating with Rasa server'}), 500


if __name__ == "__main__":
    app.run(debug=True, port=3000)
