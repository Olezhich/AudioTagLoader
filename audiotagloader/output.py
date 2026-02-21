from functools import wraps
from typing import Callable

from .models import Album, Image, Tracklist


def track_tags_to_output(func) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> tuple[Album, Image, Tracklist]:
        res: tuple[Album, Image, Tracklist] = func(*args, **kwargs)

        album, image, tracklist = res

        table = []

        for track in tracklist.tracks:
            line = [
                album.year,
                album.artist,
                album.title,
                "/".join(album.genres),
                "/".join(album.styles),
                track.position,
                track.title,
                album.thumb,
                image.url,
                image.width,
                image.height,
            ]
            line_str = "\t".join([str(i) for i in line])
            table.append(line_str)

        print()
        print("\n".join(table))
        return res

    return wrapper
