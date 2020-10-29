## About this project
This project is about building an API for a personal assistant, e.g. a bot in web conferencing systems which receives a text from the client and responds with a JSON containing pre-defined intents, entities and their confidences. 

In other words if you want an API which can make sense out of the string *"Hey my friend <bot_name> mute Christian for me please"* and identifies that Christian should be muted here then you are at the right address. 

The provided model is capable of identifying the following intents:

| Intent         | Example                | Entities identified |
|----------------|------------------------|---------------------|
| wake_up        | hey big blue button    |                     |
| mute           | mute Hoa and Niklas    | Hoa, Niklas         |
| summarize      | summarize the meeting  |                     |
| give_presenter | give Mike presenter    | Mike                |
| share_screen   | share my screen please |                     |
| raise_hand     | raise my hand          |                     |
| out_of_scope   | I don't like it here   |                     |

It is also capable of identifying multiple intents if one of them is a wake_up intent like wake_up+mute, wake_up+share_screen etc.
It it is very simple to train a model with your own data to meet your individual neets. I have described it in the [How to train the model](#How-to-train-the-model) section.

Although this is a standalone project it is used by the [Personal-Voice-and-Chat-Assistant-within-bigbluebutton](https://github.com/nvbogu/Personal-Voice-and-Chat-Assistant-within-bigbluebutton) project where the [bigbluebutton](https://github.com/bigbluebutton) (open source web conferencing) application is altered in order to bring a personal voice assistant to live and useable.


## Table of contents

* [Installation](#installation)
  * [Prerequisites](#prerequisites)
  * [RASA](#rasa)
  * [NGINX](#nginx)
  * [HTTPS certificate](#https-certificate)
* [How to start the API](#how-to-start-the-API)
* [How to train the model](#How-to-train-the-model)
* [How to test the model](#How-to-test-the-model)
* [License](#license)


## Installation

In this section you will install and configure everything what is necessary to run a web server (with an https protocol) which acts like a proxy server and points to a local RASA server. 
[Rasa Open Source](https://rasa.com/) is a machine learning framwork to automate text- and voice-based assistants.

## Prerequisites

In this section I will talk about what you should have to be able to follow this guide and install your own RASA API server. 

I recommend:

4 CPU cores which are capable to execute AVX instructions for Tensorflow, 
16 GB RAM and 20 GB of SSD storage for a production server. 

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
your own domain name and be able to point it to the servers public ip address. In this guide you will only create the server and not buy a domain name and not link your domain name to your server.


## RASA

In this section you will install the RASA package and clone the Git repository. 

To install the RASA package first create a project folder and a virtual environment to avoid conflicts.  

To create a project folder run:
```sh
mkdir <your_project_name>
```

To move into the folder run: 
```sh
cd <your_project_name>
```

To be able to create a virtual environment in python3 you need to install the fallowing package: 
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
`Hint`: Keep in mind that you have to be in <your_project_name> folder to activate your venv. 

Now install the RASA package by running: 
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
git https://github.com/nvbogu/Natural-Language-Understanding-API.git

```

The repository you just downloaded makes usage of the Spacy package which is a free open source library for Natural Language Processing in Python.
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

In this section you will install a NGINX web server which will make it possible to access your server with a public ip adress. 

First install the NGINX package by running: 
```sh
apt install nginx
```
Now unlink the default landing page of the NGNIX server by running: 
```sh
unlink /etc/nginx/sites-enabled/default
```
To link it to our local RASA server first navigate to the site-variables folder by running: 
```sh
cd /etc/nginx/sites-available
```

Create a new file called reverse-proxy.conf by running: 
```sh
nano reverse-proxy.conf
```

Now copy paste the fallowing code (called server block) and change the line <server_name example.de www<i></i>.example.de;> accordingly to your domain address: 

`Hint`: After pasting save the file by pressing Ctrl + O and exit it after by pressing Ctrl + X

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
Which should be successfull. If so you have installed your NGINX web server successfully!

## HTTPS certificate
I this section you will get a certificate from [Let's Encript](https://letsencrypt.org/) which is for free and makes your server accessible over the https protocol.
You also alter your NGINX configuration (automatically). 

First you will use the classic certbot package. You can install it by running:

```sh
sudo snap install --classic certbot
```

To ensure that the certbot is working properly run: 
```sh
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```
Now you will use the certbot to deploy the certificate for your name server and enable https.
You will need to fallow a dialogue. The certbot also changes your reverse-proxy.conf file accordingly. 
```sh
sudo certbot --nginx
```


To get the certbot automatically renew your certificates before they expire run:
```sh
sudo certbot renew --dry-run
```

Now your NGINX web server should be automatically accessible over https.  

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
cd Natural-Language-Understanding-API
```

Start the RASA server with the bigbluebutton (which is a open source web conferencing software) model on port 5000
```sh
rasa run --enable-api -m models/bigbluebutton.tar.gz -p 5000
```
`Hint`: You can stop the server by pressing Ctrl + c

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
`Hint`: You need to open a new shell if you started your RASA server within the current shell to be able to do something different than watching the RASA server running on http:<i></i>//localhost:5000. 

Now you can navigate to your <example.com> domain and enjoy your rasa server running with the https protocol ready for your requests.

You can also test it on your ubuntu machine by curling it by running: 

```sh
curl localhost:5000/model/parse -d "{\"text\":\"hey big blue button mute Steffen please\"}"
```

Which should return:

{"intent":{"name":"wake_up+mute","confidence":0.3771627578},"entities":[{"entity":"PERSON","start":25,"end":32,"confidence_entity":0.8901095716,"value":"Steffen","extractor":"CRFEntityExtractor"},{"entity":"PERSON","value":"Steffen","start":25,"confidence":null,"end":32,"extractor":"SpacyEntityExtractor"}],"intent_ranking":[{"name":"wake_up+mute","confidence":0.3771627578},{"name":"wake_up+give_presenter","confidence":0.17544354},{"name":"wake_up","confidence":0.0876565409},{"name":"wake_up+out_of_scope","confidence":0.0771458429},{"name":"out_of_scope","confidence":0.074283539},{"name":"wake_up+summarize","confidence":0.0429107613},{"name":"wake_up+raise_hand","confidence":0.0404340016},{"name":"wake_up+share_screen","confidence":0.0355202072},{"name":"mute","confidence":0.0290603673},{"name":"give_presenter","confidence":0.0201405552}],"text":"hey big blue button mute Steffen please"}


## How to train the model

In this section you will learn how quickly you can change the training data and change the entity extractor pipeline thus your model running on the rasa server will meet your individual needs.

Activate your virtual environment and move to the repository folder (explained above).

To train a model run: 

```sh
rasa train nlu
```

This creates a new model which is stored in the model folder. The data used to train the model is stored in the nlu.md file which is located in the data folder. 
You can just change the data and re-run the above command to train your own model. 
Althow training the model is pretty straight forward please visit the [official rasa documentation](https://rasa.com/docs/rasa/nlu-training-data/) for more details. 



You can make your API Server to use your own model by altering the rasa run command:   

```sh
rasa run --enable-api -m models/<your_model_name> -p 5000
```

It is really that simple!

`Hint`: You can access the models pipeline by opening the config.yml file. I have reduced the dimensions of the SpacyEntityExtractor to ["PERSON"] which let the extractor only be able to extract persons. Delete this line if you also want to identify other entities e.g. organisations. 
    

## How to test the model

In this section I will give you an example how you can test your model in Python Jupyter Notebook. 
I used a local RASA server and Windows for this purpose. You can also use another operating system and your public accessible RASA server as well but you need to change the server address accordingly in the intent_entity_confidence_test.ipynb file. 

The testfile is located at:

```sh
Natural-Language-Understanding-API/tests/intent_entity_confidence_test.ipynb
```

`Hint`: If GitHub says: *"Sorry"* , you can view the file here: https://nbviewer.jupyter.org/github/nvbogu/Natural-Language-Understanding-API/blob/main/tests/intent_entity_confidence_test.ipynb

The test file sends pre-defined use cases to the RASA server and evalutes the reponses. It also prints charts to find a good min_confidence value which can filter out wrong results (hopefully). 

You can simply add more or other use cases by altering the according dictionaries and re-run the script. 


## License

This project is open source for everyone. 

