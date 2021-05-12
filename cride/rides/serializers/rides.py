"""Rides serializer"""

# Django Rest Frameword
from rest_framework import serializers

# Models
from cride.circles.models import Membership
from cride.rides.models import Ride
from cride.users.models import User
from cride.users.serializers import UserModelSerializer

# Utilities
from datetime import timedelta
from django.utils import timezone



class CreateRideSerializer(serializers.ModelSerializer):
    """Create ride serializer"""
    offered_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    available_seats = serializers.IntegerField(min_value=1, max_value=15)

    class Meta:
        model = Ride
        exclude = ('offered_in','passengers','rating','is_active')

    def validate_departure_date(self, data):
        """Verify date is not in the past."""
        min_date = timezone.now() + timedelta(minutes=10)
        if data < min_date:
            raise serializers.ValidationError(
                'Departure time must be at least pass the next 20 minutes window.'
            )
        return data

    def validate(self, data):
        """Validate.
        Verify that the person who offers the ride is member
        and also the same user making the request.
        """
        if self.context['request'].user != data['offered_by']:
            raise serializers.ValidationError('Rides offered on behalf of others are not allowed.')

        user = data['offered_by']
        circle = self.context['circle']
        try:
            membership = Membership.objects.get(
                user=user,
                circle=circle,
                is_active=True
            )
        except Membership.DoesNotExist:
            raise serializers.ValidationError('User is not an active member of the circle.')

        if data['arrival_date'] <= data['departure_date']:
            raise serializers.ValidationError('Departure date must happen after arrival date.')

        self.context['membership'] = membership
        return data

    def create(self, data):
        """Create ride and update stats."""
        circle = self.context['circle']
        ride = Ride.objects.create(**data, offered_in=circle)

        # Circle
        circle.rides_offered += 1
        circle.save()

        # Membership
        membership = self.context['membership']
        membership.rides_offered += 1
        membership.save()

        # Profile
        profile = data['offered_by'].profile
        profile.rides_offered += 1
        profile.save()

        return ride

class RideModelSerializer(serializers.ModelSerializer):

    offered_by = UserModelSerializer(read_only=True)
    offered_in = serializers.StringRelatedField()
    passengers = UserModelSerializer(read_only=True, many=True)

    class Meta:
        model = Ride
        fields = '__all__'
        read_only_fields = (
            'offered_by',
            'offered_in',
            'rating'
        )

    def update(self, instance, validated_data):
        """Allow updates only before departure date"""
        if instance.departure_date <= timezone.now():
            raise serializers.ValidationError('Ongoing rides cannot be modified')
        return super(RideModelSerializer, self).update(instance, validated_data)


class JoinRideSerializer(serializers.ModelSerializer):
    """Join ride serializer"""
    passenger = serializers.IntegerField()

    class Meta:
        """Meta class"""
        model = Ride
        fields = ('passenger',)

    def validate_passenger(self, data):
        """Verify passenger exists and is a circle member"""
        try:
            user = User.objects.get(pk=data)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid passenger')

        circle = self.context['circle']
        try:
            membership = Membership.objects.get(
                user=user,
                circle=circle,
                is_active=True
            )
        except Membership.DoesNotExist:
            raise serializers.ValidationError('User is not an active member of the circle.')

        self.context['user'] = user
        self.context['membership'] = membership

        return data

    def validate(self, data):
        """Verify rides allow new passenger"""
        offset = timezone.now() + timedelta(seconds=60)
        ride = self.context['ride']
        if ride.departure_date <= offset:
            raise serializers.ValidationError('You can\'t join in this ride ')

        if ride.available_seats < 1:
            raise serializers.ValidationError("Ride is already full!")

        if ride.passengers.filter(pk=self.context['user'].pk).exists():
            raise serializers.ValidationError("User is already in this ride")
        return data


    def update(self, instance, validated_data):
        """Add passenger to ride, and updaye stats."""
        ride = self.context['ride']
        user = self.context['user']
        # Ride
        ride.passengers.add(user)
        instance.available_seats -= 1
        instance.save()

        # Profile
        profile = user.profile
        profile.rides_taken +=1
        profile.save()

        # Membership
        membership = self.context['membership']
        membership.rides_taken +=1
        membership.save()

        #Circle
        circle = self.context['circle']
        circle.rides_taken += 1
        circle.save()
        return ride


class EndRideSerializer(serializers.ModelSerializer):
    """End ride serializers"""
    current_time = serializers.DateTimeField()

    class Meta:
        """Meta class"""

        model = Ride
        fields = ('is_active','current_time')

    def validate_current_time(self, data):
        """Verify ride have inded started"""
        ride = self.context['view'].get_object()
        if data <= ride.departure_date:
            raise serializers.ValidationError("Ride has not started yet")

        return data


