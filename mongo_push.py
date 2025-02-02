from pymongo import MongoClient
import json

# MongoDB Configuration
MONGO_URI = "mongodb+srv://Sarthak:rwUJw01ToJWgK7WZ@cluster0.zrgbq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "TBO"
COLLECTION_NAME = "Hotels"
JSON_FILE_PATH = "data/hotels.json"  # Update with correct path

def load_and_transform_json(file_path):
    """
    Load and transform hotel JSON data to match MongoDB format.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict) or "detail" not in data:
            raise ValueError("Invalid JSON structure. Expected a dictionary with a 'detail' key.")

        hotels = data["detail"]

        # Transform data: Ensure each document has a unique "_id"
        for hotel in hotels:
            if "HotelCode" in hotel:
                hotel["_id"] = hotel["HotelCode"]  # Use HotelCode as _id
        
        with open("data/hotel.json", "w") as f:
            json.dump(hotels, f)

        return hotels

    except json.JSONDecodeError as e:
        print(f"❌ JSON Decode Error: {e}")
        return []
    except FileNotFoundError:
        print(f"❌ Error: The file '{file_path}' was not found.")
        return []
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return []

def insert_json_to_mongodb(json_data):
    """
    Insert transformed JSON data into MongoDB collection.
    """
    if not json_data:
        print("⚠️ No valid data to insert.")
        return

    try:
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]

        # Insert transformed data
        collection.insert_many(json_data, ordered=False)  # ordered=False allows skipping duplicates
        print(f"✅ Successfully inserted {len(json_data)} documents into MongoDB.")

    except Exception as e:
        print(f"❌ Error inserting data into MongoDB: {e}")

    finally:
        client.close()

if __name__ == "__main__":
    # Load and transform JSON
    hotel_data = load_and_transform_json(JSON_FILE_PATH)

    # Insert into MongoDB
    insert_json_to_mongodb(hotel_data)
