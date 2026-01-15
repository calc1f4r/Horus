---
# Core Classification
protocol: AAVE
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56807
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/AAVE/Umbrella/README.md#1-underflow-with-_coverdeficit
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.60
financial_impact: medium

# Scoring
quality_score: 3
rarity_score: 3

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Underflow with `_coverDeficit()`

### Overview


The report describes a bug in the Umbrella contract where an attacker can transfer tokens directly to the contract, causing an error when certain functions are triggered. This is because the function responsible for transferring tokens returns the entire contract balance instead of just the portion sent by the attacker. The report also mentions that governance has the ability to transfer excess tokens, but the attacker can exploit this by front-running the next function calls. The recommendation is to fix the function to account for the scenario where the contract already holds funds.

### Original Finding Content

##### Description
An attacker can directly transfer tokens to the Umbrella contract, causing an underflow error when `Umbrella._setPendingDeficit()` or `Umbrella._setDeficitOffset()` is triggered.

This happens because the `_coverDeficit()` function returns the entire contract balance when transferring tokens, rather than just the portion sent by `msg.sender`, and hacker can increase it by a direct transfer:
```solidity
IERC20(aToken).safeTransferFrom(_msgSender(), address(this), amount);
amount = IERC20(aToken).balanceOf(address(this));
```
https://github.com/bgd-labs/aave-umbrella-private/blob/946a220a57b4ae0ad11d088335f9bcbb0e34dcef/src/contracts/umbrella/Umbrella.sol#L148-L151

Governance has the ability to transfer excess tokens via an emergency function. However, an attacker can frontrun the next call to `coverDeficitOffset()` and `coverPendingDeficit()` functions, causing a DoS again.

##### Recommendation
We recommend considering the case where the contract already holds funds when calculating the actual received balance.

***

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3/5 |
| Rarity Score | 3/5 |
| Audit Firm | MixBytes |
| Protocol | AAVE |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/AAVE/Umbrella/README.md#1-underflow-with-_coverdeficit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

