$(document).ready(function () {
    const successMessage = $("#jq-notification");
    const $cartCounters = $(".goods-in-cart-count");
    const cartItemsContainer = $(".cart_items");

    // Универсальная функция обновления UI
    function updateTourUI(data, isAdd = null) {
        if (data.message) {
            successMessage.html(data.message).fadeIn(400);
            setTimeout(() => successMessage.fadeOut(400), 5000);
        }

        // Обновление счетчика
        let currentCount = parseInt($cartCounters.first().text() || 0);
        let totalCount = data.total_tours;

        if (totalCount !== undefined) {
            $cartCounters.text(totalCount);
        } else if (isAdd === true) {
            $cartCounters.text(currentCount + 1);
        } else if (isAdd === false && data.quantity_deleted !== undefined) {
            $cartCounters.text(currentCount - data.quantity_deleted);
        }

        // Обновление разметки корзины
        if (data.cart_items_html) {
            cartItemsContainer.html(data.cart_items_html);
        }
    }

    // Обработка уведомлений от Django (messages)
    const notification = $('#notification');
    if (notification.length > 0) {
        setTimeout(() => notification.alert('close'), 5000);
    }

    // 1. Добавление и Удаление (Click)
    $(document).on("click", ".add-to-cart, .remove-from-cart", function (e) {
        e.preventDefault();
        const $el = $(this);
        const isAdding = $el.hasClass("add-to-cart");
        const url = $el.attr("href");

        const postData = { csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val() };
        if (isAdding) {
            postData.accommodation_id = $el.data("accommodation-id");
        } else {
            postData.cart_id = $el.data("cart-id");
        }

        $.ajax({
            type: "POST",
            url: url,
            cache: false,
            data: postData,
            success: (data) => updateTourUI(data, isAdding),
            error: () => console.error("Ошибка при обновлении корзины")
        });
    });

    // 2. Изменение параметров тура (Select / Input)
    // Объединяем .roomclass-change, .guest-change, .night-change
    $(document).on("change input", ".roomclass-change, .guest-change, .night-change", function () {
        const $el = $(this);
        const postData = {
            cart_id: $el.data('cart-id'),
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
        };

        // Динамически определяем ключ для POST (roomclass, guests или nights)
        if ($el.hasClass('roomclass-change')) postData.roomclass = $el.val();
        else if ($el.hasClass('guest-change')) postData.guests = $el.val();
        else if ($el.hasClass('night-change')) postData.nights = $el.val();

        $.ajax({
            type: "POST",
            url: $el.data('cart-change-url'),
            cache: false,
            data: postData,
            success: updateTourUI,
            error: () => console.error("Ошибка при редактировании тура")
        });
    });

    // Универсальный обработчик для всех кнопок +/-
    $(document).on("click", ".step-btn", function() {
        const $button = $(this);
        // Ищем ближайший инпут внутри той же группы (неважно, guest или night)
        const $input = $button.closest(".input-group").find("input[type='number']");

        // Берем значения из атрибутов конкретного инпута
        const step = parseInt($input.attr("step")) || 1; // Если step не указан, шаг = 1
        const min = parseInt($input.attr("min")) || 1;  // Если min не указан, минимум = 1
        let currentValue = parseInt($input.val()) || min;

        if ($button.data("action") === "plus") {
            $input.val(currentValue + step);
        } else if (currentValue > min) {
            $input.val(currentValue - step);
        }

        $input.trigger("input");
    });

    // 3. Маска телефона (с защитой от null)
    const phoneInput = document.getElementById('id_phone_number');
    if (phoneInput) {
        phoneInput.addEventListener('input', function (e) {
            let x = e.target.value.replace(/\D/g, '').match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
            if (!x) return;
            e.target.value = !x[2] ? x[1] : '(' + x[1] + ') ' + x[2] + (x[3] ? '-' + x[3] : '');
        });
    }

    // 4. Валидация формы
    $('#create_order_form').on('submit', function (e) {
        const $phone = $('#id_phone_number');
        const phoneNumber = $phone.val();
        if (!/^\(\d{3}\) \d{3}-\d{4}$/.test(phoneNumber)) {
            $('#phone_number_error').show();
            e.preventDefault();
        } else {
            $('#phone_number_error').hide();
            $phone.val(phoneNumber.replace(/\D/g, ''));
        }
    });
});
