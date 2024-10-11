from pydantic import BaseModel, HttpUrl
from typing import List, Optional


class ExternalUrls(BaseModel):
    spotify: HttpUrl


class ExternalIds(BaseModel):
    isrc: str


class Image(BaseModel):
    url: HttpUrl
    height: Optional[int] = None
    width: Optional[int] = None


class Artist(BaseModel):
    name: str
    id: str
    href: HttpUrl
    external_urls: ExternalUrls


class Album(BaseModel):
    album_type: str
    artists: List[Artist]
    available_markets: List[str]
    external_urls: ExternalUrls
    href: HttpUrl
    id: str
    images: List[Image]
    name: str
    release_date: str
    release_date_precision: str
    total_tracks: int
    type: str
    uri: str


class Track(BaseModel):
    artists: List[Artist]
    available_markets: List[str]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_ids: ExternalIds
    external_urls: ExternalUrls
    href: HttpUrl
    id: str
    is_local: bool
    name: str
    popularity: int
    preview_url: Optional[HttpUrl] = None
    track_number: int
    type: str
    uri: str
    genre: str | None = None
    data: str | None = None
