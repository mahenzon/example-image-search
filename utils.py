from dataclasses import dataclass
from typing import Any


@dataclass
class SortValueGetter:
    attr_name: str

    def get_value(self, item: Any) -> Any:
        value = getattr(item, self.attr_name)
        if isinstance(value, str):
            value = value.lower()
        return value
