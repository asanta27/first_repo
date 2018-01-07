from flask import Flask, request, redirect
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os.path
import os
import sys
import json
import apiai

account_sid = "ACc1390d4277e1a693915c8e3ecfea9bf4"
auth_token = "2e689141e1694e99997607b7a7673065"
client = Client(account_sid, auth_token)
CLIENT_ACCESS_TOKEN_API_AI = '0287590ad3dd449dacb09f389926f0be'

app = Flask(__name__)


@app.route("/sms", methods=['GET', 'POST'])
def main():
    sms_reply = robo_response()[0]
    print(sms_reply)
    resp = MessagingResponse()
    resp.message(sms_reply)
    return str(resp)

def incoming_sms():
    number = request.form['From']
    message_body = request.form['Body']
    return [message_body,number]

def robo_response():
    user_query = incoming_sms()
#    user_id = incoming_sms()[1]

    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN_API_AI)
    request = ai.text_request()
    request.query = user_query[0]

    json_response = json.loads(request.getresponse().read())
    speech = json_response['result']['fulfillment']['speech']
    return [speech]

if __name__ == "__main__":
    app.run(debug=True)
