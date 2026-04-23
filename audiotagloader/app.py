from pathlib import Path
import discogs_client  # type: ignore

from .config import DISCOGS_TOKEN, MAX_PROPOSED_LEN, IMAGE_SIZE_STUB

from .models import Artist, Album, Image, Tracklist, Track, ReleaseType, ReleaseList

import re

from .output import track_tags_to_output, releases_to_output

from .cache import cache

import questionary

custom_style = questionary.Style(
    [
        ("selected", "#ffffff bg:#0066cc"),
        ("highlighted", "#ffffff bg:#0066cc"),
        ("pointer", "#ff0000 bold"),
    ]
)


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

        target_albums = set()

        for i in range(releases.pages):
            for master in releases.page(i):
                title_match = pattern.match(master.title)
                if title_match:
                    try:
                        target_albums.add(
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

        return sorted([i for i in target_albums], key=lambda x: x.year)

    @cache
    def _get_album_by_id(
        self, master_id: int, type: ReleaseType = ReleaseType.MASTER
    ) -> Album:
        master = (
            self._client.master(master_id)
            if type == ReleaseType.MASTER
            else self._client.release(master_id)
        )
        print(
            master.genres,
            master.styles,
            master.data.get("genre", None),
            master.data.get("style", None),
        )
        return Album(
            id=master.id,
            title=master.title,
            year=master.data.get("year", 0),
            genres=master.genres,
            styles=master.styles,
            thumb=master.data.get("thumb", ""),
            artist="VA",
        )

    @cache
    def _get_cover_image(
        self, album_id: int, type: ReleaseType = ReleaseType.MASTER
    ) -> Image:
        master = (
            self._client.master(album_id)
            if type == ReleaseType.MASTER
            else self._client.release(album_id)
        )
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
    def _get_tracklist(
        self, album_id: int, type: ReleaseType = ReleaseType.MASTER
    ) -> Tracklist:
        master = (
            self._client.master(album_id)
            if type == ReleaseType.MASTER
            else self._client.release(album_id)
        )

        return Tracklist(
            tracks=[Track(title=track.title) for track in master.tracklist]
        )

    @track_tags_to_output
    def get_track_tags_by_artist(
        self, artist_name: str
    ) -> tuple[Album, Image, Tracklist]:
        artists = self._get_artists_by_name(artist_name)

        choices = []
        for i, artist in enumerate(artists):
            choices.append(
                questionary.Choice(title=f"[{i:02d}] {artist.name}", value=artist)
            )

        current_artist = questionary.select(
            "Select artist:",
            style=custom_style,
            choices=choices,
        ).ask()

        albums = self._get_albums_by_artist(current_artist)

        max_title_len = min(max(max(len(a.title) for a in albums), 40), 40)

        choices = []
        for i, album in enumerate(albums):
            title = album.title
            if len(title) > 40:
                title = title[:37] + "..."
            title_str = (
                f"[{i:02d}] {album.year:04d} - {title:<{max_title_len}} - {album.id}"
            )

            choices.append(questionary.Choice(title=title_str, value=album))

        current_album = questionary.select(
            "Select album:",
            style=custom_style,
            choices=choices,
        ).ask()

        image = self._get_cover_image(current_album.id)
        tracks = self._get_tracklist(current_album.id)

        self._get_releases_by_master_id(current_album.id)

        return (current_album, image, tracks)

    @track_tags_to_output
    def get_track_tags_by_master_id(
        self, master_id: int
    ) -> tuple[Album, Image, Tracklist]:
        current_album = self._get_album_by_id(master_id)
        image = self._get_cover_image(current_album.id)
        tracks = self._get_tracklist(current_album.id)

        self._get_releases_by_master_id(master_id)

        return (current_album, image, tracks)

    @track_tags_to_output
    def get_track_tags_by_release_id(
        self, release_id: int
    ) -> tuple[Album, Image, Tracklist]:
        current_album = self._get_album_by_id(release_id, ReleaseType.RELEASE)
        image = self._get_cover_image(current_album.id, ReleaseType.RELEASE)
        tracks = self._get_tracklist(current_album.id, ReleaseType.RELEASE)

        return (current_album, image, tracks)

    @releases_to_output
    @cache
    def _get_releases_by_master_id(self, master_id: int) -> ReleaseList:
        res = self._client.master(master_id).versions

        res.per_page = 100
        releases = ReleaseList()
        for i in range(res.pages):
            for release in res.page(i):
                if (id := release.data.get("id", None)) is not None:
                    if "CD" in release.data.get("major_formats", None):
                        releases.cd_flag = True
                    if "SACD" in release.data.get("major_formats", None):
                        releases.add_sacd(
                            id=id,
                            label=release.data.get("label", None),
                            country=release.data.get("country", None),
                            year=release.year,
                        )
        return releases
