import os
from dotenv import load_dotenv
load_dotenv(verbose=True)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
