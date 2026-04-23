from functools import wraps
from typing import Callable

from .models import Album, Image, Tracklist, ReleaseList

import typer


def track_tags_to_output(func) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> tuple[Album, Image, Tracklist]:
        res: tuple[Album, Image, Tracklist] = func(*args, **kwargs)

        album, image, tracklist = res

        dir = getattr(args[0], "_target_dir")

        table = []

        for track in tracklist.tracks:
            total_genres = album.genres + album.styles
            line = [
                album.year,
                album.artist,
                album.title,
                "/".join(total_genres),
                track.position,
                track.title,
                album.thumb,
                image.url,
                image.width,
                image.height,
            ]
            line_str = "\t".join([str(i) if i else "Null" for i in line])
            table.append(line_str)

        with open((dir / "tags.txt"), "w") as fp:
            fp.write("\n".join(table))
            fp.write("\n")

        typer.secho(
            f"{album.year} - {album.artist} - {album.title}",
            fg=typer.colors.BLUE,
            bold=True,
        )

        return res

    return wrapper


def releases_to_output(func) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> ReleaseList:
        res: ReleaseList = func(*args, **kwargs)
        if len(res.sacds) > 0:
            typer.secho("SACDs:", fg=typer.colors.GREEN, bold=True)
            for release in res.sacds:
                print(release)
        else:
            typer.secho("no SACDs", fg=typer.colors.RED, bold=True)
        if res.cd_flag:
            typer.secho("CDs exist", fg=typer.colors.GREEN, bold=True)
        else:
            typer.secho("no CDs", fg=typer.colors.RED, bold=True)
        return res

    return wrapper
