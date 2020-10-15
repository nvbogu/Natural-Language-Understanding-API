## About The Project
This project is about building an API for a personal voice assistant, e.g. a bot in a web conferencing systems which receives a text from the client and responds with a JSON containing pre-defined intents, entities and their confidences. 

In other words if you want an API which can make sense out of the string "Hey my friend <bot_name> mute Christian" and identifies that Christian should be muted here then you are at the right adress here. 

https://nbviewer.jupyter.org/github/Ameckto/voice_assistant_ai_for_conference_systems/blob/main/intent_entity_confidence_test.ipynb

## Table of Contents

* [About the Project](#about-the-project)
* [Installation](#installation)
    *[Prerequisites](#prerequisites)
    *[RASA-NLU](#rasa-nlu)
    *[NGINX](#nginx)
    *[HTTPS-Certificate](#https-certificate)
* [How to use the API](#usage)
* [How to train the model](#train)
* [How to test the model](#test)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)


## Installation

## Prerequisites

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

You can update you pip3 version by running:
```sh
sudo apt update
sudo apt install python3-pip
```




## RASA-NLU

## NGINX
## HTTPS-Certificate


Use a virtual environment with python 3.6 on Ubuntu 16.04

```bash
//Clone the git repository
git clone https://github.com/Ameckto/voice_assistant_ai_for_conference_systems.git

//install rasa (it automatically installs all package dependencies)
pip install rasa

//install language model package
pip install spacy

//donwload the used model
python -m spacy download en_core_web_md

//link the used model 
python -m spacy link en_core_web_md en

//install nginx (webserver)
apt install nginx

//unlink the default virtual host
unlink /etc/nginx/sites-enabled/default

//navigate to the site-variables folder where we create a reverse proxy configuration file
cd /etc/nginx/sites-available

//create a new file called reverse-proxy.conf
nano reverse-proxy.conf

//copy paste the fallowing code (called Server-Block)
//before change the line <server_name example.de www.example.de;> accordingly to your domain
//errors will be located at: /var/log/nginx
//after pasting save the file by pressing Ctrl + O and exit it after by pressing Ctrl + X

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

//no copy the file to /etc/nginx/sites-enabled
ln -s /etc/nginx/sites-available/reverse-proxy.conf /etc/nginx/sites-enabled/reverse-proxy.conf

//check syntax of your reverse-proxy.conf file
nginx -t

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


