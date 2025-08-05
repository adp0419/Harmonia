import pandas as pd

def load_playlist(filepath):
    df = pd.read_csv(filepath)

    df.columns = [col.strip() for col in df.columns]

    playlist = df.to_dict(orient='records')

    return playlist


