---
# Core Classification
protocol: Curve Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40996
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/Curve%20Lending/README.md#1-an-inflated-fee-in-the-amm-leads-to-a-partial-amm-dos
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
  - MixBytes
---

## Vulnerability Title

An inflated fee in the AMM leads to a partial AMM DOS

### Overview


The bug report discusses a potential issue with the `admin_fees_x` variable in the AMM `withdraw()` function. Currently, the variable is not being divided by the `BORROWED_PRECISION` which can lead to a significant error in fee accrual, especially if the `borrowed_token` is WBTC with a decimal precision of 8. This could potentially allow a hacker to inflate the `admin_fees_x` variable and cause a partial denial of service attack on the AMM. The report recommends adding a division by `BORROWED_PRECISION` to prevent this issue.

### Original Finding Content

##### Description
The `admin_fees_x`  variable is not divided by `BORROWED_PRECISION` in AMM `withdraw()`:
```
## If withdrawal is the last one - transfer dust to admin fees
if new_shares == 0:
    if x > 0:
        self.admin_fees_x += x
    if y > 0:
        self.admin_fees_y += unsafe_div(y, COLLATERAL_PRECISION)
```
https://github.com/curvefi/curve-stablecoin/blob/c3f7040960627f023a2098232658c49e74400d03/contracts/AMM.vy#L794

If `borrowed_token` is WBTC (decimals=8), then the error in fee accrual will be on the order of 10 magnitudes. A hacker could perform an inflation attack on the nearest available tick to trigger this piece of code and inflate `admin_fees_x` to the total amount of the `borrowed_token` balance in the AMM, while losing 10 magnitudes less funds than the final inflation amount. If the hacker then calls `collect_fees()`, which is a public method, all borrowed tokens from the AMM will be sent to `FACTORY.fee_receiver()`.

This will lead to a partial DOS of the AMM, as users will lose the ability to withdraw borrowed tokens from ticks, as there simply won't be any funds in the AMM for this.

There are a few notes on this:
1. **This attack does not depend on `ADMIN_FEE`**; the code is always activated when there is dust in the tick. In order to execute the attack, the hacker needs to inflate the share price in the tick, causing the dust to have a large value.
2. AMM uses dead shares, but price inflation is still possible via the `exchange()` method or other means. It's just not profitable for the hacker.
3. Currently, `collect_fees()` reverts as `Vault` does not have a `fee_receiver()` method which is called by the `collect_fees()` method. Still, if the `collect_fees()` revert issue is addressed by introducing a `fee_receiver()` in the factory, then the fee inflation bug will arise.

##### Recommendation
We recommend adding the missing division by the `BORROWED_PRECISION`:
```
self.admin_fees_x += unsafe_div(x, BORROWED_PRECISION)
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Curve Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/Curve%20Lending/README.md#1-an-inflated-fee-in-the-amm-leads-to-a-partial-amm-dos
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

