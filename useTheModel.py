# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 21:37:33 2020

@author: Niklas
"""

from rasa.nlu.model import Interpreter

interpreter = Interpreter.load('models/nlu')

#interpreter.parse("hey bbb")

result = interpreter.parse("hey bbb mute Steffen")

intent = result.get("intent")
entities = result.get("entities")[0]['value']
intent = result.get("intent")