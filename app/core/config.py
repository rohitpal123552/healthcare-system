import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    PGUSER = os.getenv('PGUSER','healthuser')
    PGPASSWORD = os.getenv('PGPASSWORD','healthpass')
    PGHOST = os.getenv('PGHOST','localhost')
    PGPORT = os.getenv('PGPORT','5432')
    PGDB = os.getenv('PGDB','healthdb')
    MONGO_HOST = os.getenv('MONGO_HOST','localhost')
    MONGO_PORT = int(os.getenv('MONGO_PORT',27017))
    MONGO_DB = os.getenv('MONGO_DB','healthdb')

settings = Settings()
