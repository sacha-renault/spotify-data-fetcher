from .pytype import Track, TrackData
from .spotify import SpotifyClient, get_preview_data
from .db import init_database, Database
from .queries import MongoQuery
from .env import get_env_var
from .mongo import MongoDocker

def fill_db(database: Database, spotify_client: SpotifyClient, genres: list[str], pages: int = 20) -> None:
    from tqdm import trange 

    # iterate over the requested genres
    for genre in genres:
        bar = trange(pages)
        bar.set_description_str(f"{genre=}")

        # iterate over the number of requested pages (max 20)
        for page in bar:

            # get many tracks
            tracks = spotify_client.single_page_genre_request(genre, page)

            # insert in db
            num_new = len(tracks) - database.meta.insert_many(tracks)
            bar.set_postfix_str(f"batch {page+1} / {pages} ; {num_new=}")

def fill_previews_data(database: Database) -> None:
    from tqdm import tqdm
    # query database to get all songs that has a preview link
    tracks = database.meta.query(data = None, preview_url = {MongoQuery.NE : None})

    # get all ids of tracks in the data database
    tracks_ids_with_data = database.data.get_all_ids()

    # iterate and get data
    for track in tqdm(tracks):
        # if the track already have a data, we skip, otherwise, we download
        if not track.id in tracks_ids_with_data:
            data = get_preview_data(track)
            track_data = TrackData(id = track.id, data = data)
            database.data.insert(track_data)
