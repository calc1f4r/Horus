---
# Core Classification
protocol: Visor
chain: everychain
category: uncategorized
vulnerability_type: erc721

# Attack Vector Details
attack_type: erc721
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 191
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-05-visor-contest
source_link: https://code4rena.com/reports/2021-05-visorfinance
github_link: https://github.com/code-423n4/2021-05-visorfinance-findings/issues/48

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - erc721
  - approve

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - cmichel
  - gpersoon
  - pauliax
---

## Vulnerability Title

[H-03] Approval for NFT transfers is not removed after transfer

### Overview


This bug report is about a vulnerability in the `Visor.transferERC721` function. This vulnerability could allow an approved delegatee to steal a Non-Fungible Token (NFT) from the contract. The delegatee can move the NFT out of the contract once, and then someone else could buy it from a market and deposit it back to the same vault. The delegatee can then steal the NFT again and move it out of the contract a second time. 

To mitigate this vulnerability, it is recommended to reset the approval on transfer.

### Original Finding Content

_Submitted by cmichel, also found by gpersoon, and pauliax_

The `Visor.transferERC721` does not reset the approval for the NFT.

An approved delegatee can move the NFT out of the contract once.
It could be moved to a market and bought by someone else who then deposits it again to the same vault.
The first delegatee can steal the NFT and move it out of the contract a second time.

Recommend resetting the approval on transfer.

**[xyz-ctrl (Visor) confirmed](https://github.com/code-423n4/2021-05-visorfinance-findings/issues/48#issuecomment-856953219):**
> We will be mitigating this issue for our next release and before these experimental features are introduced in platform.
> PR pending

**[ztcrypto (Visor) commented](https://github.com/code-423n4/2021-05-visorfinance-findings/issues/48#issuecomment-889192312):**
> duplicate of above ones and fixed



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Visor |
| Report Date | N/A |
| Finders | cmichel, gpersoon, pauliax |

### Source Links

- **Source**: https://code4rena.com/reports/2021-05-visorfinance
- **GitHub**: https://github.com/code-423n4/2021-05-visorfinance-findings/issues/48
- **Contest**: https://code4rena.com/contests/2021-05-visor-contest

### Keywords for Search

`ERC721, Approve`

