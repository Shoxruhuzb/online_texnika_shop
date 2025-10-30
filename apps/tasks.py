from celery import shared_task
from django.core.mail import send_mail

# from root.settings import EMAIL_HOST_USER

# @shared_task
# def send_email(email: str):
#     subject = 'Registration confirmation'
#     contex = {
#         'app_name': 'P33 Group',
#         'verification_url': 'https://localhost:8000/'
#     }
#     msg = "Bu xabar saytga ro'yxatdan o'tishni tasdiqlash uchun jo'natildi"
#     send_mail(subject, msg, EMAIL_HOST_USER, [email])

