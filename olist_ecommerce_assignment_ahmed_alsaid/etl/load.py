from sqlalchemy import create_engine
from config import PG_DB_URL
from utils import logger

engine = create_engine(PG_DB_URL)

def load(df, table):
    df.to_sql(table, engine, if_exists='append', index=False, method='multi', chunksize=2000)
    logger.info(f"Loaded {len(df)} into {table}")