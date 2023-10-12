from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from poe_trade.poe_trade import PoeTrade
import os
from tqdm import tqdm

class MongoDB:
  def __init__(self, price_checker: PoeTrade):
      self.poe_trade = price_checker

  def connect(self):
    account = os.getenv('DB_ACCOUNT')
    password = os.getenv('DB_PASSWORD')
    uri = f"mongodb+srv://{account}:{password}@cluster0.nalsnoj.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi("1"))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    db = client["exile_profit"]  # Replace with your database name

    # Select the collection you want to query
    collection = db["divination_cards_queries"]  # Replace with your collection name

    # Define your query
    query = {}  # Replace with your specific query criteria

    # Execute the query and retrieve the data
    results = collection.find(query)

    # Iterate through the results
    for document in tqdm(results, desc="DB: "):
        type = document["type"]
        status = document["status"]
        stats = document["stats"]
        filters = document["filters"]

        # print(f"Type: {type}")
        # print(f"Status: {status}")
        # print(f"Stats: {stats}")
        # print(f"Filters: {filters}")

        query = {
            "query": {
                "status": status,
                "type": type,
                "stats": stats,
                "filters": filters,
            },
            "sort": {"price": "asc"},
        }

        average_price, total_listed = self.poe_trade.get_item_price(query)

        # Create a document to insert
        document = {
            "type": type,
            "price": average_price,
            "listed": total_listed,
        }

        collection_div_prices = db["divination_cards_prices"]

        # Insert the document into the collection
        result = collection_div_prices.insert_one(document)
        
        print(f"Inserted document with ID: {result.inserted_id}")
        break

    client.close()