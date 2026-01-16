---
# Core Classification (Required)
protocol: generic
chain: everychain
category: token
vulnerability_type: erc20_token_integration

# Attack Vector Details (Required)
attack_type: data_manipulation|economic_exploit|logical_error|reentrancy
affected_component: token_transfer|approval|balance|mint_burn|decimals

# Token-Specific Fields
token_standard: erc20|erc777|erc4626|rebasing|fee_on_transfer
token_attack_vector: transfer|approval|balance_manipulation|inflation|blacklist|reentrancy

# Technical Primitives (Required)
primitives:
  - transfer
  - transferFrom
  - approve
  - allowance
  - balanceOf
  - totalSupply
  - decimals
  - mint
  - burn
  - safeTransfer
  - safeTransferFrom
  - safeApprove

# Impact Classification (Required)
severity: critical|high|medium|low
impact: fund_loss|dos|manipulation|accounting_error|locked_funds
exploitability: 0.80
financial_impact: high

# Context Tags
tags:
  - defi
  - lending
  - dex
  - vault
  - staking
  - bridge
  - external_dependency

# Version Info
language: solidity
version: all
---

## References & Source Reports

> **For Agents**: Analysis based on 761+ vulnerability reports from Solodit. Read individual reports in `reports/erc20_token_findings/` for detailed context.

### Transfer Vulnerabilities (87 reports analyzed)
| Report | Path | Severity | Key Issue |
|--------|------|----------|-----------|
| Unchecked ERC20 Transfers | `reports/erc20_token_findings/h-01-unchecked-erc20-transfers-can-cause-lock-up.md` | HIGH | Missing return value check |
| ERC20 Return Values Not Checked | `reports/erc20_token_findings/m-07-erc20-return-values-not-checked.md` | MEDIUM | Silent transfer failures |
| Fee on Transfer Tokens | `reports/erc20_token_findings/fee-on-transfer-tokens-will-cause-users-to-lose-funds.md` | HIGH | Balance mismatch |
| Solmate SafeTransfer Code Size | `reports/erc20_token_findings/m-14-solmate-safetransfer-and-safetransferfrom-does-not-check-the-code-size-of-t.md` | MEDIUM | No contract existence check |

### Approval/Allowance Vulnerabilities (26 reports analyzed)
| Report | Path | Severity | Key Issue |
|--------|------|----------|-----------|
| Approve Front-Running | `reports/erc20_token_findings/approve-function-can-be-front-ran-resulting-in-token-theft.md` | MEDIUM | Race condition |
| Must Approve 0 First | `reports/erc20_token_findings/m-02-must-approve-0-first.md` | MEDIUM | USDT-like tokens |
| Decrease Allowance Issue | `reports/erc20_token_findings/decrease-allowance-when-it-is-already-set-a-non-zero-value.md` | MEDIUM | Non-standard behavior |

### Decimals Vulnerabilities (23 reports analyzed)
| Report | Path | Severity | Key Issue |
|--------|------|----------|-----------|
| Protocol Assumes 18 Decimals | `reports/erc20_token_findings/h-1-protocol-assumes-18-decimals-collateral.md` | HIGH | Precision errors |
| Claim Underflow Non-18 Decimals | `reports/erc20_token_findings/claim-will-underflow-and-revert-for-all-tokens-without-18-decimals.md` | MEDIUM | Arithmetic underflow |

### Fee-on-Transfer & Rebasing (100+ reports analyzed)
| Report | Path | Severity | Key Issue |
|--------|------|----------|-----------|
| Fee on Transfer Incompatibility | `reports/erc20_token_findings/m-01-incompatibility-with-fee-on-transferinflationarydeflationaryrebasing-tokens.md` | MEDIUM | Balance tracking |
| Contracts Don't Support Rebasing | `reports/erc20_token_findings/contracts-do-not-support-tokens-with-fees-or-rebasing-tokens.md` | MEDIUM | State inconsistency |
| Aave Rebasing Tokens | `reports/erc20_token_findings/h-05-aaves-share-tokens-are-rebasing-breaking-current-strategy-code.md` | HIGH | Interest loss |

### ERC777 Reentrancy (27 reports analyzed)
| Report | Path | Severity | Key Issue |
|--------|------|----------|-----------|
| ERC777 Reentrancy Attack | `reports/erc20_token_findings/1-erc777-re-entrancy-attack.md` | HIGH | tokensToSend hook |
| Buy Function Reentrancy | `reports/erc20_token_findings/h-01-reentrancy-in-buy-function-for-erc777-tokens-allows-buying-funds-with-consi.md` | HIGH | Fund drain |
| Withdraw Reentrancy | `reports/erc20_token_findings/m-04-erc777-reentrancy-when-withdrawing-can-be-used-to-withdraw-all-collateral.md` | MEDIUM | Collateral theft |

### Blacklist/Pausable Tokens (28 reports analyzed)
| Report | Path | Severity | Key Issue |
|--------|------|----------|-----------|
| USDC Blacklist DoS | `reports/erc20_token_findings/orderbook-denial-of-service-leveraging-blacklistable-tokens-like-usdc.md` | HIGH | Orderbook freeze |
| Borrower Blacklisted | `reports/erc20_token_findings/m-17-if-borrower-or-kicker-got-blacklisted-by-asset-contract-their-collateral-or.md` | MEDIUM | Frozen funds |
| Liquidation Blocked | `reports/erc20_token_findings/m-12-liquidations-will-revert-if-a-position-has-been-blacklisted-for-usdc.md` | MEDIUM | Protocol insolvency risk |

### Inflation/First Depositor Attacks (63+ reports analyzed)
| Report | Path | Severity | Key Issue |
|--------|------|----------|-----------|
| Share Value Inflation | `reports/erc20_token_findings/h-04-an-attacker-can-massively-inflate-the-share-value.md` | HIGH | First depositor exploit |
| Initial Mint Front-Run | `reports/erc20_token_findings/initial-mint-front-run-inflation-attack.md` | HIGH | LP token theft |
| First Vault Deposit Rounding | `reports/erc20_token_findings/first-vault-deposit-can-cause-excessive-rounding.md` | MEDIUM | Share manipulation |

---

# ERC20 Token Integration Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for ERC20 Token Security Audits**

**Analysis Based On: 761+ Vulnerability Reports**

---

## Table of Contents

1. [Transfer & TransferFrom Vulnerabilities](#1-transfer--transferfrom-vulnerabilities)
2. [Approval & Allowance Vulnerabilities](#2-approval--allowance-vulnerabilities)
3. [Decimals & Precision Vulnerabilities](#3-decimals--precision-vulnerabilities)
4. [Fee-on-Transfer Token Vulnerabilities](#4-fee-on-transfer-token-vulnerabilities)
5. [Rebasing Token Vulnerabilities](#5-rebasing-token-vulnerabilities)
6. [ERC777 Reentrancy Vulnerabilities](#6-erc777-reentrancy-vulnerabilities)
7. [Blacklist & Pausable Token Vulnerabilities](#7-blacklist--pausable-token-vulnerabilities)
8. [Inflation & First Depositor Attacks](#8-inflation--first-depositor-attacks)
9. [Balance & Supply Manipulation](#9-balance--supply-manipulation)
10. [Mint & Burn Vulnerabilities](#10-mint--burn-vulnerabilities)

---

## 1. Transfer & TransferFrom Vulnerabilities

### Overview

ERC20 token transfer operations are the most fundamental yet frequently vulnerable operations in DeFi protocols. Analysis of 87+ reports reveals consistent patterns where protocols fail to properly handle transfer return values, non-standard tokens, and edge cases.

> **📚 Source Reports for Deep Dive:**
> - `reports/erc20_token_findings/h-01-unchecked-erc20-transfers-can-cause-lock-up.md` (Reality Cards - Code4rena)
> - `reports/erc20_token_findings/m-07-erc20-return-values-not-checked.md` (Amun - Code4rena)
> - `reports/erc20_token_findings/m-14-solmate-safetransfer-and-safetransferfrom-does-not-check-the-code-size-of-t.md` (Bond Protocol - Sherlock)

### Vulnerability Description

#### Root Cause

The ERC20 standard specifies that `transfer()` and `transferFrom()` should return a boolean indicating success. However:
1. Some tokens (like USDT) don't return any value
2. Some tokens return `false` instead of reverting on failure
3. Some libraries (Solmate) don't check contract existence before calling

#### Attack Scenario

1. Protocol calls `token.transfer()` or `token.transferFrom()`
2. Transfer fails silently (returns `false` or no return value)
3. Protocol assumes transfer succeeded and updates internal state
4. Attacker exploits the state/balance mismatch to drain funds or cause DoS

### Vulnerable Pattern Examples

**Example 1: Unchecked Transfer Return Value** [HIGH]
> 📖 Reference: `reports/erc20_token_findings/h-01-unchecked-erc20-transfers-can-cause-lock-up.md`
```solidity
// ❌ VULNERABLE: Return value not checked - silent failure possible
function withdraw(uint256 amount) external {
    balances[msg.sender] -= amount;
    IERC20(token).transfer(msg.sender, amount);  // May silently fail!
}
```

**Example 2: Using Solmate Without Contract Check** [MEDIUM]
> 📖 Reference: `reports/erc20_token_findings/m-14-solmate-safetransfer-and-safetransferfrom-does-not-check-the-code-size-of-t.md`
```solidity
// ❌ VULNERABLE: Solmate doesn't check if token contract exists
import {SafeTransferLib} from "solmate/utils/SafeTransferLib.sol";

function deposit(address token, uint256 amount) external {
    // If token address has no code, this returns success without transferring
    SafeTransferLib.safeTransferFrom(ERC20(token), msg.sender, address(this), amount);
    balances[msg.sender] += amount;  // Balance updated but no tokens received!
}
```

**Example 3: Direct Transfer Without SafeERC20** [MEDIUM]
> 📖 Reference: `reports/erc20_token_findings/m-07-erc20-return-values-not-checked.md`
```solidity
// ❌ VULNERABLE: USDT returns no value, this will revert or misbehave
function sendTokens(address to, uint256 amount) external {
    bool success = IERC20(token).transfer(to, amount);
    require(success, "Transfer failed");  // USDT doesn't return bool!
}
```

**Example 4: TransferFrom Without Proper Handling** [HIGH]
```solidity
// ❌ VULNERABLE: No return value check, state updated regardless
function stake(uint256 amount) external {
    token.transferFrom(msg.sender, address(this), amount);
    stakedBalance[msg.sender] += amount;  // Updated even if transfer failed
    emit Staked(msg.sender, amount);
}
```

### Impact Analysis

#### Technical Impact
- Silent transfer failures cause state/balance mismatches
- Protocol accounting becomes corrupted
- Funds can be locked or stolen

#### Business Impact
- **Frequency**: Found in 87+ of 761 analyzed reports (11.4%)
- Direct fund loss for users or protocol
- Protocol can become insolvent
- Complete loss of user trust

#### Affected Scenarios
- Staking contracts accepting deposits
- Withdrawal functions in vaults
- Token bridges and transfers
- Reward distribution mechanisms

### Secure Implementation

**Fix 1: Use OpenZeppelin SafeERC20**
```solidity
// ✅ SECURE: SafeERC20 handles all edge cases
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

using SafeERC20 for IERC20;

function withdraw(uint256 amount) external {
    balances[msg.sender] -= amount;
    IERC20(token).safeTransfer(msg.sender, amount);
}

function deposit(uint256 amount) external {
    IERC20(token).safeTransferFrom(msg.sender, address(this), amount);
    balances[msg.sender] += amount;
}
```

**Fix 2: Manual Return Value Check with Low-Level Call**
```solidity
// ✅ SECURE: Handles tokens that don't return value
function safeTransfer(address token, address to, uint256 amount) internal {
    (bool success, bytes memory data) = token.call(
        abi.encodeWithSelector(IERC20.transfer.selector, to, amount)
    );
    require(success && (data.length == 0 || abi.decode(data, (bool))), "Transfer failed");
}
```

**Fix 3: Add Contract Existence Check for Solmate**
```solidity
// ✅ SECURE: Check contract exists before using Solmate
function deposit(address token, uint256 amount) external {
    require(token.code.length > 0, "Token contract does not exist");
    SafeTransferLib.safeTransferFrom(ERC20(token), msg.sender, address(this), amount);
    balances[msg.sender] += amount;
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: Direct .transfer() or .transferFrom() calls without SafeERC20
- Pattern 2: Using Solmate SafeTransferLib with user-supplied token addresses
- Pattern 3: Boolean return value check with require() on non-standard tokens
- Pattern 4: State changes before transfer completion
```

#### Audit Checklist
- [ ] Is SafeERC20 (OpenZeppelin) used for all token transfers?
- [ ] If using Solmate, is contract existence checked for dynamic tokens?
- [ ] Are state changes made before or after the transfer call?
- [ ] Does the protocol handle tokens that don't return boolean values?
- [ ] Are there any direct .transfer() or .transferFrom() calls?

---

## 2. Approval & Allowance Vulnerabilities

### Overview

ERC20 approval mechanism has inherent design flaws that lead to front-running attacks and incompatibility with certain tokens. Analysis of 26+ reports shows these issues consistently affect protocols across different use cases.

> **📚 Source Reports for Deep Dive:**
> - `reports/erc20_token_findings/approve-function-can-be-front-ran-resulting-in-token-theft.md` (Liquid Collective - Spearbit)
> - `reports/erc20_token_findings/m-02-must-approve-0-first.md` (Tigris Trade - Code4rena)
> - `reports/erc20_token_findings/decrease-allowance-when-it-is-already-set-a-non-zero-value.md`

### Vulnerability Description

#### Root Cause

1. **Race Condition**: The `approve()` function doesn't protect against front-running when changing allowance from non-zero to non-zero
2. **Non-Standard Tokens**: USDT and similar tokens require approval to be set to 0 before setting a new non-zero value
3. **Deprecated safeApprove**: OpenZeppelin's deprecated `safeApprove()` can revert unexpectedly

#### Attack Scenario: Approval Front-Running

1. Alice has approved Bob to spend 100 tokens
2. Alice sends TX to change approval to 50 tokens
3. Bob sees pending TX and front-runs with `transferFrom(alice, bob, 100)`
4. After Alice's TX confirms, Bob calls `transferFrom(alice, bob, 50)`
5. Bob steals 150 tokens instead of intended 50

### Vulnerable Pattern Examples

**Example 1: Approval Front-Running Race Condition** [MEDIUM]
> 📖 Reference: `reports/erc20_token_findings/approve-function-can-be-front-ran-resulting-in-token-theft.md`
```solidity
// ❌ VULNERABLE: Classic approval race condition
function approve(address spender, uint256 amount) public returns (bool) {
    allowance[msg.sender][spender] = amount;  // Direct overwrite enables front-running
    emit Approval(msg.sender, spender, amount);
    return true;
}

// Attack: If allowance changes from 100 to 50, attacker can get 150 total
```

**Example 2: Not Approving 0 First for USDT-like Tokens** [MEDIUM]
> 📖 Reference: `reports/erc20_token_findings/m-02-must-approve-0-first.md`
```solidity
// ❌ VULNERABLE: USDT requires approve(0) before setting new allowance
function updateAllowance(address token, address spender, uint256 newAmount) external {
    IERC20(token).approve(spender, newAmount);  // Will REVERT for USDT if current allowance != 0
}
```

**Example 3: Using Deprecated safeApprove** [MEDIUM]
```solidity
// ❌ VULNERABLE: safeApprove reverts if allowance is non-zero
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

function approveMax(address token, address spender) external {
    // This will revert if there's existing allowance > 0
    IERC20(token).safeApprove(spender, type(uint256).max);
}
```

**Example 4: Infinite Approval Without Control** [LOW]
```solidity
// ❌ VULNERABLE: Infinite approval to untrusted contract
function deposit(uint256 amount) external {
    token.approve(untrustedRouter, type(uint256).max);  // Router can drain all tokens
    untrustedRouter.swap(amount);
}
```

### Impact Analysis

#### Technical Impact
- Double-spending via front-running
- Transaction reverts with USDT-like tokens
- Unexpected contract behavior

#### Business Impact
- **Frequency**: Found in 26+ of 761 analyzed reports (3.4%)
- Token theft via allowance manipulation
- Protocol incompatibility with major tokens (USDT)
- User funds at risk from infinite approvals

#### Affected Scenarios
- Token swap routers
- Staking contracts with changing allowances
- Multi-sig wallets with approval management
- DeFi aggregators

### Secure Implementation

**Fix 1: Use increaseAllowance/decreaseAllowance**
```solidity
// ✅ SECURE: Prevents front-running by using relative changes
function increaseAllowance(address spender, uint256 addedValue) public returns (bool) {
    _approve(msg.sender, spender, allowance[msg.sender][spender] + addedValue);
    return true;
}

function decreaseAllowance(address spender, uint256 subtractedValue) public returns (bool) {
    uint256 currentAllowance = allowance[msg.sender][spender];
    require(currentAllowance >= subtractedValue, "Decreased allowance below zero");
    _approve(msg.sender, spender, currentAllowance - subtractedValue);
    return true;
}
```

**Fix 2: Approve 0 Before New Amount (for USDT compatibility)**
```solidity
// ✅ SECURE: Compatible with USDT and similar tokens
function safeApproveWithReset(address token, address spender, uint256 amount) internal {
    // First reset to 0
    IERC20(token).safeApprove(spender, 0);
    // Then set new amount
    if (amount > 0) {
        IERC20(token).safeApprove(spender, amount);
    }
}
```

**Fix 3: Use forceApprove (OpenZeppelin 5.0+)**
```solidity
// ✅ SECURE: OpenZeppelin's forceApprove handles edge cases
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

using SafeERC20 for IERC20;

function setApproval(address token, address spender, uint256 amount) internal {
    IERC20(token).forceApprove(spender, amount);  // Handles USDT-like tokens
}
```

**Fix 4: Approve Only Required Amount**
```solidity
// ✅ SECURE: Minimal approval reduces risk
function swap(uint256 amount) external {
    // Approve only what's needed for this transaction
    token.approve(router, amount);
    router.swap(amount);
    // Optionally reset approval after
    token.approve(router, 0);
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: Direct approve() calls without checking current allowance
- Pattern 2: safeApprove() with non-zero amounts when allowance might exist
- Pattern 3: Infinite approvals (type(uint256).max) to external contracts
- Pattern 4: Missing approve(0) before new approval for USDT compatibility
```

#### Audit Checklist
- [ ] Does the protocol use increaseAllowance/decreaseAllowance?
- [ ] Are USDT-like tokens (require approve 0 first) supported?
- [ ] Is safeApprove() being used correctly (only when allowance is 0)?
- [ ] Are infinite approvals given only to trusted contracts?
- [ ] Is forceApprove() used for better compatibility?

---

## 3. Decimals & Precision Vulnerabilities

### Overview

ERC20 tokens can have varying decimal values (0-18+), but many protocols assume 18 decimals. This leads to severe calculation errors, fund loss, and protocol dysfunction. Analysis of 23+ reports shows decimals-related issues are consistently HIGH/CRITICAL severity.

> **📚 Source Reports for Deep Dive:**
> - `reports/erc20_token_findings/h-1-protocol-assumes-18-decimals-collateral.md` (GMX Synthetics - Sherlock)
> - `reports/erc20_token_findings/claim-will-underflow-and-revert-for-all-tokens-without-18-decimals.md` (Perennial - Sherlock)
> - `reports/erc20_token_findings/h-01-reward-calculation-will-be-wrong-for-non-standard-tokens-0-decimals.md`

### Vulnerability Description

#### Root Cause

1. **Hardcoded 18 Decimals**: Using `1e18` or `10**18` as scaling factor regardless of actual token decimals
2. **Missing Normalization**: Failing to normalize tokens with different decimals before calculations
3. **Precision Loss**: Integer division before multiplication causing severe rounding errors
4. **Overflow/Underflow**: Multiplication by 1e18 on tokens with >18 decimals causing overflow

#### Common Token Decimals
| Token | Decimals | Risk Factor |
|-------|----------|-------------|
| USDC | 6 | High - 12 orders of magnitude difference |
| USDT | 6 | High - Same as USDC |
| WBTC | 8 | High - 10 orders of magnitude difference |
| DAI | 18 | Standard |
| WETH | 18 | Standard |
| YAM | 24 | Very High - Overflow risk |

### Vulnerable Pattern Examples

**Example 1: Hardcoded 18 Decimals Assumption** [HIGH]
> 📖 Reference: `reports/erc20_token_findings/h-1-protocol-assumes-18-decimals-collateral.md`
```solidity
// ❌ VULNERABLE: Assumes 18 decimals for all tokens
function calculateCollateralValue(address token, uint256 amount) public view returns (uint256) {
    uint256 price = oracle.getPrice(token);  // Price in 1e18
    return (amount * price) / 1e18;  // WRONG if token has 6 decimals!
    // For USDC: 1000 USDC (1000e6) * price / 1e18 = almost 0
}
```

**Example 2: Division Before Multiplication (Precision Loss)** [MEDIUM]
> 📖 Reference: `reports/erc20_token_findings/claim-will-underflow-and-revert-for-all-tokens-without-18-decimals.md`
```solidity
// ❌ VULNERABLE: Precision loss due to division before multiplication
function calculateReward(uint256 amount, uint256 rate) public pure returns (uint256) {
    return (amount / 1e18) * rate;  // If amount < 1e18, result is 0!
    // For USDC: 1000e6 / 1e18 = 0 → reward = 0
}
```

**Example 3: Cross-Token Calculation Without Normalization** [HIGH]
```solidity
// ❌ VULNERABLE: Comparing tokens with different decimals
function swap(address tokenIn, address tokenOut, uint256 amountIn) external {
    uint256 amountOut = (amountIn * getPrice(tokenIn)) / getPrice(tokenOut);
    // If tokenIn=USDC(6), tokenOut=DAI(18): massive calculation error
    IERC20(tokenOut).transfer(msg.sender, amountOut);
}
```

**Example 4: Overflow with High-Decimal Tokens** [CRITICAL]
```solidity
// ❌ VULNERABLE: Overflow with tokens having >18 decimals
function scaleToStandard(uint256 amount, uint8 decimals) public pure returns (uint256) {
    return amount * (10 ** (18 - decimals));  // Underflows if decimals > 18!
    // For YAM (24 decimals): 10 ** (18 - 24) = 10 ** -6 = underflow
}
```

**Example 5: Share Calculation with Low Decimal Tokens** [HIGH]
> 📖 Reference: `reports/erc20_token_findings/h-01-reward-calculation-will-be-wrong-for-non-standard-tokens-0-decimals.md`
```solidity
// ❌ VULNERABLE: Share calculation fails with low decimals
function mintShares(uint256 depositAmount) external {
    uint256 shares = (depositAmount * totalShares) / totalAssets;
    // For USDC deposit: small amounts may round to 0 shares
    _mint(msg.sender, shares);
}
```

### Impact Analysis

#### Technical Impact
- Calculation results off by 10^12 or more
- Transactions reverting due to underflow
- Zero rewards/shares for legitimate deposits
- Integer overflow causing catastrophic errors

#### Business Impact
- **Frequency**: Found in 23+ of 761 analyzed reports (3.0%)
- **Severity**: Consistently HIGH to CRITICAL
- Direct fund loss from incorrect calculations
- Protocol insolvency from miscalculated collateral
- User exploitation of calculation errors

#### Affected Scenarios
- Lending protocols (collateral valuation)
- AMMs (swap calculations)
- Yield aggregators (share calculation)
- Cross-chain bridges (token normalization)
- Reward distribution systems

### Secure Implementation

**Fix 1: Dynamic Decimal Handling**
```solidity
// ✅ SECURE: Normalize to common precision
function normalizeAmount(address token, uint256 amount) public view returns (uint256) {
    uint8 decimals = IERC20Metadata(token).decimals();
    if (decimals < 18) {
        return amount * 10**(18 - decimals);
    } else if (decimals > 18) {
        return amount / 10**(decimals - 18);
    }
    return amount;
}
```

**Fix 2: Safe Decimal Scaling with Validation**
```solidity
// ✅ SECURE: Safe scaling with bounds checking
function scaleToDecimals(
    uint256 amount,
    uint8 fromDecimals,
    uint8 toDecimals
) public pure returns (uint256) {
    if (fromDecimals == toDecimals) {
        return amount;
    } else if (fromDecimals < toDecimals) {
        uint256 multiplier = 10 ** (toDecimals - fromDecimals);
        require(amount <= type(uint256).max / multiplier, "Overflow");
        return amount * multiplier;
    } else {
        uint256 divisor = 10 ** (fromDecimals - toDecimals);
        return amount / divisor;  // Note: precision loss is acceptable here
    }
}
```

**Fix 3: Multiply Before Divide (Precision Preservation)**
```solidity
// ✅ SECURE: Multiply first, then divide
function calculateRewardSecure(
    uint256 amount,
    uint256 rate,
    uint8 decimals
) public pure returns (uint256) {
    // Multiply first to preserve precision
    uint256 scaledAmount = amount * rate;
    return scaledAmount / (10 ** decimals);
}
```

**Fix 4: Use Fixed-Point Math Library**
```solidity
// ✅ SECURE: Use battle-tested fixed-point library
import {FixedPointMathLib} from "solmate/utils/FixedPointMathLib.sol";

function calculateValue(uint256 amount, uint256 price, uint8 decimals) public pure returns (uint256) {
    uint256 normalizedAmount = amount * 10**(18 - decimals);
    return FixedPointMathLib.mulWadDown(normalizedAmount, price);
}
```

**Fix 5: Validate Supported Decimals**
```solidity
// ✅ SECURE: Whitelist supported decimal ranges
function validateToken(address token) public view {
    uint8 decimals = IERC20Metadata(token).decimals();
    require(decimals >= 6 && decimals <= 18, "Unsupported decimals");
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: Hardcoded 1e18, 10**18, or similar constants in calculations
- Pattern 2: Division before multiplication in financial formulas
- Pattern 3: Missing decimals() calls before token amount calculations
- Pattern 4: Cross-token arithmetic without normalization
- Pattern 5: Subtraction in exponents (18 - decimals) without checks
```

#### Audit Checklist
- [ ] Does the protocol query token.decimals() for each token?
- [ ] Are calculations normalized to a common precision?
- [ ] Is multiplication performed before division?
- [ ] Are tokens with unusual decimals (0, 2, 24) handled?
- [ ] Are there overflow/underflow checks in scaling operations?
- [ ] Is there a whitelist of supported token decimals?

---

## 4. Fee-on-Transfer Token Vulnerabilities

### Overview

Fee-on-transfer (FOT) tokens deduct a percentage during transfers, causing the received amount to be less than the sent amount. This breaks accounting logic in most DeFi protocols. Analysis of 72+ reports shows this is the **most common** ERC20 integration vulnerability.

> **📚 Source Reports for Deep Dive:**
> - `reports/erc20_token_findings/fee-on-transfer-tokens-will-cause-users-to-lose-funds.md` (Teller - Sherlock)
> - `reports/erc20_token_findings/m-01-incompatibility-with-fee-on-transferinflationarydeflationaryrebasing-tokens.md` (Ajna - Sherlock)
> - `reports/erc20_token_findings/contracts-do-not-support-tokens-with-fees-or-rebasing-tokens.md` (Particle Protocol)
> - `reports/erc20_token_findings/h-3-tokens-with-fees-on-transfer-are-not-fully-supported.md`

### Vulnerability Description

#### Root Cause

1. **Balance Tracking Mismatch**: Protocol tracks transferred amount instead of actual received amount
2. **Assumed 1:1 Transfer**: `transferFrom(user, contract, amount)` doesn't always mean contract receives `amount`
3. **Missing Balance Verification**: No before/after balance check to determine actual received amount

#### Common Fee-on-Transfer Tokens
| Token | Fee | Notes |
|-------|-----|-------|
| PAXG (Pax Gold) | 0.02% | Gold-backed stablecoin |
| USDT (Tether) | Configurable | Fee currently disabled but can be enabled |
| STA (Statera) | 1% | Deflationary token |
| SAFEMOON | 10% | Popular deflationary token |
| Various Reflection Tokens | 2-10% | Auto-staking/reflection mechanism |

### Vulnerable Pattern Examples

**Example 1: Direct Amount Tracking (Most Common)** [HIGH]
> 📖 Reference: `reports/erc20_token_findings/fee-on-transfer-tokens-will-cause-users-to-lose-funds.md`
```solidity
// ❌ VULNERABLE: Assumes received amount equals transferred amount
function deposit(uint256 amount) external {
    token.transferFrom(msg.sender, address(this), amount);
    balances[msg.sender] += amount;  // WRONG! May receive less due to fee
}

function withdraw(uint256 amount) external {
    require(balances[msg.sender] >= amount);
    balances[msg.sender] -= amount;
    token.transfer(msg.sender, amount);  // May fail if contract has less tokens
}
```

**Example 2: Lending Protocol Collateral Tracking** [HIGH]
> 📖 Reference: `reports/erc20_token_findings/m-01-incompatibility-with-fee-on-transferinflationarydeflationaryrebasing-tokens.md`
```solidity
// ❌ VULNERABLE: Collateral amount recorded exceeds actual tokens held
function depositCollateral(address token, uint256 amount) external {
    IERC20(token).transferFrom(msg.sender, address(this), amount);
    userCollateral[msg.sender][token] += amount;  // Overstated if FOT token
    
    // User can now borrow against inflated collateral value
    uint256 borrowLimit = calculateBorrowLimit(msg.sender);
}
```

**Example 3: Token Swap Accounting Error** [HIGH]
```solidity
// ❌ VULNERABLE: Swap calculations use wrong input amount
function swap(address tokenIn, address tokenOut, uint256 amountIn) external {
    IERC20(tokenIn).transferFrom(msg.sender, address(this), amountIn);
    
    // Calculation based on amountIn, but contract received less
    uint256 amountOut = calculateSwapOutput(amountIn);  // Overpays user
    IERC20(tokenOut).transfer(msg.sender, amountOut);
}
```

**Example 4: Liquidity Pool Imbalance** [HIGH]
```solidity
// ❌ VULNERABLE: LP tokens minted based on stated deposit, not actual
function addLiquidity(uint256 amount0, uint256 amount1) external {
    token0.transferFrom(msg.sender, address(this), amount0);
    token1.transferFrom(msg.sender, address(this), amount1);
    
    // Mints LP based on requested amounts, not received
    uint256 lpTokens = calculateLPTokens(amount0, amount1);
    _mint(msg.sender, lpTokens);  // User gets more LP than deserved
}
```

**Example 5: Staking Rewards Miscalculation** [MEDIUM]
```solidity
// ❌ VULNERABLE: Stake amount used for rewards calculation is wrong
function stake(uint256 amount) external {
    stakingToken.transferFrom(msg.sender, address(this), amount);
    stakes[msg.sender] += amount;
    totalStaked += amount;  // Total is inflated
}

function claimRewards() external {
    // Rewards calculated on inflated stake amounts
    uint256 reward = (stakes[msg.sender] * rewardRate) / totalStaked;
    rewardToken.transfer(msg.sender, reward);
}
```

### Impact Analysis

#### Technical Impact
- Contract balance becomes less than sum of all user balances
- Last users to withdraw cannot get their full balance
- Protocol becomes insolvent over time
- Accounting invariants broken

#### Business Impact
- **Frequency**: Found in 72+ of 761 analyzed reports (9.5%) - **MOST COMMON**
- **Severity**: Consistently MEDIUM to HIGH
- Direct fund loss for users
- Protocol insolvency
- Unfair distribution of funds

#### Affected Scenarios (from reports)
- Lending protocols (collateral accounting)
- DEX/AMMs (swap calculations)
- Staking contracts (reward distribution)
- Vaults (share calculations)
- Bridges (cross-chain transfers)
- Escrow contracts (locked fund tracking)

### Secure Implementation

**Fix 1: Balance Difference Pattern (Recommended)**
```solidity
// ✅ SECURE: Track actual received amount
function deposit(uint256 amount) external {
    uint256 balanceBefore = token.balanceOf(address(this));
    token.transferFrom(msg.sender, address(this), amount);
    uint256 balanceAfter = token.balanceOf(address(this));
    
    uint256 actualReceived = balanceAfter - balanceBefore;
    balances[msg.sender] += actualReceived;  // Correct amount tracked
    
    emit Deposit(msg.sender, actualReceived);
}
```

**Fix 2: Complete Implementation with Events**
```solidity
// ✅ SECURE: Full implementation with proper accounting
contract SecureVault {
    IERC20 public immutable token;
    mapping(address => uint256) public balances;
    uint256 public totalDeposits;
    
    function deposit(uint256 amount) external returns (uint256 actualDeposit) {
        uint256 balanceBefore = token.balanceOf(address(this));
        token.safeTransferFrom(msg.sender, address(this), amount);
        uint256 balanceAfter = token.balanceOf(address(this));
        
        actualDeposit = balanceAfter - balanceBefore;
        require(actualDeposit > 0, "Zero deposit");
        
        balances[msg.sender] += actualDeposit;
        totalDeposits += actualDeposit;
        
        emit Deposit(msg.sender, actualDeposit, amount);  // Log both values
    }
    
    function withdraw(uint256 amount) external {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        balances[msg.sender] -= amount;
        totalDeposits -= amount;
        
        token.safeTransfer(msg.sender, amount);
        emit Withdrawal(msg.sender, amount);
    }
}
```

**Fix 3: Reject Fee-on-Transfer Tokens**
```solidity
// ✅ SECURE: Explicitly reject FOT tokens
function deposit(uint256 amount) external {
    uint256 balanceBefore = token.balanceOf(address(this));
    token.transferFrom(msg.sender, address(this), amount);
    uint256 balanceAfter = token.balanceOf(address(this));
    
    require(balanceAfter - balanceBefore == amount, "Fee-on-transfer tokens not supported");
    balances[msg.sender] += amount;
}
```

**Fix 4: Token Whitelist Approach**
```solidity
// ✅ SECURE: Only allow pre-vetted tokens
mapping(address => bool) public supportedTokens;

function deposit(address tokenAddr, uint256 amount) external {
    require(supportedTokens[tokenAddr], "Token not supported");
    // Can now safely assume no transfer fee for whitelisted tokens
    IERC20(tokenAddr).transferFrom(msg.sender, address(this), amount);
    balances[msg.sender][tokenAddr] += amount;
}

// Admin function to whitelist tokens after verification
function addSupportedToken(address tokenAddr) external onlyOwner {
    // Verify token doesn't have transfer fees before whitelisting
    supportedTokens[tokenAddr] = true;
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: transferFrom() followed by += amount (without balance check)
- Pattern 2: Amount parameter used directly in calculations after transfer
- Pattern 3: Missing balanceOf() calls before and after transfers
- Pattern 4: Lending/staking contracts without FOT token handling
- Pattern 5: totalSupply or totalDeposits tracking without verification
```

#### Semgrep Rule
```yaml
rules:
  - id: fee-on-transfer-vulnerability
    patterns:
      - pattern-either:
          - pattern: |
              $TOKEN.transferFrom($FROM, $TO, $AMOUNT);
              ...
              $VAR += $AMOUNT;
          - pattern: |
              $TOKEN.safeTransferFrom($FROM, $TO, $AMOUNT);
              ...
              $VAR += $AMOUNT;
    message: "Potential fee-on-transfer token vulnerability"
    severity: WARNING
```

#### Audit Checklist
- [ ] Does the protocol use balance-before/after pattern for deposits?
- [ ] Are fee-on-transfer tokens explicitly supported or rejected?
- [ ] Is there a token whitelist/blacklist mechanism?
- [ ] Do withdrawal functions verify sufficient contract balance?
- [ ] Are transfer amounts returned and used in accounting?
- [ ] Does documentation clarify FOT token support?

---

## 5. Rebasing Token Vulnerabilities

### Overview

Rebasing tokens automatically adjust user balances based on external factors (interest accrual, supply changes). Protocols that cache balances or use shares incorrectly become incompatible with rebasing tokens. Analysis of 28+ reports shows this vulnerability leads to permanent fund loss or protocol insolvency.

> **📚 Source Reports for Deep Dive:**
> - `reports/erc20_token_findings/h-05-aaves-share-tokens-are-rebasing-breaking-current-strategy-code.md` (Y2K Finance - Sherlock)
> - `reports/erc20_token_findings/lack-of-rebasable-tokens-support.md` (Arcade - Sherlock)
> - `reports/erc20_token_findings/contracts-do-not-support-tokens-with-fees-or-rebasing-tokens.md` (Particle Protocol)
> - `reports/erc20_token_findings/m-01-incompatibility-with-fee-on-transferinflationarydeflationaryrebasing-tokens.md`

### Vulnerability Description

#### Root Cause

1. **Cached Balance**: Storing balanceOf() result and using cached value later
2. **Share Mismatch**: Using raw token amounts instead of protocol's internal share system
3. **Missing Rebase Hooks**: Not implementing or triggering rebase before balance reads
4. **Static Amount Tracking**: Recording deposit amount that becomes stale after rebase

#### Common Rebasing Tokens
| Token | Type | Mechanism |
|-------|------|-----------|
| stETH (Lido) | Positive Rebase | Balance increases daily with staking rewards |
| aUSDC (Aave) | Positive Rebase | Balance increases with interest accrual |
| AMPL (Ampleforth) | Elastic Supply | Balance changes to maintain price target |
| OHM (Olympus) | Positive Rebase | Balance increases with staking rewards |
| yTokens (Yearn) | Value Accrual | Share value increases (not balance) |

### Vulnerable Pattern Examples

**Example 1: Cached Balance Becomes Stale** [HIGH]
> 📖 Reference: `reports/erc20_token_findings/h-05-aaves-share-tokens-are-rebasing-breaking-current-strategy-code.md`
```solidity
// ❌ VULNERABLE: Cached balance doesn't reflect rebases
contract VaultWithCachedBalance {
    mapping(address => uint256) public userDeposits;  // Cached on deposit
    
    function deposit(uint256 amount) external {
        token.transferFrom(msg.sender, address(this), amount);
        userDeposits[msg.sender] = amount;  // Static value, doesn't update with rebase
    }
    
    function withdraw() external {
        uint256 amount = userDeposits[msg.sender];  // Returns stale value
        // For stETH: if balance increased 5% due to rebase, user loses that 5%
        token.transfer(msg.sender, amount);
        userDeposits[msg.sender] = 0;
    }
}
```

**Example 2: Negative Rebase Causes Insolvency** [CRITICAL]
> 📖 Reference: `reports/erc20_token_findings/lack-of-rebasable-tokens-support.md`
```solidity
// ❌ VULNERABLE: Negative rebase makes withdrawals impossible
function deposit(uint256 amount) external {
    token.transferFrom(msg.sender, address(this), amount);
    balances[msg.sender] += amount;
    totalDeposits += amount;
}

function withdraw(uint256 amount) external {
    require(balances[msg.sender] >= amount);
    balances[msg.sender] -= amount;
    totalDeposits -= amount;
    
    // After negative rebase, contract may have less tokens than totalDeposits
    token.transfer(msg.sender, amount);  // REVERTS - insufficient balance!
}
```

**Example 3: Share-Based Token Used as Direct Balance** [HIGH]
```solidity
// ❌ VULNERABLE: Using aToken amount directly without share conversion
function depositAave(uint256 amount) external {
    aToken.transferFrom(msg.sender, address(this), amount);
    // aToken balance will increase over time, but we track static amount
    userShares[msg.sender] = amount;
}

function getClaimableAmount(address user) external view returns (uint256) {
    return userShares[user];  // Returns deposit amount, not current value
}
```

**Example 4: Collateral Value Calculation Error** [HIGH]
```solidity
// ❌ VULNERABLE: Collateral value doesn't reflect rebasing
function getCollateralValue(address user) public view returns (uint256) {
    // Uses cached deposit amount, not current rebased balance
    return collateralDeposits[user] * oracle.getPrice(collateralToken);
}

function liquidate(address user) external {
    require(getCollateralValue(user) < getDebtValue(user), "Not liquidatable");
    // User might have more collateral than tracked due to positive rebase
    // Allows unfair liquidation
}
```

**Example 5: Reward Distribution Based on Static Amounts** [MEDIUM]
```solidity
// ❌ VULNERABLE: Rewards calculated on stale balances
mapping(address => uint256) public stakedAmounts;  // Static

function calculateReward(address user) public view returns (uint256) {
    // Uses static stakedAmounts instead of current balance
    return (stakedAmounts[user] * rewardRate) / totalStaked;
    // If token rebased positively, rewards are underpaid
}
```

### Impact Analysis

#### Technical Impact
- Cached balances become inaccurate after rebase
- Protocol accounting doesn't match actual token balances
- Withdrawal failures due to insufficient contract balance
- Incorrect share/value calculations

#### Business Impact
- **Frequency**: Found in 28+ of 761 analyzed reports (3.7%)
- **Severity**: Consistently MEDIUM to CRITICAL
- Users lose rebased gains (positive rebase)
- Protocol insolvency (negative rebase)
- Unfair reward distribution
- Incorrect liquidation thresholds

#### Affected Scenarios
- Yield vaults using stETH, aTokens
- Lending protocols accepting rebasing collateral
- Staking contracts with rebasing tokens
- AMMs with rebasing token pairs
- Escrow/vesting contracts

### Secure Implementation

**Fix 1: Use Shares Instead of Amounts**
```solidity
// ✅ SECURE: Track proportional shares, not absolute amounts
contract RebaseCompatibleVault {
    uint256 public totalShares;
    mapping(address => uint256) public userShares;
    IERC20 public rebasingToken;
    
    function deposit(uint256 amount) external {
        uint256 currentBalance = rebasingToken.balanceOf(address(this));
        rebasingToken.transferFrom(msg.sender, address(this), amount);
        uint256 newBalance = rebasingToken.balanceOf(address(this));
        uint256 deposited = newBalance - currentBalance;
        
        uint256 sharesToMint;
        if (totalShares == 0 || currentBalance == 0) {
            sharesToMint = deposited;
        } else {
            sharesToMint = (deposited * totalShares) / currentBalance;
        }
        
        userShares[msg.sender] += sharesToMint;
        totalShares += sharesToMint;
    }
    
    function withdraw(uint256 shares) external {
        require(userShares[msg.sender] >= shares, "Insufficient shares");
        
        uint256 currentBalance = rebasingToken.balanceOf(address(this));
        uint256 amountToWithdraw = (shares * currentBalance) / totalShares;
        
        userShares[msg.sender] -= shares;
        totalShares -= shares;
        
        rebasingToken.transfer(msg.sender, amountToWithdraw);
    }
    
    function getClaimableAmount(address user) external view returns (uint256) {
        if (totalShares == 0) return 0;
        return (userShares[user] * rebasingToken.balanceOf(address(this))) / totalShares;
    }
}
```

**Fix 2: Use Wrapped Non-Rebasing Version**
```solidity
// ✅ SECURE: Use wstETH instead of stETH
contract VaultWithWrappedToken {
    IWstETH public immutable wstETH;  // Non-rebasing wrapper
    
    function deposit(uint256 stETHAmount) external {
        stETH.transferFrom(msg.sender, address(this), stETHAmount);
        stETH.approve(address(wstETH), stETHAmount);
        
        // Convert to non-rebasing wrapper
        uint256 wstETHAmount = wstETH.wrap(stETHAmount);
        userDeposits[msg.sender] += wstETHAmount;  // Safe to cache
    }
    
    function withdraw() external {
        uint256 wstETHAmount = userDeposits[msg.sender];
        userDeposits[msg.sender] = 0;
        
        // Convert back and send stETH
        uint256 stETHAmount = wstETH.unwrap(wstETHAmount);
        stETH.transfer(msg.sender, stETHAmount);  // Includes rebased gains
    }
}
```

**Fix 3: Real-Time Balance Reads**
```solidity
// ✅ SECURE: Always read current balance
function getCollateralValue(address user) public view returns (uint256) {
    // Read actual current balance, not cached value
    uint256 currentBalance = rebasingToken.balanceOf(address(this));
    uint256 userProportion = (userShares[user] * currentBalance) / totalShares;
    return userProportion * oracle.getPrice(address(rebasingToken));
}
```

**Fix 4: Reject Rebasing Tokens**
```solidity
// ✅ SECURE: Explicitly reject rebasing tokens
mapping(address => bool) public isRebasingToken;

function setRebasingToken(address token, bool isRebasing) external onlyOwner {
    isRebasingToken[token] = isRebasing;
}

function deposit(address token, uint256 amount) external {
    require(!isRebasingToken[token], "Rebasing tokens not supported");
    // Safe to use direct amount tracking
    IERC20(token).transferFrom(msg.sender, address(this), amount);
    balances[msg.sender][token] += amount;
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: Caching balanceOf() result in storage for later use
- Pattern 2: Using static deposit amounts for withdrawal calculations
- Pattern 3: Missing share-based accounting for user deposits
- Pattern 4: totalDeposits tracking without rebase handling
- Pattern 5: Collateral/staking calculations using cached values
```

#### Audit Checklist
- [ ] Does the protocol use share-based accounting?
- [ ] Are rebasing tokens explicitly supported or rejected?
- [ ] Is balanceOf() called at withdrawal time (not cached)?
- [ ] Are wrapped versions (wstETH, etc.) used when appropriate?
- [ ] Does documentation clarify rebasing token support?
- [ ] Are collateral calculations using real-time balance reads?

---

## 6. ERC777 Reentrancy Vulnerabilities

### Overview

ERC777 tokens are backwards-compatible with ERC20 but include hooks (`tokensToSend` and `tokensReceived`) that call external contracts during transfers. These hooks enable reentrancy attacks even when standard ERC20 reentrancy guards are in place. Analysis of 27+ reports shows ERC777 reentrancy consistently leads to CRITICAL severity exploits.

> **📚 Source Reports for Deep Dive:**
> - `reports/erc20_token_findings/1-erc777-re-entrancy-attack.md` (imBTC/Uniswap exploit analysis)
> - `reports/erc20_token_findings/h-01-reentrancy-in-buy-function-for-erc777-tokens-allows-buying-funds-with-consi.md` (Sherlock)
> - `reports/erc20_token_findings/m-04-erc777-reentrancy-when-withdrawing-can-be-used-to-withdraw-all-collateral.md` (Sherlock)

### Vulnerability Description

#### Root Cause

1. **Hidden Callbacks**: ERC777 transfers trigger hooks that execute arbitrary code
2. **Standard ERC20 Interface**: ERC777 tokens expose standard `transfer()`/`transferFrom()` that hide the callback behavior
3. **State Update Ordering**: State changes made after token transfers can be manipulated via reentrancy
4. **Missing Reentrancy Guards**: Standard nonReentrant modifiers may not protect against cross-function reentrancy

#### ERC777 Hook Mechanism
```
Token Transfer Flow:
1. sender.tokensToSend() hook called (if registered)
2. Balance updates
3. recipient.tokensReceived() hook called (if registered)
```

#### Known ERC777 Tokens
| Token | Notes |
|-------|-------|
| imBTC | Wrapped Bitcoin, caused Uniswap V1 exploit |
| WETH777 | Wrapped ETH with ERC777 |
| Various DeFi tokens | Many protocols issued ERC777 tokens |

### Vulnerable Pattern Examples

**Example 1: State Update After Transfer (Classic)** [CRITICAL]
> 📖 Reference: `reports/erc20_token_findings/1-erc777-re-entrancy-attack.md`
```solidity
// ❌ VULNERABLE: State updated after external call
function buy(uint256 amount) external payable {
    require(msg.value >= amount * price);
    
    token.transfer(msg.sender, amount);  // ERC777: calls msg.sender hook
    // Attacker re-enters here before sold is updated!
    
    sold += amount;  // State update AFTER transfer
}

// Attack contract:
contract Attacker is IERC777Recipient {
    function tokensReceived(...) external {
        if (shouldReenter) {
            shouldReenter = false;
            target.buy(amount);  // Re-enter before sold is updated
        }
    }
}
```

**Example 2: Collateral Withdrawal Reentrancy** [CRITICAL]
> 📖 Reference: `reports/erc20_token_findings/m-04-erc777-reentrancy-when-withdrawing-can-be-used-to-withdraw-all-collateral.md`
```solidity
// ❌ VULNERABLE: Collateral can be drained via reentrancy
function withdrawCollateral(uint256 amount) external {
    require(collateral[msg.sender] >= amount);
    
    // Transfer ERC777 token - triggers tokensReceived hook on recipient
    collateralToken.transfer(msg.sender, amount);  // CALLBACK HERE
    
    // Attacker re-enters and withdraws again before this executes
    collateral[msg.sender] -= amount;
}
```

**Example 3: Uniswap V1 Style Exploit** [CRITICAL]
```solidity
// ❌ VULNERABLE: AMM swap with ERC777 token
function swapTokenForEth(uint256 tokenAmount) external {
    uint256 ethAmount = getEthAmount(tokenAmount);
    
    // ERC777 transfer triggers sender hook BEFORE balances update internally
    token.transferFrom(msg.sender, address(this), tokenAmount);  // CALLBACK
    
    // Attacker re-enters and swaps again at old price
    payable(msg.sender).transfer(ethAmount);
    
    // Update reserves AFTER transfers
    tokenReserve += tokenAmount;
    ethReserve -= ethAmount;
}
```

**Example 4: Auction/Marketplace Reentrancy** [HIGH]
```solidity
// ❌ VULNERABLE: NFT marketplace with ERC777 payment
function buyNFT(uint256 tokenId, uint256 price) external {
    require(listings[tokenId].price == price);
    
    // ERC777 payment - triggers hook
    paymentToken.transferFrom(msg.sender, seller, price);  // CALLBACK
    
    // Attacker can re-enter and buy same NFT again
    nft.transferFrom(address(this), msg.sender, tokenId);
    delete listings[tokenId];
}
```

**Example 5: Staking Reentrancy** [HIGH]
```solidity
// ❌ VULNERABLE: Stake and immediately unstake via reentrancy
function stake(uint256 amount) external {
    stakingToken.transferFrom(msg.sender, address(this), amount);  // CALLBACK
    // Attacker unstakes in callback before stake is recorded
    stakes[msg.sender] += amount;
    totalStaked += amount;
}

function unstake(uint256 amount) external {
    require(stakes[msg.sender] >= amount);
    stakes[msg.sender] -= amount;
    totalStaked -= amount;
    stakingToken.transfer(msg.sender, amount);  // CALLBACK
}
```

### Impact Analysis

#### Technical Impact
- Complete protocol drain possible
- State corruption across multiple functions
- Violation of protocol invariants
- Manipulation of prices/reserves in AMMs

#### Business Impact
- **Frequency**: Found in 27+ of 761 analyzed reports (3.5%)
- **Severity**: Consistently HIGH to CRITICAL
- **Real-World Exploits**:
  - imBTC/Uniswap V1: $300K+ drained
  - Multiple DeFi protocol exploits

#### Affected Scenarios
- DEXs/AMMs accepting ERC777 tokens
- Lending protocols with ERC777 collateral
- NFT marketplaces with ERC777 payments
- Staking contracts
- Any protocol with state changes after token transfers

### Secure Implementation

**Fix 1: Checks-Effects-Interactions Pattern**
```solidity
// ✅ SECURE: Update state BEFORE external calls
function buy(uint256 amount) external payable {
    require(msg.value >= amount * price);
    
    // CHECKS
    require(available >= amount, "Not enough tokens");
    
    // EFFECTS - Update state BEFORE transfer
    sold += amount;
    available -= amount;
    
    // INTERACTIONS - External call LAST
    token.transfer(msg.sender, amount);
}
```

**Fix 2: Reentrancy Guard (ReentrancyGuard)**
```solidity
// ✅ SECURE: Use OpenZeppelin ReentrancyGuard
import {ReentrancyGuard} from "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract SecureVault is ReentrancyGuard {
    function withdrawCollateral(uint256 amount) external nonReentrant {
        require(collateral[msg.sender] >= amount);
        collateral[msg.sender] -= amount;
        collateralToken.transfer(msg.sender, amount);
    }
    
    function deposit(uint256 amount) external nonReentrant {
        collateralToken.transferFrom(msg.sender, address(this), amount);
        collateral[msg.sender] += amount;
    }
}
```

**Fix 3: Combined CEI + Reentrancy Guard**
```solidity
// ✅ SECURE: Belt and suspenders approach
contract SecureAMM is ReentrancyGuard {
    function swap(uint256 amountIn) external nonReentrant {
        // Calculate output based on current reserves
        uint256 amountOut = calculateOutput(amountIn);
        
        // EFFECTS - Update reserves BEFORE transfers
        tokenReserve += amountIn;
        ethReserve -= amountOut;
        
        // INTERACTIONS
        token.transferFrom(msg.sender, address(this), amountIn);
        payable(msg.sender).transfer(amountOut);
    }
}
```

**Fix 4: Block ERC777 Tokens**
```solidity
// ✅ SECURE: Explicitly reject ERC777 tokens
function deposit(address tokenAddr, uint256 amount) external {
    // Check if token implements ERC777 interface
    try IERC1820Registry(0x1820a4B7618BdE71Dce8cdc73aAB6C95905faD24)
        .getInterfaceImplementer(tokenAddr, keccak256("ERC777Token")) 
    returns (address impl) {
        require(impl == address(0), "ERC777 tokens not supported");
    } catch {}
    
    IERC20(tokenAddr).transferFrom(msg.sender, address(this), amount);
    balances[msg.sender][tokenAddr] += amount;
}
```

**Fix 5: Mutex Lock Pattern**
```solidity
// ✅ SECURE: Simple mutex implementation
contract SecureContract {
    bool private _locked;
    
    modifier noReentrant() {
        require(!_locked, "Reentrant call");
        _locked = true;
        _;
        _locked = false;
    }
    
    function sensitiveOperation() external noReentrant {
        // Safe from reentrancy
    }
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: State updates AFTER token.transfer() or token.transferFrom()
- Pattern 2: Missing nonReentrant modifier on functions with external calls
- Pattern 3: Functions that accept any ERC20 without ERC777 check
- Pattern 4: Cross-function state dependencies without shared reentrancy lock
- Pattern 5: Balance/reserve updates after token transfers in AMMs
```

#### Audit Checklist
- [ ] Do all functions follow Checks-Effects-Interactions pattern?
- [ ] Is ReentrancyGuard applied to all state-changing functions?
- [ ] Are ERC777 tokens explicitly supported or rejected?
- [ ] Are all cross-function reentrancy paths analyzed?
- [ ] Is there documentation about ERC777 token compatibility?
- [ ] Are AMM reserve updates performed before token transfers?

---

## 7. Blacklist & Pausable Token Vulnerabilities

### Overview

Tokens like USDC, USDT, and PAXG can blacklist addresses or pause all transfers. When protocols don't account for this behavior, blacklisted users can cause permanent fund lockups, DoS conditions, or griefing attacks. Analysis of 28+ reports shows these issues consistently affect lending, orderbook, and escrow protocols.

> **📚 Source Reports for Deep Dive:**
> - `reports/erc20_token_findings/m-17-if-borrower-or-kicker-got-blacklisted-by-asset-contract-their-collateral-or.md` (Ajna - Sherlock)
> - `reports/erc20_token_findings/orderbook-denial-of-service-leveraging-blacklistable-tokens-like-usdc.md` (Rubicon - Code4rena)
> - `reports/erc20_token_findings/h-02-funds-will-be-stuck-in-the-contract-if-a-user-becomes-blacklisted.md`

### Vulnerability Description

#### Root Cause

1. **Assumed Transferability**: Protocols assume transfers will always succeed
2. **Direct Recipient Dependency**: Funds sent directly to addresses that may be blacklisted
3. **No Fallback Mechanism**: No way to redirect funds if recipient is blocked
4. **Pause Vulnerability**: Entire protocol can halt if underlying token is paused

#### Tokens with Blacklist/Pause Features
| Token | Blacklist | Pause | Notes |
|-------|-----------|-------|-------|
| USDC (Circle) | ✅ | ✅ | Most commonly used stablecoin |
| USDT (Tether) | ✅ | ✅ | Can freeze individual addresses |
| PAXG | ✅ | ✅ | Gold-backed, regulatory compliance |
| BUSD | ✅ | ✅ | Binance stablecoin |
| cUSDC (Compound) | ✅ | - | Inherits from USDC |

### Vulnerable Pattern Examples

**Example 1: Collateral Stuck When User Blacklisted** [MEDIUM]
> 📖 Reference: `reports/erc20_token_findings/m-17-if-borrower-or-kicker-got-blacklisted-by-asset-contract-their-collateral-or.md`
```solidity
// ❌ VULNERABLE: Collateral permanently locked if user gets blacklisted
function repayAndWithdrawCollateral(uint256 repayAmount) external {
    require(debt[msg.sender] >= repayAmount);
    
    debtToken.transferFrom(msg.sender, address(this), repayAmount);
    debt[msg.sender] -= repayAmount;
    
    uint256 collateralAmount = collateral[msg.sender];
    collateral[msg.sender] = 0;
    
    // If msg.sender is USDC blacklisted, this reverts and collateral is stuck
    collateralToken.transfer(msg.sender, collateralAmount);  // REVERTS!
}
```

**Example 2: Orderbook DoS Attack** [HIGH]
> 📖 Reference: `reports/erc20_token_findings/orderbook-denial-of-service-leveraging-blacklistable-tokens-like-usdc.md`
```solidity
// ❌ VULNERABLE: Attacker can DoS order fills
contract Orderbook {
    struct Order {
        address maker;
        uint256 amount;
        uint256 price;
    }
    
    function fillOrder(uint256 orderId) external {
        Order storage order = orders[orderId];
        uint256 cost = order.amount * order.price;
        
        // Attacker creates order, then gets themselves blacklisted
        // All attempts to fill the order will revert
        paymentToken.transfer(order.maker, cost);  // REVERTS if maker blacklisted
        
        // Order cannot be filled, cannot be cancelled by others
        // Clogs the orderbook permanently
    }
}
```

**Example 3: Escrow Funds Locked Forever** [HIGH]
```solidity
// ❌ VULNERABLE: Escrow funds stuck if recipient blacklisted
contract Escrow {
    function release(uint256 escrowId) external {
        Escrow storage e = escrows[escrowId];
        require(e.releaseTime <= block.timestamp);
        require(!e.released);
        
        e.released = true;
        
        // If recipient got blacklisted during escrow period, funds are stuck
        token.transfer(e.recipient, e.amount);  // REVERTS!
        // Cannot recover - funds locked in contract forever
    }
}
```

**Example 4: Liquidation Blocked** [CRITICAL]
```solidity
// ❌ VULNERABLE: Liquidation fails if borrower is blacklisted
function liquidate(address borrower) external {
    require(isUndercollateralized(borrower));
    
    // Seize collateral
    uint256 collateralAmount = collateral[borrower];
    collateral[borrower] = 0;
    
    // If borrower is blacklisted for USDC, liquidator can't receive collateral
    collateralToken.transfer(msg.sender, collateralAmount);  // REVERTS!
    // Position cannot be liquidated, bad debt accumulates
}
```

**Example 5: Vesting/Airdrop Claim Blocked** [MEDIUM]
```solidity
// ❌ VULNERABLE: Vested tokens cannot be claimed
function claimVested(address beneficiary) external {
    uint256 vested = calculateVested(beneficiary);
    claimed[beneficiary] += vested;
    
    // If beneficiary is blacklisted, they can never claim
    token.transfer(beneficiary, vested);  // REVERTS!
    // Tokens are effectively burned/stuck
}
```

### Impact Analysis

#### Technical Impact
- Transfer reverts block protocol functions
- Funds become permanently locked
- Critical functions (liquidation) can be blocked
- Protocol state becomes inconsistent

#### Business Impact
- **Frequency**: Found in 28+ of 761 analyzed reports (3.7%)
- **Severity**: MEDIUM to CRITICAL depending on context
- Permanent loss of user funds
- Protocol insolvency (blocked liquidations)
- DoS attacks on orderbooks/auctions
- Regulatory compliance issues

#### Affected Scenarios
- Lending protocols (collateral withdrawal, liquidation)
- DEXs with orderbooks
- Escrow/vesting contracts
- Auction platforms
- Cross-chain bridges
- Any protocol with direct transfers to users

### Secure Implementation

**Fix 1: Pull-Over-Push Pattern**
```solidity
// ✅ SECURE: Users pull their own funds
contract SecureVault {
    mapping(address => uint256) public withdrawable;
    
    function repayAndReleaseCollateral(uint256 repayAmount) external {
        require(debt[msg.sender] >= repayAmount);
        
        debtToken.transferFrom(msg.sender, address(this), repayAmount);
        debt[msg.sender] -= repayAmount;
        
        // Don't transfer directly - make available for withdrawal
        uint256 collateralAmount = collateral[msg.sender];
        collateral[msg.sender] = 0;
        withdrawable[msg.sender] += collateralAmount;
        
        emit CollateralReleased(msg.sender, collateralAmount);
    }
    
    function withdraw() external {
        uint256 amount = withdrawable[msg.sender];
        require(amount > 0, "Nothing to withdraw");
        withdrawable[msg.sender] = 0;
        
        // If user is blacklisted, they can't withdraw but protocol continues
        collateralToken.transfer(msg.sender, amount);
    }
}
```

**Fix 2: Alternative Recipient Pattern**
```solidity
// ✅ SECURE: Allow specifying alternative recipient
function withdrawCollateral(address recipient) external {
    require(collateral[msg.sender] > 0, "No collateral");
    
    uint256 amount = collateral[msg.sender];
    collateral[msg.sender] = 0;
    
    // User can specify non-blacklisted recipient
    collateralToken.transfer(recipient, amount);
    
    emit CollateralWithdrawn(msg.sender, recipient, amount);
}

function liquidate(address borrower, address collateralRecipient) external {
    require(isUndercollateralized(borrower));
    
    uint256 collateralAmount = collateral[borrower];
    collateral[borrower] = 0;
    
    // Liquidator specifies where to receive collateral
    collateralToken.transfer(collateralRecipient, collateralAmount);
}
```

**Fix 3: Try-Catch with Fallback**
```solidity
// ✅ SECURE: Handle transfer failures gracefully
function releaseEscrow(uint256 escrowId) external {
    Escrow storage e = escrows[escrowId];
    require(e.releaseTime <= block.timestamp);
    require(!e.released);
    
    e.released = true;
    
    try token.transfer(e.recipient, e.amount) {
        emit EscrowReleased(escrowId, e.recipient, e.amount);
    } catch {
        // Transfer failed - store for later claim
        failedTransfers[e.recipient] += e.amount;
        emit TransferFailed(escrowId, e.recipient, e.amount);
    }
}

function claimFailedTransfer(address recipient) external {
    uint256 amount = failedTransfers[msg.sender];
    require(amount > 0);
    failedTransfers[msg.sender] = 0;
    
    // Allow specifying different recipient
    token.transfer(recipient, amount);
}
```

**Fix 4: Admin Recovery Function**
```solidity
// ✅ SECURE: Admin can redirect stuck funds
function adminRecoverStuckFunds(
    uint256 escrowId,
    address newRecipient
) external onlyOwner {
    Escrow storage e = escrows[escrowId];
    require(e.released, "Not released yet");
    require(e.stuckFunds > 0, "No stuck funds");
    
    uint256 amount = e.stuckFunds;
    e.stuckFunds = 0;
    
    token.transfer(newRecipient, amount);
    
    emit FundsRecovered(escrowId, newRecipient, amount);
}
```

**Fix 5: Orderbook with Cancellation**
```solidity
// ✅ SECURE: Anyone can cancel orders for blacklisted makers
contract SecureOrderbook {
    function fillOrder(uint256 orderId) external {
        Order storage order = orders[orderId];
        require(!order.filled && !order.cancelled);
        
        // Try to transfer to maker
        try paymentToken.transfer(order.maker, order.cost) {
            order.filled = true;
            // Transfer tokens to taker
        } catch {
            // Maker is likely blacklisted - cancel order
            order.cancelled = true;
            emit OrderCancelledDueToBlacklist(orderId, order.maker);
        }
    }
    
    // Allow anyone to cancel orders for blacklisted addresses
    function cancelBlacklistedOrder(uint256 orderId) external {
        Order storage order = orders[orderId];
        require(!order.filled && !order.cancelled);
        
        // Verify maker is actually blacklisted
        require(!canReceive(order.maker), "Maker not blacklisted");
        
        order.cancelled = true;
        // Return locked tokens to maker's withdrawable balance
    }
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: Direct transfer() to user addresses without fallback
- Pattern 2: Liquidation functions that transfer to liquidator directly
- Pattern 3: Escrow/vesting with fixed recipient and no recovery
- Pattern 4: Orderbooks without order cancellation mechanism
- Pattern 5: No alternative recipient parameter in withdrawal functions
```

#### Audit Checklist
- [ ] Does the protocol use pull-over-push pattern?
- [ ] Can users specify alternative recipients for withdrawals?
- [ ] Are there try-catch wrappers around transfers?
- [ ] Is there admin/emergency recovery for stuck funds?
- [ ] Can orders/positions be cancelled if user is blacklisted?
- [ ] Is blacklist/pause behavior documented?

---

## 8. Inflation & First Depositor Attack Vulnerabilities

### Overview

Share-based token vaults (like ERC4626) are vulnerable to inflation attacks where the first depositor manipulates the share price to steal funds from subsequent depositors. Analysis of 35+ reports shows this attack pattern affects virtually all share-based vault implementations without proper safeguards.

> **📚 Source Reports for Deep Dive:**
> - `reports/erc20_token_findings/h-04-an-attacker-can-massively-inflate-the-share-value.md` (Y2K Finance - Sherlock)
> - `reports/erc20_token_findings/first-vault-deposit-can-cause-excessive-rounding.md` (Sentiment - Sherlock)
> - `reports/erc20_token_findings/initial-mint-front-run-inflation-attack.md` (Multiple protocols)
> - `reports/erc20_token_findings/vault-inflation-attack-is-possible.md`

### Vulnerability Description

#### Root Cause

1. **Share Price Manipulation**: First depositor can inflate share price by donating tokens
2. **Rounding Errors**: Integer division in share calculation rounds down, causing loss
3. **Empty Vault State**: No protection when vault has 0 shares or 0 assets
4. **Front-Running**: Attackers can front-run legitimate first deposits

#### Attack Mechanism
```
Initial State: Vault has 0 shares, 0 assets

1. Attacker deposits 1 wei → Gets 1 share
2. Attacker donates 1e18 tokens directly to vault
3. Vault State: 1 share, 1e18+1 assets
4. Share price: 1e18+1 per share
5. Victim deposits 2e18 tokens
6. Victim shares = (2e18 * 1) / (1e18+1) = 1 share (rounds down)
7. Attacker redeems: gets (1e18+1 + 2e18) / 2 = 1.5e18 tokens
8. Victim redeems: gets 1.5e18 tokens (lost 0.5e18!)
```

### Vulnerable Pattern Examples

**Example 1: Basic ERC4626 Vault Without Protection** [CRITICAL]
> 📖 Reference: `reports/erc20_token_findings/h-04-an-attacker-can-massively-inflate-the-share-value.md`
```solidity
// ❌ VULNERABLE: Standard share calculation without protection
contract VulnerableVault is ERC20 {
    IERC20 public asset;
    
    function deposit(uint256 assets) external returns (uint256 shares) {
        shares = totalSupply() == 0 
            ? assets  // First depositor gets 1:1
            : (assets * totalSupply()) / totalAssets();  // Vulnerable to inflation
        
        _mint(msg.sender, shares);
        asset.transferFrom(msg.sender, address(this), assets);
    }
    
    function totalAssets() public view returns (uint256) {
        return asset.balanceOf(address(this));  // Includes donations!
    }
}

// Attack:
// 1. deposit(1) → get 1 share
// 2. asset.transfer(vault, 1e18) → inflate price to 1e18+1 per share
// 3. Victim deposits 1.9e18 → gets 0 shares due to rounding!
```

**Example 2: Staking Pool Share Inflation** [HIGH]
> 📖 Reference: `reports/erc20_token_findings/first-vault-deposit-can-cause-excessive-rounding.md`
```solidity
// ❌ VULNERABLE: Staking pool with same issue
function stake(uint256 amount) external {
    uint256 shares;
    if (totalShares == 0) {
        shares = amount;
    } else {
        shares = (amount * totalShares) / stakingToken.balanceOf(address(this));
    }
    
    totalShares += shares;
    userShares[msg.sender] += shares;
    stakingToken.transferFrom(msg.sender, address(this), amount);
}
```

**Example 3: Lending Pool Interest Accumulation Attack** [HIGH]
```solidity
// ❌ VULNERABLE: Lending pool with accrued interest
contract LendingPool {
    function deposit(uint256 assets) external returns (uint256 shares) {
        uint256 supply = totalSupply();
        uint256 assets_plus_interest = asset.balanceOf(address(this)) + accruedInterest;
        
        shares = supply == 0
            ? assets
            : (assets * supply) / assets_plus_interest;  // Attacker can manipulate
        
        _mint(msg.sender, shares);
    }
}
```

**Example 4: Front-Running Attack on First Deposit** [CRITICAL]
> 📖 Reference: `reports/erc20_token_findings/initial-mint-front-run-inflation-attack.md`
```solidity
// ❌ VULNERABLE: Attacker front-runs legitimate first deposit
// 1. Victim sends TX: deposit(1000e18)
// 2. Attacker sees in mempool and front-runs:
//    - deposit(1)
//    - donate(1000e18)
// 3. Victim's TX executes: gets (1000e18 * 1) / (1000e18 + 1) = 0 shares!
// 4. Victim loses entire deposit
```

**Example 5: Yield Aggregator Vault** [HIGH]
```solidity
// ❌ VULNERABLE: Yield vault with external balance
contract YieldVault {
    function deposit(uint256 assets) external {
        uint256 shares;
        uint256 totalAssets_ = totalAssets();  // Reads from external protocol
        
        if (totalSupply() == 0) {
            shares = assets;
        } else {
            shares = (assets * totalSupply()) / totalAssets_;
        }
        // Attacker can manipulate external protocol's reported balance
    }
}
```

### Impact Analysis

#### Technical Impact
- First depositor can steal from all subsequent depositors
- Rounding causes significant fund loss
- Share price manipulation breaks vault economics
- Front-running makes any unprotected deposit dangerous

#### Business Impact
- **Frequency**: Found in 35+ of 761 analyzed reports (4.6%)
- **Severity**: Consistently HIGH to CRITICAL
- Complete loss of deposited funds possible
- Vault becomes unusable for legitimate users
- Requires coordinated attack before legitimate deposits

#### Affected Scenarios
- ERC4626 vaults
- Staking pools with share tokens
- Lending protocols with receipt tokens
- Yield aggregators
- Any share-based accounting system

### Secure Implementation

**Fix 1: Virtual Offset (OpenZeppelin Recommendation)**
```solidity
// ✅ SECURE: Add virtual shares and assets offset
contract SecureVault is ERC4626 {
    uint256 private constant OFFSET = 10 ** 3;  // 1000 virtual shares
    
    function _convertToShares(
        uint256 assets,
        Math.Rounding rounding
    ) internal view override returns (uint256) {
        return assets.mulDiv(
            totalSupply() + OFFSET,  // Add virtual shares
            totalAssets() + 1,        // Add virtual asset
            rounding
        );
    }
    
    function _convertToAssets(
        uint256 shares,
        Math.Rounding rounding
    ) internal view override returns (uint256) {
        return shares.mulDiv(
            totalAssets() + 1,
            totalSupply() + OFFSET,
            rounding
        );
    }
}
```

**Fix 2: Minimum First Deposit with Dead Shares**
```solidity
// ✅ SECURE: Burn minimum shares on first deposit
contract SecureVault is ERC4626 {
    uint256 public constant MINIMUM_SHARES = 1000;
    address public constant DEAD_ADDRESS = address(0xdead);
    
    function deposit(uint256 assets, address receiver) public override returns (uint256 shares) {
        if (totalSupply() == 0) {
            // First deposit must be significant
            require(assets >= MINIMUM_SHARES * 2, "Initial deposit too small");
            
            shares = assets;
            
            // Burn minimum shares to dead address
            _mint(DEAD_ADDRESS, MINIMUM_SHARES);
            _mint(receiver, shares - MINIMUM_SHARES);
        } else {
            shares = previewDeposit(assets);
            _mint(receiver, shares);
        }
        
        asset.safeTransferFrom(msg.sender, address(this), assets);
    }
}
```

**Fix 3: Internal Accounting (Not Using balanceOf)**
```solidity
// ✅ SECURE: Track assets internally, ignore donations
contract SecureVault is ERC4626 {
    uint256 private _totalManagedAssets;
    
    function totalAssets() public view override returns (uint256) {
        return _totalManagedAssets;  // Not balanceOf!
    }
    
    function deposit(uint256 assets, address receiver) public override returns (uint256 shares) {
        shares = previewDeposit(assets);
        
        _mint(receiver, shares);
        _totalManagedAssets += assets;  // Update internal tracking
        
        asset.safeTransferFrom(msg.sender, address(this), assets);
    }
    
    function withdraw(uint256 assets, address receiver, address owner) public override returns (uint256 shares) {
        shares = previewWithdraw(assets);
        
        _burn(owner, shares);
        _totalManagedAssets -= assets;  // Update internal tracking
        
        asset.safeTransfer(receiver, assets);
    }
}
```

**Fix 4: Minimum Deposit Amount**
```solidity
// ✅ SECURE: Require minimum deposit amount
contract SecureVault {
    uint256 public constant MIN_DEPOSIT = 1e18;  // 1 token minimum
    
    function deposit(uint256 assets) external {
        require(assets >= MIN_DEPOSIT, "Deposit too small");
        
        uint256 shares = _convertToShares(assets);
        require(shares > 0, "Zero shares");
        
        _mint(msg.sender, shares);
        asset.transferFrom(msg.sender, address(this), assets);
    }
}
```

**Fix 5: Initialize with Seed Deposit**
```solidity
// ✅ SECURE: Protocol seeds the vault at deployment
contract SecureVault {
    constructor(address _asset, uint256 seedDeposit) {
        asset = IERC20(_asset);
        
        // Protocol deposits seed amount at deployment
        if (seedDeposit > 0) {
            asset.transferFrom(msg.sender, address(this), seedDeposit);
            _mint(address(this), seedDeposit);  // Locked forever
        }
    }
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: ERC4626 or share-based vaults without virtual offset
- Pattern 2: Using balanceOf(address(this)) for totalAssets calculation
- Pattern 3: No minimum deposit/share requirements
- Pattern 4: Empty vault state (totalSupply == 0) special case without protection
- Pattern 5: No dead shares or initialization deposit
```

#### Audit Checklist
- [ ] Does the vault use virtual shares/assets offset?
- [ ] Is totalAssets() based on internal accounting (not balanceOf)?
- [ ] Are minimum deposit amounts enforced?
- [ ] Are dead shares minted on first deposit?
- [ ] Is the vault seeded at deployment?
- [ ] Is rounding behavior analyzed for edge cases?

---

## 9. Mint & Burn Vulnerabilities

### Overview

Improper access control, missing validation, and arithmetic errors in token minting and burning functions lead to unauthorized token creation, supply manipulation, and complete protocol compromise. Analysis of 63+ reports shows mint/burn vulnerabilities consistently result in CRITICAL severity issues.

> **📚 Source Reports for Deep Dive:**
> - `reports/erc20_token_findings/mint-perpetualyieldtokens-for-free-by-self-transfer.md` (Spectra - Sherlock)
> - `reports/erc20_token_findings/h-01-unchecked-erc20-transfers-can-cause-lock-up.md`
> - `reports/erc20_token_findings/unauthorized-token-minting.md`

### Vulnerability Description

#### Root Cause

1. **Missing Access Control**: Mint/burn functions without proper authorization
2. **Self-Transfer Exploits**: Minting tokens via self-referential operations
3. **Arithmetic Errors**: Underflow/overflow in burn calculations
4. **Flash Loan Attacks**: Temporary balance inflation for mint/burn manipulation
5. **Incorrect Burn Accounting**: Burning without proper balance verification

### Vulnerable Pattern Examples

**Example 1: Missing Access Control on Mint** [CRITICAL]
```solidity
// ❌ VULNERABLE: Anyone can mint tokens
function mint(address to, uint256 amount) external {
    // No access control!
    _mint(to, amount);
}
```

**Example 2: Self-Transfer Mint Exploit** [CRITICAL]
> 📖 Reference: `reports/erc20_token_findings/mint-perpetualyieldtokens-for-free-by-self-transfer.md`
```solidity
// ❌ VULNERABLE: Self-transfer triggers double-counting
function depositAndMint(address from, address to, uint256 amount) external {
    token.transferFrom(from, address(this), amount);
    yieldToken.mint(to, amount);
}

// Attack: Call depositAndMint(attacker, attacker, 0)
// If from == to, internal accounting may credit attacker twice
```

**Example 3: Burn Without Balance Check** [HIGH]
```solidity
// ❌ VULNERABLE: Burns more than sender owns
function burnFrom(address account, uint256 amount) external {
    // Missing balance check - relies on underflow protection
    _burn(account, amount);
    // In Solidity 0.7 without SafeMath, this could underflow
}
```

**Example 4: Incorrect Burn Accounting in Vault** [HIGH]
```solidity
// ❌ VULNERABLE: Burns shares but doesn't update internal accounting
function withdraw(uint256 shares) external {
    uint256 assets = convertToAssets(shares);
    _burn(msg.sender, shares);
    // Missing: totalAssets -= assets
    token.transfer(msg.sender, assets);
}
```

**Example 5: Flash Loan Mint Manipulation** [CRITICAL]
```solidity
// ❌ VULNERABLE: Flash loan can manipulate mint calculations
function mintBasedOnBalance(address user) external {
    uint256 balance = token.balanceOf(user);
    // Attacker flash loans tokens to inflate balance
    uint256 sharesToMint = (balance * totalShares) / totalAssets;
    _mint(user, sharesToMint);  // Mints inflated amount
}
```

### Impact Analysis

#### Technical Impact
- Unlimited token supply creation
- Total supply manipulation
- Protocol token value destruction
- Accounting invariant violations

#### Business Impact
- **Frequency**: Found in 63+ of 761 analyzed reports (8.3%)
- **Severity**: Consistently HIGH to CRITICAL
- Complete protocol drain possible
- Token value goes to zero
- User funds at immediate risk

### Secure Implementation

**Fix 1: Proper Access Control**
```solidity
// ✅ SECURE: Role-based access control
import {AccessControl} from "@openzeppelin/contracts/access/AccessControl.sol";

contract SecureToken is ERC20, AccessControl {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    
    function mint(address to, uint256 amount) external onlyRole(MINTER_ROLE) {
        _mint(to, amount);
    }
    
    function burn(address from, uint256 amount) external onlyRole(MINTER_ROLE) {
        require(balanceOf(from) >= amount, "Insufficient balance");
        _burn(from, amount);
    }
}
```

**Fix 2: Self-Transfer Protection**
```solidity
// ✅ SECURE: Prevent self-referential operations
function depositAndMint(address from, address to, uint256 amount) external {
    require(from != to, "Self-transfer not allowed");
    require(from != address(this), "Cannot deposit from self");
    
    token.transferFrom(from, address(this), amount);
    yieldToken.mint(to, amount);
}
```

**Fix 3: Supply Cap Enforcement**
```solidity
// ✅ SECURE: Enforce maximum supply
contract CappedToken is ERC20 {
    uint256 public constant MAX_SUPPLY = 1_000_000_000e18;
    
    function mint(address to, uint256 amount) external onlyMinter {
        require(totalSupply() + amount <= MAX_SUPPLY, "Exceeds max supply");
        _mint(to, amount);
    }
}
```

### Detection Patterns

#### Audit Checklist
- [ ] Are mint/burn functions properly access controlled?
- [ ] Is there a maximum supply cap?
- [ ] Are self-transfer edge cases handled?
- [ ] Is burn amount validated against balance?
- [ ] Are flash loan vectors considered?

---

## 10. Comprehensive Keyword Index

This section provides keywords optimized for vector search to help auditors find relevant vulnerability patterns.

### Primary Vulnerability Keywords

```
Transfer Vulnerabilities:
  transfer, transferFrom, safeTransfer, safeTransferFrom, 
  return_value, bool_return, silent_fail, unchecked_return,
  ERC20_transfer, token_transfer, transfer_revert

Approval Vulnerabilities:
  approve, allowance, increaseAllowance, decreaseAllowance,
  safeApprove, forceApprove, front_running, race_condition,
  USDT_approval, zero_approval, infinite_approval

Decimal Vulnerabilities:
  decimals, precision, scaling, normalization,
  1e18, 10**18, decimal_assumption, precision_loss,
  low_decimals, high_decimals, USDC_decimals, WBTC_decimals

Fee-on-Transfer:
  fee_on_transfer, FOT, deflationary, transfer_fee,
  balance_mismatch, actual_received, balance_before_after,
  SAFEMOON, reflection_token, elastic_supply

Rebasing Tokens:
  rebase, rebasing, stETH, aToken, AMPL,
  elastic_supply, balance_change, cached_balance,
  share_accounting, wstETH, wrapped_rebasing

ERC777:
  ERC777, tokensToSend, tokensReceived, hooks,
  reentrancy, callback, ERC1820, operator,
  imBTC, WETH777

Blacklist/Pause:
  blacklist, blocklist, pause, pausable,
  USDC_blacklist, USDT_freeze, frozen_funds,
  transfer_blocked, stuck_funds, DoS

Inflation Attack:
  inflation, first_depositor, share_manipulation,
  vault_attack, ERC4626, donation_attack,
  rounding_error, dead_shares, virtual_offset

Mint/Burn:
  mint, burn, _mint, _burn, supply_manipulation,
  access_control, unauthorized_mint, self_transfer,
  supply_cap, MAX_SUPPLY
```

### Protocol-Specific Keywords

```
DeFi Primitives:
  vault, lending, borrowing, collateral, liquidation,
  AMM, DEX, swap, pool, staking, yield,
  bridge, escrow, vesting, airdrop

Token Standards:
  ERC20, ERC777, ERC4626, ERC1155,
  IERC20, IERC20Metadata, SafeERC20

Common Tokens:
  USDC, USDT, DAI, WETH, WBTC, stETH, wstETH,
  aToken, cToken, yToken, PAXG, BUSD
```

---

## Summary & Quick Reference

### Vulnerability Frequency by Category

| Category | Reports | Percentage | Typical Severity |
|----------|---------|------------|------------------|
| Fee-on-Transfer | 72+ | 9.5% | MEDIUM-HIGH |
| Mint/Burn | 63+ | 8.3% | HIGH-CRITICAL |
| Transfer/Return Values | 87+ | 11.4% | MEDIUM-HIGH |
| Inflation/First Depositor | 35+ | 4.6% | HIGH-CRITICAL |
| Rebasing Tokens | 28+ | 3.7% | MEDIUM-CRITICAL |
| Blacklist/Pause | 28+ | 3.7% | MEDIUM-HIGH |
| ERC777 Reentrancy | 27+ | 3.5% | HIGH-CRITICAL |
| Approval/Allowance | 26+ | 3.4% | MEDIUM |
| Decimals/Precision | 23+ | 3.0% | HIGH-CRITICAL |

### Quick Mitigation Reference

| Vulnerability | Primary Mitigation |
|---------------|-------------------|
| Unchecked transfer | Use SafeERC20.safeTransfer() |
| Fee-on-transfer | Balance before/after check |
| Rebasing | Share-based accounting |
| Decimals | Dynamic normalization |
| ERC777 reentrancy | CEI pattern + ReentrancyGuard |
| Blacklist | Pull-over-push + alt recipient |
| Inflation attack | Virtual offset / dead shares |
| Approval front-run | increaseAllowance() |
| USDT approval | Approve 0 first |

---

## Related Vulnerabilities

This template compounds with:
- **Oracle Vulnerabilities**: Price manipulation affects token valuations
- **Access Control**: Authorization bypasses enable unauthorized minting
- **Reentrancy**: Token callbacks enable state manipulation
- **Flash Loans**: Temporary balance inflation attacks

---

## References

- [OpenZeppelin SafeERC20](https://docs.openzeppelin.com/contracts/4.x/api/token/erc20#SafeERC20)
- [ERC4626 Security Considerations](https://eips.ethereum.org/EIPS/eip-4626#security-considerations)
- [Trail of Bits: Building Secure Contracts](https://github.com/crytic/building-secure-contracts)
- [Weird ERC20 Tokens](https://github.com/d-xo/weird-erc20)

---

*Template generated from analysis of 761+ vulnerability reports from Sherlock, Code4rena, Spearbit, Pashov, and other audit platforms.*
