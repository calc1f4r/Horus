---
# Core Classification
protocol: PoolTogether
chain: everychain
category: uncategorized
vulnerability_type: safetransfer

# Attack Vector Details
attack_type: safetransfer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25482
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-06-pooltogether
source_link: https://code4rena.com/reports/2021-06-pooltogether
github_link: https://github.com/code-423n4/2021-06-pooltogether-findings/issues/115

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.20
financial_impact: medium

# Scoring
quality_score: 1
rarity_score: 1

# Context Tags
tags:
  - safetransfer
  - transferfrom_vs_safetransferfrom
  - erc721

protocol_categories:
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-07] Using `transferFrom` on ERC721 tokens

### Overview


A bug has been identified in the function `awardExternalERC721` of contract `PrizePool`. Currently, the `transferFrom` keyword is used instead of `safeTransferFrom` when awarding external ERC721 tokens to the winners. This could cause problems if a winner is a contract and is not aware of incoming ERC721 tokens, as the sent tokens could be locked. It is recommended to change `transferFrom` to `safeTransferFrom` at line 602. However, this could introduce a DoS attack vector if any winner maliciously rejects the received ERC721 tokens to make the others unable to get their awards. Possible solutions to this are to use a `try/catch` statement to handle error cases separately or provide a function for the pool owner to remove malicious winners manually if this happens. The severity of this bug was initially debated by shw, asselstine (PoolTogether) and dmvt (judge). Asselstine and dmvt agreed that it poses a low risk to the Prize Pool, and should be implemented to respect the interface.

### Original Finding Content

_Submitted by shw_

In the function `awardExternalERC721` of contract `PrizePool`, when awarding external ERC721 tokens to the winners, the `transferFrom` keyword is used instead of `safeTransferFrom`. If any winner is a contract and is not aware of incoming ERC721 tokens, the sent tokens could be locked.

Recommend consider changing `transferFrom` to `safeTransferFrom` at line 602. However, it could introduce a DoS attack vector if any winner maliciously rejects the received ERC721 tokens to make the others unable to get their awards. Possible mitigations are to use a `try/catch` statement to handle error cases separately or provide a function for the pool owner to remove malicious winners manually if this happens.

**[asselstine (PoolTogether) confirmed and disagreed with severity](https://github.com/code-423n4/2021-06-pooltogether-findings/issues/115#issuecomment-868021913):**
 > This issue poses no risk to the Prize Pool, so it's more of a `1 (Low Risk` IMO.
>
> This is just about triggering a callback on the ERC721 recipient.  We omitted it originally because we didn't want a revert on the callback to DoS the prize pool.
>
> However, to respect the interface it makes sense to implement it fully.  That being said, if it does throw we must ignore it to prevent DoS attacks.

**[dmvt (judge) commented](https://github.com/code-423n4/2021-06-pooltogether-findings/issues/115#issuecomment-907507608):**
 > I agree with the medium risk rating provided by the warden.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 1/5 |
| Rarity Score | 1/5 |
| Audit Firm | Code4rena |
| Protocol | PoolTogether |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-06-pooltogether
- **GitHub**: https://github.com/code-423n4/2021-06-pooltogether-findings/issues/115
- **Contest**: https://code4rena.com/reports/2021-06-pooltogether

### Keywords for Search

`SafeTransfer, transferFrom vs safeTransferFrom, ERC721`

