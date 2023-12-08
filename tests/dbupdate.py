from pymongo import MongoClient


def main():
    # Set up the MongoDB client
    client = MongoClient(
        "mongodb+srv://vyaryw:JKDmqN07j7YuwV62@cluster0.nalsnoj.mongodb.net/"
    )

    # Select the database and collection
    database = client["exile_profit"]
    collection = database["gems"]

    # Define the filter to find the document with the name "Ancestral Cry"
    filter = {"name": "Ancestral Cry"}

    # Define the update to set the "buy_price" to 20
    update = {"$set": {"buy_price": 20}}

    # Perform the update operation
    result = collection.update_one(filter, update)

    # Print the number of documents updated
    print(
        f"Matched {result.matched_count} document and modified {result.modified_count} document."
    )


if __name__ == "__main__":
    main()
