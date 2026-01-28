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
        country_accommodations = (
            models.Accommodation.objects.get_extra_fields().
                                  filter(country__slug=country.slug)
        )
        field_name_lst = [attr for attr in country_accommodations[0].__dict__
                          if attr.__contains__('availability')] [:-1]
        room_classes = models.RoomClass.objects.all()
        availability_nums = []
        for field in field_name_lst:
            availability_nums.append(
                len([item for item in country_accommodations if getattr(item, field) > 0])
            )
        res_dict = {key: val for key, val in zip(room_classes, availability_nums)}
        return res_dict


