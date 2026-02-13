# Project Submission: Agentic AI Workflow for Smart Contract Auditing

## Summary
This project builds an agentic workflow to audit smart contracts using specialized AI agents. It combines deep codebase context building, pattern matching, external research, unique finding synthesis, and a curated vulnerability database. The system is designed to improve audit quality, reduce hallucinations, and produce structured, traceable security insights.

The repository includes a growing knowledge base of vulnerability patterns, protocol-specific findings, and unique exploit archetypes derived from real-world reports. These artifacts are organized for fast retrieval and for use in automated analysis pipelines (Semgrep/CodeQL) as well as LLM-driven reasoning. The end goal is a repeatable audit workflow that preserves provenance (finding → evidence → database entry), increases coverage, and supports continuous learning as new incidents are added.

## Objectives
- Build a repeatable, multi-agent pipeline for smart contract security audits.
- Generate high-fidelity codebase context before analysis.
- Leverage a structured vulnerability database to guide detection and reasoning.
- Produce consistent, evidence-backed findings and reports.
- Maintain an extensible database schema optimized for vector search and long-term maintenance.
- Provide protocol-specific checklists and retrieval shortcuts for auditors and agents.
- Support cross-protocol reasoning (EVM, Solana, Cosmos) with consistent output formats.

## Architecture Overview
The workflow orchestrates five core agents:

1. **Context Creator Agent**
   - Input: target codebase.
   - Output: ultra-granular architectural context and function-level analysis.
   - Role: establish a reliable mental model before vulnerability hunting.

2. **Pattern Matching Agent**
   - Input: codebase + vulnerability database.
   - Output: candidate findings via Semgrep/CodeQL patterns and synthesized reports.
   - Role: fast, deterministic pattern detection and cross-referencing.

3. **Research Agent**
   - Input: preliminary findings and protocol context.
   - Output: external references, historical incidents, and relevant exploit patterns.
   - Role: enrich reasoning with real-world evidence.

4. **Unique Finding Agent**
   - Input: “unique” signals from the database + synthesized patterns.
   - Output: novel or protocol-specific hypotheses and findings.
   - Role: capture non-obvious issues beyond standard patterns.

5. **Vulnerability Database Creation**
   - Input: curated vulnerability knowledge and reports.
   - Output: structured, searchable database entries.
   - Role: continuously improve detection quality and recall.

## Repository Structure & Data Sources
The repository is organized to support both automated analysis and manual triage:

- **DB/index.json**: central index that maps categories, keywords, and protocol contexts to relevant vulnerability files. This is the primary retrieval entrypoint for agents.
- **DB/**: canonical vulnerability entries organized by category (oracle, AMM, bridge, tokens, general, Cosmos, Solana) and “unique” exploit patterns.
- **reports/**: sourced findings and incident reports grouped by protocol domains (bridge, chainlink, ERC4626, proxies, etc.). These reports seed database entries and provide real-world grounding.
- **Variant-analysis/**: Semgrep and CodeQL templates to drive deterministic pattern matching and automated detection.
- **TEMPLATE.md / Example.md**: standardized entry formats to ensure consistent, vector-friendly documentation.

This structure allows fast lookup via index keywords, protocol contexts, and category browsing, while keeping raw evidence and curated entries tightly linked.

## Context Creator Agent (Core Spec)
**Name:** audit-context-building

**Description:** Enables ultra-granular, line-by-line code analysis to build deep architectural context before vulnerability or bug finding.

### Purpose
Establish a detailed, evidence-based model of the codebase. The output serves as the foundation for all downstream agents.

### Behavior
- Line-by-line / block-by-block analysis.
- First Principles, 5 Whys, and 5 Hows applied per block.
- Explicit invariants, assumptions, and flow mappings.
- Continuous cross-referencing across internal and external calls.
- Evidence-first analysis with explicit uncertainty labeling.
- Formal output structure that preserves traceability between functions and system-level flows.

### Non-Goals
- No vulnerability discovery or severity assessment during context building.

## Pattern Matching Agent (Core Spec)
This agent operationalizes the vulnerability database by turning curated knowledge into automated detection:

- Uses Semgrep/CodeQL patterns in [Variant-analysis/](Variant-analysis/) to scan codebases.
- Matches on risky constructs, missing validations, dangerous calls, and known exploit sequences.
- Produces candidate findings with references to the relevant DB entries and source evidence.
- Prioritizes deterministic matches before reasoning-based escalation.

## Research Agent (Core Spec)
This agent enriches and validates findings against external evidence:

- Pulls historical incidents, CVEs, writeups, and protocol-specific exploit postmortems.
- Validates that observed patterns map to known failure modes.
- Supplies references that strengthen reasoning and report credibility.
- Expands edge cases and informs the Unique Finding Agent.

## Unique Finding Agent (Core Spec)
This agent synthesizes “unique” signals from the database to detect non-obvious issues:

- Uses the **unique** category and protocol-specific exploit patterns as priors.
- Performs deeper reasoning to uncover multi-step or cross-contract issues.
- Flags novel hypotheses that are not strictly detected by static rules.
- Feeds back to the database creation flow when new patterns are confirmed.

## Data & Knowledge Sources
- Curated vulnerability database in [DB/](DB/).
- Protocol-specific findings in [reports/](reports/).
- Unique exploit patterns in [DB/unique/](DB/unique/).
- Index and retrieval metadata in [DB/index.json](DB/index.json).
- Semgrep/CodeQL templates in [Variant-analysis/](Variant-analysis/).

## Repository Alignment
The current repository layout supports the workflow end-to-end:
- **DB/**: vulnerability database and index.
- **reports/**: sourced findings and synthesized reports.
- **TEMPLATE.md / Example.md**: standard entry formats.
- **CodebaseStructure.md**: repo conventions and structure.
- **Variant-analysis/**: deterministic scan rules and templates.

## Expected Outputs
- Consistent, structured vulnerability entries aligned with templates.
- Evidence-backed audit reports tied to database artifacts.
- Searchable, vector-friendly metadata for retrieval and reasoning.
- Automated candidate findings with deterministic pattern matches and supporting references.
- Protocol-specific audit checklists and retrieval paths for rapid onboarding.

## Workflow (High-Level)
1. **Ingest** target codebase and determine protocol context.
2. **Context Creator Agent** builds a detailed, line-level model of the system.
3. **Pattern Matching Agent** runs Semgrep/CodeQL rules and maps hits to database entries.
4. **Research Agent** enriches findings with real-world evidence and known exploit patterns.
5. **Unique Finding Agent** evaluates unique signals to surface non-obvious hypotheses.
6. **Database Creation** converts validated findings into structured entries to improve future recall.

## Success Criteria
- High recall of known vulnerability patterns.
- Clear traceability from findings → evidence → database entries.
- Reduced hallucination and improved audit consistency.
- Increased cross-protocol coverage (EVM, Solana, Cosmos).
- Reduced false positives through stronger pattern-to-evidence alignment.

## Status
Active development. The database and agent prompts are being expanded and refined as new findings are incorporated.