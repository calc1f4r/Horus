---
# Core Classification
protocol: Golom
chain: everychain
category: uncategorized
vulnerability_type: vote

# Attack Vector Details
attack_type: vote
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 8730
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-golom-contest
source_link: https://code4rena.com/reports/2022-07-golom
github_link: https://github.com/code-423n4/2022-07-golom-findings/issues/169

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - vote

protocol_categories:
  - dexes
  - services
  - liquidity_manager
  - nft_marketplace
  - options_vault

# Audit Details
report_date: unknown
finders_count: 24
finders:
  - 0x52
  - scaraven
  - berndartmueller
  - GiveMeTestEther
  - arcoun
---

## Vulnerability Title

[H-04] Old delegatee not deleted when delegating to new tokenId

### Overview


A bug was reported in the VoteEscrowDelegation.sol file on line 80 of the code. The vulnerability allows users to multiply their voting power, which makes the token useless for voting and governance decisions. This is done by calling the `delegate` function with different tokenIds. For example, Bob owns token 1 with a balance of 1000 and also owns tokens 2, 3, 4, and 5. If he calls `delegate(1, 2)`, `delegate(1, 3)`, `delegate(1, 4)`, and `delegate(1, 5)`, then when `getVotes` is called, Bob's balance of 1000 is included in tokens 2, 3, 4, and 5, thus quadrupling the voting power of token 1. To mitigate this vulnerability, the entry in `delegatedTokenIds` of the old delegatee should be removed or `removeDelegation` should be called first.

### Original Finding Content


[VoteEscrowDelegation.sol#L80](https://github.com/code-423n4/2022-07-golom/blob/8f198624b97addbbe9602a451c908ea51bd3357c/contracts/vote-escrow/VoteEscrowDelegation.sol#L80)<br>

In `delegate`, when a user delegates to a new tokenId, the tokenId is not removed from the current delegatee. Therefore, one user can easily multiply his voting power, which makes the toking useless for voting / governance decisions.

### Proof Of Concept

Bob owns the token with ID 1 with a current balance of 1000. He also owns tokens 2, 3, 4, 5. Therefore, he calls `delegate(1, 2)`, `delegate(1, 3)`, `delegate(1, 4)`, `delegate(1, 5)`. Now, if there is a governance decision and `getVotes` is called, Bobs balance of 1000 is included in token 2, 3, 4, and 5. Therefore, he quadrupled the voting power of token 1.

### Recommended Mitigation Steps

Remove the entry in `delegatedTokenIds` of the old delegatee or simply call `removeDelegation` first.

**[zeroexdead (Golom) confirmed](https://github.com/code-423n4/2022-07-golom-findings/issues/169)**

**[zeroexdead (Golom) commented](https://github.com/code-423n4/2022-07-golom-findings/issues/169#issuecomment-1238345165):**
 > Fixed. 
> 
> Ref: https://github.com/golom-protocol/contracts/commit/c74d95b4105eeb878d2781982178db5ca08a1a9b



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Golom |
| Report Date | N/A |
| Finders | 0x52, scaraven, berndartmueller, GiveMeTestEther, arcoun, Twpony, 0xDjango, Lambda, Green, 0xA5DF, MEP, kenzo, Bahurum, 0xsanson, cccz, kyteg, 0xpiglet, panprog, GalloDaSballo, rajatbeladiya, dipp, neumo, obront, GimelSec |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-golom
- **GitHub**: https://github.com/code-423n4/2022-07-golom-findings/issues/169
- **Contest**: https://code4rena.com/contests/2022-07-golom-contest

### Keywords for Search

`Vote`

