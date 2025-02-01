import json
import numpy as np
import torch
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
        max_length=77  # CLIP's default max_length for text
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        text_features = clip_model.get_text_features(**inputs)
    return text_features.cpu().numpy()[0]

def load_hotel_data(file_path="data/hotels.json"):
    """
    Load hotel data from a JSON file.
    """
    with open(file_path, "r") as f:
        data = json.load(f)
    return data.get("detail", [])

def preprocess_hotel(hotel):
    """
    Combine multiple hotel fields into one searchable text.
    """
    fields = []
    for key in ["HotelName", "Description", "HotelFacilities", "Address", "CityName", "CountryName"]:
        val = hotel.get(key, "")
        if isinstance(val, list):
            val = " ".join(val)
        fields.append(str(val))
    return " ".join(fields).strip()

def build_hotel_embeddings(hotels):
    """
    Compute and store embeddings for all hotels.
    """
    for hotel in hotels:
        combined_text = preprocess_hotel(hotel)
        text_emb = compute_text_embedding(combined_text)
        hotel["embedding"] = text_emb.tolist()  # Convert to list for JSON storage
    return hotels

# ---------------------------
# Compute and Save Embeddings
# ---------------------------
def main():
    hotels = load_hotel_data("data/hotels.json")
    if not hotels:
        print("No hotel data found. Please check your JSON file.")
        return

    print("Computing embeddings for hotels...")
    hotels = build_hotel_embeddings(hotels)

    # Save with embeddings
    with open("data/hotel_embeddings.json", "w") as f:
        json.dump(hotels, f)

    print("Embeddings saved to 'data/hotel_embeddings.json'.")

if __name__ == "__main__":
    main()
