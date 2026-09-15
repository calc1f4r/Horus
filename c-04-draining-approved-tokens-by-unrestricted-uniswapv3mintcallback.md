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
solodit_id: 55211
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Burve-security-review_2025-01-29.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.70
financial_impact: high

# Scoring
quality_score: 3.5
rarity_score: 2.5

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[C-04] Draining approved tokens by unrestricted `uniswapV3MintCallback()`

### Overview


The bug report states that there is a high severity and likelihood bug in the `Burve` smart contract. The contract has an external function called `uniswapV3MintCallback` which does not have any access control. This function takes in three parameters and decodes the `data` parameter to get an address. It then transfers tokens from that address to the liquidity pool. This means that an attacker can see which addresses have approved the `Burve` contract and can transfer tokens from those addresses to the pool. This can result in a direct loss of funds for the users. The recommendation is to restrict this function so that only the pool can call it.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** High

## Description

`Burve::uniswapV3MintCallback` is an external function with no access control. This function takes three parameters: `amount0Owed`, `amount1Owed`, and `data`. It then decodes `data` to get an address and transfers tokens from that address to the liquidity pool (lp). An attacker could see which addresses have approved to `Burve.sol` and transfer tokens from those addresses to the pool.

```solidity
  function uniswapV3MintCallback(uint256 amount0Owed, uint256 amount1Owed, bytes calldata data) external {
        address source = abi.decode(data, (address));
        TransferHelper.safeTransferFrom(token0, source, address(pool), amount0Owed);
        TransferHelper.safeTransferFrom(token1, source, address(pool), amount1Owed);
    }
```

1. Provide `data` which decodes to a user address with a hanging approval to `Burve` and amounts equal to the approved amounts
2. As the function has no access control, the funds will be transferred into the pool
3. This causes a direct loss of funds for the users

## Recommendations

Restrict this function so that only the pool can call it.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3.5/5 |
| Rarity Score | 2.5/5 |
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

