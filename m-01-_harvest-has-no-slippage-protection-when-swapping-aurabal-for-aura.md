---
# Core Classification
protocol: BadgerDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2684
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-06-badger-vested-aura-contest
source_link: https://code4rena.com/reports/2022-06-badger
github_link: https://github.com/code-423n4/2022-06-badger-findings/issues/104

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
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 16
finders:
  - IllIllI
  - 0x52
  - cccz
  - scaraven
  - Picodes
---

## Vulnerability Title

[M-01] `_harvest` has no slippage protection when swapping `auraBAL` for `AURA`

### Overview


This bug report concerns the vulnerability of a single swap of the '_harvest' function in the MyStrategy.sol contract. Without slippage or deadline protection, it is vulnerable to sandwich attacks and other MEV exploits, potentially leading to significant losses of yield. A proof of concept is provided, wherein an authorized actor calls 'harvest' and two swaps are generated, one of AURA to BAL/ETH BPT and another of WETH to BAL. While the transaction is in the mempool, it is exploited as detailed in a linked article. The easiest mitigation would be to pass a minimum amount of AURA that the swap is supposed to get in 'harvest'. Alternatively, the use of an aggregator such as Cowswap could be used.

### Original Finding Content

_Submitted by Picodes, also found by 0x1f8b, 0x52, berndartmueller, cccz, Chom, defsec, georgypetrov, GimelSec, hyh, IllIllI, kenzo, minhquanym, oyc_109, scaraven, and unforgiven_

<https://github.com/Badger-Finance/vested-aura/blob/d504684e4f9b56660a9e6c6dfb839dcebac3c174/contracts/MyStrategy.sol#L249>

<https://github.com/Badger-Finance/vested-aura/blob/d504684e4f9b56660a9e6c6dfb839dcebac3c174/contracts/MyStrategy.sol#L275>

### Impact

Single swaps of `_harvest` contains no slippage or deadline, which makes it vulnerable to sandwich attacks, MEV exploits and may lead to significant loss of yield.

### Proof of Concept

When using `BALANCER_VAULT.swap` [here](https://github.com/Badger-Finance/vested-aura/blob/d504684e4f9b56660a9e6c6dfb839dcebac3c174/contracts/MyStrategy.sol#L249) and [here](https://github.com/Badger-Finance/vested-aura/blob/d504684e4f9b56660a9e6c6dfb839dcebac3c174/contracts/MyStrategy.sol#L275), there is no slippage protection. Therefore a call to `_harvest` generating swaps could be exploited for sandwich attacks or other MEV exploits such as [JIT](https://twitter.com/bertcmiller/status/1459175379265073155).

The scenario would be:
A authorized actor calls `harvest`, leading to a swap of say x `auraBAL` to `BAL/ETH BPT` and then y `WETH` to `BAL`.

Then while the transaction is in the mempool, it is exploited for example like in <https://medium.com/coinmonks/defi-sandwich-attack-explain-776f6f43b2fd>

### Recommended Mitigation Steps

The easiest mitigation would be to pass a minimum amount of `AURA` that the swap is supposed to get in `harvest`. It should not add security issues as callers of `harvest` are trusted.

Another solution would be to do like [here](https://github.com/GalloDaSballo/fair-selling/blob/main/contracts/CowSwapSeller.sol) to use Cowswap for example, or any other aggregator.

**[Alex the Entreprenerd (BadgerDAO) commented](https://github.com/code-423n4/2022-06-badger-findings/issues/104#issuecomment-1162497318):**
 > I love how the warden linked my code to integrate cowswap XD

 **[jack-the-pug (judge) validated](https://github.com/code-423n4/2022-06-badger-findings/issues/104)**

**[Alex the Entreprenerd (BadgerDAO) confirmed and commented](https://github.com/code-423n4/2022-06-badger-findings/issues/104#issuecomment-1183746029):**
 > Confirmed and mitigated in 2 ways:
> - We do use Private Transactions to Harvest (reduce change of front-run can still be sandwiched).
> - We Refactored to have a slippage tollerance



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | BadgerDAO |
| Report Date | N/A |
| Finders | IllIllI, 0x52, cccz, scaraven, Picodes, minhquanym, unforgiven_, Chom, berndartmueller, georgypetrov, 0x1f8b, oyc109, hyh, GimelSec, kenzo, defsec |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-badger
- **GitHub**: https://github.com/code-423n4/2022-06-badger-findings/issues/104
- **Contest**: https://code4rena.com/contests/2022-06-badger-vested-aura-contest

### Keywords for Search

`vulnerability`

