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