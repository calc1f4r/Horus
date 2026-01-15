---
# Core Classification
protocol: Folks Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61022
audit_firm: Immunefi
contest_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033443%20-%20%5BSmart%20Contract%20-%20Low%5D%20StalenessCircuitBreakerNode%20checks%20if%20the%20last%20update%20time%20of%20the%20parent%20node%20is%20less%20than%20the%20threshold%20but%20the%20publicTime%20could%20be%20greater%20than%20current%20blocktimestamp.md
source_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033443%20-%20%5BSmart%20Contract%20-%20Low%5D%20StalenessCircuitBreakerNode%20checks%20if%20the%20last%20update%20time%20of%20the%20parent%20node%20is%20less%20than%20the%20threshold%20but%20the%20publicTime%20could%20be%20greater%20than%20current%20blocktimestamp.md
github_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033443%20-%20%5BSmart%20Contract%20-%20Low%5D%20StalenessCircuitBreakerNode%20checks%20if%20the%20last%20update%20time%20of%20the%20parent%20node%20is%20less%20than%20the%20threshold%20but%20the%20publicTime%20could%20be%20greater%20than%20current%20blocktimestamp.md

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
finders_count: 1
finders:
  - Tripathi
---

## Vulnerability Title

StalenessCircuitBreakerNode checks if the last update time of the parent node is less than the threshold but the `publicTime` could be greater than current `block.timestamp`

### Overview

See description below for full details.

### Original Finding Content




Report type: Smart Contract


Target: https://testnet.snowtrace.io/address/0xA758c321DF6Cd949A8E074B22362a4366DB1b725

Impacts:
- Contract fails to deliver promised returns, but doesn't lose value

## Description
## Brief/Intro
StalenessCircuitBreakerNode checks if the last update time of the parent node is less than the threshold but the `publicTime` could be greater than current `block.timestamp` .

`PythNode::Process()` calls `pyth.getEmaPriceUnsafe()` and `pyth.getPriceUnsafe()` for fetching price. 

Issue is In `StalenessCircuitBreakerNode` `stalenessTolerance`is conceived as the maximum number of seconds that the price can be in the past(compared to block.timestamp) but in reality the price could also be in future

## Vulnerability Details

This fact is corroborated by the logic inside Pyth SDK that performs an abs delta between the `price.publishTime` in `[getPriceNoOlderThan](https://github.com/pyth-network/pyth-crosschain/blob/main/target_chains/ethereum/sdk/solidity/AbstractPyth.sol#L48-L58)`. In the [near SDK](https://github.com/pyth-network/pyth-crosschain/blob/main/target_chains/near/receiver/src/lib.rs#L503-L505) the check is even more explicit

Let's analyse `getPriceUnsafe()`
```js
  pub fn get_price_unsafe(&self, price_identifier: PriceIdentifier) -> Option<Price> {
        self.get_price_no_older_than(price_identifier, u64::MAX)
    }

    /// Get the latest available price cached for the given price identifier, if that price is
    /// no older than the given age.
    pub fn get_price_no_older_than(
        &self,
        price_id: PriceIdentifier,
        age: Seconds,
    ) -> Option<Price> {
        self.prices.get(&price_id).and_then(|feed| {
            let block_timestamp = env::block_timestamp() / 1_000_000_000;
            let price_timestamp = feed.price.publish_time;

            // - If Price older than STALENESS_THRESHOLD, set status to Unknown.
            // - If Price newer than now by more than STALENESS_THRESHOLD, set status to Unknown.
            // - Any other price around the current time is considered valid.
            if u64::abs_diff(block_timestamp, price_timestamp.try_into().unwrap()) > age {
                return None;
            }

            Some(feed.price)
        })
    }
```
https://github.com/pyth-network/pyth-crosschain/blob/main/target_chains/near/receiver/src/lib.rs#L491

we can see that absolute difference is taken between`price.publishtime` and age which shows that `price.publishtime` could be greater than `block.timestamp` but during staleness check `stalenessTolerance` is used for only previous prices 
## Impact Details
`price.publishtime` could be greater than block.timestamp. In such case fetching price will revert due to underflow since `block.timestamp < price.publishtime `

## References

https://github.com/pyth-network/pyth-crosschain/blob/main/target_chains/near/receiver/src/lib.rs#L509
        
## Proof of concept
## Proof of Concept


call `getPriceNoOlderThan()` on any `Pyth` priceFeed and check `price.publishtime`


For more clarifications

Check 5.4.13 of https://github.com/euler-xyz/euler-price-oracle/blob/master/audits/Euler_Price_Oracle_Spearbit_Report_DRAFT.pdf


### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Immunefi |
| Protocol | Folks Finance |
| Report Date | N/A |
| Finders | Tripathi |

### Source Links

- **Source**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033443%20-%20%5BSmart%20Contract%20-%20Low%5D%20StalenessCircuitBreakerNode%20checks%20if%20the%20last%20update%20time%20of%20the%20parent%20node%20is%20less%20than%20the%20threshold%20but%20the%20publicTime%20could%20be%20greater%20than%20current%20blocktimestamp.md
- **GitHub**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033443%20-%20%5BSmart%20Contract%20-%20Low%5D%20StalenessCircuitBreakerNode%20checks%20if%20the%20last%20update%20time%20of%20the%20parent%20node%20is%20less%20than%20the%20threshold%20but%20the%20publicTime%20could%20be%20greater%20than%20current%20blocktimestamp.md
- **Contest**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033443%20-%20%5BSmart%20Contract%20-%20Low%5D%20StalenessCircuitBreakerNode%20checks%20if%20the%20last%20update%20time%20of%20the%20parent%20node%20is%20less%20than%20the%20threshold%20but%20the%20publicTime%20could%20be%20greater%20than%20current%20blocktimestamp.md

### Keywords for Search

`vulnerability`

