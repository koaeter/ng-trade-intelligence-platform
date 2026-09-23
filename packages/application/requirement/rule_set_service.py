from packages.domain.requirement.rule_sets import RuleSetStatus


class RuleSetVersionService:
    def __init__(self, repository, validator=None) -> None:
        self.repository = repository
        self.validator = validator

    def validate(self, version_id: str) -> None:
        target = self.repository.get(version_id)
        if target is None:
            raise ValueError("Rule-set version does not exist")
        if target.status not in {RuleSetStatus.DRAFT, RuleSetStatus.VALIDATED}:
            raise ValueError("Only draft or validated rule sets can be validated")
        if self.validator is not None:
            self.validator.validate(target.id)
        self.repository.set_status(target.id, RuleSetStatus.VALIDATED)

    def publish(self, version_id: str) -> None:
        target = self.repository.get(version_id)
        if target is None:
            raise ValueError("Rule-set version does not exist")
        if target.status != RuleSetStatus.VALIDATED:
            raise ValueError("Only validated rule sets can be published")
        self.repository.set_status(target.id, RuleSetStatus.PUBLISHED)

    def activate(self, version_id: str) -> None:
        target = self.repository.get(version_id)
        if target is None:
            raise ValueError("Rule-set version does not exist")
        if target.status not in {RuleSetStatus.PUBLISHED, RuleSetStatus.ACTIVE}:
            raise ValueError("Only published rule sets can be activated")
        if self.validator is not None:
            self.validator.validate(target.id)
        active = self.repository.get_active()
        if active is not None and active.id != target.id:
            self.repository.set_status(active.id, RuleSetStatus.RETIRED)
        self.repository.set_status(target.id, RuleSetStatus.ACTIVE)
