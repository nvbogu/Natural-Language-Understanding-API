# voice_assistant_ai_for_conference_systems
Personal voice assistant for web conferencing systems using RASA-NLU



### Installation 

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
nano reverse-proxy.conf


//enter the fallowing code (called Server-Block)
//change the 

server {
        listen 80;
        listen [::]:80;
        
        server_name niklasproject.de www.niklasproject.de;
	      add_header 'Access-Control-Allow-Origin' '*';
  
        access_log /var/log/nginx/reverse-access.log;
        error_log /var/log/nginx/reverse-error.log;

        location / {
                    proxy_pass http://localhost:5000;
  }
}


```




go to the folder voice_assistant_ai_for_conference_systems
and run the api at localhost on port 5000

rasa run --enable-api -m models/bigbluebutton.tar.gz -p 5000

-------------------------

Install N
