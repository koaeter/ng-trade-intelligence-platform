from packages.domain.source.models import SourceStatus


_ALLOWED = {
    SourceStatus.DISCOVERED: {SourceStatus.ACQUIRED, SourceStatus.RETIRED},
    SourceStatus.ACQUIRED: {SourceStatus.EXTRACTED, SourceStatus.RETIRED},
    SourceStatus.EXTRACTED: {SourceStatus.CANDIDATE, SourceStatus.RETIRED},
    SourceStatus.CANDIDATE: {SourceStatus.REVIEWED, SourceStatus.RETIRED},
    SourceStatus.REVIEWED: {SourceStatus.PUBLISHED, SourceStatus.CANDIDATE, SourceStatus.RETIRED},
    SourceStatus.PUBLISHED: {SourceStatus.SUPERSEDED, SourceStatus.RETIRED},
    SourceStatus.SUPERSEDED: {SourceStatus.RETIRED},
    SourceStatus.RETIRED: set(),
}


class SourceLifecycleService:
    def transition(self, source, target: SourceStatus):
        if target not in _ALLOWED[source.status]:
            raise ValueError(f"Invalid source lifecycle transition: {source.status.value} -> {target.value}")
        return type(source)(
            source.id,
            source.name,
            source.organization,
            source.source_type,
            source.jurisdiction,
            source.official_url,
            target,
        )
