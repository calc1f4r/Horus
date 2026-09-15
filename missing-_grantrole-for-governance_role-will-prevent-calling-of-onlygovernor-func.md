---
# Core Classification
protocol: Infrared Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49847
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Infrared-Spearbit-Security-Review-January-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Infrared-Spearbit-Security-Review-January-2025.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - 0xRajeev
  - Chinmay Farkya
  - Cryptara
  - Noah Marconi
---

## Vulnerability Title

Missing _grantRole for GOVERNANCE_ROLE will prevent calling of onlyGovernor functions including

### Overview


This bug report is about a critical issue found in the code for the Infrared protocol. The problem is that the GOVERNANCE_ROLE is not being granted to any privileged address during initialization, which means that certain important functions cannot be called. This affects the functioning of several core contracts, including InfraredBERA, Voter, and BribeCollector. The bug has a high impact because it prevents important functions like enabling withdrawals and setting deposit signatures, and it also prevents these contracts from being upgraded in the future. The likelihood of this bug occurring is high because the necessary code is missing from the initialization functions and deployment scripts. The recommendation is to add the missing code in all relevant functions to fix the issue. The bug has been addressed in the code with three pull requests (PR 283, PR 294, and PR 316) which add the missing code to grant the GOVERNANCE_ROLE.

### Original Finding Content

## Upgrades

**Severity:** Critical Risk  
**Context:** (No context files were provided by the reviewer)  
**Summary:** Missing the granting of role for `GOVERNANCE_ROLE` to any privileged address will prevent calling of onlyGovernor functions including upgrades across InfraredBERA contracts along with Voter and BribeCollector core contracts of Infrared.

## Finding Description
All InfraredBERA related contracts derive from `UUPSUpgradeable` and `AccessControlUpgradeable` where `_authorizeUpgrade` is restricted to the `GOVERNANCE_ROLE`. InfraredBERA also has several protocol-critical onlyGovernor functions:

- `setWithdrawalsEnabled()`
- `setFeeShareholders()`
- `setDepositSignature()`
- `setDepositor()`
- `setWithdrawor()`
- `setClaimor()`
- `setReceivor()`

However, the `GOVERNANCE_ROLE` is not granted to any privileged address during initialization, as done in `Infrared.sol` via `_grantRole(GOVERNANCE_ROLE, _admin)`. This is the case in `Voter.sol`, which prevents upgrading it and calling onlyGovernor functions of:

- `setMaxVotingNum()`
- `whitelistNFT()`
- `killBribeVault()`
- `reviveBribeVault()`

This is also the case in `BribeCollector.sol`, which prevents upgrading it and calling the onlyGovernor function `setPayoutAmount()`. Related unit tests succeed because this role is granted during their setup.

## Impact Explanation
**High**, because several protocol-critical functions can never be called, for example:

1. `setWithdrawalsEnabled()` cannot be called to enable voluntary withdrawals in future.
2. `setDepositSignature()` cannot be called to set valid deposit signatures for validators, which will prevent InfraredBERADepositor deposits from executing and effectively preventing liquid staking to function.
3. Voter bribe vaults cannot be killed or revived.
4. `BribeCollector.setPayoutAmount()` cannot be called to set `payoutAmount`, which allows anyone to claim all bribe tokens for free (because default `payoutAmount` is 0).
5. None of these contracts can be upgraded in future.

## Likelihood Explanation
**High**, because `_grantRole` for `GOVERNANCE_ROLE` is missing in all relevant `initialize()` functions and also absent in related deployment scripts.

## Recommendation
Consider adding something similar to `_grantRole(GOVERNANCE_ROLE, _admin)` in all relevant `initialize()` functions.

## Infrared
Fixed in PR 283, PR 294, and PR 316.

## Spearbit Reviewed that:
1. PR 283 fixes the issue as recommended using `_grantRole(GOVERNANCE_ROLE, _gov)` for InfraredBERA contracts.
2. PR 294 fixes the issue as recommended using `_grantRole(GOVERNANCE_ROLE, _gov)` for BribeCollector.
3. PR 316 fixes the issue as recommended using `_grantRole(GOVERNANCE_ROLE, _gov)` for Voter.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Infrared Contracts |
| Report Date | N/A |
| Finders | 0xRajeev, Chinmay Farkya, Cryptara, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Infrared-Spearbit-Security-Review-January-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Infrared-Spearbit-Security-Review-January-2025.pdf

### Keywords for Search

`vulnerability`

