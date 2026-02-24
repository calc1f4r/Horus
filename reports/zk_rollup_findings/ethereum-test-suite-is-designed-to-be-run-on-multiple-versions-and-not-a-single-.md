---
# Core Classification
protocol: Polygon zkEVM
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21370
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/PolygonzkEVM-Protocol/zkEVM-engagement-1-Spearbit-27-March.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/PolygonzkEVM-Protocol/zkEVM-engagement-1-Spearbit-27-March.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 8
finders:
  - Thibaut Schaeffer
  - Alex Beregszaszi
  - Lucas Vella
  - Miguel Palhas
  - Paweł Bylica
---

## Vulnerability Title

Ethereum Test Suite is designed to be run on multiple versions and not a single one

### Overview


This bug report is regarding the Ethereum Test Suite, which is designed to support multiple protocol versions and is ran from the genesis until the last release. Some tests are enabled from specific old versions or starting specific new versions. The zkEVM is tied to the Berlin release only and may miss out on some test cases, though some have been updated to be enabled on Berlin too. To ensure that all relevant tests are run on the Berlin version, a comprehensive review of the test suite is needed. Polygon-Hermez is addressing this issue by reviewing the full Ethereum test suite to identify missing tests regarding the Berlin version to increase test coverage in PR #178.

### Original Finding Content

## Severity: Medium Risk

## Context
zkevm-testvectors

## Description
The Ethereum Test Suite is designed to support multiple protocol versions (called Network), ran from the genesis (called Frontier) in increments until the last release. Some tests are enabled:

a) on specific old versions (e.g. only Frontier) because nobody updated them.  
b) starting specific new versions (e.g. London) because they rely on some new EVM features to make testing easier, but the feature they actually are designed to test were enabled from earlier upgrades.

The zkEVM is tied to the Berlin release only and may miss out on some test cases. We have updated some test cases to be enabled on Berlin too, but a comprehensive review of the test suite is needed.

## Recommendation
Ensure that all relevant tests are run on the Berlin version.

## Polygon-Hermez
We will review the full Ethereum test suite to identify missing tests regarding the Berlin version to increase test coverage. This is done in the PR #178.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Polygon zkEVM |
| Report Date | N/A |
| Finders | Thibaut Schaeffer, Alex Beregszaszi, Lucas Vella, Miguel Palhas, Paweł Bylica, Christian Reitwiessner, Andrei Maiboroda, Leo Alt |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/PolygonzkEVM-Protocol/zkEVM-engagement-1-Spearbit-27-March.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/PolygonzkEVM-Protocol/zkEVM-engagement-1-Spearbit-27-March.pdf

### Keywords for Search

`vulnerability`

