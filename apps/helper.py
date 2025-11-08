from datetime import timedelta

from django.conf import settings
from twilio.rest import Client
from django.utils import timezone
import random
from django.core.cache import cache
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
    def __init__(self, phone) -> None:
        self.phone = phone

    def send_otp_via_message(self):
        otp = str(random.randint(1000, 9999))
        print(f"[TEST MODE] OTP for {self.phone}: {otp}")
        cache.set(f"otp_{self.phone}", otp, timeout=60)
        return otp


def is_otp_valid(phone, entered_otp):
    saved_otp = cache.get(f"otp_{phone}")
    if not saved_otp:
        return False
    return saved_otp == entered_otp