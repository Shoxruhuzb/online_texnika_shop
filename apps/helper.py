from datetime import timedelta

from django.conf import settings
from twilio.rest import Client
from django.utils import timezone

#
# class MessageHandler:
#     def __init__(self, phone, otp):
#         self.phone = phone
#         self.otp = otp
#
#     def send_otp_via_message(self):
#         client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
#         message = client.messages.create(
#             body=f'Your OTP is: {self.otp}',
#             from_=settings.TWILIO_PHONE_NUMBER,
#             to=f'{settings.COUNTRY_CODE}{self.phone}'
#         )
#         print(f"OTP for {self.phone} is {self.otp}")

class MessageHandler:
    def __init__(self, phone, otp, user) -> None:
        self.phone = phone
        self.otp = otp
        self.user = user

    def send_otp_via_message(self):
        print(f"[TEST MODE] OTP for {self.phone}: {self.otp}")

        self.user.otp = self.otp
        self.user.otp_created_at = timezone.now()
        self.user.save()

def is_otp_valid(user, entered_otp):
    if not user.otp or not user.otp_created_at:
        return False
    now = timezone.now()
    if now - user.otp_created_at > timedelta(minutes=1):
        return False
    if entered_otp != user.otp:
        return False
    return True