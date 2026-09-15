---
# Core Classification
protocol: Hyperstable_2025-03-19
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57826
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Hyperstable-security-review_2025-03-19.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-02] `delegateBySig()` wrongly limits delegation

### Overview


The `delegateBySig()` function in the `vePeg` contract is not working as intended. It is supposed to allow anyone with a valid signature to delegate votes on behalf of someone else, but currently it can only be accessed by the owner or approved address of the lock (NFT). This goes against the purpose of delegation by signature and prevents external parties from delegating votes. To fix this, the check restricting the caller to be the owner or operator should be removed from the function.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The `delegateBySig()` function in the `vePeg` contract is intended to allow anyone with a valid signature to delegate votes on behalf of a delegator. However, the issue is that this function includes a check requiring the caller to be the owner or operator (approved address) of the lock (NFT) to access it. This makes the function effectively useless for delegation by signature, as it should be callable by anyone with a valid signature, regardless of the caller status:

```solidity
function delegateBySig(uint256 from, uint256 to, uint256 nonce, uint256 expiry, uint8 v, bytes32 r, bytes32 s)
        public
    {
        //...
        require(_isApprovedOrOwner(msg.sender, from), "Not approved");
        //...
    }
```

This behavior prevents the delegation from being done by an external party with a valid signature, contradicting the intended design and functionality of delegation by signature.

## Recommendations

Remove the check that restricts the caller to be the owner or operator, as the `delegateBySig()` function should allow anyone with a valid signature to delegate votes:

```diff
 function delegateBySig(uint256 from, uint256 to, uint256 nonce, uint256 expiry, uint8 v, bytes32 r, bytes32 s)
        public
    {
        //...
-       require(_isApprovedOrOwner(msg.sender, from), "Not approved");
        //...
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Hyperstable_2025-03-19 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Hyperstable-security-review_2025-03-19.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

