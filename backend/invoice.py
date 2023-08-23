from utils import Create_Service
import base64

from utils import match_subject
from utils import match_amount
from utils import match_beneficiary_bank_name
from utils import match_beneficiary_name
from utils import match_credit_account
from utils import match_debit_account
from utils import match_order_number

CLIENT_SECRET_FILE = 'credentials/client_secret.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def get_unread_mess():
    message_list = service.users().messages().list(userId='me').execute()
    mess_id = []
    for mess in message_list["messages"]:
        mess_id.append(mess['id'])
    return mess_id
    
def get_subject(mess_id: str):
    content = service.users().messages().get(userId='me', id=mess_id).execute()
    Subjects = content["payload"]["headers"]
    for subject in Subjects:
        if subject['name'] == 'subject':
            return subject['value']

def core(timerange: int):
    final_data = []
    # results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
    timerange = f"newer_than:{timerange}m"
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q=timerange).execute()
    messages = results.get('messages',[]);
    for message in messages:
        
        msg = service.users().messages().get(userId='me', id=message['id']).execute()                
        email_data = msg['payload']['headers']
        for values in email_data:
            name = values['name']
            if name == 'Subject':
                subject_name = values['value']   
                if match_subject(subject_name) and 'parts' in msg['payload']:
                    try:
                        data = msg['payload']['parts'][0]['body']["data"]
                        byte_code = base64.urlsafe_b64decode(data)
                        text = byte_code.decode("utf-8")
                        # result = " ".join(line.strip() for line in text.splitlines())     # Flatten 
                        final_data.append({"amount":match_amount(text),
                                           "debit_account": match_debit_account(text),
                                           "credit_account": match_credit_account(text),
                                           "beneficiary_name": match_beneficiary_name(text),
                                           "beneficiary_bank": match_beneficiary_bank_name(text),
                                           "order_number": match_order_number(text),
                                           })        
                    except BaseException as error:
                        pass  
                else:
                    break
    return final_data

if __name__ == "__main__":
    finall_data = core(30)
    print(finall_data)