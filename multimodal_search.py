import json
import numpy as np
import torch
from transformers import CLIPProcessor, CLIPModel
from numpy.linalg import norm

# ---------------------------
# 1. Load the CLIP Model for Text Encoding
# ---------------------------

MODEL_NAME = "openai/clip-vit-base-patch32"
device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model = CLIPModel.from_pretrained(MODEL_NAME)
clip_processor = CLIPProcessor.from_pretrained(MODEL_NAME)
clip_model.to(device)

# ---------------------------
# 2. Utility Functions
# ---------------------------

def compute_text_embedding(text):
    """
    Compute a text embedding using CLIP's text encoder.
    Explicitly enables truncation to avoid warnings.
    """
    inputs = clip_processor(
        text=[text],
        return_tensors="pt",
        truncation=True,
        max_length=77  # CLIP's default max_length for text
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
# 3. Data Preprocessing Functions
# ---------------------------

def load_hotel_data(file_path="data/hotels.json"):
    """
    Load hotel data from a JSON file.
    Expects the JSON to have a top-level key "detail" containing a list of hotels.
    """
    with open(file_path, "r") as f:
        data = json.load(f)
    return data.get("detail", [])

def preprocess_hotel(hotel):
    """
    Combine multiple hotel fields into one searchable text.
    Adjust the field names according to your JSON.
    """
    fields = []
    # Using keys that exist in your data; note that JSON keys are case-sensitive.
    for key in ["HotelName", "Description", "HotelFacilities", "Address", "CityName", "CountryName"]:
        val = hotel.get(key, "")
        if isinstance(val, list):
            val = " ".join(val)
        fields.append(str(val))
    return " ".join(fields).strip()

def build_hotel_embeddings(hotels):
    """
    For each hotel, compute a text embedding from the combined hotel text.
    The final embedding is stored in the hotel dictionary under the key "embedding".
    """
    for hotel in hotels:
        combined_text = preprocess_hotel(hotel)
        text_emb = compute_text_embedding(combined_text)
        hotel["embedding"] = text_emb
    return hotels

# ---------------------------
# 4. Search and Ranking Functions
# ---------------------------

def search_hotels(hotels, query, top_k=5):
    """
    Given a list of hotels (with precomputed embeddings) and a text query,
    compute the query embedding and return the top_k hotels sorted by cosine similarity.
    """
    query = query.strip()
    if not query:
        raise ValueError("Query must be a non-empty string.")
    query_emb = compute_text_embedding(query)
    results = []
    for hotel in hotels:
        sim = cosine_similarity(query_emb, hotel["embedding"])
        hotel["similarity"] = sim
        results.append(hotel)
    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:top_k]

# ---------------------------
# 5. Main Function
# ---------------------------

def main():
    # Load the hotel data from JSON.
    hotels = load_hotel_data("data/hotels.json")
    if not hotels:
        print("No hotel data found. Please check your JSON file.")
        return

    print("Precomputing text embeddings for all hotels (this may take a while)...")
    hotels = build_hotel_embeddings(hotels)
    print("Embeddings computed.")

    # Get user query.
    query = input("Enter your hotel search query: ").strip()
    if not query:
        print("Query cannot be empty!")
        return

    # Search for hotels.
    top_hotels = search_hotels(hotels, query, top_k=5)

    # Display results.
    print("\nTop Hotel Results:")
    for i, hotel in enumerate(top_hotels):
        print(f"{i+1}. {hotel.get('HotelName', 'N/A')} (Similarity: {hotel['similarity']:.3f})")
        snippet = preprocess_hotel(hotel)[:150]
        print(f"   {snippet}...\n")

if __name__ == "__main__":
    main()
