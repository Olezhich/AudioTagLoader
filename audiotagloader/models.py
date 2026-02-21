from __future__ import annotations
from pathlib import Path
from pydantic import BaseModel, Field, field_validator

from .config import PERMITTED_IMAGE_EXTS, IMAGE_SIZE_STUB


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
        return "|".join([self.name] + self.variations)


class Album(BaseModel):
    id: int
    title: str = Field(default="")
    year: int = Field(default=0)
    genres: list[str] = Field(default_factory=lambda: list())
    styles: list[str] = Field(default_factory=lambda: list())
    thumb: Path = Field(default_factory=lambda: Path())

    @field_validator("genres", "styles", mode="before")
    @classmethod
    def normlize_list(cls, value: list[str] | None) -> list[str]:
        if value is None:
            res: list[str] = []
            return res
        return value


class Image(BaseModel):
    url: Path = Field(default_factory=lambda: Path())
    width: int = Field(default=IMAGE_SIZE_STUB)
    height: int = Field(default=IMAGE_SIZE_STUB)

    @field_validator("url", mode="before")
    @classmethod
    def check_extension(cls, url: Path) -> Path:
        if url and not any(
            str(url).lower().endswith(ext) for ext in PERMITTED_IMAGE_EXTS
        ):
            raise ValueError(f"image url extension sould be in: {PERMITTED_IMAGE_EXTS}")
        return url
