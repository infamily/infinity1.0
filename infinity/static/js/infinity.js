/* Project specific Javascript goes here. */

try{
  setTimeout(function(){
    if($ && $.fn && $.fn.select2){
      $.fn.select2.defaults.allowClear = true;  
    }
  },
  300)
}catch(e){}

$(function() {
  $("#id_personal").change(function() {$("#div_id_sharewith").toggle()});
});
