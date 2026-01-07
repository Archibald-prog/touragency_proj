from django.db import models


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

    def __str__(self):
        return f"{self.name} ({self.country.name})"

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
        return f"{self.accommodation__name}{self.room_class}"

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
        return f"{self.accommodation__name}{self.room_class}"

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
        return f"{self.accommodation__name}"

    class Meta:
        verbose_name = "Характеристика объекта"
        verbose_name_plural = "Характеристики объекта"
