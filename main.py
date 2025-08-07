# main.py
# -------------------
# Main entry point for the project.
# Loads the playlist data and handles overall program flow.
# This is where the core functions will be called and responses managed.



from classifier import load_playlist, filter_playlist
from openaiutility import openai_metric_filter


def main():
    filepath = "sample-playlist.csv" # Replace if your file has a different name
    playlist = load_playlist(filepath)

    mood = input("Describe the kind of music you are in the mood for: ").strip()

    try:
        print("\nInterpreting your request using AI...")
        mood_filter = openai_metric_filter(mood)
        print(f"\nFilter criteria generated: {mood_filter}")
    except Exception as e:
        print(f"Failed to generate a filter for your request: {e}")
        return
    
    filtered_songs = filter_playlist(playlist, mood_filter)

    if not filtered_songs:
        print("\nNo songs found matching your request.")
    else:
        print("\nSongs matching your request:")
        for i, song in enumerate(filtered_songs, 1):
            title = song.get("track_name", "Unknown")
            artist = song.get("artist_name(s)", "Unknown")
            print(f"{i}. {title} - {artist}")

if __name__ == "__main__":
    main()





