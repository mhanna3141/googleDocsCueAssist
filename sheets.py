import tkinter as tk
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from functools import partial
from re import findall
from tkinter import simpledialog
from tkinter import messagebox


# something important with google drive or docs or something
scope = ["https://spreadsheets.google.com/feeds",
         'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive",
         'https://www.googleapis.com/auth/documents.readonly']

# credentials for google drive
creds = ServiceAccountCredentials.from_json_keyfile_name("downloadedJSON.json", scope)

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
allCues = {}
allCueNumbers = []

index = 0
cueName = "None"

# splice the document object
for i in documentContent:

    # characters in i
    if "paragraph" in i:

        # loop through the line
        for element in i['paragraph']['elements']:

            # line break
            if element['textRun']['content'] == "\n":

                # add the sub number
                cueInfoChunk += "\nsubNum: " + str(index)

                # light cue
                if "Lights:" in cueInfoChunk:

                    # add cue info to allCues
                    allCues[cueName] = cueInfoChunk
                    allCueNumbers.append(cueName)

                    # increase the sub number
                    index += 1

                cueInfoChunk = """"""
                continue

            # found new cue number
            if "Cue " in element['textRun']['content']:

                # set name of the cue to just the cue number
                cueName = findall('[0-9]+', element['textRun']['content'])[0]
                cueInfoChunk = """"""

            # add string to something
            cueInfoChunk += element['textRun']['content']


def findCue(event):
    global cueIndex, cueLabel

    # cue that user wants to skip to
    thisCue = simpledialog.askstring("Find Cue", "Enter Cue Number: ", parent=root)

    # user might try to enter a cue that doesn't exist
    try:

        # remove anything that isn't a number
        thisCue = findall('[0-9]+', thisCue)[0]

        # set the cueIndex to the index where thisCue, a string, is located.
        cueIndex = allCueNumbers.index(thisCue)

        # change the current cue
        cueLabel['text'] = allCues[thisCue]

    # cue doesn't exist in dictionary
    except ValueError:
        print("Lights are not effected by that cue \n")
        messagebox.showerror("Cue Existence Error", "that cue doesn't have anything \n to do with lights")


def changeCue(goForward, other):
    global cueIndex, cueLabel

    # want to go forward
    if goForward:
        cueIndex += 1
        newCueString = allCues[allCueNumbers[cueIndex]]

    # want to go back
    else:

        cueIndex -= 1
        newCueString = allCues[allCueNumbers[cueIndex]]

    cueLabel['text'] = newCueString



cueIndex = 0

countLightFromMe = "Cue 10"

root = tk.Tk()

mainFrame = tk.Frame(master=root)
mainFrame.pack()
cueLabel = tk.Label(master=mainFrame, text=allCues[allCueNumbers[cueIndex]])

root.bind('<Left>', partial(changeCue, False))
root.bind('<Right>', partial(changeCue, True))
root.bind('n', partial(changeCue, True))
root.bind('f', findCue)
cueLabel.pack()
root.mainloop()

"""
while True:

    thisCue = input("Cue: ")
    try:
        print(allCues[thisCue])
    except KeyError:
        print("Lights are not effected by that cue \n")
"""