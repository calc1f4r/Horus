---
title: "Uniswap V4 Hook Security and Token Compatibility Vulnerabilities"
vulnerability_class: "Hook Security / Token Compatibility"
severity: "HIGH to CRITICAL"
chain: "Multi-chain"
affected_protocols:
  - "Uniswap V4"
  - "Bunni V2"
  - "Vii Finance"
  - "Licredity"
  - "BMX Deli Swap"
  - "SolidlyV3"
  - "Numoen"
tags:
  - "uniswap-v4"
  - "hooks"
  - "reentrancy"
  - "fee-on-transfer"
  - "non-standard-erc20"
  - "gas-griefing"
  - "callback-security"
  - "malicious-hook"
last_updated: "2025-01-17"
---

# Uniswap V4 Hook Security and Token Compatibility Vulnerabilities

## Overview

Uniswap V4 introduces a powerful hook system that allows custom logic execution at various points during pool operations. While this enables unprecedented customization, it also creates new attack surfaces through malicious hooks, gas manipulation, reentrancy via hooks, and unverified hook behavior. Additionally, concentrated liquidity AMMs across V3/V4 frequently encounter compatibility issues with non-standard ERC20 tokens.

**Root Cause Statement:**
> "This vulnerability exists because protocols integrating with Uniswap V4 fail to properly validate hook implementations, enforce gas limits on hook callbacks, prevent reentrancy through hook execution paths, or handle non-standard ERC20 token behaviors (fee-on-transfer, missing return values, rebasing), allowing attackers to bypass security controls, drain funds, cause DoS, or corrupt accounting through malicious hooks and incompatible tokens."

**Observed Frequency:** 35+ reports analyzed covering hook reentrancy, gas griefing, malicious hooks, and token compatibility issues.

---

## Vulnerable Pattern Examples

### Pattern 1: Malicious Hook Bypassing Reentrancy Guards (CRITICAL)

Hooks with malicious implementations can call `unlockForRebalance()` to bypass global reentrancy protection and drain funds from all legitimate pools.

**Reference**: [pools-configured-with-a-malicious-hook-can-bypass-the-bunnihub-re-entrancy-guard.md](../../../reports/constant_liquidity_amm/pools-configured-with-a-malicious-hook-can-bypass-the-bunnihub-re-entrancy-guard.md) (Cyfrin - Bunni, CRITICAL)

```solidity
// VULNERABLE: Hook not constrained to canonical implementation
function deployBunniToken(DeployBunniTokenParams calldata params) external {
    // No validation that hooks is the canonical BunniHook!
    if (address(params.hooks) == address(0)) revert BunniHub__HookCannotBeZero();
    if (!params.hooks.isValidParams(params.hookParams)) revert BunniHub__InvalidHookParams();
    // Attacker can deploy pool with malicious hook
}

// Reentrancy lock uses global transient storage
function lockForRebalance(PoolKey calldata key) external {
    if (msg.sender != address(key.hooks)) revert BunniHub__Unauthorized();
    _nonReentrantBefore();  // Sets global lock
}

function unlockForRebalance(PoolKey calldata key) external {
    if (msg.sender != address(key.hooks)) revert BunniHub__Unauthorized();
    _nonReentrantAfter();  // Clears global lock - DANGEROUS!
}

// Attack:
// 1. Deploy pool with malicious hook
// 2. Call lockForRebalance() to set global reentrancy lock
// 3. Call unlockForRebalance() to CLEAR global lock
// 4. Now reenter BunniHub and drain legitimate pools

// SECURE: Whitelist valid hooks or use per-pool reentrancy guards
mapping(address => bool) public whitelistedHooks;

function deployBunniToken(DeployBunniTokenParams calldata params) external {
    require(whitelistedHooks[address(params.hooks)], "Hook not whitelisted");
    // ...
}
```

---

### Pattern 2: Gas Limit Underestimation in Hook Callbacks (HIGH)

Uniswap V4's `notifyUnsubscribe` has gas limits to protect against malicious subscribers, but underestimation allows attackers to force unsubscribe while keeping positions in gauges.

**Reference**: [h-1-gas-consumed-in-notifyunsubscribe-is-underestimated-during-tests-and-is-grea.md](../../../reports/constant_liquidity_amm/h-1-gas-consumed-in-notifyunsubscribe-is-underestimated-during-tests-and-is-grea.md) (Sherlock - BMX Deli Swap, HIGH)

```solidity
// Uniswap V4 Notifier protection mechanism
function unsubscribe(uint256 tokenId) external {
    if (address(_subscriber).code.length > 0) {
        // Require minimum gas for subscriber callback
        if (gasleft() < unsubscribeGasLimit) GasLimitTooLow.selector.revertWith();
        
        // Try/catch protects against reverting subscriber
        try _subscriber.notifyUnsubscribe{gas: unsubscribeGasLimit}(tokenId) {} catch {}
    }
}

// VULNERABLE: Subscriber callback exceeds gas limit
// unsubscribeGasLimit on Base = 300,000
// Actual gas consumed can exceed 300,000 without pre-warming
function notifyUnsubscribe(uint256 tokenId) external {
    // Complex operations that consume > 300,000 gas
    // When cold storage is accessed, gas costs spike
    _updateRewards(tokenId);  // Multiple cold SLOADs
    _processIncentives(tokenId);  // More cold storage
    _updateGaugeAccounting(tokenId);  // Even more
}

// Attack:
// 1. Provide liquidity, subscribe to PositionManagerAdapter
// 2. Call unsubscribe with gas limit that causes OOG in notifyUnsubscribe
// 3. Uniswap V4 successfully unsubscribes (try/catch catches OOG)
// 4. But Deli gauge accounting NOT updated (call failed)
// 5. Position liquidity remains in gauge forever, diluting rewards

// SECURE: Optimize gas or increase unsubscribeGasLimit
function notifyUnsubscribe(uint256 tokenId) external {
    // Use minimal storage operations
    // Pre-warm storage slots in subscribe
    // Or: request higher unsubscribeGasLimit from Uniswap governance
}
```

---

### Pattern 3: Hook Callback Fee Farming via Self-Triggered Backrun (HIGH)

Hook callbacks that auto-execute trades based on price thresholds can be exploited by LPs to farm fees.

**Reference**: [self-triggered-licredity_afterswap-back-run-enables-lp-fee-farming.md](../../../reports/constant_liquidity_amm/self-triggered-licredity_afterswap-back-run-enables-lp-fee-farming.md) (Cyfrin - Licredity, HIGH)

```solidity
// VULNERABLE: Auto back-run when price hits threshold
function _afterSwap(
    PoolKey calldata poolKey,
    IPoolManager.SwapParams calldata params,
    BalanceDelta balanceDelta
) internal override {
    (uint160 sqrtPriceX96,,,) = poolManager.getSlot0(poolKey.toId());
    
    // When price <= 1, auto-execute back-run swap
    if (sqrtPriceX96 <= ONE_SQRT_PRICE_X96) {
        // Back-run pays fees to LPs!
        IPoolManager.SwapParams memory backrunParams = IPoolManager.SwapParams(
            false,  // opposite direction
            -balanceDelta.amount0(),
            MAX_SQRT_PRICE_X96 - 1
        );
        poolManager.swap(poolKey, backrunParams, "");
    }
}

// Attack:
// 1. Attacker provides concentrated liquidity around price = 1
// 2. Swap to push price slightly below 1, earning back swap fees as LP
// 3. Hook auto-triggers back-run, LP earns fees again!
// 4. Redeem position at ~1:1 exchange rate
// 5. Repeat to farm fees continuously

// SECURE: Add rate limiting or require external trigger
uint256 public lastBackrunTime;
uint256 public constant BACKRUN_COOLDOWN = 1 hours;

function _afterSwap(...) internal override {
    if (sqrtPriceX96 <= ONE_SQRT_PRICE_X96) {
        require(block.timestamp >= lastBackrunTime + BACKRUN_COOLDOWN, "Cooldown");
        lastBackrunTime = block.timestamp;
        // Execute backrun
    }
}
```

---

### Pattern 4: Fee-on-Transfer Token Incompatibility (MEDIUM)

AMMs that assume `balanceAfter - balanceBefore == transferAmount` break with fee-on-transfer tokens.

**Reference**: [m-01-fee-on-transfer-tokens-will-not-behave-as-expected.md](../../../reports/constant_liquidity_amm/m-01-fee-on-transfer-tokens-will-not-behave-as-expected.md) (Code4rena - Numoen, MEDIUM)

```solidity
// VULNERABLE: Assumes transfer amount equals received amount
function mint(
    address to,
    uint256 collateral,
    bytes calldata data
) external nonReentrant returns (uint256 shares) {
    // Calculate shares based on collateral amount
    uint256 liquidity = convertCollateralToLiquidity(collateral);
    shares = convertLiquidityToShare(liquidity);
    
    uint256 balanceBefore = Balance.balance(token1);
    IMintCallback(msg.sender).mintCallback(collateral, amount0, amount1, liquidity, data);
    uint256 balanceAfter = Balance.balance(token1);
    
    // REVERTS for fee-on-transfer tokens!
    // balanceAfter = balanceBefore + collateral - fee
    // balanceBefore + collateral > balanceAfter
    if (balanceAfter < balanceBefore + collateral) revert InsufficientInputError();
}

// SECURE: Use actual received amount
function mint(...) external nonReentrant returns (uint256 shares) {
    uint256 balanceBefore = Balance.balance(token1);
    IMintCallback(msg.sender).mintCallback(collateral, amount0, amount1, liquidity, data);
    uint256 balanceAfter = Balance.balance(token1);
    
    // Calculate based on ACTUAL received amount
    uint256 actualReceived = balanceAfter - balanceBefore;
    uint256 liquidity = convertCollateralToLiquidity(actualReceived);
    shares = convertLiquidityToShare(liquidity);
    
    require(shares > 0, "Zero shares");
}
```

---

### Pattern 5: Non-Standard ERC20 Return Value Handling (MEDIUM)

Tokens like USDT and BNB don't return `bool` on transfer, causing reverts with standard interfaces.

**Reference**: [m-01-pools-are-incompatible-with-non-standard-erc20-tokens.md](../../../reports/constant_liquidity_amm/m-01-pools-are-incompatible-with-non-standard-erc20-tokens.md) (Pashov - SolidlyV3, MEDIUM)

```solidity
// VULNERABLE: Expects bool return value
function transfer(address token, address to, uint256 amount) internal {
    // USDT doesn't return bool - this reverts!
    bool success = IERC20(token).transfer(to, amount);
    require(success, "Transfer failed");
}

// Also vulnerable: Not checking return value
function transferUnsafe(address token, address to, uint256 amount) internal {
    // ZRX returns false on failure instead of reverting
    IERC20(token).transfer(to, amount);
    // No check - silent failure!
}

// SECURE: Use SafeERC20 or TransferHelper
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
using SafeERC20 for IERC20;

function transferSafe(address token, address to, uint256 amount) internal {
    IERC20(token).safeTransfer(to, amount);
}

// Alternative: Low-level call with return data handling
function transferRobust(address token, address to, uint256 amount) internal {
    (bool success, bytes memory data) = token.call(
        abi.encodeWithSelector(IERC20.transfer.selector, to, amount)
    );
    require(
        success && (data.length == 0 || abi.decode(data, (bool))),
        "Transfer failed"
    );
}
```

---

### Pattern 6: Hook Collision in Token Accounting (MEDIUM)

When Bunni pools use Bunni tokens as underlying assets, hook callbacks can corrupt accounting due to balance collisions.

**Reference**: [collision-between-rebalance-order-consideration-tokens-and-am-amm-fees-for-bunni.md](../../../reports/constant_liquidity_amm/collision-between-rebalance-order-consideration-tokens-and-am-amm-fees-for-bunni.md) (Cyfrin - Bunni, MEDIUM)

```solidity
// VULNERABLE: Balance check doesn't account for am-AMM bid during callback
function _rebalancePreHook(HookArgs memory hookArgs) internal {
    // Cache output balance BEFORE callback
    uint256 outputBalanceBefore = hookArgs.postHookArgs.currency.balanceOfSelf();
    assembly ("memory-safe") {
        tstore(REBALANCE_OUTPUT_BALANCE_SLOT, outputBalanceBefore)
    }
}

// am-AMM bid happens during sourceConsideration callback
// This ADDS Bunni tokens to hook balance!

function _rebalancePostHook(PostHookArgs memory args) internal {
    uint256 outputBalanceBefore;
    assembly ("memory-safe") {
        outputBalanceBefore := tload(REBALANCE_OUTPUT_BALANCE_SLOT)
    }
    
    // Current balance includes am-AMM bid tokens!
    uint256 orderOutputAmount = args.currency.balanceOfSelf();
    orderOutputAmount -= outputBalanceBefore;  // Inflated by am-AMM!
    
    // Accounting now corrupted
}

// Attack (for pools using Bunni tokens):
// 1. Deploy Bunni pool with Bunni token as underlying
// 2. During rebalance, perform am-AMM bid in sourceConsideration
// 3. This adds Bunni tokens to hook balance
// 4. orderOutputAmount inflated, accounting corrupted

// SECURE: Track am-AMM separately or exclude Bunni token pools
function _rebalancePostHook(PostHookArgs memory args) internal {
    uint256 amAmmReceived = /* track separately */;
    uint256 orderOutputAmount = args.currency.balanceOfSelf() - outputBalanceBefore - amAmmReceived;
}
```

---

### Pattern 7: Uniswap V4 Wrapper Position Fee Theft (HIGH)

Partial unwrap of V4 positions doesn't decrement `tokensOwed` state, enabling repeated fee theft.

**Reference**: [fees-can-be-stolen-from-partially-unwrapped-uniswapv4wrapper-positions.md](../../../reports/constant_liquidity_amm/fees-can-be-stolen-from-partially-unwrapped-uniswapv4wrapper-positions.md) (Cyfrin - Vii Finance, HIGH)

```solidity
// VULNERABLE: tokensOwed never decremented after partial unwrap
function _unwrap(address to, uint256 tokenId, uint256 amount, bytes calldata extraData) internal override {
    PositionState memory positionState = _getPositionState(tokenId);

    (uint256 pendingFees0, uint256 pendingFees1) = _pendingFees(positionState);
    _accumulateFees(tokenId, pendingFees0, pendingFees1);

    uint128 liquidityToRemove = proportionalShare(tokenId, positionState.liquidity, amount).toUint128();
    (uint256 amount0, uint256 amount1) = _principal(positionState, liquidityToRemove);

    _decreaseLiquidity(tokenId, liquidityToRemove, ActionConstants.MSG_SENDER, extraData);

    // Transfer proportional fees
    poolKey.currency0.transfer(to, amount0 + proportionalShare(tokenId, tokensOwed[tokenId].fees0Owed, amount));
    poolKey.currency1.transfer(to, amount1 + proportionalShare(tokenId, tokensOwed[tokenId].fees1Owed, amount));
    
    // BUG: tokensOwed NOT decremented!
    // Stale state can be reused after re-wrapping
}

// Attack:
// 1. Alice wraps Uniswap V4 position, accumulates fees
// 2. Alice fully unwraps using partial unwrap function
// 3. tokensOwed still contains fee values in storage
// 4. Alice retrieves underlying position, adds liquidity
// 5. Alice re-wraps same position
// 6. Alice can claim fees again using stale tokensOwed!

// SECURE: Decrement tokensOwed after distribution
function _unwrap(...) internal override {
    // ... existing code ...
    
    uint256 fees0Distributed = proportionalShare(tokenId, tokensOwed[tokenId].fees0Owed, amount);
    uint256 fees1Distributed = proportionalShare(tokenId, tokensOwed[tokenId].fees1Owed, amount);
    
    poolKey.currency0.transfer(to, amount0 + fees0Distributed);
    poolKey.currency1.transfer(to, amount1 + fees1Distributed);
    
    // Decrement tokensOwed
    tokensOwed[tokenId].fees0Owed -= fees0Distributed;
    tokensOwed[tokenId].fees1Owed -= fees1Distributed;
}
```

---

### Pattern 8: Reentrancy via Yield Strategy Trade Path (CRITICAL)

External swap paths in yield strategies allow reentrancy through malicious tokens.

**Reference**: [redeemnative-reentrancy-enables-permanent-fund-freeze-systemic-misaccounting-and.md](../../../reports/constant_liquidity_amm/redeemnative-reentrancy-enables-permanent-fund-freeze-systemic-misaccounting-and.md) (MixBytes - Notional Finance, CRITICAL)

```solidity
// VULNERABLE: External swap during redemption allows reentrancy
function redeemNative(uint256 shares, bytes calldata exchangeData) external {
    uint256 yieldTokensBefore = yieldToken.balanceOf(address(this));
    
    // _burnShares calls _executeTrade which does external swap
    _burnShares(shares, exchangeData);  // External call here!
    
    uint256 yieldTokensAfter = yieldToken.balanceOf(address(this));
    uint256 yieldTokensRedeemed = yieldTokensBefore - yieldTokensAfter;
    
    // Update accounting based on pre-reentrancy snapshot
    s_yieldTokenBalance -= yieldTokensRedeemed;  // DOUBLE SUBTRACTION!
}

// Attack using malicious token in swap path:
// 1. Attacker deploys malicious ERC20
// 2. Creates Uniswap V2 pools: yieldToken -> maliciousToken -> asset
// 3. Calls redeemNative with swap path through malicious token
// 4. Malicious token's transfer() reenters via initiateWithdraw()
// 5. Withdraw request manager transfers N tokens, decrements s_yieldTokenBalance
// 6. Original redeemNative continues, subtracts again
// 7. Result: s_yieldTokenBalance decremented 2x, tokens frozen

// SECURE: Add reentrancy guard to all entry points
function redeemNative(...) external nonReentrant {
    // ...
}

function initiateWithdraw(...) external nonReentrant {
    // ...
}

// Also: Validate swap path doesn't contain untrusted tokens
```

---

### Pattern 9: Dynamic LDF Tick Bound Overflow (MEDIUM)

Dynamic Liquidity Distribution Functions (LDFs) can have tick bounds overflow after shift operations.

**Reference**: [dos-of-bunni-pools-configured-with-dynamic-ldfs-due-to-insufficient-validation-o.md](../../../reports/constant_liquidity_amm/dos-of-bunni-pools-configured-with-dynamic-ldfs-due-to-insufficient-validation-o.md) (Cyfrin - Bunni, MEDIUM)

```solidity
// VULNERABLE: tickUpper not validated after shift
function query(PoolKey calldata key, int24 roundedTick, ...) external view override returns (...) {
    (int24 tickLower, int24 tickUpper, ShiftMode shiftMode) =
        LibUniformDistribution.decodeParams(twapTick, key.tickSpacing, ldfParams);
    
    (bool initialized, int24 lastTickLower) = _decodeState(ldfState);
    
    if (initialized) {
        int24 tickLength = tickUpper - tickLower;
        tickLower = enforceShiftMode(tickLower, lastTickLower, shiftMode);
        tickUpper = tickLower + tickLength;  // CAN EXCEED maxUsableTick!
    }
    
    // Reverts with InvalidTick() if tickUpper > MAX_TICK
    (liquidityDensityX96_, ...) = LibUniformDistribution.query(
        roundedTick, key.tickSpacing, tickLower, tickUpper
    );
}

// Attack:
// 1. Create pool with LDF at edge of usable range
// 2. Wait for shift to trigger
// 3. Shift causes tickUpper to exceed maxUsableTick
// 4. All pool operations now revert with InvalidTick()

// SECURE: Cap tickUpper after shift
if (initialized) {
    int24 tickLength = tickUpper - tickLower;
    tickLower = enforceShiftMode(tickLower, lastTickLower, shiftMode);
    tickUpper = tickLower + tickLength;
    
    // Validate and cap
    int24 maxUsableTick = TickMath.maxUsableTick(key.tickSpacing);
    if (tickUpper > maxUsableTick) {
        tickUpper = maxUsableTick;
        tickLower = tickUpper - tickLength;  // Adjust lower too
    }
}
```

---

### Pattern 10: am-AMM Manager Verification Bypass (MEDIUM)

Not checking if am-AMM is disabled allows stale managers to fulfill orders.

**Reference**: [m-14-bunnizone-does-not-verify-amamm-manager-properly.md](../../../reports/constant_liquidity_amm/m-14-bunnizone-does-not-verify-amamm-manager-properly.md) (Pashov - Bunni, MEDIUM)

```solidity
// VULNERABLE: Doesn't check if am-AMM is disabled
function validate(
    OrderDetails calldata details,
    address fulfiller,
    PoolKey calldata key
) external view returns (bool) {
    PoolId id = key.toId();
    IAmAmm amAmm = IAmAmm(address(key.hooks));
    
    // Gets top bid without checking if am-AMM enabled!
    IAmAmm.Bid memory topBid = amAmm.getTopBid(id);
    
    // Allows stale manager even if am-AMM disabled
    return isWhitelisted[fulfiller] || topBid.manager == fulfiller;
}

// Attack:
// 1. Become am-AMM manager for pool
// 2. Admin disables am-AMM for the pool
// 3. Stale manager can still fulfill rebalance orders
// 4. Manager benefits from rebalances they shouldn't control

// SECURE: Check am-AMM enabled status
function validate(...) external view returns (bool) {
    PoolId id = key.toId();
    IAmAmm amAmm = IAmAmm(address(key.hooks));
    
    // Check if am-AMM is enabled
    if (!amAmm.getAmAmmEnabled(id)) {
        return isWhitelisted[fulfiller];  // Only whitelisted allowed
    }
    
    IAmAmm.Bid memory topBid = amAmm.getTopBid(id);
    return isWhitelisted[fulfiller] || topBid.manager == fulfiller;
}
```

---

## Secure Implementation Examples

### Secure Pattern 1: Hook Whitelist and Per-Pool Reentrancy

```solidity
// SECURE: Whitelist valid hooks and use per-pool reentrancy guards
contract SecureBunniHub is ReentrancyGuardPerPool {
    mapping(address => bool) public whitelistedHooks;
    mapping(PoolId => bool) private _poolLocked;
    
    modifier nonReentrantPool(PoolId poolId) {
        require(!_poolLocked[poolId], "Pool locked");
        _poolLocked[poolId] = true;
        _;
        _poolLocked[poolId] = false;
    }
    
    function deployBunniToken(DeployBunniTokenParams calldata params) external {
        require(whitelistedHooks[address(params.hooks)], "Hook not whitelisted");
        // ...
    }
    
    function deposit(PoolId poolId, ...) external nonReentrantPool(poolId) {
        // Per-pool reentrancy guard
    }
}
```

### Secure Pattern 2: Robust Token Transfer Handling

```solidity
// SECURE: Handle all ERC20 edge cases
library TokenHelper {
    function safeTransferWithFeeCheck(
        address token,
        address to,
        uint256 amount
    ) internal returns (uint256 actualReceived) {
        uint256 balanceBefore = IERC20(token).balanceOf(to);
        
        // Low-level call handles missing return value
        (bool success, bytes memory data) = token.call(
            abi.encodeWithSelector(IERC20.transfer.selector, to, amount)
        );
        require(
            success && (data.length == 0 || abi.decode(data, (bool))),
            "Transfer failed"
        );
        
        // Calculate actual received (handles fee-on-transfer)
        actualReceived = IERC20(token).balanceOf(to) - balanceBefore;
    }
}
```

### Secure Pattern 3: Gas-Optimized Hook Callbacks

```solidity
// SECURE: Minimize gas in critical callbacks
contract OptimizedPositionAdapter {
    // Pre-warm storage slots during subscribe
    function notifySubscribe(uint256 tokenId) external {
        // Warm all storage that notifyUnsubscribe needs
        _warmPositionStorage(tokenId);
        _warmRewardStorage(tokenId);
        _warmGaugeStorage(tokenId);
    }
    
    function notifyUnsubscribe(uint256 tokenId) external {
        // Now all SLOADs are warm (100 gas instead of 2100)
        _updateRewards(tokenId);
        _processIncentives(tokenId);
        _updateGaugeAccounting(tokenId);
    }
    
    function _warmPositionStorage(uint256 tokenId) internal {
        // Touch all storage slots to pre-warm them
        assembly {
            let slot := add(positions.slot, tokenId)
            let _ := sload(slot)
            // ... warm other slots
        }
    }
}
```

### Secure Pattern 4: Rate-Limited Hook Triggers

```solidity
// SECURE: Rate limit automatic hook triggers
contract RateLimitedHook {
    mapping(PoolId => uint256) public lastTriggerTime;
    uint256 public constant MIN_TRIGGER_INTERVAL = 1 hours;
    
    function _afterSwap(
        PoolKey calldata poolKey,
        IPoolManager.SwapParams calldata params,
        BalanceDelta balanceDelta
    ) internal override {
        PoolId poolId = poolKey.toId();
        
        if (_shouldTriggerBackrun(poolKey)) {
            // Rate limit
            if (block.timestamp < lastTriggerTime[poolId] + MIN_TRIGGER_INTERVAL) {
                return;  // Skip trigger, too soon
            }
            
            lastTriggerTime[poolId] = block.timestamp;
            _executeBackrun(poolKey, balanceDelta);
        }
    }
}
```

---

## Impact Analysis

### Technical Impact

| Impact Type | Severity | Description |
|-------------|----------|-------------|
| Global Reentrancy Bypass | CRITICAL | Malicious hooks can unlock global guards, drain all pools |
| Accounting Corruption | HIGH | Token collisions and state mismatches corrupt balances |
| DoS via Gas Exhaustion | HIGH | Gas limit underestimation blocks legitimate operations |
| Fee Theft | HIGH | Stale state enables repeated fee extraction |

### Financial Impact

1. **Reentrancy Attacks** (5/35 reports) - Complete fund drainage via malicious hooks
2. **Fee Farming** (4/35 reports) - Continuous extraction of LP fees via self-triggered hooks
3. **Token Incompatibility** (8/35 reports) - Reverts on valid operations or silent fund loss
4. **Position Corruption** (6/35 reports) - Inflated tokensOwed enables fee theft

### Attack Scenarios

1. **Malicious Hook Fund Drain**
   - Deploy pool with custom hook implementing `unlockForRebalance()`
   - Call to clear global reentrancy lock
   - Reenter BunniHub deposit/withdraw on legitimate pools
   - Drain funds from all users

2. **LP Fee Farming**
   - Add concentrated liquidity around price threshold
   - Execute swap to trigger automatic backrun
   - Collect fees from both swap legs
   - Repeat indefinitely with minimal capital

3. **V4 Wrapper Fee Theft**
   - Wait for other users to partially unwrap positions
   - Their fees accumulate in wrapper tokensOwed
   - Wrap/unwrap own position repeatedly
   - Steal accumulated fees using stale state

---

## Detection Patterns

### Static Analysis

```yaml
# Semgrep rules for hook vulnerabilities
rules:
  - id: unvalidated-hook-address
    patterns:
      - pattern: |
          function deployPool(... address hooks ...) {
            ...
          }
      - pattern-not: |
          require(whitelistedHooks[$HOOKS], ...);
    message: "Hook address not validated against whitelist"
    severity: ERROR

  - id: fee-on-transfer-assumption
    patterns:
      - pattern: |
          if (balanceAfter < balanceBefore + $AMOUNT) revert ...;
    message: "Assumes exact transfer amount - breaks with fee-on-transfer tokens"
    severity: WARNING

  - id: missing-reentrancy-guard
    patterns:
      - pattern: |
          function $FUNC(...) external {
            ...
            $TOKEN.call(...);
            ...
            $STATE -= ...;
          }
      - pattern-not: |
          function $FUNC(...) external nonReentrant {
            ...
          }
    message: "External call before state update without reentrancy guard"
    severity: ERROR
```

### Manual Audit Checklist

- [ ] Are hooks whitelisted or verified against canonical implementation?
- [ ] Is reentrancy protection per-pool or global?
- [ ] Do hook callbacks fit within gas limits?
- [ ] Are critical storage slots pre-warmed?
- [ ] Is fee-on-transfer handled with balance checks?
- [ ] Are ERC20 return values handled (SafeERC20)?
- [ ] Are tokensOwed/fee state variables properly decremented?
- [ ] Are auto-triggered hooks rate-limited?
- [ ] Are LDF tick bounds validated after shifts?
- [ ] Is am-AMM enabled status checked before manager validation?

---

## Real-World Examples

| Protocol | Vulnerability | Severity | Audit Firm | Year |
|----------|--------------|----------|------------|------|
| Bunni V2 | Malicious hook reentrancy bypass | CRITICAL | Cyfrin | 2025 |
| BMX Deli Swap | Gas limit underestimation | HIGH | Sherlock | 2025 |
| Licredity | Self-triggered backrun fee farming | HIGH | Cyfrin | 2025 |
| Numoen | Fee-on-transfer incompatibility | MEDIUM | Code4rena | 2023 |
| SolidlyV3 | Non-standard ERC20 handling | MEDIUM | Pashov | 2023 |
| Bunni V2 | Token accounting collision | MEDIUM | Cyfrin | 2025 |
| Vii Finance | V4 wrapper fee theft | HIGH | Cyfrin | 2025 |
| Notional V4 | Reentrancy via trade path | CRITICAL | MixBytes | 2025 |
| Bunni V2 | LDF tick bound overflow | MEDIUM | Cyfrin | 2025 |
| Bunni V2 | am-AMM manager verification | MEDIUM | Pashov | 2024 |

---

## Keywords for Search

**Primary Terms:** uniswap v4, hooks, hook security, callback, notifySubscribe, notifyUnsubscribe

**Token Terms:** fee-on-transfer, deflationary token, rebasing token, non-standard ERC20, SafeERC20

**Attack Vectors:** reentrancy, gas griefing, malicious hook, callback manipulation, fee farming

**Impacts:** fund drain, accounting corruption, DoS, fee theft, position corruption

**Related APIs:** lockForRebalance, unlockForRebalance, _afterSwap, _beforeSwap, tokensOwed

**Code Patterns:** hook whitelist, per-pool reentrancy, gas optimization, rate limiting

**Protocol Examples:** bunni_v2, vii_finance, licredity, bmx_deli_swap, solidly_v3, numoen

---

## Related Vulnerabilities

- [Fee Collection Vulnerabilities](./fee-collection-distribution.md) - Fee accounting issues
- [DoS and Arithmetic](./dos-arithmetic-initialization.md) - Initialization attacks
- [Tick and Position](./tick-range-position-vulnerabilities.md) - Position state issues
- [Reentrancy](../../general/reentrancy/) - General reentrancy patterns

---

## References

1. [Uniswap V4 Hooks Documentation](https://docs.uniswap.org/contracts/v4/concepts/hooks)
2. [EIP-4626 Inflation Attack Defense](https://blog.openzeppelin.com/a-novel-defense-against-erc4626-inflation-attacks)
3. [OpenZeppelin SafeERC20](https://docs.openzeppelin.com/contracts/4.x/api/token/erc20#SafeERC20)
4. [Bunni V2 Architecture](https://docs.bunni.xyz/bunni-v2/architecture)
