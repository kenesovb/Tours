from django.contrib import admin

from .models import *


# Register your models here.


class RegionAdmin(admin.ModelAdmin):
    model = Region
    list_display = ('region_name',)


class ToursTravelAgentAdmin(admin.ModelAdmin):
    model = ToursTravelAgent
    list_display = ('travel_agent_name',)


class CityAdmin(admin.ModelAdmin):
    model = City
    list_display = ['get_region_name', 'city_name', ]
    list_select_related = ('city_region',)

    def get_region_name(self, obj):
        return obj.city_region.region_name


class HotelsImagesAdmin(admin.StackedInline):
    model = HotelsImages


class TourHotelAdmin(admin.ModelAdmin):
    model = Hotels
    list_display = ('hotel_name', 'hotel_city')
    list_select_related = ('hotel_city',)
    inlines = [HotelsImagesAdmin]


class TourImageAdmin(admin.StackedInline):
    model = TourImage


class ProvidedServiceAdmin(admin.ModelAdmin):
    model = ProvidedServices


class TourCommentsAdmin(admin.StackedInline):
    model = TourReview
    list_display = ['tour', 'comment_creator', 'comment_text', ]

class BookingAdmin(admin.StackedInline):
    model = Booking


class TourAdminFilter(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(TourAdminFilter, self).get_queryset(request)
        if request.user.is_superuser:
            return qs.all()
        else:
            return qs.filter(creator=request.user)

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        obj.save()

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        if request.user.is_superuser or obj.creator == request.user:
            return True
        else:
            return False

    has_delete_permission = has_change_permission


class TypeOfTourAdmin(admin.ModelAdmin):
    model = TypeOfTour


class TourAdmin(TourAdminFilter):
    """ admin page of Tours"""
    # model = Tour
    list_display = ['creator', 'created_date', 'title', 'city', 'region',
                    'duration', 'tours_travel_agent']
    list_filter = ('city', 'region',)
    exclude = ['creator']
    inlines = [TourImageAdmin]

    def city(self, obj):
        return obj.city.city_name

    def region(self, obj):
        return obj.city.city_region.region_name

    def type_of_tour(self, obj):
        return obj.type_of_tour.type_of_tour_name

    def tours_travel_agent(self, obj):
        return obj.travel_agent_id.travel_agent_name


class TourDetailsAdmin(admin.ModelAdmin):
    list_display = ['get_tour_name', 'tour_start_date', 'tour_end_date']
    inlines = [BookingAdmin,]
    def get_tour_name(self, obj):
        return obj.tour.title


admin.site.register(Tour, TourAdmin)
admin.site.register(ToursTravelAgent, ToursTravelAgentAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(ProvidedServices, ProvidedServiceAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(TypeOfTour, TypeOfTourAdmin)
admin.site.register(Hotels, TourHotelAdmin)
admin.site.register(TourDetails, TourDetailsAdmin)
