from pathlib import Path
import discogs_client  # type: ignore

from .config import DISCOGS_TOKEN, MAX_PROPOSED_LEN, IMAGE_SIZE_STUB

from .models import Artist, Album, Image, Tracklist, Track

import re

from .output import track_tags_to_output

from .cache import cache


class App:
    def __init__(self, target_dir: Path):
        self._client = discogs_client.Client("Fetcher/1.0", user_token=DISCOGS_TOKEN)
        self._target_dir = target_dir

    @cache
    def _get_artists_by_name(self, name: str) -> list[Artist]:
        res = []

        artists = self._client.search(name, type="artist").page(1)

        for i in range(min(len(artists), MAX_PROPOSED_LEN)):
            current: discogs_client.Artist = artists[i]
            res.append(Artist(name=current.name, variations=current.name_variations))

        return res

    @cache
    def _get_albums_by_artist(self, artist: Artist) -> list[Album]:
        releases = self._client.search(
            type="master", format="album", artist=artist.name
        ).sort(key="year", order="asc")

        pattern = re.compile(rf"^({artist.aliases})\*?\s*\S+\s*(.+)$")

        target_albums = []

        for i in range(releases.pages):
            for master in releases.page(i):
                title_match = pattern.match(master.title)
                if title_match:
                    try:
                        target_albums.append(
                            Album(
                                id=master.id,
                                title=title_match.group(2),
                                year=master.data.get("year", 0),
                                genres=master.data.get("genre", None),
                                styles=master.data.get("style", None),
                                thumb=master.data.get("thumb", ""),
                                artist=artist.name,
                            ),
                        )
                    except Exception:
                        pass

        return target_albums

    @cache
    def _get_cover_image(self, album_id: int) -> Image:
        master = self._client.master(album_id)

        images = master.images
        try:
            for image in images:
                if image.get("type", "") == "primary":
                    return Image(
                        url=image.get("resource_url", ""),
                        width=int(image.get("width", IMAGE_SIZE_STUB)),
                        height=int(image.get("height", IMAGE_SIZE_STUB)),
                    )

            if len(images) > 0:
                return Image(
                    url=images[0].get("resource_url", ""),
                    width=int(images[0].get("width", IMAGE_SIZE_STUB)),
                    height=int(images[0].get("height", IMAGE_SIZE_STUB)),
                )
        except Exception:
            return Image()
        return Image()

    @cache
    def _get_tracklist(self, album_id: int) -> Tracklist:
        master = self._client.master(album_id)

        return Tracklist(
            tracks=[Track(title=track.title) for track in master.tracklist]
        )

    @track_tags_to_output
    def get_track_tags_by_artist(
        self, artist_name: str
    ) -> tuple[Album, Image, Tracklist]:
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

        image = self._get_cover_image(current_album.id)
        tracks = self._get_tracklist(current_album.id)

        return (current_album, image, tracks)
