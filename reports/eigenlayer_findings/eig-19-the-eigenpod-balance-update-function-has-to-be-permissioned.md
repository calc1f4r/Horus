---
# Core Classification
protocol: Eigenlayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53496
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-10-16-EigenLayer.md
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
finders_count: 1
finders:
  - Hexens
---

## Vulnerability Title

[EIG-19] The EigenPod balance update function has to be permissioned

### Overview


The bug report discusses an issue with the `verifyBalanceUpdate()` function in the EigenPod.sol contract. This function can be called by anyone with valid proof of a validator's current balance on the beacon chain, which could result in the adjustment of a pod owner's shares. However, there is a potential vulnerability where someone with malicious intent could call this function before a pod owner processes a withdrawal, causing the pod owner's shares to be massively decreased. To fix this, the function should be permissioned. This issue has been resolved.

### Original Finding Content

**Severity:** Medium

**Path:** EigenPod.sol:verifyBalanceUpdate#L193-L274

**Description:**  

The `verifyBalanceUpdate()` function is permissionless and, therefore, could be called by anyone with valid proof of a validator's current balance on the beacon chain. Resulting in the adjustment of a pod owner's shares.

Whilst withdrawals are processed by `verifyAndProcessWithdrawals()` against historical summaries https://github.com/Layr-Labs/eigenlayer-contracts/blob/master/docs/core/proofs/BeaconChainProofs.md#beaconchainproofsverifywithdrawal. They could be generated with a time lag of `8192 slots` or ~ `27 hours`.

Consider the following scenario when a Pod owner withdrew a fraction of their validators. In an unlucky case,  withdrawal slots of validators are close, and are at the beginning of the `8192 slot` window. So the pod owner have to wait one day before they can call the `verifyAndProcessWithdrawals()`.

In the meantime, someone with malicious intent could call `verifyBalanceUpdate` before the pod owner processes the withdrawal. And so the balances of those validators will be set to `0`, and the pod owner's shares will be massively decreased.

```
    function verifyBalanceUpdate(
        uint64 oracleTimestamp,
        uint40 validatorIndex,
        BeaconChainProofs.StateRootProof calldata stateRootProof,
        BeaconChainProofs.BalanceUpdateProof calldata balanceUpdateProof,
        bytes32[] calldata validatorFields
    ) external onlyWhenNotPaused(PAUSED_EIGENPODS_VERIFY_BALANCE_UPDATE) {  // @audit permissionless
    ...
    }
```

**Remediation:**  The `verifyBalanceUpdate()` function should be permissioned.  

**Status:**   Fixed

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Eigenlayer |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-10-16-EigenLayer.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

