# Audio Metadata and Data Collection with MongoDB

## Purpose

The idea behind this project is to create a reliable way to collect and store audio track metadata and preview data for future **AI experiments**. I’m not entirely sure yet what specific AI applications I’ll be building, but whether it's audio classification, recommendation systems, or something else, I needed a strong foundation to access and manage audio data.

By using MongoDB for storage and Spotify as the source of the track info and previews, this setup allows me to easily gather and organize everything I need for any potential AI task involving audio. This system is built to handle large amounts of track metadata and audio preview data efficiently.

## Features

- Track Metadata Collection: Retrieves track metadata (e.g., title, artist, album, genres) using the Spotify API.
- Audio Preview Data Collection: Downloads and stores audio previews as Base64-encoded data for easy integration with MongoDB.
- Efficient Storage: Metadata and preview data are stored separately, making it easy to query and manage large datasets.
- Support for Multiple Genres: Collect metadata for tracks belonging to any specified genres, with customizable paging options to retrieve data in bulk.
- Progress Tracking: Uses progress bars to show real-time progress while collecting track data and audio previews.

## Installation

- Clone the Repository: git clone <repository-url> cd <repository-directory>

- Install Dependencies: Use pip to install the necessary dependencies: pip install -r requirements.txt

- Set Up MongoDB: Ensure you have a running MongoDB instance, either locally or remotely, and update the connection URI in the project configuration:

  - ensure docker is running.
  - mongoDB will store data in a volume in a local directory.

    - you can either use context manager :

    ```py
    with MongoDocker(path_volume"./data") as db_uri: # with return the uri of the db
        db = init_database(db_uri)
        # do something
    ```

    - or use it with start and termintate

    ```py
    mongo_docker = MongoDocker(path_volume = "./data")
    db_uri = mongo_docker.start()
    # DO THIGNS
    mongo_docker.terminate()
    ```

  - alternatively, you can setup any mongodb you want and use directly this uri.

- Set Up Spotify API:

  - Register your application at Spotify for Developers.
  - Get your client_id and client_secret.
  - Use these credentials to authenticate and access the Spotify API.
  - set them up in a `.env` file at root of directory

  ```.env
  SPOTIFY_ID=<YOUR_ID>
  SPOTIFY_SECRET=<YOUR_SECRET>
  ```

## Usage

### Filling the Database with Track Metadata

The fill_db function fetches metadata for tracks based on the specified genres and stores the data in the MongoDB database. You can customize the number of pages (results per genre) to fetch. Each page contains a fixed number of tracks.

```py
def fill_db(database: Database, spotify_client: SpotifyClient, genres: list[str], pages: int = 20) -> None:
# Usage example: fill_db(database, spotify_client, ["rock", "electronic"], pages=10)
```

### Filling the Database with Audio Previews

Once the metadata is filled, you can use the fill_previews_data function to download and store the audio previews for tracks that have a valid preview_url.

```py
def fill_previews_data(database: Database) -> None
```

# Usage example: fill_previews_data(database)

## Next Steps

- Exploration of AI Models: With the track metadata and audio previews in place, the next step is to explore AI models that can analyze, classify, or generate insights from this data.
- Data Enrichment: Enhance metadata with additional information, such as popularity scores or artist-related data.
