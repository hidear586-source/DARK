import base64
import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ضع بيانات بوت التيليجرام الخاص بك هنا
TELEGRAM_BOT_TOKEN = "8564924688:AAEhOZpBhJ5vHZa11VP6yhq76V-NYyXLFgk"
TELEGRAM_CHAT_ID = "1458736423"

@app.route('/send_feedback', methods=['POST'])
def send_feedback():
    try:
        # استقبال البيانات المرسلة من اللعبة
        base64_image = request.form.get('base64_image')
        caption = request.form.get('caption', '🏆 صورة فوز جديدة')

        if not base64_image:
            return jsonify({"status": false, "error": "No image provided"}), 400

        # تنظيف وتفكيك تشفير Base64 إلى صورة حقيقية
        # (استبدال الرموز المحفوظة للـ URL)
        base64_image = base64_image.replace('%2B', '+').replace('%2F', '/').replace('%3D', '=')
        
        image_data = base64.b64decode(base64_image)
        image_path = "temp_win.jpg"
        
        with open(image_path, "wb") as f:
            f.write(image_data)

        # إرسال الصورة إلى بوت تيليجرام
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        with open(image_path, "rb") as img_file:
            files = {'photo': img_file}
            data = {
                'chat_id': TELEGRAM_CHAT_ID,
                'caption': caption,
                'parse_mode': 'HTML'
            }
            response = requests.post(url, data=data, files=files)

        # حذف الصورة المؤقتة من السيرفر
        if os.path.exists(image_path):
            os.remove(image_path)

        if response.status_code == 200:
            return jsonify({"status": True, "message": "Sent to Telegram successfully"})
        else:
            return jsonify({"status": False, "error": response.text}), 500

    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
