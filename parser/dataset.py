import pandas as pd
from .yandex import search_playlists
from .tunebat import search_tracks, props_dict
import csv


def scrap_playlist_data(keyword, count=-1):
    tracks = search_playlists(keyword)
    results = []
    for i, track in enumerate(tracks):
        if i == count:
            break
        data = search_tracks(f"{track['title']} - {track['artists']}", 1)
        if i % 10 == 0:
            print(data)
        data["yt_track_id"] = track["id"]
        results.append(data)

    return results


def create_subset(query: list, label: str, count: int=10):
    cols = list(props_dict.values())
    rows = []
    f = open(f"{label}_temp.csv", "a+", newline="", encoding="utf-8")
    writer = csv.writer(f)

    for q in query:
        data = scrap_playlist_data(q, count=count)
        for track in data:
            rows.append(list(track.values()))
            writer.writerow(list(track.values()))

    df = pd.DataFrame(data=rows, columns=cols + ["yt_id"])
    df.to_csv(f"{label}.csv")

    return df

