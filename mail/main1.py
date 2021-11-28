#working on the email sending module

import smtplib

sender = "weather.app.test.python@gmail.com"
receiver = "dragos.daniel199@gmail.com"   #account login info
password = "Zalman123"
subject = "Python email test" #email title
body = "Attention! Temperature or Humidity delta too big! New Temp & Humidity : "  #email subject

# header
message = f"""From: Weather {sender}
To: {receiver}
Subject: {subject}\n
{body}
"""

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

try:
    server.login(sender,password)
    print("Logged in...")
    server.sendmail(sender, receiver, message)
    print("Email has been sent!")
except smtplib.SMTPAuthenticationError:
    print("Unable to sign in")