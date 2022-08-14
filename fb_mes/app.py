from flask import Flask, request
import requests
from utils import crypt
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
print(find_dotenv())

FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = crypt.decrypt("H<3M4w8l^V07Y^r#81rD771189707493413012006922572306101655663709673306600953320672800718538504301370490031411370670063800872238737006433146610586", os.getenv('PRIVATE_KEY'))
PAGE_ACCESS_TOKEN = crypt.decrypt("GZM3Fj5W%2uPQ_lck9c_nZ8O2#vA8FJ2!qV1OK14vi01tM0sz6xz60tCO2~k]bl5W84HMM[3)ucC70Aks#4Wk|7WQ57K0W5j2s2u86E)^6It9V98WU_H5Jz6_2%cO21}_Q6_!K2nKkVt%)5cW9O8u5c,I_%L2AC_7]P5;05[K0OWFjK6sg5K|?jS0O:bk..3~vQ}3lK!3cq|9yE1G_E:7ycQu3uF8|qt82xli433O_8Uj[4VVFLn,4Zc7Wki3I_8y2F]l|988C}S5}tJFL|91Z9v,I1K%JC1]bu^82]yGk]73vu1OuA1KOZ5.1!M99}0_[A_04?sU2WZs8spV5EW57j2u~n1Pn736u)847}Ov6KZ8Z68JZ[;s6zQ)yi179794789274", os.getenv("PRIVATE_KEY"))

app = Flask(__name__)

def get_bot_response(message):
    """This is just a dummy function, returning a variation of what
    the user said. Replace this function with one connected to chatbot."""
    return "This is a dummy response to '{}'".format(message)


def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"

def respond(sender, message):
    """Formulate a response to the user and
    pass it on to a function that sends it."""
    response = get_bot_response(message)
    send_message(sender, response)


def is_user_message(message):
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))


def send_message(recipient_id, text):
    """Send a response to Facebook"""
    payload = {
        'message': {
            'text': text
        },
        'recipient': {
            'id': recipient_id
        },
        'notification_type': 'regular'
    }

    auth = {
        'access_token': PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        FB_API_URL,
        params=auth,
        json=payload
    )

    return response.json()


@app.route("/")
def listen():
    """This is the main function flask uses to 
    listen at the `/webhook` endpoint"""
    if request.method == 'GET':
        return verify_webhook(request)

    if request.method == 'POST':
        payload = request.json
        event = payload['entry'][0]['messaging']
        for x in event:
            if is_user_message(x):
                text = x['message']['text']
                sender_id = x['sender']['id']
                respond(sender_id, text)

        return "ok"


if __name__ == "__main__":
    app.run(host='localhost', port='5000', debug=True)