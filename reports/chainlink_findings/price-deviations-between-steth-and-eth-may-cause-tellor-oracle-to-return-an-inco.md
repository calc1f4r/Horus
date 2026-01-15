---
# Core Classification
protocol: Tempus Raft
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17574
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-04-tempus-raft-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-04-tempus-raft-securityreview.pdf
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
finders_count: 2
finders:
  - Justin Jacob
  - Michael Colburn
---

## Vulnerability Title

Price deviations between stETH and ETH may cause Tellor oracle to return an incorrect price

### Overview

See description below for full details.

### Original Finding Content

## Diﬃculty: Low

## Type: Configuration

## Target: TellorPriceOracle.sol

### Description
The Raft finance contracts rely on oracles to compute the price of the collateral tokens used throughout the codebase. If the Chainlink oracle is down, the Tellor oracle is used as a backup. However, the Tellor oracle does not use the stETH/USD price feed. Instead, it uses the ETH/USD price feed to determine the price of stETH. This could be problematic if stETH depegs, which can occur during black swan events.

```solidity
function _getCurrentTellorResponse() internal view returns (TellorResponse memory tellorResponse) {
    uint256 count;
    uint256 time;
    uint256 value;
    try tellor.getNewValueCountbyRequestId(ETHUSD_TELLOR_REQ_ID) returns (uint256 count_) {
        count = count_;
    } catch {
        return (tellorResponse);
    }
}
```

_Figure 6.1: The Tellor oracle fetching the price of ETH to determine the price of stETH_

### Exploit Scenario
Alice has a position in the system. A significant black swan event causes the depeg of staked Ether. As a result, the Tellor oracle returns an incorrect price, which prevents Alice's position from being liquidated despite being eligible for liquidation.

### Recommendations
- **Short term:** Carefully monitor the Tellor oracle, especially during any sort of market volatility.
- **Long term:** Investigate the robustness of the oracles and document possible circumstances that could cause them to return incorrect prices.

---

## Trail of Bits
## Tempus Raft Security Assessment
**PUBLIC**

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Tempus Raft |
| Report Date | N/A |
| Finders | Justin Jacob, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2023-04-tempus-raft-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2023-04-tempus-raft-securityreview.pdf

### Keywords for Search

`vulnerability`

