---
# Core Classification
protocol: Juicebox
chain: everychain
category: dos
vulnerability_type: dos

# Attack Vector Details
attack_type: dos
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5811
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-juicebox-contest
source_link: https://code4rena.com/reports/2022-10-juicebox
github_link: https://github.com/code-423n4/2022-10-juicebox-findings/issues/64

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - dos
  - broken_loop

protocol_categories:
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - brgltd
  - Lambda
---

## Vulnerability Title

[M-04] Iterations over all tiers in recordMintBestAvailableTier can render system unusable

### Overview


This bug report is about the JBTiered721DelegateStore.sol contract, which is part of the juice-nft-rewards project on GitHub. The vulnerability is that when there are many tiers, transactions with a high leftover amount within the _processPayment function will always revert due to the loop running out of gas. This is because the loop in the recordMintBestAvailableTier function is iterating over all tiers to find the one with the highest contribution floor that is lower than the amount. The implicit limit for the number of tiers is 2^16 - 1, so it is possible that this happens in practice.

The recommended mitigation step is to use a binary search for determining the best available tier. This would cause the gas usage to grow logarithmically instead of linearly with the number of tiers, meaning that it would only be 16 times higher for 65535 tiers as for 2 tiers. This would reduce the risk of transactions with a high leftover amount within the _processPayment function reverting due to the loop running out of gas.

### Original Finding Content


`JBTiered721DelegateStore.recordMintBestAvailableTier` potentially iterates over all tiers to find the one with the highest contribution floor that is lower than `_amount`. When there are many tiers, this loop can always run out of gas, which will cause some transactions (the ones that have a high `_leftoverAmount` within `_processPayment`) to always revert. The (implicit) limit for the number of tiers is 2^16 - 1, so it is possible that this happens in practice.

### Proof Of Concept

Let's say that 1,000 tiers are registered for a project. Small payments without a leftover amount or a small amount will be succesfully processed by `_processPayment`, because `_mintBestAvailableTier` is either not called or it is called with a small amount, meaning that `recordMintBestAvailableTier` will exit the loop early (when it is called with a small amount). However, if a payment with a large leftover amount (let's say greater than the highest contribution floor) is processed, it is necessary to iterate over all tiers, which will use too much gas and cause the processing to revert.

### Recommended Mitigation Steps

Use a binary search (which requires some architectural changes) for determining the best available tier. Then, the gas usage grows logarithmically (instead of linear with the current design) with the number of tiers, meaning that it would only be \~16 times higher for 65535 tiers as for 2 tiers.


**[drgorillamd (Juicebox DAO) commented on duplicate issue #226](https://github.com/code-423n4/2022-10-juicebox-findings/issues/226#issuecomment-1288627984):**
> Disagree with:

> > Over time maxTierIdOf for a nft address gets large due to several increments

> There is no several increments outside of adding new tiers by the project owner (this is similar to adding new token in an erc1155 - there is no such check in, for instance, OZ https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC1155/ERC1155.sol), this is a project owner choice, not faulty logic.


**[Picodes (judge) commented on duplicate issue #226](https://github.com/code-423n4/2022-10-juicebox-findings/issues/226#issuecomment-1307478020):**
 > User funds could be at stake as `redeemParams` would revert because of the for loop in `totalRedemptionWeight`. A limit value would be indeed a good safeguard.


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Juicebox |
| Report Date | N/A |
| Finders | brgltd, Lambda |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-juicebox
- **GitHub**: https://github.com/code-423n4/2022-10-juicebox-findings/issues/64
- **Contest**: https://code4rena.com/contests/2022-10-juicebox-contest

### Keywords for Search

`DOS, Broken Loop`

