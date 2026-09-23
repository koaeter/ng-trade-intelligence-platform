from packages.application.source.source_acquisition import SourceAcquisitionPolicy
from infrastructure.acquisition.http import HTTPSourceFetcher


def test_source_policy_requires_allowlisted_https_host():
    fetcher = HTTPSourceFetcher(SourceAcquisitionPolicy(frozenset({"example.gov"})))
    try:
        fetcher.fetch("http://example.gov/document.pdf")
        assert False, "expected HTTPS rejection"
    except ValueError as exc:
        assert "HTTPS" in str(exc)


def test_source_policy_rejects_unknown_host():
    fetcher = HTTPSourceFetcher(SourceAcquisitionPolicy(frozenset({"example.gov"})))
    try:
        fetcher.fetch("https://untrusted.example/document.pdf")
        assert False, "expected allowlist rejection"
    except ValueError as exc:
        assert "allowlisted" in str(exc)


def test_source_policy_rejects_url_credentials():
    fetcher = HTTPSourceFetcher(SourceAcquisitionPolicy(frozenset({"example.gov"})))
    try:
        fetcher.fetch("https://user:password@example.gov/document.pdf")
        assert False, "expected credential rejection"
    except ValueError as exc:
        assert "credentials" in str(exc)
