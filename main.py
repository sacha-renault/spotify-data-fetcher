from src.dataset import (TrackDatabase, SpotifyClient, 
                         get_env_var, use_mongo_docker, MongoQuery, 
                         fill_db, fill_previews_data)
from tqdm import trange

db_name = "music_database"
collection_name = "tracks"

if __name__ == "__main__":
    mgenres = ["rock", "metal", "dubstep", "electro", "pop", "jazz", "reggae",
               "techno", "hip hop", "rap", "disco", "salsa"]

    with use_mongo_docker("data") as db_uri:
        var = get_env_var()
        db = TrackDatabase(db_uri, db_name, collection_name)
        sc = SpotifyClient(var.spotify_client_id, var.spotify_client_secret)

        # fille db
        # fill_db(db, sc, mgenres)
        fill_previews_data(db, sc)

        print(len(db.query(data = None, preview_url = {MongoQuery.NE : None})))
            