---
# Core Classification
protocol: Panoptic Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33823
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/panoptic-audit
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
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Initial Deposit to One Collateral Tracker Could Be Zero

### Overview


A bug has been found in the deployment process of a new Panoptic pool. The deployer must provide a small amount of liquidity to the underlying AMM pool, which is then divided and deposited into collateral trackers to prevent an inflation attack. However, due to a formula error, one of the deposits may be set to 0 if the current tick is close to the maximum or minimum tick. This allows an attacker to manipulate the tick and profit from the attack. The bug has been resolved by ensuring a minimum number of shares are minted during pool deployment.

### Original Finding Content

When deploying a new Panoptic pool, the deployer is required to provide a small amount of full-range liquidity to the underlying AMM pool. The returned amounts, `amount0` and `amount1`, are then divided by `100` and deposited into both collateral trackers in the name of the `PanopticFactory` to prevent the ERC-4626 inflation attack. It is possible that one of `amount0` or `amount1` is less than `100`. This happens when the current tick is very close to either `MAX_TICK` or `MIN_TICK` as seen in the `getAmount0Delta` or `getAmount1Delta` formulae. In that case, the initial deposit to one of the collateral trackers could be `0` due to truncation.


While it is generally not possible to obtain enough liquidity to move a pool's tick to `MAX_TICK` or `MIN_TICK`, it is possible for pools with very low liquidity. Depending on the AMM pool, the cost of tick manipulation may be worth the potential profit. This enables the attacker to be the first depositor to the collateral tracker and launch the inflation attack as follows:


* The attacker deposits 1 asset to the collateral tracker to get 1 share back.
* A subsequent LP deposits some amount to the collateral tracker.
* The attacker front-runs the transaction by transferring directly the same amount to the Panoptic pool. Thus, the LP from the previous step would get 0 shares in return due to rounding.
* The attacker can then redeem his single share to get the combined amount of the LP deposit as well as the prior direct transfer.


Since a new Panoptic pool cannot be deployed with the same underlying AMM pool, it would be difficult to stop this attack once the attacker's initial deposit takes place. Consider ensuring that a minimum number of shares are minted in each collateral tracker during pool deployment to be resilient against the inflation attack.


***Update:** Resolved*.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Panoptic Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/panoptic-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

