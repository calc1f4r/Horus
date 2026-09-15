---
# Core Classification
protocol: Ouroboros_2024-12-06
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45969
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Ouroboros-security-review_2024-12-06.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[L-10] Calls to Chainlink do not prevent griefing attacks

### Overview

See description below for full details.

### Original Finding Content

The `EthPriceFeed.fetchEthPrice()` function calls Chainlink's price aggregator to get the latest price of ETH. If the call to the price aggregator reverts Chainlink oracle is considered broken and its status is set accordingly, requiring the intervention of the guardian to restore it.

```solidity
141:        try priceAggregator.latestRoundData() returns
142:        (
    (...)
156:        } catch {
157:            // If call to Chainlink aggregator reverts, return a zero response with success = false
158:            return chainlinkResponse;
159        }
```

There are two important things to note here:

- If the call to the target function reverts due to an out-of-gas exception, the exception is caught and the `catch` block is executed.
- Only [63/64 of the gas is forwarded](https://eips.ethereum.org/EIPS/eip-150) to the target function.

This means that a grief attack would be possible if a malicious actor called the `fetchEthPrice()` function with a small amount of gas, provoking an out-of-gas exception and causing the Chainlink oracle to be considered broken.

It is important to note that for the main transaction not to revert due to an out-of-gas exception, the outstanding gas (1/64 of the gas forwarded) should be enough to execute the update of the Chainlink oracle status. Or expressed differently, the execution of `priceAggregator.latestRoundData()` needs to consume at least 64 times the gas consumed by the execution of `fetchEthPrice()` after the exception is caught. While this is currently not the case, given that the price aggregator contract acts as a proxy, this could change in the future and make the attack possible.

Consider implementing a solution similar to the one [added in Liquity V2](https://github.com/liquity/bold/commit/68486579f6e10876e0120aa931279390afdd0d87#diff-c6e1b047b66e00e49cfb8eb4d05e549495b8f27e7a1f0e2268c4b342127f7b74R40) to all the calls to the Chainlink oracle.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Ouroboros_2024-12-06 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Ouroboros-security-review_2024-12-06.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

