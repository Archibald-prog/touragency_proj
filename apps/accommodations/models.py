from django.db import models
from django.urls import reverse
from django.db.models import F, Value, Sum, Q
from apps.accommodations.utils import gen_slug


class AccommodationManager(models.Manager):
    def get_extra_fields(self):
        accommodations = self.model.objects.annotate(
            single_price=Sum(
                F("room_costs__cost_per_night"),
                filter=Q(room_costs__room_class_id=1),
                distinct=True),
            start_price=F("single_price") * Value(7) + F("flight_cost_per_one"),
            single_availability=Sum(
                F("accommodationavailability__availability"),
                filter=Q(accommodationavailability__room_class_id=1),
                distinct=True),
            standard_availability=Sum(
                F("accommodationavailability__availability"),
                filter=Q(accommodationavailability__room_class_id=2),
                distinct=True),
            comfort_availability=Sum(
                F("accommodationavailability__availability"),
                filter=Q(accommodationavailability__room_class_id=3),
                distinct=True),
            deluxe_availability=Sum(
                F("accommodationavailability__availability"),
                filter=Q(accommodationavailability__room_class_id=4),
                distinct=True),
            total_availability=F("single_availability") + F("standard_availability") +
                               F("comfort_availability") + F("deluxe_availability")
        )
        return accommodations


class Country(models.Model):
    name = models.CharField(
        verbose_name="Страна",
        max_length=150, unique=True
    )
    slug = models.SlugField(
        max_length=160, blank=True, unique=True,
        db_index=True, verbose_name="URL"
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    country_image = models.ImageField(
        verbose_name="Изображение",
        upload_to="country_img/"
    )
    is_active = models.BooleanField(
        verbose_name="Активна",
        default=True
    )

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self, self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("country_list", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"


class Region(models.Model):
    name = models.CharField(
        verbose_name="Регион",
        max_length=150, unique=True
    )
    slug = models.SlugField(
        max_length=160, blank=True, unique=True,
        db_index=True, verbose_name="URL"
    )
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE,
        verbose_name="Страна", related_name="country_regions"
    )
    is_active = models.BooleanField(
        verbose_name="Активен",
        default=True
    )

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self, self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"


class Accommodation(models.Model):
    name = models.CharField(
        verbose_name="Объект",
        max_length=150, unique=True
    )
    slug = models.SlugField(
        max_length=160, blank=True, unique=True,
        db_index=True, verbose_name="URL"
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True
    )
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE,
        verbose_name="Страна",
    )
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE,
        verbose_name="Регион",
    )
    old_price = models.DecimalField(
        verbose_name="Старая цена",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )
    is_new = models.BooleanField(
        verbose_name="Новинка",
        default=False
    )
    is_top = models.BooleanField(
        verbose_name="Топовое направление",
        default=False
    )
    flight_cost_per_one = models.DecimalField(
        verbose_name="Стоимость перелета на одного",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        verbose_name="Активен",
        default=True
    )

    objects = AccommodationManager()

    def __str__(self):
        return f"{self.name} ({self.country.name})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self, self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("accommodation_detail",
                       kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Объект"
        verbose_name_plural = "Объекты"
        ordering = ["id"]


class AccommodationImage(models.Model):
    CARD = 'c'
    SLIDER = 's'
    TYPES = (
        (CARD, 'карточка'),
        (SLIDER, 'слайдер')
    )

    name = models.CharField(
        verbose_name="Название",
        max_length=100
    )
    image = models.ImageField(
        verbose_name="Изображение",
        upload_to="accommodation_images/"
    )
    image_type = models.CharField(
        verbose_name="тип", max_length=1,
        choices=TYPES, blank=True, default=SLIDER
    )
    accommodation = models.ForeignKey(
        Accommodation, verbose_name="Объект",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Изображение объекта"
        verbose_name_plural = "Изображения объекта"


class RoomClass(models.Model):
    name = models.CharField(
        verbose_name="Класс",
        max_length=150, unique=True
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Класс номера"
        verbose_name_plural = "Классы номеров"


class AccommodationCost(models.Model):
    accommodation = models.ForeignKey(
        Accommodation, verbose_name="Объект",
        related_name="room_costs",
        on_delete=models.CASCADE
    )
    room_class = models.ForeignKey(
        RoomClass, verbose_name="Класс номера",
        on_delete=models.CASCADE
    )
    cost_per_night = models.DecimalField(
        verbose_name="Стоимость суток",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.accommodation.slug}-{self.room_class}"

    class Meta:
        verbose_name = "Стоимость номера"
        verbose_name_plural = "Стоимость номеров"


class AccommodationAvailability(models.Model):
    accommodation = models.ForeignKey(
        Accommodation, verbose_name="Объект",
        on_delete=models.CASCADE
    )
    room_class = models.ForeignKey(
        RoomClass, verbose_name="Класс номера",
        on_delete=models.CASCADE
    )
    availability = models.PositiveIntegerField(
        verbose_name="Число свободных номеров",
        default=0
    )

    def __str__(self):
        return f"{self.accommodation.slug}-{self.room_class}"

    class Meta:
        verbose_name = "Наличие номера"
        verbose_name_plural = "Наличие номеров"


class AccommodationFeatures(models.Model):
    accommodation = models.ForeignKey(
        Accommodation, verbose_name="Объект",
        on_delete=models.CASCADE
    )
    detailed_desc = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE,
        verbose_name="Страна",
    )
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE,
        verbose_name="Регион",
    )

    def __str__(self):
        return f"{self.accommodation.name}"

    class Meta:
        verbose_name = "Характеристика объекта"
        verbose_name_plural = "Характеристики объекта"
