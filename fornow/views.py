import os

from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from io import BytesIO
from django.http import HttpResponse
from xhtml2pdf import pisa
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from .models import Tour, Booking, TourImage, Hotels, TourDetails
from .serializers import (TourSerializers, TourPageSerializers, UserPageSerializers, TourReviewsPostSerializers,
                          BookingPostSerializers, HotelSerializers,
                          TourDetailsPostSerializers, BookingSerializers, HotelPageSerializers, TourImageSerializer)


# Create your views here.

class TourView(APIView):
    """Tour"""
    permission_classes = [permissions.AllowAny, ]

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
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, pk, format=None):
        serializer = TourReviewsPostSerializers(data=request.data)
        tours = get_object_or_404(Tour, pk=pk)
        if serializer.is_valid():
            serializer.save(review_creator=request.user, tour=tours)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """ User page """
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, format=None):
        user = get_object_or_404(User, username=self.request.user)
        serializer = UserPageSerializers(user)
        return Response(serializer.data)


class UserDetailDeleteBooking(APIView):
    """ User page delete tour and create PDF"""
    permission_classes = [permissions.IsAuthenticated, ]

    def delete(self, request, pk, format=None):
        book = get_object_or_404(Booking, pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetailPDFView(APIView):
    """PDF of tour ticket """
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, pk):
        user = get_object_or_404(User, username=self.request.user)
        book = get_object_or_404(Booking, pk=pk)
        start_date = str(book.tour_detail.tour_start_date)
        end_date = str(book.tour_detail.tour_end_date)
        total_amount = book.booking_number_of_persons * book.tour_detail.tour.price
        type_of_tour = book.tour_detail.tour.type_of_tour.all()
        paragraph = {
            "FirstName": user.first_name,
            "LastName": user.last_name,
            "book": book,
            "type_of_tour": type_of_tour,
            "start_date": start_date,
            "end_date": end_date,
            "total_amount": total_amount
        }
        pdf = render_to_pdf('pdf_template.html', paragraph)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
        return response


class UserDetailPDFViewDownload(APIView):
    """PDF of tour ticket """
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, pk):
        user = get_object_or_404(User, username=self.request.user)
        book = get_object_or_404(Booking, pk=pk)
        start_date = str(book.tour_detail.tour_start_date)
        end_date = str(book.tour_detail.tour_end_date)
        total_amount = book.booking_number_of_persons * book.tour_detail.tour.price
        paragraph = {
            "FirstName": user.first_name,
            "LastName": user.last_name,
            "book": book,
            "start_date": start_date,
            "end_date": end_date,
            "total_amount": total_amount
        }
        pdf = render_to_pdf('pdf_template.html', paragraph)
        pdf = render_to_pdf('pdf_template.html', paragraph)
        if pdf:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=ticket.pdf'
            response.write(pdf)
        return response


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)
    if not pdf.err:
        return result.getvalue()


class TourBooking(APIView):
    """ Booking of a tour """
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, pk, detailid, format=None):
        tours = get_object_or_404(Tour, pk=pk)
        tours_detail = get_object_or_404(TourDetails, pk=detailid)
        serializer = TourPageSerializers(tours)
        return Response(serializer.data)

    def post(self, request, pk, detailid):
        tour = get_object_or_404(Tour, pk=pk)
        tours = get_object_or_404(TourDetails, pk=detailid)
        serializer = BookingPostSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(booking_creator=request.user, tour_detail=tours, booking_price=tour.price,
                            booking_number_of_persons=request.data['booking_number_of_persons'])
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingPayView(APIView):
    """all Bookings payment update status to approved """

    def post(self, request):
        user = get_object_or_404(User, username=self.request.user)
        bookings = get_object_or_404(Booking, pk=request.data['id'])
        tour = get_object_or_404(Tour, pk=bookings.tour_detail.tour.id)
        image = TourImage.objects.filter(tour=bookings.tour_detail.tour.id)[0]
        tour.tour_rating = tour.tour_rating + int(bookings.booking_number_of_persons)
        message = Mail(
            from_email='kenesovbt@gmail.com',
            to_emails=user.email,
            subject='Information about your ' + bookings.tour_detail.tour.title + ' tour',
            html_content='<h2>Hello, dear Traveller! </h2> <br> <h3>Below some information about your tour </h3> <br>' +
                         '<strong>' + bookings.tour_detail.tour.title + '</strong>' +
                         '<p> Star date: <strong>' + str(bookings.tour_detail.tour_start_date) + '</strong> </p>' +
                         '<p> End date: <strong>' + str(bookings.tour_detail.tour_end_date) + '</strong> </p>' +
                         '<p> Starting city: <strong>' + str(
                bookings.tour_detail.tour.city.city_name) + '</strong> </p>' +
                         '<p> Ending city: <strong>' + str(bookings.tour_detail.tour.tour_end_city) + '</strong> </p>' +
                         '<p> Price: <strong>' + str(bookings.tour_detail.tour.price) + ' ' + str(bookings.tour_detail.tour.currency) + '</strong> </p>' +
                         '<p> Status: <strong>' + str(bookings.booking_status) + '</strong> </p>' +
                         '<p>you can download your ticket <a href="https://tourismera.herokuapp.com/api/v1/fornow/users/me/' + str(bookings.id) + '/pdf/download"> here </a> </p> <br><br><br><br>' +
                         '<img src="' + image.file.url + '" width="450px" height="450px">' +
                         '<h3>Have fun, hope you will enjoy your vacation across Kazakhstan</h3>' +
                         '<h3>best regards from travel-kazakhstan team.</h3>'
        )
        try:
            sg = SendGridAPIClient(os.environ.get('SendGridAPIClient'))
            response = sg.send(message)
        except Exception as e:
            print(e)
        tour.save()
        bookings.tour_detail.cur_person_number = bookings.tour_detail.cur_person_number + \
                                                 int(bookings.booking_number_of_persons)
        bookings.booking_status = 'Approved'
        bookings.tour_detail.save()
        bookings.save()

        return Response(status=status.HTTP_201_CREATED)


class HotelsView(APIView):
    """"""

    def get(self, request):
        hotels = Hotels.objects.all()
        serializer = HotelSerializers(hotels, many=True)
        return Response(serializer.data)


class HotelPageView(APIView):
    """"""

    def get(self, request, pk):
        hotels = get_object_or_404(Hotels, pk=pk)
        serializer = HotelPageSerializers(hotels)
        return Response(serializer.data)
