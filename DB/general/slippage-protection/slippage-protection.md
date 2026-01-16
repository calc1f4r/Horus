---
# Core Classification
vulnerability_class: slippage-protection
title: "Missing or Insufficient Slippage Protection"
category: DeFi/Token Operations
severity_range: "MEDIUM to HIGH"

# Affected Patterns
affected_operations:
  - AMM Swaps
  - Liquidity Operations
  - Leverage/Deleverage
  - Token Conversions
  - Vault Deposits/Withdrawals

# Attack Vectors
attack_vectors:
  - Sandwich Attacks
  - MEV Exploitation
  - Front-running
  - Price Manipulation

# Common Manifestations
manifestations:
  - Zero slippage parameters
  - Unused minAmountOut parameters
  - block.timestamp as deadline
  - Hardcoded zero values
  - No user-specified minimums

# Reference Reports
references:
  - file: "reports/yield_protocol_findings/h-31-unused-slippage-params.md"
    protocol: "Vader Protocol"
    severity: "HIGH"
    auditor: "Code4rena"
  - file: "reports/yield_protocol_findings/m-15-lack-of-slippage-protection-during-withdrawal-in-superpool-and-pool-contrac.md"
    protocol: "Sentiment V2"
    severity: "MEDIUM"
    auditor: "Sherlock"
  - file: "reports/yield_protocol_findings/insufficient-slippage-protection-for-liquidity-operations.md"
    protocol: "Hifi Finance"
    severity: "MEDIUM"
    auditor: "Quantstamp"
  - file: "reports/yield_protocol_findings/m-01-voltburnbuynsendtovolttreasury-function-is-subjected-to-a-sandwich-attack.md"
    protocol: "Kaizen"
    severity: "MEDIUM"
    auditor: "Shieldify"
  - file: "reports/yield_protocol_findings/h-06-no-slippage-checks-when-removing-leverage.md"
    protocol: "Peapods"
    severity: "HIGH"
    auditor: "Pashov Audit Group"
  - file: "reports/yield_protocol_findings/m-07-pendleadapter-provides-zero-slippage.md"
    protocol: "AdapterFinance"
    severity: "MEDIUM"
    auditor: "Pashov Audit Group"
  - file: "reports/yield_protocol_findings/m-02-dangerous-use-of-deadline-parameter.md"
    protocol: "Particle Protocol"
    severity: "MEDIUM"
    auditor: "Code4rena"
---

# Missing or Insufficient Slippage Protection

## Overview

Missing or insufficient slippage protection occurs when DeFi protocols fail to implement proper safeguards against price manipulation during token swaps, liquidity operations, or other value-exchanging transactions. This vulnerability enables attackers to execute sandwich attacks, front-running, and MEV extraction, resulting in users receiving significantly fewer tokens than expected or paying more than they should.

**Root Cause Statement**: This vulnerability exists because swap and liquidity operations lack user-specified minimum output parameters (slippage protection) or use ineffective deadline checks, allowing MEV bots and attackers to manipulate transaction ordering and extract value from pending transactions.

**Observed Frequency**: Very common pattern (15+ reports analyzed)
**Consensus Severity**: MEDIUM to HIGH

---

## Vulnerable Code Patterns

### Example 1: Unused Slippage Parameters (HIGH - Vader Protocol)

**Reference**: [h-31-unused-slippage-params.md](reports/yield_protocol_findings/h-31-unused-slippage-params.md)

```solidity
// VULNERABLE: Slippage parameters declared but never used
function addLiquidity(
    address tokenA,
    address tokenB,
    uint256 amountADesired,
    uint256 amountBDesired,
    uint256, // amountAMin = unused  // <-- NEVER CHECKED
    uint256, // amountBMin = unused  // <-- NEVER CHECKED
    address to,
    uint256 deadline
) external returns (uint256 amountA, uint256 amountB, uint256 liquidity) {
    // Parameters exist but are completely ignored
    // No validation against minimums occurs
    (amountA, amountB) = _addLiquidity(tokenA, tokenB, amountADesired, amountBDesired);
    // ...
}
```

**Why Vulnerable**: The function signature includes `amountAMin` and `amountBMin` parameters for slippage protection, but they are completely ignored in the implementation, giving users a false sense of security.

---

### Example 2: Zero Slippage in Swap Operations (MEDIUM - Kaizen)

**Reference**: [m-01-voltburnbuynsendtovolttreasury-function-is-subjected-to-a-sandwich-attack.md](reports/yield_protocol_findings/m-01-voltburnbuynsendtovolttreasury-function-is-subjected-to-a-sandwich-attack.md)

```solidity
// VULNERABLE: User can set zero slippage allowing sandwich attacks
function buyNSendToVoltTreasury(uint256 _amountVoltMin, uint32 _deadline)
    external
    notExpired(_deadline)
    onlyEOA
    notAmount0(erc20Bal(shogun))
{
    // ...
    _swapShogunForVolt(balance, _amountVoltMin, _deadline);
    // Problem: _amountVoltMin can be set to 0 by caller
    // No minimum slippage enforcement exists
}
```

**Attack Scenario**:
1. Pool has 1000 Shogun and 100 Volt tokens
2. Attacker swaps 9000 Shogun into pool first (gets 90 Volt, pool = 10000S:10V)
3. Victim's transaction executes with 0 slippage (gets only 0.91 Volt for 1000 Shogun)
4. Attacker swaps back 90 Volt (extracts 991 Shogun profit)

---

### Example 3: Missing Withdrawal Slippage Protection (MEDIUM - Sentiment V2)

**Reference**: [m-15-lack-of-slippage-protection-during-withdrawal-in-superpool-and-pool-contrac.md](reports/yield_protocol_findings/m-15-lack-of-slippage-protection-during-withdrawal-in-superpool-and-pool-contrac.md)

```solidity
// VULNERABLE: No slippage protection during bad debt events
function withdraw(uint256 poolId, uint256 assets, address receiver)
    external
    returns (uint256 shares)
{
    // No minimum shares parameter
    // If bad debt occurs while tx is pending, user burns more shares than expected
    shares = _convertToShares(assets, pool.totalDepositAssets, pool.totalDepositShares);
    // User expected to burn 500 shares for 500 assets
    // But if totalAssets dropped from 2000 to 1500 (bad debt), burns 666 shares instead
}
```

**Scenario**:
- `pool.totalAssets = 2000`, `pool.totalShares = 2000`
- User wants to withdraw 500 assets, expecting to burn 500 shares
- Bad debt liquidation occurs: `totalAssets` drops to 1500
- User burns `500 * 2000 / 1500 = 666` shares (33% more than expected)

---

### Example 4: block.timestamp as Deadline (MEDIUM - Particle Protocol)

**Reference**: [m-02-dangerous-use-of-deadline-parameter.md](reports/yield_protocol_findings/m-02-dangerous-use-of-deadline-parameter.md)

```solidity
// VULNERABLE: Using block.timestamp defeats the purpose of deadline
(tokenId, liquidity, amount0Minted, amount1Minted) = UNI_POSITION_MANAGER.mint(
    INonfungiblePositionManager.MintParams({
        token0: params.token0,
        token1: params.token1,
        fee: params.fee,
        tickLower: params.tickLower,
        tickUpper: params.tickUpper,
        amount0Desired: params.amount0ToMint,
        amount1Desired: params.amount1ToMint,
        amount0Min: params.amount0Min,
        amount1Min: params.amount1Min,
        recipient: address(this),
        deadline: block.timestamp  // <-- ALWAYS PASSES, NO PROTECTION
    })
);
```

**Why Vulnerable**: `block.timestamp` is set when the transaction is mined, so `deadline: block.timestamp` always satisfies `block.timestamp <= block.timestamp`. Pending transactions can be executed at any later time by validators or MEV bots.

---

### Example 5: Zero Slippage in Leverage Operations (HIGH - Peapods)

**Reference**: [h-06-no-slippage-checks-when-removing-leverage.md](reports/yield_protocol_findings/h-06-no-slippage-checks-when-removing-leverage.md)

```solidity
// VULNERABLE: Exact output swap with no slippage protection
function _removeLeverage(...) internal {
    // Swaps pod token for borrow token
    _podAmtRemaining = _swapPodForBorrowToken(
        _pod, 
        _borrowToken, 
        _podAmtReceived, 
        _borrowAmtNeededToSwap  // amountInMax set to all available pods
    );
    // No minPodAmtRemaining check!
    // Attacker can sandwich to consume all pod tokens in the swap
}
```

**Impact**: User removing leverage can have nearly all their pod tokens consumed by a sandwich attack, receiving far fewer tokens than expected.

---

### Example 6: Hardcoded Zero Minimums (MEDIUM - AdapterFinance)

**Reference**: [m-07-pendleadapter-provides-zero-slippage.md](reports/yield_protocol_findings/m-07-pendleadapter-provides-zero-slippage.md)

```python
# VULNERABLE: Intentionally setting 0 for minimum output (Vyper)
netPyOut, netSyInterm = PendleRouter(pendleRouter).mintPyFromToken(
    self,
    yt_token,
    0,  # minPyOut = 0, no slippage protection
    inp
)

PendleRouter(pendleRouter).swapExactYtForPt(
    self,
    pendleMarket,
    netPyOut,
    0,  # minPtOut = 0, no slippage protection
    pg.approx_params_swapExactYtForPt
)
```

**Issue**: Comment states "minPtOut=0 is intentional, it's up to the vault to revert if it does not like what it sees" - but the vault has no slippage check either, creating a complete gap in protection.

---

### Example 7: Missing Liquidity Operation Protection (MEDIUM - Hifi Finance)

**Reference**: [insufficient-slippage-protection-for-liquidity-operations.md](reports/yield_protocol_findings/insufficient-slippage-protection-for-liquidity-operations.md)

```solidity
// VULNERABLE: No minimum/maximum ratio checks for liquidity operations
function addLiquidity(...) external {
    // Only checks maxHTokenRequired (protects against hToken price going up)
    // Missing minHTokenRequired (no protection against underlying price going up)
    require(hTokenAmount <= maxHTokenRequired, "Too many hTokens");
    // No protection for the other direction!
}

function removeLiquidity(...) external {
    // No minHTokenOut or minUnderlyingOut parameters
    // Liquidity providers can receive far less than expected
}
```

**Affected Functions** (20+ in this single protocol):
- `addLiquidity()`, `removeLiquidity()`, `removeLiquidityAndRedeem()`
- All `*WithSignature()` variants

---

## Secure Implementation Patterns

### Fix 1: User-Specified Minimum Output

```solidity
// SECURE: User specifies minimum acceptable output
function swap(
    address tokenIn,
    address tokenOut,
    uint256 amountIn,
    uint256 minAmountOut,  // User-specified minimum
    address recipient,
    uint256 deadline
) external returns (uint256 amountOut) {
    require(block.timestamp <= deadline, "Transaction expired");
    
    amountOut = _executeSwap(tokenIn, tokenOut, amountIn);
    
    // Enforce slippage protection
    require(amountOut >= minAmountOut, "Insufficient output amount");
    
    IERC20(tokenOut).transfer(recipient, amountOut);
}
```

---

### Fix 2: Maximum Shares for Withdrawals

```solidity
// SECURE: User specifies maximum shares willing to burn
function withdraw(
    uint256 poolId,
    uint256 assets,
    address receiver,
    uint256 maxSharesBurned  // Slippage protection for withdrawals
) external returns (uint256 shares) {
    shares = _convertToShares(assets, pool.totalDepositAssets, pool.totalDepositShares);
    
    // Protect against exchange rate changes (e.g., bad debt)
    require(shares <= maxSharesBurned, "Slippage exceeded");
    
    _burn(msg.sender, shares);
    IERC20(pool.asset).transfer(receiver, assets);
}
```

---

### Fix 3: User-Provided Deadline

```solidity
// SECURE: User provides deadline, not block.timestamp
function mint(
    MintParams calldata params,
    uint256 deadline  // User-provided deadline
) external returns (uint256 tokenId, uint256 liquidity) {
    require(block.timestamp <= deadline, "Transaction expired");
    
    (tokenId, liquidity, , ) = UNI_POSITION_MANAGER.mint(
        INonfungiblePositionManager.MintParams({
            token0: params.token0,
            token1: params.token1,
            // ...
            deadline: deadline  // Forward user's deadline
        })
    );
}
```

---

### Fix 4: Minimum Enforcement for Protocol Operations

```solidity
// SECURE: Protocol enforces minimum slippage even when user can't specify
function buyNSendToVoltTreasury(uint256 _deadline) external {
    uint256 balance = erc20Bal(shogun);
    
    // Calculate expected output using oracle or TWAP
    uint256 expectedVolt = getExpectedOutput(balance);
    
    // Enforce minimum 95% of expected (5% max slippage)
    uint256 minVoltOut = (expectedVolt * 95) / 100;
    
    _swapShogunForVolt(balance, minVoltOut, _deadline);
}
```

---

### Fix 5: Bidirectional Liquidity Protection

```solidity
// SECURE: Protect both directions in liquidity operations
function addLiquidity(
    uint256 amountDesired,
    uint256 minLpTokens,      // Minimum LP tokens to receive
    uint256 maxTokensSpent,   // Maximum tokens willing to spend
    uint256 deadline
) external returns (uint256 lpTokens, uint256 tokensUsed) {
    require(block.timestamp <= deadline, "Expired");
    
    (lpTokens, tokensUsed) = _addLiquidity(amountDesired);
    
    require(lpTokens >= minLpTokens, "Insufficient LP tokens");
    require(tokensUsed <= maxTokensSpent, "Too many tokens used");
}

function removeLiquidity(
    uint256 lpTokens,
    uint256 minTokenAOut,     // Minimum token A to receive
    uint256 minTokenBOut,     // Minimum token B to receive
    uint256 deadline
) external returns (uint256 amountA, uint256 amountB) {
    require(block.timestamp <= deadline, "Expired");
    
    (amountA, amountB) = _removeLiquidity(lpTokens);
    
    require(amountA >= minTokenAOut, "Insufficient token A");
    require(amountB >= minTokenBOut, "Insufficient token B");
}
```

---

## Impact Analysis

### Technical Impact
- **State Corruption**: Users receive incorrect token amounts
- **Value Extraction**: MEV bots and attackers extract value from transactions
- **Transaction Failures**: Users may need to retry transactions multiple times

### Business Impact
- **Direct Fund Loss**: Users lose value through sandwich attacks (MEDIUM-HIGH)
- **User Trust Erosion**: Protocol reputation damage
- **Increased Costs**: Users pay more gas for failed/retried transactions

### Affected Scenarios (by frequency)
| Scenario | Frequency | Severity |
|----------|-----------|----------|
| AMM Swaps without minOut | Very Common | HIGH |
| Liquidity operations | Common | MEDIUM |
| Vault deposits/withdrawals | Common | MEDIUM |
| Leverage operations | Less Common | HIGH |
| Cross-protocol integrations | Common | MEDIUM |

---

## Detection Patterns

### Semgrep Rules

```yaml
rules:
  - id: zero-slippage-swap
    patterns:
      - pattern-either:
          - pattern: $ROUTER.swap(..., 0, ...)
          - pattern: $ROUTER.swapExactTokensForTokens(..., 0, ...)
          - pattern: swapExactTokensForTokens($AMT, 0, ...)
    message: "Swap with zero slippage protection"
    severity: ERROR

  - id: block-timestamp-deadline
    patterns:
      - pattern: deadline: block.timestamp
    message: "Using block.timestamp as deadline provides no protection"
    severity: WARNING

  - id: unused-slippage-param
    patterns:
      - pattern: |
          function $FUNC(..., uint256, ...) {  // unnamed parameter
            ...
          }
      - pattern-not: |
          function $FUNC(..., uint256 $MIN, ...) {
            ...
            require($_ >= $MIN, ...);
            ...
          }
    message: "Slippage parameter may be unused"
    severity: WARNING
```

### Manual Audit Checklist

- [ ] All swap functions have `minAmountOut` parameter that is enforced
- [ ] All liquidity operations have min/max parameters for both tokens
- [ ] Deadline is user-provided, not `block.timestamp`
- [ ] Vault deposits have `minShares` protection
- [ ] Vault withdrawals have `maxShares` protection
- [ ] Protocol-initiated swaps use oracle/TWAP for minimum calculation
- [ ] Cross-protocol calls preserve slippage parameters

---

## Real-World Examples

| Protocol | Vulnerability | Severity | Auditor |
|----------|--------------|----------|---------|
| Vader Protocol | Unused slippage params in addLiquidity | HIGH | Code4rena |
| Sentiment V2 | No withdrawal slippage protection | MEDIUM | Sherlock |
| Hifi Finance | 20+ functions missing slippage checks | MEDIUM | Quantstamp |
| Kaizen | Zero slippage allowed in swap | MEDIUM | Shieldify |
| Peapods | No slippage in leverage removal | HIGH | Pashov |
| AdapterFinance | Hardcoded zero minimums in Pendle | MEDIUM | Pashov |
| Particle Protocol | block.timestamp as deadline | MEDIUM | Code4rena |

---

## Keywords for Search

**Primary Terms**: slippage, minAmountOut, minAmount, amountOutMin, slippage protection
**Attack Terms**: sandwich attack, frontrunning, MEV, price manipulation
**Parameter Terms**: deadline, block.timestamp, minOut, maxIn, minShares
**Operation Terms**: swap, liquidity, leverage, withdrawal, deposit, redeem
**Impact Terms**: fund loss, value extraction, unfavorable price
