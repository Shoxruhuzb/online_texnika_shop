from django.core.mail import send_mail

from root.settings import EMAIL_HOST_USER

def send_email(email: str):
    subject = 'Registration confirmation'
    msg = "Bu xabar saytga ro'yxatdan o'tishni tasdiqlash uchun jo'natildi"
    send_mail(subject, msg, EMAIL_HOST_USER, [email])

