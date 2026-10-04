---
# Core Classification
protocol: Ionprotocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36439
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/IonProtocol-security-review.md
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

[M-05] Non-whitelisted addresses can be lenders

### Overview


This bug report discusses a low severity issue in the Ion Protocol. The problem is that only users on the whitelist are supposed to earn interest from lending tokens, but there is a way for non-whitelisted users to receive interest by having the tokens transferred to them. The report suggests disabling transfers for Ion pools with a whitelist as a potential solution, but the Ion Protocol team has commented that they do not intend to restrict transfers and the whitelist was only meant to be a temporary measure. Therefore, they will not be fixing this issue. 

### Original Finding Content

**Severity**

**Impact:** Low

**Likelihood:** High

**Description**

Only users that are on the whitelist are allowed to earn interest from lending the underlying tokens:

```solidity
    function supply(
        address user,
        uint256 amount,
        bytes32[] calldata proof
    )
        external
        whenNotPaused
>>      onlyWhitelistedLenders(user, proof)
    {
```

However, the transferability of the reward token opens an opportunity for users who are not on the list to receive interest-accruing tokens simply by having them transferred.

**Recommendations**

It is not possible to pass proof to the Whitelist contract within an ERC20 `_transfer` function. Therefore, a potential solution could be to disable transfers for Ion pools that have a whitelist.

**Ion Protocol comments**

It is by design that `Whitelist` only serves to limit who can receive the minted `iToken`s. If the owner of that `iToken` wishes to transfer the tokens to a different address, we do not intend to restrict it.

In addition, the `Whitelist` was only meant to serve as a safeguard for the protocol's initial rollout and will not be a persistent feature.

Will not fix.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Ionprotocol |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/IonProtocol-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

