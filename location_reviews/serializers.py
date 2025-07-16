from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Location, LocationCategories, Review, Address
from django.contrib.auth.models import User

class LocationCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationCategories
        fields = "__all__"

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location.address.field.related_model
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(),
        required=False,
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment', 'likes', 'dislikes', 'location', 'user']

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['location', 'user'],
                message="User can leave only one review per location."
            )
        ]

    def create(self, validated_data):
        review = super().create(validated_data)
        location = review.location
        location.rating = location.average_rating
        location.save()
        return review

    def update(self, instance, validated_data):
        review = super().update(instance, validated_data)
        location = review.location
        location.rating = location.average_rating
        location.save()
        return review

class LocationSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=True)
    reviews = ReviewSerializer(many=True, read_only=True, source='review_set')
    categories = serializers.PrimaryKeyRelatedField(
        queryset=LocationCategories.objects.all(),
        many=True,
    )
    average_rating = serializers.ReadOnlyField()
    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(),
        required=False,
        read_only=True,
    )

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address, created = Address.objects.get_or_create(**address_data)
        categories_data = validated_data.pop('categories')
        location = Location.objects.create(address=address, **validated_data)
        location.categories.set(categories_data)
        location.save()
        return location

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        categories_data = validated_data.pop('categories', None)
        if address_data:
            other_locations = Location.objects.filter(address=instance.address).exclude(pk=instance.pk)
            address_changed = any(
                getattr(instance.address, attr) != value for attr, value in address_data.items()
            )
            if other_locations.exists() and address_changed:
                existing_address = Address.objects.filter(**address_data).first()
                if existing_address:
                    instance.address = existing_address
                else:
                    address_serializer = AddressSerializer(data=address_data)
                    address_serializer.is_valid(raise_exception=True)
                    new_address = address_serializer.save()
                    instance.address = new_address
            else:
                address_serializer = AddressSerializer(instance.address, data=address_data, partial=True)
                address_serializer.is_valid(raise_exception=True)
                address_serializer.save()
        if categories_data:
            instance.categories.set(categories_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = Location
        fields = [
            'id', 'name', 'description', 'address', 'categories', 'average_rating', 'reviews', 'user',
        ]