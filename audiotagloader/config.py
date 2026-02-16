from dotenv import load_dotenv
import os

load_dotenv()

DISCOGS_TOKEN = os.environ["DISCOGS_TOKEN"]
MAX_PROPOSED_LEN = int(os.environ["MAX_PROPOSED_LEN"])
