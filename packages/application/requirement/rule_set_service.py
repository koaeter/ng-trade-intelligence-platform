from packages.domain.requirement.rule_sets import RuleSetStatus


class RuleSetVersionService:
    def __init__(self, repository, validator=None) -> None:
        self.repository = repository
        self.validator = validator

    def _get(self, version_id: str):
        target = self.repository.get(version_id)
        if target is None:
            raise ValueError("Rule-set version does not exist")
        return target

    def _require_validator(self) -> None:
        if self.validator is None:
            raise ValueError("Rule-set publication validator is required for this operation")

    def validate(self, version_id: str) -> None:
        target = self._get(version_id)
        if target.status not in {RuleSetStatus.DRAFT, RuleSetStatus.VALIDATED}:
            raise ValueError("Only draft or validated rule sets can be validated")
        self._require_validator()
        self.validator.validate(target.id)
        self.repository.set_status(target.id, RuleSetStatus.VALIDATED)

    def publish(self, version_id: str) -> None:
        target = self._get(version_id)
        if target.status != RuleSetStatus.VALIDATED:
            raise ValueError("Only validated rule sets can be published")
        self.repository.set_status(target.id, RuleSetStatus.PUBLISHED)

    def activate(self, version_id: str) -> None:
        target = self._get(version_id)
        if target.status not in {RuleSetStatus.PUBLISHED, RuleSetStatus.ACTIVE}:
            raise ValueError("Only published rule sets can be activated")
        self._require_validator()
        # Revalidate at activation: a previously validated draft must not bypass
        # current integrity checks immediately before becoming the active policy.
        self.validator.validate(target.id)
        activate = getattr(self.repository, "activate", None)
        if activate is None:
            raise ValueError("Atomic rule-set activation is not supported by this repository")
        activate(target.id)
