from dotenv import load_dotenv

import os

load_dotenv()
ENVIRONMENT = os.getenv('environment')
SQLALCHEMY_DATABASE_URL = "postgresql://novapardaz:novapardaz@1234@localhost:5432/store"
match ENVIRONMENT:
    case 'production':
        SQLALCHEMY_DATABASE_URL = 'postgresql://novapardaz:novapardaz@1234@store-db.novapardaz.svc:5432/store'
    case 'local':
        SQLALCHEMY_DATABASE_URL = 'postgresql://novapardaz:novapardaz@1234@localhost:5432/store'
