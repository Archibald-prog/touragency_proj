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

    def get_queryset(self):
        country_slug = self.kwargs["slug"]
        queryset = Accommodation.objects.get_extra_fields().filter(
            country__slug=country_slug)
        region_lst = self.request.GET.getlist("region")
        available_lst = self.request.GET.getlist("roomclass")

        filters = Q()
        if region_lst:
            filters &= Q(region__in=region_lst)
        if available_lst:
            # Используем distinct(), так как фильтр по ManyToMany/ForeignKey
            # может дублировать строки
            filters &= Q(accommodationavailability__room_class_id__in=available_lst,
                         accommodationavailability__availability__gt=0)
            queryset = queryset.distinct()

        queryset = queryset.filter(filters)

        user_ordering = self.request.GET.get("orderby")
        if user_ordering:
            queryset = queryset.order_by(user_ordering, "id")
        else:
            # Дефолтная сортировка
            queryset = queryset.order_by("id")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params = self.request.GET.copy()
        if 'page' in params:
            del params['page']
        context['url_params'] = params.urlencode()
        context["selected_regions"] = self.request.GET.getlist("region")
        context["selected_roomclasses"] = self.request.GET.getlist("roomclass")

        country = get_object_or_404(Country, slug=self.kwargs["slug"])
        context.update({
            "title": f"Страна - {country}",
            "country": country,
            "country_regions": self.get_regions(country),
            "available_accommodations": self.get_available(country),
        })
        return context
