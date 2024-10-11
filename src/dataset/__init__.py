from .pytype import Track, TrackData
from .spotify import SpotifyClient, get_preview_data
from .db import init_database, Database
from .queries import MongoQuery
from .env import get_env_var
from .mongo import MongoDocker

def fill_db(database: Database, spotify_client: SpotifyClient, genres: list[str], pages: int = 20) -> None:
    from tqdm import trange 
    for genre in genres:
        bar = trange(pages)
        bar.set_description_str(f"{genre=}")
        for page in bar:
            tracks = spotify_client.single_page_genre_request(genre, page)
            num_failed = database.meta.insert_many(tracks)
            bar.set_postfix_str(f"batch {page+1} / {pages} ; {num_failed=}")

def fill_previews_data(database: Database) -> None:
    from tqdm import tqdm
    # query database to get all songs that has a preview link AND not data set
    tracks = database.meta.query(data = None, preview_url = {MongoQuery.NE : None})
    tracks_ids_with_data = database.data.get_all_ids()

    # iterate and get data
    for track in tqdm(tracks):
        if not track.id in tracks_ids_with_data:
            data = get_preview_data(track)
            track_data = TrackData(id = track.id, data = data)
            database.data.insert(track_data)
