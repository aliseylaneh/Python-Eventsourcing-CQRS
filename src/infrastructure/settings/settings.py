from dotenv import load_dotenv

import os

load_dotenv()
ENVIRONMENT = os.getenv('environment')
SQLALCHEMY_DATABASE_URL = 'postgresql://app_store:1234@localhost:5432/store'
