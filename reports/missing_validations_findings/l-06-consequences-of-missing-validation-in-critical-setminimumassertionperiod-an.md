---
# Core Classification
protocol: Arbitrum Foundation
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33544
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-05-arbitrum-foundation
source_link: https://code4rena.com/reports/2024-05-arbitrum-foundation
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-06] Consequences of Missing Validation in critical `setMinimumAssertionPeriod` and `setBaseStake` Functions

### Overview

See description below for full details.

### Original Finding Content


The function setMinimumAssertionPeriod sets the minimumAssertionPeriod state variable to newPeriod without performing any validation checks. This lack of validation can lead to the assignment of invalid or unreasonable values, which can adversely affect the contract's behavior and security. Same to `setBaseStake()` function.

```solidity
FILE: 2024-05-arbitrum-foundation/src/rollup
/RollupAdminLogic.sol

function setMinimumAssertionPeriod(uint256 newPeriod) external override {
        minimumAssertionPeriod = newPeriod;
        emit OwnerFunctionCalled(8);
    }

function setBaseStake(uint256 newBaseStake) external override {
        baseStake = newBaseStake;
        emit OwnerFunctionCalled(12);
    }

``` 
https://github.com/code-423n4/2024-05-arbitrum-foundation/blob/6f861c85b281a29f04daacfe17a2099d7dad5f8f/src/rollup/RollupAdminLogic.sol#L204-L207



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Arbitrum Foundation |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-05-arbitrum-foundation
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-05-arbitrum-foundation

### Keywords for Search

`vulnerability`

