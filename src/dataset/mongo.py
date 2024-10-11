from contextlib import contextmanager
import os
import docker

@contextmanager
def use_mongo_docker(path_volume: str):
    client = docker.from_env()
    
    # Run the MongoDB container with a volume and port binding
    container = client.containers.run(
        "mongo:latest", 
        detach=True,  # Run container in detached mode
        ports={'27017/tcp': 27017},  # Expose port 27017 to localhost
        volumes={os.path.abspath(path_volume): {'bind': '/data/db', 'mode': 'rw'}}  # Persist data
    )
    try:
        print("Mongo DB is running.")
        yield f"mongodb://localhost:{27017}"
    finally:
        # Stop and remove the container after use
        print("Mongo DB stopping.")
        container.stop()
        container.remove()
        print("Mongo DB stopped.")