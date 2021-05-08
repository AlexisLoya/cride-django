"""Users serializers"""

# Django
from django.contrib.auth import password_validation,authenticate

# Django Rest Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator

# Models
from cride.users.models import User, Profile

class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    class Meta:
        """Meta class."""

        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number'
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
    # password
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
        """Verify passeords match"""
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
        return validated_data

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
