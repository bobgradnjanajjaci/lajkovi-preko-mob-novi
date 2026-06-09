from flask import Flask, render_template_string, request
import requests
import random

app = Flask(__name__)

# --- KONFIGURACIJA ---
# Panel 1: Lajkovi
L_URL = "https://smmcoder.com/api/v2"
L_KEY = "d648018680a19c64fcecfc9718d9d5d4"
L_SID = 7904

# Panel 2: Replyevi
R_URL = "https://dnoxsmm.com/api/v2"
R_KEY = "8e1e447b6a8ba2189d0afcd04487c5b"
R_SID = 4575

# TVOJE LISTE
REPLIES_SET_1 = [
    "I saw that this book was removed a few time, and there are rumors that the author is part of some high tier people. It really revealed too much",
    "For me its scary how much power this book has. I felt like someone had reached into my head and exposed everything about how are we controlled and how to actually leave this cycle...",
    "This book will become top 1 for money strategies and mindset, I can guarantee that. I highly recommend it to everyone..",
    "If you’re trying to find his book, don’t buy it on Amazon. I made that mistake and it was some weird fake version. The real one isn’t even sold there",
    "Didnt he get banned from Facebook a while ago because he started getting too much attention? I remember people saying the government didnt like what he was talking about. This whole thing is honestly insane.",
    "Where can I find it? ",
    "Original version of book you can only get from their official site, Just search name or the author of the book and first site is real..",
    "Am I the only one who remembers people saying he got silenced after his work started spreading online? The whole story around him is genuinely weird",
    "The more I hear about this, the stranger it gets. I vaguely remember people saying he disappeared from the spotlight almost overnight",
    "I could be wrong, but didn't he suddenly vanish from social media after gaining a huge following? That always seemed suspicious to me...",
]

# Možeš ovdje dodati REPLIES_SET_2 ako želiš drugu listu

HTML = """
<!doctype html>
<html>
<body style="background:#0f172a; color:white; font-family:sans-serif; padding:20px;">
    <div style="max-width:600px; margin:auto; background:#1e293b; padding:20px; border-radius:12px;">
        <h2>🚀 Combo Sender</h2>
        <form method="post" action="/send">
            <input type="text" name="link" placeholder="TikTok link komentara" required style="width:100%; padding:10px; margin-bottom:10px; background:#020617; border:1px solid #334155; color:white;">
            <input type="number" name="likes" placeholder="Broj lajkova" required style="width:100%; padding:10px; margin-bottom:10px; background:#020617; border:1px solid #334155; color:white;">
            <button type="submit" style="width:100%; padding:12px; background:#6366f1; border:none; color:white; cursor:pointer; font-weight:bold;">POŠALJI SVE</button>
        </form>
        {% if log %}<pre style="margin-top:15px; font-size:12px; background:#020617; padding:10px; border-radius:8px;">{{log}}</pre>{% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML)

@app.route("/send", methods=["POST"])
def send():
    link = request.form.get("link")
    qty = request.form.get("likes")
    
    # Nasumično odaberi jedan komentar iz liste
    selected_reply = random.choice(REPLIES_SET_1)
    
    # 1. Šalji lajkove
    r1 = requests.post(L_URL, data={"key": L_KEY, "action": "add", "service": L_SID, "link": link, "quantity": qty})
    
    # 2. Šalji reply
    r2 = requests.post(R_URL, data={"key": R_KEY, "action": "add", "service": R_SID, "link": link, "comments": selected_reply})
    
    log = f"Likes Result: {r1.text}\nReply Sent: '{selected_reply}'\nReply Result: {r2.text}"
    return render_template_string(HTML, log=log)

if __name__ == "__main__":
    app.run(debug=True)
