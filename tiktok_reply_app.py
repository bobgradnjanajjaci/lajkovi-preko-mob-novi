from flask import Flask, render_template_string, request
import requests
from urllib.parse import urlparse

app = Flask(__name__)

# ================= CONFIGURACIJA =================
# PANEL 1: LIKES
LIKES_PANEL_URL = "https://smmcoder.com/api/v2"
LIKES_API_KEY = "d648018680a19c64fcecfc9718d9d5d4"
LIKES_SERVICE_ID = 7904

# PANEL 2: REPLIES
REPLIES_PANEL_URL = "https://dnoxsmm.com/api/v2"
REPLIES_API_KEY = "8e1e447b6a8ba2189d0afcd04487c5b"
REPLIES_SERVICE_ID = 4575

REPLIES_SET_1 = ["I saw that this book was removed a few time, and there are rumors that the author is part of some high tier people. It really revealed too much",
"For me its scary how much power this book has. I felt like someone had reached into my head and exposed everything about how are we controlled and how to actually leave this cycle...",
"‎This book will become top 1 for money strategies and mindset, I can guarantee that. I highly recommend it to everyone..",
"‎If you’re trying to find his book, don’t buy it on Amazon. I made that mistake and it was some weird fake version. The real one isn’t even sold there",
"Didnt he get banned from Facebook a while ago because he started getting too much attention? I remember people saying the government didnt like what he was talking about. This whole thing is honestly insane.",
"Where can I find it?",
"Original version of book you can only get from their official site, Just search name or the author of the book and first site is real..",
"Am I the only one who remembers people saying he got silenced after his work started spreading online? The whole story around him is genuinely weird",
"The more I hear about this, the stranger it gets. I vaguely remember people saying he disappeared from the spotlight almost overnight",
"I could be wrong, but didn't he suddenly vanish from social media after gaining a huge following? That always seemed suspicious to me..."]
REPLIES_SET_2 = ["Changed my life", "Chapter 4 is gold", "Claiming this energy"]

# ================= HTML TEMPLATE =================
HTML = """
<!doctype html>
<html>
<head>
    <style>
        body { background: #0f172a; color: white; font-family: sans-serif; padding: 20px; }
        .card { background: #1e293b; padding: 20px; border-radius: 12px; margin-bottom: 20px; }
        textarea { width: 100%; height: 100px; background: #0f172a; color: #86efac; border: 1px solid #334155; padding: 10px; }
        button { padding: 10px 20px; background: #6366f1; border: none; color: white; cursor: pointer; border-radius: 6px; margin-top: 10px; }
        .log { background: #020617; padding: 10px; margin-top: 10px; font-size: 12px; white-space: pre-wrap; border-left: 4px solid #6366f1; }
    </style>
</head>
<body>
    <h1>TikTok Control Panel</h1>
    
    <div class="card">
        <h2>1. Slanje Lajkova (Link kolicina)</h2>
        <form method="post" action="/send_likes">
            <textarea name="orders" placeholder="Link komentara 100"></textarea>
            <button type="submit">POŠALJI LAJKOVE</button>
        </form>
    </div>

    <div class="card">
        <h2>2. Slanje Replyeva</h2>
        <form method="post" action="/send_replies">
            <textarea name="links" placeholder="Link komentara"></textarea>
            <select name="set">
                <option value="1">Set 1</option>
                <option value="2">Set 2</option>
            </select><br>
            <button type="submit">POŠALJI REPLYEVE</button>
        </form>
    </div>

    {% if log %}<div class="log">{{log}}</div>{% endif %}
</body>
</html>
"""

# ================= LOGIKA =================

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML)

@app.route("/send_likes", methods=["POST"])
def send_likes():
    raw = request.form.get("orders", "")
    lines = [l.strip() for l in raw.splitlines() if l.strip()]
    logs = []
    for line in lines:
        parts = line.rsplit(maxsplit=1)
        if len(parts) == 2:
            link, qty = parts
            payload = {"key": LIKES_API_KEY, "action": "add", "service": LIKES_SERVICE_ID, "link": link, "quantity": qty}
            r = requests.post(LIKES_PANEL_URL, data=payload)
            logs.append(f"Likes: {link} -> {r.json()}")
    return render_template_string(HTML, log="\n".join(logs))

@app.route("/send_replies", methods=["POST"])
def send_replies():
    links = request.form.get("links", "").splitlines()
    set_id = request.form.get("set")
    comments = REPLIES_SET_1 if set_id == "1" else REPLIES_SET_2
    logs = []
    for link in links:
        payload = {"key": REPLIES_API_KEY, "action": "add", "service": REPLIES_SERVICE_ID, "link": link.strip(), "comments": "\n".join(comments)}
        r = requests.post(REPLIES_PANEL_URL, data=payload)
        logs.append(f"Reply: {link} -> {r.json()}")
    return render_template_string(HTML, log="\n".join(logs))

if __name__ == "__main__":
    app.run(debug=True)
