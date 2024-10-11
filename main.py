from src.dataset import TrackDatabase, SpotifyClient, get_env_var, use_mongo_docker, MongoQuery
from tqdm import trange

def download_genres(database: TrackDatabase, spotify_client: SpotifyClient,  mgenre: str):
    nb_in_database = len(database.query(genre = mgenre))
    nb_page_in_db = nb_in_database // 50
    bar = trange(nb_page_in_db, 20)
    bar.set_description_str(f"Genre : {mgenre}")

    if nb_in_database != 0:
        print(f"Genre {mgenre} has already {nb_in_database} entry in the mongo database;")

    for i in bar:
        tracks = spotify_client.single_page_genre_request(mgenre, i, known_ids = database.get_all_ids())
        num_failed = database.insert_many(tracks)
        bar.set_postfix_str(f"batch {i+1} / 20 ; {num_failed=}")

    print(f"Number of {mgenre} song with data", len(
        database.query(
            genre = mgenre,
            data = { MongoQuery.NE: None}
        )
    ))

db_name = "music_database"
collection_name = "tracks"

if __name__ == "__main__":
    mgenres = ["rock", "metal", "dubstep", "electro"]

    with use_mongo_docker("data") as db_uri:
        var = get_env_var()
        db = TrackDatabase(db_uri, db_name, collection_name)
        sc = SpotifyClient(var.spotify_client_id, var.spotify_client_secret)

        for mgenre in mgenres:
            number_of_entry = len(db.query(genre = mgenre))
            if number_of_entry == 0:
                download_genres(db, sc, mgenre)
            else:
                print(f"Genre {mgenre} is already initialized : {number_of_entry}")