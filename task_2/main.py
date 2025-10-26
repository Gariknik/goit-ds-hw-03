from spiders import get_data_quotes, get_data_authors
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json
import os
from dotenv import load_dotenv


def main():
    """
    Головна функція програми
    """
    load_dotenv()
    CONN = os.getenv("CONN")
    client = MongoClient(
        CONN,
        server_api=ServerApi('1')
    )

    db = client.db_quotes
    get_data_quotes()
    get_data_authors()
    with open('quotes.json', 'r', encoding='utf-8')  as f:
        data = json.load(f)
        result = db.quotes.insert_many(data)
        print(f"✅ Успішно додано {len(result.inserted_ids)}")

    
    with open('authors.json', 'r', encoding='utf-8')  as f:
        data = json.load(f)
        result = db.authors.insert_many(data)
        print(f"✅ Успішно додано {len(result.inserted_ids)}")

    
    

if __name__ == "__main__":
    main()