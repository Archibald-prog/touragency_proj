from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.views.generic import ListView, DetailView
from apps.accommodations.models import Accommodation, Country
from apps.accommodations.utils import get_random_id
from apps.helpers import GetAdditionalData


class AccommodationListView(ListView, GetAdditionalData):
    model = Accommodation

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = Accommodation.objects.get_extra_fields().filter(
                Q(name__iregex=search_query) |
                Q(country__name__iregex=search_query) |
                Q(region__name__iregex=search_query) |
                Q(description__iregex=search_query)
            )
        else:
            id_list = get_random_id()
            queryset = Accommodation.objects.get_extra_fields().filter(
                pk__in=id_list
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "объекты/главная"
        id_list = get_random_id(top=False)
        new_accommodations = (Accommodation.objects.get_extra_fields().
                              filter(pk__in=id_list))
        context["new_accommodations"] = new_accommodations
        if 'search' in self.request.GET:
            context['searching'] = True
        return context


class AccommodationDetailView(DetailView, GetAdditionalData):
    queryset = Accommodation.objects.get_extra_fields()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "объекты/объект"
        obj = context["object"]
        features = obj.accommodationfeatures_set.all().first()
        same_accommodations = (Accommodation.objects.get_extra_fields().
                               filter(
            country=obj.country).exclude(pk=obj.pk))
        context["same_accommodations"] = same_accommodations
        context["features"] = features
        return context


class CountryListView(ListView, GetAdditionalData):
    model = Accommodation
    template_name = "accommodations/country_list.html"
    paginate_by = 6
    allow_empty = True

    def get_queryset(self):
        country_slug = self.kwargs["slug"]
        q_objects = Q()
        region_lst = self.request.GET.getlist("region")
        if region_lst:
            q_objects.add(Q(region__in=region_lst), Q.AND)

        available_lst = self.request.GET.getlist("roomclass")
        if available_lst:
            q_objects.add(
                Q(accommodationavailability__room_class_id__in=available_lst),
                Q.AND)
            q_objects.add(
                Q(accommodationavailability__availability__gt=0), Q.AND)

        if q_objects:
            queryset = (Accommodation.objects.get_extra_fields().
                        filter(q_objects, country__slug=country_slug))
        else:
            queryset = (Accommodation.objects.get_extra_fields().
                        filter(country__slug=country_slug))

        ordering = self.get_ordering()
        if ordering:
            queryset = queryset.order_by(*(ordering,))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        country = get_object_or_404(Country, slug=self.kwargs["slug"])
        context["title"] = "Страна -" + str(country)
        context["country"] = country
        context["country_regions"] = self.get_regions(country)
        context["available_accommodations"] = self.get_available(country)
        return context

    def get_ordering(self):
        ordering = self.request.GET.get("orderby")
        return ordering
