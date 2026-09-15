---
# Core Classification
protocol: Puffer Institutional
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50015
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Puffer-Spearbit-Security-Review-February-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Puffer-Spearbit-Security-Review-February-2025.pdf
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
finders_count: 3
finders:
  - Hyh
  - Ladboy233
  - Noah Marconi
---

## Vulnerability Title

Withdrawn stake can be miscounted in total assets right after the Eigen Layer withdrawal

### Overview

See description below for full details.

### Original Finding Content

## Severity: Low Risk

## Context
InstitutionalVault.sol#L314-L318

## Description
The total asset value becomes incorrect after the `completeQueuedWithdrawals()` call concludes, since it doesn't reduce `restakedValidatorsETH`, but increases the ETH balance by the corresponding amount withdrawn:

### EigenPod.sol#L412-L420
```solidity
function withdrawRestakedBeaconChainETH(address recipient, uint256 amountWei) external onlyEigenPodManager {
    uint64 amountGwei = uint64(amountWei / GWEI_TO_WEI);
    amountWei = amountGwei * GWEI_TO_WEI;
    require(amountGwei <= restakedExecutionLayerGwei, InsufficientWithdrawableBalance());
    restakedExecutionLayerGwei -= amountGwei;
    emit RestakedBeaconChainETHWithdrawn(recipient, amountWei);
    // transfer ETH from pod to `recipient` directly
    Address.sendValue(payable(recipient), amountWei); // <<<
}
```
Also, total assets can be miscalculated and value removed from the Vault shares owners if `staker` in the structure is set to any address other than Vault's:

### DelegationManager.sol#L600
```solidity
shareManager.withdrawSharesAsTokens({
    staker: withdrawal.staker, // <<<
    strategy: withdrawal.strategies[i],
    token: tokens[i],
    shares: sharesToWithdraw
});
```

## Recommendation
Consider adding the initial value of ETH supplied for restaking corresponding to this exact withdrawal directly to function arguments, e.g., making it function `completeQueuedWithdrawals(withdrawal, receiveAsTokens, restakedETHRemoved)` and performing the update atomically:

### InstitutionalVault.sol#L314-L318
```solidity
EIGEN_DELEGATION_MANAGER.completeQueuedWithdrawals({
    withdrawals: withdrawals,
    tokens: tokens,
    receiveAsTokens: receiveAsTokens
});
+ $.restakedValidatorsETH -= restakedETHRemoved;
```
Also, as `staker` in the Withdrawal structure has to be the Vault address in order to keep the accounting consistent, consider controlling for this.

### Puffer Finance: 
Introducing a code like:
```solidity
// If we are dealing with ETH withdrawal that will transfer ETH to the vault
// We need to update the non-restaked validators ETH
if (receiveAsTokens[0]) {
    _getVaultStorage().restakedValidatorsETH -= SafeCast.toUint128(withdrawals[0].scaledShares[0]);
    emit RestakedValidatorsETHUpdated(_getVaultStorage().restakedValidatorsETH);
}
```
This would introduce another issue (DoS):
- Assume one restaking validator is started. (This means that the `restakedValidatorsETH = 32 ETH`).
- They earn 1 ETH of rewards and those rewards accumulate in the EigenPod.
- They shut down the validator & queue a 33 ETH withdrawal.

Now the `completeQueuedWithdrawal` can’t be finished because of the overflow/underflow issue. Since this is a permissioned, closed system, the issue of inaccurate exchange rates has already been documented and will be communicated to our clients and partners. Given this, along with the DoS attack scenario, we have decided not to implement the suggested change. Additionally, the system includes the `setValidatorsETH()` function, which allows the admin to centrally update the number of restaked and non-restaked validators’ ETH.

### Cantina Managed: 
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Puffer Institutional |
| Report Date | N/A |
| Finders | Hyh, Ladboy233, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Puffer-Spearbit-Security-Review-February-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Puffer-Spearbit-Security-Review-February-2025.pdf

### Keywords for Search

`vulnerability`

