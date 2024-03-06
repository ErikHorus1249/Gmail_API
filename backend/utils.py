
import os
from O365 import Account
from O365.utils.token import FileSystemTokenBackend

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SENDER = os.getenv("SENDER")

def send_email(hostname: str,
               ntp: str,
               status: bool):
    
    credentials = (CLIENT_ID, CLIENT_SECRET)
    
    account = Account(credentials)
    m = account.new_message()
    m.to.add(SENDER)
    m.subject = f'ALERT: Mismatched NTP Server on {hostname}'
    m.body = f"Current NTP server: {ntp}\nExpected NTP server: {10.0.14.11}\nPlease investigate and correct the NTP server configuration on this machine."
    m.send() 

def get_token():
    scopes =  ["IMAP.AccessAsUser.All", "POP.AccessAsUser.All", "SMTP.Send", "Mail.Send", "offline_access"]
    account = Account(credentials=(CLIENT_ID, CLIENT_SECRET))
    result = account.authenticate(scopes=scopes)  # request a token for this scopes
    
if __name__ == "__main__":
    # get_token()
    send_email("test", "test", True)