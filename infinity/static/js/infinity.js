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
  var id_personal_checked = $("#id_personal").prop('checked', true);

  if (id_personal_checked) {
    // Show if Personal checkbox is checked
    $("#div_id_sharewith").show();
  }
});
