---
# Core Classification
protocol: 0xhoneyjar
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52967
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/1fce4414-74e9-490b-ac89-cf65755563d2
source_link: https://cdn.cantina.xyz/reports/cantina_honeyjar_february2025.pdf
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
finders_count: 2
finders:
  - chris
  - Cryptara
---

## Vulnerability Title

Deposits and Mints to Whitelisted Vaults Result in Lost Rewards 

### Overview


A bug has been found in the fatBERA contract, specifically in the functions that allow for minting and depositing directly to a receiver address. Currently, if a vault is whitelisted, any shares deposited or minted to it will not accrue any rewards, resulting in permanently lost rewards. This is a problem because it means that shares held by whitelisted vaults will not contribute to the reward calculations. To fix this, deposits and mints should only be allowed to non-whitelisted vaults, unless there is a valid business reason to allow them to whitelisted vaults. The code has been fixed in the HoneyJar and Cantina Managed contracts to prevent this issue from occurring.

### Original Finding Content

## Context
- `fatBERA.sol#L323-L343`
- `fatBERA.sol#L352-L359`
- `fatBERA.sol#L368-L376`

## Description
The contract currently allows minting and depositing directly to a receiver address. Vaults that are whitelisted have an effective balance of zero, meaning that any shares deposited or minted to them will not accrue any rewards. This results in permanently lost rewards for any shares held by such vaults if they are set as the receivers.

From a logical perspective, allowing deposits and mints to whitelisted vaults seems problematic, as it creates a scenario where shares exist but do not contribute to the reward calculations. If there is no business reason to support this, it should likely be restricted.

## DRAFT

## Recommendation
Deposits and mints should be restricted only to receivers that are explicitly non-whitelisted vaults to prevent shares from being rendered ineffective for rewards. Before processing a deposit or mint, the contract should check if `isWhitelistedVault(receiver)` is true if the receiver is a vault. If there is a valid business reason to allow deposits to whitelisted vaults, documentation should clarify why, and the implications should be well understood.

## HoneyJar
Fixed in commit `bab55d54`.

## Cantina Managed
Fixed. The code is now checking for `isWhitelistedVault` in `depositNative`, `deposit`, and `mint` functions to prevent the unsync of the `vaultedShares` mapping and the expected way of vault transfer.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | 0xhoneyjar |
| Report Date | N/A |
| Finders | chris, Cryptara |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_honeyjar_february2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/1fce4414-74e9-490b-ac89-cf65755563d2

### Keywords for Search

`vulnerability`

