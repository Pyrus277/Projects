import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3

# define our constants
DATABASE_LOCATION = "sqlite:///my_played_tacks"
USER_ID = "22spaqn7osucmwakfga7772dq"
# Apparently this token expires after a few min, so we need to regenerate. How to solve this?
TOKEN = "BQA-7hSzvW4EPyqqs6tCz4mcv0f8O6WZwZwZZs57TxeF_c45DAaT99RdnBP70x315gEBYdxz358sprt4v_tmFh52tyF9FkVd_XgIsBKnzcEwEMgJrBSEz3tcWzOTGBQlpXeqC5Y07iS_GO-q0AKQazx2xh3ZdZFV90XN1cgr"

# protect         
if __name__ == "__main__":
    
# Extract recent listening data from the spotify API
    # We need to send some info in the header with our request. 
    # Here we populate fields according to the API's instructions. 
    headers = {
        "Accept" : "application",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }

    # We want the time in UNIX miliseconds
    today = datetime.datetime.now()
    # We are getting yesterday because we want to run this feed daily, and every day
    # we want to see the played list of the prior 24hrs
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    # requests.get(). Construct your URL, and get a response object r
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp), headers = headers)

    # Use .json() with r to make a python object we can pick apart
    data = r.json()

    # Print it out to see what we're working with:
    # print(json.dumps(data, indent=2)) # Checkpoint! We pulled the data.
    # print(data)
    # 'data' has a lot of clutter. For our purposes we only want
    # song name, artist name, played at (time the song was played),
    # and timestamp (the 24 hr period we are looking at). 

    # Set up some lists to store the data we're interested in
    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []
    
    for song in data["items"]:
        song_names.append(song["track"]["name"]) 
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10]) #NO
    
    # Now we plug our lists into a dictionary and format the data into
    # a pandas dataframe


    song_dict = {
        "song_name" : song_names,
        "artist_name" : artist_names,
        "played_at" : played_at_list,
        "timestamps" : timestamps
    }

# checkpoint. ^All this works properly
    print("-----")
    print(timestamps)
    print("-----")

    song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "timestamps"])
    print(song_df)

