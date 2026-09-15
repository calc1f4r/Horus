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
solodit_id: 27687
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/StableSwapNG/README.md#1-rebasing-rewards-will-get-stuck-on-the-contract
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

Rebasing rewards will get stuck on the contract

### Overview


This bug report concerns the stored_balances feature of the CurveStableSwapNG and CurveStableSwapMetaNG contracts. This issue causes tokens with accrued rewards to not be able to be removed from the contracts, leading to users' tokens becoming stuck and unable to be retrieved. This is classified as a critical issue, as the contracts do not allow upgrades.

The recommended solution is to update the stored_balances feature so that it will account for possible token balance rebases. This should ensure that users are able to retrieve their tokens from the contracts.

### Original Finding Content

##### Description
The main problem here is that `stored_balances` does not account for rewards for rebaseable tokens (e.g. stETH):
https://github.com/curvefi/stableswap-ng/blob/8c78731ed43c22e6bcdcb5d39b0a7d02f8cb0386/contracts/main/CurveStableSwapNG.vy#L380
https://github.com/curvefi/stableswap-ng/blob/8c78731ed43c22e6bcdcb5d39b0a7d02f8cb0386/contracts/main/CurveStableSwapMetaNG.vy#L440
This leads to the situation where deposited tokens with accrued rewards cannot be removed from the contract because of the revert on the lines pointed above. The test scenario was sent to the client during the audit. This finding is classified as critical because pools' contracts do not allow upgrades, which means that users' tokens will get stuck on the contract and there will be no possibility to retrieve them.

##### Recommendation
We recommend updating work with the `stored_balances` so that it will account for possible token balance rebases.


***

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/StableSwapNG/README.md#1-rebasing-rewards-will-get-stuck-on-the-contract
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

