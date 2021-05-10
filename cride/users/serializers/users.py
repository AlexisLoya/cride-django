"""Users serializers"""

# Django
from django.conf import settings
from django.contrib.auth import password_validation,authenticate
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# Django Rest Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator

# Models
from cride.users.models import User, Profile
from .profiles import ProfileModelSerializer

# Utilities
from datetime import timedelta
import jwt



class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""
    profile = ProfileModelSerializer(read_only=True)
    class Meta:
        """Meta class."""

        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'profile'
        )


class UserSignUpSerializer(serializers.Serializer):
    """user sign up serializaer
    Handle sign up data validation and user/profile creation
    """
    # email
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    # username
    username = serializers.CharField(
        min_length=2,
        max_length=20,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    # phone number
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed."
    )
    phone_number = serializers.CharField(validators=[phone_regex], max_length=17)

    # Password
    password = serializers.CharField(min_length=8)
    password_confirmation = serializers.CharField(min_length=8)

    # Names
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    def validate(self, attrs):
        """Verify passwords match"""
        password = attrs['password']
        password_confirmation = attrs['password_confirmation']
        if password != password_confirmation:
            raise serializers.ValidationError('passwords don\'t match')
        password_validation.validate_password(password)
        return attrs

    def create(self, validated_data):
        """Handle user and profile creation"""
        validated_data.pop('password_confirmation')
        user = User.objects.create_user(**validated_data, is_verified=False)
        profile = Profile.objects.create(user=user)
        profile.save()
        self.send_confimation_email(user)
        return validated_data


    def send_confimation_email(self, user):
        """Send account verification link to given user"""
        verification_token = self.gen_verification_token(user)
        subject = 'Welcome @{}! verify your accoutn yo start usign Comparte Ride'.format(user.username)
        from_email = 'Comparte Ride <noreply@comparteride.com>'
        to = user.email
        text_content = render_to_string(
            'emails/users/account_verification.html',
            {'token':verification_token,'user':user}
        )
        msg = EmailMultiAlternatives(subject, text_content, from_email,[to])
        msg.attach_alternative(text_content, "text/html")
        msg.send()


    def gen_verification_token(self, user):
        """Create a JWT token that the user can use to verify its accoutn"""
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            'exp': int(exp_date.timestamp()),
            'type': 'email_confirmation'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token.decode()

class UserLoginSerializer(serializers.Serializer):
    """User login serializer.
    Handle the login request data just if the accoutn is verified.
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)


    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_verified:
            raise serializers.ValidationError('Acccoutn isn\'t active yet')
        self.context['user'] = user
        return data

    def create(self, data):
        """Generate or retrieve new token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class AccountVerificationSerializer(serializers.Serializer):
    """Accoutn verification serilizer"""
    token = serializers.CharField()

    def validate_token(self, data):
        """verify token expiration"""
        try:
            payload = jwt.decode(data,settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token.')

        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token.')

        self.context['payload'] = payload
        return data


    def save(self):
        """update user's verified status"""
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()
