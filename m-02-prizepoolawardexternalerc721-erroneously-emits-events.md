---
# Core Classification
protocol: PoolTogether
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25560
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-10-pooltogether
source_link: https://code4rena.com/reports/2021-10-pooltogether
github_link: https://github.com/code-423n4/2021-10-pooltogether-findings/issues/62

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
finders_count: 0
finders:
---

## Vulnerability Title

[M-02] `PrizePool.awardExternalERC721()` Erroneously Emits Events

### Overview


This bug report concerns the `awardExternalERC721()` function in the PrizePool smart contract of PoolTogether. This function is used to ensure that a single tokenId cannot deny function execution. If the try statement fails, an `ErrorAwardingExternalERC721` event is emitted with the relevant error. However, the failed tokenId is not removed from the list of tokenIds emitted at the end of function execution, meaning the `AwardedExternalERC721` event is emitted with the entire list of tokenIds, regardless of failure. This could lead to users or scripts being tricked into thinking an ERC721 tokenId was successfully awarded. 

Manual code review was used to identify this bug. To mitigate this issue, the recommendation is to only emit successfully transferred tokenIds in the `AwardedExternalERC721` event. PoolTogether acknowledged and patched the issue with a pull request, and an additional comment from a judge noted that the sponsor actively managed a list of `_awardedTokenIds` to keep track of the tokens that didn't go through the `catch` part of the error handling.

### Original Finding Content

_Submitted by leastwood_.

#### Impact

The `awardExternalERC721()` function uses solidity's try and catch statement to ensure a single tokenId cannot deny function execution. If the try statement fails, an `ErrorAwardingExternalERC721` event is emitted with the relevant error, however, the failed tokenId is not removed from the list of tokenIds emitted at the end of function execution. As a result, the `AwardedExternalERC721` is emitted with the entire list of tokenIds, regardless of failure.  An off-chain script or user could therefore be tricked into thinking an ERC721 tokenId was successfully awarded.

#### Proof of Concept

<https://github.com/pooltogether/v4-core/blob/master/contracts/prize-pool/PrizePool.sol#L250-L270>

#### Tools Used

Manual code review

#### Recommended Mitigation Steps

Consider emitting only successfully transferred tokenIds in the `AwardedExternalERC721` event.

**[PierrickGT (PoolTogether) confirmed and patched](https://github.com/code-423n4/2021-10-pooltogether-findings/issues/62#issuecomment-943617886):**
 > PR: https://github.com/pooltogether/v4-core/pull/246

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2021-10-pooltogether-findings/issues/62#issuecomment-943857035):**
 > The sponsor acknowledged and mitigated by actively managing a list of `_awardedTokenIds` to keep track of the tokens that didn't go through the `catch` part of the error hadling



 


### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | PoolTogether |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-10-pooltogether
- **GitHub**: https://github.com/code-423n4/2021-10-pooltogether-findings/issues/62
- **Contest**: https://code4rena.com/reports/2021-10-pooltogether

### Keywords for Search

`vulnerability`

