---
# Core Classification
protocol: Stargaze Infinity
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48189
audit_firm: OtterSec
contest_link: https://www.stargaze.zone/
source_link: https://www.stargaze.zone/
github_link: https://github.com/public-awesome/infinity

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
finders_count: 3
finders:
  - James Wang
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Incorrect Calculation For Linear Curves

### Overview


The bug report discusses an issue with the pricing of pools in the Infinity Swap platform. There are three different curves that pool owners can choose from to set prices, and for Trade pools, dealers can buy and sell NFTs to the pool. However, there is a problem with the calculation of the buy price for NFTs using the Linear curve, which can result in pools buying NFTs at a higher price than they should. This can lead to a loss of funds for pool owners. The bug is caused by an error in the code and has been fixed in the latest patch.

### Original Finding Content

## Pricing Curves for Pools

While setting prices of pools, owners have three curves to choose from: **Linear**, **Exponential**, and **Constant Product**. Additionally, for Trade pools, dealers can buy and sell NFTs to the pool. 

`get_buy_quote` and `get_sell_quote` are used to calculate the price where pools buy and sell NFTs. Since all pricing curves support dynamic prices and Trade pools essentially allow the price to move in both directions, it is crucial for infinity to ensure that pools will not suffer a loss from a sequence of buy and sell actions.

To simplify, if a pool buys an NFT and then sells it immediately, the number of tokens spent on buying the NFT should not exceed the number of tokens collected from selling the NFT. This rule is enforced by the following logic:

- When a pool buys an NFT, the price is calculated with respect to the pool state after the swap has finished.
- When a pool sells an NFT, the price is calculated with respect to the current pool state.

These rules ensure that the pool state will always be restored if N sells + N buys occur. However, an error in calculating the NFT buy price causes pools using Linear curves to buy at a higher price than it should. This potentially leads to a loss of funds for pool owners and is shown in the code snippet below:

```rust
// File: infinity-swap/src/pool.rs
pub fn get_buy_quote(&self, min_quote: Uint128) -> Result<Option<Uint128>, ContractError> {
    // Calculate the buy price with respect to pool types and bonding curves
    let buy_price = match self.pool_type {
        PoolType::Token => Ok(self.spot_price),
        PoolType::Nft => Err(ContractError::InvalidPool("pool cannot buy nfts".to_string())),
        PoolType::Trade => match self.bonding_curve {
            BondingCurve::Linear => self.spot_price
                .checked_add(self.delta)
                .map_err(|e| ContractError::Std(StdError::overflow(e))),
            // ...
        },
    }?;
    // If the pool has insufficient tokens to buy the NFT, return None
    if self.total_tokens < buy_price || buy_price < min_quote {
        return Ok(None);
    }
    Ok(Some(buy_price))
}
```

## Infinity Swap Audit 04 | Vulnerabilities

### Remediation

Calculate the correct price when acquiring NFTs.

```rust
// File: infinity-swap/src/pool.rs
pub fn get_buy_quote(&self, min_quote: Uint128) -> Result<Option<Uint128>, ContractError> {
    // Calculate the buy price with respect to pool types and bonding curves
    let buy_price = match self.pool_type {
        // ...
        PoolType::Trade => match self.bonding_curve {
            BondingCurve::Linear => self.spot_price
                .checked_add(self.delta)
                .checked_sub(self.delta)
                .map_err(|e| ContractError::Std(StdError::overflow(e))),
            // ...
        },
    }?;
    // ...
}
```

### Patch

Resolved in **4453377**.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Stargaze Infinity |
| Report Date | N/A |
| Finders | James Wang, Robert Chen, OtterSec |

### Source Links

- **Source**: https://www.stargaze.zone/
- **GitHub**: https://github.com/public-awesome/infinity
- **Contest**: https://www.stargaze.zone/

### Keywords for Search

`vulnerability`

