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
solodit_id: 8751
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-golom-contest
source_link: https://code4rena.com/reports/2022-07-golom
github_link: https://github.com/code-423n4/2022-07-golom-findings/issues/631

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
finders_count: 4
finders:
  - GimelSec
  - GalloDaSballo
  - kenzo
  - kebabsec
---

## Vulnerability Title

[M-14] `VoteEscrowDelegation._transferFrom` can only be executed by the token owner

### Overview


This bug report is about the permission control in the VoteEscrowDelegation smart contract. The `_transferFrom` function should be successfully executed if `msg.sender` is the current owner, an authorized operator, or the approved address. However, the `removeDelegation` function which is called in `_transferFrom` only accepts the token owner. This means that the `_transferFrom` function can only be executed by the token owner. To fix this, the permission control in `removeDelegation` should be changed.

### Original Finding Content


`VoteEscrowDelegation._transferFrom` should be successfully executed if `msg.sender` is the current owner, an authorized operator, or the approved address. `removeDelegation` is called in `_transferFrom`. `removeDelegation` only accepts the token owner. Thus, `_transferFrom` can only be executed by the token owner.

### Proof of Concept

`removeDelegation` is called in `_transferFrom`<br>
<https://github.com/code-423n4/2022-07-golom/blob/main/contracts/vote-escrow/VoteEscrowDelegation.sol#L242>

        function _transferFrom(
            address _from,
            address _to,
            uint256 _tokenId,
            address _sender
        ) internal override {
            require(attachments[_tokenId] == 0 && !voted[_tokenId], 'attached');

            // remove the delegation
            this.removeDelegation(_tokenId);

            // Check requirements
            require(_isApprovedOrOwner(_sender, _tokenId));
            …
        }

However, `removeDelegation` only accept the token owner<br>
<https://github.com/code-423n4/2022-07-golom/blob/main/contracts/vote-escrow/VoteEscrowDelegation.sol#L211>

        function removeDelegation(uint256 tokenId) external {
            require(ownerOf(tokenId) == msg.sender, 'VEDelegation: Not allowed');
            uint256 nCheckpoints = numCheckpoints[tokenId];
            Checkpoint storage checkpoint = checkpoints[tokenId][nCheckpoints - 1];
            removeElement(checkpoint.delegatedTokenIds, tokenId);
            _writeCheckpoint(tokenId, nCheckpoints, checkpoint.delegatedTokenIds);
        }

### Recommended Mitigation Steps

Fix the permission control in `removeDelegation`.

**[zeroexdead (Golom) confirmed](https://github.com/code-423n4/2022-07-golom-findings/issues/631)**

**[zeroexdead (Golom) commented](https://github.com/code-423n4/2022-07-golom-findings/issues/631#issuecomment-1236182667):**
 > Changed the `external` function to `public`. Users address will be passed as `msg.sender` now.<br>
> https://github.com/golom-protocol/contracts/commit/10ec920765a5ee2afc2fe269d32ea9138d1156b6

**[0xsaruman (Golom) resolved](https://github.com/code-423n4/2022-07-golom-findings/issues/631)**



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
| Finders | GimelSec, GalloDaSballo, kenzo, kebabsec |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-golom
- **GitHub**: https://github.com/code-423n4/2022-07-golom-findings/issues/631
- **Contest**: https://code4rena.com/contests/2022-07-golom-contest

### Keywords for Search

`vulnerability`

