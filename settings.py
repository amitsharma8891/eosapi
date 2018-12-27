import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


SERVER_HOST=os.getenv('SERVER_HOST')
PORT=int(os.getenv('PORT'))
