import os # used to search for the files path etc
import glob # used in order to retrieve files 
import pandas as pd # pandas can become handy
import psycopg2  # used to connect potgresql with python
from sql import artists__insert,songs__insert,time__insert,users__insert,song__select,songplayed__insert
from connect import DropTable, SetUp_DataBase, create_tables
host = "localhost"
dbname = "postgres"
user = "postgres"
password = "*******"


def get__files(filepath):
    all__files = []
    for (root, dirs, files) in os.walk(filepath):
        files = glob.glob(os.path.join(root,"*.json"))
        for f in files:
            all__files.append(os.path.abspath(f))
    return all__files
        # go to the filepath and print all the directories and sub-directories and all the files in this two
#get__files("D:\dataenginner")

def Process__Song__files(cur,conn,filepath):
    song__file = pd.DataFrame([pd.read_json(filepath, typ="series", convert_dates = False)])
    for value in song__file.values:
        num_songs, artist_id, artist_latitude, artist_longitude, artist_location, artist_name, song_id, title, duration, year = value
        artist_data = artist_id, artist_name, artist_location, artist_latitude, artist_longitude
        cur.execute(artists__insert,(artist_data))
        
        song_data = song_id, title, artist_id, year, duration
        cur.execute(songs__insert, (song_data))
        
        print("inserted with sucess")
        
def Process__long__files(cur,conn,filepath):
    """ process just one file """
    long_data = pd.read_json(filepath, lines = True)
    long_data = long_data[long_data["page"] == "NextSong"].astype({"ts":"datetime64[ms]"})
    t = pd.Series(long_data["ts"], index = long_data.index)
    print(t)
    #long_data['ts'] = pd.to_datetime(long_data['ts'], unit='ms')
    column_labels = ["timestamp", "hour", "day", "weelofyear", "month", "year", "weekday"]
    time_data = []

    for data in t:
        time_data.append([data ,data.hour, data.day, data.weekofyear, data.month, data.year, data.day_name()])
        
    time_df = pd.DataFrame.from_records(data = time_data, columns = column_labels)
    
    
    # now we loop at each raows of the dataFrame and then insert the data into the postgresql database.
    for i, row in time_df.iterrows():
        cur.execute(time__insert, list(row))
        conn.commit()
    user_df = long_data[['userId','firstName','lastName','gender','level']]
    #print(user_df.head())
    for i, row in user_df.iterrows():
        cur.execute(users__insert,list(row))
        conn.commit()
    for i, row in long_data.iterrows():
        cur.execute(song__select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        #print(results)
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay__data = ( row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplayed__insert, songplay__data)
def Process__All__DataSet(cur,conn,function,filepath):
    all__files = get__files(filepath)
    for i, file in enumerate(all__files):
        function(cur,conn,file)
        conn.commit()
        print("Done")
           
def main():
    cur, conn =  SetUp_DataBase()
    DropTable(cur,conn)
    create_tables(cur,conn)
    get__files("D:\dataenginner")
    Process__All__DataSet(cur,conn,filepath = "D:\dataenginner\data\log_data", function=Process__long__files)
    Process__All__DataSet(cur,conn,filepath = "D:\dataenginner\data\song_data",  function=Process__Song__files)
    #Process__Song__files(cur,all__files[0]) 
    conn.close()
    print("ceated successfully")
    
if __name__ == "__main__":
    main()     