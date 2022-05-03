import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import csv

credentials = None
#If exist --> load token from pickle
if os.path.exists("mock_token.pickle"):
    print("Loading credentials from file...")
    with open("mock_token.pickle", "rb") as token:
        credentials = pickle.load(token)

#Keep credentials logged and reuse them; also defining scopes
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print("Refreshing access token...")
        credentials.refresh(Request())
    else:
        print("Fetching new tokens...")
        flow = InstalledAppFlow.from_client_secrets_file(
            "mock_client_secrets.json",
            scopes=["https://www.googleapis.com/auth/youtube.readonly"]
        )

        flow.run_local_server(
            port=MOCK_PORT_CHANGE_HERE, prompt="consent", authorization_prompt_message=""
        )

        credentials = flow.credentials

        #Save credentials to not run through all auth again next usage
        with open("mock_token.pickle", "wb") as f:
            print("Saving credentials for future use...")
            pickle.dump(credentials, f)

#Create pickle files
def createPickle(output_name, variable):
    with open(f'{output_name}.pickle', 'wb') as handle:
        pickle.dump(variable, handle, protocol=pickle.HIGHEST_PROTOCOL)

#Load Pickle
def loadPickle(filename):
    with open(f'{filename}', 'rb') as handle:
        loaded_pickle = pickle.load(handle)
    return loaded_pickle

#Request information from the Youtube API
#playlistItems --> need status (private/public); contentDetails (video id, etc.); snippet (title, etc.)
def APICall(playlistId):
    request = youtube.playlistItems().list(
        part="status, contentDetails, snippet",
        playlistId=playlistId,
        maxResults=50
    )
    return request

def createListOfDicts():
    global request

    playlistItems = []
    #Keep going through the nextPage tokens, otherwise limited to 50
    while request:
        response = request.execute()
        playlistItems.extend(response['items'])
        request = youtube.playlistItems().list_next(
            request, response)

    return playlistItems


youtube = build("youtube", "v3", credentials=credentials)
request = APICall('LL') #LL = ID for liked videos

#Do this only once everytime you need to refresh
#listInfo = createListOfDicts()
#createPickle('mock_playlistMetaData', listInfo)

meta = loadPickle('mock_playlistMetaData.pickle')

def getAllData():

    data = []
    for i in range(len(meta)):
            title = meta[i]['snippet'].get('title')
            description = meta[i]['snippet'].get('description')
            # icon = meta[i]['snippet']['thumbnails'].get('standard')
            # if type(icon) == dict:
            #     icon = icon.get('url')
            # else:
            #     icon = None
            icon = meta[i]['snippet']['thumbnails'].get('standard', {}).get('url')
            video_owner = meta[i]['snippet'].get('videoOwnerChannelTitle')
            video_owner_channel_id = f"https://youtube.com/channel/{meta[i]['snippet'].get('videoOwnerChannelId')}"
            video_liked_at = meta[i]['snippet'].get('publishedAt')

            video_id = f"https://youtu.be/{meta[i]['contentDetails'].get('videoId')}"
            videoPublishedAt = meta[i]['contentDetails'].get('videoPublishedAt')

            data.append((title, video_id, icon, description, video_owner, video_owner_channel_id, video_liked_at, videoPublishedAt))

    return data

all_data = getAllData()

def writeToCSV():
    with open('mock_my_liked_videos.csv', 'w', encoding='utf-8', newline='') as file:
        write = csv.writer(file)

        for row in all_data:
            name = row[0]; link = row[1]; icon = row[2]; descr = row[3]; video_owner = row[4]
            video_owner_chanel_id = row[5]; liked_AT_date = row[6]; published_AT_date = row[7]

            #print(name, link, icon, descr, video_owner, video_owner_chanel_id, liked_AT_date, published_AT_date)

            write.writerow([name, link, icon, descr, video_owner, video_owner_chanel_id, liked_AT_date, published_AT_date])