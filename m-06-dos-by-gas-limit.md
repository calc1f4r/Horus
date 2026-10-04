---
# Core Classification
protocol: Biconomy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1634
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-03-biconomy-hyphen-20-contest
source_link: https://code4rena.com/reports/2022-03-biconomy
github_link: https://github.com/code-423n4/2022-03-biconomy-findings/issues/24

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
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - danb
  - benk10  pedroais
---

## Vulnerability Title

[M-06] DoS by gas limit

### Overview


A bug has been reported in the "deposit" function of the LiquidityFarming.sol contract, which is part of the code-423n4/2022-03-biconomy repository on Github. This bug could potentially allow an attacker to deposit too many non-fungible tokens (NFTs) to another user's "nftIdsStaked" list. When the user tries to withdraw an NFT at the end of the list, they will iterate on the list and the transaction will fail due to a gas limit being exceeded. This could result in the user losing access to their NFTs. Developers should check the code to ensure that an attacker cannot push to another user's "nftIdsStaked" list.

### Original Finding Content

_Submitted by danb, also found by benk10 and pedroais_

[LiquidityFarming.sol#L220](https://github.com/code-423n4/2022-03-biconomy/blob/main/contracts/hyphen/LiquidityFarming.sol#L220)<br>
[LiquidityFarming.sol#L233](https://github.com/code-423n4/2022-03-biconomy/blob/main/contracts/hyphen/LiquidityFarming.sol#L233)<br>

In `deposit` function it is possible to push to `nftIdsStaked` of anyone, an attacker can deposit too many nfts to another user, and when the user will try to withdraw an nft at the end of the list, they will iterate on the list and revert because of gas limit.

**[ankurdubey521 (Biconomy) confirmed and commented](https://github.com/code-423n4/2022-03-biconomy-findings/issues/24):**
 > [HP-25: C4 Audit Fixes, Dynamic Fee Changes bcnmy/hyphen-contract#42](https://github.com/bcnmy/hyphen-contract/pull/42)

**[pauliax (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-03-biconomy-findings/issues/24#issuecomment-1109684991):**
 > A valid concern, but I think it should be of medium severity because the victim can still withdraw NFTs one by one until reaching the necessary index because it breaks inside the loop: [LiquidityFarming.sol#L234-L235](https://github.com/code-423n4/2022-03-biconomy/blob/main/contracts/hyphen/LiquidityFarming.sol#L234-L235).



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Biconomy |
| Report Date | N/A |
| Finders | danb, benk10  pedroais |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-biconomy
- **GitHub**: https://github.com/code-423n4/2022-03-biconomy-findings/issues/24
- **Contest**: https://code4rena.com/contests/2022-03-biconomy-hyphen-20-contest

### Keywords for Search

`vulnerability`

