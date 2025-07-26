import secrets
from dataclasses import dataclass, field
from functools import cached_property


@dataclass
class Product:
    name: str
    price: int
    brand: str
    category: str
    rating: int
    id: str = field(default_factory=lambda: secrets.token_urlsafe(8))

    @cached_property
    def categories(self) -> set[str]:
        return {cat.strip() for cat in self.category.split(",")}
