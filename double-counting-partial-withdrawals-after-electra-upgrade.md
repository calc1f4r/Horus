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
solodit_id: 53594
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Eigen_Labs_EigenLayer_Checkpoint_Proofs_Security_Assessment_Report_v2.0.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Eigen_Labs_EigenLayer_Checkpoint_Proofs_Security_Assessment_Report_v2.0.pdf
github_link: none

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
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Double-Counting Partial Withdrawals After Electra Upgrade

### Overview

See description below for full details.

### Original Finding Content

## Description

Due to EIP-7251 and EIP-7002, partial withdrawals can occur below the MAX_EFFECTIVE_BALANCE after the Electra upgrade. Hence, it is possible for ETH from partial withdrawals to be double-counted. A pod owner can choose the `beaconTimestamp` used to verify a validator's withdrawal credentials on the EigenPod. This opens the checkpoint system to a timing attack where ETH withdrawn to the EigenPod is double-counted by picking a `beaconTimestamp` before the withdrawal has occurred.

The `_verifyWithdrawalCredentials()` protects against this attack by preventing exiting validators from verifying their withdrawal credentials in the check below:

```solidity
require(
    validatorFields.getExitEpoch() == BeaconChainProofs.FAR_FUTURE_EPOCH,
    "EigenPod._verifyWithdrawalCredentials: validator must not be exiting"
);
```

This check only protects against timing attacks for full withdrawals. Currently, as of the Deneb upgrade, only ETH greater than MAX_EFFECTIVE_BALANCE is partially withdrawn. Hence, timing attacks for partial withdrawals are not possible, as this ETH does not get counted in a validator's effective balance.

EIP-7251 and EIP-7002, both included in the upcoming Electra upgrade, allow a validator to have partial withdrawals that occur below MAX_EFFECTIVE_BALANCE through withdrawal requests submitted from the execution layer (EL). This opens the EigenPod to partial withdrawal timing attacks. Fortunately, partial withdrawal requests are only valid if they're from the validator's compounding withdrawal credentials. Hence, only the EigenPod is capable of submitting valid partial withdrawal requests.

Note, this issue has an informational severity rating as the in-scope EigenPod code currently does not implement EL-triggerable withdrawals and hence is not vulnerable to the attack described above.

## Recommendations

- Consider only allowing validators verified in the EigenPod to submit withdrawal requests. This would prevent EL-triggered partial withdrawals below MAX_EFFECTIVE_BALANCE from being processed before the validator has been verified on the EigenPod.
- Note that the recommendation above only protects against EL-triggered partial withdrawals introduced in EIP-7002. If custom ceilings for partial withdrawal sweeps were included in another future Ethereum upgrade, then the EigenPod will still be susceptible to partial withdrawal timing attacks.
- Alternatively, consider capping the amount of ETH credited to the validator's `ValidatorInfo::restakedBalanceGwei` to 32 ETH in `_verifyWithdrawalCredentials()`, such that any ETH that is able to be partially withdrawn is deducted from the validator's effective balance. If this recommendation is implemented, then the pod owner will then need to start and finalize a checkpoint to accurately record their validator's balance if it is above the 32 ETH cap.

## Resolution

The EigenLayer team has acknowledged the issue with the following comment:

"We will carefully consider the recommendations provided when upgrading the EigenPod beacon in the future to support execution layer triggerable withdrawals."

## EGN5-06 Miscellaneous General Comments

- **Asset:** All contracts
- **Status:** Closed: See Resolution
- **Rating:** Informational

### Description

This section details miscellaneous findings discovered by the testing team that do not have direct security implications:

1. **Custom Errors**
   - **Related Asset(s):** /*
   - The codebase makes use of string errors rather than the newer custom errors feature. Since this feature has now matured, it is advised to use custom errors to reduce gas costs. Replace string errors with custom errors throughout the codebase.

2. **Misleading NatSpec Comment**
   - **Related Asset(s):** `pods/EigenPod.sol`
   - On line 124 of `EigenPod.sol`, there is the NatSpec comment: "and any validators with 0 balance are marked WITHDRAWN." This flow is only present for checkpoints that continue through `verifyCheckpointProofs()`. It is possible for a checkpoint to be completed in `startCheckpoint()` due to there being no active validators; hence, this flow may not necessarily be present. Update the NatSpec comment to make it clear validators are only marked as WITHDRAWN if the function `verifyCheckpointProofs()` is called.

3. **Typos**
   - **Related Asset(s):** `interfaces/IEigenPod.sol`, `interfaces/IEigenManager.sol`
   - There are some typos present in the interface which should be corrected to improve reader clarity.
     - In the `IEigenPod` contract:
       - On line [74], "validaor" should read "validator" and "to have" should read "to have had" given a checkpoint is in the past.
       - On line [97], "Create" should read "Creates".
       - On line [99], "marked" should read "marked as".
     - In the `IEigenPodManager` contract:
       - On line [89], "from Pod owner owner" should read "from Pod owner".
   - Correct typos where noted.

4. **Floating Version Pragma**
   - **Related Asset(s):** /*
   - The contracts specify a floating Solidity pragma `^0.8.12`. This can introduce version-specific bugs should any contracts be deployed with a different Solidity version. The pragma version should be locked at the version where testing occurred.

## Recommendations

Ensure that the comments are understood and acknowledged, and consider implementing the suggestions above.

## Resolution

The EigenLayer team has acknowledged the miscellaneous comments above.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | EigenLayer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Eigen_Labs_EigenLayer_Checkpoint_Proofs_Security_Assessment_Report_v2.0.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Eigen_Labs_EigenLayer_Checkpoint_Proofs_Security_Assessment_Report_v2.0.pdf

### Keywords for Search

`vulnerability`

