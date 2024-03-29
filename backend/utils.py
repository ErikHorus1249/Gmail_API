import re 
import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request


def match_subject(subject: str):
    pattern = r'[A-Z]+\_BL'
    return re.match(pattern, subject)

def match_amount(raw_text: str) -> str:
    pattern = r'(\*Amount\*\s)([\d\,]+)(\sVND)'
    result = re.findall(pattern, raw_text)
    # return {"name": "amount", "value": result[0][1]}
    return str(result[0][1])

def match_order_number(raw_text: str) -> str:
    pattern = r'(\*Order Number\*\s)([\d]+)'
    result = re.findall(pattern, raw_text)
    # return {"name": "order number", "value": result[0][1]}
    return str(result[0][1])

def match_debit_account(raw_text: str) -> str:
    pattern = r'(\*Debit Account\*\s)([\d]+)'
    result = re.findall(pattern, raw_text)
    # return {"name": "Debit Account", "value": result[0][1]}
    return str(result[0][1])

def match_credit_account(raw_text: str) -> str:
    pattern = r'(\*Credit Account\*\s)([\d]+)'
    result = re.findall(pattern, raw_text)
    # return {"name": "Credit Account", "value": result[0][1]}
    return str(result[0][1])

def match_beneficiary_name(raw_text: str) -> str:
    pattern = r'(\*Beneficiary Name\*\s)([A-Z\s]+)\r\n'
    result = re.findall(pattern, raw_text)
    # return {"name": "Beneficiary Name", "value": result[0][1]}
    return str(result[0][1])

def match_beneficiary_bank_name(raw_text: str) -> str:
    pattern = r'(\*Beneficiary Bank Name\*\s)(.*)\r\n'
    result = re.findall(pattern, raw_text)
    # return {"name": "Beneficiary Bank Name", "value": result[0][1]}
    return str(result[0][1])
        
def Create_Service(client_secret_file, api_name, api_version, *scopes):
    # print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    
    cred = None
    working_dir = os.getcwd()
    token_dir = 'token files'

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    # print(pickle_file)
    
    ### Check if token dir exists first, if not, create the folder
    if not os.path.exists(os.path.join(working_dir, token_dir)):
        os.mkdir(os.path.join(working_dir, token_dir))

    if os.path.exists(os.path.join(working_dir, token_dir, pickle_file)):
        with open(os.path.join(working_dir, token_dir, pickle_file), 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server(port=8080)

        with open(os.path.join(working_dir, token_dir, pickle_file), 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        # print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print(e)
        print(f'Failed to create service instance for {API_SERVICE_NAME}')
        os.remove(os.path.join(working_dir, token_dir, pickle_file))
        return None