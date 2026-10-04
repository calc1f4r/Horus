---
# Core Classification
protocol: OpalProtocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54311
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/0c9f46ff-e5b4-412c-b928-ecb135f44007
source_link: https://cdn.cantina.xyz/reports/cantina_competition_opal_feb2024.pdf
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
finders_count: 2
finders:
  - giraffe0x
  - 0xTheBlackPanther
---

## Vulnerability Title

No way to reduce or set gauge weight to zero due to underﬂow 

### Overview


The GaugeController contract has a bug that affects its ability to reduce or set a gauge's weight to zero. This is due to multiple underflow errors in the `_changeGaugeWeight` function. This means that the admin cannot change the weight of a gauge or make it obsolete. To fix this, the code needs to be changed in line 448 by removing brackets and the totalWeight calculation also needs to be re-evaluated.

### Original Finding Content

## GaugeController Vulnerability

## Context
GaugeController.sol#L448

## Description
Due to multiple underflow errors in `_changeGaugeWeight`, the admin does not have the ability to reduce or set a gauge's weight to zero.

### Code Snippet
```solidity
// GaugeController.sol
function _changeGaugeWeight(address gauge, uint256 weight) internal {
    int128 gaugeType = gaugeTypes[gauge] - 1;
    uint256 oldGaugeWeight = _getWeight(gauge);
    uint256 typeWeight = _getTypeWeight(gaugeType);
    uint256 oldSum = _getSum(gaugeType);
    uint256 totalWeight = _getTotal();
    uint256 nextTimestamp = ((block.timestamp + WEEK) / WEEK) * WEEK;
    gaugeVotes[gauge][nextTimestamp] = weight;
    lastGaugeUpdate[gauge] = nextTimestamp;
    //@audit if weight is less than oldGaugeWeight, this will underflow
    uint256 newSum = oldSum + (weight - oldGaugeWeight);
    //@audit this will also underflow when new weight = 0
    totalWeight += (oldSum * weight) - (oldSum * typeWeight);
}
```

If `weight` is less than `oldGaugeWeight`, the calculation for `newSum` will underflow and revert. This is also true for the calculation of `totalWeight`.

## Impact
There are no ways for an admin to reduce the weight of a gauge or deprecate it by setting weight to zero.

## Recommendation
Change the line to `uint256 newSum = oldSum + weight - oldGaugeWeight;` by removing brackets. Need to re-evaluate totalWeight calculations too.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | OpalProtocol |
| Report Date | N/A |
| Finders | giraffe0x, 0xTheBlackPanther |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_opal_feb2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/0c9f46ff-e5b4-412c-b928-ecb135f44007

### Keywords for Search

`vulnerability`

