---
# Core Classification
protocol: Burve_2025-01-29
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55212
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Burve-security-review_2025-01-29.md
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

[H-01] Missing transfer of tokens before island.mint()

### Overview


The Burve contract has a bug that prevents users from successfully providing liquidity to the island pool through the contract. This happens because the contract does not transfer the necessary tokens before calling `Burve.mint()`, resulting in a failed transaction. To fix this, the contract should be updated to transfer and approve the required tokens before calling `island.mint()`. This bug has a medium impact and a high likelihood of occurring.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

The Burve contract allows users to provide liquidity to both the island pool and Uniswap V3 pools. When adding liquidity to the island pool, it will transfer tokens in from the sender (which is the Burve contract itself) before providing liquidity to Uniswap.

```solidity
    function mint(address recipient, uint128 liq) external {
        for (uint256 i = 0; i < distX96.length; ++i) {
            uint128 liqAmount = uint128(shift96(liq * distX96[i], true));
            mintRange(ranges[i], recipient, liqAmount);
        }

        _mint(recipient, liq);
    }
```

However, when users call `Burve.mint()`, it does not transfer the necessary tokens beforehand. This results in a failed transaction, preventing users from successfully providing liquidity to the island pool through the Burve contract.

## Recommendations

Ensure the required tokens are transferred and approved before calling `island.mint()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Burve_2025-01-29 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Burve-security-review_2025-01-29.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

