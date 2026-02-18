import discogs_client  # type: ignore

from .config import DISCOGS_TOKEN, MAX_PROPOSED_LEN

from .models import Artist, Album

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

    def _get_albums_by_artist(self, artist: Artist) -> list[Album]:
        releases = self._client.search(
            type="master", format="album", artist=artist.name
        ).sort(key="year", order="asc")

        pattern = re.compile(rf"^({artist.aliases})\*?\s*-\s*(.+)$")

        target_albums = []

        for i in range(releases.pages):
            for master in releases.page(i):
                title_match = pattern.match(master.title)
                if title_match:
                    target_albums.append(
                        Album(
                            title=title_match.group(0),
                            year=master.data.get("year", 0),
                            genres=master.data.get("genre", None),
                            styles=master.data.get("style", None),
                            thumb=master.data.get("thumb", None),
                            cover=master.data.get("cover", None),
                        )
                    )

        return target_albums

    def select_artist(self, artist_name: str) -> None:
        artists = self._get_artists_by_name(artist_name)

        for i in range(len(artists)):
            print(f"[{i}] {artists[i].name}")

        current_artist = artists[
            max(0, min(MAX_PROPOSED_LEN - 1, int(input("select artist: "))))
        ]

        albums = self._get_albums_by_artist(current_artist)

        for i in range(len(albums)):
            print(f"[{i:02d}] {albums[i].year} - {albums[i].title}")

        current_album = albums[
            max(0, min(len(albums) - 1, int(input("select album: "))))
        ]

        print(current_album)
