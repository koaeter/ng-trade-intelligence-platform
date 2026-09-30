from datetime import datetime, timezone
from packages.application.source.extraction_comparison import CompareExtractionRuns
from packages.domain.source.extraction import ExtractionComparisonResult, ExtractionRun, ExtractionSegment

def run(i, checksum):
    return ExtractionRun(i, "artifact-1", "version-1", checksum, "extractor", "1", datetime.now(timezone.utc))

def seg(i, text, sequence):
    return ExtractionSegment(i, "artifact-1", sequence, text, extraction_id="run")

def test_same_input_same_output():
    r = CompareExtractionRuns().execute(run("a","a"*64), run("b","a"*64), [seg("a1","one",1)], [seg("b1","one",1)])
    assert r.result == ExtractionComparisonResult.SAME_INPUT_SAME_OUTPUT

def test_same_input_different_output():
    r = CompareExtractionRuns().execute(run("a","a"*64), run("b","a"*64), [seg("a1","one",1)], [seg("b1","changed",1)])
    assert r.result == ExtractionComparisonResult.SAME_INPUT_DIFFERENT_OUTPUT

def test_different_input():
    r = CompareExtractionRuns().execute(run("a","a"*64), run("b","b"*64), [seg("a1","one",1)], [seg("b1","two",1)])
    assert r.result == ExtractionComparisonResult.DIFFERENT_INPUT_DIFFERENT_OUTPUT

def test_different_artifacts_rejected():
    a = run("a","a"*64)
    b = ExtractionRun("b","artifact-2","version-1","a"*64,"extractor","1",datetime.now(timezone.utc))
    try: CompareExtractionRuns().execute(a,b,[],[]); assert False
    except ValueError as exc: assert "same artifact" in str(exc)

def test_same_run_rejected():
    a = run("a","a"*64)
    try: CompareExtractionRuns().execute(a,a,[],[]); assert False
    except ValueError as exc: assert "itself" in str(exc)
