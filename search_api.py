import json
import numpy as np
import torch
from flask import Flask, request, jsonify
from transformers import CLIPProcessor, CLIPModel
from numpy.linalg import norm

# ---------------------------
# Load the CLIP Model
# ---------------------------
MODEL_NAME = "openai/clip-vit-base-patch32"
device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model = CLIPModel.from_pretrained(MODEL_NAME)
clip_processor = CLIPProcessor.from_pretrained(MODEL_NAME)
clip_model.to(device)

# ---------------------------
# Utility Functions
# ---------------------------

def compute_text_embedding(text):
    """
    Compute a text embedding using CLIP's text encoder.
    """
    inputs = clip_processor(
        text=[text],
        return_tensors="pt",
        truncation=True,
        max_length=77
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        text_features = clip_model.get_text_features(**inputs)
    return text_features.cpu().numpy()[0]

def cosine_similarity(a, b):
    """
    Compute cosine similarity between two vectors.
    """
    if norm(a) == 0 or norm(b) == 0:
        return 0.0
    return np.dot(a, b) / (norm(a) * norm(b))

# ---------------------------
# Load Hotel Data and Embeddings
# ---------------------------

def load_hotel_data(file_path="data/hotels.json"):
    """
    Load complete hotel data from JSON.
    """
    with open(file_path, "r") as f:
        data = json.load(f)
    return {hotel["HotelCode"]: hotel for hotel in data.get("detail", [])}  # Store by Hotel ID

def load_hotel_embeddings(file_path="data/hotel_embeddings.json"):
    """
    Load precomputed embeddings for hotels.
    """
    with open(file_path, "r") as f:
        hotels = json.load(f)
    for hotel in hotels:
        hotel["embedding"] = np.array(hotel["embedding"])  # Convert to NumPy array
    return hotels

# Load full hotel data and embeddings
hotel_data = load_hotel_data("data/hotels.json")
hotels = load_hotel_embeddings("data/hotel_embeddings.json")

# ---------------------------
# Flask API
# ---------------------------
app = Flask(__name__)

@app.route("/search", methods=["POST"])
def search_hotels():
    """
    API Endpoint to search for hotels using CLIP embeddings.
    Expects a JSON payload with "query" and optional "top_k".
    Example usage:
    ```
    POST /search
    {
        "query": "Luxury hotel in Paris",
        "top_k": 5
    }
    ```
    """
    try:
        data = request.get_json()
        if not data or "query" not in data:
            return jsonify({"error": "Request must contain 'query' in the JSON body."}), 400

        query = data["query"].strip()
        top_k = int(data.get("top_k", 5))

        if not query:
            return jsonify({"error": "Query must be a non-empty string."}), 400

        query_emb = compute_text_embedding(query)

        results = []
        for hotel in hotels:
            sim = cosine_similarity(query_emb, hotel["embedding"])
            hotel_id = hotel.get("HotelCode", "N/A")
            
            # Retrieve full hotel details from hotel_data
            full_hotel_info = hotel_data.get(hotel_id, {})
            
            results.append({
                "HotelID": hotel_id,
                "HotelName": full_hotel_info.get("HotelName", "N/A"),
                "Address": full_hotel_info.get("Address", "N/A"),
                "CityName": full_hotel_info.get("CityName", "N/A"),
                "CountryName": full_hotel_info.get("CountryName", "N/A"),
                "HotelFacilities": full_hotel_info.get("HotelFacilities", []),
                "Description": full_hotel_info.get("Description", "N/A"),
                "Similarity": sim
            })

        results.sort(key=lambda x: x["Similarity"], reverse=True)
        return jsonify(results[:top_k])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
