---
# Core Classification
protocol: Linea ENS
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34975
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2024/06/linea-ens/
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

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

Missing Validation for Matching Number of Storage Proofs and Commands ✓ Fixed

### Overview


This bug report describes an issue with the `getStorageValues` function in the `LineaProofHelper` library. If the number of storage proofs returned by the gateway is less than the number of commands, an out-of-bounds array error occurs. This can happen when the gateway provides fewer storage proofs than requested, causing the function to fail. The bug has been fixed in a pull request and the recommendation is to add a `require` statement to check for equal numbers of storage proofs and commands.

### Original Finding Content

#### Resolution



 The problem has been fixed in the [PR\#165](https://github.com/Consensys/linea-resolver/pull/165/files).
 

#### Description


In the function `getStorageValues` of the `LineaProofHelper` library, if the number of storage proofs (`storageProofs`) returned by the gateway is less than number of commands (`commands.length`), there will be an out\-of\-bounds array error. This situation arises when the gateway provides fewer storage proofs than the requested storage slots leading to a failure in `getStorageValues`.


#### Examples


**packages/l1\-contracts/contracts/linea\-verifier/LineaProofHelper.sol:L232\-L260**



```
for (uint256 i = 0; i < commands.length; i++) {
    bytes32 command = commands[i];
    (bool isDynamic, uint256 slot) = computeFirstSlot(
        command,
        constants,
        values
    );
    if (!isDynamic) {
        if (!storageProofs[proofIdx].initialized) {
            values[i] = abi.encode(0);
            proofIdx++;
        } else {
            verifyStorageProof(
                account,
                storageProofs[proofIdx].leafIndex,
                storageProofs[proofIdx].proof.proofRelatedNodes,
                storageProofs[proofIdx].proof.value,
                bytes32(slot)
            );

            values[i] = abi.encode(
                storageProofs[proofIdx++].proof.value
            );

            if (values[i].length > 32) {
                revert InvalidSlotSize(values[i].length);
            }
        }
    } else {

```
#### Recommendation


Add a `require` statement to check whether the number of storage proofs is equal to the number of commands

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Linea ENS |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2024/06/linea-ens/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

