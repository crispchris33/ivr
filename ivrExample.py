import os
import requests
import time
import pprint
import json
import threading

from signalwire.rest import Client as signalwire_client
from signalwire.voice_response import VoiceResponse, Say, Gather
from flask import Flask,request

app = Flask(__name__)

# accept web requests to /get_menu route from GET or POST
@app.route('/get_menu', methods=['GET', 'POST'])
def get_menu():
    response = VoiceResponse()

    # read menus from json file
    with open('menus.json') as f:
         menus = json.load(f)

    # check to see if a default menu was specified, else default to "main"
    menu = request.values.get("menu")
    if menu not in menus:
        response.say("Thank you for calling one two three Company. Please listen carefully to the menu options.")
        menu = "main"

    # read input_type variable
    input_type = request.values.get("input_type")

    # check if user input was provided via dtmf entry
    if input_type == "dtmf":
        # get digits pressed at menu
        digits = request.values.get("Digits")
        input_action = menus[menu][digits]["action"]
        response.say("you pressed " + digits)
        response.redirect(url=input_action)
        response.hangup()
    else:
        # no user input was detected, so lets present a menu
        gather = Gather(action='/get_menu' + "?menu=" + menu, input='dtmf', timeout="3", method='GET')

        # loop through menus and generate menu options
        for key in menus[menu]:
            print(key, '->', menus[menu][key]["verbiage"])
            gather.say(menus[menu][key]["verbiage"])

        # add menu to response 
        response.append(gather)
        response.hangup()

    # return response
    return str(response)

#establish call reception 
def call_reception(args):
    switcher = {
        #enter number here
        "reception": '+15055034455',
    }
    errorOccurred = "An error occurred. We could not route to the correct department. Please record a message with detailed " \
                    "information and we will get back to you as soon as possible. "
    return switcher.get(args, errorOccurred)

#dial reception func
@app.route('/dial_reception', methods=['GET', 'POST'])
def dial_reception():
    group = request.args.get('group')
    name = request.args.get('name')
    response = VoiceResponse()
    response.dial(call_reception(name), action='/handleDialCallStatus?group=' + group, methods=['GET', 'POST'])
    return str(response)

# Front Office Voicemail 
@app.route('/get_voicemail_fo', methods=['GET', 'POST'])
def get_voicemail_fo():
    response = VoiceResponse()
    response.say('You have reached our Front Office voicemail, please leave a message.')
    response.hangup()
    return str(response)

# IT Voicemail 
@app.route('/get_voicemail_it', methods=['GET', 'POST'])
def get_voicemail_if():
    response = VoiceResponse()
    response.say('You have reached our IT voicemail, please leave a message.')
    response.hangup()
    return str(response)

# General Voicemail 
@app.route('/get_voicemail', methods=['GET', 'POST'])
def get_voicemail():
    response = VoiceResponse()
    response.say('You have reached the voicemail of 123 Company, please leave a message.')
    response.hangup()
    return str(response)

# Default route
@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(host="0.0.0.0")