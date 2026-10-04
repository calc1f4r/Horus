---
# Core Classification
protocol: Linea Message Service
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26808
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/06/linea-message-service/
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 2
finders:
  -  Tejaswa Rastogi

  - Rai Yang
---

## Vulnerability Title

Front Running finalizeBlocks When Sequencers Are Decentralized

### Overview


This bug report is about a potential vulnerability in the decentralized sequencer system. The issue is that one sequencer could front run another sequencer’s `finalizeBlocks` transaction, without doing the actual proving and sequencing, and steal the reward for sequencing if there is one. The code snippet provided shows the `finalizeBlocks` function from the ZkEvmV2.sol contract. The recommendation is to add the sequencer’s address as one parameters in the `_finalizeBlocks` function and include the sequencer’s address in the public input hash of the proof in verification function `_verifyProof`. This would ensure that the original sequencer’s work is not wasted and the reward is not stolen.

### Original Finding Content

#### Description


When sequencer is decentralized in the future, one sequencer could front run another sequencer’s `finalizeBlocks` transaction, without doing the actual proving and sequencing, and steal the reward for sequencing if there is one. Once the frontrunner’s finalizeBlocks is executed, the original sequencer’s transaction would fail as `currentL2BlockNumber` would increment by one and state root hash won’t match, as a result the original sequencer’s sequencing and proving work will be wasted.


#### Examples


**contracts/contracts/ZkEvmV2.sol:L110-L126**



```
function finalizeBlocks(
 BlockData[] calldata \_blocksData,
 bytes calldata \_proof,
 uint256 \_proofType,
 bytes32 \_parentStateRootHash
)
 external
 whenTypeNotPaused(PROVING\_SYSTEM\_PAUSE\_TYPE)
 whenTypeNotPaused(GENERAL\_PAUSE\_TYPE)
 onlyRole(OPERATOR\_ROLE)
{
 if (stateRootHashes[currentL2BlockNumber] != \_parentStateRootHash) {
 revert StartingRootHashDoesNotMatch();
 }

 \_finalizeBlocks(\_blocksData, \_proof, \_proofType, \_parentStateRootHash, true);
}

```
#### Recommendation


Add the sequencer’s address as one parameters in `_finalizeBlocks` function, and include the sequencer’s address in the public input hash of the proof in verification function `_verifyProof`.



```
function _finalizeBlocks(
   BlockData[] calldata _blocksData,
   bytes memory _proof,
   uint256 _proofType,
   bytes32 _parentStateRootHash,
   bool _shouldProve,
   address _sequencer
 )

```

```
_verifyProof(
        uint256(
          keccak256(
            abi.encode(
              keccak256(abi.encodePacked(blockHashes)),
              firstBlockNumber,
              keccak256(abi.encodePacked(timestampHashes)),
              keccak256(abi.encodePacked(hashOfRootHashes)),
              keccak256(abi.encodePacked(_sequencer)
            )
          )
        ) % MODULO_R,
        _proofType,
        _proof,
        _parentStateRootHash
      );

```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Linea Message Service |
| Report Date | N/A |
| Finders |  Tejaswa Rastogi
, Rai Yang |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2023/06/linea-message-service/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

