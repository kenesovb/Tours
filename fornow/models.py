from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# Create your models here.
#
# class CustomUser(AbstractUser):
#     email = models.EmailField(_('email_address'), unique=True)
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#
#     gender_choices = (
#         ('M', 'Man'), ('W', 'Woman')
#     )
#
#     date_of_birth = models.DateField(blank=True, null=True)
#     gender = models.CharField(max_length=5, choices=gender_choices)


class Region(models.Model):
    region_name = models.CharField(max_length=150, verbose_name='Regions of Kazakhstan')

    def __str__(self):
        return self.region_name

    class Meta:
        verbose_name = 'Regions of Kazakhstan'


class City(models.Model):
    city_region = models.ForeignKey(Region, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=100, verbose_name='City name')

    def __str__(self):
        return self.city_name

    class Meta:
        verbose_name = 'Cities of Kazakhstan'


class Hotels(models.Model):
    """ Hotel for tour if provide """

    hotel_stars_choices = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    )

    hotel_name = models.CharField(max_length=150, verbose_name='Hotel name')
    hotel_description = models.TextField(verbose_name='Hotel description')
    hotel_city = models.ForeignKey(City, on_delete=models.CASCADE)
    hotel_stars = models.CharField(max_length=10, choices=hotel_stars_choices)

    def __str__(self):
        return self.hotel_name


def content_image_name(instance, filename):
    """ Where to save Images"""

    return 'hotel_{0}/{1}'.format(instance.hotel.id, filename)


class HotelsImages(models.Model):
    """Hotel Images"""

    hotel = models.ForeignKey(Hotels,related_name='hotel_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=content_image_name, blank=True, null=False)


class ToursTravelAgent(models.Model):
    """ Tours Travel Agent which has made that tour """

    travel_agent_name = models.CharField(max_length=150, verbose_name='Travel agent name')
    travel_agent_location = models.ForeignKey(City, verbose_name='Travel agent location', on_delete=models.CASCADE)

    def __str__(self):
        return self.travel_agent_name


class TypeOfTour(models.Model):
    """Type of tour"""
    type_of_tour_name = models.CharField(max_length=150, verbose_name='What Type of tour')

    def __str__(self):
        return self.type_of_tour_name

    class Meta:
        verbose_name = 'Types of Tour'


class ProvidedServices(models.Model):
    """ Provided services for tour """

    service_name = models.CharField(max_length=150, verbose_name='Kind of services')

    def __str__(self):
        return self.service_name


class Tour(models.Model):
    """Tours model """
    duration_choices = (
        ('2 days', '2-3 days'),
        ('5 days', '5-6 days'),
        ('7 days', '7-9 days'),
        ('9 days', '9-12 days'),
        ('12 days', '12-24 days'),
    )

    age_choices = (
        ('12 years and older', '12'),
        ('16  years and older', '16'),
        ('18  years and older', '18'),
        ('21  years and older', '21'),
    )

    currency_choices = (
        ('tg', 'tenge'),
        ('$ USA', 'Dollars USA'),
        ('€', 'Euro'),
    )

    creator = models.ForeignKey(User, verbose_name='Tour creator', on_delete=models.CASCADE)
    created_date = models.DateTimeField('created time of Tour', auto_now_add=True)
    title = models.CharField(max_length=150, verbose_name='Tour title')
    text = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    tour_end_city = models.ForeignKey(City,related_name='city_end', on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    price = models.IntegerField()
    currency = models.CharField(max_length=50, choices=currency_choices)
    type_of_tour = models.ManyToManyField(TypeOfTour)
    provided_services = models.ManyToManyField(ProvidedServices)
    age_requirements = models.CharField(max_length=50, choices=age_choices)
    duration = models.CharField(max_length=50, choices=duration_choices)
    travel_agent_id = models.ForeignKey(ToursTravelAgent, related_name='booking_travel_agent', on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotels, related_name='hotel_id', on_delete=models.CASCADE, null=True)
    tour_rating = models.IntegerField()

    class Meta:
        verbose_name = 'Tour of the site'

    def __str__(self):
        return self.title


def content_file_name(instance, filename):
    """ Where to save Images"""

    return 'tour_{0}/{1}'.format(instance.tour.id, filename)


class TourImage(models.Model):
    """" Images for Tour """

    tour = models.ForeignKey(Tour, related_name='images', on_delete=models.CASCADE)
    file = models.ImageField(upload_to=content_file_name, blank=True, null=False)

    class Meta:
        verbose_name = 'Tours Images model'


class TourReview(models.Model):
    """ Tours review model """

    tour = models.ForeignKey(Tour, related_name='reviews', on_delete=models.CASCADE)
    review_creator = models.ForeignKey(User, related_name='review_creator', on_delete=models.CASCADE)
    review_text = models.TextField()
    review_title = models.CharField(max_length=100, verbose_name='review title')
    review_created_data = models.DateTimeField('Time of when review was added', auto_now_add=True)
    review_rating = models.IntegerField(verbose_name='Review Rating')


class TourDetails(models.Model):
    """ Tour details about ordering """

    tour = models.ForeignKey(Tour, related_name='tour_detail', verbose_name='Tour', on_delete=models.CASCADE)
    tour_start_date = models.DateField()
    tour_end_date = models.DateField()
    tour_person_number = models.IntegerField(verbose_name='Number of persons for one Tour')
    cur_person_number = models.IntegerField(verbose_name='Current Number of persons for one Tour', default=0, null=True)

    class Meta:
        verbose_name = "Tour Details"

    def __str__(self):
        return self.tour.title


class Booking(models.Model):
    """ Booking of tours """

    booking_choices = (
        ('Reserved', 'Reserved'),
        ('Waiting for payment', 'Waiting for payment'),
        ('Approved', 'Approved'),
    )

    booking_creator = models.ForeignKey(User, related_name='bookings', verbose_name='Booking user', on_delete=models.CASCADE)
    tour_detail = models.ForeignKey(TourDetails, related_name='booking_tour', on_delete=models.CASCADE)
    booking_price = models.IntegerField()
    booking_status = models.CharField(max_length=50, choices=booking_choices)
    booking_number_of_persons = models.IntegerField()
