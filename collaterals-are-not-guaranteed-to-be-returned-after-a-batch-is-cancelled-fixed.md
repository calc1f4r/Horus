---
# Core Classification
protocol: AragonBlack Fundraising
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13920
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2019/11/aragonblack-fundraising/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Sergii Kravchenko
  - Martin Ortner
---

## Vulnerability Title

Collaterals are not guaranteed to be returned after a batch is cancelled ✓ Fixed

### Overview


This bug report is related to the AragonBlack/fundraising#162 project. When traders open buy orders, they transfer collateral tokens to a market maker contract. If the current batch is cancelled, these collateral tokens may not be returned to the traders. For example, if the `collateralsToBeClaimed` value is zero on a batch initialization and only buy orders are submitted, the value will remain zero. Additionally, if the `tapped` amount is bigger than `_maximumWithdrawal()` on batch initialisation, the beneficiary may be able to withdraw part of the tokens. To mitigate this issue, the `floor` value in the `Tap` contract should be taken into account. The recommendation is to ensure that `tapped` is not bigger than `_maximumWithdrawal()`.

### Original Finding Content

#### Resolution



Fixed with [AragonBlack/fundraising#162](https://github.com/AragonBlack/fundraising/pull/162)


#### Description


When traders open buy orders, they also transfer collateral tokens to the market maker contract. If the current batch is going to be cancelled, there is a chance that these collateral tokens will not be returned to the traders.


#### Examples


If a current `collateralsToBeClaimed` value is zero on a batch initialization and in this new batch only buy orders are submitted, `collateralsToBeClaimed` value will still stay zero.


At the same time if in `Tap` contract `tapped` amount was bigger than `_maximumWithdrawal()` on batch initialisation, `_maximumWithdrawal()` will most likely increase when the traders transfer new collateral tokens with the buy orders. And a beneficiary will be able to withdraw part of these tokens. Because of that, there might be not enough tokens to withdraw by the traders if the batch is cancelled.


It’s partially mitigated by having `floor` value in `Tap` contract, but if there are more collateral tokens in the batch than `floor`, the issue is still valid.


#### Recommendation


Ensure that `tapped` is not bigger than `_maximumWithdrawal()`

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | AragonBlack Fundraising |
| Report Date | N/A |
| Finders | Sergii Kravchenko, Martin Ortner |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2019/11/aragonblack-fundraising/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

