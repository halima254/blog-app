from flask_mail import Message
from flask import render_template
from . import Mail

import smtplib

def mail_message(subject,template,to,**kwargs):
    sender_email = 'hcheptoo0@gmail.com'
    email = Message(subject, sender=sender_email, recipients=[to])
    email.body= render_template(template + ".txt",**kwargs)
    email.html = render_template(template + ".html",**kwargs)
    email.send(email)
    