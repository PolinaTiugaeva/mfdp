import chromadb
import pandas as pd
import json
import numpy

GAMES_JSON = './games_metadata_new.json'
GAMES_CSV = './games.csv'

if __name__ == '__main__':
    
    client = chromadb.HttpClient(host="chromadb",
                                 port=8000)
    
    with open(GAMES_JSON) as f:
        data = f.read()
    
    df_games = pd.read_csv(GAMES_CSV)

    games_metadata = json.loads(data)
    client.delete_collection(name="games")
    collection = client.create_collection(name="games")
    for game_metadata in games_metadata:
        description = str(game_metadata['description'])
        title = df_games[df_games['app_id'] == game_metadata['app_id']]['title'].astype(str).values
        title = title[0]
        collection.add(
            documents=[description],
            metadatas=[{'title' : title}],
            ids=[str(game_metadata['app_id'])]
        )