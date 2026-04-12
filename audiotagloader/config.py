from dotenv import load_dotenv
import os

load_dotenv(".config")
load_dotenv(".secrets")

DISCOGS_TOKEN = os.environ["DISCOGS_TOKEN"]
MAX_PROPOSED_LEN = int(os.environ["MAX_PROPOSED_LEN"])

PERMITTED_IMAGE_EXTS = os.environ["PERMITTED_IMAGE_EXTS"].split(",")
IMAGE_SIZE_STUB = int(os.environ["IMAGE_SIZE_STUB"])

REDIS_PASSWORD = os.environ["REDIS_PASSWORD"]
REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = int(os.environ["REDIS_PORT"])
