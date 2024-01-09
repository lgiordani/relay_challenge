import os

from src.application.app import create_app

app = create_app(os.environ["RELAY_API_CONFIG"])
