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
