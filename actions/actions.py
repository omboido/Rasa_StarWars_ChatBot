# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import sys
import requests
import json
import re

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset


def search_person(person):
    
    r = requests.get('https://swapi.dev/api/people/?search={0}'.format(person))
    
    return r.json()['results'][0]


def translate_olhos(cor : str):
  cor = cor.replace('blue','azuis')
  cor = cor.replace('yellow','amarelos')
  cor = cor.replace('red','vermelhos')
  cor = cor.replace('brown','castanhos')
  cor = cor.replace('blue-gray','azul-cinza')
  cor = cor.replace('black','negros')
  cor = cor.replace('orange','laranjas')
  cor = cor.replace('hazel','cor de mel')
  cor = cor.replace('pink','rosas')
  cor = cor.replace('unknown','cor desconhecida...')
  cor = cor.replace('gold','dourados')
  cor = cor.replace('green','verdes')
  cor = cor.replace('white','brancos')
  return cor


def translate_cabelo(cor : str):
  cor = cor.replace('blond','loiro')
  cor = cor.replace('n/a','sem cabelo...')
  cor = cor.replace('none','sem cabelo...')
  cor = cor.replace('brown','castanho')
  cor = cor.replace('grey','cinza')
  cor = cor.replace('black','preto')
  cor = cor.replace('white','branco')
  cor = cor.replace('auburn','ruivo')
  cor = cor.replace('blonde','loiro')
  return cor


def translate_pele(cor : str):
  cor = cor.replace('fair','clara')
  cor = cor.replace('gold','dourada')
  cor = cor.replace('white','branca')
  cor = cor.replace('blue','azul')
  cor = cor.replace('light','clara')
  cor = cor.replace('red','vermelha')
  cor = cor.replace('unknown','desconhecida...')
  cor = cor.replace('green','verde')
  cor = cor.replace('tan','bronzeada')
  cor = cor.replace('brown','marrom')
  cor = cor.replace('pale','pálida')
  cor = cor.replace('metal','metálica')
  cor = cor.replace('dark','negra')
  cor = cor.replace('mottle','manchada')
  cor = cor.replace('grey','cinza')
  cor = cor.replace('orange','laranja')
  cor = cor.replace('yellow','amarela')
  cor = cor.replace('silver','prateada')
  return cor
  

def translate_genero(gen : str):
  gen = gen.replace('female', 'feminino')
  gen = gen.replace('male', 'masculino')
  gen = gen.replace('n/a', 'sem sexo...')
  gen = gen.replace('none', 'sem sexo...')
  gen = gen.replace('hermaphrodite', 'hermafrodita')
  return gen


def get_tipo(intent):

    dic = {
        'peso': 'mass',
        'pele': 'skin_color',
        'idade': 'birth_year',
        'genero': 'gender',
        'cabelos': 'hair_color',
        'altura': 'height',
        'olhos': 'eye_color'
        }

    match = re.search(r'(?<=/)(.+$)', intent)
    
    return dic[match.group(0)]


class ActionClearSlots(Action):

    def name(self) -> Text:
        return "action_clear_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [AllSlotsReset()]


class ActionCompara(Action):

    def name(self) -> Text:
        return "action_compara"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        person1 = tracker.get_slot('person1')
        person2 = tracker.get_slot('person2')

        person1_response = search_person(person1)
        person2_response = search_person(person2)

        tipo = get_tipo(tracker.latest_message['intent'].get('name'))
        
        person1_info = person1_response[tipo]
        person2_info = person2_response[tipo]

        person1_name = person1_response['name']
        person2_name = person2_response['name']
        
        return [
            SlotSet('person1_info', person1_info),
            SlotSet('person2_info', person2_info),
            SlotSet('person1', person1_name),
            SlotSet('person2', person2_name)
            ]


class ActionDescreve(Action):

    def name(self) -> Text:
        return "action_descreve"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        person1 = tracker.get_slot('person1')

        person1_response = search_person(person1)

        tipo = get_tipo(tracker.latest_message['intent'].get('name'))
        
        person1_info = person1_response[tipo]

        person1_name = person1_response['name']
        
        return [
            SlotSet('person1_info', person1_info),
            SlotSet('person1', person1_name)
        ]
