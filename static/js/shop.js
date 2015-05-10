$(function(){
  filters.init();

  $('.product_wrapper .add_info .ttl').on('click', function(){
    if($(this).parent().find('.info').height() > 0){
      var h = '0';
    }else{
      var h = $(this).parent().find('.inside').height();
    }
    $(this).parent().find('.info').animate({
      height: h
    }, 500);
    return false;
  })

  $('.individual_sewing').on('click', function(event) {
    event.preventDefault();
    $('#sewingModal').modal()        
  });

  $('.sizes_table').on('click', function(event) {
    event.preventDefault();
    $('#sizesModal').modal()        
  });

})

var filters = {
  params: [],
  init: function(){
    filters.listeners();
    var url_params = window.location.href.split('?');
    var key_val = '';
  },
  listeners: function(){

    $('.filter_btn').on('click', function(){
      var start_price = $('input[name="start_price"]').val();
      var fin_price = $('input[name="fin_price"]').val();
      var sizes = [];
      if(filters.isInt(start_price) && start_price != '')
        filters.add_param('start_price='+start_price);
      if(filters.isInt(fin_price)  && fin_price != '')
        filters.add_param("fin_price="+fin_price);
      $.each($('.filters .sizes .item'), function(index, value) {
        var obj = $(this).find('input');
        if(obj.is(':checked')){
          sizes.push(obj.val());
        }
      })
      console.log('sizes=', sizes)
      if(sizes.length > 0) filters.add_param('sizes='+sizes);
      var url = '';
      $.each(filters.params, function(index, value) {
        if(index == 0){
          url += format('/shop/?%0', value);
        }else{
          url += format('&%0', value);
        }
      })
      window.location.href = url;
      return false;
    })
  },
  add_param: function(param){
    filters.params.push(param);
  },
  isInt: function (n){
    return !isNaN(parseInt(n * 1))
  }
}
