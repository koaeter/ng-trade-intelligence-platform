from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Requirement:
    id: str
    name: str
    effective_from: date
    effective_to: date | None = None

    def is_effective_on(self, when: date) -> bool:
        return self.effective_from <= when and (
            self.effective_to is None or when <= self.effective_to
        )
