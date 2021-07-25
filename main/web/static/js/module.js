var last_text_server = "";
var last_text_create_script = "";

$(document).on('submit', "#server_conf_form",function( event ) {
    event.preventDefault();
});

$(document).on('submit', "#create_script_conf_form",function( event ) {
    event.preventDefault();
});

var page_path = window.location.pathname;
if (page_path === "/server") {
    getServerConf()
}
if (page_path === '/create_script') {
    getCreateScriptResp()
}

function getServerConf(){
    // get server conf and put it in /server url bottom div

    $('.stop_server_event').removeAttr('disabled');

    var url = $("#server_conf_form").attr('action');

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.send();
    setInterval(function() {
        insertText(xhr.responseText);
    }, 1000);

}

function insertText(text) {

    if (last_text_server !== text) {
        last_text_server = text;
        $('.server_conf_response').html(last_text_server);
   }

}

$(document).on("click", ".stop_server_event", function( event ) {

    var url = $("#server_conf_form").attr('action') + "_stop";
    var method = $("#server_conf_form").attr('method');

    $.ajax({
        url: url,
        method: method,
        data: {"stop_server":"True"},
        success: function(r) {
        }
        })

    })

$(document).on("click", ".start_server_event", function( event ) {

    var url = $("#server_conf_form").attr('action') + "_start";
    var method = $("#server_conf_form").attr('method');
    var lip = $("#lip").val();
    var lport = $("#lport").val();

    if (lip === "") {
        alert("Listening IP is required");
        return;
    }
    else if (lport === "") {
        alert("Listening port is required");
        return;
    }

    $.ajax({
        url: url,
        method: method,
        data: {"lip":lip ,"lport":lport},
        success: function(r, jqXHR, textStatus, errorThrown) {
        }
        })

    })

function insertTextInCS(text) {

    if (last_text_create_script !== text) {
        last_text_create_script = text;
        $('.server_create_script_response').html(last_text_create_script);
   }

}

function getCreateScriptResp(){
    // get create script resp and put it in /create_script url bottom div

    var url_cs = $("#create_script_conf_form").attr('action');
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url_cs, true);
    xhr.send();
    setInterval(function() {
        insertTextInCS(xhr.responseText);
    }, 1000);

}

$(document).on("click", ".event_create_script", function( event ) {

    var url_cs = $("#create_script_conf_form").attr('action') + "_create";
    var method_cs = $("#create_script_conf_form").attr('method');
    var localhost_createscript = $("#localhost_create_script").val();
    var localport_createscript = $("#localport_create_script").val();
    var lang_create_script = $('.create_script_lang').val();

    if (localhost_createscript === "") {
        alert("LHost is required");
        return;
    }
    else if (localport_createscript === "") {
        alert("LPort is required");
        return;
    }
    else if (lang_create_script === "") {
        alert("Language cannot be empty");
        return;
    }

    $.ajax({
        url: url_cs,
        method: method_cs,
        data: {"localhost":localhost_createscript ,
            "localport":localport_createscript ,
            "lang_create_script":lang_create_script},
        success: function(r) {
        }

    })

});
