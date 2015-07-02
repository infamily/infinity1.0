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
    $.ajax({
        url: '.',
        data: data,
        dataType: 'jsonp',
        jsonp: 'callback',
        jsonpCallback: 'searchResult',
    });
}


function searchResult(data) {
    if (data && data[0] && typeof data[0] != 'string') {
        showProposals(data[0]);
        data.splice(0,1);
    } else {
        $('.hint').remove();
    }
    $("#id_name").autocomplete ({
        source: data
    });
    /*
    if (data) {
        $('#id_definition')[0].className = 'textinput textInput form-control';
        $('#id_definition')[0].type = 'text';
        $('.create-button')[0].className = 'col-xs-2 create-button';
    }
    */
}


function showProposals(data) {
    $('.hint').remove();
    var definitionsBlock = $(".hints-block")[0];
    data.forEach(function(entry) {
        definitionsBlock.insertAdjacentHTML(
            'afterend', '<div class="row hint form-group"><div class="col-xs-10"><p class="hint-text">' + entry[0] + 
            '</p></div><div class="col-xs-2"><a class="btn btn-primary choose-need" href="' + entry[1] + '">Choose</a></div></div>'
        );
    });
    definitionsBlock.insertAdjacentHTML('afterend', '<div align="center" class="row hint form-group"><b>Did you mean?</b></div>');
}


$(document).ready(function() {
    document.getElementById('id_language').value = getCookie('infinity_search_lang') || 1322;
    $('#id_language').bind('input', function() { 
        setCookie('infinity_search_lang', $(this).val(), 365);
        searchOpen($('#id_name').val(), $(this).val());
    });
    searchResult()
    $("#id_name").bind("autocompleteselect", function(event, ui) {
        searchOpen(ui.item.value, $('#id_language').val());
    });
});
