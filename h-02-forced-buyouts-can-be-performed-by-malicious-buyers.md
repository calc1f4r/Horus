---
# Core Classification
protocol: Fractional
chain: everychain
category: uncategorized
vulnerability_type: erc1155

# Attack Vector Details
attack_type: erc1155
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2983
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-fractional-v2-contest
source_link: https://code4rena.com/reports/2022-07-fractional
github_link: https://github.com/code-423n4/2022-07-fractional-findings/issues/212

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
  - erc1155

protocol_categories:
  - dexes
  - bridge
  - yield
  - launchpad
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cccz
---

## Vulnerability Title

[H-02] Forced buyouts can be performed by malicious buyers

### Overview


A bug has been identified in the end function of the Buyout contract. If a buyout fails, ERC1155 tokens are sent to the proposer, but if the proposer is a malicious contract that cannot receive ERC1155 tokens, the end function fails and prevents any new buyout from being started. This bug has been highlighted in the code at the link given in the report. No tools were used to identify the bug.

The impact of this bug is that it prevents any new buyout from being started. To mitigate this bug, it is recommended to save the status of the proposer after a failed buyout and implement functions to allow the proposer to withdraw the ERC1155 tokens and ETH.

### Original Finding Content

_Submitted by cccz_

In the end function of the Buyout contract, when the buyout fails, ERC1155 tokens are sent to the proposer. A malicious proposer can start a buyout using a contract that cannot receive ERC1155 tokens, and if the buyout fails, the end function fails because it cannot send ERC1155 tokens to the proposer. This prevents a new buyout from being started.

### Proof of Concept

<https://github.com/code-423n4/2022-07-fractional/blob/8f2697ae727c60c93ea47276f8fa128369abfe51/src/modules/Buyout.sol#L224-L238>

### Recommended Mitigation Steps

Consider saving the status of the proposer after a failed buyout and implementing functions to allow the proposer to withdraw the ERC1155 tokens and eth.

**[Ferret-san (Fractional) confirmed](https://github.com/code-423n4/2022-07-fractional-findings/issues/212)** 

**[HardlyDifficult (judge) commented](https://github.com/code-423n4/2022-07-fractional-findings/issues/212#issuecomment-1217143098):**
 > The 1155 receiver can prevent a failed buyout from ending, which prevents a new one from starting. Agree with severity.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Fractional |
| Report Date | N/A |
| Finders | cccz |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-fractional
- **GitHub**: https://github.com/code-423n4/2022-07-fractional-findings/issues/212
- **Contest**: https://code4rena.com/contests/2022-07-fractional-v2-contest

### Keywords for Search

`ERC1155`

