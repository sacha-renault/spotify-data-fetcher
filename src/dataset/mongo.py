import os
import docker
import atexit

class MongoDocker:
    def __init__(self, path_volume: str):
        self.client = docker.from_env()
        self.path_volume = os.path.abspath(path_volume)
        self.container = None
        atexit.register(self.terminate)

    def start(self):
        """Start the MongoDB Docker container."""
        self.container = self.client.containers.run(
            "mongo:latest", 
            detach=True,  # Run container in detached mode
            ports={'27017/tcp': 27017},  # Expose port 27017 to localhost
            volumes={self.path_volume: {'bind': '/data/db', 'mode': 'rw'}}  # Persist data
        )
        return f"mongodb://localhost:{27017}"

    def terminate(self):
        """Stop and remove the MongoDB Docker container."""
        if self.container:
            print("MongoDB stopping.")
            self.container.stop()
            self.container.remove()
            print("MongoDB stopped.")
        self.container = None

    def __enter__(self):
        """Start the container when entering the context."""
        return self.start()

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensure the container is stopped and removed when exiting the context."""
        self.terminate()
