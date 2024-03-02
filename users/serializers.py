from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer.
    """

    password = serializers.CharField(max_length=128, write_only=True)
    password2 = serializers.CharField(max_length=128, write_only=True)

    # isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('uuid', 'username', "firstname", 'is_staff', 'referral',
                  'date_joined', 'password', 'password2')

        # def get_isAdmin(self, obj):
        #     return obj.is_staff

    def validate(self, data):
        # check pwd is valid and hash it before saving
        if data.get('password'):
            if data['password'] != data.get('password2'):
                raise serializers.ValidationError('Passwords must match')

            del data['password2']
            data['password'] = make_password(data['password'])

        return data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128)
