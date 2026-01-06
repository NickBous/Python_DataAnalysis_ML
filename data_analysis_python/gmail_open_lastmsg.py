from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import base64
from email.message import EmailMessage

# Scopes required for accessing Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Authenticate the user and return the Gmail API service."""
    creds = None
    # Load credentials from file
    if creds is None or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
    return build('gmail', 'v1', credentials=creds)

def get_latest_email(service):
    """Retrieve the latest email."""
    # Get the list of messages
    results = service.users().messages().list(userId='me', maxResults=1).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No messages found.")
        return

    # Get the message ID
    message_id = messages[0]['id']
    # Retrieve the message
    message = service.users().messages().get(userId='me', id=message_id).execute()

    # Decode the email content
    payload = message['payload']
    headers = payload['headers']
    for header in headers:
        if header['name'] == 'Subject':
            print("Subject:", header['value'])
        if header['name'] == 'From':
            print("From:", header['value'])

    # Decode the body
    if 'parts' in payload:
        body = payload['parts'][0]['body']['data']
        decoded_body = base64.urlsafe_b64decode(body).decode('utf-8')
        print("\nMessage Body:\n", decoded_body)

if __name__ == '__main__':
    # Authenticate and build the service
    service = authenticate_gmail()
    # Retrieve the latest email
    get_latest_email(service)
