---
# Core Classification
protocol: Golom
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 8754
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-golom-contest
source_link: https://code4rena.com/reports/2022-07-golom
github_link: https://github.com/code-423n4/2022-07-golom-findings/issues/191

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - services
  - liquidity_manager
  - nft_marketplace
  - options_vault

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 0x52
  - 0xsanson
---

## Vulnerability Title

[M-17] NFTs that don't have a checkpoint can't be transferred

### Overview


This bug report is about a vulnerability in the transferFrom() function of the VoteEscrowDelegation.sol contract. It impacts the transfer of NFTs (Non-Fungible Tokens) that don't have a checkpoint, as they can't be transferred. A proof of concept is provided, showing that the transferFrom() function calls removeDelegation() with the tokenId of the token being transferred. If the token doesn't have any checkpoints, an underflow error will occur and the transfer will be reverted. The recommended mitigation step is to make removeDelegation simply return if nCheckpoints = 0.

### Original Finding Content


Submitting as high risk because it breaks a fundamental operation (transferring) for a large number of tokens.

### Proof of Concept

<https://github.com/code-423n4/2022-07-golom/blob/7bbb55fca61e6bae29e57133c1e45806cbb17aa4/contracts/vote-escrow/VoteEscrowDelegation.sol#L212-L213>

        uint256 nCheckpoints = numCheckpoints[tokenId];
        Checkpoint storage checkpoint = checkpoints[tokenId][nCheckpoints - 1];

L242 of `transferFrom()` calls `removeDelegation()` with the tokenId of the token being transferred. For tokens that don't have any checkpoints, L212 will return 0. This was cause an underflow error and revert in L213.

### Recommended Mitigation Steps

Make removeDelegation simply return if `nCheckpoints = 0`.

**[kenzo (warden) commented](https://github.com/code-423n4/2022-07-golom-findings/issues/191#issuecomment-1202226637):**
 > Unsure if high risk, but warden correctly identified the issue (that some others didn't) that the underflow in `removeDelegation` will prevent tokens from being transferred.

**[zeroexdead (Golom) disagreed with severity](https://github.com/code-423n4/2022-07-golom-findings/issues/191)**

**[LSDan (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-07-golom-findings/issues/191#issuecomment-1276259331):**
 > Marking this as a medium risk because it only temporarily breaks functionality. The workaround would be to delegate the token and then transfer it, making the impact aggravating but ultimately minimal.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Golom |
| Report Date | N/A |
| Finders | 0x52, 0xsanson |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-golom
- **GitHub**: https://github.com/code-423n4/2022-07-golom-findings/issues/191
- **Contest**: https://code4rena.com/contests/2022-07-golom-contest

### Keywords for Search

`vulnerability`

