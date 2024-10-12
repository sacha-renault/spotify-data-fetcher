from src.dataset import (Database, SpotifyClient, init_database,
                         fill_db, fill_previews_data, MongoDocker,
                         get_env_var)
from src.dataset import MongoQuery as mq

db_name = "music_database"
collection_name = "tracks"

if __name__ == "__main__":
    mgenres = ["rock", "metal", "dubstep", "electro", "pop", "jazz", "reggae",
               "techno", "hip hop", "rap", "disco", "salsa"]

    with MongoDocker("data") as db_uri:
        var = get_env_var()
        db = init_database(db_uri)
        sc = SpotifyClient(var.spotify_client_id, var.spotify_client_secret)

        # fille db
        # fill_db(db, sc, mgenres)
        # fill_previews_data(db)

        print(len(db.meta.query(
            genres = "metal"
        )))
            