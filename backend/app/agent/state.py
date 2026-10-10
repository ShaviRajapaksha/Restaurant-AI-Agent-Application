from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class AgentState:
    intent: str | None = None
    party_size: int | None = None
    cuisine: str | None = None
    location: str | None = None
    budget: int | None = None
    date: str | None = None
    time: str | None = None
    selected_restaurant_id: int | None = None
    selected_restaurant_name: str | None = None
    last_search_results: list[dict] = field(default_factory=list)
    pending_confirmation: dict | None = None
    pending_order: dict | None = None
    reservation_id: int | None = None
    order_id: int | None = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict | None) -> "AgentState":
        if not d:
            return cls()
        allowed = {f for f in cls().__dict__.keys()}
        return cls(**{k: v for k, v in d.items() if k in allowed})

    def merge(self, updates: dict) -> None:
        for k, v in updates.items():
            if v is not None and k in self.__dict__:
                setattr(self, k, v)