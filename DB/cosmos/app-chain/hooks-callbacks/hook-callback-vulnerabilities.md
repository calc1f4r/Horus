---
protocol: generic
chain: cosmos
category: hooks_callbacks
vulnerability_type: hook_callback_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: hooks_callbacks_logic

primitives:
  - before_after
  - order_dependency
  - revert_propagation
  - reentrancy_via_hook

severity: medium
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - hooks_callbacks
  - staking
  - defi

language: go|solidity|rust
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Hooks Before After
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-05] L2 hooks don’t execute `ValidateBasic` on provided me | `reports/cosmos_cometbft_findings/m-05-l2-hooks-dont-execute-validatebasic-on-provided-messages.md` | MEDIUM | Code4rena |
| [M-26] ZRC20 Token Pause Check Bypass | `reports/cosmos_cometbft_findings/m-26-zrc20-token-pause-check-bypass.md` | MEDIUM | Code4rena |
| Staking and withdrawal operations might be blocked. | `reports/cosmos_cometbft_findings/staking-and-withdrawal-operations-might-be-blocked.md` | MEDIUM | Zokyo |

### Hooks Reentrancy Via Hook
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| bitcoin.waitForPayment function callback could be called mul | `reports/cosmos_cometbft_findings/bitcoinwaitforpayment-function-callback-could-be-called-multiple-times.md` | MEDIUM | OpenZeppelin |
| Potential Reentrancy Into Strategies | `reports/cosmos_cometbft_findings/potential-reentrancy-into-strategies.md` | MEDIUM | ConsenSys |

---

# Hook Callback Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Hook Callback Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Hooks Before After](#1-hooks-before-after)
2. [Hooks Reentrancy Via Hook](#2-hooks-reentrancy-via-hook)

---

## 1. Hooks Before After

### Overview

Implementation flaw in hooks before after logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: MEDIUM: 3.

> **Key Finding**: The L1 deposit function allows a depositor to send a signed payload to be executed along with the deposited tokens. However, there is a bug in the code that can cause issues when executing Cosmos Messages. This is because a step that is usually executed by `BaseApp` is missing in the `msg` loop. Thi

### Vulnerability Description

#### Root Cause

Implementation flaw in hooks before after logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies hooks before after in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to hooks operations

### Vulnerable Pattern Examples

**Example 1: [M-05] L2 hooks don’t execute `ValidateBasic` on provided messages** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-05-l2-hooks-dont-execute-validatebasic-on-provided-messages.md`
```go
File: deposit.go
54: 	for _, msg := range tx.GetMsgs() {
55: 		handler := k.router.Handler(msg)
56: 		if handler == nil {
57: 			reason = fmt.Sprintf("Unrecognized Msg type: %s", sdk.MsgTypeURL(msg))
58: 			return
59: 		}
60:
61: 		_, err = handler(cacheCtx, msg)
62: 		if err != nil {
63: 			reason = fmt.Sprintf("Failed to execute Msg: %s", err)
64: 			return
65: 		}
66: 	}
```

**Example 2: [M-26] ZRC20 Token Pause Check Bypass** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-26-zrc20-token-pause-check-bypass.md`
```go
go test ./x/crosschain/keeper/gas_payment_test.go -run TestZRC20PauseBypassTry2 -v
```

**Example 3: Staking and withdrawal operations might be blocked.** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/staking-and-withdrawal-operations-might-be-blocked.md`
```
// Vulnerable pattern from Radiant Capital:
**Description**

MultiFee Distribution.sol: _stake(), line 644,_withdrawExpiredLocks For(), line 1134. 
During staking and withdrawing funds, a 'beforeLockUpdate hook is called on the Incentives Controller. This hook checks if a user is to be disqualified. For this purpose, the contract performs another external call to Disqualifier.sol, function processUser(). Inside this function, the contract calls an internal function of Disqualifier, _processUserWithBounty(). It has a "require" which will r
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in hooks before after logic allows exploitation through missing validation, inco
func secureHooksBeforeAfter(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 3 audit reports
- **Severity Distribution**: MEDIUM: 3
- **Affected Protocols**: Radiant Capital, ZetaChain, Initia
- **Validation Strength**: Moderate (2 auditors)

---

## 2. Hooks Reentrancy Via Hook

### Overview

Implementation flaw in hooks reentrancy via hook logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: MEDIUM: 2.

> **Key Finding**: The bug report is about the waitForPayment function of the bitcoin.js module in the fundraiser-lib. It states that the function does not handle requests that take longer than 6 seconds correctly, and it could call the callback multiple times. It is suggested that a reentrancy guard should be added, 

### Vulnerability Description

#### Root Cause

Implementation flaw in hooks reentrancy via hook logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies hooks reentrancy via hook in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to hooks operations

### Vulnerable Pattern Examples

**Example 1: bitcoin.waitForPayment function callback could be called multiple times** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/bitcoinwaitforpayment-function-callback-could-be-called-multiple-times.md`
```
// Vulnerable pattern from COSMOS Fundraiser Audit:
[waitForPayment function of bitcoin.js module in fundraiser-lib](https://github.com/cosmos/fundraiser-lib/blob/426425dfc296060a9b87830e69e19ae8a6d444c0/src/bitcoin.js#L60) doesn’t handle correctly requests that take longer than 6 seconds, and could call the callback multiple times. Consider adding a reentrancy guard, as shown on this sample code:


 [**maraoz/fundraiser-lib**  

*fundraiser-lib – JS module for participating in Cosmos Fundraiser* github.com](https://github.com/maraoz/fundraiser-l
```

**Example 2: Potential Reentrancy Into Strategies** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/potential-reentrancy-into-strategies.md`
```solidity
function withdraw(address depositor, IERC20 token, uint256 amountShares)
    external
    virtual
    override
    onlyWhenNotPaused(PAUSED\_WITHDRAWALS)
    onlyStrategyManager
{
    require(token == underlyingToken, "StrategyBase.withdraw: Can only withdraw the strategy token");
    // copy `totalShares` value to memory, prior to any decrease
    uint256 priorTotalShares = totalShares;
    require(
        amountShares <= priorTotalShares,
        "StrategyBase.withdraw: amountShares must be less than or equal to totalShares"
    );

    // Calculate the value that `totalShares` will decrease to as a result of the withdrawal
    uint256 updatedTotalShares = priorTotalShares - amountShares;
    // check to avoid edge case where share rate can be massively inflated as a 'griefing' sort of attack
    require(updatedTotalShares >= MIN\_NONZERO\_TOTAL\_SHARES || updatedTotalShares == 0,
        "StrategyBase.withdraw: updated totalShares amount would be nonzero but below MIN\_NONZERO\_TOTAL\_SHARES");
    // Actually decrease the `totalShares` value
    totalShares = updatedTotalShares;

    /\*\*
 \* @notice calculation of amountToSend \*mirrors\* `sharesToUnderlying(amountShares)`, but is different since the `totalShares` has already
 \* been decremented. Specifically, notice how we use `priorTotalShares` here instead of `totalShares`.
 \*/
    uint256 amountToSend;
    if (priorTotalShares == amountShares) {
        amountToSend = \_tokenBalance();
    } else {
        amountToSend = (\_tokenBalance() \* amountShares) / priorTotalShares;
    }

    underlyingToken.safeTransfer(depositor, amountToSend);
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in hooks reentrancy via hook logic allows exploitation through missing validatio
func secureHooksReentrancyViaHook(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 2 audit reports
- **Severity Distribution**: MEDIUM: 2
- **Affected Protocols**: EigenLabs — EigenLayer, COSMOS Fundraiser Audit
- **Validation Strength**: Moderate (2 auditors)

---

## Detection Patterns

### Automated Detection
```
# Hooks Before After
grep -rn 'hooks|before|after' --include='*.go' --include='*.sol'
# Hooks Reentrancy Via Hook
grep -rn 'hooks|reentrancy|via|hook' --include='*.go' --include='*.sol'
```

## Keywords

`after`, `appchain`, `before`, `bypass`, `callback`, `called`, `check`, `cosmos`, `could`, `dependency`, `execute`, `function`, `hook`, `hooks`, `hooks callbacks`, `into`, `messages`, `might`, `multiple`, `operations`, `order`, `pause`, `potential`, `propagation`, `provided`, `reentrancy`, `revert`, `staking`, `strategies`, `times`
