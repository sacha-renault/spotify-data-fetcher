import base64

import numpy as np
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from .pytype import Track

def get_preview_data(track_or_url: Track | str) -> str:
    # Get URL from the track object or directly from the input
    if isinstance(track_or_url, str):
        url = track_or_url
    elif isinstance(track_or_url, Track):
        url = track_or_url.preview_url
    
    # Request the data from the URL
    try:
        result = requests.get(url)
        result.raise_for_status()  # Raise an error for bad responses
    except requests.exceptions.RequestException as e:
        return None  # Return empty string or handle the error
    
    # Check if the request was successful and content is returned
    if result.status_code == 200 and result.content:
        # Base64 encode the binary data to store it in MongoDB as a string
        audio_base64 = base64.b64encode(result.content).decode('utf-8')
        return audio_base64
    return None


class SpotifyClient:
    def __init__(self, client_id: str, client_secret: str) -> None:
        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self._sp = spotipy.Spotify(auth_manager=auth_manager)

    def single_page_request(self, search: str, type: str, page: int) -> list[Track]:
        items = []
        results = self._sp.search(q=search, type=type, limit=50, offset=50 * page)
        for _, track in enumerate(results['tracks']['items']):
            items.append(Track.model_validate(track))
        return items

    def single_page_genre_request(self, genre: str, page: int, **kwargs) -> list[Track]:
        tracks = self.single_page_request(f"genre:{genre}", "track", page, **kwargs)
        for track in tracks:
            track.genres.add(genre)
        return tracks