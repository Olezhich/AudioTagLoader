from pathlib import Path

import typer

from audiotagloader import cache

from .app import App
import re


cli_app = typer.Typer()


@cli_app.command("fba")
def fetch_by_artist(
    destination: Path,
    name: str,
    target_dir: Path = typer.Argument(default=Path(".")),
    update_cache: bool = typer.Option(False, "-uc"),
):
    cache.UPDATE_CACHE = update_cache
    app = App((destination / target_dir).resolve())
    app.get_track_tags_by_artist(name)


@cli_app.command("fbmi")
def fetch_by_master_id(
    destination: Path,
    master_id: str,
    target_dir: Path = typer.Argument(default=Path(".")),
    update_cache: bool = typer.Option(False, "-uc"),
):
    cache.UPDATE_CACHE = update_cache
    app = App((destination / target_dir).resolve())
    match = re.match(r"\[m(\d+)\]", master_id)
    if match:
        master_id = match.group(1)

    app.get_track_tags_by_master_id(int(master_id))


@cli_app.command("fbri")
def fetch_by_release_id(
    destination: Path,
    release_id: str,
    target_dir: Path = typer.Argument(default=Path(".")),
    update_cache: bool = typer.Option(False, "-uc"),
):
    cache.UPDATE_CACHE = update_cache
    app = App((destination / target_dir).resolve())
    match = re.match(r"\[r(\d+)\]", release_id)
    if match:
        release_id = match.group(1)

    app.get_track_tags_by_release_id(int(release_id))
