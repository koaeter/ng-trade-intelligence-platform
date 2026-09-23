from typing import Protocol

from packages.domain.requirement.revisions import RequirementRevision


class RequirementRevisionRepository(Protocol):
    def add(self, revision: RequirementRevision) -> None: ...

    def get(self, revision_id: str) -> RequirementRevision | None: ...
