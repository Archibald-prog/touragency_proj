from django.db.models import Count
from apps.accommodations import models


class GetAdditionalData:
    def get_link_menu(self):
        """
        Returns a collection of all countries
        """
        return models.Country.objects.all()

    def get_regions(self, country):
        """
        Returns a collection of regions
        in a given country and a number of hotels in each region
        """
        country_regions = country.country_regions.all()
        accommodations_num = [item.accommodation_set.all().count()
                              for item in country_regions]
        res_dict = {key: val for key, val in zip(
            country_regions, accommodations_num)
                    }
        return res_dict

    def get_available(self, country):
        """
        Returns a number of hotels in a given country
        with available rooms of each class
        """
        counts = models.RoomClass.objects.filter(
            accommodationavailability__accommodation__country=country,
            accommodationavailability__availability__gt=0
        ).annotate(
            hotel_count=Count(
                'accommodationavailability__accommodation',
                distinct=True)
        )
        res_dict = {rc: rc.hotel_count for rc in counts}
        return res_dict

    @staticmethod
    def get_user_cart(request):
        """
        Returns a collection of items
        in the current user's cart.
        """
        from apps.carts import models
        if request.user.is_authenticated:
            return (models.Cart.objects.filter(user=request.user).
                    select_related("accommodation"))
        if not request.session.session_key:
            request.session.create()
        return (models.Cart.objects.filter(
            session_key=request.session.session_key).
                select_related("accommodation"))

    @staticmethod
    def get_roomclasses():
        return models.RoomClass.objects.all()
