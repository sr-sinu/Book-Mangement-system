'''Import required Models'''
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_confirmation_email(review_id: int):
    '''Sending email for aknowledgement of users'''
    
    #email login
    email_from = "starunofficial@gmail.com"
    email_password = "eugp oqno aecn pckg"
    email_to = "shinde.shrikant2609@gmail.com"
    
    #email setup
    subject = "Review Confirmation"
    body = f"Thank you for your review! Your review with ID {review_id} has been received"

    msg = MIMEMultipart()
    msg['From'] = email_from
    msg["To"] = email_to
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_from, email_password)
        server.sendmail(email_from, email_to, msg.as_string())
        server.quit()
        print(f"Email sent for review id: {review_id}")
    except Exception as e:                              #raising exception
        print(f"Error sending email: {e}")
