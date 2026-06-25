from sqlalchemy import create_engine
from src.core.settings import configs

def get_engine():
    return create_engine(configs.DB_URL, echo = True if configs.ENV == "dev" else False)
