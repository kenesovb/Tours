from django.urls import path
from .views import PagesReview, TourView, TourPage, UserDetail, TourBooking

urlpatterns = [
    path('tours/', TourView.as_view()),
    path('tours/<int:pk>/', TourPage.as_view()),
    path('tours/<int:pk>/reviews', PagesReview.as_view()),
    path('tours/<int:pk>/booking', TourBooking.as_view()),
    path('users/me', UserDetail.as_view()),
    path('users/me/<int:pk>', UserDetail.as_view()),
]