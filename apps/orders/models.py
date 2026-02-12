from django.db import models
from django.conf import settings
from apps.accommodations.models import Accommodation, RoomClass


class OrderitemQueryset(models.QuerySet):
    def total_price(self):
        return sum(item.price for item in self)

    def total_quantity(self):
        return len([item for item in self])


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_DEFAULT,
        blank=True,
        null=True,
        verbose_name="Пользователь",
        default=None
    )
    created_timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания заказа"
    )
    phone_number = models.CharField(
        max_length=20, verbose_name="Номер телефона"
    )
    email = models.EmailField(
        verbose_name="Электронная почта", blank=True
    )
    payment_on_get = models.BooleanField(
        default=False, verbose_name="Оплата в офисе"
    )
    is_paid = models.BooleanField(
        default=False, verbose_name="Оплачено"
    )
    status = models.CharField(
        max_length=50, default='В обработке',
        verbose_name="Статус заказа"
    )

    class Meta:
        db_table = "order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ("id",)

    def __str__(self):
        return (f"Заказ № {self.pk} | "
                f"Покупатель {self.user.first_name} "
                f"{self.user.last_name}")


class OrderItem(models.Model):
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        verbose_name="Заказ"
    )
    accommodation = models.ForeignKey(
        to=Accommodation,
        on_delete=models.SET_DEFAULT,
        null=True,
        verbose_name="Тур",
        default=None
    )
    name = models.CharField(
        max_length=150, verbose_name="Название"
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
    price = models.DecimalField(
        verbose_name="Цена",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата продажи"
    )

    class Meta:
        db_table = "order_item"
        verbose_name = "Проданный тур"
        verbose_name_plural = "Проданные туры"
        ordering = ("id",)

    objects = OrderitemQueryset.as_manager()

    def __str__(self):
        return f"Отель {self.name} Заказ № {self.order.pk}"
