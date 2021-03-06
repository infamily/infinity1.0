// Translation requests

function get_translations() {

	var json = {};

	$('div[id^="source-"]').each(function() {
		 json[this.id] = this.innerHTML;
	});

  $.ajax({
      url : "/ajax/comment-translate/",
      type : "POST",
      data : json,
      success : function(json) {
          for (var key in json) {
            $('#'+key.replace('source','translation')).html(json[key]);
          }
          $('#translation-title').find('h1').css('color','#36648b');
          $('#translation-subtitle').find('h2').css('color','#36648b');
      },
      error : function(xhr,errmsg,err) {
          console.log(xhr.status + ": " + xhr.responseText);
      }
  });
}
