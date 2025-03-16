import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_things3_todos(body):
    # Email configuration
    sender_email = "oyvind.auk@gmail.com"  # Replace with your Gmail address
    sender_password = "ibex aikv cfoi aoyf"   # Replace with your Gmail app password
    receiver_email = "oyvind.auk@gmail.com"

    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"Things3 todos - {datetime.now().strftime('%Y-%m-%d')}"

    # Email body
    example_body = """
    Hello Øyvind,

    Here is your daily todo list from Things 3.

    Have a productive day!

    Best regards,
    Your Todo Bot
    """
    
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Create server connection
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        # Login
        server.login(sender_email, sender_password)
        
        # Send email
        server.send_message(msg)
        print("Email sent successfully!")
        
    except Exception as e:
        print(f"Error sending email: {e}")
        
    finally:
        server.quit()

if __name__ == "__main__":
    send_things3_todos('asdf')
