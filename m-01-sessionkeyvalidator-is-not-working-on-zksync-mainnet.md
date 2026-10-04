---
# Core Classification
protocol: Clave_2024-12-23
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50028
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Clave-security-review_2024-12-23.md
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

[M-01] `SessionKeyValidator` is not working on ZkSync mainnet

### Overview


The bug report discusses an issue with the SessionKeyValidator contract on ZkSync mainnet. This issue has a low impact but a high likelihood of occurring. The problem lies in the `TimestampAsserterLocator.locate` function, which is causing the session key functionality to break on mainnet. This is due to the function explicitly reverting on ZkSync mainnet, causing it to fail. The report recommends updating the `TimestampAsserterLocator` with the mainnet address to fix the issue.

### Original Finding Content

## Severity

**Impact:** Low

**Likelihood:** High

## Description

The SessionKeyValidator contract fails to function on ZkSync mainnet due to the `TimestampAsserterLocator.locate` function explicitly reverting on chainId `324` (ZkSync mainnet). This breaks all session key functionality for mainnet deployments.

```solidity
  function locate() internal view returns (ITimestampAsserter) {
    ...
    if (block.chainid == 324) { // @audit revert if the chain is ZkSync mainnet
      revert("Timestamp asserter is not deployed on ZKsync mainnet yet");
    }
    ...
  }
```

## Recommendations

Update the `TimestampAsserterLocator` with the mainnet address.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Clave_2024-12-23 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Clave-security-review_2024-12-23.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

