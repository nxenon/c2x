# C2X

[![Tool Category](https://badgen.net/badge/Tool/Post%20Exploitation/black)](https://github.com/nxenon/c2x)
[![APP Version](https://badgen.net/badge/Version/Beta/red)](https://github.com/nxenon/c2x)
[![Python Version](https://badgen.net/badge/Python/3.x/blue)](https://www.python.org/download/releases/3.0/)
[![License](https://badgen.net/badge/License/GPLv2/purple)](https://github.com/nxenon/c2x/blob/master/LICENSE)

C2X is a C2/Post-Exploitation Framework for Red Teaming and Ethical Hacking.

Screenshots
----
![Screenshot](https://user-images.githubusercontent.com/61124903/127577653-92b93102-1e06-413e-baa3-6e1bb3a6110a.png)

![Screenshot_terminal](https://user-images.githubusercontent.com/61124903/127780339-bc852540-919b-4977-a257-d037731fad5d.png)

Installation
----
    git clone https://github.com/nxenon/c2x.git
    cd c2x
    pip3 install -r requirements.txt
    
Usage
----
    python3 c2x.py --web [recommended option]
    or
    python3 c2x.py --gui [is not recommended]
    --gui will be removed in newer versions of C2X

Web Interface [Recommended]
----

[Web README and Screenshots](https://github.com/nxenon/c2x/blob/main/main/web/README.md)

Client Side
----
You need some instructions for running client side codes after creating your scripts:

[Client Side README](https://github.com/nxenon/c2x/blob/main/modules/client-side/README.md)

GUI Interface [Not Recommended]
----

[GUI README and Screenshots](https://github.com/nxenon/c2x/blob/main/main/gui/README.md)

Help
----
      .oooooo.     .oooo.   oonoooo  ooooo
     d8P'  `Y8b  .dP""Y88b   `8x88    d8'
    888                ]8P'    Ye88..8P
    888              .d8P'      `8n88'
    888            .dP'        .8PYo88.       {version : Beta}
    `88b    ooo  .oP     .o   d8'  `n88b      https://github.com/nxenon/c2x
     `-nxenon-'  8888888888 o888o  o88888o
    
    usage: python3 c2x.py --web or --gui
     help: python3 c2x.py --help
      Web: python3 c2x.py --web
      GUI: python3 c2x.py --gui
    
    optional arguments:
      -h, --help   show this help message and exit
      --gui        Start GUI Window
      --web        Start Web Interface
      --use-https  Enable HTTPS for Web Interface

Configuration
----
All of project configuration params are in main/core/config.json file which you can change them.

[config.json](https://github.com/nxenon/c2x/blob/main/main/core/config.json)
