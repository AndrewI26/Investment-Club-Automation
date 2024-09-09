import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from util import createDocsRequests, createDefinitionsRequests

SCOPES = ['https://www.googleapis.com/auth/documents']

# The ID of a sample presentation.
DOCUMENT_ID = "ENTER_DOC_ID"
DEFINITION_DOC_ID = "ENTER_DOC_ID"

def updateDocs(leaders: list): 
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token_docs.json'):
        creds = Credentials.from_authorized_user_file('token_docs.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8000, open_browser=True)
        # Save the credentials for the next run
        with open('token_docs.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('docs', 'v1', credentials=creds)

        # Call the Slides API

        document = service.documents()
        
    
        body = {
            'requests': createDocsRequests(leaders)
        }
        
        document.batchUpdate(documentId=DOCUMENT_ID, body=body).execute()

        body = {
            'requests': createDefinitionsRequests()
        }

        document.batchUpdate(documentId=DEFINITION_DOC_ID, body=body).execute()

    except HttpError as err:
        print(err)
