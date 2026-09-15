---
# Core Classification
protocol: Swivel
chain: everychain
category: uncategorized
vulnerability_type: safetransfer

# Attack Vector Details
attack_type: safetransfer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 867
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-09-swivel-contest
source_link: https://code4rena.com/reports/2021-09-swivel
github_link: https://github.com/code-423n4/2021-09-swivel-findings/issues/155

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 4

# Context Tags
tags:
  - safetransfer

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 11
finders:
  - nikitastupin
  - JMukesh
  - 0xsanson
  - cmichel
  - leastwood
---

## Vulnerability Title

[H-01] Unsafe handling of underlying tokens

### Overview


This bug report is about an issue with ERC20 tokens. It is possible for a transferFrom function to not revert upon failure, but instead return false. This means that a msg.sender can exploit this vulnerability by initiating a trade without sending any underlying. This can be seen by running the command "grep 'transfer' Swivel.sol" in an editor. 

The recommended mitigation step is to use the OpenZeppelin library with safe versions of transfer functions. This library can be found at the following URL: https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol. This library ensures that any transfer function will revert upon failure instead of returning false.

### Original Finding Content

_Submitted by 0xsanson, also found by 0xRajeev, cmichel, defsec, GalloDaSballo, JMukesh, leastwood, loop, nikitastupin, pants, and pauliax_.

#### Impact

Not every ERC20 token follows OpenZeppelin's recommendation. It's possible (inside ERC20 standard) that a `transferFrom` doesn't revert upon failure but returns `false`.

The code doesn't check these return values. For example `uToken.transferFrom(msg.sender, o.maker, a);` in `initiateVaultFillingZcTokenInitiate` can be exploited by the msg.sender to initiate a trade without sending any underlying.

#### Proof of Concept

`grep 'transfer' Swivel.sol`

#### Tools Used

editor

#### Recommended Mitigation Steps

Consider using [OpenZeppelin's library](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol) with *safe* versions of transfer functions.




### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Swivel |
| Report Date | N/A |
| Finders | nikitastupin, JMukesh, 0xsanson, cmichel, leastwood, GalloDaSballo, 0xRajeev, pauliax., loop, pants, defsec |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-swivel
- **GitHub**: https://github.com/code-423n4/2021-09-swivel-findings/issues/155
- **Contest**: https://code4rena.com/contests/2021-09-swivel-contest

### Keywords for Search

`SafeTransfer`

