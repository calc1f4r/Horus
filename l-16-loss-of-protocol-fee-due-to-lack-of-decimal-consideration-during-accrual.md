---
# Core Classification
protocol: Covenant_2025-08-18
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62843
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Covenant-security-review_2025-08-18.md
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

[L-16] Loss of protocol fee due to lack of decimal consideration during accrual

### Overview

See description below for full details.

### Original Finding Content


_Resolved_

The protocol fee is calculated inside the `_calculateMarketState()` function whenever core protocol actions such as swap, redeem, or mint take place:
```solidity
            if (marketState.lexConfig.protocolFee > 0) {
                uint256 fee = DebtMath.calculateLinearAccrual(
                    baseTokenSupply,
                    marketState.lexConfig.protocolFee,
                    elapsedTime
                );
                if (fee > type(uint96).max) fee = type(uint96).max;
                if (fee > (baseTokenSupply >> 3)) fee = baseTokenSupply >> 3; // @dev set max update of 12.5% of baseTokenSupply
                unchecked {
                    marketState.accruedProtocolFee = uint96(fee);
                }
            }
```
However, upon further observation of `calculateLinearAccrual()`, it is found to have not considered fee accrual for tokens with lower decimals:
```solidity
    function calculateLinearAccrual(
        uint256 _value,
        uint256 _rate,
        uint256 _timeDelta
    ) internal pure returns (uint256 accrualValue_) {
        return Math.mulDiv(_value, _rate * _timeDelta, SECONDS_PER_YEAR * 1e4);
    }
```
A decent impact can be observed for tokens such as WBTC (8 decimal). A hypothetical scenario would be:

1. Total base token supply reaches 1 WBTC, which can be considered a decent market size (approx. $110k at current market rate).
2. Protocol averages a transaction every 60 seconds, and the rate is set to be 100 (1%):
```text
(1e8 * (1e2 * 60)) / (31536000 * 1e4) = 1.90258751903 ~ 1.   (rounding down in solidity)
```
3. For a smaller base Token supply, such as 0.5 WBTC, it would round down to zero:
```text
(5e7 * (1e2 * 60)) / (31536000 * 1e4) = 0.95129375951 ~ 0    (rounding down in solidity)
```

This example considers the fee to be set as 1%, however, it can be set to 10 (0.1%) as well, which would result in an even higher protocol fee loss.

Also, an attacker can grief the protocol by updating the market state by swapping dust amounts just before the fee accrual could be significant.

**Recommendations**

It is recommended to use a global high-precision index in RAY, which would grow linearly as we advance it periodically upon state update. This can be used for transferring fee shares proportional to the index delta.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Covenant_2025-08-18 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Covenant-security-review_2025-08-18.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

