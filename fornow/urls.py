from django.urls import path
from .views import PagesReview, TourView, TourPage, UserDetail, TourBooking, UserDetailDelAndPdf, HotelsView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('tours/', TourView.as_view()),
    path('hotels/', HotelsView.as_view()),
    path('tours/<int:pk>/', TourPage.as_view()),
    path('tours/<int:pk>/reviews', PagesReview.as_view()),
    path('tours/<int:pk>/<int:detailid>/booking', TourBooking.as_view()),
    path('users/me', UserDetail.as_view()),
    path('users/me/<int:pk>', UserDetailDelAndPdf.as_view()),
]