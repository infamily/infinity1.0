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
          console.log(json);
          for (var key in json) {
            $('#'+key.replace('source','translation')).html(json[key]);
            console.log(key + ' -> ' + json[key]);
          }
      },
      error : function(xhr,errmsg,err) {
          console.log(xhr.status + ": " + xhr.responseText);
      }
  });
}
