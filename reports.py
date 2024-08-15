from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import csv
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from googleapiclient.discovery import build
from datetime import datetime
from edit_config import *

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

creds = None

# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json')
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# Call the Gmail API
service = build('gmail', 'v1', credentials=creds)

def create_message(sender, to, subject, html, attachment_file=None):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    msg = MIMEText(html, 'html')
    message.attach(msg)

    if attachment_file:
        with open(attachment_file, 'rb') as f:
            mime_base = MIMEBase('application', 'octet-stream')
            mime_base.set_payload(f.read())
            encoders.encode_base64(mime_base)
            mime_base.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_file)}"')
            message.attach(mime_base)

    raw_message = base64.urlsafe_b64encode(message.as_bytes())
    raw_message = raw_message.decode()
    body = {'raw': raw_message}
    return body

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print(f"Message Id: {message['id']}")
        return message
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def sendEmail(sender, reciver, subject, message_text, attachment_file=None):
    message = create_message(sender, reciver, subject, message_text, attachment_file)
    print(send_message(service, "me", message))

def sendReport():
    config = getConfigData()
    bal = []
    time = []
    initial = 0
    final = 0
    percentChange = 0
    balChange = 0
    
    now = datetime.now()
    date = now.strftime("%m%d%y")
    fname = f"{date}.csv"
    image_filename = f"BalGraph-{datetime.now().strftime('%m%d%y')}.png"  # The name of the exported image file

    with open(f"Sheets/{fname}", mode = 'r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=",")
        for row in csv_reader:
            bal.append(row[1])
            time.append(row[0])
            
    initial = float(bal[0])
    final = float(bal[-1])
    balChange = final - initial
    percentChange = (balChange / initial) * 100
    #percentChange = 0
    
    sender_email = "noreply@malcarne.com"
    to_email = "caleb.malcarne@gmail.com"
    subject = "Test Trading report"
    html_msg = f'''
        <p><strong>Report, {datetime.now()}</strong></p>
        <p>Account: {config.get("account","")}</p>
        <p>Initial Balance: ${initial}</p>
        <p>Final Balance:  ${final}</p>
        <p>Balance Change: ${balChange}</p>
        <p>Account Growth: {percentChange:.2f}%</p>
    '''

    #sendEmail(sender_email, to_email, subject, html_msg, attachment_file=image_filename)
    sendEmail(sender_email, "calebw@malcarne.com", subject, html_msg, attachment_file=image_filename)

