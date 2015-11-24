function setCookie(c_name,value,exdays) {
    var exdate=new Date();
    exdate.setDate(exdate.getDate() + exdays);
    var c_value=escape(value) + ((exdays==null) ? "" : ";path=/;expires="+exdate.toUTCString());
    document.cookie=c_name + "=" + c_value;
}


function getCookie(c_name) {
    var i,x,y,ARRcookies=document.cookie.split(";");
    for (i=0;i<ARRcookies.length;i++) {
        x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
        y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
        x=x.replace(/^\s+|\s+$/g,"");
        if (x==c_name) {
            return unescape(y);
        }
    }
}


function searchOpen(name, language) {
    var name = name || $('#id_name').val();
    var language = language || $('#id_language').val();
    var data = {
        name: name,
        language: language,
    };
    console.log(name);
    $.ajax({
        url: '.',
        data: data,
    }).success(function(data){
        searchResult(data);
    });
}


function searchResult(data) {
    if(!$('#id_language').val()) {
        var language = window.navigator.userLanguage || window.navigator.language;
        $.ajax({
            url: ".",
            data: {
                'find_language': language
            },
        }).done(function(lang_pk) {
            document.getElementById('id_language').value = lang_pk;
        });
    };
    console.log(data);
    if (data && data[0]) {
        console.log('show', data)
        showProposals(data);
    } else {
        $('.hint').remove();
        console.log('remove')
    };
}


function showProposals(data) {
    $('.hint').remove();
    var definitionsBlock = $(".hints-block")[0];
    data.forEach(function(entry) {
        definitionsBlock.insertAdjacentHTML(
            'afterend', '<div class="row hint form-group"><div class="col-sm-10"><p class="hint-text">' + entry[0] +
            '</p></div><div class="col-sm-2"><a class="btn btn-primary choose-definition" style="color:white;" href="' + entry[1] + '">y</a></div></div>'
        );
    });
    // definitionsBlock.insertAdjacentHTML('afterend', '<div align="center" class="row hint form-group"><b>Did you mean?</b></div>');
}


$(document).ready(function() {
    document.getElementById('id_language').value = getCookie('infinity_search_lang');
    $('#id_language').bind('input', function() {
        setCookie('infinity_search_lang', $(this).val(), 365);
        searchOpen($('#id_name').val(), $(this).val());
    });
    var delay = (function(){
        var timer = 0;
        return function(callback, ms){
            clearTimeout (timer);
            timer = setTimeout(callback, ms);
        };
    })();
    $('#id_name').bind('input', function() { 
        searchOpen();
    });
    searchResult()
});


function redirectIndex(seconds) {
    var refresh,       
        intvrefresh = function() {
            clearInterval(refresh);
            refresh = setTimeout(function() {
              if (!$("#id_name").val()) {
                 location.href = '/w';
              }
            }, seconds * 1000);
        };

    $(document).on('keypress click', function() { intvrefresh() });
    intvrefresh();

}


$(function() {
    $("#id_name").keyup(function() {

    if ($("#id_name").val()) {
      $("#div_id_define").show();
    }
    else {
      $("#div_id_define").hide();
      redirectIndex(15);
    }

    });
});

$( document ).ready(function() {
	$("#id_name").focus();
	redirectIndex(15);
});


