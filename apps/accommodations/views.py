from django.views.generic import ListView, DetailView
from apps.accommodations.models import Accommodation
from apps.accommodations.utils import get_random_id


class AccommodationListView(ListView):
    model = Accommodation

    def get_queryset(self):
        id_list = get_random_id()
        return (Accommodation.objects.get_extra_fields().
                filter(pk__in=id_list))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "объекты/главная"
        id_list = get_random_id(top=False)
        new_accommodations = (Accommodation.objects.get_extra_fields().
                              filter(pk__in=id_list))
        context["new_accommodations"] = new_accommodations
        return context


class AccommodationDetailView(DetailView):
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
