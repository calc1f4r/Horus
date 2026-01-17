---
# Core Classification
protocol: Numoen
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6520
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-01-numoen-contest
source_link: https://code4rena.com/reports/2023-01-numoen
github_link: #l-04-minting-tokens-to-the-zero-address-should-be-avoided

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

protocol_categories:
  - liquid_staking
  - dexes
  - lending
  - bridge
  - yield

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-04] Minting tokens to the zero address should be avoided

### Overview

See description below for full details.

### Original Finding Content

The core function `mint` is used by users to mint an option position by providing token1 as collateral and borrowing the max amount of liquidity. Address(0) check is missing in both this function and the internal function `_mint`, which is triggered to mint the tokens to the `to` address. Consider applying a check in the function to ensure tokens aren't minted to the zero address.

```solidity
src/core/Lendgine.sol

71:  function mint(
72:    address to,
73:    uint256 collateral,
74:    bytes calldata data
75:  )
76:    external
77:    override
78:    nonReentrant
79:    returns (uint256 shares)
80:  {
81:    _accrueInterest();
82:
83:    uint256 liquidity = convertCollateralToLiquidity(collateral);
84:    shares = convertLiquidityToShare(liquidity);
85:
86:    if (collateral == 0 || liquidity == 0 || shares == 0) revert InputError();
87:    if (liquidity > totalLiquidity) revert CompleteUtilizationError();
88:    // next check is for the case when liquidity is borrowed but then was completely accrued
89:    if (totalSupply > 0 && totalLiquidityBorrowed == 0) revert CompleteUtilizationError();
90:
91:    totalLiquidityBorrowed += liquidity;
92:    (uint256 amount0, uint256 amount1) = burn(to, liquidity);
93:    _mint(to, shares);
94:
95:    uint256 balanceBefore = Balance.balance(token1);
96:    IMintCallback(msg.sender).mintCallback(collateral, amount0, amount1, liquidity, data);
97:    uint256 balanceAfter = Balance.balance(token1);
98:
99:    if (balanceAfter < balanceBefore + collateral) revert InsufficientInputError();
100:
101:    emit Mint(msg.sender, collateral, shares, liquidity, to);
102:  }
```



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Numoen |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-numoen
- **GitHub**: #l-04-minting-tokens-to-the-zero-address-should-be-avoided
- **Contest**: https://code4rena.com/contests/2023-01-numoen-contest

### Keywords for Search

`vulnerability`

