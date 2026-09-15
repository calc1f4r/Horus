---
# Core Classification
protocol: Increment Finance: Increment Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17367
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-09-incrementprotocol-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-09-incrementprotocol-securityreview.pdf
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
finders_count: 3
finders:
  - Vara Prasad Bandaru
  - Anish Naik
  - Justin Jacob
---

## Vulnerability Title

Excessive dust collection may lead to premature closures of long positions

### Overview


This bug report is about a potential issue with the Perpetual contract in the Increment Protocol. It is classified as a High difficulty and Undefined Behavior bug. The issue is that the upper bound on the amount of funds considered dust by the protocol may lead to the premature closure of long positions. The protocol collects dust to encourage complete closures instead of closures that leave a position with a small balance of vBase. 

The _reducePositionOnMarket function in Perpetual.sol is where dust collection occurs. If the netPositionSize, which represents a user’s position after its reduction, is between 0 and 1e17 (1/10 of an 18-decimal token), the system will treat the position as closed and donate the dust to the insurance protocol. This will occur regardless of whether the user intended to reduce, rather than fully close, the position.

The exploit scenario is that Alice holds a long position in the vBTC / vUSD market and decides to close most of her position. After the swap, netPositionSize is slightly less than 1e17. Since a leftover balance of that amount is considered dust, her ~1e17 vBTC tokens are sent to the Insurance contract, and her position is fully closed.

The recommendation is to have the protocol calculate the notional value of netPositionSize by multiplying it by the return value of the indexPrice function. Then have it compare that notional value to the dust thresholds. Note that the dust thresholds must also be expressed in the notional token and that the comparison should not lead to a significant decrease in a user’s position. Long term, document this system edge case to inform users that a fraction of their long positions may be donated to the Insurance contract after being reduced.

### Original Finding Content

## Vulnerability Assessment

### Difficulty: High

### Type: Undefined Behavior

### Target: contracts/Perpetual.sol

## Description

The upper bound on the amount of funds considered dust by the protocol may lead to the premature closure of long positions. The protocol collects dust to encourage complete closures instead of closures that leave a position with a small balance of vBase. One place that dust collection occurs is the Perpetual contract’s `_reducePositionOnMarket` function (Figure 7.1).

```solidity
function _reducePositionOnMarket (
    LibPerpetual.TraderPosition memory user,
    bool isLong,
    uint256 proposedAmount,
    uint256 minAmount
) internal returns (
    int256 baseProceeds,
    int256 quoteProceeds,
    int256 addedOpenNotional,
    int256 pnl
) {
    int256 positionSize = int256(user.positionSize);
    uint256 bought;
    uint256 feePer;
    
    if (isLong) {
        quoteProceeds = -(proposedAmount.toInt256());
        (bought, feePer) = _quoteForBase(proposedAmount, minAmount);
        baseProceeds = bought.toInt256();
    } else {
        (bought, feePer) = _baseForQuote(proposedAmount, minAmount);
        quoteProceeds = bought.toInt256();
        baseProceeds = -(proposedAmount.toInt256());
    }

    int256 netPositionSize = baseProceeds + positionSize;
    if (netPositionSize > 0 && netPositionSize <= 1e17) {
        _donate(netPositionSize.toUint256());
        baseProceeds -= netPositionSize;
    }
    [...]
}
```

Figure 7.1: The `_reducePositionOnMarket` function in `Perpetual.sol#L876-921`

If `netPositionSize`, which represents a user’s position after its reduction, is between 0 and 1e17 (1/10 of an 18-decimal token), the system will treat the position as closed and donate the dust to the insurance protocol. This will occur regardless of whether the user intended to reduce, rather than fully close, the position. (Note that `netPositionSize` is positive if the overall position is long. The dust collection mechanism used for short positions is discussed in TOB-INC-11.)

However, if `netPositionSize` is tracking a high-value token, the donation to Insurance will no longer be insignificant; 1/10 of 1 vBTC, for instance, would be worth ~USD 2,000 (at the time of writing). Thus, the donation of a user’s vBTC dust (and the resultant closure of the vBTC position) could prevent the user from profiting off of a ~USD 2,000 position.

## Exploit Scenario

Alice, who holds a long position in the vBTC / vUSD market, decides to close most of her position. After the swap, `netPositionSize` is slightly less than 1e17. Since a leftover balance of that amount is considered dust (unbeknownst to Alice), her ~1e17 vBTC tokens are sent to the Insurance contract, and her position is fully closed.

## Recommendations

**Short term:** Have the protocol calculate the notional value of `netPositionSize` by multiplying it by the return value of the `indexPrice` function. Then have it compare that notional value to the dust thresholds. Note that the dust thresholds must also be expressed in the notional token and that the comparison should not lead to a significant decrease in a user’s position.

**Long term:** Document this system edge case to inform users that a fraction of their long positions may be donated to the Insurance contract after being reduced.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Increment Finance: Increment Protocol |
| Report Date | N/A |
| Finders | Vara Prasad Bandaru, Anish Naik, Justin Jacob |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2022-09-incrementprotocol-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2022-09-incrementprotocol-securityreview.pdf

### Keywords for Search

`vulnerability`

