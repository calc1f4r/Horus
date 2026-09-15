---
# Core Classification
protocol: Splits Oracle
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31834
audit_firm: ZachObront
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-splits-oracle.md
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
  - Zach Obront
---

## Vulnerability Title

[H-01] UniV3 Oracle unsafe on L2s in event of Sequencer downtime

### Overview


This bug report addresses an issue with the UniV3 oracle, which is used to determine the time weighted price of a pool. The report explains that the oracle uses a function called `consult()` to query the pool and calculate the price. However, if there has been no recent observation of the pool, the oracle will assume that the latest observation is still accurate. This can create a problem if the oracle goes down and comes back online, as it will continue to use the outdated price until it is able to query the pool again. This could potentially allow an attacker to exploit the outdated price and manipulate transactions.

The report recommends using the Chainlink oracle instead, as it has measures in place to prevent this issue. However, in the event that the Uniswap oracle must be used, the report suggests implementing changes such as checking the Chainlink Sequencer Feed to confirm the oracle is up, and ensuring that the oracle has been up for at least 1 hour before querying the pool. These changes have been implemented in the code and can be seen in specific commits.

Overall, this report highlights the potential vulnerability of the UniV3 oracle and suggests using the Chainlink oracle or implementing specific changes to prevent exploitation. 

### Original Finding Content

The UniV3 oracle uses the built in `consult()` function provided by Uniswap's Oracle Library to query the pool and determine the time weighted price. This takes in a `secondsAgo` and observes the price at `secondsAgo` and `block.timestamp`, returning the time weighted average between these two points.

In the event that we haven't had any observation since `secondsAgo`, we assume the latest observation still holds:
```solidity
    function getSurroundingObservations(
        Observation[65535] storage self,
        uint32 time,
        uint32 target,
        int24 tick,
        uint16 index,
        uint128 liquidity,
        uint16 cardinality
    ) private view returns (Observation memory beforeOrAt, Observation memory atOrAfter) {
        // optimistically set before to the newest observation
        beforeOrAt = self[index];

        // if the target is chronologically at or after the newest observation, we can early return
        if (lte(time, beforeOrAt.blockTimestamp, target)) {
            if (beforeOrAt.blockTimestamp == target) {
                // if newest observation equals target, we're in the same block, so we can ignore atOrAfter
                return (beforeOrAt, atOrAfter);
            } else {
                // otherwise, we need to transform
                return (beforeOrAt, transform(beforeOrAt, target, tick, liquidity));
            }
        }
        ...
}
```
In the event that an L2's sequencer goes down, the time weighted price when it comes back online will be the extrapolated previous price. This will create an opportunity to push through transactions at the old price before it is updated. Even when the new price is observed, it will be assumed by the sequencer that the previous price held up until the moment it came back online, which will result in a slow, time weighted adjustment back to the current price.

Note that, in the case of Arbitrum, there is the ability to force transactions through the delayed inbox. If other users are forcing transactions into the given pool, this could solve the problem, but if not it could also make the problem worse by allowing an attacker to force a transaction that abuses the outdated price while the sequencer is down, guaranteeing inclusion.

**Recommendation**

Use the Chainlink oracle for all L2s.

**Review**

0xSplits will prioritize the Chainlink oracle for all L2s. In the event that they need to deploy the Uniswap oracle, they have implemented the following changes:
- check the Chainlink Sequencer Feed to confirm the sequencer is up
- confirm that the sequencer has been back up for at least 1 hour
- for each queried pool, confirm that the sequencer has been up for at least the period the TWAP will be taken over

This ensures that, even in the event that the sequencer goes down and therefore propagates the old prices throughout the downtime, that downtime will be completely out of the TWAP by the time the oracle can be queried.

These changes can be seen in the following commits: [3a8a7a01](https://github.com/0xSplits/splits-oracle/pull/5/commits/3a8a7a010d454628532aa4db3887a9330423467c), [59124dbc](https://github.com/0xSplits/splits-oracle/pull/5/commits/59124dbc46222dfdee74a7115965cd0a61fc9874), [46baca33](https://github.com/0xSplits/splits-oracle/pull/5/commits/46baca33aae9dac8db734af3c704ef8b77fed3e1)

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ZachObront |
| Protocol | Splits Oracle |
| Report Date | N/A |
| Finders | Zach Obront |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-splits-oracle.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

