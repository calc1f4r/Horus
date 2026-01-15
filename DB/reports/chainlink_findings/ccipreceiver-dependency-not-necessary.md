---
# Core Classification
protocol: Sherpa
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63844
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Immeas
  - MrPotatoMagic
---

## Vulnerability Title

`CCIPReceiver` dependency not necessary

### Overview

See description below for full details.

### Original Finding Content

**Description:** `SherpaVault` inherits `CCIPReceiver`, but the protocol’s cross-chain flow uses CCIP burn/mint token pools rather than ad-hoc message passing. Chainlink’s [cross-chain token pattern](https://docs.chain.link/ccip/concepts/cross-chain-token/evm/tokens) on EVM chains does not require a `CCIPReceiver` implementation on the token/vault contract, only pool authorization via `mint/burn` style hooks. Keeping `CCIPReceiver` (and its `_ccipReceive` stub) increases bytecode size, deployment cost, and surface area without delivering any functionality.

Consider removing the inheritance and associated code to simplify the contract, reduce gas/bytecode footprint, and avoid implying a message-bridge dependency that isn’t actually used.

**Sherpa:** Removed in commit [`59974b2`](https://github.com/hedgemonyxyz/sherpa-vault-smartcontracts/commit/59974b29c59e2cc5afce87bbfd87a625bc05a94b)

**Cyfrin:** Verified. `CCIPReceiver` dependency now removed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Sherpa |
| Report Date | N/A |
| Finders | Immeas, MrPotatoMagic |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

