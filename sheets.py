
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

# something important with google drive or docs or something
scope = ["https://spreadsheets.google.com/feeds",
         'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive",
         'https://www.googleapis.com/auth/documents.readonly']

# credentials for google drive
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

# im not really sure
service = build('docs', 'v1', credentials=creds)

# the document id (this is the same as )
DOCUMENT_ID = '1OxZn0MKg6uqWYS_VLAnEeTm4NYliI0mHLvLsE_p55CA'

# getting the contents from the docs service
document = service.documents().get(documentId=DOCUMENT_ID).execute()

# get a google doc object
documentContent = document.get('body')['content']
cueInfoChunk = """"""

# list of all cues
allCues = []

# splice the document object
for i in documentContent:
    if "paragraph" in i:
        for element in i['paragraph']['elements']:
            if element['textRun']['content'] == "\n":
                allCues.append(cueInfoChunk)
                cueInfoChunk = """"""
                continue

            cueInfoChunk += element['textRun']['content']

for i in allCues:
    print(i)