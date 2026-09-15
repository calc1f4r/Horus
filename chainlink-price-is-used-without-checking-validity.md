---
# Core Classification
protocol: Meta
chain: everychain
category: oracle
vulnerability_type: chainlink

# Attack Vector Details
attack_type: chainlink
affected_component: oracle

# Source Information
source: solodit
solodit_id: 19115
audit_firm: Hans
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hans/2023-07-13-Meta.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - chainlink
  - stale_price
  - oracle

protocol_categories:
  - liquid_staking
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Hans
---

## Vulnerability Title

Chainlink price is used without checking validity

### Overview


The bug report is about a vulnerability in the Meta protocol that affects user assets when the Chainlink oracle is in bad status. The current implementation lacks checks for the staleness of the price obtained from Chainlink, which can lead to issues if Chainlink starts a new round and struggles to establish consensus on the new value for the oracle. It is also important to check if the Arbitrum sequencer is active.

To address this issue, it is recommended to implement checks to ensure that the price returned by Chainlink is not stale. The following code snippet can be used to validate the price obtained from Chainlink:

```solidity
( roundId, rawPrice, , updateTime, answeredInRound ) = priceFeed.latestRoundData();
require(rawPrice > 0, "Chainlink price <= 0");
require(updateTime != 0, "Incomplete round");
require(answeredInRound >= roundId, "Stale price");
```

The Meta Team fixed the issue in the latest commit by adding the checks on the price value and also sequencer validation. Hans verified the changes.

The severity of this vulnerability is classified as MEDIUM because it affects user assets only when the Chainlink oracle is in bad status.

### Original Finding Content

**Severity:** Medium

**Context:** [`Helper.sol#L75-L78`](https://github.com/getmetafinance/meta/blob/00bbac1613fa69e4c180ff53515451df4df9f69e/contracts/musd/Helper.sol#L75-L78)

**Description:**
The Meta protocol relies on a Chainlink price oracle to calculate the excess income distributed to all mUSD holders.
However, the current implementation lacks checks for the staleness of the price obtained from Chainlink.

```solidity
function getPriceOfRewardToken() external view returns (uint256) {
(,int256 price,,,) = priceFeed.latestRoundData();//@audit chainlink price feed - stale price check is missing
return (uint256(price) * Constants.PINT) / PRICE_FEED_PRECISION;
}
```

This omission can lead to issues if Chainlink starts a new round and struggles to establish consensus on the new value for the oracle. Without proper checks, consumers of this contract may continue using outdated, stale, or incorrect data if oracles are unable to submit and start a new round. Possible reasons for this could include Chainlink nodes abandoning the oracle, chain congestion, or vulnerabilities/attacks on the Chainlink system.

Additionally, it is important to check if the Arbitrum sequencer is active.
Please refer to the issue at https://github.com/sherlock-audit/2022-11-sentiment-judging/issues/3 for more information.

**Impact**
This vulnerability is classified as MEDIUM because it affects user assets only when the Chainlink oracle is in bad status.

**Recommendation:**
To address this issue, it is recommended to implement checks to ensure that the price returned by Chainlink is not stale. The following code snippet can be used to validate the price obtained from Chainlink:

```solidity
( roundId, rawPrice, , updateTime, answeredInRound ) = priceFeed.latestRoundData();
require(rawPrice > 0, "Chainlink price <= 0");
require(updateTime != 0, "Incomplete round");
require(answeredInRound >= roundId, "Stale price");
```

**Meta Team:**

Fixed in the latest commit. Added the checks on the price value and also sequencer validation.

```diff

+    function isSequencerActive() internal view returns (bool) {
+        (, int256 answer, uint256 startedAt,,) = sequencer.latestRoundData();
+        if (block.timestamp - startedAt <= GRACE_PERIOD_TIME || answer == 1)
+            return false;
+        return true;
+    }

function getPriceOfRewardToken() external view returns (uint256) {
(uint80 roundId,int256 price,,uint256 updateTime, uint80 answeredInRound) = priceFeed.latestRoundData();
+       require(isSequencerActive(), "HLP: Sequencer is down");
+       require(price > 0, "HLP: Invalid chainlink price");
+       require(updateTime > 0, "HLP: Incomplete round");
+       require(answeredInRound >= roundId, "HLP: Stale price");
return (uint256(price) * Constants.PINT) / PRICE_FEED_PRECISION;
}

```

**Hans:**
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Hans |
| Protocol | Meta |
| Report Date | N/A |
| Finders | Hans |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hans/2023-07-13-Meta.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Chainlink, Stale Price, Oracle`

