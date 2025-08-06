# main.py
# -------------------
# Main entry point for the project.
# Loads the playlist data and handles overall program flow.
# This is where the core functions will be called and responses managed.



from classifier import load_playlist, filter_playlist

def main():
    filepath = "sample-playlist.csv" # Replace if your file has a different name
    playlist = load_playlist(filepath)

    mood = input("Enter the mood you want to filter by (e.g., sad, happy, fast, slow, loud, quiet): ").strip()

    filtered_songs = filter_playlist(playlist, mood)

    if not filtered_songs:
        print(f"No songs found for the mood: '{mood}'")
    else:
        print(f"Songs matching the mood '{mood}':")
        for i, song in enumerate(filtered_songs, 1):
            print(f"{i}. {song.get('track_name', 'Unknown')} - {song.get('artist_name(s)', 'Unknown')}")

if __name__ == "__main__":
    main()

