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

class LocationSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=True)
    reviews = ReviewSerializer(many=True, read_only=True, source='review_set')
    categories = serializers.PrimaryKeyRelatedField(
        queryset=LocationCategories.objects.all(),
        many=True
    )
    average_rating = serializers.ReadOnlyField()

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        categories_data = validated_data.pop('categories')
        address = Address.objects.create(**address_data)
        location = Location.objects.create(address=address, **validated_data)
        location.categories.set(categories_data)
        location.save()
        return location

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        categories_data = validated_data.pop('categories', None)
        if address_data:
            for attr, value in address_data.items():
                setattr(instance.address, attr, value)
            instance.address.save()
        if categories_data:
            instance.categories.set(categories_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.rating = instance.average_rating
        instance.save()
        return instance

    class Meta:
        model = Location
        fields = [
            'id', 'name', 'description', 'address', 'categories', 'average_rating', 'reviews'
        ]