from django.urls import path
from .views import PagesReview, TourView, TourPage, UserDetail, TourBooking, UserDetailDeleteBooking, HotelsView, UserDetailPDFView,UserDetailPDFViewDownload, HotelPageView, \
    BookingPayView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('tours/', TourView.as_view()),
    path('hotels/', HotelsView.as_view()),
    path('hotels/<int:pk>', HotelPageView.as_view()),
    path('tours/<int:pk>/', TourPage.as_view()),
    path('tours/<int:pk>/reviews', PagesReview.as_view()),
    path('tours/<int:pk>/<int:detailid>/booking', TourBooking.as_view()),
    path('users/me', UserDetail.as_view()),
    path('users/me/<int:pk>', UserDetailDeleteBooking.as_view()),
    path('users/me/payment', BookingPayView.as_view()),
    path('users/me/<int:pk>/pdf', UserDetailPDFView.as_view()),
    path('users/me/<int:pk>/pdf/download', UserDetailPDFViewDownload.as_view()),
]