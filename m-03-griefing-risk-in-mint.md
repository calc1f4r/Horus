---
# Core Classification
protocol: Canto Identity Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 8871
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-01-canto-identity-protocol-contest
source_link: https://code4rena.com/reports/2023-01-canto-identity
github_link: https://github.com/code-423n4/2023-01-canto-identity-findings/issues/115

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - cross_chain
  - payments

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - shenwilly
  - gzeon
---

## Vulnerability Title

[M-03] Griefing risk in `mint`

### Overview


This bug report is about the optional parameter `_addList` in the `CidNFT.mint()` function. This parameter enables users to register subprotocol NFTs to the CID NFT right after the mint. However, there is a potential issue that could occur if a malicious actor or a lot of users are trying to mint at the same time.

This issue can happen when a malicious actor or multiple users are trying to mint at the same time. For example, if Alice wants to mint and prepares `_addList` with the expected `_cidNFTID` of `1000`, but Bob frontruns her, incrementing the next minting ID to `1001`, Alice's transaction tries to add subprotocol NFTs to ID `1000` which is owned by Bob. This causes the transaction to revert.

In order to mitigate this issue, the `mint` function should be modified so that the minted ID is the one used during the `add` loop, ensuring that `mint` will always succeed.

### Original Finding Content


[CidNFT.sol#L147-L157](https://github.com/code-423n4/2023-01-canto-identity/blob/dff8e74c54471f5f3b84c217848234d474477d82/src/CidNFT.sol#L147-L157)<br>
[CidNFT.sol#L177-L182](https://github.com/code-423n4/2023-01-canto-identity/blob/dff8e74c54471f5f3b84c217848234d474477d82/src/CidNFT.sol#L177-L182)

`CidNFT.mint()` has an optional parameter `_addList` that enables users to register subprotocol NFTs to the CID NFT right after the mint.

However, there is no guarantee that the `_cidNFTID`  encoded in `_addList` is the same ID as the newly minted NFT. If there is a pending mint transaction and another user frontrun the mint transaction with higher fee, the previous transaction will revert as the `_cidNFTID` is no longer the expected ID.

[CidNFT.sol#L177-L182](https://github.com/code-423n4/2023-01-canto-identity/blob/dff8e74c54471f5f3b84c217848234d474477d82/src/CidNFT.sol#L177-L182)

```solidity
address cidNFTOwner = ownerOf[_cidNFTID];
if (
    cidNFTOwner != msg.sender &&
    getApproved[_cidNFTID] != msg.sender &&
    !isApprovedForAll[cidNFTOwner][msg.sender]
) revert NotAuthorizedForCIDNFT(msg.sender, _cidNFTID, cidNFTOwner);
```

A malicious actor can grief this by frontrunning users that try to mint with non-zero `_addList`, causing their mint transaction to fail.

In absence of malicious actor, it is also possible for this issue to happen randomly during busy period where a lot of users are trying to mint at the same time.

### Proof of Concept

*   The next CidNFT mint ID is `1000`.
*   Alice wants to mint and prepares `_addList` with the expected `_cidNFTID` of `1000`.
*   Bob saw Alice's transaction and frontran her, incrementing the next minting ID to `1001`.
*   Alice's transaction tries to add subprotocol NFTs to ID `1000` which is owned by Bob. This causes the transaction to revert.

### Recommended Mitigation Steps

Modify `mint` so that the minted ID is the one used during the `add` loop, ensuring that `mint` will always succeed.

**[berndartmueller (judge) commented](https://github.com/code-423n4/2023-01-canto-identity-findings/issues/115#issuecomment-1435289830):**
 > Although this submission and [H-01](https://github.com/code-423n4/2023-01-canto-identity-findings/issues/67) both share a common root cause of frontrunning mints and colliding CidNFT ids in the `CidNFT.add` function, it is essential to note that the impact of each issue is significantly different and therefore warrant to be kept separate. 

**[OpenCoreCH (Canto Identity) confirmed](https://github.com/code-423n4/2023-01-canto-identity-findings/issues/115#issuecomment-1499329752)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Canto Identity Protocol |
| Report Date | N/A |
| Finders | shenwilly, gzeon |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-canto-identity
- **GitHub**: https://github.com/code-423n4/2023-01-canto-identity-findings/issues/115
- **Contest**: https://code4rena.com/contests/2023-01-canto-identity-protocol-contest

### Keywords for Search

`vulnerability`

