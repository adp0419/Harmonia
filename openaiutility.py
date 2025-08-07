# openai-utility.py
# -------------------
# Contains functions to interact with the OpenAI API.
# Handles prompt construction, API requests, and response parsing for song categorization.

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def openai_metric_filter(user_prompt):
    """
    Building the prompt to tell OpenAI to come up with metadata metrics based on user input.
    """
    system_prompt = (
       """
       You are a music mood classifier assistant designed to interpret user mood descriptions and return an appropriate set of audio feature filters for a music recommendation system.
        
       ## Your Goal:
       Given a user's description of the music they want (e.g., "I want upbeat music for a sunny day"), return a valid **Python dictionary** containing **only relevant filters** for Spotify audio features.

       ## Only Use These Keys:
       You can include **any combination** of the following keys as needed:

       - valence_min / valence_max  → mood positivity (0 = sad, 1 = happy)
       - energy_min / energy_max    → intensity and activity (0 = calm, 1 = energetic)
       - tempo_min / tempo_max      → BPM (beats per minute, typically 60–200)
       - danceability_min / max     → how danceable a track is (0 to 1)
       - acousticness_min / max     → acoustic vs synthetic (0 = synthetic, 1 = acoustic)
       - loudness_min / loudness_max → measured in dB (approx -60 to 0; louder tracks are closer to 0)
       - instrumentalness_min / max → whether a track is mostly instrumental (0 to 1)
       - mode                       → 0 = minor (sad, serious), 1 = major (happy, bright)
       - speechiness_min / max      → talkiness in track (0 = musical, >0.5 = speech-like)

       ## Reference Value Ranges:
       - valence: 0 (very sad) to 1 (very happy)
       - energy: 0 (low) to 1 (high)
       - tempo: typically 60 (slow) to 200 (fast)
       - loudness: -60 dB (quiet) to 0 dB (loud)
       - acousticness: 0 (electronic) to 1 (acoustic)
       - danceability: 0 (not danceable) to 1 (very danceable)
       - instrumentalness: 0 (vocal) to 1 (instrumental)

       ## How to Think:
       - Interpret ambiguous language carefully. Guess intelligently if needed.
       - Examples:
       - “Sad song” → valence_max ≈ 0.3, mode = 0, energy_max ≈ 0.4
       - “High-energy gym music” → energy_min ≈ 0.7, tempo_min ≈ 130, loudness_min ≈ -5
       - “Rainy day background music” → energy_max ≈ 0.4, acousticness_min ≈ 0.5, instrumentalness_min ≈ 0.3
       - “Loud and intense” → loudness_min ≈ -5, energy_min ≈ 0.8
       - “Chill study music” → tempo_max ≈ 100, energy_max ≈ 0.5, instrumentalness_min ≈ 0.4, acousticness_min ≈ 0.3

       ## Constraints:
       - DO NOT include explanation, description, or apologies.
       - DO NOT include non-audio features like track name or artist.
       - DO NOT make up field names.
       - Return ONLY a Python dictionary. Nothing else.
       """
    )

    response = client.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"User input: {user_prompt}"}
        ],
        temperature=0.3  # Lower temperature for more deterministic responses
    )

    content = response.choices[0].message.content

    try:
        filters = eval(content)
        if isinstance(filters, dict):
            return filters
        else:
            print("Error: OpenAI response is not a dictionary.")
            return {}
    except Exception as e:
        print(f"Error: failed to parse OpenAI response: {e}")
        print("Raw content was:", content)
        return {}
