var vigioApp = angular.module('vigioApp', []).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

vigioApp.controller('baseController', function($scope, $rootScope) {

  $scope.total = 0;

  $scope.tryAdd = function(product) {
    if (!$scope.cart) {
      $scope.cart = angular.fromJson($.cookie('cart'));
      if (!$scope.cart) $scope.cart = [];
    }
    var find = false

    $.each($scope.cart, function() {
      if (this.id == product.id) {
        find = true
        return false
      }
    })
    if (!find) $scope.cart.push(product)
    $scope.saveCart()
    $('html, body').animate({scrollTop:0}, 600, function(){
      $('.service .basket_btn').addClass('active');
      setTimeout(function(){
        $('.cart_list').fadeOut('1000', function() {
          $('.service .basket_btn').removeClass('active');
        });
      }, 2000);
    });
  }

  $scope.saveCart = function(apply) {
    $.cookie('cart', angular.toJson($scope.cart), { expires: 360000, path: '/' });
  }

  $scope.removeItem = function(index) {
    $scope.cart.splice(index, 1);
  }

  $scope.onlyNumber = function(num) {
    num = num * 1
    if (!num) num = 1
    return num
  }

  $scope.calcTotal = function() {
    ret = 0

    $.each($scope.cart, function() {
      ret += this.price*this.count
    })
    total = ret

    $scope.saveCart(true);

    return ret.toFixed(2)
  }

  $scope.productsAmount = function() {
    ret = 0

    $.each($scope.cart, function() {
      ret += this.count
    })


    return ret
  }

  $scope.onSubmit = function() {
    $('#order_form .msg').html('');
    var valid = 1;
    $.each($('#order_form input[type=text], #order_form textarea'), function() {
      if(!$(this).val() && $(this).attr('name') != 'email'){
        valid = 0;
      }
    })
    if(valid){
      if($('#order_form input[name=email]').val() != ''){
        if(!validateEmail($('#order_form input[name=email]').val())){
          valid = 0;
          $('#order_form .msg').html('Некорректный Email');
        }
      };
      if(valid){
        var param = $('#order_form').serialize()

        if ($scope.user.id) {
          param += '&user_id='+$scope.user.id
        }

        param += '&prod='

        $.each($scope.cart, function() {
          var size = '';
          var color = '';
          if(this.size){
            size = this.size;
          }
          if(this.color){
            color = this.color;
          }
          param += this.id+':'+this.count+':'+size+':'+color+','
        })

        $.post('/new_order/', param, function(data) {
          alert('Заказ принят. В ближайшее время с Вами свяжеться менеджер.')
          $scope.cart = [];
          $scope.saveCart();
          $scope.$apply();
        }, 'json')
      };
    }else{
      $('#order_form .msg').html('Заполните обьязательные поля');
    }

  }
  $scope.individualSewingSubmit = function() {
    $('#sewingModal .modal-footer .msg').html('');
    var valid = 1;
    $.each($('#sewingModal input[type=text]'), function() {
      if(!$(this).val() && $(this).attr('name') != 'email'){
        valid = 0;
      }
    })
    if(valid){
      if($('#sewingModal input[name=email]').val() != ''){
        if(!validateEmail($('#sewingModal input[name=email]').val())){
          valid = 0;
          $('#sewingModal .modal-footer .msg').html('Некорректный Email');
        }
      }
      if(valid){
        var param = $('#sewing-form').serialize()
        $.post('/individual-sewing/', param, function(data) {
          $('#sewingModal .modal-body').html('Заказ принят. В ближайшее время с Вами свяжеться менеджер.');
          $('#sewingModal .modal-footer').html('');
        }, 'json')
      }
    }else{
      $('#sewingModal .modal-footer .msg').html('Заполните обязательные поля');
    }
  }
  $scope.contactsSubmit = function() {
    $('#contacts_form .msg').html('');
    var valid = 1;
    $.each($('#contacts_form input[type=text], #contacts_form textarea'), function() {
      if(!$(this).val()){
        valid = 0;
      }
    })
    if(valid){
      if(validateEmail($('#contacts_form input[name=email]').val())){
        var param = $('#contacts_form').serialize()
        $.post('/contacts/', param, function(data) {
          $('.contacts_wrap .form_ttl').html('Сообщение отправлено. В ближайшее время с Вами свяжеться менеджер.');
          $('#contacts_form').remove();
        }, 'json')
      }else{
        $('#contacts_form .msg').html('Некорректный Email');
      }
    }else{
      $('#contacts_form .msg').html('Заполните все поля');
    }
  }

  $scope.trySubmit = function() {
    $scope.form_submited = true;
  }

})

vigioApp.directive('addToCart', function() {
    return function($scope, element, attrs) {
        $(element).find('.add-to-cart-btn').on('click', function() {
          var color = $(element).find('ul.colors li.active').data('color');
          var size = $(element).find('ul.sizes li.active').data('size');
          var count = $(element).find('input[name="pcount"]').val()*1;
          var product = angular.fromJson(attrs.addToCart);
          if (count) {
            product['count'] = count;
          }
          if (color) {
            product['color'] = color;
          }
          if (size) {
            product['size'] = size;
          }
          $scope.tryAdd(product);
          $scope.$apply();
          return false;
        })
        $(element).find('ul.colors li').on('click', function() {
          $(element).find('ul.colors li').removeClass('active');
          $(this).addClass('active');
          prod_thumbs.init();
        })
        $(element).find('ul.sizes li').on('click', function() {
          $(element).find('ul.sizes li').removeClass('active');
          $(this).addClass('active');
        })
    }
})

vigioApp.directive('match', function () {
    return {
        require: 'ngModel',
        restrict: 'A',
        scope: {
            match: '='
        },
        link: function(scope, elem, attrs, ctrl) {
            scope.$watch(function() {
                var modelValue = ctrl.$modelValue || ctrl.$$invalidModelValue;
                return (ctrl.$pristine && angular.isUndefined(modelValue)) || scope.match === modelValue;
            }, function(currentValue) {
                ctrl.$setValidity('match', currentValue);
            });
        }
    };
});

function validateEmail(email) {
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}
