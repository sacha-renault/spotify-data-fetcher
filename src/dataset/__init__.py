from .pytype import Track
from .spotify import SpotifyClient, get_preview_data
from .db import TrackDatabase
from .queries import MongoQuery
from .env import get_env_var
from .mongo import MongoDocker

def fill_db(database: TrackDatabase, spotify_client: SpotifyClient, genres: list[str], pages: int = 20) -> None:
    from tqdm import trange 
    for genre in genres:
        bar = trange(pages)
        bar.set_description_str(f"{genre=}")
        for page in bar:
            tracks = spotify_client.single_page_genre_request(genre, page)
            num_failed = database.insert_many(tracks)
            bar.set_postfix_str(f"batch {page+1} / {pages} ; {num_failed=}")

def fill_previews_data(database: TrackDatabase, spotify_client: SpotifyClient) -> None:
    from tqdm import tqdm
    # query database to get all songs that has a preview link AND not data set
    tracks_to_set = database.query(data = None, preview_url = {MongoQuery.NE : None})

    # iterate and get data
    for track in tqdm(tracks_to_set):
        # get data
        data = get_preview_data(track)

        # update value on the db
        database.update_by_id(track.id, data = data)

