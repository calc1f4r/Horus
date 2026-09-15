---
# Core Classification
protocol: RWf(x)_2025-08-20
chain: everychain
category: arithmetic
vulnerability_type: protocol_reserve

# Attack Vector Details
attack_type: protocol_reserve
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63648
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/RWf(x)-security-review_2025-08-20.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.60
financial_impact: medium

# Scoring
quality_score: 3
rarity_score: 2

# Context Tags
tags:
  - protocol_reserve
  - deposit/reward_tokens
  - minout/maxin_validation
  - pre/post_balance
  - precision_loss

protocol_categories:
  - payments

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-01] Minting of `fToken` and `xToken` allowed during stability mode

### Overview


The bug report discusses an issue with the `Market.mint()` function, which creates both fTokens and xTokens based on the current collateral ratio. The original implementation only allowed this function to be called once, but a recent change has removed this restriction. This means that the function can now be called multiple times, even during stability mode when the collateral ratio has fallen below a safe threshold. This makes it more difficult for the system to recover, as each new mint increases the amount of base tokens needed to restore the ratio. The report recommends restricting the function from being called during stability mode to prevent further problems. The severity of this issue is considered medium, as only trusted entities are able to use the function and they are not likely to intentionally harm the stability of the system.

### Original Finding Content


_Resolved_

## Severity

**Impact:** Medium  

**Likelihood:** Medium  

## Description

The `Market.mint()` function mints both fToken and xToken [based on the current collateral ratio](https://github.com/RegnumAurumAcquisitionCorp/fx-contracts/blob/main/contracts/f(x)/math/FxLowVolatilityMath.sol#L293-L307).  
In the original Aladdin implementation, this function could be called only once. However, RegnumFx [removed this restriction](https://github.com/RegnumAurumAcquisitionCorp/fx-contracts/compare/bbb461cba879349c24c02d87872e93ec0a1a1975...f6e865df2dd46d67a49391d94e54b26e6a8af43c#diff-2c8d19ba3d13b72d110c2a9536e5e9915118ad919b38848357200e91afb683faL252), allowing it to be called multiple times.

When the system enters stability mode, the collateral ratio has fallen below the defined safe threshold. This indicates that additional base tokens need to be deposited to restore the ratio.

Allowing `mint()` during stability mode worsens the problem: each new mint increases the number of fTokens in circulation, which in turn raises the amount of base tokens required to bring the system back to a healthy state. As a result, recovery becomes more difficult, and the system may remain undercollateralized for longer.

The severity chosen for this issue is medium, because only whitelisted managers can use the function, and they are trusted entities that are not interested in making stablecoin depeg.

## Recommendations

Restrict `mint()` from being called when the system is in stability mode to prevent further dilution of collateralization and to simplify recovery.




### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3/5 |
| Rarity Score | 2/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | RWf(x)_2025-08-20 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/RWf(x)-security-review_2025-08-20.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Protocol Reserve, Deposit/Reward tokens, MinOut/MaxIn Validation, Pre/Post Balance, Precision Loss`

