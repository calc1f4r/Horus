---
# Core Classification (Required)
protocol: generic
chain: everychain
category: restaking
vulnerability_type: slashing_mechanism

# Attack Vector Details (Required)
attack_type: logical_error|state_manipulation|economic_exploit
affected_component: slashing_handler|penalty_distribution|accounting|vault_configuration

# Technical Primitives (Required)
primitives:
  - slashing
  - slashing_handler
  - slash_store
  - over_slashing
  - under_slashing
  - slashing_factor
  - penalty_distribution
  - protocol_insolvency
  - lido_slashing
  - lst_rebasing
  - validator_penalty
  - native_vault

# Impact Classification (Required)
severity: high|medium
impact: fund_loss|insolvency|dos|unfair_distribution
exploitability: 0.5
financial_impact: high

# Context Tags
tags:
  - defi
  - restaking
  - eigenlayer
  - karak
  - slashing
  - validator
  - lst
  - steth
  - insolvency

# Version Info
language: solidity
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Unslashable Vault Creation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Operator Creates Silently Unslashable NativeVault | `reports/eigenlayer_findings/h-02-the-operator-can-create-a-nativevault-that-can-be-silently-unslashable.md` | HIGH | Code4rena |
| Changing slashingHandler DoSes Slashing | `reports/eigenlayer_findings/m-01-changing-the-slashinghandler-for-nativevaults-will-dos-slashing.md` | MEDIUM | Code4rena |

### Over-Slashing / Under-Slashing
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Slashing NativeVault Locks ETH (Double-Reduction) | `reports/eigenlayer_findings/h-01-slashing-nativevault-will-lead-to-locked-eth-for-the-users.md` | HIGH | Code4rena |
| Node Operator Slashed for Full Duration | `reports/eigenlayer_findings/h-03-node-operator-is-getting-slashed-for-full-duration-even-though-rewards-are-.md` | HIGH | Code4rena |
| Staker Bypasses Slashing via Over-Commitment | `reports/eigenlayer_findings/m-01-a-staker-with-verified-over-commitment-can-potentially-bypass-slashing-comp.md` | MEDIUM | Code4rena |

### Slashing Accounting & Report Issues
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Incorrect reportRecoveredEffectiveBalance | `reports/eigenlayer_findings/incorrect-accounting-of-reportrecoveredeffectivebalance-can-prevent-report-from-.md` | HIGH | Cyfrin |
| Snapshot DoS from Combined Slashing + Penalty | `reports/eigenlayer_findings/m-02-a-snapshot-may-face-a-permanent-dos-if-both-a-slashing-event-occurs-in-the-.md` | MEDIUM | Code4rena |
| Restaking Funds Should Be Un-Slashed Back | `reports/eigenlayer_findings/on-restaking-funds-should-be-unslashed-back.md` | MEDIUM | Hans |

### Protocol Insolvency from LST Slashing
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Insolvency from Lido Slashing (Nexus) | `reports/eigenlayer_findings/m-03-potential-protocol-insolvency-due-to-lido-slashing-events.md` | MEDIUM | Pashov Audit Group |
| Insolvency from Lido Slashing (Puffer) | `reports/eigenlayer_findings/possibly-protocol-insolvency-during-a-lido-slashing-event-once-redeemwithdraw-is.md` | MEDIUM | Immunefi |

### Unfair Penalty Distribution
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Slashing Penalty Paid by First Withdrawal Cohort | `reports/eigenlayer_findings/m-10-slashing-penalty-is-unfairly-paid-by-a-subset-of-users-if-a-deficit-is-accu.md` | MEDIUM | Sherlock |
| Slashing During Calculator Deployment Shows Bad APR | `reports/eigenlayer_findings/m-18-slashing-during-lstcalculatorbasesol-deployment-can-show-bad-apr-for-months.md` | MEDIUM | Sherlock |

---

# Restaking Slashing Mechanism Vulnerabilities — Comprehensive Database

**A Pattern-Matching Guide for Slashing Security in Restaking Protocols**

---

## Table of Contents

1. [Unslashable Vault Creation](#1-unslashable-vault-creation)
2. [Over-Slashing and Double-Reduction](#2-over-slashing-and-double-reduction)
3. [Slashing Bypass via Timing](#3-slashing-bypass-via-timing)
4. [Protocol Insolvency from LST Slashing](#4-protocol-insolvency-from-lst-slashing)
5. [Unfair Penalty Distribution](#5-unfair-penalty-distribution)
6. [Slashing Accounting Errors](#6-slashing-accounting-errors)

---

## 1. Unslashable Vault Creation

### Overview

Operators can create NativeVaults that are permanently unslashable by manipulating the `slashStore` address at deployment time, or vaults become unslashable when the admin updates slashing handler addresses after deployment.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/h-02-the-operator-can-create-a-nativevault-that-can-be-silently-unslashable.md` (Karak - Code4rena)
> - `reports/eigenlayer_findings/m-01-changing-the-slashinghandler-for-nativevaults-will-dos-slashing.md` (Karak - Code4rena)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **the `NativeVault.slashAssets()` function checks `slashingHandler == self.slashStore`**, but these values can diverge. `slashStore` is set at initialization via `extraData`, while `assetSlashingHandlers` is managed separately in `Core`. Either the operator sets a malicious `slashStore` at init, or the admin updates `assetSlashingHandlers` post-deployment, creating a permanent mismatch.

**Frequency:** Moderate (2/12 reports)
**Validation:** Strong — Code4rena with 12 independent finders

### Vulnerable Pattern Examples

**Example 1: Operator Deploys with Mismatched slashStore** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-02-the-operator-can-create-a-nativevault-that-can-be-silently-unslashable.md`
```solidity
// ❌ VULNERABLE: Operator controls extraData containing slashStore
function deployVaults(VaultLib.Config[] calldata vaultConfigs) external {
    // Operator provides vaultConfigs with arbitrary extraData
    vaultConfigs[0] = VaultLib.Config({
        asset: address(0), // Native ETH
        extraData: abi.encode(
            manager,
            ARBITRARY_ADDRESS, // slashStore — set by operator!
            nativeNodeImpl
        )
    });
}

// In NativeVault.slashAssets():
function slashAssets(uint256 amount, address slashingHandler) external onlyCore {
    // BUG: slashingHandler comes from Core.assetSlashingHandlers
    // but self.slashStore comes from operator-controlled extraData
    if (slashingHandler != self.slashStore) {
        revert NotSlashStore(); // Always reverts if addresses don't match!
    }
}
```

**Example 2: Admin Update Creates Mismatch** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/m-01-changing-the-slashinghandler-for-nativevaults-will-dos-slashing.md`
```solidity
// ❌ VULNERABLE: Admin can update handler, breaking existing vaults
function updateAssetSlashingHandler(address asset, address handler) external onlyOwner {
    assetSlashingHandlers[asset] = handler; // Updates in Core
    // BUG: NativeVault.slashStore remains at old value
    // All existing NativeVaults become unslashable
    // Restoring old handler to fix old vaults breaks new vaults
}
```

### Impact Analysis

#### Technical Impact
- Operator creates vault that can never be slashed (permanently)
- Undermines entire restaking security model — operator faces zero risk
- Admin actions (updating handlers) break existing vaults

#### Business Impact
- Malicious operators can misbehave in AVS tasks without consequence
- Total loss of slashing guarantee — core EigenLayer/Karak value proposition
- **Financial impact observed:** Entire slashed amount (any amount deposited) unrecoverable

### Secure Implementation

```solidity
// ✅ SECURE: Verify slashStore matches at deployment time
function deployVaults(VaultLib.Config[] calldata vaultConfigs) external {
    for (uint i = 0; i < vaultConfigs.length; i++) {
        if (vaultConfigs[i].asset == address(0)) {
            (, address slashStore, ) = abi.decode(
                vaultConfigs[i].extraData, (address, address, address)
            );
            require(
                slashStore == assetSlashingHandlers[address(0)],
                "SlashStore must match handler"
            );
        }
    }
}

// ✅ SECURE: Allow slashStore updates via callable function
function updateSlashStore(address newSlashStore) external onlyCore {
    self.slashStore = newSlashStore;
}
```

### Detection Patterns

#### Audit Checklist
- [ ] Can vault deployers (operators) control slashing-related addresses?
- [ ] Does `slashAssets()` compare two independently-configurable addresses?
- [ ] Can admin updates to slashing handlers break existing vaults?
- [ ] Is there a mechanism to update vault-side slashing addresses after deployment?

---

## 2. Over-Slashing and Double-Reduction

### Overview

When slashing occurs across multiple systems (protocol-level slash + validator penalty), double-counting of the reduction creates over-slashing where users lose more than intended. Conversely, using full staking duration instead of reward cycle duration creates disproportionate penalties.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/h-01-slashing-nativevault-will-lead-to-locked-eth-for-the-users.md` (Karak - Code4rena)
> - `reports/eigenlayer_findings/h-03-node-operator-is-getting-slashed-for-full-duration-even-though-rewards-are-.md` (GoGoPool - Code4rena)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **slashing accounting applies reductions in multiple places without coordination**. After `_transferToSlashStore` reduces `totalRestakedETH`, the subsequent `validateSnapshotProofs` applies a *second* reduction based on the full validator balance delta, effectively double-counting the slash amount.

**Frequency:** Moderate (2/12 reports)
**Validation:** Strong — Code4rena with multiple independent finders

### Vulnerable Pattern Examples

**Example 1: Double-Reduction Creates Locked ETH** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-01-slashing-nativevault-will-lead-to-locked-eth-for-the-users.md`
```solidity
// ❌ VULNERABLE: Two independent reductions for the same slash event
function slashAssets(uint256 slashAmount) external onlyCore {
    // First reduction: transfer to slash store
    _transferToSlashStore(slashAmount);
    totalRestakedETH -= slashAmount; // -3 ETH
}

function validateSnapshotProofs(bytes[] proofs) external {
    uint256 balanceDelta = prevBalance - currentBalance; // 32 - 29 = 3 ETH
    // Second reduction: snapshot records the same 3 ETH drop
    totalRestakedETH -= balanceDelta; // -3 ETH AGAIN
    
    // Total reduction: 6 ETH instead of 3 ETH
    // Alice had 32 ETH, slashed 3 ETH, should get 29 ETH
    // But withdrawableCreditedNodeETH = 32 - 6 = 26 ETH → 3 ETH locked forever
}
```

**Example 2: Full Duration Slashing Instead of Cycle Duration** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-03-node-operator-is-getting-slashed-for-full-duration-even-though-rewards-are-.md`
```solidity
// ❌ VULNERABLE: Uses full staking duration for penalty calculation
function getExpectedAVAXRewardsAmt(uint256 duration, uint256 avaxAmt) public view returns (uint256) {
    // duration = full staking period (e.g., 365 days)
    // But rewards are distributed in 14-day cycles!
    return (avaxAmt.mulWadDown(rate) * duration) / 365 days;
    // 365-day staker: penalty = ~100 ETH
    // 14-day staker: penalty = ~3.8 ETH
    // Same infraction → 26x different penalty
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Single source of truth for slashing amount
function slashAssets(uint256 slashAmount) external onlyCore {
    _transferToSlashStore(slashAmount);
    totalRestakedETH -= slashAmount;
    // Mark that snapshot proofs should NOT double-count
    slashedAmounts[currentSnapshot] += slashAmount;
}

function validateSnapshotProofs(bytes[] proofs) external {
    uint256 balanceDelta = prevBalance - currentBalance;
    uint256 alreadySlashed = slashedAmounts[currentSnapshot];
    // Only reduce by the NET difference not already accounted for
    uint256 additionalReduction = balanceDelta > alreadySlashed ? balanceDelta - alreadySlashed : 0;
    totalRestakedETH -= additionalReduction;
}
```

### Detection Patterns

#### Audit Checklist
- [ ] Are there multiple code paths that reduce balance/shares for the same slashing event?
- [ ] Is the penalty calculation based on the actual reward cycle, not full staking duration?
- [ ] Does burn amount exceed available shares in any scenario (zero-balance after combined events)?
- [ ] Can over-slash result in more shares burned than exist, causing revert?

---

## 3. Slashing Bypass via Timing

### Overview

Stakers can bypass slashing entirely by exploiting timing: being in a state with 0 withdrawable shares when the slash occurs, then recovering full shares after the operator is unfrozen.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/m-01-a-staker-with-verified-over-commitment-can-potentially-bypass-slashing-comp.md` (EigenLayer - Code4rena)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **over-commitment proofs reduce shares to 0, and slashing 0 shares has no effect**. After the operator is unfrozen, the staker exits the beacon chain and gets full shares credited back — completely bypassing the slash.

**Frequency:** Rare (1/12 reports)
**Validation:** Moderate — 4 finders (Code4rena)

### Vulnerable Pattern Examples

**Example 1: Over-Commitment as Slashing Shield** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/m-01-a-staker-with-verified-over-commitment-can-potentially-bypass-slashing-comp.md`
```solidity
// ❌ VULNERABLE: Slash has no effect on 0-share staker
// Step 1: Staker has shares. An over-commitment proof reduces them to 0.
overCommitmentProof(staker); // shares → 0

// Step 2: Operator gets slashed — staker's 0 shares are "slashed" to... still 0
slashOperator(operator); // No effect on staker with 0 shares

// Step 3: Operator unfrozen. Staker exits beacon chain.
exitValidator(staker); // Full shares credited back
// Result: staker completely bypassed slashing
```

### Secure Implementation

```solidity
// ✅ SECURE: Track over-committed amounts and include in slash calculation
function slashShares(address staker, uint256 amount) external {
    uint256 activeShares = stakerShares[staker];
    uint256 overCommittedShares = overCommittedAmounts[staker]; // Track this!
    
    // Slash proportionally including over-committed amount
    uint256 totalShares = activeShares + overCommittedShares;
    uint256 slashProportion = amount * 1e18 / totalOperatorShares;
    
    // Record slash against over-committed shares too
    overCommittedSlashing[staker] += overCommittedShares * slashProportion / 1e18;
}
```

---

## 4. Protocol Insolvency from LST Slashing

### Overview

Protocols using rebasing LSTs (particularly stETH) assume that the underlying balance only increases. When Lido validators are slashed, the stETH balance decreases (negative rebase), but the protocol's accounting doesn't handle this, creating phantom assets that inflate `totalAssets()`.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/m-03-potential-protocol-insolvency-due-to-lido-slashing-events.md` (Nexus - Pashov)
> - `reports/eigenlayer_findings/possibly-protocol-insolvency-during-a-lido-slashing-event-once-redeemwithdraw-is.md` (Puffer - Immunefi)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **reward tracking functions floor negative returns at zero** (`max(0, balance - strategy)`), and withdrawal accounting assumes `received == requested`. During a Lido slashing event, stETH balance decreases, but `getRewards()` returns 0 instead of negative. The share price never adjusts downward.

**Frequency:** Moderate (3/12 reports, including withdrawal interaction)
**Validation:** Moderate — 2 independent auditors (Pashov, Immunefi)

### Vulnerable Pattern Examples

**Example 1: Negative Rewards Not Tracked** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/m-03-potential-protocol-insolvency-due-to-lido-slashing-events.md`
```solidity
// ❌ VULNERABLE: Only tracks positive returns — negative slashing is invisible
function getRewards(address receiver) public view returns (uint256) {
    uint256 currentBalance = IERC20(stETH).balanceOf(receiver);
    uint256 strategyBalance = strategies[receiver].deposited;
    
    if (currentBalance > strategyBalance) {
        return currentBalance - strategyBalance; // Only positive returns
    } else {
        return 0; // BUG: Slashing event completely hidden
    }
}
// rewardsClaimed only increases → share price only increases → insolvency
```

**Example 2: Withdrawal Receives Less Than Requested** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/possibly-protocol-insolvency-during-a-lido-slashing-event-once-redeemwithdraw-is.md`
```solidity
// ❌ VULNERABLE: Adjusts by received, not by requested
receive() external payable {
    if ($.isLidoWithdrawal) {
        $.lidoLockedETH -= msg.value; // Actual received amount
        // If Lido slashing: requested 1000 ETH, received 900 ETH
        // lidoLockedETH reduced by 900, but should be reduced by 1000
        // 100 ETH phantom remains → totalAssets() inflated by 100 ETH
    }
}
```

### Impact Analysis

#### Technical Impact
- `totalAssets()` permanently inflated after any LST slashing event
- Share price only goes up, never down → protocol issues more shares than backed
- Bank run scenario: first withdrawers get full value, later withdrawers get nothing

#### Business Impact
- Protocol insolvency proportional to slashing severity
- Users race to withdraw → cascading failures
- **Financial impact observed:** 10% Lido slash → entire LRT protocol insolvent

### Secure Implementation

```solidity
// ✅ SECURE: Track negative rewards (slashing events)
function getRewards(address receiver) public view returns (int256) {
    uint256 currentBalance = IERC20(stETH).balanceOf(receiver);
    uint256 strategyBalance = strategies[receiver].deposited;
    return int256(currentBalance) - int256(strategyBalance); // Can be negative!
}

function _updateSharePrice() internal {
    int256 rewards = getRewards(address(this));
    if (rewards < 0) {
        // Reduce share price to reflect slashing
        totalAssets -= uint256(-rewards);
        emit SlashingLossRecorded(uint256(-rewards));
    }
}
```

---

## 5. Unfair Penalty Distribution

### Overview

Slashing penalties that should be socialized across all stakers are instead absorbed by whichever users interact with the protocol first after the slashing event. This creates unfair burden distribution.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/m-10-slashing-penalty-is-unfairly-paid-by-a-subset-of-users-if-a-deficit-is-accu.md` (Rio Network - Sherlock)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **settlement functions use `balanceBefore`/`balanceAfter` patterns** that capture any accumulated deficit. The first cohort to settle an epoch absorbs the entire slashing deficit rather than it being spread proportionally.

**Frequency:** Moderate (3/12 reports)
**Validation:** Moderate — 3 auditors

### Vulnerable Pattern Examples

**Example 1: First Settlement Absorbs Entire Deficit** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/m-10-slashing-penalty-is-unfairly-paid-by-a-subset-of-users-if-a-deficit-is-accu.md`
```solidity
// ❌ VULNERABLE: First settler absorbs ALL slashing deficit
function settleEpochFromEigenLayer(Withdrawal[] calldata withdrawals) external {
    uint256 balanceBefore = asset.balanceOf(address(this));
    
    delegationManager.completeQueuedWithdrawal(withdrawals, ...);
    
    uint256 assetsReceived = asset.balanceOf(address(this)) - balanceBefore;
    // BUG: If EigenPodManager has deficit from slashing,
    // assetsReceived = 0 for first settlement (entire deficit absorbed)
    // Second settlement gets full amount
    
    epochSettlements[epoch].amountReceived = assetsReceived;
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Spread deficit proportionally across all users/epochs
function settleEpochFromEigenLayer(Withdrawal[] calldata withdrawals) external {
    uint256 expectedAssets = epochSettlements[epoch].expectedAmount;
    
    delegationManager.completeQueuedWithdrawal(withdrawals, ...);
    
    uint256 actualReceived = asset.balanceOf(address(this)) - balanceBefore;
    
    if (actualReceived < expectedAssets) {
        // Spread deficit across all active epochs proportionally
        uint256 deficit = expectedAssets - actualReceived;
        _socializeDeficit(deficit);
    }
}
```

---

## 6. Slashing Accounting Errors

### Overview

Accounting errors in slashing-related state variables cause cascading failures: report finalization blocked, snapshot DoS, and asymmetric slash/unslash logic in restake flows.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/incorrect-accounting-of-reportrecoveredeffectivebalance-can-prevent-report-from-.md` (Casimir - Cyfrin)
> - `reports/eigenlayer_findings/m-02-a-snapshot-may-face-a-permanent-dos-if-both-a-slashing-event-occurs-in-the-.md` (Karak - Code4rena)

### Vulnerable Pattern Examples

**Example 1: Missing Recovery in Reward Accounting** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/incorrect-accounting-of-reportrecoveredeffectivebalance-can-prevent-report-from-.md`
```solidity
// ❌ VULNERABLE: Slashing reduces balance metrics but recovery doesn't increase them
function finalizeReport() external {
    // rewardStakeRatioSum was reduced during slashing event
    // reportRecoveredEffectiveBalance (collateral recovery) NOT added back
    // Arithmetic underflow on: latestActiveBalanceAfterFee - totalPenalties
    // REVERTS: new reports can never finalize → system halted
}
```

**Example 2: Over-Burn in Combined Slash + Penalty** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/m-02-a-snapshot-may-face-a-permanent-dos-if-both-a-slashing-event-occurs-in-the-.md`
```solidity
// ❌ VULNERABLE: Burn exceeds available shares after combined events
function _decreaseBalance(address staker, uint256 burnAmount) internal {
    // If Karak slashing reduced assets AND validator fully penalized:
    // burnAmount > staker's remaining shares → revert
    // Permanent snapshot DoS — staker continues receiving rewards
    _burn(staker, burnAmount); // REVERTS if insufficient balance
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Include recovery in reward calculations
function finalizeReport() external {
    uint256 netPenalty = totalPenalties - reportRecoveredEffectiveBalance;
    uint256 adjustedBalance = latestActiveBalanceAfterFee - netPenalty;
    // No underflow — recovery amount offsets penalties
}

// ✅ SECURE: Cap burns at available balance
function _decreaseBalance(address staker, uint256 burnAmount) internal {
    uint256 available = balanceOf(staker);
    uint256 actualBurn = burnAmount > available ? available : burnAmount;
    _burn(staker, actualBurn);
    if (burnAmount > available) {
        emit SlashingLossUnrecoverable(staker, burnAmount - available);
    }
}
```

---

### Prevention Guidelines

#### Development Best Practices
1. Validate slashing handler addresses at vault deployment time, not just at slash execution
2. Use a single source of truth for slashing accounting — avoid double-reduction
3. Track over-committed amounts and include them in slash calculations
4. Handle negative LST rebases explicitly (don't floor at zero)
5. Socialize slashing deficits proportionally across all stakers
6. Cap burn operations at available balance to prevent revert-based DoS
7. Include collateral recovery in reward accounting formulas
8. Use reward cycle duration (not full staking duration) for penalty calculations

#### Testing Requirements
- Unit tests for: combined protocol + validator slashing, over-commitment timing attack, negative stETH rebase
- Integration tests for: vault deployment with mismatched handlers, settlement after slashing deficit, snapshot after combined events
- Fuzzing targets: slashing factor calculations, penalty duration formulas, negative rebase scenarios

### Keywords for Search

> These keywords enhance vector search retrieval:

`slashing`, `slash`, `slashAssets`, `slashStore`, `slashingHandler`, `unslashable`, `over-slashing`, `under-slashing`, `penalty`, `validator penalty`, `slashing factor`, `beaconChainSlashingFactor`, `protocol insolvency`, `lido slashing`, `stETH rebase`, `negative rebase`, `phantom assets`, `double counting`, `double reduction`, `penalty distribution`, `deficit socialization`, `restaking`, `eigenlayer`, `karak`, `native vault`, `operator`, `AVS`, `over-commitment`, `GoGoPool`, `Renzo`, `Puffer`, `Nexus`, `Rio`, `Casimir`

### Related Vulnerabilities

- [Restaking Withdrawal Vulnerabilities](RESTAKING_WITHDRAWAL_VULNERABILITIES.md)
- [EigenPod Beacon Chain Verification](EIGENPOD_BEACON_CHAIN_VULNERABILITIES.md)
- [LRT Share Accounting Errors](LRT_SHARE_ACCOUNTING_VULNERABILITIES.md)
