---
# Core Classification
protocol: GEB Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11199
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/geb-protocol-audit/
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
  - liquid_staking
  - cdp
  - yield
  - launchpad
  - rwa_lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M01] Starting debt auctions can be prevented

### Overview


A bug was discovered in the AccountingEngine contract within the Github repository reflexer-labs/geb. The bug is related to the function auctionDebt, which contains a check that the AccountingEngine contract instance has no system coin balance. However, the function transferInternalCoins within the SAFEEngine contract allows transfers of internal tokens to any contract. As a result, any user can transfer their internal coins to the AccountingEngine contract, causing the check within auctionDebt to fail.

This means that any user can front-run calls to auctionDebt, preventing any new debt auctions from starting. However, the front-runner may fail in their attempt and a new debt auction can begin. To fix this issue, the visibility of the settleDebt function should be changed to public and a call to settleDebt should be made before the balance check is enforced. The bug has been fixed in pull request #75.

### Original Finding Content

Within the [`AccountingEngine`](https://github.com/reflexer-labs/geb/blob/261407b6b332c2063e4256aa5f9b223d52dad7e1/src/AccountingEngine.sol) contract, the function [`auctionDebt`](https://github.com/reflexer-labs/geb/blob/261407b6b332c2063e4256aa5f9b223d52dad7e1/src/AccountingEngine.sol#L259) contains a check that the `AccountingEngine` contract instance [has no system coin balance](https://github.com/reflexer-labs/geb/blob/261407b6b332c2063e4256aa5f9b223d52dad7e1/src/AccountingEngine.sol#L261). However, the [`transferInternalCoins` function](https://github.com/reflexer-labs/geb/blob/261407b6b332c2063e4256aa5f9b223d52dad7e1/src/SAFEEngine.sol#L313) within the [`SAFEEngine`](https://github.com/reflexer-labs/geb/blob/261407b6b332c2063e4256aa5f9b223d52dad7e1/src/SAFEEngine.sol) contract allows transfers of internal tokens to any contract, provided [`canModifySafe(src, msg.sender)`](https://github.com/reflexer-labs/geb/blob/261407b6b332c2063e4256aa5f9b223d52dad7e1/src/SAFEEngine.sol#L314) returns true. Thus, any user can transfer their internal coins to the `AccountingEngine` contract. For any nonzero amount of coins, this will cause [the check within `auctionDebt`](https://github.com/reflexer-labs/geb/blob/261407b6b332c2063e4256aa5f9b223d52dad7e1/src/AccountingEngine.sol#L261) to fail.


The result of this is that any user can front-run calls to `auctionDebt` to prevent them from executing, effectively preventing any new debt auctions from starting. However, it should be noted that eventually, the front-runner may fail in their front-running attempt, and at that point a new debt auction can begin.


Consider replacing this check with a call to [`settleDebt(safeEngine.coinBalance(address(this))`](https://github.com/reflexer-labs/geb/blob/261407b6b332c2063e4256aa5f9b223d52dad7e1/src/AccountingEngine.sol#L235) before [the balance check](https://github.com/reflexer-labs/geb/blob/261407b6b332c2063e4256aa5f9b223d52dad7e1/src/AccountingEngine.sol#L261) is enforced. This may require changing the visibility of `settleDebt` to `public`.


***Update:** Fixed in [pull request #75.](https://github.com/reflexer-labs/geb/pull/75/files)*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | GEB Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/geb-protocol-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

