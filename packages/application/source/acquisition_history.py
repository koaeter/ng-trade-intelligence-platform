from packages.application.source.acquisition_repositories import AcquisitionEventRepository


class GetSourceAcquisitionHistory:
    def __init__(self, events: AcquisitionEventRepository) -> None:
        self.events = events

    def execute(self, source_id: str):
        return self.events.list_for_source(source_id)
