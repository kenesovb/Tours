from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings

from .models import Tour, Booking
from .serializers import (TourSerializers, TourPageSerializers, UserPageSerializers, TourReviewsPostSerializers, BookingPostSerializers, )


# Create your views here.

class TourView(APIView):
    """Tour"""
    permission_classes = [permissions.AllowAny,]

    def get(self, request):
        tours = Tour.objects.all()
        serializer = TourSerializers(tours, many=True)
        return Response(serializer.data) 


class TourPage(APIView):

    """ Page of Tour """
    
    def get(self, request, pk, format=None):
        tour = get_object_or_404(Tour, pk=pk)
        serializer = TourPageSerializers(tour)
        return Response(serializer.data)


class PagesReview(APIView):
    """ Comments for a tour """
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request, pk, format=None):
        serializer = TourReviewsPostSerializers(data=request.data)
        tours = get_object_or_404(Tour, pk=pk)
        if serializer.is_valid():
            serializer.save(review_creator=request.user, tour=tours)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete(request, pk, format=None):
    tour = get_object_or_404(Tour, pk=pk)


class UserDetail(APIView):
    """ User page """
    permission_classes = [permissions.IsAuthenticated,]
    
    def get(self, request, format=None):
        user = get_object_or_404(User, username=self.request.user)
        serializer = UserPageSerializers(user)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        book = get_object_or_404(Booking, pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TourBooking(APIView):
    """ Booking of a tour """
    permission_classes = [permissions.IsAuthenticated,]

    def get(self, request, pk, format=None):
        tours = get_object_or_404(Tour, pk=pk)
        serializer = TourPageSerializers(tours)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        tours = get_object_or_404(Tour, pk=pk)
        serializer = BookingPostSerializers(data=request.data)
        data = 'Hello, ' + request.user.username + '! This is confirmation email about your booking for ' + tours.title + '\n '\
               + tours.text + ' \nPlace: ' + str(tours.city) + ' \nType of tour: ' + str(tours.type_of_tour) + '\nAge requirements is ' + tours.age_requirements +\
               '\nPrice ' + str(tours.price) + ' ' + tours.currency + '\nDuration ' + tours.duration + '\n Thank you for choosing us!' + '\n Best Regards, \n team of Tours_KZ'
        if serializer.is_valid():
            serializer.save(booking_creator=request.user, tour=tours, booking_price=tours.price)
            send_mail('Confirmation', data, 'kenesovbt@gmail.com', [request.user.email])
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
