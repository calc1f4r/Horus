---
# Core Classification
protocol: Kinetiq LST Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64005
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-November-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-November-2025.pdf
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
finders_count: 4
finders:
  - 0xRajeev
  - Kamensec
  - Optimum
  - Rvierdiiev
---

## Vulnerability Title

L1 Account Activation Not Verified Before CoreWriter Actions

### Overview

See description below for full details.

### Original Finding Content

## Severity: Low Risk

## Context
(No context files were provided by the reviewer)

## Description
HyperCore accounts must be activated before they can execute CoreWriter actions such as staking deposits. According to HyperLiquid documentation, activation occurs when an account receives its first spot transfer from an already-activated sender, which charges a 1 USDC activation fee.

The `StakingManager.stake()` function calls `_distributeStake()` with `OperationType.UserDeposit`, which performs two L1 operations without verifying the StakingManager's L1 account is activated:

```solidity
// lib/lst/src/StakingManager.sol:249
function stake() external payable nonReentrant whenNotPaused returns (uint256 kHYPEAmount) {
    // ... validation ...
    kHYPE.mint(msg.sender, kHYPEAmount);
    _distributeStake(msg.value, OperationType.UserDeposit); // No activation check
    stakingAccountant.recordStake(msg.value);
}
```

Within `_distributeStake()` for `UserDeposit`:

```solidity
// lib/lst/src/StakingManager.sol:482-490
// 1. Move HYPE from EVM to spot balance on L1
(bool success,) = payable(L1_HYPE_CONTRACT).call{value: amount}("");
require(success, "Failed to send HYPE to L1");
// 2. Move from spot balance to staking balance (CoreWriter action)
uint256 truncatedAmount = _convertTo8Decimals(amount, false);
L1Write.sendCDeposit(uint64(truncatedAmount)); // Requires activated account!
// 3. Queue the delegation operation
_queueL1Operation(validator, truncatedAmount, operationType);
```

Then `L1_HYPE_CONTRACT.call{value: amount}` is executed, which triggers `CoreExecution.executeNativeTransfer()` that has the `initAccountWithToken` modifier. However, this modifier calls `_initializeAccount()` which checks if the account already exists on Core:

```solidity
// hyper-evm-lib/test/simulation/hyper-core/CoreState.sol:183-190
RealL1Read.CoreUserExists memory coreUserExists = RealL1Read.coreUserExists(_account);
if (!coreUserExists.exists && !force) {
    return; // Early return - does NOT activate!
}
_initializedAccounts[_account] = true;
account.activated = true;
```

If `coreUserExists` returns false (account never received a spot transfer), the function returns early without activating. The HYPE then goes to latent balance instead of usable spot balance:

```solidity
// hyper-evm-lib/test/simulation/hyper-core/CoreExecution.sol:51-55
if (_accounts[from].activated) {
    _accounts[from].spot[HYPE_TOKEN_INDEX] += (value / 1e10).toUint64();
} else {
    _latentSpotBalance[from][HYPE_TOKEN_INDEX] += (value / 1e10).toUint64(); // Unusable!
}
```

The subsequent `L1Write.sendCDeposit()` call attempts to move funds from spot balance to staking balance. CoreWriter actions from unactivated accounts fail silently - the EVM transaction succeeds but the L1 operation is not executed (guarded by `whenActivated` modifier which returns early).

## Impact Explanation
If the StakingManager's L1 account is not activated before the first staking operation:
1. Users call `stake()` and receive kHYPE tokens (EVM state updated).
2. HYPE is sent to L1 but lands in latent balance (not usable spot balance).
3. `sendCDeposit()` silently fails (account not activated).
4. `sendTokenDelegate()` silently fails (account not activated).
5. **Result:** Users hold kHYPE backed by HYPE that is stuck in latent balance and never actually staked.

This creates unbacked LST shares and in some cases underlying reverts during market launch if minimum hype balances are insufficient.

## Likelihood Explanation
Low - the deployment script provides an option to activate the account by sending USDC, and operators are expected to follow proper initialization procedures. However, this is an optional step with no on-chain enforcement, relying entirely on off-chain operational discipline.

## Recommendation
Add the `coreUserExists` precompile to `L1Read.sol` and verify account activation before the first CoreWriter action.

## Kinetiq
Acknowledged. Will add into deploy scripts for our markets launch.

## Spearbit
Acknowledged. Be cautious in permissionless case we might need something in a factory contract that checks these things if they use some non-standard staking manager contract.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Kinetiq LST Protocol |
| Report Date | N/A |
| Finders | 0xRajeev, Kamensec, Optimum, Rvierdiiev |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-November-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Kinetiq-Spearbit-Security-Review-November-2025.pdf

### Keywords for Search

`vulnerability`

