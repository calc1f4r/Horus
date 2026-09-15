---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24833
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-08-frax
source_link: https://code4rena.com/reports/2022-08-frax
github_link: https://github.com/code-423n4/2022-08-frax-findings/issues/238

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
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-04] Wrong percent for `FraxlendPairCore.dirtyLiquidationFee`.

### Overview


This bug report is about the wrong fee calculation in the code of FraxlendPairCore.sol. According to the sponsor, the `dirtyLiquidationFee` should be 90% of the `cleanLiquidationFee`, however the code uses `9% (9000 / 1e5 = 0.09)` which results in an incorrect fee calculation. To fix this issue, the code should be changed from `9000` to `90000`. This was confirmed by DrakeEvans (Frax) and gititGoro (judge) commented that this report is complete, short and to the point and the sponsor's preference was factored in.

### Original Finding Content


After confirming with the sponsor, `dirtyLiquidationFee` is 90% of `cleanLiquidationFee` like the [comment](https://github.com/code-423n4/2022-08-frax/blob/c4189a3a98b38c8c962c5ea72f1a322fbc2ae45f/src/contracts/FraxlendPairCore.sol#L194).

But it uses `9% (9000 / 1e5 = 0.09)` and the fee calculation will be wrong [here](https://github.com/code-423n4/2022-08-frax/blob/c4189a3a98b38c8c962c5ea72f1a322fbc2ae45f/src/contracts/FraxlendPairCore.sol#L988-L990).

### Recommended Mitigation Steps

We should change `9000` to `90000`.

    dirtyLiquidationFee = (_liquidationFee * 90000) / LIQ_PRECISION; // 90% of clean fee


**[DrakeEvans (Frax) confirmed and commented](https://github.com/code-423n4/2022-08-frax-findings/issues/238#issuecomment-1238157712):**
 > Confirmed.

**[gititGoro (judge) commented](https://github.com/code-423n4/2022-08-frax-findings/issues/238#issuecomment-1259011750):**
 > This issue has a great many duplicates. Reason for setting this report as the original:
> 1. It's complete in that it charts the problem and gives a code based mitigation
> 2. It's short and to the point.
> 3. The sponsor's preference was factored in.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-08-frax
- **GitHub**: https://github.com/code-423n4/2022-08-frax-findings/issues/238
- **Contest**: https://code4rena.com/reports/2022-08-frax

### Keywords for Search

`vulnerability`

