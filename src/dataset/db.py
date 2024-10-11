import os
from functools import wraps
from typing import Any, List
from pymongo import MongoClient
from .pytype import Track


def cast_as_track(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return [Track.model_validate(document) for document in func(*args, **kwargs)]
    return wrapper

class TrackDatabase:

    def __init__(self, db_uri: str, db_name: str, collection_name: str) -> None:
        # Initialize the MongoDB client and database
        self._client = MongoClient(db_uri)
        self._db = self._client[db_name]
        self._collection = self._db[collection_name]
    
    def insert(self, track: Track) -> bool:
        # Check if a track with the same ID already exists
        if not self.get_by_id(track.id):
            self._collection.insert_one(track.model_dump(mode="json"))
            return True
        else:
        # If track exists, update the genre field by adding the new genres
            if track.genres:
                self._collection.update_one(
                    {"id": track.id},  # Find the track by ID
                    {"$addToSet": {"genres": {"$each": list(track.genres)}}}  # Add the genres to the set
                )
            return False

    def insert_many(self, tracks: List[Track]) -> int:
        num_failed = 0
        for track in tracks:
            if not self.insert(track):
                num_failed += 1
        return num_failed

    @cast_as_track
    def get_by_id(self, track_id: str) -> List[Track]:
        # Search for track by ID
        return list(self._collection.find({'id': track_id}))

    @cast_as_track
    def query(self, **query: dict[str, Any]) -> List[Track]:
        # Search for track by multiple fields and values using kwargs
        return list(self._collection.find(query))

    @cast_as_track
    def get_all(self) -> List[Track]:
        # Get all tracks from the collection
        return list(self._collection.find())

    def update_by_id(self, track_id: str, **kwargs) -> None:
        # Retrieve track by ID
        results = self.get_by_id(track_id)

        # Ensure exactly one result is found
        if len(results) != 1:
            raise ValueError(f"Search doesn't have exactly one result: {len(results)} results")

        # Get the track object
        result = results[0]

        # Iterate over key-value pairs in kwargs to update fields
        for key, new_value in kwargs.items():
            # Ensure the key exists in the model
            if not hasattr(result, key):
                raise AttributeError(f"Track has no attribute '{key}'")

            # Set the new value
            setattr(result, key, new_value)

        # Update the entry in the MongoDB collection
        self._collection.update_one({'id': track_id}, {'$set': result.model_dump(mode="json")})

    def get_all_ids(self) -> list[str]:
        return [track.id for track in self.get_all()]
