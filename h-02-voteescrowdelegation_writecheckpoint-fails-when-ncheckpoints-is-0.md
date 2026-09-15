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
solodit_id: 8728
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-golom-contest
source_link: https://code4rena.com/reports/2022-07-golom
github_link: https://github.com/code-423n4/2022-07-golom-findings/issues/630

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
  - cryptphi
  - arcoun
---

## Vulnerability Title

[H-02] `VoteEscrowDelegation._writeCheckpoint` fails when `nCheckpoints` is 0

### Overview


This bug report is regarding a vulnerability in the VoteEscrowDelegation.sol contract. The vulnerability occurs when a user calls the `VoteEscrowDelegation.delegate` function in order to make a delegation. This function calls `VoteEscrowDelegation._writeCheckpoint` which updates the checkpoint of `toTokenId`. However, if `nCheckpoints` is 0, `_writeCheckpoint` always reverts. This is because `checkpoints[toTokenId][nCheckpoints - 1]` will trigger an underflow in Solidity 0.8.11. This means that users cannot make any delegation, resulting in a denial of service.

The recommended mitigation step for this vulnerability is to fix `_writeCheckpoint` by adding an if statement that checks if `nCheckpoints` is greater than 0 and if the `oldCheckpoint.fromBlock` equals the current block number. If this is true, then the `oldCheckpoint.delegatedTokenIds` should be set to `_delegatedTokenIds`. If it is false, then a new checkpoint should be created with the `block.number` and `_delegatedTokenIds`.

### Original Finding Content


<https://github.com/code-423n4/2022-07-golom/blob/main/contracts/vote-escrow/VoteEscrowDelegation.sol#L101><br>

<https://github.com/code-423n4/2022-07-golom/blob/main/contracts/vote-escrow/VoteEscrowDelegation.sol#L82-L86><br>

When a user call `VoteEscrowDelegation.delegate` to make a delegation, it calls `VoteEscrowDelegation._writeCheckpoint` to update the checkpoint of `toTokenId`. However, if `nCheckpoints` is 0, `_writeCheckpoint` always reverts. What’s worse, `nCheckpoints` would be zero before any delegation has been made. In conclusion, users cannot make any delegation.

### Proof of Concept

When a user call `VoteEscrowDelegation.delegate` to make a delegation, it calls `VoteEscrowDelegation._writeCheckpoint` to update the checkpoint of `toTokenId`.<br>
<https://github.com/code-423n4/2022-07-golom/blob/main/contracts/vote-escrow/VoteEscrowDelegation.sol#L82-L86>

        function delegate(uint256 tokenId, uint256 toTokenId) external {
            require(ownerOf(tokenId) == msg.sender, 'VEDelegation: Not allowed');
            require(this.balanceOfNFT(tokenId) >= MIN_VOTING_POWER_REQUIRED, 'VEDelegation: Need more voting power');

            delegates[tokenId] = toTokenId;
            uint256 nCheckpoints = numCheckpoints[toTokenId];

            if (nCheckpoints > 0) {
                Checkpoint storage checkpoint = checkpoints[toTokenId][nCheckpoints - 1];
                checkpoint.delegatedTokenIds.push(tokenId);
                _writeCheckpoint(toTokenId, nCheckpoints, checkpoint.delegatedTokenIds);
            } else {
                uint256[] memory array = new uint256[](1);
                array[0] = tokenId;
                _writeCheckpoint(toTokenId, nCheckpoints, array);
            }

            emit DelegateChanged(tokenId, toTokenId, msg.sender);
        }

if `nCheckpoints` is 0, `_writeCheckpoint` always reverts.<br>
Because `checkpoints[toTokenId][nCheckpoints - 1]` will trigger underflow in Solidity 0.8.11<br>
<https://github.com/code-423n4/2022-07-golom/blob/main/contracts/vote-escrow/VoteEscrowDelegation.sol#L101>

        function _writeCheckpoint(
            uint256 toTokenId,
            uint256 nCheckpoints,
            uint256[] memory _delegatedTokenIds
        ) internal {
            require(_delegatedTokenIds.length < 500, 'VVDelegation: Cannot stake more');

            Checkpoint memory oldCheckpoint = checkpoints[toTokenId][nCheckpoints - 1];
            …
        }

### Recommended Mitigation Steps

Fix `_writeCheckpoint`

        function _writeCheckpoint(
            uint256 toTokenId,
            uint256 nCheckpoints,
            uint256[] memory _delegatedTokenIds
        ) internal {
            require(_delegatedTokenIds.length < 500, 'VVDelegation: Cannot stake more');

       

            if (nCheckpoints > 0 && oldCheckpoint.fromBlock == block.number) {
                Checkpoint memory oldCheckpoint = checkpoints[toTokenId][nCheckpoints - 1];
                oldCheckpoint.delegatedTokenIds = _delegatedTokenIds;
            } else {
                checkpoints[toTokenId][nCheckpoints] = Checkpoint(block.number, _delegatedTokenIds);
                numCheckpoints[toTokenId] = nCheckpoints + 1;
            }
        }

**[zeroexdead (Golom) confirmed](https://github.com/code-423n4/2022-07-golom-findings/issues/630)**

**[zeroexdead (Golom) resolved and commented](https://github.com/code-423n4/2022-07-golom-findings/issues/630#issuecomment-1236185600):**
 > Fixed.
> Ref: https://github.com/golom-protocol/contracts/commit/95e83a1abead683083b7ddf07853a26803c70b88



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
| Finders | 0x52, scaraven, berndartmueller, cryptphi, arcoun, Twpony, Lambda, 0xA5DF, MEP, kenzo, Bahurum, simon135, 0xsanson, kyteg, 0xSky, hansfriese, zzzitron, panprog, CertoraInc, ElKu, GalloDaSballo, JohnSmith, rajatbeladiya, GimelSec |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-golom
- **GitHub**: https://github.com/code-423n4/2022-07-golom-findings/issues/630
- **Contest**: https://code4rena.com/contests/2022-07-golom-contest

### Keywords for Search

`vulnerability`

