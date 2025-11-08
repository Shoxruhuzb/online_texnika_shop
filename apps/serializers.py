import re
from rest_framework import serializers
from apps.models import User


class UserPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone',)

    def validate_phone(self, phone):
        digits = re.sub(r'\D', '', phone)

        if not digits.startswith('998'):
            raise serializers.ValidationError("Telefon raqam 998 bilan boshlanishi kerak.")

        if len(digits) != 12:
            raise serializers.ValidationError("Telefon raqam noto‘g‘ri uzunlikda kiritilgan.")

        return f"+{digits}"
