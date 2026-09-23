from dataclasses import dataclass

from packages.domain.source.authority import Instrument, InstrumentType


@dataclass(frozen=True)
class InstrumentValidationResult:
    valid: bool
    errors: tuple[str, ...]


def validate_instrument(instrument: Instrument) -> InstrumentValidationResult:
    errors: list[str] = []
    if instrument.instrument_type in {InstrumentType.MOU, InstrumentType.MOA} and len(instrument.parties) < 2:
        errors.append("MOU/MOA must identify at least two parties")
    if instrument.supersedes_instrument_id == instrument.id:
        errors.append("Instrument cannot supersede itself")
    return InstrumentValidationResult(not errors, tuple(errors))
