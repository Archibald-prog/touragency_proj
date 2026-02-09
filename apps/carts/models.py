from django.db import models
from django.conf import settings
from apps.accommodations.models import Accommodation, RoomClass


class CartQueryset(models.QuerySet):
    def total_price(self):
        return sum(cart.accommodation_cost for cart in self)

    def total_nights(self):
        if self:
            return sum(cart.nights for cart in self)
        return 0

    def total_flights(self):
        if self:
            return sum(cart.flight_cost for cart in self)
        return 0

    def total_tours(self):
        return len([cart for cart in self])


class Cart(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='cart'
    )
    session_key = models.CharField(
        max_length=32,
        null=True,
        blank=True
    )
    accommodation = models.ForeignKey(
        Accommodation,
        on_delete=models.CASCADE,
        verbose_name="Объект",
    )
    room_class = models.ForeignKey(
        RoomClass, verbose_name="Класс номера",
        on_delete=models.CASCADE,
        default=1
    )
    nights = models.PositiveIntegerField(
        verbose_name="Число ночей",
        default=3
    )
    guests = models.PositiveIntegerField(
        verbose_name="Число гостей",
        default=1
    )
    add_datetime = models.DateTimeField(
        verbose_name='Время добавления',
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"
        ordering = ("id",)

    objects = CartQueryset().as_manager()

    def __str__(self):
        if self.user:
            return (f"Корзина {self.user.username} | "
                    f"Объект {self.accommodation.name}")
        return (f"Анонимная корзина |"
                f"Объект {self.accommodation.name}")

    @property
    def cost_per_night(self):
        from apps.accommodations.models import AccommodationCost
        obj = AccommodationCost.objects.filter(
            accommodation_id=self.accommodation,
            room_class_id=self.room_class).first()
        return obj.cost_per_night * self.guests

    @property
    def flight_cost(self):
        return self.accommodation.flight_cost_per_one * self.guests

    @property
    def accommodation_cost(self):
        return self.cost_per_night * self.nights + self.flight_cost
