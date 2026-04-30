---
title: "DoS, Arithmetic, and Initialization Vulnerabilities in Concentrated Liquidity AMMs"
protocol: generic
category: amm/concentrated-liquidity
vulnerability_class: "DoS/Arithmetic/Initialization Vulnerabilities"
vulnerability_type: dos_arithmetic_initialization
attack_type: denial_of_service|arithmetic_error|initialization_manipulation
affected_component: pool_initialization|liquidity_math|share_accounting
severity: high
impact: fund_loss|denial_of_service|state_corruption
chain: "Multi-chain"
affected_protocols:
  - "Uniswap V3/V4"
  - "PancakeSwap V3"
  - "Morpho"
  - "Bunni"
  - "MagicLP"
  - "Mellow"
tags:
  - "denial-of-service"
  - "arithmetic"
  - "overflow"
  - "underflow"
  - "rounding"
  - "initialization"
  - "reentrancy"
  - "first-depositor"
last_updated: "2025-01-15"

# Pattern Identity (Required)
root_cause_family: missing_initialization_guard
pattern_key: missing_initialization_guard | unknown | unknown

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - add
  - and
  - block.timestamp
  - buyShares
  - calculateOwedFees
  - computeSwap
  - createPool
  - deposit
  - emptyRebalance
  - getBuyInfo
  - getOwedFee
  - getSellInfo
  - griefing
  - inflation
  - initialize
  - initializer
  - mint
  - msg.sender
  - mulDiv
  - processWithdrawals
---

# DoS, Arithmetic, and Initialization Vulnerabilities in Concentrated Liquidity AMMs

## Overview

Concentrated liquidity AMMs involve complex mathematical operations for price calculations, liquidity distributions, and share minting. Vulnerabilities in arithmetic operations, initialization sequences, and state management can lead to denial of service, fund theft, and protocol manipulation.

**Root Cause Statement:**
> "This vulnerability exists because protocols implementing concentrated liquidity mechanisms fail to properly handle arithmetic edge cases (overflow/underflow/rounding), protect initialization sequences from manipulation, or prevent griefing attacks on critical operations, allowing attackers to cause DoS, steal funds through share inflation attacks, or corrupt protocol state leading to fund loss."

**Observed Frequency:** 60+ reports analyzed covering arithmetic errors, DoS vectors, initialization attacks, and first depositor exploits.

---



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of missing_initialization_guard"
- Pattern key: `missing_initialization_guard | unknown | unknown`
- Interaction scope: `single_contract`
- Primary affected component(s): `unknown`
- High-signal code keywords: `add`, `and`, `block.timestamp`, `buyShares`, `calculateOwedFees`, `computeSwap`, `createPool`, `deposit`
- Typical sink / impact: `fund_loss`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `Counter.function -> SecureInitializable.function -> SecurePool.function`
- Trust boundary crossed: `internal`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: Initializer function callable more than once (missing initializer modifier)
- Signal 2: Proxy implementation has unprotected initialize() callable by anyone
- Signal 3: Constructor logic not replicated in initializer for upgradeable contract
- Signal 4: Implementation contract left uninitialized, allowing attacker takeover

#### False Positive Guards

- Not this bug when: OpenZeppelin `initializer` modifier prevents re-initialization
- Safe if: Proxy implementation initialize() called in same transaction as deployment
- Requires attacker control of: specific conditions per pattern

#### Code Patterns to Look For

```solidity
uint256 prod0 = a * b; // migrated FullMath without unchecked overflow behavior
amountOut = mulDiv(amountIn, reserveOut, reserveIn); // wrong rounding direction for buys/sells
initialize(token0, token1, sqrtPriceX96); // callable by anyone or callable twice
buyShares(1); deposit(donation); // first-depositor or initial-donation share inflation
for (...) processWithdrawals(queue[i]); // attacker can inflate queue or force permanent revert
```

#### False Positive Detail

- Initialization issues are high signal when the initializer sets ownership, pool price, trusted tokens, or accounting baselines and remains callable after deployment.
- Arithmetic DoS requires a realistic input range that triggers revert or zero output in a public path, not only unreachable max-value math.
- First-depositor findings need a low/empty supply state plus donation, rounding, or initial-price control that transfers value from later users.

## Vulnerable Pattern Examples

### Pattern 1: Unchecked Overflow in FullMath Migration (HIGH)

Migrating Uniswap V3's FullMath from pre-0.8 Solidity to 0.8+ without `unchecked` blocks breaks intentional overflow behavior.

**Reference**: [fullmath-requires-overflow-behavior.md](../../../reports/constant_liquidity_amm/fullmath-requires-overflow-behavior.md) (Spearbit - Morpho, HIGH)

```solidity
// VULNERABLE: Solidity 0.8 reverts on intentional overflow
// This is migrated from Uniswap V3's Solidity <0.8 code
library FullMath {
    function mulDiv(uint256 a, uint256 b, uint256 denominator) internal pure returns (uint256 result) {
        // Original relies on overflow wrapping
        uint256 prod0 = a * b;  // REVERTS in 0.8+ on overflow!
        uint256 prod1;
        assembly {
            let mm := mulmod(a, b, not(0))
            prod1 := sub(sub(mm, prod0), lt(mm, prod0))
        }
        // ...
    }
}

// SECURE: Wrap in unchecked block for 0.8+
library FullMathFixed {
    function mulDiv(uint256 a, uint256 b, uint256 denominator) internal pure returns (uint256 result) {
        unchecked {
            uint256 prod0 = a * b;  // Intentional overflow allowed
            uint256 prod1;
            assembly {
                let mm := mulmod(a, b, not(0))
                prod1 := sub(sub(mm, prod0), lt(mm, prod0))
            }
            // ...
        }
    }
}
```

---

### Pattern 2: Fee Growth Underflow Not Handled (HIGH)

Uniswap V3's intentional underflow in fee growth calculations isn't properly handled in wrapper protocols.

**Reference**: [getowedfee-can-incorrectly-return-zero-because-of-fee-growth-underﬂow.md](../../../reports/constant_liquidity_amm/getowedfee-can-incorrectly-return-zero-because-of-fee-growth-underﬂow.md) (Cantina - Particle, HIGH)

```solidity
// VULNERABLE: Comparison instead of subtraction
function getOwedFee(
    uint256 feeGrowthInside0X128,
    uint256 feeGrowthInside1X128,
    uint256 feeGrowthInside0LastX128,
    uint256 feeGrowthInside1LastX128,
    uint128 liquidity
) internal pure returns (uint256 token0Owed, uint256 token1Owed) {
    // Problem: Uses comparison, but Uniswap V3 uses wrapping subtraction
    if (feeGrowthInside0X128 > feeGrowthInside0LastX128) {
        token0Owed = FullMath.mulDiv(
            feeGrowthInside0X128 - feeGrowthInside0LastX128,
            liquidity,
            FixedPoint128.Q128
        );
    }
    // When feeGrowthInside0X128 < feeGrowthInside0LastX128 (due to underflow wrap)
    // this returns 0 instead of correct value
    // Example: 2e18 - (type(uint256).max - 1e18 + 1) should = 3e18 via underflow
}

// SECURE: Use unchecked subtraction like Uniswap V3
function getOwedFee(...) internal pure returns (uint256 token0Owed, uint256 token1Owed) {
    unchecked {
        // Wrapping subtraction handles the underflow case correctly
        token0Owed = FullMath.mulDiv(
            feeGrowthInside0X128 - feeGrowthInside0LastX128,
            liquidity,
            FixedPoint128.Q128
        );
        token1Owed = FullMath.mulDiv(
            feeGrowthInside1X128 - feeGrowthInside1LastX128,
            liquidity,
            FixedPoint128.Q128
        );
    }
}
```

---

### Pattern 3: Rounding Error Amplification Breaking Pool Invariants (HIGH)

Rounding errors in initial LP minting can be amplified to break pool pricing invariants.

**Reference**: [h-02-attacker-can-amplify-a-rounding-error-in-magiclp-to-break-the-i-invariant-a.md](../../../reports/constant_liquidity_amm/h-02-attacker-can-amplify-a-rounding-error-in-magiclp-to-break-the-i-invariant-a.md) (Code4rena - Abracadabra MagicLP, HIGH)

```solidity
// VULNERABLE: Wrong rounding direction enables invariant manipulation
function buyShares() external {
    if (totalSupply() == 0) {
        // quoteBalance = 1, baseBalance = 19999, I = 1e14
        // Check: 1 < 19999 * 1e14 / 1e18 => 1 < 1 => FALSE (due to mulFloor)
        shares = quoteBalance < DecimalMath.mulFloor(baseBalance, _I_) 
            ? DecimalMath.divFloor(quoteBalance, _I_) 
            : baseBalance;
        
        // shares = 19999 (baseBalance)
        _BASE_TARGET_ = shares;  // = 19999
        _QUOTE_TARGET_ = DecimalMath.mulFloor(shares, _I_);  // = 19999 * 1e14 / 1e18 = 1
        
        // Result: ratio becomes 1:19999 instead of intended 1:10000 (from I = 1e14)
        // Attacker can trade at 2x advantage vs expected ratio
    }
}

// SECURE: Use ceiling rounding to ensure enough quote balance
function buyShares() external {
    if (totalSupply() == 0) {
        // Use mulCeil to round UP the threshold
        shares = quoteBalance < DecimalMath.mulCeil(baseBalance, _I_) 
            ? DecimalMath.divFloor(quoteBalance, _I_)  // Defensive path
            : baseBalance;
        // Now 1 < ceil(19999 * 1e14 / 1e18) => 1 < 2 => TRUE
        // Takes divFloor path, preventing invariant manipulation
    }
}
```

---

### Pattern 4: First Depositor / Inflation Attack (HIGH)

First depositor can inflate share price to steal from subsequent depositors.

**Reference**: [h-01-univ3tokenizedlp-can-be-attacked-by-an-initial-donation.md](../../../reports/constant_liquidity_amm/h-01-univ3tokenizedlp-can-be-attacked-by-an-initial-donation.md) (Pashov - Radiant, HIGH)

```solidity
// VULNERABLE: No protection against share inflation
function deposit(uint256 amount0, uint256 amount1) external returns (uint256 shares) {
    if (totalSupply() != 0) {
        uint256 pool0PricedInToken1 = (pool0 * oraclePrice) / PRECISION;
        // Shares calculated based on current value
        shares = (shares * totalSupply()) / (pool0PricedInToken1 + pool1);
    }
    // Attack:
    // 1. Attacker mints 1 wei LP
    // 2. Attacker donates 1e18 WETH directly to contract
    // 3. totalSupply = 1, but pool value = 1e18
    // 4. Victim deposits 0.5 ETH, receives 0 shares (rounding)
    // 5. Attacker withdraws 1 share, receives 1.5 ETH
}

// SECURE: Virtual shares and minimum liquidity lock
function deposit(uint256 amount0, uint256 amount1) external returns (uint256 shares) {
    uint256 VIRTUAL_SHARES = 1e6;
    uint256 VIRTUAL_ASSETS = 1;
    
    if (totalSupply() == 0) {
        shares = _calculateShares(amount0, amount1);
        // Lock minimum shares to dead address
        _mint(address(0xdead), MINIMUM_LIQUIDITY);
        shares -= MINIMUM_LIQUIDITY;
    } else {
        // Use virtual shares/assets to prevent inflation
        shares = ((amount0 + VIRTUAL_ASSETS) * (totalSupply() + VIRTUAL_SHARES)) 
                 / (totalAssets() + VIRTUAL_ASSETS) - VIRTUAL_SHARES;
    }
}
```

---

### Pattern 5: Counter Overflow DoS (MEDIUM)

Shared counter contracts can be overflowed by attackers to DoS legitimate operations.

**Reference**: [denial-of-service-attack-on-lpwrapper-s-deposit-and-withdraw-functions.md](../../../reports/constant_liquidity_amm/denial-of-service-attack-on-lpwrapper-s-deposit-and-withdraw-functions.md) (Cantina - Mellow, MEDIUM)

```solidity
// VULNERABLE: Shared counter can be overflowed by anyone
function emptyRebalance(uint256 positionId) external {
    Position storage pos = positions[positionId];
    
    // Attacker can set their position's counter to LpWrapper's Counter
    // Then cause rebalance with huge value
    ICounter(pos.counter).add(pos.gauge.rewardToken, hugeValue);
    // Counter.add will overflow, causing all future LpWrapper deposits to revert
}

contract Counter {
    mapping(address => uint256) public value;
    
    function add(address token, uint256 amount) external {
        // If value + amount > type(uint256).max, reverts in 0.8+
        value[token] += amount;  // DoS for LpWrapper!
    }
}

// SECURE: Validate counter addresses, or use per-position counters
function setPositionParams(uint256 positionId, address counter) external onlyManager {
    // Only allow known, trusted counter addresses
    require(trustedCounters[counter], "Invalid counter");
    positions[positionId].counter = counter;
}
```

---

### Pattern 6: Withdrawal Queue Griefing DoS (HIGH)

Unlimited withdrawal requests enable queue flooding attacks.

**Reference**: [attacker-can-dos-withdrawals.md](../../../reports/constant_liquidity_amm/attacker-can-dos-withdrawals.md) (OpenZeppelin - RestakeFi, HIGH)

```solidity
// VULNERABLE: No limit on withdrawal requests
function requestWithdraw(uint256 amount) external {
    // Attacker deposits 1000 tokens
    // Calls requestWithdrawal(1) x 1000 times
    // Each request added to FIFO queue
    withdrawalQueue.push(WithdrawalRequest({
        user: msg.sender,
        amount: amount,
        nonce: currentNonce++
    }));
}

function processWithdrawals(uint256 count) external onlyManager {
    // Must process ALL requests in order
    // Attacker's 1000 requests must be processed before legitimate users
    for (uint256 i; i < count; i++) {
        _processNextWithdrawal();
    }
}

// SECURE: Aggregate requests per user, minimum amount
mapping(address => uint256) public pendingWithdrawals;

function requestWithdraw(uint256 amount) external {
    require(amount >= MIN_WITHDRAWAL, "Below minimum");
    // Aggregate into single pending amount
    pendingWithdrawals[msg.sender] += amount;
}
```

---

### Pattern 7: Re-initialization Vulnerability (CRITICAL)

Missing access control on `initialize()` allows attackers to reconfigure critical parameters.

**Reference**: [c-01-anyone-can-re-initialize-the-swapproxy.md](../../../reports/constant_liquidity_amm/c-01-anyone-can-re-initialize-the-swapproxy.md) (Pashov - WishWish, CRITICAL)

```solidity
// VULNERABLE: No access control, no initialization guard
function initialize(
    address _universalRouter,
    address _permit2,
    address _weth
) external {
    // No check for already initialized!
    // No access control!
    $.router = IUniversalRouter(_universalRouter);
    $.permit2 = _permit2;
    $.WETH = IWETH9(_weth);
    
    // Gives attacker's contract full approval over WETH
    $.WETH.safeApprove(_permit2, type(uint256).max);
}

// Attack:
// 1. Call initialize() with malicious router and permit2
// 2. Malicious permit2 now has unlimited WETH approval
// 3. Drain all WETH from contract

// SECURE: Use initializer modifier and access control
bool private _initialized;

function initialize(...) external {
    require(!_initialized, "Already initialized");
    require(msg.sender == factory, "Unauthorized");
    _initialized = true;
    // ...
}
```

---

### Pattern 8: Inconsistent Rounding Directions (MEDIUM)

Using same rounding for buy and sell operations leads to value leakage.

**Reference**: [different-rounding-directions-are-recommended-for-getting-buysell-info.md](../../../reports/constant_liquidity_amm/different-rounding-directions-are-recommended-for-getting-buysell-info.md) (Cyfrin - Sudoswap, MEDIUM)

```solidity
// VULNERABLE: Same rounding direction for both buy and sell
function getBuyInfo(...) external returns (uint256 price, uint256 fee) {
    price = _calculatePrice(...);  // Rounds down
    fee = _calculateFee(price);    // Rounds down
    // User pays LESS than fair value - value leaks from pool
}

function getSellInfo(...) external returns (uint256 price, uint256 fee) {
    price = _calculatePrice(...);  // Rounds down
    fee = _calculateFee(price);    // Rounds down  
    // User receives MORE than fair value - value leaks from pool
}

// SECURE: Round against user (in favor of protocol)
function getBuyInfo(...) external returns (uint256 price, uint256 fee) {
    price = _calculatePriceCeil(...);  // Round UP for buyer
    fee = _calculateFeeCeil(price);    // Round UP fees
}

function getSellInfo(...) external returns (uint256 price, uint256 fee) {
    price = _calculatePriceFloor(...);  // Round DOWN for seller
    fee = _calculateFeeFloor(price);    // Keep fee rounding consistent
}
```

---

### Pattern 9: Broken Multi-Token Pool Invariants (HIGH)

Applying 2-token AMM formulas to multi-token pools breaks invariants.

**Reference**: [h-01-protocol-allows-creating-broken-tri-crypto-cpmm-pools.md](../../../reports/constant_liquidity_amm/h-01-protocol-allows-creating-broken-tri-crypto-cpmm-pools.md) (Code4rena - MANTRA DEX, HIGH)

```solidity
// VULNERABLE: 2-token formula used for 3-token pool
function computeSwap(
    uint256 offerAmount,
    uint256 offerPool,
    uint256 askPool
) internal returns (uint256) {
    // Uniswap x*y=k formula - only valid for 2 tokens!
    return askPool * offerAmount / (offerPool + offerAmount);
}

// Creating pool with 3 tokens uses wrong formula
function createPool(address[] tokens) external {
    // No check: tokens.length <= 2 for CPMM
    if (poolType == PoolType.ConstantProduct) {
        // Allows 3+ token constant product pool
        // But swap formula only considers 2 tokens at a time!
        // Invariant x*y*z=k not enforced
    }
}

// Attack: Arbitrage between token pairs in same pool
// 1. Swap A→B changes A*B=k ratio
// 2. But A*B*C=k NOT maintained
// 3. Swap B→C at incorrect rate
// 4. Profit from broken invariant

// SECURE: Enforce 2-token limit for CPMM
function createPool(address[] tokens, PoolType poolType) external {
    if (poolType == PoolType.ConstantProduct) {
        require(tokens.length == 2, "CPMM requires exactly 2 tokens");
    }
}
```

---

### Pattern 10: Initial LP Token Calculation Ignoring Relative Values (HIGH)

Calculating initial LP tokens by adding token amounts ignores relative values.

**Reference**: [flawed-calculation-of-lp-tokens-in-liquidity-swap-pbc.md](../../../reports/constant_liquidity_amm/flawed-calculation-of-lp-tokens-in-liquidity-swap-pbc.md) (Halborn - Partisia, HIGH)

```solidity
// VULNERABLE: Adding token amounts regardless of value
function provideInitialLiquidity(
    uint256 tokenAAmount,  // e.g., 1000 USDC (6 decimals)
    uint256 tokenBAmount   // e.g., 1 ETH (18 decimals)
) external {
    // 1000 + 1e18 = dominated by ETH amount, ignores USDC value
    uint256 liquidityTokensMinted = tokenAAmount + tokenBAmount;
    liquidityProviders[msg.sender] = liquidityTokensMinted;
    
    // Attack: Provide 1 wei USDC + 1e18 wei worthless token
    // Receive 1e18+1 LP tokens, claim huge share of pool
}

// SECURE: Use geometric mean for initial liquidity
function provideInitialLiquidity(uint256 amount0, uint256 amount1) external {
    // Geometric mean: sqrt(x * y) - standard for AMMs
    uint256 liquidity = Math.sqrt(amount0 * amount1);
    
    // Lock minimum liquidity
    require(liquidity >= MINIMUM_LIQUIDITY, "Insufficient liquidity");
    _mint(address(0), MINIMUM_LIQUIDITY);
    _mint(msg.sender, liquidity - MINIMUM_LIQUIDITY);
}
```

---

## Secure Implementation Examples

### Secure Pattern 1: Protected Initialization with Immutable Flag

```solidity
// SECURE: One-time initialization with access control
abstract contract SecureInitializable {
    bool private _initialized;
    address private immutable _factory;
    
    modifier initializer() {
        require(!_initialized, "Already initialized");
        require(msg.sender == _factory, "Only factory");
        _initialized = true;
        _;
    }
    
    constructor(address factory_) {
        _factory = factory_;
    }
}

contract SecurePool is SecureInitializable {
    function initialize(uint160 sqrtPriceX96) external initializer {
        // Safe - can only be called once by factory
        _slot0.sqrtPriceX96 = sqrtPriceX96;
    }
}
```

### Secure Pattern 2: Consistent Underflow Handling

```solidity
// SECURE: Handle Uniswap V3 style underflow correctly
library FeeGrowthCalculator {
    function calculateOwedFees(
        uint256 feeGrowthInsideX128,
        uint256 feeGrowthInsideLastX128,
        uint128 liquidity
    ) internal pure returns (uint256 tokensOwed) {
        // Use unchecked to allow intentional underflow (Uniswap V3 pattern)
        unchecked {
            tokensOwed = FullMath.mulDiv(
                feeGrowthInsideX128 - feeGrowthInsideLastX128,
                liquidity,
                FixedPoint128.Q128
            );
        }
    }
}
```

### Secure Pattern 3: First Depositor Protection

```solidity
// SECURE: Virtual shares and minimum liquidity
contract SecureVault {
    uint256 private constant VIRTUAL_SHARES = 1e8;
    uint256 private constant VIRTUAL_ASSETS = 1;
    uint256 private constant MINIMUM_LIQUIDITY = 1000;
    
    function deposit(uint256 assets) external returns (uint256 shares) {
        uint256 supply = totalSupply();
        
        if (supply == 0) {
            shares = assets;
            require(shares >= MINIMUM_LIQUIDITY, "Below minimum");
            // Lock minimum to dead address
            _mint(address(0xdead), MINIMUM_LIQUIDITY);
            shares -= MINIMUM_LIQUIDITY;
        } else {
            // Virtual offset prevents inflation attack
            shares = ((assets + VIRTUAL_ASSETS) * (supply + VIRTUAL_SHARES)) 
                     / (totalAssets() + VIRTUAL_ASSETS) - VIRTUAL_SHARES;
        }
        
        _mint(msg.sender, shares);
    }
}
```

### Secure Pattern 4: Bounded Queue with Rate Limiting

```solidity
// SECURE: Rate-limited withdrawal queue
contract SecureWithdrawQueue {
    uint256 public constant MAX_PENDING_REQUESTS = 100;
    uint256 public constant MIN_WITHDRAWAL = 1e18;
    uint256 public constant COOLDOWN = 1 hours;
    
    mapping(address => uint256) public lastRequestTime;
    mapping(address => uint256) public pendingAmount;
    
    function requestWithdraw(uint256 amount) external {
        require(amount >= MIN_WITHDRAWAL, "Below minimum");
        require(block.timestamp >= lastRequestTime[msg.sender] + COOLDOWN, "Cooldown");
        
        // Aggregate requests instead of queuing individually
        pendingAmount[msg.sender] += amount;
        lastRequestTime[msg.sender] = block.timestamp;
    }
}
```

---

## Impact Analysis

### Technical Impact

| Impact Type | Severity | Description |
|-------------|----------|-------------|
| Complete DoS | HIGH | Counter overflow, queue flooding block all operations |
| Fund Theft | CRITICAL | Re-initialization allows draining contract |
| Share Dilution | HIGH | Inflation attack steals from depositors |
| Invariant Breaking | HIGH | Wrong arithmetic corrupts pool state |

### Financial Impact

1. **First Depositor Attack** (8/60 reports) - Inflation attack steals deposits
2. **Re-initialization Drain** (5/60 reports) - Complete fund theft
3. **Value Leakage** (10/60 reports) - Gradual loss from rounding errors
4. **DoS Extortion** (6/60 reports) - Griefing attacks on withdrawals

### Attack Scenarios

1. **Share Inflation Attack**
   - Be first depositor with 1 wei
   - Donate large amount directly to contract
   - Victim deposits, receives 0 shares (rounding)
   - Withdraw 1 share, receive victim's deposit

2. **Re-initialization Hijack**
   - Monitor for proxy deployments
   - Call initialize() with malicious parameters
   - Set permit2 to attacker contract
   - Drain approved tokens

3. **Fee Growth Underflow Exploit**
   - Position with high feeGrowthInsideLast (from underflow)
   - Protocol calculates 0 fees due to comparison
   - LP loses all accumulated fees

---

## Detection Patterns

### Static Analysis

```yaml
# Semgrep rule for initialization vulnerabilities
rules:
  - id: unprotected-initialize
    patterns:
      - pattern: |
          function initialize(...) external {
            ...
          }
      - pattern-not: |
          function initialize(...) external initializer {
            ...
          }
      - pattern-not: |
          function initialize(...) external {
            require(!initialized, ...);
            ...
          }
    message: "Initialize function lacks access control"
    severity: ERROR

  - id: fee-growth-comparison
    patterns:
      - pattern: |
          if ($CURRENT > $LAST) {
            ... = $CURRENT - $LAST;
          }
    message: "Fee growth should use unchecked subtraction, not comparison"
    severity: WARNING
```

### Manual Audit Checklist

- [ ] Is `initialize()` protected by initializer modifier?
- [ ] Are FullMath operations wrapped in `unchecked`?
- [ ] Is fee growth calculation using subtraction (not comparison)?
- [ ] Is first depositor protected with minimum liquidity lock?
- [ ] Are rounding directions consistent (favor protocol)?
- [ ] Are queues bounded with rate limiting?
- [ ] Are multi-token pools using correct invariant formulas?
- [ ] Is initial LP using geometric mean (not sum)?

---

## Real-World Examples

| Protocol | Vulnerability | Severity | Audit Firm | Year |
|----------|--------------|----------|------------|------|
| Morpho | FullMath overflow in 0.8 | HIGH | Spearbit | 2022 |
| Particle | Fee growth underflow | HIGH | Cantina | 2024 |
| MagicLP | Rounding amplification | HIGH | Code4rena | 2024 |
| Radiant | First depositor attack | HIGH | Pashov | 2024 |
| Mellow | Counter overflow DoS | MEDIUM | Cantina | 2024 |
| RestakeFi | Withdrawal queue DoS | HIGH | OpenZeppelin | 2024 |
| WishWish | Re-initialization | CRITICAL | Pashov | 2025 |
| Sudoswap | Inconsistent rounding | MEDIUM | Cyfrin | 2023 |
| MANTRA DEX | Broken tri-crypto invariant | HIGH | Code4rena | 2024 |
| Partisia | LP calculation flaw | HIGH | Halborn | 2024 |

---

## Keywords for Search

**Primary Terms:** denial of service, DoS, arithmetic, overflow, underflow, initialization

**Math Terms:** FullMath, mulDiv, rounding, precision, fee growth, geometric mean

**Attack Vectors:** inflation attack, first depositor, griefing, queue flooding, re-initialization

**Impacts:** fund theft, share dilution, invariant corruption, stuck funds

**Related APIs:** initialize(), deposit(), mulFloor(), mulCeil(), unchecked

**Code Patterns:** initializer modifier, virtual shares, minimum liquidity, rate limiting

**Protocol Examples:** morpho, particle, magiclp, radiant, mellow, sudoswap

---

## Related Vulnerabilities

- [Liquidity Management](./liquidity-management-vulnerabilities.md) - Deposit/withdrawal issues
- [Fee Collection](./fee-collection-distribution.md) - Fee calculation errors
- [Price Oracle Manipulation](./price-oracle-manipulation.md) - Price-related arithmetic

---

## References

1. [Uniswap V3 FullMath](https://github.com/Uniswap/v3-core/blob/main/contracts/libraries/FullMath.sol)
2. [OpenZeppelin ERC4626 Inflation Attack Defense](https://blog.openzeppelin.com/a-novel-defense-against-erc4626-inflation-attacks)
3. [Trail of Bits Yearn Audit TOB-YEARN-003](https://github.com/trailofbits/publications)
4. [Solidity 0.8 Breaking Changes](https://docs.soliditylang.org/en/v0.8.0/080-breaking-changes.html)

### Detection Patterns

#### Code Patterns to Look For
```
- See vulnerable pattern examples above for specific code smells
- Check for missing validation on critical state-changing operations
- Look for assumptions about external component behavior
```

#### Audit Checklist
- [ ] Verify all state-changing functions have appropriate access controls
- [ ] Check for CEI pattern compliance on external calls
- [ ] Validate arithmetic operations for overflow/underflow/precision loss
- [ ] Confirm oracle data freshness and sanity checks

### Keywords for Search

> These keywords enhance vector search retrieval:

`add`, `and`, `arithmetic`, `block.timestamp`, `buyShares`, `calculateOwedFees`, `computeSwap`, `createPool`, `denial-of-service`, `deposit`, `emptyRebalance`, `first-depositor`, `getBuyInfo`, `getOwedFee`, `getSellInfo`, `griefing`, `inflation`, `initialization`, `initialize`, `initializer`, `mint`, `msg.sender`, `mulDiv`, `overflow`, `processWithdrawals`, `reentrancy`, `rounding`, `underflow`
