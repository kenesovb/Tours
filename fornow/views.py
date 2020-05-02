from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail, EmailMessage
import io
from django.http import HttpResponse
from xhtml2pdf import pisa
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from .models import Tour, Booking, TourImage, Hotels, TourDetails
from .serializers import (TourSerializers, TourPageSerializers, UserPageSerializers, TourReviewsPostSerializers, BookingPostSerializers, HotelSerializers,
                          TourDetailsPostSerializers)


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


class UserDetail(APIView):
    """ User page """
    permission_classes = [permissions.IsAuthenticated,]
    
    def get(self, request, format=None):
        user = get_object_or_404(User, username=self.request.user)
        serializer = UserPageSerializers(user)
        return Response(serializer.data)

class UserDetailDelAndPdf(APIView):
    """ User page delete tour and create PDF"""
    permission_classes = [permissions.IsAuthenticated, ]
    def delete(self, request, pk, format=None):
        book = get_object_or_404(Booking, pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk,format=None):
        user = get_object_or_404(User, username=self.request.user)
        book = get_object_or_404(Booking, pk=pk)
        image = TourImage.objects.filter(tour=book.tour.id)
        template = get_template('pdf_template.html')
        paragraph = {
            "FirstName": user.username,
            "LastName": user.last_name,
        }
        html = template.render(paragraph)
        pdf = render_to_pdf('pdf_template.html', paragraph)
        if pdf:
           response = HttpResponse(pdf, content_type='application/pdf')
        # ms = EmailMessage('cofirmation', "Everything is ok", 'kenesovbt@gmail.com', [request.user.email])
        # ms.attach(pdf)
        # ms.send()
        return response


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')


class TourBooking(APIView):
    """ Booking of a tour """
    permission_classes = [permissions.IsAuthenticated,]

    def get(self, request, pk, detailid, format=None):
        tours = get_object_or_404(Tour, pk=pk)
        tours_detail = get_object_or_404(TourDetails, pk=detailid)
        serializer = TourPageSerializers(tours)
        return Response(serializer.data)

    def post(self, request, pk, detailid):
        tour = get_object_or_404(Tour, pk=pk)
        tours = get_object_or_404(TourDetails, pk=detailid)
        serializer = BookingPostSerializers(data=request.data)
        tours.cur_person_number = tours.cur_person_number+int(request.data['cur_person_number'])
        tours.save()
        if serializer.is_valid():
            serializer.save(booking_creator=request.user, tour_detail=tours, booking_price=tour.price)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def update(self, instance, validated_data):
    #     instance.cur_person_number = validated_data['cur_person_number']
    #     instance.save()


class HotelsView(APIView):
    """"""
    def get(self, request):
        hotels = Hotels.objects.all()
        serializer = HotelSerializers(hotels, many=True)
        return Response(serializer.data)
