from flask import Flask, request, redirect
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os.path
import os
import sys
import json

account_sid = "ACc1390d4277e1a693915c8e3ecfea9bf4"
auth_token = "2e689141e1694e99997607b7a7673065"
client = Client(account_sid, auth_token)
CLIENT_ACCESS_TOKEN_API_AI = '0f1d8b806b2b448eb738674f9fe6356c'

try:
    import apiai
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
    import apiai

app = Flask(__name__)
@app.route("/sms", methods=['GET', 'POST'])

def main():
    # activate robot
    roboOutput = roboreply()

   # Add a message
    resp = MessagingResponse()
    resp.message(roboOutput[0])
    adminMessage = roboOutput[4] + " is " + roboOutput[1] + " for " + roboOutput[3]


    if (roboOutput[2] == False and roboOutput[1] == "available"):
        client.messages.create(to="+17029075019",
                            from_="+17022003374",
                            body = adminMessage)
        print(adminMessage)
    print(roboOutput)
    return str(resp)

def smsinput():
    number = request.form['From']
    message_body = request.form['Body']
    return [message_body,number]

def roboreply():
    # turn sms into userinput
    userinput = smsinput()
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN_API_AI)
    request = ai.text_request()
    request.lang = 'en'  # optional, default value equal 'en'
    request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"
    request.query = userinput[0] # userinput

    json_response = json.loads(request.getresponse().read())
    speech = json_response['result']['fulfillment']['speech']
    action = json_response['result']['action']
    actionIncomplete = json_response['result']['actionIncomplete']
    time = json_response['result']['resolvedQuery']

    return [speech,action,actionIncomplete,time,userinput[1]]

if __name__ == "__main__":
    app.run(debug=True)