---
title: "Liquidity Management Vulnerabilities in Concentrated Liquidity AMMs"
vulnerability_class: "Liquidity Management Vulnerabilities"
severity: high
chain: "Multi-chain"
affected_protocols:
  - "Uniswap V3/V4"
  - "PancakeSwap V3"
  - "SushiSwap Trident"
  - "Good Entry"
  - "Predy"
  - "Arcadia"
tags:
  - "liquidity-deposit"
  - "liquidity-withdrawal"
  - "position-management"
  - "liquidity-accounting"
  - "flash-loan-attack"
  - "fee-theft"
last_updated: "2025-01-15"
---

# Liquidity Management Vulnerabilities in Concentrated Liquidity AMMs

## Overview

Concentrated liquidity AMMs introduce complex liquidity management mechanisms that require precise accounting across multiple tick ranges. Vulnerabilities in deposit, withdrawal, and position management operations can lead to fund loss, stuck liquidity, and exploitable accounting errors.

**Root Cause Statement:**
> "This vulnerability exists because protocols managing concentrated liquidity positions fail to properly account for liquidity changes across tick boundaries, validate position ownership/state, or correctly calculate liquidity amounts, allowing attackers to exploit flash loan attacks, fee theft, and accounting discrepancies leading to fund loss and protocol insolvency."

**Observed Frequency:** 40+ reports analyzed covering liquidity deposit/withdrawal issues, fee accounting errors, initialization attacks, and position state manipulation.

---

## Vulnerable Pattern Examples

### Pattern 1: Overestimation of Available Liquidity in Compound/Rebalance (HIGH)

Calculating theoretical liquidity amounts that exceed actual available liquidity causes transaction reverts and DoS.

**Reference**: [h-01-dos-on-mint-and-burn-due-to-overestimation-of-available-liquidity.md](../../../reports/constant_liquidity_amm/h-01-dos-on-mint-and-burn-due-to-overestimation-of-available-liquidity.md) (Pashov - Burve, HIGH)

```solidity
// VULNERABLE: Overestimating liquidity from multiple ranges
function collectAndCalcCompound() internal returns (uint256 mintNominalLiq) {
    // Get current balance
    uint256 balance0 = token0.balanceOf(address(this));
    uint256 balance1 = token1.balanceOf(address(this));
    
    // Calculate theoretical liquidity based on unit amounts
    uint256 nominalLiq0 = (balance0 << 64) / amount0InUnitLiqX64;
    uint256 nominalLiq1 = (balance1 << 64) / amount1InUnitLiqX64;
    
    // Problem: Doesn't account for distribution not matching actual pool state
    // With 2 ranges of equal weight and 1 wei balance each:
    // Calculated: 14 units of liquidity
    // Actual: 0 (1 wei cannot split across 2 ranges)
    mintNominalLiq = min(nominalLiq0, nominalLiq1) - (numRanges * 2);
    
    // Transaction reverts with "STF" when trying to mint calculated amount
}
```

---

### Pattern 2: Wrong Inequality at Price Range Boundary (HIGH)

Using strict inequality `<` instead of `<=` when checking if current price is at position boundary causes incorrect liquidity calculations.

**Reference**: [h-08-wrong-inequality-when-addingremoving-liquidity-in-current-price-range.md](../../../reports/constant_liquidity_amm/h-08-wrong-inequality-when-addingremoving-liquidity-in-current-price-range.md) (Code4rena - SushiSwap Trident, HIGH)

```solidity
// VULNERABLE: Strict inequality excludes boundary condition
function mint(uint128 liquidity) internal {
    // When priceLower == currentPrice, liquidity should be added
    // But strict < excludes this case
    if (priceLower < currentPrice && currentPrice < priceUpper) {
        // Add liquidity with both tokens
        _addLiquidityBothTokens(liquidity);
    } else if (currentPrice >= priceUpper) {
        // Only token0
        _addLiquidityToken0(liquidity);
    } else {
        // Only token1
        _addLiquidityToken1(liquidity);
    }
}

// SECURE: Include boundary with <=
function mint(uint128 liquidity) internal {
    if (priceLower <= currentPrice && currentPrice < priceUpper) {
        _addLiquidityBothTokens(liquidity);
    } else if (currentPrice >= priceUpper) {
        _addLiquidityToken0(liquidity);
    } else {
        _addLiquidityToken1(liquidity);
    }
}
```

---

### Pattern 3: Incorrect Active Liquidity at Tick Boundaries (HIGH)

Skipping liquidity delta when current tick is exactly at range boundary causes underflow or incorrect reward distribution.

**Reference**: [all-rewards-can-be-stolen-due-to-incorrect-active-liquidity-calculations-when-th.md](../../../reports/constant_liquidity_amm/all-rewards-can-be-stolen-due-to-incorrect-active-liquidity-calculations-when-th.md) (Cyfrin - Sorella L2 Angstrom, HIGH)

```solidity
// VULNERABLE: Tick iteration skips boundary tick
function _advanceToNextDown(TickIteratorDown memory self) private view {
    do {
        // Problem: When currentTick == tickUpper exactly (multiple of spacing)
        // This subtracts 1 and compresses, skipping the boundary tick entirely
        (int16 wordPos, uint8 bitPos) =
            TickLib.position((self.currentTick - 1).compress(self.tickSpacing));
        
        // Net liquidity delta of the skipped tick is never applied
        // Causes: arithmetic underflow OR stolen rewards via global accumulator
    } while (self.endTick < self.currentTick);
}

// Attack: 
// 1. Current tick at boundary T1
// 2. Add liquidity L' to range [T1-s, T1)
// 3. Swap zero-for-one - boundary liquidity skipped
// 4. L' not added to active liquidity calculation
// 5. Rewards calculated with smaller liquidity = larger growth per unit
// 6. Attacker receives disproportionate rewards

// SECURE: Perform net liquidity decrement before iteration
function _advanceToNextDown(TickIteratorDown memory self) private view {
    // First apply current tick's liquidity delta if at boundary
    if (self.currentTick % self.tickSpacing == 0) {
        _applyLiquidityDelta(self.currentTick);
    }
    // Then iterate to next tick
}
```

---

### Pattern 4: Pool Initialization Front-Running (MEDIUM)

Permissionless `initialize()` function allows attackers to set unfair initial price before legitimate deployer.

**Reference**: [front-running-pools-initialization-can-lead-to-draining-of-liquidity-providers-i.md](../../../reports/constant_liquidity_amm/front-running-pools-initialization-can-lead-to-draining-of-liquidity-providers-i.md) (TrailOfBits - Uniswap V3 Core, MEDIUM)

```solidity
// VULNERABLE: No access control on initialize
function initialize(uint160 sqrtPriceX96) external override {
    require(slot0.sqrtPriceX96 == 0, 'AI');
    int24 tick = TickMath.getTickAtSqrtRatio(sqrtPriceX96);
    slot0 = Slot0({
        sqrtPriceX96: sqrtPriceX96,
        tick: tick,
        // ... other fields
    });
}

// Attack scenario:
// 1. Bob deploys pool with market price 1 A == 1 B
// 2. Eve front-runs initialize() with price 1 A == 10 B
// 3. Bob calls mint() depositing 10x more B than A
// 4. Eve swaps A for B at unfair price, profits from Bob

// SECURE: Add access control or move to constructor
function initialize(uint160 sqrtPriceX96) external override {
    require(msg.sender == factory || msg.sender == deployer, "Unauthorized");
    require(slot0.sqrtPriceX96 == 0, 'AI');
    // ...
}
```

---

### Pattern 5: Fee Theft via Flash Loan Deposit/Withdraw (HIGH)

Non-reinvested fees can be stolen via flash loan attack when fee accounting doesn't properly scale LP token minting.

**Reference**: [h-04-tokenisableranges-incorrect-accounting-of-non-reinvested-fees-in-deposit-ex.md](../../../reports/constant_liquidity_amm/h-04-tokenisableranges-incorrect-accounting-of-non-reinvested-fees-in-deposit-ex.md) (Code4rena - Good Entry, HIGH)

```solidity
// VULNERABLE: Fee accounting can be bypassed
function deposit(uint256 n0, uint256 n1) external returns (uint256 lpAmt) {
    // Collect pending fees
    claimFee();
    
    // Problem 1: 1% reinvestment check uses amounts, not value
    // When price changes significantly, fee VALUE can exceed 1% even if amounts don't
    if (fee0 < liquidity0 / 100 && fee1 < liquidity1 / 100) {
        // Fees not reinvested
    }
    
    // Problem 2: LP scaling only happens if BOTH tokens are 0
    if (newFee0 == 0 && newFee1 == 0) {
        // Scale LP tokens by fee value
    } else {
        // No scaling - attacker adds tiny amount of second token to skip
    }
    
    // Attack:
    // 1. Flash loan large amount
    // 2. Deposit with tiny second token amount (bypasses scaling)
    // 3. Receive LP tokens without fee deduction
    // 4. Withdraw LP tokens (now includes share of fees)
    // 5. Profit from fees, repay flash loan
}

// SECURE: Always factor in fee value
function deposit(uint256 n0, uint256 n1) external returns (uint256 lpAmt) {
    uint256 TOKEN0_PRICE = oracle.getPrice(address(token0));
    uint256 TOKEN1_PRICE = oracle.getPrice(address(token1));
    
    // Calculate fee value relative to total value
    uint256 feeValue = (fee0 * TOKEN0_PRICE) + (fee1 * TOKEN1_PRICE);
    uint256 totalValue = (reserve0 * TOKEN0_PRICE) + (reserve1 * TOKEN1_PRICE);
    
    // ALWAYS scale LP minting by fee proportion
    uint256 feeLiquidity = (lpAmt * feeValue) / totalValue;
    lpAmt = lpAmt - feeLiquidity;
}
```

---

### Pattern 6: Shared Pool Liquidity Theft Between Pairs (HIGH)

Multiple pairs using same Uniswap pool with overlapping tick ranges can steal each other's liquidity.

**Reference**: [h-03-one-pair-can-steal-another-pairs-uniswap-liquidity-during-reallocate-call-i.md](../../../reports/constant_liquidity_amm/h-03-one-pair-can-steal-another-pairs-uniswap-liquidity-during-reallocate-call-i.md) (Code4rena - Predy, HIGH)

```solidity
// VULNERABLE: No internal liquidity tracking per pair
function reallocate(uint256 pairId) external {
    PairStatus storage pair = pairs[pairId];
    
    // Gets ALL liquidity in the tick range from Uniswap
    // Doesn't distinguish between pair1's liquidity and pair2's liquidity
    (uint128 liquidity,,,) = pool.positions(
        keccak256(abi.encodePacked(address(this), pair.tickLower, pair.tickUpper))
    );
    
    // Reallocates liquidity that may belong to different pair!
    // If pair1 has 100 liquidity and pair2 has 0, but same ticks,
    // reallocating pair2 will take pair1's liquidity
}

// Attack:
// 1. Operator creates pair1 for USDC/ETH with USDC as quote
// 2. Operator creates pair2 for USDC/ETH with ETH as quote (same pool, same ticks)
// 3. User trades gamma on pair1, adding liquidity
// 4. Price moves outside pair2's threshold
// 5. Anyone calls reallocate(pair2)
// 6. Pair2 steals pair1's liquidity, breaking pair1's accounting

// SECURE: Track liquidity per pair internally
mapping(uint256 => uint128) public pairLiquidity;

function reallocate(uint256 pairId) external {
    PairStatus storage pair = pairs[pairId];
    
    // Only reallocate this pair's tracked liquidity
    uint128 liquidityToReallocate = pairLiquidity[pairId];
    // ...
}
```

---

### Pattern 7: Permissionless Fee Withdrawal on Behalf of Pool (HIGH)

Allowing anyone to call `withdrawFees()` for any address including the pool itself enables fee theft.

**Reference**: [h-1-liquidity-provider-fees-can-be-stolen-from-any-pair.md](../../../reports/constant_liquidity_amm/h-1-liquidity-provider-fees-can-be-stolen-from-any-pair.md) (Sherlock - Goat Trading, HIGH)

```solidity
// VULNERABLE: Permissionless fee withdrawal for any address
function withdrawFees(address recipient) external {
    uint256 earned = _earnedFees(recipient);
    
    // Transfers fees from pool to pool (if recipient == address(this))
    // Lowers _pendingLiquidityFee by earned amount
    _pendingLiquidityFee -= earned;
    
    WETH.transfer(recipient, earned);
}

// Also vulnerable: No fee tracking update on transfer to pool
function _transfer(address from, address to, uint256 amount) internal {
    if (to != address(this)) {
        _updateFeeRewards(to);  // Pool address skipped
    }
    // feesPerTokenPaid[address(pair)] remains 0
}

// Attack:
// 1. Add liquidity, receive LP tokens
// 2. Transfer LP tokens to pair itself
// 3. Call withdrawFees(address(pair))
//    - feesPerTokenPaid[pair] == 0, so calculates large fees
//    - Transfers WETH pool→pool, lowers _pendingLiquidityFee
// 4. Pool thinks excess WETH was donated
// 5. Swap "donated" WETH for profit
// 6. Burn LP tokens to recover original funds

// SECURE: Prevent fee withdrawal for pool address
function withdrawFees(address recipient) external {
    require(recipient != address(this), "Cannot withdraw on behalf of pool");
    // ...
}
```

---

### Pattern 8: Cached Liquidity Allows Undercollateralized Positions (HIGH)

Caching Uniswap position liquidity at deposit time allows manipulation via ERC777 hooks.

**Reference**: [h-3-caching-uniswap-position-liquidity-allows-borrowing-using-undercollateralize.md](../../../reports/constant_liquidity_amm/h-3-caching-uniswap-position-liquidity-allows-borrowing-using-undercollateralize.md) (Sherlock - Arcadia, HIGH)

```solidity
// VULNERABLE: Liquidity cached before transfer completes
function _deposit(address[] memory assetAddresses, uint256[] memory assetIds, uint256[] memory assetAmounts) internal {
    // Step 1: Cache liquidity from Uniswap position
    IRegistry(registry).batchProcessDeposit(...);  // Stores liquidity in mapping
    
    // Step 2: Transfer assets
    for (uint256 i; i < assetAddresses.length; ++i) {
        if (assetTypes[i] == 0) {
            _depositERC20(from, assetAddresses[i], assetAmounts[i]);  // ERC777 hook here!
        } else if (assetTypes[i] == 1) {
            _depositERC721(from, assetAddresses[i], assetIds[i]);
        }
    }
}

// In UniswapV3AM:
function _addAsset(uint256 assetId) internal {
    (,,,,,,,uint128 liquidity,,,,) = NON_FUNGIBLE_POSITION_MANAGER.positions(assetId);
    assetToLiquidity[assetId] = liquidity;  // Cached liquidity
}

// Attack:
// 1. Malicious contract deposits: [ERC777 token, Uniswap position]
// 2. Registry caches Uniswap liquidity = 100
// 3. ERC777 transfer triggers tokensToSend() hook
// 4. In hook: decrease Uniswap position liquidity to 0 (still owned by attacker)
// 5. After hook: Uniswap position (now empty) transferred to account
// 6. Protocol thinks position has 100 liquidity, actually has 0
// 7. Borrow against "100 liquidity" collateral

// SECURE: Check liquidity AFTER transfer
function _deposit(...) internal {
    // Transfer first
    for (uint256 i; ...) {
        _transferAsset(...);
    }
    
    // Then cache/verify liquidity
    for (uint256 i; ...) {
        if (isUniswapPosition) {
            uint128 actualLiquidity = getNFTPositionLiquidity(assetId);
            require(actualLiquidity >= minRequired, "Insufficient liquidity");
            assetToLiquidity[assetId] = actualLiquidity;
        }
    }
}
```

---

### Pattern 9: Recovery Mode Blocking Liquidity Withdrawal (HIGH)

Whitelisting mechanisms that block token transfers prevent legitimate users from withdrawing liquidity.

**Reference**: [h-02-unable-to-remove-liquidity-in-recovery-mode.md](../../../reports/constant_liquidity_amm/h-02-unable-to-remove-liquidity-in-recovery-mode.md) (Code4rena - Malt Finance, HIGH)

```solidity
// VULNERABLE: Transfer verification blocks withdrawal
function removeLiquidity(uint256 lpAmount) external {
    // UniswapV2Pair.burn() calls safeTransfer for both tokens
    IUniswapV2Pair(pair).burn(msg.sender);  // This reverts!
}

// In token's _beforeTokenTransfer:
function verifyTransfer(address from, address to) internal {
    if (recoveryMode && priceBelow Peg) {
        // Only whitelisted addresses can receive tokens
        require(whitelist[to], "Not whitelisted in recovery");
        // User is NOT whitelisted, so withdrawal reverts
    }
}

// Problem: Documentation says users can remove via UniswapHandler (whitelisted)
// But UniswapHandler sends tokens directly to msg.sender:
function removeLiquidityForUser(uint256 lpAmount) external {
    (uint256 amount0, uint256 amount1) = pair.burn(address(this));
    token0.transfer(msg.sender, amount0);  // Reverts if msg.sender not whitelisted
    token1.transfer(msg.sender, amount1);
}

// SECURE: Two-step withdrawal to whitelisted intermediary
function removeLiquidityForUser(uint256 lpAmount) external {
    (uint256 amount0, uint256 amount1) = pair.burn(address(this));
    // Store for user to claim later, or use approved claims
    pendingWithdrawals[msg.sender].amount0 += amount0;
    pendingWithdrawals[msg.sender].amount1 += amount1;
}
```

---

## Secure Implementation Examples

### Secure Pattern 1: Atomic Liquidity Verification

```solidity
// SECURE: Verify liquidity state before and after operations
contract SecureLiquidityManager {
    function deposit(uint256 tokenId) external {
        // Get liquidity BEFORE transfer
        uint128 liquidityBefore = getPositionLiquidity(tokenId);
        
        // Transfer position
        nonfungiblePositionManager.safeTransferFrom(msg.sender, address(this), tokenId);
        
        // Get liquidity AFTER transfer
        uint128 liquidityAfter = getPositionLiquidity(tokenId);
        
        // Verify no manipulation occurred
        require(liquidityAfter == liquidityBefore, "Liquidity changed during deposit");
        
        // Now safe to cache
        positionLiquidity[tokenId] = liquidityAfter;
    }
}
```

### Secure Pattern 2: Per-Position Liquidity Accounting

```solidity
// SECURE: Track liquidity per logical position/pair
contract SecureMultiPairManager {
    // Separate accounting per pair
    mapping(uint256 => mapping(bytes32 => uint128)) public pairPositionLiquidity;
    
    function addLiquidity(uint256 pairId, int24 tickLower, int24 tickUpper, uint128 amount) external {
        bytes32 positionKey = keccak256(abi.encodePacked(tickLower, tickUpper));
        
        // Add to pair-specific accounting
        pairPositionLiquidity[pairId][positionKey] += amount;
        
        // Add to Uniswap
        nonfungiblePositionManager.increaseLiquidity(params);
    }
    
    function reallocate(uint256 pairId) external {
        // Only use this pair's tracked liquidity
        bytes32 positionKey = currentPositionKey(pairId);
        uint128 liquidity = pairPositionLiquidity[pairId][positionKey];
        
        // Cannot steal other pairs' liquidity
        _reallocateAmount(pairId, liquidity);
    }
}
```

### Secure Pattern 3: Fee-Adjusted LP Minting

```solidity
// SECURE: Always account for fees in LP minting
contract SecureLPToken {
    function deposit(uint256 amount0, uint256 amount1) external returns (uint256 lpAmount) {
        // Collect any pending fees first
        _collectFees();
        
        // Calculate total value including fees
        uint256 totalValue = _getTotalValue();
        uint256 depositValue = _calculateDepositValue(amount0, amount1);
        
        // LP tokens proportional to total value (including fees)
        lpAmount = (depositValue * totalSupply()) / totalValue;
        
        // Transfer tokens
        token0.transferFrom(msg.sender, address(this), amount0);
        token1.transferFrom(msg.sender, address(this), amount1);
        
        _mint(msg.sender, lpAmount);
    }
    
    function _getTotalValue() internal view returns (uint256) {
        // Include: position value + collected fees + pending fees
        return _getPositionValue() + fee0 + fee1;
    }
}
```

### Secure Pattern 4: Protected Initialization

```solidity
// SECURE: Controlled pool initialization
contract SecurePoolFactory {
    function createAndInitializePool(
        address token0,
        address token1,
        uint24 fee,
        uint160 sqrtPriceX96
    ) external returns (address pool) {
        // Create pool
        pool = factory.createPool(token0, token1, fee);
        
        // Initialize atomically - no gap for front-running
        IUniswapV3Pool(pool).initialize(sqrtPriceX96);
        
        // Deployer can immediately add liquidity
        emit PoolCreated(pool, msg.sender);
    }
}
```

---

## Impact Analysis

### Technical Impact

| Impact Type | Severity | Description |
|-------------|----------|-------------|
| DoS on Mint/Burn | HIGH | Overestimated liquidity causes transaction reverts |
| Accounting Corruption | HIGH | Incorrect liquidity tracking breaks position management |
| Underflow/Overflow | HIGH | Boundary tick issues cause arithmetic errors |
| State Desynchronization | HIGH | Cached vs actual liquidity divergence |

### Financial Impact

1. **Fee Theft** (6/40 reports) - Flash loan attacks extract accumulated fees
2. **Liquidity Theft** (8/40 reports) - Cross-pair or cross-position liquidity stealing
3. **Undercollateralized Borrowing** (4/40 reports) - Empty positions used as collateral
4. **Stuck Funds** (5/40 reports) - Liquidity cannot be withdrawn due to DoS

### Attack Scenarios

1. **Flash Loan Fee Extraction**
   - Flash loan large amount
   - Deposit into pool with high accumulated fees
   - Bypass fee scaling with tiny second token
   - Receive LP tokens including fee share
   - Withdraw and repay flash loan with profit

2. **ERC777 Hook Exploitation**
   - Deposit ERC777 token + Uniswap position
   - During ERC777 transfer, hook triggers
   - In hook, decrease Uniswap position liquidity
   - Protocol caches stale (high) liquidity value
   - Borrow against empty collateral

3. **Initialization Front-Running**
   - Monitor mempool for pool deployments
   - Front-run `initialize()` with skewed price
   - Legitimate user deposits at unfair ratio
   - Swap to extract value from imbalanced deposit

---

## Detection Patterns

### Static Analysis

```yaml
# Semgrep rule for liquidity caching issues
rules:
  - id: liquidity-cache-before-transfer
    patterns:
      - pattern: |
          $LIQUIDITY = $NFT.positions($ID)
          ...
          $NFT.safeTransferFrom(...)
      - pattern-not: |
          $NFT.safeTransferFrom(...)
          ...
          $LIQUIDITY = $NFT.positions($ID)
    message: "Liquidity cached before transfer - potential manipulation"
    severity: ERROR
```

### Manual Audit Checklist

- [ ] Is liquidity cached AFTER asset transfer completes?
- [ ] Are boundary conditions (`<=` vs `<`) handled correctly?
- [ ] Is pool initialization protected from front-running?
- [ ] Are fees accounted for in LP token minting?
- [ ] Is per-position/per-pair liquidity tracked separately?
- [ ] Are permissionless functions protected against pool self-calls?
- [ ] Are ERC777/callback hooks considered in deposit flow?
- [ ] Can recovery/emergency modes block legitimate withdrawals?

---

## Real-World Examples

| Protocol | Vulnerability | Severity | Audit Firm | Year |
|----------|--------------|----------|------------|------|
| Burve | Liquidity overestimation DoS | HIGH | Pashov | 2025 |
| SushiSwap Trident | Wrong boundary inequality | HIGH | Code4rena | 2021 |
| Sorella L2 | Tick boundary liquidity skip | HIGH | Cyfrin | 2025 |
| Uniswap V3 | Initialize front-running | MEDIUM | TrailOfBits | 2021 |
| Good Entry | Flash loan fee theft | HIGH | Code4rena | 2023 |
| Predy | Cross-pair liquidity theft | HIGH | Code4rena | 2024 |
| Goat Trading | Permissionless fee withdrawal | HIGH | Sherlock | 2024 |
| Arcadia | Cached liquidity manipulation | HIGH | Sherlock | 2023 |
| Malt Finance | Recovery mode blocks withdrawal | HIGH | Code4rena | 2021 |

---

## Keywords for Search

**Primary Terms:** liquidity deposit, liquidity withdrawal, position management, LP token, fee accounting

**Liquidity Terms:** addLiquidity, removeLiquidity, mint, burn, increaseLiquidity, decreaseLiquidity

**Attack Vectors:** flash loan, fee theft, front-running, initialization attack, ERC777 hook

**Impacts:** stuck funds, undercollateralized, accounting error, DoS, overflow

**Related APIs:** positions(), mint(), burn(), collect(), increaseLiquidity(), NonfungiblePositionManager

**Code Patterns:** liquidity caching, boundary inequality, permissionless withdrawal, cross-pair access

**Protocol Examples:** uniswap_v3, sushiswap_trident, good_entry, predy, arcadia, goat_trading

---

## Related Vulnerabilities

- [Fee Collection Distribution](./fee-collection-distribution.md) - Fee-related vulnerabilities
- [Tick Range Position Vulnerabilities](./tick-range-position-vulnerabilities.md) - Tick boundary issues
- [Price Oracle Manipulation](./price-oracle-manipulation.md) - Price manipulation in liquidity ops

---

## References

1. [Uniswap V3 Core Audit - TrailOfBits](https://github.com/trailofbits/publications/blob/master/reviews/UniswapV3Core.pdf)
2. [Uniswap V3 Position Management](https://docs.uniswap.org/contracts/v3/guides/providing-liquidity/mint-a-position)
3. [ERC777 Token Standard](https://eips.ethereum.org/EIPS/eip-777)
