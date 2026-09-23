from packages.domain.requirement.rule_sets import RuleSetStatus


class RuleSetVersionService:
    def __init__(self, repository, validator=None) -> None:
        self.repository = repository
        self.validator = validator

    def activate(self, version_id: str) -> None:
        target = self.repository.get(version_id)
        if target is None:
            raise ValueError("Rule-set version does not exist")
        if self.validator is not None:
            self.validator.validate(target.id)
        active = self.repository.get_active()
        if active is not None and active.id != target.id:
            self.repository.set_status(active.id, RuleSetStatus.RETIRED)
        self.repository.set_status(target.id, RuleSetStatus.ACTIVE)
