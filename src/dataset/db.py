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

class MongoQuery:
    """
    Helper class for MongoDB query operators.
    
    Example Usage:
    
    >>> query = {"field": {MongoQuery.IN: [v1, v2, v3]}}
    >>> query = {"age": {MongoQuery.GT: 21}}
    >>> query = {MongoQuery.OR: [
            {"age": {MongoQuery.LT: 21}},
            {"status": "student"}
        ]}
    """
    
    # Comparison Operators
    EQ = "$eq"
    """Equal: Matches values that are equal to the specified value."""
    
    NE = "$ne"
    """Not Equal: Matches all values that are not equal to the specified value."""
    
    GT = "$gt"
    """Greater Than: Matches values that are greater than the specified value."""
    
    GTE = "$gte"
    """Greater Than or Equal: Matches values that are greater than or equal to the specified value."""
    
    LT = "$lt"
    """Less Than: Matches values that are less than the specified value."""
    
    LTE = "$lte"
    """Less Than or Equal: Matches values that are less than or equal to the specified value."""
    
    IN = "$in"
    """In: Matches any of the values specified in an array."""
    
    NIN = "$nin"
    """Not In: Matches none of the values specified in an array."""
    
    # Logical Operators
    AND = "$and"
    """Logical AND: Joins query clauses with a logical AND returns all documents that match the conditions of both clauses."""
    
    OR = "$or"
    """Logical OR: Joins query clauses with a logical OR returns all documents that match the conditions of either clause."""
    
    NOT = "$not"
    """Logical NOT: Inverts the effect of a query expression and returns documents that do not match the query expression."""
    
    NOR = "$nor"
    """Logical NOR: Joins query clauses with a logical NOR returns all documents that fail to match both clauses."""
    
    # Element Operators
    EXISTS = "$exists"
    """Exists: Matches documents that have the specified field."""
    
    TYPE = "$type"
    """Type: Selects documents if a field is of the specified type."""
    
    # Array Operators
    ALL = "$all"
    """All: Matches arrays that contain all elements specified in the query."""
    
    SIZE = "$size"
    """Size: Matches any array with the specified number of elements."""
    
    # Text Search Operators
    TEXT = "$text"
    """Text: Performs a text search on the content of the fields indexed with a text index."""
    
    # Modifiers
    REGEX = "$regex"
    """Regular Expression: Provides regular expression capabilities for pattern matching strings in queries."""
    
    OPTIONS = "$options"
    """Options: Specifies options for regular expression searches, such as case insensitivity."""



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

            # Get current value of the field
            current_value = getattr(result, key)

            # Check if the new value is of the same type as the current value
            if not isinstance(new_value, type(current_value)):
                raise TypeError(f"Type mismatch: '{key}' must be of type {type(current_value).__name__}, got {type(new_value).__name__}")

            # Set the new value
            setattr(result, key, new_value)

        # Update the entry in the MongoDB collection
        self._collection.update_one({'id': track_id}, {'$set': result.model_dump()})

    def get_all_ids(self) -> list[str]:
        return [track.id for track in self.get_all()]
