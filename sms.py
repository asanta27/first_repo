from flask import Flask, request, redirect
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import json
import apiai
import time

account_sid = "ACc139####"
auth_token = "#####"
client = Client(account_sid, auth_token)
CLIENT_ACCESS_TOKEN_API_AI = '0287590ad3dd449dacb09f389926f0b#'

app = Flask(__name__)


@app.route("/sms", methods=['GET', 'POST'])
def main():
    sms_reply = robo_response()[0]
    print(sms_reply)
    time.sleep(1)
    resp = MessagingResponse()
    resp.message(sms_reply)
    return str(resp)

def incoming_sms():
    number = request.form['From']
    message_body = request.form['Body']
    message_text = message_body.split('- ', 1)
    print(message_text)
    return [message_text[1],number]

def robo_response():
    user_query = incoming_sms()

    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN_API_AI)
    request = ai.text_request()
    request.query = user_query[0]

    json_response = json.loads(request.getresponse().read())
    speech = json_response['result']['fulfillment']['speech']
    return [speech]

if __name__ == "__main__":
    app.run(debug=True)
