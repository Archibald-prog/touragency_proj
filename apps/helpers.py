from apps.accommodations import models


class GetAdditionalData:
    def get_link_menu(self):
        """
        Returns a collection of all countries
        """
        return models.Country.objects.all()
