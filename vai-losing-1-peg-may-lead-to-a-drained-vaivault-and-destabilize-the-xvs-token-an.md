---
# Core Classification
protocol: Venus protocol (vaults)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59871
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/venus-protocol-vaults/9497f0a0-be2e-4214-9ade-f4f2e76b5cb2/index.html
source_link: https://certificate.quantstamp.com/full/venus-protocol-vaults/9497f0a0-be2e-4214-9ade-f4f2e76b5cb2/index.html
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
finders_count: 4
finders:
  - Shih-Hung Wang
  - Julio Aguilar
  - Roman Rohleder
  - Ibrahim Abouzied
---

## Vulnerability Title

VAI Losing 1$ Peg May Lead to a Drained `VAIVault` and Destabilize the XVS Token and Vault

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> VAIVault distributions are continuously monitored by the risk team. The current value of reward per block corresponds to the market analysis. That being said, the reward amount per block is fixed, so users will not be receiving more XVS if there are more deposits.

**File(s) affected:**`VAIVault.sol`

**Description:** The [VAI token is an algorithmic stable coin](https://github.com/VenusProtocol/venus-protocol/#venus-protocol) and pegged to 1 USD, similar to [MakerDAO's DAI](https://developer.makerdao.com/dai/1/). However, it is not guaranteed to always hold its peg to 1 USD under all circumstances.

Should the token lose its peg and be (much) less valuable than 1 USD it could lead to a high increase of users depositing their `VAI` tokens in the `VAIVault` and earning `XVS` tokens as interest at a (high) discount.

This could lead to an unexpectedly quick depletion of `XVS` funds in the `VAIVault` and in turn destabilize the `XVS` token value and all its associated pools in the `XVSVault`.

**Recommendation:** We recommend documenting this fact in public user-facing documentation, closely monitoring the `VAI` token, and, if necessary, pausing the `VAIVault`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Venus protocol (vaults) |
| Report Date | N/A |
| Finders | Shih-Hung Wang, Julio Aguilar, Roman Rohleder, Ibrahim Abouzied |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/venus-protocol-vaults/9497f0a0-be2e-4214-9ade-f4f2e76b5cb2/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/venus-protocol-vaults/9497f0a0-be2e-4214-9ade-f4f2e76b5cb2/index.html

### Keywords for Search

`vulnerability`

