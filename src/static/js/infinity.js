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
  $("#id_personal").change(function() {$("#div_id_sharewith").toggle(); 
    // Also switch background color to indicate private with grey
    if ($('body').css('background-color') != 'rgb(0, 0, 0)') {
        $('body').css('background-color', '#ffffff');
    }
    if ($("#id_personal").is(":checked")) {
        $('body').css('background-color', '#e0e0e0');
    }
  });

  if ($("#id_personal").is(":checked")) {
    // Show if Personal checkbox is checked
    $('body').css('background-color', '#e0e0e0');
    $("#div_id_sharewith").show();
  }
});

$(function() {
  $("#id_monetary").change(function() {$("#div_id_amount").toggle(); $("#div_id_currency").toggle();});

  if ($("#id_monetary").is(":checked")) {
    // Show if Monetary checkbox is checked
    $("#div_id_amount").show();
    $("#div_id_currency").show();
  }
});

$(function() {
  $("#id_is_link").change(function() {$("#div_id_url").toggle()});

  if ($("#id_is_link").is(":checked")) {
    // Show url box if is_link checkbox is checked
    $("#div_id_url").show();
  }
});

$(function(){

    // Scroll screen horizontally by one screen
    $('#scroll_arrowleft').on("click",function(event){
      $( "div.row-horizon" ).scrollLeft( -$(window).width() );
			event.preventDefault();
    });

    $('#scroll_arrowright').on("click",function(event){
      $( "div.row-horizon" ).scrollLeft( $(window).width() );
			event.preventDefault();
    });
});
