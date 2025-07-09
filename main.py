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