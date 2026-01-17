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
solodit_id: 20064
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-04-eigenlayer
source_link: https://code4rena.com/reports/2023-04-eigenlayer
github_link: https://github.com/code-423n4/2023-04-eigenlayer-findings/issues/38

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

[L-05] The condition for full withdrawals in the code is different from that in the documentation

### Overview

See description below for full details.

### Original Finding Content


### Proof of Concept
The condition in [docs](https://github.com/code-423n4/2023-04-eigenlayer/blob/138cf7edb887f641ae48e33e963ab1be4ff474c1/docs/EigenPods.md) for full withdrawal is `validator.withdrawableEpoch < executionPayload.slot/SLOTS_PER_EPOCH` while in the code its `validator.withdrawableEpoch <= executionPayload.slot/SLOTS_PER_EPOCH`.

```solidity
    function verifyAndProcessWithdrawal(
        BeaconChainProofs.WithdrawalProofs calldata withdrawalProofs, 
        bytes calldata validatorFieldsProof,
        bytes32[] calldata validatorFields,
        bytes32[] calldata withdrawalFields,
        uint256 beaconChainETHStrategyIndex,
        uint64 oracleBlockNumber
    )
...
        // reference: uint64 withdrawableEpoch = Endian.fromLittleEndianUint64(validatorFields[BeaconChainProofs.VALIDATOR_WITHDRAWABLE_EPOCH_INDEX]);
        if (Endian.fromLittleEndianUint64(validatorFields[BeaconChainProofs.VALIDATOR_WITHDRAWABLE_EPOCH_INDEX]) <= slot/BeaconChainProofs.SLOTS_PER_EPOCH) {
            _processFullWithdrawal(withdrawalAmountGwei, validatorIndex, beaconChainETHStrategyIndex, podOwner, validatorStatus[validatorIndex]);
        } else {
            _processPartialWithdrawal(slot, withdrawalAmountGwei, validatorIndex, podOwner);
        }
    }

```
[src/contracts/pods/EigenPod.sol#L354](https://github.com/code-423n4/2023-04-eigenlayer/blob/398cc428541b91948f717482ec973583c9e76232/src/contracts/pods/EigenPod.sol#L354)

### Recommended Mitigation Steps
Synchronize them with each other.

**[Sidu28 (EigenLayer) disputed, disagreed with severity and commented](https://github.com/code-423n4/2023-04-eigenlayer-findings/issues/38#issuecomment-1545178392):**
>We believe this is an informational-level issue. We failed to update this statement in the higher-level documentation. The code is correct.

**[Alex the Entreprenerd (judge) decreased severity to QA and commented](https://github.com/code-423n4/2023-04-eigenlayer-findings/issues/38#issuecomment-1571504055):**
>Great catch, but in lack of an impact am downgrading to QA.
>
>Will award extra points. L + 3.

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
- **GitHub**: https://github.com/code-423n4/2023-04-eigenlayer-findings/issues/38
- **Contest**: https://code4rena.com/reports/2023-04-eigenlayer

### Keywords for Search

`vulnerability`

