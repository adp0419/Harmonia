# classifier.py
# -------------------
# Contains functions to load and process the sample playlist data.
# Includes logic to interpret playlist metadata and classify songs by given metrics.



import pandas as pd

def load_playlist(filepath):
    df = pd.read_csv(filepath)
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    playlist = df.to_dict(orient='records')
    return playlist

song_filters = {
    "sad": {"mode": 0, "valence_max": 0.4},
    "happy": {"mode": 1, "valence_min": 0.7},
    "fast": {"tempo_min": 120},
    "slow": {"tempo_max": 90},
    "loud": {"loudness_min": -10},
    "quiet": {"loudness_max": -30},   
}

def song_matches_filter(song, filters):
    for key, value in filters.items():
        if key.endswith('_min'):
            attr = key[:-4]
            if song.get(attr, song.get(attr.lower(), None)) is None:
                return False
            if song.get(attr, song.get(attr.lower())) < value:
                return False
        elif key.endswith('_max'):
            attr = key[:-4]
            if song.get(attr, song.get(attr.lower(), None)) is None:
                return False
            if song.get(attr, song.get(attr.lower())) > value:
                return False
        else:
            if song.get(key, song.get(key.lower(), None)) != value:
                return False
    return True

def filter_playlist(playlist, filters):
    if not filters or not isinstance(filters, dict):
        print(f"No valid filters provided, returning empty list.")
        return []

    filtered_songs = [song for song in playlist if song_matches_filter(song, filters)]
    
    if not filtered_songs:
        print(f"No songs match the given filters.")
    
    return filtered_songs

