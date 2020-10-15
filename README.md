## About The Project
This project is about building an API for a personal voice assistant, e.g. a bot in a web conferencing systems which receives a text from the client and responds with a JSON containing pre-defined intents, entities and their confidences. 

In other words if you want an API which can make sense out of the string "Hey my friend <bot_name> mute Christian" and identifies that Christian should be muted here then you are at the right adress here. 

https://nbviewer.jupyter.org/github/Ameckto/voice_assistant_ai_for_conference_systems/blob/main/intent_entity_confidence_test.ipynb

## Table of Contents

* [About the Project](#about-the-project)
* [Installation](#installation)
  * [Prerequisites](#prerequisites)
  * [RASA-NLU](#rasa-nlu)
  * [NGINX](#nginx)
  * [HTTPS-Certificate](#https-certificate)
* [How to use the API](#usage)
* [How to train the model](#train)
* [How to test the model](#test)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)


## Installation

## Prerequisites

In this section I will talk about what you should have to be able to follow this guide and install your own RASA-API server. 

I redommend:

4 CPU-Corese which do have AVX instructions for tensorflow, 
16 GB RAM and 20 GB of SSD for a production server. 

Ubuntu 18.04 and Python 3.6.9 should be installed (Python 3.6.9 is installed on Ubuntu 18.04 by default).

You can check you python version by running:

```sh
python3 --version
```

You should also have pip3 9.0.1 installed.
You can check your pip3 version by running: 
```sh
pip3 --version
```

You can install pip3 by running:
```sh
sudo apt update
sudo apt install python3-pip
```

You can update pip3 by running:
```sh
pip install -U pip
```

This guide will assumes that you need to have the server be accesible over https and not only http and therefore you will need 
your own domain name and be able to point it to the servers public ip adress which you will create here in this guide. 


## RASA-NLU

In this section we will install the RASA package and clone the git repository. 

To install the RASA-NLU package we first create a project folder and a virtual environment to avoid conflicts.  

To create a project folder run:
```sh
mkdir <your_project_name>
```

To move into the folder run: 
```sh
cd <your_project_name>
```

To be able to create a virtual environment in python3 we need to install the fallowing package: 
```sh
sudo apt install python3-venv
```

Now, create a virtual environment (venv) by running: 
```sh
python3 -m venv ./<your_virtual_environment_name>
```

To activate your newly created virtual environment run:
```sh
source ./<your_virtual_environment_name>/bin/activate
```
Keep in mind that you have to be in <your_project_name> folder to activate your venv. 

Now we will install the RASA package by running: 
```sh
pip install rasa
```
After running the above command check the version of RASA by running: 
```sh
rasa --version
```
It should be the version Rasa 1.10.14.

After installing RASA make sure that you are in <your_project_name> folder and clone the git repository by running: 
```sh
git clone https://github.com/Ameckto/voice_assistant_ai_for_conference_systems.git
```

The repository you just downloaded makes usage of the spacy package which is a free open-source library for natural language processing in python. 
Thus you need to install it by running:

```sh
pip install spacy
```

The repository also makes usage of the spacy en_core_web_md pretrained statistical model for english. Download it by running:
```sh
python -m spacy download en_core_web_md
```

You also need to link the model by running: 
```sh
python -m spacy link en_core_web_md en
```

By now, you have installed RASA successfully!  

## NGINX

In this section we will install a NGINX-Webserver which will make it possible to access your server with a public ip adress. 

First we install the NGINX package by running: 
```sh
apt install nginx
```
Now we will unlink the default landing page of the NGNIX server by running: 
```sh
unlink /etc/nginx/sites-enabled/default
```
To link it to our local RASA server we first navigate to the site-variables folder by running: 
```sh
cd /etc/nginx/sites-available
```

Create a new file called reverse-proxy.conf by running: 
```sh
nano reverse-proxy.conf
```

Now copy paste the fallowing code (called Server-Block) and change the line <server_name example.de www.example.de;> accordingly to your domain adress: 
Hint: After pasting save the file by pressing Ctrl + O and exit it after by pressing Ctrl + X

```sh
server {
        listen 80;
        listen [::]:80;
        
        server_name example.de www.example.de;
	      add_header 'Access-Control-Allow-Origin' '*';
  
        access_log /var/log/nginx/reverse-access.log;
        error_log /var/log/nginx/reverse-error.log;

        location / {
                    proxy_pass http://localhost:5000;
  }
}
```

Now stay in the folder and copy the file you just created and edited to the /etc/nginx/sites-enabled folder by running:
```sh
ln -s /etc/nginx/sites-available/reverse-proxy.conf /etc/nginx/sites-enabled/reverse-proxy.conf
```

You can check the syntax of your reverse-proxy.conf file by running: 
```sh
nginx -t
```
Which should be successfull. If so you have installed your NGINX-Webserver successfully. 

## HTTPS-Certificate



//install the certbot
sudo snap install --classic certbot


//ensure that the certbot is working properly
sudo ln -s /snap/bin/certbot /usr/bin/certbot

//get certbot configuring your reverse-proxy.conf file (server block file) automatically
sudo certbot --nginx

//get certbot automatically renew your certificates automatically before they expire
sudo certbot renew --dry-run


//navigate to your voice_assistant_ai_for_conference_systems folder
//start the rasa server with the bigbluebutton model on port 5000
rasa run --enable-api -m models/bigbluebutton.tar.gz -p 5000

//navigate to your example.com domain and enjoy your rasa-server running with the https protocol ready for your post requests
//you can test your sever by curling it on your Ubuntu-Server 

curl localhost:5000/model/parse -d "{\"text\":\"hey big blue button\"}"

//it should return

{
   "intent":{
      "name":"wake_up",
      "confidence":0.531367585
   },
   "entities":[
      
   ],
   "intent_ranking":[
      {
         "name":"wake_up",
         "confidence":0.531367585
      },
      {
         "name":"wake_up+give_presentor",
         "confidence":0.1351553757
      },
      {
         "name":"wake_up+mute",
         "confidence":0.0850125531
      },
      {
         "name":"wake_up+share_first_screen",
         "confidence":0.0763415973
      },
      {
         "name":"out_of_scope",
         "confidence":0.0672892096
      },
      {
         "name":"wake_up+raise_hand",
         "confidence":0.0590120959
      },
      {
         "name":"mute",
         "confidence":0.012295431
      },
      {
         "name":"share_first_screen",
         "confidence":0.01197029
      },
      {
         "name":"raise_hand",
         "confidence":0.0113284591
      },
      {
         "name":"give_presentor",
         "confidence":0.0102274033
      }
   ],
   "text":"hey big blue button"
}


