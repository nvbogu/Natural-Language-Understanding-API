## About The Project
This project is about building an API for a personal voice assistant, e.g. a bot in web conferencing systems which receives a text from the client and responds with a JSON file containing pre-defined intents, entities and their confidences. 

In other words if you want an API which can make sense out of the string "Hey my friend <bot_name> mute Christian" and identifies that Christian should be muted here then you are at the right address. 


## Table of Contents

* [Installation](#installation)
  * [Prerequisites](#prerequisites)
  * [RASA](#rasa)
  * [NGINX](#nginx)
  * [HTTPS-Certificate](#https-certificate)
* [How to start the API](#how-to-start-the-API)
* [How to train the model](#How-to-train-the-model)
* [How to test the model](#How-to-test-the-model)
* [License](#license)


## Installation

In this section you will install and configure everything what is necessary to run a web server (with an https protocol) which acts like a proxy server and points to a local RASA-Server. 
Rasa Open Source is a machine learning framework to automate text- and voice-based assistants.

## Prerequisites

In this section I will talk about what you should have to be able to follow this guide and install your own RASA-API server. 

I recommend:

4 CPU-Corese which do have AVX instructions for Tensorflow, 
16 GB RAM and 20 GB of SSD for a production server. 

Ubuntu 18.04 and Python 3.6.9 should be installed (Python 3.6.9 is installed on Ubuntu 18.04 by default).

You can check you Python version by running:

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

This guide assumes that you need to have the server be accesible over https and not only http and therefore you will need 
your own domain name and be able to point it to the servers public ip address. In this guide you will create the server.


## RASA

In this section we will install the RASA package and clone the Git repository. 

To install the RASA package we first create a project folder and a virtual environment to avoid conflicts.  

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

After installing RASA make sure that you are in <your_project_name> folder and clone the Git repository by running: 
```sh
git clone https://github.com/Ameckto/voice_assistant_ai_for_conference_systems.git
```

The repository you just downloaded makes usage of the Spacy package which is a free open-source library for Natural Language Processing in Python.
Thus you need to install it by running:

```sh
pip install spacy
```

The repository also makes usage of the Spacy en_core_web_md pretrained statistical model for English. Download it by running:
```sh
python -m spacy download en_core_web_md
```

You also need to link the model by running: 
```sh
python -m spacy link en_core_web_md en
```

By now, you have installed RASA successfully!  

## NGINX

In this section we will install a NGINX web server which will make it possible to access your server with a public ip adress. 

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

Now copy paste the fallowing code (called server block) and change the line <server_name example.de www&#58.example.de;> accordingly to your domain adress: 
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
I this section we will make https for your domain name and alter automatically your NGINX configuration. 

First we will use the classic certbot package. You can install it by running:

```sh
sudo snap install --classic certbot
```

To ensure that the certbot is working properly run: 
```sh
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```
Now we will use the certbot to deploy the certificate (which uses the "Let's Encrypt" service) for your name server and enable https.
You will need to fallow a dialogue. The certbot also change your reverse-proxy.conf accordingly. 
```sh
sudo certbot --nginx
```


To get the certbot automatically renew your certificates before they expire run:
```sh
sudo certbot renew --dry-run
```

Now you should have enabled accessing your name server over https!

## How to start the API

In this section you will make the server running and waiting for your requests. 

First navigate to your project folder:

```sh
cd <your_project_name>
```

Activate your venv by running: 
```sh
source ./<your_virtual_environment_name>/bin/activate
```

Now navigate to your repository folder by running:
```sh
cd voice_assistant_ai_for_conference_systems
```

Start the rasa server with the bigbluebutton (which is a open source web conferencing software) model on port 5000
```sh
rasa run --enable-api -m models/bigbluebutton.tar.gz -p 5000
```
Hint: You can stop the server by pressing Ctrl + c

Your NGNIX Server should run be default. If not you can get the current status by running: 
```sh
sudo systemctl status nginx
```

Stop the server by running: 
```sh
sudo systemctl stop nginx
```

Start the server by running: 
```sh
sudo systemctl start nginx
```
Hint: You need to open a new shell if you started your RASA-Server within the current shell to be able to do something different than watching the RASA-Server running on http://localhost:5000. 

Now you can navigate to your example.com domain and enjoy your rasa-server running with the https protocol ready for your requests.

You can also test it on your ubuntu machine by curling it by running: 

```sh
curl localhost:5000/model/parse -d "{\"text\":\"hey big blue button mute Steffen please\"}"
```

Which should return 

{"intent":{"name":"wake_up+mute","confidence":0.3771627578},"entities":[{"entity":"PERSON","start":25,"end":32,"confidence_entity":0.8901095716,"value":"Steffen","extractor":"CRFEntityExtractor"},{"entity":"PERSON","value":"Steffen","start":25,"confidence":null,"end":32,"extractor":"SpacyEntityExtractor"}],"intent_ranking":[{"name":"wake_up+mute","confidence":0.3771627578},{"name":"wake_up+give_presenter","confidence":0.17544354},{"name":"wake_up","confidence":0.0876565409},{"name":"wake_up+out_of_scope","confidence":0.0771458429},{"name":"out_of_scope","confidence":0.074283539},{"name":"wake_up+summarize","confidence":0.0429107613},{"name":"wake_up+raise_hand","confidence":0.0404340016},{"name":"wake_up+share_screen","confidence":0.0355202072},{"name":"mute","confidence":0.0290603673},{"name":"give_presenter","confidence":0.0201405552}],"text":"hey big blue button mute Steffen please"}


## How to train the model

In this section you will learn how quickly you can change the training data and change the entity extractor pipeline and fit the model to your needs.

Activate your virtual environment and move to the repository folder (explained above).

To train a model run: 

```sh
rasa train nlu
```

This creates a new model which is stored in the model folder. The data used to train the model is stored in the nlu.md file which is located in the data folder. 
You can just change the data and re-run the above command to train your model. 

You can make your API Server to use your model by altering the rasa run command:   

```sh
rasa run --enable-api -m models/<your_model_name> -p 5000
```

It is really that simple!



## How to test the model

In this section I will give you an example how you can test your model in python jupyter notebook. 
I used a local RASA server and Windows for this purpose. You can also use another operating system and your public accessible RASA-Server as well but you need to change the server address accordingly. 

The testfile is located at:

```sh
voice_assistant_ai_for_conference_systems/tests/intent_entity_confidence_test.ipynb
```
Hint: If GitHub says: "Sorry" you can view the file here: https://nbviewer.jupyter.org/github/Ameckto/voice_assistant_ai_for_conference_systems/blob/main/tests/intent_entity_confidence_test.ipynb

The test file sends pre-defined use-cases to the RASA-Server and evalutes the reponses. It also prints charts to find a good min_confidence value which can filter out wrong results (hopefully). 



## License

Feel free to use my code. 

