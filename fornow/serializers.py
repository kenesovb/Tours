from rest_framework import serializers

from django.contrib.auth.models import User
from .models import *
from django.db.models import Avg


class UserSerializers(serializers.ModelSerializer):
    """ Serializer for User to show instead of id Username"""

    class Meta:
        model = User
        fields = ("username",)


class TourImageSerializer(serializers.ModelSerializer):
    """ Serializer for IMAGE of tour """

    file = serializers.ImageField(use_url=True)

    class Meta:
        model = TourImage
        fields = ('file',)



class RegionSerializer(serializers.ModelSerializer):
    """ Serializer for Regions """

    class Meta:
        model = Region
        fields = ("region_name",)


class CitySerializer(serializers.ModelSerializer):
    """ Serializer for Cities """

    city_region = RegionSerializer()

    class Meta:
        model = City
        fields = ("city_region", "city_name",)


class TypeOfTourSerializer(serializers.ModelSerializer):
    """ Serializer for types of tour """

    class Meta:
        model = TypeOfTour
        fields = ('type_of_tour_name',)


class TourReviewSerializer(serializers.ModelSerializer):
    """ Serializer for Regions """
    review_creator = UserSerializers()

    class Meta:
        model = TourReview
        fields = ('review_creator', 'review_title', 'review_text', 'review_created_data', 'review_rating')


class TourPageSerializers(serializers.ModelSerializer):
    """ Serializer for TourPage of Tour model """

    creator = UserSerializers()
    images = TourImageSerializer(many=True, read_only=True)
    city = CitySerializer()
    type_of_tour = TypeOfTourSerializer()
    reviews = TourReviewSerializer(many=True)
    average_review = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = ('creator', 'id', 'images', 'city', 'duration', 'title', 'reviews', 'text', 'type_of_tour', 'currency',
                  'age_requirements', 'price', 'average_review')

    def get_average_review(self, obj):
        av = TourReview.objects.filter(id=obj.id).aggregate(avg_rating=Avg('review_rating', output_field=models.IntegerField()))
        if av['avg_rating'] is None:
            return 0
        return av['avg_rating']

    # def create(self, validated_data):
    #     images_data = self.context.get('view').request.FILES
    #     tour = Tour.objects.create(title=validated_data.get('title'),
    #                                 creator=validated_data.get('user'),
    #                                 text=validated_data.get('text'),
    #                                 city=validated_data.get('city'),
    #                                 region=validated_data.get('region'),
    #                                 type_of_tour=validated_data.get('type_of_tour'),
    #                                 duration=validated_data.get('duration'))
    #     for image_data in images_data.values():
    #         TourImage.objects.create(tour=tour,file=image_data)

    #     return tour


class TravelAgentSerializer(serializers.ModelSerializer):
    """Travel Agent Serializer """
    travel_agent_location = CitySerializer()

    class Meta:
        model = ToursTravelAgent
        fields = ('travel_agent_name', 'travel_agent_location')


class TourSerializers(serializers.ModelSerializer):
    """ Serializer for Tour model """
    images = TourImageSerializer(many=True)
    creator = UserSerializers()
    travel_agent_id = TravelAgentSerializer()
    average_review = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = ('creator', 'id', 'title', 'text', 'duration', 'images', 'travel_agent_id', 'average_review')

    def get_my_absolute_url(self, obj):
        return obj.get_absolute_url()  # return the absolute url of the object

    def get_average_review(self, obj):
        av = TourReview.objects.filter(id=obj.id).aggregate(avg_rating=Avg('review_rating'))
        if av['avg_rating'] is None:
            return 0
        return av['avg_rating']


class BookingSerializers(serializers.ModelSerializer):
    """ Serializer for Booking to add booking into users page"""
    tour = TourPageSerializers()

    class Meta:
        model = Booking
        fields = ('id', 'booking_creator', 'booking_price', 'tour', 'booking_status')


class UserPageSerializers(serializers.ModelSerializer):
    """ Serializer for User to show instead of id Username"""
    bookings = BookingSerializers(many=True)

    class Meta:
        model = User
        fields = ('username', 'bookings')


class TourReviewsPostSerializers(serializers.ModelSerializer):
    """ Serializers to post comments """

    # comment_creator = UserSerializers()

    class Meta:
        model = TourReview
        fields = ('review_title', 'review_text', 'review_rating')


class BookingPostSerializers(serializers.ModelSerializer):
    """ Serializer for Booking to add booking into users page"""

    class Meta:
        model = Booking
        fields = ('booking_status',)