---
# Core Classification
protocol: EigenLayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20060
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-04-eigenlayer
source_link: https://code4rena.com/reports/2023-04-eigenlayer
github_link: https://github.com/code-423n4/2023-04-eigenlayer-findings/issues/63

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

[L-01] `computePhase0Eth1DataRoot` always returns an incorrect Merkle tree

### Overview

See description below for full details.

### Original Finding Content


The Merkle tree creation inside the `computePhase0Eth1DataRoot` function is incorrect.

### Proof of Concept

Provide direct links to all referenced code in GitHub. Add screenshots, logs, or any other relevant proof that illustrates the concept. Not all fields of `eth1DataFields` are being used in an array due to the usage of `i < ETH1_DATA_FIELD_TREE_HEIGHT` instead of `i<NUM_ETH1_DATA_FIELDS`. Check other similar functions.

[src/contracts/libraries/BeaconChainProofs.sol#L160](https://github.com/Layr-Labs/eigenlayer-contracts/blob/eccdfd43bb882d66a68cad8875dde2979e204546/src/contracts/libraries/BeaconChainProofs.sol#L160)

```solidity
    function computePhase0Eth1DataRoot(bytes32[NUM_ETH1_DATA_FIELDS] calldata eth1DataFields) internal pure returns(bytes32) {  
        bytes32[] memory paddedEth1DataFields = new bytes32[](2**ETH1_DATA_FIELD_TREE_HEIGHT);
        
        for (uint256 i = 0; i < ETH1_DATA_FIELD_TREE_HEIGHT; ++i) {
            paddedEth1DataFields[i] = eth1DataFields[i];
        }

        return Merkle.merkleizeSha256(paddedEth1DataFields);
    }

```

### Recommended Mitigation Steps

```diff
    function computePhase0Eth1DataRoot(bytes32[NUM_ETH1_DATA_FIELDS] calldata eth1DataFields) internal pure returns(bytes32) {  
        bytes32[] memory paddedEth1DataFields = new bytes32[](2**ETH1_DATA_FIELD_TREE_HEIGHT);
        
_        for (uint256 i = 0; i < ETH1_DATA_FIELD_TREE_HEIGHT; ++i) {
+        for (uint256 i = 0; i < NUM_ETH1_DATA_FIELDS; ++i) {
           paddedEth1DataFields[i] = eth1DataFields[i];
        }

        return Merkle.merkleizeSha256(paddedEth1DataFields);
    }

```

### Assessed type

Math

**[Sidu28 (EigenLayer) disagreed with severity and commented](https://github.com/code-423n4/2023-04-eigenlayer-findings/issues/63#issuecomment-1545172210):**
 > We believe this is low severity. The code is unused and informally deprecated, but it is indeed technically incorrect.

**[Alex the Entreprenerd (judge) decreased severity to QA and commented](https://github.com/code-423n4/2023-04-eigenlayer-findings/issues/63#issuecomment-1567105145):**
 > Agree with the Sponsor, because the code is unused.

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2023-04-eigenlayer-findings/issues/63#issuecomment-1582482224):**
>Consistently high quality submissions. After grading the QAs I believe the Warden deserves the best place.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | EigenLayer |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2023-04-eigenlayer
- **GitHub**: https://github.com/code-423n4/2023-04-eigenlayer-findings/issues/63
- **Contest**: https://code4rena.com/reports/2023-04-eigenlayer

### Keywords for Search

`vulnerability`

