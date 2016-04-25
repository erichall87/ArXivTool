from __future__ import print_function
import httplib2
import os
import base64
import re
import json

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from apiclient import errors

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'GMail ArXiv Scraper'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.getcwd()
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-scrape-arxiv.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def parseEmail(email):
    abstracts = re.split(r'-{6,}',email)
    abstracts = [temp for temp in abstracts if re.search(r'.*Title:.*\\\\.*\\\\',temp,re.S)]
    absDict = dict()
    for ab in abstracts:
        ab = re.split(r'\\\\',ab)
        cats = re.findall(r'\n[^:\n ]*:',ab[1])
        cats = [c.strip('\n') for c in cats]
        parseAb = re.split(re.compile('|'.join(cats)),ab[1])
        tempDict = dict()
        for i,j in enumerate(cats):
            tempDict[j.strip(':')] = re.sub('[ ]+',' ',re.sub(r'\r\n',' ',parseAb[i+1])).strip()

        tempDict['Abstract'] = re.sub('\r\n',' ',ab[2]).strip()
        absDict[tempDict['Title']] = tempDict

    return absDict


def main(saving = False):
    """
    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    dataDict = dict()

    try:
        response = service.users().messages().list(userId='me',
                                                   q = 'label:ArXiv').execute()

        emails = []
        if 'messages' in response: 
          emails.extend(response['messages'])

        while 'nextPageToken' in response:
          page_token = response['nextPageToken']
          response = service.users().messages().list(userId='me',
                                                     q='label:ArXiv',
                                                     pageToken=page_token).execute()
          if 'messages' in response: 
            emails.extend(response['messages'])
        counter = 1
        for email in emails:
            if counter%10 == 0:
                print(counter)
            counter += 1
            response = service.users().messages().get(userId='me',id = email['id']).execute()
            msgStr = base64.urlsafe_b64decode(response['payload']['body']['data'].encode('ASCII'))
            absDict = parseEmail(msgStr)
            absDict.update(dataDict)
            dataDict = absDict
        if saving:
            with open('FullCorpus.json','w') as f:
                json.dump(dataDict,f)
    
    except errors.HttpError, error:
        print('An error occurred: %s' % error)



if __name__ == '__main__':

    email = main()
 

