---
# Core Classification
protocol: StationX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41392
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/StationX-security-review.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-08] Cross-chain deposits will fail when the deposit token is the native token

### Overview


This bug report discusses a problem with the `crossChainMint()` function in a cross-chain DAO contract. The function calculates the `_daoBalance` using a `balanceOf()` call on a contract address, but the issue is that the DAO can be deployed with a native token that does not have a contract address. This means that any user trying to buy DAO tokens will have their transaction fail because the function is trying to call `balanceOf()` on a non-existing contract. The recommendation is to check the balance of the native token in case the DAO was deployed with it.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

The `crossChainMint()` function calculates the `_daoBalance` as:

```solidity
uint256 _daoBalance = IERC20(_daoDetails.depositTokenAddress).balanceOf(_daoAddress);
```

The problem is that the cross-chain DAO can be deployed with the native token (defined in the contract as address: `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`).

So, anytime a user tries to buy cross-chain DAO tokens, they will deposit tokens but the transaction on the destination chain will always revert as it will try to perform a `balanceOf()` call on a non-existing contract.

## Recommendations

Check the native token balance in case the cross-chain DAO was deployed with it.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | StationX |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/StationX-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

