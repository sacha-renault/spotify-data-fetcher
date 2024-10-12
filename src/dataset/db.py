from dataclasses import dataclass
from functools import wraps
from typing import Any, List
from pymongo import MongoClient
from .pytype import Track, TrackData


def cast_as_model(func):
    @wraps(func)
    def wrapper(self: Collection, *args, **kwargs):
        result = func(self, *args, **kwargs)
        model = self.model_class
        if isinstance(result, list):
            return [model.model_validate(document) for document in result]
        elif result is not None:
            return model.model_validate(result)
        return None
    return wrapper

class Collection:
    def __init__(self, db, collection_name: str, model_class):
        """Initialize a collection with an index on 'id' and a reference to the Pydantic model."""
        self._collection = db[collection_name]
        self._collection.create_index("id", unique=True)
        self.model_class = model_class

    def insert(self, document: Any) -> bool:
        """Insert a document if it doesn't already exist."""
        if not self.get_by_id(document.id):
            self._collection.insert_one(document.model_dump(mode="json"))
            return True
        return False

    def insert_many(self, documents: List[Any]) -> int:
        """Insert many documents and return the count of failed inserts."""
        num_failed = sum(0 if self.insert(doc) else 1 for doc in documents)
        return num_failed

    @cast_as_model
    def get_by_id(self, document_id: str) -> Track | None:
        """Get a document by its ID."""
        return self._collection.find_one({'id': document_id})
    
    @cast_as_model
    def get_all(self) -> Track | None:
        """Get all documents in the collection."""
        return list(self._collection.find())

    @cast_as_model
    def query(self, projection: dict = None, **query: dict[str, Any]) -> List[Track]:
        """Query the collection with optional projection and filters."""
        return list(self._collection.find(query, projection))

    def remove(self, document_id: str) -> bool:
        """Remove a document by its ID."""
        result = self._collection.delete_one({"id": document_id})
        return result.deleted_count > 0
    
    def get_all_ids(self) -> list[str]:
        # query id with hint and projection
        cursor = self._collection.find(
            {}, {"id": 1, "_id": 0}
        ).hint("id_1") 

        # return only id
        return [doc["id"] for doc in cursor]
    
class MetaCollection(Collection):
    """Collection specialized for metadat of tracks.
    """
    def __init__(self, db):
        super().__init__(db, "tracks", Track)

    def insert(self, document: Track) -> bool:
        # Try to insert new document
        if not super().insert(document):
            self._collection.update_one(
                {"id": document.id},  # Find by ID
                {"$addToSet": {"genres": {"$each": list(document.genres)}}}  # Update genres
            )
            return False # was an update
        return True # was inserted
        
class DataCollection(Collection):
    def __init__(self, db):
        super().__init__(db, "data", TrackData)


@dataclass
class Database:
    meta: MetaCollection
    data: DataCollection

def init_database(db_uri: str):
    client = MongoClient(db_uri)
    db = client["music_database"]
    return Database(
        MetaCollection(db),
        DataCollection(db)
    )