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

  if ($("#id_personal").is(":checked")) {
    // Show if Personal checkbox is checked
    $("#div_id_sharewith").show();
  }
});
