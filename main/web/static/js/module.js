var last_text_server = "";

$(document).on('submit', "#server_conf_form",function( event ) {
  event.preventDefault();
});

function getServerConf(){
    // get server conf and put it in /server url bottom div

    $('.stop_server_event').removeAttr('disabled')

    var url = $("#server_conf_form").attr('action')

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.send();
    setInterval(function() {
        insertText(xhr.responseText);
    }, 500);

}

function insertText(text) {

    if (last_text_server != text) {
        last_text_server = text
        $('.server_conf_response').html(last_text_server);
   }

}

$(document).on("click", ".start_server_event", function( event ) {

    var url = $("#server_conf_form").attr('action')
    var method = $("#server_conf_form").attr('method')
    var lip = $("#lip").val()
    var lport = $("#lport").val()

    if (lip == "") {
        alert("Listening IP is required")
        return
    }
    else if (lport == "") {
        alert("Listening port is required")
        return
    }

    $.ajax({
        url: url,
        method: method,
        data: {"lip":lip ,"lport":lport},
        success: function(r, jqXHR, textStatus, errorThrown) {
        }

    })

    getServerConf();

});
