from app.parse import Parser
from app.config import BASE_URL
from app.db.database import Base
from app.db.database import engine
from app.db.models import product
from app.logger import logger
import json

parser = Parser(BASE_URL)

if __name__ == "__main__":
    logger.info("Creating database...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database created successfully.")

    catalogs = parser.get_catalog()
    for catalog in catalogs:
        products = parser.parse_catalog(catalog['href'], catalog['id'])
        logger.info(f"Catalog: {catalog['title']}, Products found: {len(products)}")

    parser.close()
    logger.info("Parser closed successfully.")
    
        
