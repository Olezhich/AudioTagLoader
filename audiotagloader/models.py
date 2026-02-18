from pathlib import Path
from pydantic import BaseModel, Field, field_validator


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
    title: str = Field(default="")
    year: int = Field(default=0)
    genres: list[str] = Field(default_factory=lambda: list())
    styles: list[str] = Field(default_factory=lambda: list())
    thumb: Path = Field(default_factory=lambda: Path())
    cover: Path = Field(default_factory=lambda: Path())

    @field_validator("genres", "styles", mode="before")
    @classmethod
    def normlize_list(cls, value: list[str] | None) -> list[str]:
        if value is None:
            res: list[str] = []
            return res
        return value

    @field_validator("thumb", "cover", mode="before")
    @classmethod
    def normlize_path(cls, value: str | None) -> Path:
        if value is None:
            return Path()
        return Path(value)
