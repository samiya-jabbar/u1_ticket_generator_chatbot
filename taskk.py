import json
from flask import Flask, request , make_response
import pandas as pd
from datetime import date, datetime

app = Flask(__name__)

def makeWebhookResult(req):
    req = request.get_json(force=True)
    action_name = req['queryResult']['action']
   
    if action_name == 'employee-id' or action_name == 'employee-id-wrong' or action_name == 'employee-id-wrong-wrong' :
        outputcontexts = req['queryResult']['outputContexts']
        for oc in outputcontexts:
            if oc['name'].split('/')[-1] == 'session-vars':
                employee_id = oc['parameters']['CreateCR']
                data= pd.read_csv("employee_verification.csv")
        
                dict = {'date' : [datee], 'time' : [timee], 'name': [employee_id], 'phone number': [phone_number], 'user query': [user_query]}  
                df = pd.DataFrame(dict)
                for i in range(len(df)):
                    df.loc[[i]].to_csv('query_record.csv',
                        index=False,
                        header=False,
                        mode='a')
                print("info taken")
                

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    res = makeWebhookResult(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


if __name__ == '__main__':
    app.run()