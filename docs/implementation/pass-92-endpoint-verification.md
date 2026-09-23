# Pass 92 — Authority endpoint verification metadata

Authority endpoints now distinguish active status from verification status. A newly registered endpoint is UNVERIFIED until an operational verification process confirms it. Verification timestamp and a bounded note are retained as endpoint metadata.

Verification does not grant legal authority; it records whether the configured acquisition target was operationally checked.
