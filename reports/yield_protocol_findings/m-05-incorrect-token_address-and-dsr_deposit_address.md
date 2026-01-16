---
# Core Classification
protocol: Nexus_2024-11-29
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44991
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Nexus-security-review_2024-11-29.md
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

[M-05] Incorrect `TOKEN_ADDRESS` and `DSR_DEPOSIT_ADDRESS`

### Overview


This bug report discusses an issue with the `DSRStrategy` contract on the Ethereum mainnet. The contract declares incorrect addresses for `TOKEN_ADDRESS` and `DSR_DEPOSIT_ADDRESS`, which are meant to represent the `sDAI` contract for depositing `DAI` tokens and earning yield. The current addresses point to an account with no code, preventing any operations or interactions with the intended address. To fix this issue, the `TOKEN_ADDRESS` and `DSR_DEPOSIT_ADDRESS` should be updated to the correct address on the ETH Mainnet, which is `sDAI: 0x83F20F44975D03b1b09e64809B757c47f942BEeA`. This bug has a low impact but a high likelihood of occurring.

### Original Finding Content

## Severity

**Impact:** Low

**Likelihood:** High

## Description

The `DSRStrategy` declares incorrect contract addresses for `TOKEN_ADDRESS` and `DSR_DEPOSIT_ADDRESS`, which are intended to represent the `sDAI` contract for depositing `DAI` tokens and earning yield.

```solidity
//mainnet
address public constant TOKEN_ADDRESS=0x3F1c547b21f65e10480dE3ad8E19fAAC46C95034;

address public constant DSR_DEPOSIT_ADDRESS=0x3F1c547b21f65e10480dE3ad8E19fAAC46C95034;
```

The `DSRStrategy` is primarily used as the implementation strategy for the DepositUSD contract on the Ethereum mainnet. However, the current addresses point to an [account](https://etherscan.io/address/0x3F1c547b21f65e10480dE3ad8E19fAAC46C95034) with no code.

This will prevent all operations and interactions with the intended address.

## Recommendations

Update the `TOKEN_ADDRESS` and `DSR_DEPOSIT_ADDRESS` to the correct address:
`sDAI: 0x83F20F44975D03b1b09e64809B757c47f942BEeA` (ETH Mainnet).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Nexus_2024-11-29 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Nexus-security-review_2024-11-29.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

