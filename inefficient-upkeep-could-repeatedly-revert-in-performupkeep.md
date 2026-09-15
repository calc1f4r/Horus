---
# Core Classification
protocol: Bretton Woods Digital Gold
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60832
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/bretton-woods-digital-gold/6a607c09-57af-4640-97bd-ee122e1ed0a6/index.html
source_link: https://certificate.quantstamp.com/full/bretton-woods-digital-gold/6a607c09-57af-4640-97bd-ee122e1ed0a6/index.html
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
finders_count: 4
finders:
  - Guillermo Escobero
  - Ruben Koch
  - Jeffrey Kam
  - Gelei Deng
---

## Vulnerability Title

Inefficient Upkeep Could Repeatedly Revert in `performUpkeep()`

### Overview


The developers are planning to launch a Chainlink Upkeep feature on the `HotWalletTransferer` contract, which will automatically resupply funds to a `hotWallet` address if it falls below a certain threshold. However, there is a bug in the current implementation where the `checkUpkeep()` function may repeatedly return `true` but the subsequent `performUpkeep()` call will revert. This is because the conditions in the `checkUpkeep()` function are connected by `||` instead of `&&`. To fix this, the recommendation is to use `&&` instead of `||` or to call `checkUpkeep()` at the beginning of `performUpkeep()`.

### Original Finding Content

**Update**
Addressed in: `86dc611b71111c038fbf0f1c30ed15f6d2fd2a17`.

**File(s) affected:**`HotWalletTransferer.sol`

**Description:** As part of a separate exchange platform, the developers plan to launch a Chainlink Upkeep based on the `HotWalletTransferer` contract on the Chainlink Automation Network that enables the funds in some `hotWallet` address to be relatively low but automatically resupplied if it falls below some threshold by transferring over tokens from some `holder` address through an ERC777-operator.

However, the current implementation is flawed in that there can be cases where the `checkUpKeep()` function repeatedly returns `true`, yet the costly on-chain call of `performUpkeep()` will revert. If the conditions do not change, the Upkeep will initiate an on-chain call of `performUpkeep()`_every block_ until the `LINK` balance is below the minimum balance.

The inefficiency lies in the fact that the two conditions are logically connected by `||` instead of `&&`. This would mean that `checkUpkeep()` would return true and initiate a reverting call if either the `hotWallet` address balance is below the threshold, yet the `holder` wallet is not sufficiently funded or the `hotWallet` address does not require funding, but the `holder` address balance is sufficiently high. Both conditions need to be true for the `performUpkeep()` to not revert and perform the funding of the `hotWallet` address.

**Recommendation:** In the `checkUpKeep()` function, bind the two conditions with `&&` instead of `||`. That way, the `performUpkeep()` function will not repeatedly revert in the two described cases and the vast majority of on-chain calls should complete the token transfer. Another approach could be to call `checkUpkeep()` at the beginning of `performUpkeep()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Bretton Woods Digital Gold |
| Report Date | N/A |
| Finders | Guillermo Escobero, Ruben Koch, Jeffrey Kam, Gelei Deng |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/bretton-woods-digital-gold/6a607c09-57af-4640-97bd-ee122e1ed0a6/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/bretton-woods-digital-gold/6a607c09-57af-4640-97bd-ee122e1ed0a6/index.html

### Keywords for Search

`vulnerability`

