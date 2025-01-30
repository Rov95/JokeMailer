import os
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import requests

load_dotenv()

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

TEMPLATE_PATH = 'index.html'

def get_joke():
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        if response.status_code == 200:
            joke = f"{response.json()['setup']} - {response.json()['punchline']}"
            return joke
        return "Couldn't fetch a joke!"
    except Exception as e:
        return f"Error fetching joke: {e}"
    
print(get_joke())

def send_email(subject, html_content):
    message = MIMEMultipart()
    message["From"] = EMAIL_ADDRESS
    message["To"] = RECIPIENT_EMAIL
    message["Subject"] = subject
    message.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, message.as_string())
        print("Email sent successfully!")

def load_html_template(joke):
    try:
        with open(TEMPLATE_PATH, "r") as file:
            html_content = file.read()
            return html_content.replace("<!-- JOKE_PLACEHOLDER -->", joke)
    except Exception as e:
        print(f"Error loading HTML template: {e}")
        return ""

def automate_emails():
    print("Starting email automation...")
    try:
        while True:
            joke = get_joke()
            subject = "Your Scheduled Joke"
            html_content = load_html_template(joke)
            send_email(subject, html_content)
            time.sleep(120)
    except KeyboardInterrupt:
        print("Email automation stopped.")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    automate_emails()