---
# Core Classification
protocol: MCDEX Mai Protocol V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13721
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2020/05/mcdex-mai-protocol-v2/
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

protocol_categories:
  - dexes
  - cdp
  - yield
  - yield_aggregator
  - options_vault

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Martin Ortner
  - Alexander Wade
---

## Vulnerability Title

AMM - Liquidity pools can be initialized with zero collateral  Pending

### Overview


This bug report concerns the `createPool` function in a contract, which allows it to be initialized with amount equal to zero. This is an issue because a subsequent call to `initFunding` can only happen once, and the contract is now initialized with a zero size pool that does not allow any liquidity to be added. The specification for `createPool` is inaccurate, as it can only be called once due to a check in `initFunding`, but this call may leave the pool empty. Additionally, the contract's liquidity management functionality (`addLiquidity` and `removeLiquidity`) allows adding zero liquidity (`amount == 0`) and removing zero shares (`shareAmount == 0`).

The issue was addressed by checking that `amount > 0`. The assessment team proposed two recommendations to prevent this issue in the future: requiring a minimum amount `lotSize` to be provided when creating a Pool and adding liquidity via `addLiquidity`, and requiring a minimum amount of shares to be provided when removing liquidity via `removeLiquidity`.

### Original Finding Content

#### Resolution



This issue was addressed by checking that `amount > 0`. The assessment team would like to note that;


* The client chose to verify that `amount` is non-zero when calling `createPool` instead of requiring a minimum of a `lotSize`.
* The client did not address the issues about `removeLiquidity` and `addLiquidity` allowing to remove and add zero liquidity.




#### Description


`createPool` can be initialized with `amount == 0`. Because a subsequent call to `initFunding` can only happen once, the contract is now initialized with a zero size pool that does not allow any liquidity to be added.


Trying to recover by calling `createPool` again fails as the funding state is already `initialized`. The [specification](https://github.com/mcdexio/documents/blob/84ddfa77e2bb25db7366b01fc0133cd66122c675/en/perpetual-interfaces.md) also states the following about `createPool`:



> 
> Open asset pool by deposit to AMM. Only available when pool is empty.
> 
> 
> 


This is inaccurate, as `createPool` can only be called once due to a check in `initFunding`, but this call may leave the pool empty.


Furthermore, the contract’s liquidity management functionality (`addLiquidity` and `removeLiquidity`) allows adding zero liquidity (`amount == 0`) and removing zero shares (`shareAmount == 0`). As these actions do not change the liquidity of the pool, they should be rejected.


#### Recommendation


* Require a minimum amount `lotSize` to be provided when creating a Pool and adding liquidity via `addLiquidity`
* Require a minimum amount of shares to be provided when removing liquidity via `removeLiquidity`

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | MCDEX Mai Protocol V2 |
| Report Date | N/A |
| Finders | Martin Ortner, Alexander Wade |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2020/05/mcdex-mai-protocol-v2/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

