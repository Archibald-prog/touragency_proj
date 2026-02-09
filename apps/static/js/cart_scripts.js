$(document).ready(function () {

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

});