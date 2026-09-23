# Knowledge Base Persistence and Editing Model

## Purpose

The regulatory knowledge base is editable, but it is **governed editing**, not destructive editing.

The system separates the authoritative evidence from the structured knowledge derived from that evidence:

```
Authoritative Source
  ↓
Document
  ↓
Artifact (captured bytes)
  ↓
Extraction
  ↓
Provision Candidate
  ↓
Reviewed Provision
  ↓
Requirement / Rule Revision
  ↓
Published Knowledge
```

## What is editable?

### 1. Source metadata

Administrators may maintain source metadata such as authority assignment, endpoint metadata, jurisdiction, domain, fact type, status and verification information.

Changing metadata does not alter the captured source artifact.

### 2. Extracted knowledge

A provision can be reviewed, classified, corrected or rejected. Human corrections become a governed knowledge change and retain a link to the underlying extraction and source location.

### 3. Requirements

Requirements are not overwritten in place after publication. A change creates a new requirement revision. The previous revision remains available for historical and point-in-time analysis.

### 4. Rules

Rules are versioned with requirement revisions. Published rule trees are immutable. A correction creates a new revision rather than mutating the rule tree used by an earlier evaluation.

### 5. Source documents

The captured original is immutable. If the official source changes, the system acquires a new artifact/version and preserves the previous capture.

## How the knowledge is saved

The authoritative operational records are relational/domain records. The physical implementation may later use:

- a relational database for governed entities, revisions, relationships and audit records;
- object storage for original documents and captured artifacts;
- full-text/search indexes for retrieval;
- vector indexes for semantic retrieval;
- a knowledge graph for explicit relationships.

Search indexes, embeddings and graph projections are **derived representations**, not the authoritative record. They can be rebuilt from governed records.

## Revision model

The important distinction is:

```
Object identity ≠ version/revision ≠ representation ≠ publication state
```

For example:

```
Requirement R-001
  ├── Revision 1 — published
  ├── Revision 2 — draft/review
  └── Revision 3 — published later
```

Revision 1 remains recoverable even after Revision 3 becomes current.

## Evidence chain

A published requirement must be traceable through:

```
Requirement
  → Evidence
  → Provision
  → Extraction Segment
  → Artifact
  → Document
  → Source
  → Authority Endpoint
  → Authority
```

This prevents an editor from changing a requirement while losing the evidence that justified it.

## Human review

Machine extraction may create candidates, but candidate status does not make knowledge authoritative.

A typical path is:

```
EXTRACTED
   ↓
REVIEWED
   ↓
ACCEPTED
   ↓
REQUIREMENT REVISION
   ↓
VALIDATED
   ↓
PUBLISHED
```

The exact workflow and permissions will be implemented as the knowledge-management and security layers mature.

## What the AI does

AI may assist with:

- extracting candidate provisions;
- classifying provisions;
- proposing relationships;
- identifying possible changes;
- drafting requirement candidates;
- summarising evidence.

AI does not silently write authoritative knowledge directly into the published layer.

## Key design rule

**The knowledge base is editable; the evidence history is not rewritten.**

An editor can correct what the system believes a source means, but the system must retain:

- the original source;
- the captured version;
- the original extraction;
- the previous knowledge revision;
- who changed the knowledge;
- when it changed;
- why it changed;
- what evidence supports the new revision.

This makes the knowledge base maintainable without turning it into an unauditable collection of overwritten text.
