from types import SimpleNamespace

from fastapi.testclient import TestClient
from apps.api.main import app


def test_create_export_scenario_validation() -> None:
    client = TestClient(app)
    response = client.post("/api/v1/export-scenarios", json={"product_id": "p", "hs_code": "1801"})
    assert response.status_code == 422


def test_scenario_date_is_required() -> None:
    client = TestClient(app)
    response = client.post("/api/v1/export-scenarios", json={
        "product_id": "p", "hs_version_id": "HS2022", "hs_code": "1801", "origin_country_code": "NG",
        "destination_market_code": "DE",
    })
    assert response.status_code == 422



def test_evaluation_endpoint_uses_revision_aware_service(monkeypatch) -> None:
    import apps.api.main as api

    for name in (
        "SqlAlchemyExportScenarioRepository",
        "SqlAlchemyRuleSetVersionRepository",
        "SqlAlchemyRuleSetMembershipRepository",
        "SqlAlchemyRequirementRevisionRepository",
        "SqlAlchemyRequirementRuleNodeRepository",
        "SqlAlchemyProductRepository",
        "SqlAlchemyHSCodeRepository",
        "SqlAlchemyCountryRepository",
        "SqlAlchemyMarketRepository",
        "SqlAlchemyEvidenceRepository",
        "SqlAlchemyApplicabilityEvaluationRepository",
        "SqlAlchemyApplicabilityTraceRepository",
    ):
        monkeypatch.setattr(api, name, lambda session: object())

    class Session:
        def commit(self):
            self.committed = True

    class Service:
        def __init__(self, *repositories):
            self.repository_count = len(repositories)

        def evaluate(self, scenario_id):
            return [
                SimpleNamespace(
                    scenario_id=scenario_id,
                    requirement_id="r1",
                    result=SimpleNamespace(value="APPLICABLE"),
                    rule_set_version="2026.09.23.1",
                    evidence=(),
                )
            ]

    monkeypatch.setattr(api, "RevisionAwareEvaluationService", Service)
    session = Session()
    result = api.evaluate_export_scenario("scenario-1", session)

    assert result[0].scenario_id == "scenario-1"
    assert result[0].rule_set_version == "2026.09.23.1"
    assert session.committed is True
