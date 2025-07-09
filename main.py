# Pseudo Code

# 1. Import required libraries (Flask, smtplib, dotenv, threading, etc.)

# 2. Load environment variables from .env file (for email credentials)

# 3. Define EmailSender class
#    - Initialize with sender email and password
#    - Create and send an email with subject, body, and optional attachment
#    - Send the email multiple times if 'repeat' is set

# 4. Define BrowserOpener class
#    - Check if Microsoft Edge is installed
#    - Open the app URL in Edge or default browser

# 5. Define AppController class
#    - Set up Flask app and upload folder
#    - Create route for '/' that:
#        a. Handles form submission
#        b. Validates input (recipient, subject, body)
#        c. Handles file upload
#        d. Sends email using EmailSender
#        e. Shows success or error messages
#    - Run the Flask app and open browser in a separate thread

# 6. In the main block:
#    - Create AppController instance
#    - Start the app with debugging enabled

from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
from email.message import EmailMessage
from dotenv import load_dotenv
import mimetypes
import smtplib
import threading
import webbrowser
import os

class EmailSender:
    def __init__(self, sender_email, sender_password):
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(self, recipient, subject, body, attachment_path=None, repeat=1):
        if not self.sender_email or not self.sender_password:
            raise ValueError("Missing sender credentials in .env file.")

        msg = EmailMessage()
        msg['From'] = self.sender_email
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.set_content(body)
        
        if attachment_path and os.path.isfile(attachment_path):
            mime_type, _ = mimetypes.guess_type(attachment_path)
            maintype, subtype = mime_type.split('/', 1) if mime_type else ('application', 'octet-stream')
            with open(attachment_path, 'rb') as file:
                msg.add_attachment(file.read(), maintype=maintype, subtype=subtype,
                                   filename=os.path.basename(attachment_path))

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(self.sender_email, self.sender_password)
            for i in range(repeat):
                smtp.send_message(msg)
                print(f"✅ Email {i + 1} sent to {recipient}")
                
class BrowserOpener:
    @staticmethod
    def open_browser():
        url = "http://127.0.0.1:5000"
        webbrowser.open(url)
        
class AppController:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'supersecretkey'
        self.upload_folder = 'uploads'
        self.app.config['UPLOAD_FOLDER'] = self.upload_folder

        self.email_sender = EmailSender(
            os.getenv("SENDER_EMAIL"),
            os.getenv("SENDER_APP_PASSWORD")
        )

        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/', methods=['GET', 'POST'])
        def index():
            if request.method == 'POST':
                recipient = request.form.get('recipient')
                subject = request.form.get('subject')
                body = request.form.get('body')
                repeat_raw = request.form.get('repeat', '1')

                # Validate required fields
                if not recipient or not subject or not body:
                    flash("❌ All fields (recipient, subject, and body) are required.", "error")
                    return redirect('/')

                # Parse repeat count
                try:
                    repeat = max(1, int(repeat_raw))
                except ValueError:
                    flash("❌ Repeat must be a number.", "error")
                    return redirect('/')

                # Handle file upload
                file = request.files.get('attachment')
                attachment_path = None
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    attachment_path = os.path.join(self.app.config['UPLOAD_FOLDER'], filename)
                    file.save(attachment_path)

                # Send email
                try:
                    self.email_sender.send_email(recipient, subject, body, attachment_path, repeat)
                    flash(f"✅ Email sent to {recipient} ({repeat} time(s))!", "success")
                except Exception as e:
                    flash(f"❌ Failed to send email: {e}", "error")

                return redirect('/')

            return render_template('index.html')

    def run(self):
        threading.Thread(target=BrowserOpener.open_browser).start()
        self.app.run(debug=True)


if __name__ == '__main__':
    controller = AppController()
    controller.run()