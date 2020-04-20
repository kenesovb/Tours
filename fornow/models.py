from django.db import models
from django.contrib.auth.models import User


# Create your models here.

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


class ToursTravelAgent(models.Model):
    """ Tours Travel Agent which has made that tour """

    travel_agent_name = models.CharField(max_length=150, verbose_name='Travel agent name')
    travel_agent_location = models.ForeignKey(City, verbose_name='Travel agent location', on_delete=models.CASCADE)


class TypeOfTour(models.Model):
    type_of_tour_name = models.CharField(max_length=150, verbose_name='What Type of tour')

    def __str__(self):
        return self.type_of_tour_name

    class Meta:
        verbose_name = 'Types of Tour'


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

    creater = models.ForeignKey(User, verbose_name='Tour creater', on_delete=models.CASCADE)
    created_date = models.DateTimeField('created time of Tour', auto_now_add=True)
    title = models.CharField(max_length=150, verbose_name='Tour title')
    text = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    price = models.IntegerField()
    currency = models.CharField(max_length=50, choices=currency_choices)
    type_of_tour = models.ForeignKey(TypeOfTour, on_delete=models.CASCADE)
    age_requirements = models.CharField(max_length=50, choices=age_choices)
    duration = models.CharField(max_length=50, choices=duration_choices)
    travel_agent_id = models.ForeignKey(ToursTravelAgent, related_name='booking_travel_agent', on_delete=models.CASCADE)

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
    file = models.ImageField(upload_to=content_file_name)

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


class Booking(models.Model):
    """ Booking of tours """

    booking_choices = (
        ('Reserved', 'Reserved'),
        ('Waiting for payment', 'Waiting for payment'),
        ('Approved', 'Approved'),
    )

    booking_creator = models.ForeignKey(User, related_name='bookings', verbose_name='Booking user', on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, related_name='booking_tour', on_delete=models.CASCADE)
    booking_price = models.IntegerField()
    booking_status = models.CharField(max_length=50, choices=booking_choices)
