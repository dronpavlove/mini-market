$(document).ready(function (){
  let add_button = $('#add-button')
  let url_path ='/basket/add/'
  let crsf = ($('input[name="csrfmiddlewaretoken"]').val())
  let all_add_button = $('.add-button')
  let btn = $('#test_button')
  let btn_card = $('#add-button, .add-button')
  let btn_card_text = $('#add-button .btn-content')
  let btn_compare = $('#add-compare, .add-compare')
  let btn_card_pulse = $('.add-button.add-button-pulse')

  function color_button(){
     // если эта кнопка есть на странице
    if (btn_card){
      btn_card.click(function (){
        btn_card_text.text('Товар добавлен')
      })
    }

    if (btn_card_pulse) {
      btn_card_pulse.click(function (){
        // добавить класс анимации
        $(this).addClass("add-button-pulse-anim")
        // анимация на js
        $(this).animate({
          backgroundColor: "#ebebeb",
        }, 3000, function() {
          // анимация завершена.
          // удалить класс анимации
          $(this).removeClass("add-button-pulse-anim")
        });
      })
    }

    if (btn_compare){
      btn_compare.click(function (){
        // $(this).css('background-color', '#1f7eff')
        $(this).addClass("add-button-pulse-anim")
        // анимация на js
        $(this).animate({
          backgroundColor: "#ebebeb",
        }, 3000, function() {
          // анимация завершена.
          // удалить класс анимации
          $(this).removeClass("add-button-pulse-anim")
        });
      })
    }
  }

    all_add_button.click(function (e) {
        e.preventDefault();
        var product_id = $(this).data('product_id');
        var action = $(this).data('action');
      console.log('Пришло в ajax_add_product_in_basket.js: ', product_id, action)

        $.ajax({
            type: 'GET',
            url: url_path,
            data: {
                product_id: product_id,
                action: action
            },
//            'product_amount', 'count_product_in_basket', 'full_sum', 'product_total_cost'
            success: function (json) {
                console.log('Всё прошло ок в добавлении/удалении в ajax_add_product_in_basket.js')
                document.getElementById('basket_count_id').innerHTML = json.count_product_in_basket;
                document.getElementById('subtotal').innerHTML = json.full_sum;
                document.getElementById('subtotal_1').innerHTML = json.full_sum;
                document.getElementById(
                    "product-count_product_in_basket" + product_id
                ).innerHTML = json.product_amount;
                document.getElementById(
                    "product-discount-subotal" + product_id
                ).innerHTML = json.product_total_cost;
                if (json.product_amount === 0) {
                    $('.product-item[data-index=' + product_id + ']').remove();
                    };
                if (json.product_amount > 0) {
                    $('.product-item[data-index=' + product_id + ']').innerHTML = json.product_amount;
                    };
                },
            error: function (xhr, errmsg, err) {
                console.log('Ошибка в добавлении/удалении в ajax_add_product_in_basket.js');
            }
            });
        })

    function product_in_basket_delete(){
    $('.Cart-block.Cart-block_delete').click(function (e) {
        e.preventDefault();
        var product_id = $(this).data('product_id');
        console.log('Пришло в удалить ajax_add_product_in_basket.js: ', product_id)
        $.ajax({
            type: 'GET',
            url: "/basket/delete/",
            data: {
                product_id: product_id,
                action: 'delete'
            },
            success: function (json) {
                console.log('Удалили в ajax_add_product_in_basket.js')
                $('.product-item[data-index=' + product_id + ']').remove();
                document.getElementById('basket_count_id').innerHTML = json.count_product_in_basket;
                document.getElementById('subtotal').innerHTML = json.full_sum;
                document.getElementById('subtotal_1').innerHTML = json.full_sum;
            },
            error: function (xhr, errmsg, err){
            console.log('Ошибка в удалении в ajax_add_product_in_basket.js');
            }
    });
})
    }

   function compare(){
    $(".Card-change").click(function () {
        var productId = $(this).data('product');
        var cacheKey = $(this).data('key')
        $.ajax ({
            url: "/products/count_compare_add/",
            type: "GET",
            data: {'product': productId, 'cache_key': cacheKey
            },
            cache: false,
            success: function (data) {
                console.log('ok');
                console.log(data.com_count);
                console.log(productId, cacheKey);
                $('#compare_count_id').text(data.com_count);
                },
            error: function() {
                console.log('error');
                console.log(productId, cacheKey);
                }
        });
        return false;
    });

    $(".Compare-checkDifferent input").click(function () {
        $('#full').toggle();
        return {
            init: function(){
                $checkDifferent.trigger('change');
            }
        };

    });

    $("#basket").click(function () {
        $.ajax ({
            url: "/products/compare_basket/",
            type: "GET",
            dataType: "text",
            cache: false,
        });
        return false;
    });

    $(".expand").magnificPopup({
      type: "image"
    });

    $("#category_id").click(function () {
    var sh_id = document.getElementById("selshop").value;
    var cat_id = document.getElementById("selcategory").value;
        $.ajax ({
            url: "/import/ajax/",
            type: "GET",
            data: {'shop': sh_id, 'category': cat_id
            },
            cache: false,
            success: function (data) {
                console.log('ok');
                console.log(data);
                $('#category_list').html(data.text);
                document.getElementById('update').style.display='block';
                document.getElementById('file_button').value=data.shop_id + '|' + data.category_id;
                document.getElementById('file').href='/import/export/' + data.category_id
                },
            error: function() {
                console.log('error')
                }
        });
        return false;
    });
   }

  compare()
  color_button()
  product_in_basket_delete()

})