from os.path import join, dirname

from dotenv import load_dotenv

import os

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)
ENVIRONMENT = os.environ.get('ENVIRONMENT')
DATABASE_URL = os.environ.get("DATABASE_URL")
