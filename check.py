#
# On the python side on your computer, install the Goog libs:

# $ pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

# Generate an id token and access token via the .html page
#
# you have to enable the google drive api, but the error message will give you a link for that

from google.oauth2 import id_token
from google.auth.transport import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# others here <https://developers.google.com/identity/protocols/oauth2/scopes>
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

ACCESS_TOKEN = ''  # the shorter one
CLIENT_ID = 'blahblah-blahblahblah.apps.googleusercontent.com'# UPDATE ME
ID_TOKEN = '' # the long one

try:
    # Specify the CLIENT_ID of the app that accesses the backend:
    idinfo = id_token.verify_oauth2_token(ID_TOKEN, requests.Request(), CLIENT_ID)

    # Or, if multiple clients access the backend server:
    # idinfo = id_token.verify_oauth2_token(token, requests.Request())
    # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
    #     raise ValueError('Could not verify audience.')

    # If auth request is from a G Suite domain:
    # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
    #     raise ValueError('Wrong hosted domain.')

    # ID token is valid. Get the user's Google Account ID from the decoded token.
    userid = idinfo['sub']
    print("OK. User iD:")
    print(idinfo)

    # Figured out from
    # <https://google-auth.readthedocs.io/en/stable/reference/google.oauth2.credentials.html>
    creds = Credentials(token=ACCESS_TOKEN,scopes=SCOPES)
    print(creds.has_scopes(SCOPES))
    service = build('drive', 'v3', credentials=creds)


    # Example taken from <https://developers.google.com/drive/api/v3/quickstart/python>
    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
except ValueError:
    # Invalid token
    pass
