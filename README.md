# LLM-Based Hotel Search

## Overview
This project enhances the hotel search experience by eliminating traditional filter options and introducing an LLM-based search system. Instead of manually selecting filters, users can provide a natural language description of their ideal hotel, and the system intelligently retrieves the most relevant results using vector-based similarity matching.

## Built For
This project was developed as part of the **TBO Hackathon**.

## How It Works
### Backend Workflow
1. **Precomputing Hotel Feature Vectors**
   - Features of hotels are extracted from the dataset and converted into vector representations.
   - These vectors are stored in a **MongoDB** database for fast retrieval.

2. **User Query Processing**
   - The user provides a hotel description in natural language.
   - The system vectorizes this description.

3. **Similarity Matching**
   - The vectorized user query is compared with precomputed hotel feature vectors using **cosine similarity**.
   - The hotels with the highest similarity scores are returned as the best-matched results.

## Tech Stack
### Backend
- **Node.js & Express** for server-side handling
- **Flask** for RESTful API services
- **MongoDB** for storing precomputed hotel feature vectors
- **Vectorization Techniques** for text embeddings
- **Cosine Similarity** for relevance scoring

### Frontend
- **Pug** for templating and rendering the user interface

## Setup Instructions
1. Clone this repository:
   ```sh
   git clone https://github.com/Anubhav-Vashishtha/TBO-Hacthon
   cd TBO-Hacthon
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt  # Install Flask dependencies
   npm install  # Install Node.js dependencies
   ```
3. Run the backend server:
   ```sh
   python search_api.py  # Start Flask backend
   node app.js  # Start Node.js backend
   ```
4. Use the API endpoint to query hotels using natural language descriptions.

## Future Improvements
- Implement real-time updates to hotel vectors
- Enhance the search experience with multi-modal inputs (e.g., images, voice)
- Optimize the query processing pipeline for scalability

## Contributing
Feel free to raise issues or submit pull requests to enhance this project.

