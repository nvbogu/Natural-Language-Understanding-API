# voice_assistant_ai_for_conference_systems
Personal voice assistant for web conferencing systems using RASA-NLU

git clone https://github.com/Ameckto/voice_assistant_ai_for_conference_systems.git

### Installation 

use python 3.6
```bash
pip install rasa
```

pip install spacy

download the spacy model

python -m spacy download en_core_web_md

link the spacy model 

python -m spacy link en_core_web_md en

go to the folder voice_assistant_ai_for_conference_systems
and run the api at localhost on port 5000

rasa run --enable-api -m models/bigbluebutton.tar.gz -p 5000

-------------------------

Install N
