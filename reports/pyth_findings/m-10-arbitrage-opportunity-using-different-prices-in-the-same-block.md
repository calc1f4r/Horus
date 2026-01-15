---
# Core Classification
protocol: Nabla
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36540
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Nabla-security-review.md
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

[M-10] Arbitrage opportunity using different prices in the same block

### Overview


The PythAdapter contract has a bug that allows users to make a profit without any risk. This is because the contract allows for different prices to be used for the same token in the same block. This can be exploited by omitting the token from the update list, using an outdated price, or swapping without updating the price. This means that a user can make a trade with an old price and then make another trade with the updated price in the same block, resulting in a profit. A possible solution would be to store the current price of a token when it is first used in a block and use that price for the rest of the block. This will ensure that the price remains consistent throughout the block.

### Original Finding Content

**Severity**

**Impact:** Medium

**Likelihood:** Medium

**Description**

The current implementation of the `PythAdapter` contract allows using different prices for the same token in the same block. This can be exploited by a malicious user to make a profit with zero risk.

There are different ways of performing an operation without updating the price feed of a certain token:

- Omit the target token in the array sent to `updatePriceFeeds`.
- Submit an outdated price for the target token (`updatePriceFeeds` does not revert in this case).
- Swap through `swapExactTokensForTokensWithoutPriceFeedUpdate`.

This way, a user can perform a swap with an outdated price, and then perform an operation in the opposite direction with the updated price.

> Note that even if it was enforced to successfully update the price feed before any operation, it is still possible to submit later a more recent price in another operation performed in the same block, making it still possible to arbitrage.

**Proof of concept**

At timestamp `t` the prices in the Pyth network are as follows:

- WBTC/USD: $50,000
- USDC/USD: $1

At block `b` `updatePriceFeeds` is called with the above prices.

At timestamp `t + 10` the `WBTC/USD` price increases to $51,000.

At block `b + 1` Alice calls `swapExactTokensForTokens` without updating the `WBTC` price, and swaps 50,000 USDC for 1 WBTC. In the same block, Alice calls `swapExactTokensForTokens` again, this time updating the `WBTC` price to $51,000, and swaps 1 WBTC for 51,000 USDC, making a profit with zero risk.

In this example, we have not taken into account the fees, for simplicity. The trade will be profitable as long as `total fees < Δ price * amount`. In this example, if the fees are less than $1,000 (2%), Alice would have made a profit.

**Recommendations**

A possible solution would be to store the current price of a token the first time it is used in a block, and then use this price for the rest of the block. This way, the price of a token would be consistent throughout the block.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Nabla |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Nabla-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

