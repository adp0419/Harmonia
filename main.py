from classifier import load_playlist

playlist = load_playlist("sample-playlist.csv")

for song in playlist[:2]:
    print(song)
