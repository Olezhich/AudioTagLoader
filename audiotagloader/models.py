from __future__ import annotations
from pydantic import BaseModel, Field, field_validator

from .config import PERMITTED_IMAGE_EXTS, IMAGE_SIZE_STUB

import re


class Artist(BaseModel):
    name: str = Field(default="", description="main artist name")
    variations: list[str] = Field(
        default_factory=lambda: list(), description="artist name variations list"
    )

    @field_validator("variations", mode="before")
    @classmethod
    def normalize_variations(cls, value: list[str] | None) -> list[str]:
        if value is None:
            res: list[str] = []
            return res
        return value

    @property
    def aliases(self) -> str:
        lst = sorted([self.name] + self.variations, key=len, reverse=True)
        return "|".join([re.escape(alias) for alias in lst])


class Album(BaseModel, frozen=True):
    id: int
    title: str = Field(default="")
    year: int = Field(default=0)
    genres: list[str] = Field(default_factory=lambda: list())
    styles: list[str] = Field(default_factory=lambda: list())
    thumb: str = Field(default="")
    artist: str = Field(default="")

    @field_validator("genres", "styles", mode="before")
    @classmethod
    def normlize_list(cls, value: list[str] | None) -> list[str]:
        if value is None:
            res: list[str] = []
            return res
        return value

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not isinstance(other, Album):
            return False
        return self.id == other.id


class Image(BaseModel):
    url: str = Field(default="")
    width: int = Field(default=IMAGE_SIZE_STUB)
    height: int = Field(default=IMAGE_SIZE_STUB)

    @field_validator("url", mode="before")
    @classmethod
    def check_extension(cls, url: str) -> str:
        if url and not any(url.lower().endswith(ext) for ext in PERMITTED_IMAGE_EXTS):
            raise ValueError(f"image url extension sould be in: {PERMITTED_IMAGE_EXTS}")
        return url


class Track(BaseModel):
    title: str = Field(default="")
    position: int = Field(default=0)


class Tracklist(BaseModel):
    tracks: list[Track] = Field(default_factory=lambda: list())

    @field_validator("tracks", mode="before")
    @classmethod
    def normalize_tracks(cls, value: list[Track] | None) -> list[Track]:
        if value is None:
            res: list[Track] = []
            return res
        return value

    @field_validator("tracks", mode="after")
    @classmethod
    def convert_track_position(cls, tracks: list[Track]) -> list[Track]:
        for i in range(len(tracks)):
            tracks[i].position = i + 1
        return tracks
