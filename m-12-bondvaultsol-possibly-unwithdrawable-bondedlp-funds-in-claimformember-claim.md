---
# Core Classification
protocol: Spartan Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42265
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-07-spartan
source_link: https://code4rena.com/reports/2021-07-spartan
github_link: https://github.com/code-423n4/2021-07-spartan-findings/issues/42

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

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - rwa

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-12] `BondVault.sol`: Possibly unwithdrawable bondedLP funds in `claimForMember()` + `claimRate` never zeros after full withdrawals

### Overview


The report discusses a bug found in the `claimForMember()` function, where the `_claimable` value is deducted from the bondedLP balance before a condition check is performed. This can lead to two issues: 1) if the `_claimable` value is exactly half of the remaining bondedLP balance, the other half will be permanently locked, and 2) if a user performs a full withdrawal, their claim rate for that asset will not be set to zero as expected. The suggested solution is to either change the order of the deduction and condition check, or change the condition check itself. The bug has been confirmed and a mitigation has been suggested.

### Original Finding Content

_Submitted by hickuphh3, also found by 0xRajeev_

A host of problems arise from the L110-113 of the `claimForMember()` function, where `_claimable` is deducted from the bondedLP balance before the condition check, when it should be performed after (or the condition is changed to checking if the remaining bondedLP balance to zero).

```jsx
// L110 - L113
mapBondAsset_memberDetails[asset].bondedLP[member] -= _claimable; // Remove the claim amount from the user's remainder
if(_claimable == mapBondAsset_memberDetails[asset].bondedLP[member]){
	mapBondAsset_memberDetails[asset].claimRate[member] = 0; // If final claim; zero-out their claimRate
}
```
**1. Permanently Locked Funds**

If a user claims his bonded LP asset by calling `dao.claimForMember()`, or a malicious attacker helps a user to claim by calling `dao.claimAllForMember()`, either which is done such that `_claimable` is exactly half of his remaining bondedLP funds of an asset, then the other half would be permanently locked.

- Assume `mapBondAsset_memberDetails[asset].bondedLP[member] = 2 * _claimable`
- L110: `mapBondAsset_memberDetails[asset].bondedLP[member] = _claimable`
- L111: The if condition is satisfied
- L112: User's claimRate is erroneously set to 0 ⇒ `calcBondedLP()` will return 0, ie. funds are locked permanently

**2. Claim Rate Never Zeroes For Final Claim**

On the flip side, should a user perform a claim that enables him to perform a full withdrawal (ie. `_claimable` = `mapBondAsset_memberDetails[asset].bondedLP[member]`, we see the following effects:

- L110: `mapBondAsset_memberDetails[asset].bondedLP[member] = 0`
- L111: The if condition is not satisfied, L112 does not execute, so the member's claimRate for the asset remains non-zero (it is expected to have been set to zero).

Thankfully, subsequent behavior remains as expected since `calcBondedLP` returns zero as `claimAmount` is set to the member's bondedLP balance (which is zero after a full withdrawal).

The `_claimable` deduction should occur after the condition check. Alternatively, change the condition check to `if (mapBondAsset_memberDetails[asset].bondedLP[member] == 0)`.

**[verifyfirst (Spartan) confirmed](https://github.com/code-423n4/2021-07-spartan-findings/issues/42#issuecomment-885453442):**
 > Good find, suggested mitigation solves the potential to lock funds.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Spartan Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-07-spartan
- **GitHub**: https://github.com/code-423n4/2021-07-spartan-findings/issues/42
- **Contest**: https://code4rena.com/reports/2021-07-spartan

### Keywords for Search

`vulnerability`

