from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib, os, requests
from email.message import EmailMessage
import os
app = Flask(__name__)
CORS(app)

EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")
RECAPTCHA_SECRET = os.getenv("RECAPTCHA_SECRET")

def home():
    return "Backend is running!"
    
def verify_recaptcha(token):
    url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {
        "secret": RECAPTCHA_SECRET,
        "response": token
    }
    r = requests.post(url, data=payload)
    return r.json().get("success", False)

def send_mail(msg):
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL, PASSWORD)
        smtp.send_message(msg)

@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.json

    # 🔐 Verify reCAPTCHA
    # if not verify_recaptcha(data.get("recaptchaToken")):
    #     return jsonify({"error": "Invalid reCAPTCHA"}), 400

    name = data["name"]
    email = data["email"]
    message = data["message"]

    # 1️⃣ Email to YOU (HTML)
    owner_msg = EmailMessage()
    owner_msg["Subject"] = f"📩 Portfolio Message from {name}"
    owner_msg["From"] = EMAIL
    owner_msg["To"] = EMAIL
    owner_msg.set_content("HTML not supported")
    owner_msg.add_alternative(f"""
    <html>
      <body style="font-family: Arial;">
        <h2>New Portfolio Message</h2>
        <p><b>Name:</b> {name}</p>
        <p><b>Email:</b> {email}</p>
        <p><b>Message:</b></p>
        <p>{message}</p>
      </body>
    </html>
    """, subtype="html")

    # 2️⃣ Auto-reply to CLIENT (HTML)
    reply_msg = EmailMessage()
    reply_msg["Subject"] = "Thanks for reaching out!"
    reply_msg["From"] = EMAIL
    reply_msg["To"] = email
    reply_msg.set_content("HTML not supported")
    reply_msg.add_alternative(f"""
    <html>
      <body style="font-family: Arial; background:#f5f5f5; padding:20px;">
        <div style="max-width:600px; background:white; padding:20px; border-radius:8px;">
          <h2 style="color:#333;">Hi {name},</h2>
          <p>Thanks for reaching out through my portfolio 🚀</p>
          <p>I’ve received your message and will get back to you soon.</p>
          <br/>
          <p>Best regards,</p>
          <p><b>Vishwa S</b><br/>Software Developer</p>
        </div>
      </body>
    </html>
    """, subtype="html")

    send_mail(owner_msg)
    send_mail(reply_msg)

    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
