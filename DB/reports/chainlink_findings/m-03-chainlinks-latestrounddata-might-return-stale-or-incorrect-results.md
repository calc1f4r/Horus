---
# Core Classification
protocol: Perennial
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25609
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-12-perennial
source_link: https://code4rena.com/reports/2021-12-perennial
github_link: https://github.com/code-423n4/2021-12-perennial-findings/issues/24

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
  - dexes
  - cdp
  - services
  - synthetics
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-03] Chainlink's `latestRoundData` might return stale or incorrect results

### Overview


The ChainlinkOracle.sol file is missing checks for stale data when using the latestRoundData() function. This could lead to stale prices being used according to the Chainlink documentation. kbrizzle (Perennial) and Alex the Entreprenerd (judge) both agree that checks should be added to ensure that the data is fresh and within rational bounds. An example of a check that should be added is a require statement that the feedPrice is greater than 0 and that the roundID is greater than or equal to the answeredInRound. This will ensure that the data is not stale and is within reasonable bounds.

### Original Finding Content

_Submitted by WatchPug, also found by cmichel, defsec, and ye0lde_

<https://github.com/code-423n4/2021-12-perennial/blob/fd7c38823833a51ae0c6ae3856a3d93a7309c0e4/protocol/contracts/oracle/ChainlinkOracle.sol#L50-L60>

```solidity
function sync() public {
    (, int256 feedPrice, , uint256 timestamp, ) = feed.latestRoundData();
    Fixed18 price = Fixed18Lib.ratio(feedPrice, SafeCast.toInt256(_decimalOffset));

    if (priceAtVersion.length == 0 || timestamp > timestampAtVersion[currentVersion()] + minDelay) {
        priceAtVersion.push(price);
        timestampAtVersion.push(timestamp);

        emit Version(currentVersion(), timestamp, price);
    }
}
```

On `ChainlinkOracle.sol`, we are using `latestRoundData`, but there is no check if the return value indicates stale data. This could lead to stale prices according to the Chainlink documentation:

*   <https://docs.chain.link/docs/historical-price-data/#historical-rounds>
*   <https://docs.chain.link/docs/faq/#how-can-i-check-if-the-answer-to-a-round-is-being-carried-over-from-a-previous-round>

#### Recommendation

Consider adding missing checks for stale data.

For example:

```solidity
(uint80 roundID, int256 feedPrice, , uint256 timestamp, uint80 answeredInRound) = feed.latestRoundData();
require(feedPrice > 0, "Chainlink price <= 0"); 
require(answeredInRound >= roundID, "Stale price");
require(timestamp != 0, "Round not complete");
```

**[kbrizzle (Perennial) confirmed](https://github.com/code-423n4/2021-12-perennial-findings/issues/24)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2021-12-perennial-findings/issues/24#issuecomment-1001295232):**
 > Agree with the finding, while you can get started with Chainlink's feed can be used with one line of code, in a production environment it is best to ensure that the data is fresh and within rational bounds



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Perennial |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-perennial
- **GitHub**: https://github.com/code-423n4/2021-12-perennial-findings/issues/24
- **Contest**: https://code4rena.com/reports/2021-12-perennial

### Keywords for Search

`vulnerability`

