import discogs_client
from .config import DISCOGS_TOKEN, MAX_PROPOSED_LEN

from .models import Artist

import re


class App:
    def __init__(self):
        self._client = discogs_client.Client("Fetcher/1.0", user_token=DISCOGS_TOKEN)

    def _get_artists_by_name(self, name: str) -> list[Artist]:
        res = []

        artists = self._client.search(name, type="artist").page(1)

        for i in range(min(len(artists), MAX_PROPOSED_LEN)):
            current: discogs_client.Artist = artists[i]
            res.append(Artist(name=current.name, variations=current.name_variations))

        return res

    def select_artist(self, artist_name: str) -> None:
        artists = self._get_artists_by_name(artist_name)

        for i in range(len(artists)):
            print(f"[{i}] {artists[i].name}")

        current_artist = artists[
            max(0, min(MAX_PROPOSED_LEN - 1, int(input("select artist: "))))
        ]

        releases = self._client.search(
            type="master", format="album", artist=current_artist.name
        ).sort(key="year", order="asc")

        pat = rf"^({current_artist.aliases})\*?\s*-\s*(.+)$"
        artist_pat = re.compile(pat)

        target_albums = []

        for i in range(releases.pages):
            for master in releases.page(i):
                if artist_pat.match(master.title):
                    target_albums.append(master)

        for i in range(len(target_albums)):
            release = target_albums[i]
            print(f"[{i:02d}] {release.data.get('year', 0)} - {release.title}")
