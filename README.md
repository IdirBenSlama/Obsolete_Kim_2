# Kimera SWM Repository

This repository hosts documentation for the **Spherical Word Methodology (SWM)** and supporting components of the Kimera cognitive architecture.  The materials describe how Kimera stores knowledge, manages semantic state, and routes information between its modules.

## Repository Layout

- **`Spherical Word Methodology (SWM) Theory.md`** – conceptual background.
- **`Main_Architecture.md`** and **`Kimera ARCHITECTURE.pdf`** – architectural overview.
- **`EchoForm.MD`** and **`EcoForm Engineering Specification.pdf`** – describe the EcoForm subsystem for non-linear grammar and orthography.
- **`Vault.md`** and **`Vault Engineering Specification for Kimera SWM.pdf`** – detail the Vault memory structures and algorithms.
- **`thermodynamic.md`** and **`Semantic Thermodynamic Engineering Specification.pdf`** – outline semantic energy rules.
- Additional conversation transcripts and diagrams provide further context (e.g., `conversation Abacus.pdf`).

## Navigating the Docs

The Markdown files offer concise summaries of each subsystem, while the PDFs contain full diagrams and formal specifications.  A suggested reading order is:

1. **SWM Theory** – foundational principles of the system.
2. **EcoForm** – grammar and orthography layer.
3. **Vault** – memory management and retrieval logic.
4. **Thermodynamic** – semantic energy dynamics.

### Snippets

*EcoForm (from `EchoForm.MD` lines 1‑15)*
```
EcoForm Engineering Specification
1. Overview
EcoForm is the non-linear grammar and orthography subsystem within Kimera SWM.
Its primary purpose is to represent, store, and manipulate structured grammatical
constructs (e.g., nested syntactic patterns, non-linear parse trees) alongside
orthographic transformations (e.g., script normalization, variant mappings). EcoForm
serves as the foundation for:
● Grammar Encoding: Capturing hierarchical, non-linear syntactic patterns in a
flexible data structure.
● Orthographic Mapping: Managing script-level transformations (e.g., ligatures,
diacritics, Unicode normalization) and linking them to grammatical units.
● Pattern Matching & Retrieval: Querying stored grammatical/orthographic
constructs based on similarity or structural criteria.
● Integration with SWM: Exposing structured outputs to downstream SWM
modules (e.g., Echoform, Geoid alignment) via defined APIs.
```

*Vault (from `Vault.md` lines 2‑7)*
```
Version: v1.0
Date: 2025-06-05
This document specifies the engineering details for the Vault subsystem in Kimera SWM. It
covers memory structures, data schemas, routing logic, threshold values, and pseudocode
for core algorithms. All speculative commentary has been removed; only concrete
engineering constructs remain.
```

*Thermodynamic (from `thermodynamic.md` lines 1‑8)*
```
c Thermodynamic Engineering Specification
1. Overview
Semantic Thermodynamic within Kimera SWM defines the rules governing how semantic
constructs (e.g., Echoforms, EcoForms, Geoid interactions) gain, dissipate, and transfer
“semantic energy.” This system ensures consistency in activation, resonance, and decay
across modules. It focuses strictly on engineering constructs: memory structures, data
schemas, routing logic, threshold values, and pseudocode. All speculative commentary is
omitted.
```

These documents work together to describe how Kimera SWM orchestrates knowledge storage, semantic interactions, and overall system behavior.  Browse the Markdown files directly or open the accompanying PDFs for detailed diagrams and extended explanations.

## API

Launch the FastAPI service with:

```
uvicorn kimera.server:app
```

Endpoints:

- `POST /ecoform/create` – create an EcoForm
- `GET  /ecoform/{id}/status` – fetch an EcoForm status
- `POST /ecoform/query` – search active EcoForms
- `POST /symbolic/insert` – add triples and log contradictions
- `GET  /vault/scars` – list contradiction scars
