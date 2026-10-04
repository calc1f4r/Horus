---
# Core Classification
protocol: Omo_2025-01-25
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53332
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
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

[M-02] Entry point contract cannot interact with `OmoAgent.sol` functions

### Overview


The report states that there is a bug in the `OmoAgent.sol` contract, where most of its functions can only be triggered by the entry point contract, such as `borrowAsset()`, `repayAsset()`, and `topOffToAgent()`. This is due to the `onlyAgent` modifier, which restricts interactions with the entry point. The severity and likelihood of this bug are both medium. The report recommends creating a check in the `OmoAgentStorage` library to address this issue.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

Most of the functions in `OmoAgent.sol` contract will be triggered by the entry point contract e.g.`borrowAsset()`, `repayAsset()`, `topOffToAgent()` and more.
But they have an `onlyAgent` modifier

```solidity
    modifier onlyAgent(uint256 _id) {
        require(msg.sender == OmoAgentStorage.data().agents[_id], "Only agent");
        _;
    }
```

This will prevent the standard’s intended behavior of ERC4337 (limiting interactions with the EntryPoint).

## Recommendations

The struct `Data` in the library `OmoAgentStorage` should have the address of `EntryPoint` and create a check similar to `_requireFromEntryPoint()`

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Omo_2025-01-25 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

