from flask import Flask, request , make_response
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account

app = Flask(__name__)

SERVICE_ACCOUNT_FILE = 'servicedeskmanagment-jw9q-2bea03cf277e.json'
SCOPE1 = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE1)
SAMPLE_SPREADSHEET_ID = '1T8kFZl8rPbB_6LnDI8oxlho8loMT-DM43xLzlxoPdwU'
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

def makeWebhookResult(req):
    req = request.get_json(force=True)
    action_name = req['queryResult']['action']
   
    if action_name == 'get_all_details' :
        outputcontexts = req['queryResult']['outputContexts']
        for oc in outputcontexts:
            if oc['name'].split('/')[-1] == 'session-vars':
                CreateCR = oc['parameters']['CreateCR']
                CRType = oc['parameters']['CRType']
                CRImpact = oc['parameters']['CRImpact']
                CRUrgency =  oc['parameters']['CRUrgency']
                CRRiskLevel =  oc['parameters']['CRRiskLevel']
                CRServiceImpacting = oc['parameters']['CRServiceImpacting']
                ChangeReason = oc['parameters']['ChangeReason']
                InfoType = oc['parameters']['InfoType']
                CRDetails =  oc['parameters']['CRDetails']
                CRSummary =  oc['parameters']['CRSummary']
                sheett= [[CreateCR, CRImpact, CRType, CRUrgency, CRRiskLevel, CRServiceImpacting, ChangeReason, InfoType, CRDetails, CRSummary]]
                result = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,range="details",valueInputOption="USER_ENTERED", body={"values" : sheett}).execute()
            
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