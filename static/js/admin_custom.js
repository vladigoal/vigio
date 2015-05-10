//(function($) {
//	$(document).ready(function($) {
//
//	  $('select#id_collection').change(function(){
//      get_category('collection', 'gender', $(this).val());
//    })
//
//    $('select#id_gender').change(function(){
//      get_category('category', 'gender',
//        $(this).val());
//    })
//
//    function get_category(param_name, result_name, value){
//      var params = {}
//      params[param_name] = value
//
//      var url = format("/admin-filter/%0/", result_name);
//      $('select#id_category').html('<option value="">Фильтрация</option>');
//      $.get(url, params, function(res){
//        $('select#id_category').html('<option value="">---------</option>');
//          $.each(res[result_name], function(index, val){
//            $('select#id_category').append(format('<option value="%0">%1</option>', val.id, val.name))
//          })
//      })
//    }
//	});
//})(django.jQuery.noConflict());
//
////string format example: console.log(format('<div style="width: 75%">%0 %1</div>',3, 2))
//function format(str){
//    for(var i=1;i<arguments.length;i++){str=str.replace('%'+(i-1),arguments[i])}return str
//}