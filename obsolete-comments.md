---
# Core Classification
protocol: Tsunami GMX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47814
audit_firm: OtterSec
contest_link: https://tsunami.finance/
source_link: https://tsunami.finance/
github_link: https://github.com/Tsunami-Finance/tsunami-contracts

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
finders_count: 3
finders:
  - Robert Chen
  - Woosun Song
  - OtterSec
---

## Vulnerability Title

Obsolete Comments

### Overview

See description below for full details.

### Original Finding Content

## Code Comment Update in VaultPriceFeed.sol

The comment: 

```solidity
// Chainlink can return prices for stablecoins in
// VaultPriceFeed is obsolete as Pyth returns the prices.
```

## VaultPriceFeed.sol SOLIDITY

```solidity
contract VaultPriceFeed is IVaultPriceFeed {
    [...]
    // Chainlink can return prices for stablecoins
    // that differs from 1 USD by a larger percentage than stableSwapFeeBasisPoints
    // we use strictStableTokens to cap the price to 1 USD
    // this allows us to configure stablecoins like DAI as being a stableToken
    // while not being a strictStableToken
    mapping (address => bool) public strictStableTokens;
    [...]
}
```

## Remediation

Remove the comment and replace it with the following:

```solidity
// Pyth can return prices for stablecoins.
```

## Patch

Fixed in `18460e8`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Tsunami GMX |
| Report Date | N/A |
| Finders | Robert Chen, Woosun Song, OtterSec |

### Source Links

- **Source**: https://tsunami.finance/
- **GitHub**: https://github.com/Tsunami-Finance/tsunami-contracts
- **Contest**: https://tsunami.finance/

### Keywords for Search

`vulnerability`

