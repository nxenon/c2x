# Client Side Scripts

Client side scripts will be stored in this directory

Web Interface
----

![CreateScript_sc](https://user-images.githubusercontent.com/61124903/127575808-a5fe59ed-32d6-422b-9c0f-45d1f090e752.png)

GUI
----
Using GUI is not recommended.

![Screenshot](https://user-images.githubusercontent.com/61124903/125632382-60309b73-4ced-456e-95b0-64a5f2c015ce.png)

After you have created script it will be in root of project.

Available Languages
----
- Python
- Go

Python
----
    Run the bot_script.py with python3 in target system
    python3 bot_script.py

Go
----
    For go lang you have to first compile the code created
    You have to first install Go version 1.13
    if you want the client to run in
    Linux :
    GOOS=linux go build bot_script.go
    Windows :
    GOOS=windows go build bot_script.go
    now you have c2x-client compiled.
    run it in target system and wait to connect to c2x server


Other instructions for GO client-side script [here](https://github.com/nxenon/c2x-client-go) 
