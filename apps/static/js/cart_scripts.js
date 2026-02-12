$(document).ready(function () {
    var successMessage = $("#jq-notification");

    var notification = $('#notification');
    if (notification.length > 0) {
        setTimeout(function () {
            notification.alert('close');
        }, 5000);
    }

    $(document).on("click", ".add-to-cart", function(e) {
        e.preventDefault();

        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);
        var accommodation_id = $(this).data("accommodation-id");
        var add_to_cart_url = $(this).attr("href");

        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                accommodation_id: accommodation_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },

            success: function (data) {
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 5000);

                cartCount++;
                goodsInCartCount.text(cartCount);

                // Перерисовываем html-код с разметкой корзины
                var cartItemsContainer = $(".cart_items");
                cartItemsContainer.html(data.cart_items_html);
            },
            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });

    $(document).on("click", ".remove-from-cart", function (e) {
        e.preventDefault();
        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);
        var cart_id = $(this).data("cart-id");
        var remove_from_cart = $(this).attr("href");

        $.ajax({
            type: "POST",
            url: remove_from_cart,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },

            success: function (data) {
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 5000);

                cartCount -= data.quantity_deleted;
                goodsInCartCount.text(cartCount);

                var cartItemsContainer = $(".cart_items");
                cartItemsContainer.html(data.cart_items_html);

            },
            error: function (data) {
                console.log("Ошибка при удалении товара из корзины");
            },
        });
    });

    $(document).on("click", ".roomclass-change", function () {
        var url = $(this).attr('data-cart-change-url');
        var cartID = $(this).attr('data-cart-id');
        var roomclassID = $(this).val();

        $.ajax({
           type: "POST",
           url: url,
           data: {
               cart_id: cartID,
               roomclass: roomclassID,
               csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
           },
           success: function (data) {
               var goodsInCartCount = $("#goods-in-cart-count");
               var cartCount = parseInt(goodsInCartCount.text() || 0);

               cartCount = data.total_tours;
               goodsInCartCount.text(cartCount);

               var cartItemsContainer = $(".cart_items");
               cartItemsContainer.html(data.cart_items_html);

           },
           error: function (data) {
               console.log("Ошибка при редактировании корзины");
           },
        });
    });

    $(document).on("click", ".guest-change", function(e) {
        var target_href = event.target;
        var url = target_href.getAttribute('data-cart-change-url');
        var cartID = target_href.getAttribute('data-cart-id');
        var currentValue = target_href.value;

        $.ajax({
           type: "POST",
           url: url,
           data: {
               cart_id: cartID,
               guests: currentValue,
               csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
           },
           success: function (data) {
               var goodsInCartCount = $("#goods-in-cart-count");
               var cartCount = parseInt(goodsInCartCount.text() || 0);

               cartCount = data.total_tours;
               goodsInCartCount.text(cartCount);

               var cartItemsContainer = $(".cart_items");
               cartItemsContainer.html(data.cart_items_html);

           },
           error: function (data) {
               console.log("Ошибка при редактировании корзины");
           },
        });
    });

    $(document).on("click", ".night-change", function(e) {
        var target_href = event.target;
        var url = target_href.getAttribute('data-cart-change-url');
        var cartID = target_href.getAttribute('data-cart-id');
        var currentValue = target_href.value;

        $.ajax({
           type: "POST",
           url: url,
           data: {
               cart_id: cartID,
               nights: currentValue,
               csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
           },
           success: function (data) {
               var goodsInCartCount = $("#goods-in-cart-count");
               var cartCount = parseInt(goodsInCartCount.text() || 0);

               cartCount = data.total_tours;
               goodsInCartCount.text(cartCount);

               var cartItemsContainer = $(".cart_items");
               cartItemsContainer.html(data.cart_items_html);

           },
           error: function (data) {
               console.log("Ошибка при редактировании корзины");
           },
        });
    });

    // Форматирования ввода номера телефона в форме (xxx) xxx-хххx
    document.getElementById('id_phone_number').addEventListener('input', function (e) {
        var x = e.target.value.replace(/\D/g, '').match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
        e.target.value = !x[2] ? x[1] : '(' + x[1] + ') ' + x[2] + (x[3] ? '-' + x[3] : '');
    });

    // Проверяем на стороне клинта коррекность номера телефона в форме xxx-xxx-хх-хx
    $('#create_order_form').on('submit', function (event) {
        var phoneNumber = $('#id_phone_number').val();
        var regex = /^\(\d{3}\) \d{3}-\d{4}$/;

        if (!regex.test(phoneNumber)) {
            $('#phone_number_error').show();
            event.preventDefault();
        } else {
            $('#phone_number_error').hide();

            // Очистка номера телефона от скобок и тире перед отправкой формы
            var cleanedPhoneNumber = phoneNumber.replace(/[()\-\s]/g, '');
            $('#id_phone_number').val(cleanedPhoneNumber);
        }
    });

});