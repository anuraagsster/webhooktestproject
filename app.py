from flask import Flask
from flask import request
from flask import make_response
import datetime
import json
import os

app = Flask(__name__)

@app.route('/webhook',methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))
    res = makeWebhookResult(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action")!="purchaseDate":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    print("Parameters:")
    print(parameters)
    dateOfPurchaseValue = datetime.datetime(*[int(item) for item in parameters.get("date").split('-')]).date()
    print(dateOfPurchaseValue)
    today = datetime.date.today()
    print(today)
    dateDiff = (today - dateOfPurchaseValue).days
    if dateDiff>15:
        speech = "Sorry! " + str(dateOfPurchaseValue) + " is more than 15 days old. You can't buy a mobile protection plan for phones older than 15 days."
    elif dateDiff<=15 and dateDiff>=0:
        speech = "Thanks! " + str(dateOfPurchaseValue) + " is a valid date to buy a mobile protection plan."
    else:
        speech = "That's a future date. If you still planning to buy a phone. Please buy it and subsequently purchase our plan."
    print("Response:")
    print(speech)
    return {
            "speech": speech,
            "displayText": speech,
            "source": "dateOfPurchaseWebhook"
            }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print ("Starting app on port %d" %(port))
    app.run(debug=True, port=port, host='0.0.0.0')
    
