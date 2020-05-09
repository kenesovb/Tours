from rest_framework import serializers

from django.contrib.auth.models import User
from .models import *
from django.db.models import Avg


class UserSerializers(serializers.ModelSerializer):
    """ Serializer for User to show instead of id Username"""

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")


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


class HotelsImagesSerializers(serializers.ModelSerializer):
    """"""
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = HotelsImages
        fields = ('image',)


class TourReviewSerializer(serializers.ModelSerializer):
    """ Serializer for Regions """
    review_creator = UserSerializers()

    class Meta:
        model = TourReview
        fields = ('review_creator', 'review_title', 'review_text', 'review_created_data', 'review_rating')


class TourDetailsSerializers(serializers.ModelSerializer):
    """ Serializer for Tour details"""

    class Meta:
        model = TourDetails
        fields = ('id', 'tour_start_date', 'tour_end_date', 'tour_person_number', 'cur_person_number', )


class TravelAgentSerializer(serializers.ModelSerializer):
    """Travel Agent Serializer """
    travel_agent_location = CitySerializer()

    class Meta:
        model = ToursTravelAgent
        fields = ('travel_agent_name', 'travel_agent_location')


class HotelSerializers(serializers.ModelSerializer):
    """ Serializer for hotels model """
    hotel_images = HotelsImagesSerializers(many=True)

    class Meta:
        model = Hotels
        fields = ('id', 'hotel_name', 'hotel_stars', 'hotel_images')


class HotelPageSerializers(serializers.ModelSerializer):
    """Hotel pages ser"""
    hotel_images = HotelsImagesSerializers(many=True)
    hotel_city = CitySerializer()

    class Meta:
        model = Hotels
        fields = ('id', 'hotel_name', 'hotel_stars', 'hotel_description', 'hotel_city', 'hotel_images')


class TourPageSerializers(serializers.ModelSerializer):
    """ Serializer for TourPage of Tour model """

    creator = UserSerializers()
    images = TourImageSerializer(many=True, read_only=True)
    city = CitySerializer()
    type_of_tour = TypeOfTourSerializer(many=True)
    reviews = TourReviewSerializer(many=True)
    average_review = serializers.SerializerMethodField()
    tour_detail = TourDetailsSerializers(many=True)
    travel_agent_id = TravelAgentSerializer()
    hotel = HotelSerializers()

    class Meta:
        model = Tour
        fields = ('creator', 'id', 'title', 'text', 'images', 'city', 'duration',  'type_of_tour', 'currency',
                  'age_requirements', 'price', 'reviews', 'average_review', 'tour_detail', 'travel_agent_id', 'hotel',
                  'tour_rating')

    def get_average_review(self, obj):
        av = TourReview.objects.filter(id=obj.id).aggregate(avg_rating=Avg('review_rating', output_field=models.IntegerField()))
        if av['avg_rating'] is None:
            return 0
        return av['avg_rating']


class TourSerializers(serializers.ModelSerializer):
    """ Serializer for Tour model """
    images = TourImageSerializer(many=True)
    creator = UserSerializers()
    travel_agent_id = TravelAgentSerializer()
    average_review = serializers.SerializerMethodField()
    type_of_tour = TypeOfTourSerializer(many=True)

    class Meta:
        model = Tour
        fields = ('creator', 'id', 'title', 'text', 'duration', 'images', 'travel_agent_id', 'average_review', 'tour_rating', 'type_of_tour')

    def get_my_absolute_url(self, obj):
        return obj.get_absolute_url()  # return the absolute url of the object

    def get_average_review(self, obj):
        av = TourReview.objects.filter(id=obj.id).aggregate(avg_rating=Avg('review_rating'))
        if av['avg_rating'] is None:
            return 0
        return av['avg_rating']


class UserPageTourSerializers(serializers.ModelSerializer):
    creator = UserSerializers()
    images = TourImageSerializer(many=True, read_only=True)
    city = CitySerializer()
    type_of_tour = TypeOfTourSerializer(many=True)
    reviews = TourReviewSerializer(many=True)
    average_review = serializers.SerializerMethodField()
    travel_agent_id = TravelAgentSerializer()

    class Meta:
        model = Tour
        fields = ('creator', 'id', 'title', 'text', 'images', 'city', 'duration',  'type_of_tour', 'currency',
                  'age_requirements', 'price', 'reviews', 'average_review','travel_agent_id', 'tour_rating')

    def get_average_review(self, obj):
        av = TourReview.objects.filter(id=obj.id).aggregate(avg_rating=Avg('review_rating', output_field=models.IntegerField()))
        if av['avg_rating'] is None:
            return 0
        return av['avg_rating']


class UserPageTourDetailsSerializers(serializers.ModelSerializer):
    """"""

    tour = UserPageTourSerializers()

    class Meta:
        model = TourDetails
        fields = ('id', 'tour_start_date', 'tour_end_date', 'tour_person_number', 'cur_person_number', 'tour')


class BookingSerializers(serializers.ModelSerializer):
    """ Serializer for Booking to add booking into users page"""
    tour_detail = UserPageTourDetailsSerializers()

    class Meta:
        model = Booking
        fields = ('id', 'booking_creator', 'booking_price', 'tour_detail', 'booking_status', 'booking_number_of_persons')


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


class TourDetailsPostSerializers(serializers.ModelSerializer):
    """"""
    class Meta:
        model = TourDetails
        fields = ('cur_person_number',)

