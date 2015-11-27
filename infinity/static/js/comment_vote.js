// VOTING logic
// Submit post on submit

function send_vote(json) {
  $.ajax({
      url : "/ajax/comment-vote/",
      type : "POST",
      data : json,
      success : function(json) {
          console.log(json);
          var thumb_up_id = "thumb-up-".concat(json.comment_id);
          var thumb_down_id = "thumb-down-".concat(json.comment_id);
          var total_votes_id = "total-votes-".concat(json.comment_id);
          if (json.value == 0) {
            console.log('voting result: 0');
            document.getElementById(thumb_up_id).className = "fa fa-thumbs-o-up";
            document.getElementById(thumb_down_id).className = "fa fa-thumbs-o-down";
            document.getElementById(total_votes_id).innerHTML = json.total;
          }
          else if (json.value == 1) {
            console.log('voting result: 1');
            document.getElementById(thumb_up_id).className = "fa fa-thumbs-up";
            document.getElementById(thumb_down_id).className = "fa fa-thumbs-o-down";
            document.getElementById(total_votes_id).innerHTML = json.total;
          }
          else if (json.value == -1) {
            console.log('voting result: -1');
            document.getElementById(thumb_up_id).className = "fa fa-thumbs-o-up";
            document.getElementById(thumb_down_id).className = "fa fa-thumbs-down";
            document.getElementById(total_votes_id).innerHTML = json.total;
          }
          else {
            console.log('sanity check: voting result: UNKNOWN');
          }
          console.log("success");
      },
      error : function(xhr,errmsg,err) {
          console.log(xhr.status + ": " + xhr.responseText);
      }
  });
}

// CSFR protection
// This function gets cookie with a given name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

/*
The functions below will create a header with csrftoken
*/

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
