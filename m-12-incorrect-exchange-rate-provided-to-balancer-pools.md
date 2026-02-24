---
# Core Classification
protocol: Renzo
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33507
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-renzo
source_link: https://code4rena.com/reports/2024-04-renzo
github_link: https://github.com/code-423n4/2024-04-renzo-findings/issues/113

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

protocol_categories:
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Bauchibred
  - LessDupes
---

## Vulnerability Title

[M-12] Incorrect exchange rate provided to Balancer pools

### Overview


The xRenzoDeposit contract, which handles deposits on L2s and provides exchange rates for Balancer pools, has a bug in its getRate() function. This function returns an incorrect and potentially outdated exchange rate, which can lead to mispricing of tokens and manipulation of pool joins and exits. To fix this issue, the getRate() function should be updated to use the same exchange rate used when minting xezETH. This will ensure consistency and prevent stale prices from being used. The Renzo team has confirmed the bug and implemented a mitigation to address it. 

### Original Finding Content


The [`xRenzoDeposit`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/Bridge/L2/xRenzoDeposit.sol) contract, apart from being the entry point for deposits on L2s, also acts as a rate provider for Balancer pools on L2s, allowing them to determine the exchange rate between `xezWETH` and `WETH` tokens. Rate providers are crucial for Balancer pools to calculate token prices and determine yield protocol fees during joins and exits, as explained in the [Balancer documentation](https://docs.balancer.fi/reference/contracts/rate-providers.html).

However, the [`getRate()`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/Bridge/L2/xRenzoDeposit.sol#L456) function in `xRenzoDeposit` does not provide the correct exchange rate. It simply returns the `lastPrice` state variable, which:

- May be stale if `updatePrice()` or `updatePriceByOwner()` have not been called recently.
- May be older than the rate provided by `oracle.getMintRate()`.
- Can be different from the rate at which xezETH are minted in [`_deposit()`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/Bridge/L2/xRenzoDeposit.sol#L227), which uses the newest of the oracle and internal `lastPrice` values, opening up arbitrage opportunities.

### Impact

By providing an incorrect and potentially outdated exchange rate, `xRenzoDeposit` can cause Balancer pools to misprice `xezWETH` relative to `WETH`. This can lead to incorrect yield calculations and enable manipulation of pool joins and exits.

### Proof of Concept

1. `xRenzoDeposit` is set as the rate provider between `xezWETH` and `WETH` for a Balancer pool.
2. The price of `ezETH` relative to `ETH` changes on L1, but the receiver fails and `updatePrice()` is not called on `xRenzoDeposit`.
3. However, the oracle feed still provides accurate data.
4. A user executes an operation on a WETH/xezETH Balancer pool, which calls `getRate()` on `xRenzoDeposit` to fetch the price.
5. `getRate()` returns the stale price from the internal `lastPrice` variable.
6. The Balancer pool uses this incorrect rate for its calculations, leading to mispricing of `xezWETH` and potential manipulation.

### Recommended Mitigation Steps

Update the `getRate()` function to provide the same exchange rate used when minting `xezETH`. This can be achieved by calling `getMintRate()` instead of returning `lastPrice` directly:

```diff
- return lastPrice;
+ (uint256 rate, uint256 timestamp) = getMintRate();
+ require(block.timestamp <= timestamp + 1 days, "Price is stale");
+ return rate;
```

This ensures that the rate provided to Balancer pools is consistent with the actual minting rate and is not stale.

**[jatinj615 (Renzo) confirmed](https://github.com/code-423n4/2024-04-renzo-findings/issues/113#event-12880180154)**

**[Renzo mitigated](https://github.com/code-423n4/2024-06-renzo-mitigation?tab=readme-ov-file#scope):**
> The PR adds staleness check in `getRate` function for `balancerPools` on L2.

**Status:** Mitigation confirmed. Full details in reports from [0xCiphky](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/15), [grearlake](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/54), [Fassi\_Security](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/47), [LessDupes](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/32), and [Bauchibred](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/29).



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Renzo |
| Report Date | N/A |
| Finders | Bauchibred, LessDupes |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-renzo
- **GitHub**: https://github.com/code-423n4/2024-04-renzo-findings/issues/113
- **Contest**: https://code4rena.com/reports/2024-04-renzo

### Keywords for Search

`vulnerability`

