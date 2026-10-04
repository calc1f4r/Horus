---
# Core Classification
protocol: Slock.it Incubed3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13975
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2019/09/slock.it-incubed3/
github_link: none

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
  - dexes
  - cdp
  - services
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Martin Ortner
  - Shayan Eskandari
---

## Vulnerability Title

BlockhashRegistry - recreateBlockheaders succeeds and emits an event even though no blockheaders have been provided ✓ Fixed

### Overview


A bug was discovered in the BlockhashRegistry.sol contract, which allowed for vulnerable scenarios and potentially overwriting existing blockhashes. The method used to re-create blockhashes from a list of rlp-encoded _blockheaders was not properly checking if _blockheaders actually contained items. As a result, the method was unnecessarily storing the same value that was already in the blockhashMapping at the same location and wrongly logging LogBlockhashAdded even though nothing had been added nor changed.

To fix the issue, proper checks were added to prevent passing empty _blockheaders in [8d2bfa40](https://git.slock.it/in3/in3-contracts/commit/8d2bfa40ac10dae9a1ae046ca1ed7d2fbf2e0425) and to prevent storing the same blockhash twice in [80bb6ecf](https://git.slock.it/in3/in3-contracts/commit/80bb6ecf19ec4cbc2de0367c4c5dc31661533689).

It is recommended that user provided input is validated to be within safe bounds, such as at least one _blockheader being provided, and that _blockNumber is less than block.number. Additionally, the code should not expect parts of it to throw and safe the contract from exploitation.

### Original Finding Content

#### Resolution



Fixed the vulnerable scenarios by adding proper checks to:


* Prevent passing empty `_blockheaders` in [8d2bfa40](https://git.slock.it/in3/in3-contracts/commit/8d2bfa40ac10dae9a1ae046ca1ed7d2fbf2e0425)
* Prevent storing the same blockhash twice in [80bb6ecf](https://git.slock.it/in3/in3-contracts/commit/80bb6ecf19ec4cbc2de0367c4c5dc31661533689)




#### Description


The method is used to re-create blockhashes from a list of rlp-encoded `_blockheaders`. However, the method never checks if `_blockheaders` actually contains items. The result is, that the method will unnecessarily store the same value that is already in the `blockhashMapping` at the same location and wrongly log `LogBlockhashAdded` even though nothing has been added nor changed.


* 1. assume `_blockheaders` is empty and the registry already knows the blockhash of `_blockNumber`


**code/in3-contracts/contracts/BlockhashRegistry.sol:L61-L67**



```
function recreateBlockheaders(uint \_blockNumber, bytes[] memory \_blockheaders) public {

    bytes32 currentBlockhash = blockhashMapping[\_blockNumber];
    require(currentBlockhash != 0x0, "parentBlock is not available");

    bytes32 calculatedHash = reCalculateBlockheaders(\_blockheaders, currentBlockhash);
    require(calculatedHash != 0x0, "invalid headers");

```
* 2. An attempt is made to re-calculate the hash of an empty `_blockheaders` array (also passing the `currentBlockhash` from the registry)


**code/in3-contracts/contracts/BlockhashRegistry.sol:L66-L66**



```
bytes32 calculatedHash = reCalculateBlockheaders(\_blockheaders, currentBlockhash);

```
* 3. The following loop in `reCalculateBlockheaders` is skipped and the `currentBlockhash` is returned.


**code/in3-contracts/contracts/BlockhashRegistry.sol:L134-L149**



```
function reCalculateBlockheaders(bytes[] memory \_blockheaders, bytes32 \_bHash) public pure returns (bytes32 bhash) {

    bytes32 currentBlockhash = \_bHash;
    bytes32 calcParent = 0x0;
    bytes32 calcBlockhash = 0x0;

    /// save to use for up to 200 blocks, exponential increase of gas-usage afterwards
    for (uint i = 0; i < \_blockheaders.length; i++) {
        (calcParent, calcBlockhash) = getParentAndBlockhash(\_blockheaders[i]);
        if (calcBlockhash != currentBlockhash) {
            return 0x0;
        }
        currentBlockhash = calcParent;
    }

    return currentBlockhash;

```
* 4. The assertion does not fire, the `bnr` to store the `calculatedHash` is the same as the one initially provided to the method as an argument.. Nothing has changed but an event is emitted.


**code/in3-contracts/contracts/BlockhashRegistry.sol:L69-L74**



```
    /// we should never fail this assert, as this would mean that we were able to recreate a invalid blockchain
    assert(\_blockNumber > \_blockheaders.length);
    uint bnr = \_blockNumber - \_blockheaders.length;
    blockhashMapping[bnr] = calculatedHash;
    emit LogBlockhashAdded(bnr, calculatedHash);
}

```
#### Recommendation


The method is crucial for the system to work correctly and must be tightly controlled by input validation. It should not be allowed to overwrite an existing value in the contract ([issue 6.29](#blockhashregistry---existing-blockhashes-can-be-overwritten)) or emit an event even though nothing has happened. Therefore validate that user provided input is within safe bounds. In this case, that at least one `_blockheader` has been provided. Validate that `_blockNumber` is less than `block.number` and do not expect that parts of the code will throw and safe the contract from exploitation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Slock.it Incubed3 |
| Report Date | N/A |
| Finders | Martin Ortner, Shayan Eskandari |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2019/09/slock.it-incubed3/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

