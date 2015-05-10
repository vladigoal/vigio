$(function(){
  if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
   $('header menu>li').on('click', function(){
     if($(this).hasClass('active')){
      $('header menu>li').removeClass('active');
     }else{
       $('header menu>li').removeClass('active');
       $(this).addClass("active");
     }
    })
  }
})
var prod_thumbs = {
  init: function(){
    var color_id = $('.product ul.colors li.active').data('color_id');
    $.each($('.product_wrapper .thumbs .inner li'), function(index, val){
        if($(this).data('color_id') == color_id){
          $(this).removeClass('hide');
          $(this).addClass('show');
        }else{
          $(this).addClass('hide');
          $(this).removeClass('show');
        }
//        $(this).css('top', lookbook.top_pos(index));
    });
    if($('.product_wrapper .thumbs .inner li.show').length == 0){
      $('.product_wrapper .thumbs .inner li').removeClass('hide');
      prod_thumbs.set_current($('.product_wrapper .thumbs .inner li:first'));
    }else{
      prod_thumbs.set_current($('.product_wrapper .thumbs .inner li.show:first'));
    }
    prod_thumbs.listeners();
  },
  listeners: function(){
    $('.product_wrapper .thumbs .inner li').on('click', function () {
      prod_thumbs.set_current($(this));
    })
  },
  set_current: function(obj){
    $('.product_wrapper .thumbs .inner li .current').remove();
    obj.append('<div class="current"></div>');
    $('#zoom01').attr('href', obj.data('image'))
    $('#zoom01 img').attr('src', obj.data('big'))
    $("#zoom01").data("zoom").destroy();
    $('#zoom01').CloudZoom();
  }
}

//string format example: console.log(format('<div style="width: 75%">%0 %1</div>',3, 2))
function format(str){
    for(var i=1;i<arguments.length;i++){str=str.replace('%'+(i-1),arguments[i])}return str
}


var lookbook = {
  width: $(window).width(),
  columns_amount: 4,
  column_width: 25,
  images_amount: 0,
  init: function(amount){
    lookbook.images_amount = amount;
    if(lookbook.images_amount > 0){
      $('.blur_wrap').removeClass('hide');
    }
    if(lookbook.width < 1200){
      lookbook.columns_amount = 3;
      lookbook.column_width = 33.33333333;
    }
    if(lookbook.width < 786){
      lookbook.columns_amount = 2;
      lookbook.column_width = 50;
    }
    lookbook.build_images();
  },
  build_images: function(){
    $( ".lookbook_wrapper a").eq(lookbook.images_amount - 1).find('img').load(function() {
      $.each($(".lookbook_wrapper a"), function(index, val){
        $(this).css('left', lookbook.left_pos(index));
        $(this).css('top', lookbook.top_pos(index));
      });
      lookbook.wrapper_height();
    })
  },
  left_pos: function(index){
    return (index % lookbook.columns_amount) * lookbook.column_width + '%'
  },
  top_pos: function(index){
    if(index > lookbook.columns_amount - 1){
      var obj = $( ".lookbook_wrapper a").eq(index - lookbook.columns_amount);
      return obj.position().top + obj.height();
    }else{
      return 0;
    }
  },
  wrapper_height: function(){
    if(lookbook.images_amount > 6){
      var last_line_image = $( ".lookbook_wrapper a").slice(lookbook.images_amount - 6, lookbook.images_amount);
      var lower_pos = 0;
      $.each(last_line_image, function(index, val){
        var obj = $( ".lookbook_wrapper a").eq(lookbook.images_amount - 6 + index);
        if(obj.position().top + obj.height() > lower_pos){
          lower_pos = obj.position().top + obj.height();
        }
      })
      $('.lookbook_wrapper').height(lower_pos);
    }
    $('.blur_wrap').addClass('hide');
  }
}