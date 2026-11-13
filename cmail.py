import os
import smtplib
from email.message import EmailMessage

def sendmail(to,subject,body):
    server=smtplib.SMTP_SSL(os.environ['SMTP_HOST'],int(os.environ['SMTP_PORT']))
    server.login(os.environ['SMTP_USERNAME'],os.environ['SMTP_PASSWORD'])
    msg=EmailMessage()
    msg['FrOM']=os.environ['MAIL_FROM']
    msg['SUBJECT']=subject
    msg['TO']=to
    msg.set_content(body)
    server.send_message(msg)
    server.close()