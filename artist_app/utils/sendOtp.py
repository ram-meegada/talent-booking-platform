from multiprocessing import context
import random
import base64
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from  artist_project.settings import *
from rest_framework_simplejwt.tokens import RefreshToken
import threading
from threading import Thread


def send_otp_via_mail(email, first_name="There"):
    message = make_otp()
    name = first_name
    context = {
        "OTP":message,
        "Name":name,
    }
    temp = render_to_string('otp.html', context)
    msg = EmailMultiAlternatives("", temp, EMAIL_HOST_USER, [email])
    msg.content_subtype = 'html'
    msg.send()
    print('mail sent opt')
    return message

def send_password_via_mail(email, message, first_name = "User"):
    name = first_name
    context={
        "password":message,
        "Name":name,
    }
    temp = render_to_string("password.html",context)
    msg = EmailMultiAlternatives("" , temp  , EMAIL_HOST_USER,[email])
    msg.content_subtype = "html"
    msg.send()
    

def generate_password():
    password = generate_encoded_id()
    return password
def make_otp():
    # otp = "".join(str(random.randint(0,9))for _ in range(4))
    otp = "1234"
    return otp

def generate_encoded_id():
    encoded_id = base64.b64encode(str(random.randint(1000000, 9999999)).encode()).decode()
    return encoded_id

def generate_access_token(user_obj):
    try:
        token = RefreshToken.for_user(user_obj)
        return str(token.access_token)
    except Exception as error:
        return ""  


class Email(threading.Thread):
    def __init__(self, recipient_list, notification_title, notification_description):
        self.title = notification_title
        self.recipient_list = recipient_list
        self.description = notification_description
        threading.Thread.__init__(self)
    def run(self):
        context = {'description':self.description, 'title': self.title}
        temp = render_to_string('notification.html', context)
        msg = EmailMultiAlternatives(f"{self.title}", temp, DEFAULT_FROM_EMAIL, self.recipient_list)
        msg.content_subtype = 'html'
        msg.send()
        print('sent')
        return None
def send_notification_to_mail(recipient_list, title, message):
    Email(recipient_list, title, message).start()  