---
# Core Classification (Required)
protocol: generic
chain: everychain
category: oracle
vulnerability_type: price_manipulation

# Attack Vector Details (Required)
attack_type: economic_exploit
affected_component: price_oracle

# Oracle-Specific Fields
oracle_provider: any
oracle_attack_vector: manipulation

# Technical Primitives (Required)
primitives:
  - flash_loan
  - spot_price
  - twap_oracle
  - lp_token_pricing
  - share_price
  - exchange_rate
  - reserve_ratio
  - scaling_factor
  - precision_loss
  - oracle_update
  - getReserves
  - balanceOf

# Impact Classification (Required)
severity: critical
impact: fund_loss
exploitability: 0.8
financial_impact: critical

# Context Tags
tags:
  - defi
  - lending
  - dex
  - amm
  - vault
  - real_exploit
  - flash_loan
  - price_oracle

# Version Info
language: solidity
version: all

source: DeFiHackLabs
---

## Flash Loan Oracle Manipulation

### Overview

Price oracle manipulation using flash loans is one of the most devastating attack vectors in DeFi, responsible for over $500M in losses across 100+ exploits from 2021-2025. Attackers use flash loans to temporarily manipulate on-chain price calculations (spot prices, reserves ratios, share prices) within a single transaction, exploiting protocols that rely on these manipulable price sources for critical operations like collateral valuation, liquidations, and reward calculations.

### Vulnerability Description

#### Root Cause

Protocols that derive prices from on-chain state (AMM reserves, vault share prices, LP token values) without adequate protection against flash loan manipulation are vulnerable. The core issue is a mismatch between:
1. **Price derivation**: Using instantly manipulable on-chain data
2. **Economic security**: Insufficient cost/stake requirements to manipulate prices
3. **Validation**: Missing sanity checks, TWAP comparisons, or multi-block confirmation

#### Attack Categories

This vulnerability manifests in five main patterns:

**1. Spot Price Manipulation** - Direct reserve ratio manipulation
**2. TWAP Oracle Manipulation** - Multi-block oracle attacks 
**3. LP Token Price Manipulation** - Inflating LP token values
**4. Share Price / Exchange Rate Manipulation** - Vault inflation attacks
**5. Faulty Oracle Configuration** - Cheap/missing oracle security

---

### Pattern 1: Spot Price Manipulation via Flash Loans

#### Mechanism
Attackers borrow large amounts via flash loan, swap to drastically change AMM reserve ratios, exploit the manipulated price in a vulnerable protocol, then swap back and repay.

#### Attack Scenario
1. Flash loan large amount of token A
2. Swap token A for token B in AMM pool, draining B reserves
3. Price of B (derived from reserves) artificially inflates
4. Call vulnerable protocol that uses `getReserves()` for pricing
5. Extract value (borrow against inflated collateral, claim inflated rewards)
6. Swap back and repay flash loan

#### Vulnerable Pattern Examples

**Example 1: EGD Finance (2022-08, $36K)** [HIGH]
```solidity
// @PoC: DeFiHackLabs/src/test/2022-08/EGD_Finance_exp.sol
// VULNERABLE: Price derived from AMM reserves
function getEGDPrice() external view returns (uint256) {
    // Gets reserves directly from Pancakeswap pair
    (uint112 reserve0, uint112 reserve1,) = EGD_USDT_LPPool.getReserves();
    // @audit Price = reserve ratio, instantly manipulable with flash loan
    return (reserve1 * 1e18) / reserve0;
}

// Attack: Flash loan 99.99% of USDT from pool
// -> EGD price drops to near zero
// -> Claim massive EGD rewards (calculated at manipulated price)
// -> Swap EGD back to USDT for profit
```

**Example 2: Allbridge (2023-04, $550K)** [HIGH]
```solidity
// @PoC: DeFiHackLabs/src/test/2023-04/Allbridge_exp.sol
// VULNERABLE: Bridge swap uses pool reserves for pricing
function swap(uint256 amount, bytes32 fromToken, bytes32 toToken, address recipient) external {
    // @audit Pool imbalance allows extraction of value
    // Attacker deposits into pool, swaps to create imbalance
    // Then withdraws at favorable rate
}

// Attack pattern:
// 1. Flashloan $7.5M BUSD
// 2. Deposit $5M into liquidity pool
// 3. Large swap creates imbalanced reserves
// 4. Withdraw liquidity at inflated rate
// 5. Small swap ($40K) extracts $790K due to imbalance
```

**Example 3: Generic Spot Price Oracle** [CRITICAL]
```solidity
// VULNERABLE: Direct reserve-based pricing
function getTokenPrice(address pair) public view returns (uint256) {
    (uint112 reserve0, uint112 reserve1,) = IUniswapV2Pair(pair).getReserves();
    // @audit Instantly manipulable - no TWAP, no sanity checks
    return (uint256(reserve1) * PRECISION) / uint256(reserve0);
}

function calculateCollateralValue(uint256 amount) public view returns (uint256) {
    // @audit Uses manipulated price for collateral valuation
    return amount * getTokenPrice(tokenPair) / PRECISION;
}
```

---

### Pattern 2: TWAP Oracle Manipulation

#### Mechanism
Time-Weighted Average Price (TWAP) oracles can be manipulated if:
- Observation window is too short
- Oracle uses outdated slot0 spot price
- Multi-block manipulation is economically feasible

#### Attack Scenario
1. Identify TWAP with short averaging window (e.g., 4 observations over 3 hours)
2. Execute trades across multiple blocks to shift average price
3. Wait for observation updates
4. Exploit protocol using manipulated TWAP

#### Vulnerable Pattern Examples

**Example 1: Rodeo Finance (2023-07, $888K)** [CRITICAL]
```solidity
// @PoC: DeFiHackLabs/src/test/2023-07/RodeoFinance_exp.sol
// Root Cause: TWAP averaged only 4 price updates, each 45 minutes apart
// Attack: Multi-block manipulation of Camelot V2 TWAP over ~3 hours

// VULNERABLE: Short TWAP window
function getTWAPPrice() external view returns (uint256) {
    // @audit Only 4 observations, 45 min intervals = 3 hour window
    // Attacker can manipulate price over multiple blocks
    uint256[] memory prices = oracle.getLastNPrices(4);
    return average(prices);
}

// Attack pattern:
// 1. Large swap in block N to move spot price
// 2. Wait 45 minutes for observation
// 3. Repeat 3 more times
// 4. TWAP now reflects manipulated average
// 5. Bypass health factor check, borrow funds
```

**Example 2: Using slot0 Instead of TWAP** [HIGH]
```solidity
// VULNERABLE: Uses instantaneous price from slot0
function getPrice() external view returns (uint256) {
    (uint160 sqrtPriceX96,,,,,,) = IUniswapV3Pool(pool).slot0();
    // @audit slot0 is spot price, not TWAP - instantly manipulable
    return convertSqrtPriceToPrice(sqrtPriceX96);
}

// SECURE: Use actual TWAP from observations
function getPrice() external view returns (uint256) {
    uint32[] memory secondsAgos = new uint32[](2);
    secondsAgos[0] = TWAP_PERIOD; // e.g., 30 minutes
    secondsAgos[1] = 0;
    
    (int56[] memory tickCumulatives,) = IUniswapV3Pool(pool).observe(secondsAgos);
    int24 avgTick = int24((tickCumulatives[1] - tickCumulatives[0]) / int56(int32(TWAP_PERIOD)));
    return getQuoteAtTick(avgTick, amountIn, baseToken, quoteToken);
}
```

---

### Pattern 3: LP Token Price Manipulation

#### Mechanism
LP tokens derive value from underlying pool reserves. Manipulating reserves inflates LP token price, enabling over-borrowing against LP collateral.

#### Attack Scenario
1. Flash loan large amounts of pool tokens
2. Swap/add liquidity to inflate one side of pool
3. LP token price calculation returns inflated value
4. Borrow against inflated LP collateral
5. Restore pool state and repay

#### Vulnerable Pattern Examples

**Example 1: Lodestar Finance (2022-12, $4M)** [CRITICAL]
```solidity
// @PoC: DeFiHackLabs/src/test/2022-12/Lodestar_exp.sol
// Attack: Donate GLP to inflate plvGLP price, borrow against inflated collateral

// VULNERABLE: LP price based on manipulable underlying
function getPlvGLPPrice() public view returns (uint256) {
    uint256 totalAssets = sGLP.balanceOf(address(depositor));
    uint256 totalSupply = plvGLP.totalSupply();
    // @audit Donation inflates totalAssets, manipulating price
    return (totalAssets * 1e18) / totalSupply;
}

// Attack pattern:
// 1. Flash loan ETH, USDC, etc.
// 2. Mint GLP tokens via GMX
// 3. Donate GLP to GlpDepositor (depositor.donate(glpAmount))
// 4. plvGLP price inflates dramatically
// 5. Use plvGLP as collateral to borrow all assets
// 6. Protocol becomes insolvent
```

**Example 2: Generic LP Token Pricing** [HIGH]
```solidity
// VULNERABLE: Fair LP pricing without manipulation checks
function getLPTokenPrice(address pair) public view returns (uint256) {
    uint256 totalSupply = IUniswapV2Pair(pair).totalSupply();
    (uint112 r0, uint112 r1,) = IUniswapV2Pair(pair).getReserves();
    
    uint256 price0 = getExternalPrice(token0);
    uint256 price1 = getExternalPrice(token1);
    
    // @audit Even with external prices, reserves can be manipulated
    // to create arbitrage between LP value and actual value
    uint256 totalValue = (uint256(r0) * price0 + uint256(r1) * price1);
    return totalValue / totalSupply;
}
```

---

### Pattern 4: Share Price / Exchange Rate Manipulation

#### Mechanism
Vaults using share-based accounting (ERC4626 pattern) can be manipulated via:
- Donation attacks (inflate totalAssets)
- First depositor attacks (control initial share price)
- Exchange rate manipulation before user deposits/withdrawals

#### Attack Scenario
1. Deposit small amount to vault, receive shares
2. Donate large amount to inflate share price
3. Protocol using vault for collateral sees inflated value
4. Borrow against inflated collateral
5. Withdraw donation (if possible) or accept donation as cost

#### Vulnerable Pattern Examples

**Example 1: ResupplyFi (2025-06, $9.6M)** [CRITICAL]
```solidity
// @PoC: DeFiHackLabs/src/test/2025-06/ResupplyFi_exp.sol
// Attack: Manipulate sCRVUSD oracle to borrow excessive reUSD

// VULNERABLE: Oracle manipulation via donation
function _manipulateOracles() internal {
    // Donate crvUSD to controller to manipulate price
    crvUsd.transfer(crvUSDController, crvUsdTransferAmount);
    // Mint tiny amount of sCRVUSD
    sCrvUsdContract.mint(sCrvUsdMintAmount); // Just 1 wei!
}

function _borrowAndSwapReUSD() internal {
    // With just 1 wei of collateral, borrow 10M reUSD
    resupplyVault.addCollateralVault(sCrvUsdMintAmount, address(this));
    resupplyVault.borrow(borrowAmount, 0, address(this)); // 10,000,000e18 reUSD!
}
```

**Example 2: Zunami Protocol (2023-08, $2M)** [CRITICAL]
```solidity
// @PoC: DeFiHackLabs/src/test/2023-08/Zunami_exp.sol
// Attack: Donate SDT tokens to inflate UZD balance calculation

// VULNERABLE: Balance includes donated tokens
// UZD.balanceOf uses this calculation:
// uint256 amountIn = sdtEarned + _config.sdt.balanceOf(address(this));
// uint256 sdtEarningsInFeeToken = priceTokenByExchange(amountIn, path);

// Attack pattern:
// 1. Flash loan USDC and WETH
// 2. Swap to acquire crvFRAX, UZD tokens
// 3. Swap WETH to SDT
// 4. Donate SDT to MIMCurveStakeDao contract
// 5. Manipulate reserves via large swaps
// 6. Call UZD.cacheAssetPrice() to rebase at inflated rate
// 7. UZD balance artificially inflated
// 8. Swap inflated UZD back to stables for profit
```

**Example 3: Woofi (2024-03, $8M)** [CRITICAL]
```solidity
// @PoC: DeFiHackLabs/src/test/2024-03/Woofi_exp.sol
// Attack: Price oracle manipulation via sequential swaps

// VULNERABLE: Internal oracle updated by swaps
function swap(
    address fromToken,
    address toToken,
    uint256 fromAmount,
    uint256 minToAmount,
    address to,
    address rebateTo
) external returns (uint256 realToAmount) {
    // @audit Each swap updates internal price state
    // Sequential swaps can progressively manipulate price
}

// Attack pattern:
// 1. Flash loan WOO tokens from LBT pool
// 2. Borrow WOO from Silo using USDC collateral
// 3. Large USDC->WETH swap moves price
// 4. USDC->WOO swap further manipulates WOO oracle price
// 5. WOO->USDC swap exploits manipulated price
// 6. Drain remaining USDC with tiny swap
```

---

### Pattern 5: Faulty Oracle Configuration / Low-Cost Manipulation

#### Mechanism
Some oracles have insufficient economic security - the cost to manipulate prices is lower than potential profit. This includes:
- Oracles with low staking requirements
- Missing dispute windows
- Single-source oracles without validation

#### Vulnerable Pattern Examples

**Example 1: BonqDAO / TellorFlex (2023-02, $88M)** [CRITICAL]
```solidity
// @PoC: DeFiHackLabs/src/test/2023-02/BonqDAO_exp.sol
// Root Cause: TellorFlex oracle stake ($10 TRB) << potential profit ($88M)

// VULNERABLE: Uses getCurrentValue without dispute window
function getPrice() external view returns (uint256) {
    bytes memory priceData = TellorFlex.getCurrentValue(queryId);
    // @audit No dispute window check - uses immediate price
    // @audit Staking cost to report = ~$100, potential profit = $88M
    return abi.decode(priceData, (uint256));
}

// Attack pattern (Two transactions):
// TX1: Report wALBT price as 5e27 (extremely high)
//      -> Borrow 100M BEUR with 0.1 wALBT collateral
// TX2: Report wALBT price as 0.0000001e18 (extremely low)
//      -> Liquidate all other wALBT positions
//      -> Collect massive liquidation rewards

// SECURE: Use getDataBefore with dispute window
function getPrice() external view returns (uint256) {
    (bool success, bytes memory priceData, uint256 timestamp) = 
        TellorFlex.getDataBefore(queryId, block.timestamp - DISPUTE_WINDOW);
    require(success && block.timestamp - timestamp < MAX_STALENESS);
    return abi.decode(priceData, (uint256));
}
```

**Example 2: Generic Low-Security Oracle** [HIGH]
```solidity
// VULNERABLE: No validation of reporter stake/credibility
function submitPrice(uint256 price) external {
    // @audit Anyone can submit, no minimum stake
    // @audit No comparison to trusted sources
    lastPrice = price;
    lastUpdateTime = block.timestamp;
}

// VULNERABLE: Using oracle without sanity checks
function getCollateralRatio(address user) external view returns (uint256) {
    uint256 price = oracle.lastPrice();
    // @audit No bounds checking, no deviation threshold
    return (collateral[user] * price) / debt[user];
}
```

---

### Pattern 6: Precision Loss in Price Calculations (BalancerV2 Pattern)

#### Mechanism
Mathematical operations with different token decimals/scaling factors can cause precision loss, allowing attackers to extract value through repeated small transactions.

#### Vulnerable Pattern Examples

**Example 1: BalancerV2 (2025-11, $120M)** [CRITICAL]
```solidity
// @PoC: DeFiHackLabs/src/test/2025-11/BalancerV2_exp.sol
// Root Cause: Precision loss in swapGivenOut with scaling factors

function swapGivenOut(
    uint256[] memory balances,
    uint256[] memory scalingFactors,
    uint256 tokenIndexIn,
    uint256 tokenIndexOut,
    uint256 tokenAmountOut,
    uint256 amplificationParameter,
    uint256 swapFee
) public view returns (uint256[] memory) {
    // Scale amounts for calculation
    uint256 amountOutScaled = FixedPoint.mulDown(tokenAmountOut, scalingFactors[tokenIndexOut]);
    // @audit Precision loss when tokenAmountOut is small relative to scalingFactor
    // @audit Repeated swaps with carefully chosen amounts can extract value
    
    uint256 amountInScaled = StableMath._calcInGivenOut(
        amplificationParameter, balanceScaled, tokenIndexIn, tokenIndexOut,
        amountOutScaled, invariant
    );
    
    // Reverse scaling
    uint256 rawAmountIn = FixedPoint.divUp(amountInScaled, scalingFactors[tokenIndexIn]);
    // @audit divUp combined with previous mulDown creates extractable rounding
}

// Attack pattern:
// 1. Drain pool reserves to minimal amounts via batch swaps
// 2. Execute many small swaps where precision loss accumulates
// 3. Each swap extracts tiny amounts due to rounding
// 4. Repeated hundreds of times = massive extraction
```

---

### Pattern 7: Protocol-Specific Price Manipulation (Jimbo Pattern)

#### Mechanism
Protocols with custom pricing/rebalancing mechanisms can be exploited by understanding and gaming the specific mechanics.

#### Vulnerable Pattern Examples

**Example 1: Jimbo Protocol (2023-05, $8M)** [CRITICAL]
```solidity
// @PoC: DeFiHackLabs/src/test/2023-05/Jimbo_exp.sol
// Root Cause: Liquidity rebalancing mechanism gameable via price manipulation

// VULNERABLE: Rebalancing triggered at specific price points
function shift() external {
    require(getActiveId() > triggerBin, "Below trigger");
    // @audit Predictable rebalancing behavior exploitable
    // Moves liquidity to new price range
}

function reset() external {
    // @audit Resets state, allowing repeated exploitation
}

// Attack pattern:
// 1. Flash loan ETH
// 2. Swap ETH->JIMBO to move price above triggerBin
// 3. Call shift() - liquidity moves to high bin
// 4. Buy all JIMBO in normal bins
// 5. Call shift() again - moves more liquidity
// 6. Sell JIMBO below anchorBin
// 7. Call reset() to normalize state
// 8. Repeat extraction multiple times
// 9. Swap JIMBO back to ETH for profit
```

---

### Impact Analysis

#### Technical Impact
- **Incorrect pricing**: Assets valued at manipulated rates
- **Under-collateralized loans**: Borrowers extract more than collateral value
- **Unfair liquidations**: Honest users liquidated at manipulated prices
- **Protocol insolvency**: Bad debt accumulates
- **Reward theft**: Inflated reward calculations

#### Business Impact
- **Direct fund loss**: Typically $100K - $100M per incident
- **Protocol death**: Many protocols shut down after exploits
- **User trust destruction**: TVL exodus post-exploit
- **Cascading failures**: Protocols using affected protocol as dependency

#### Financial Impact Summary (Selected Incidents)
| Protocol | Date | Loss | Pattern |
|----------|------|------|---------|
| BalancerV2 | 2025-11 | $120M | Precision loss |
| BonqDAO | 2023-02 | $88M | Cheap oracle manipulation |
| Cream Finance | 2021-10 | $130M | Flash loan oracle manipulation |
| MonoX | 2021-11 | $31M | Self-referential pricing |
| UwULend | 2024-06 | $19.3M | Price manipulation |
| Jimbo | 2023-05 | $8M | Protocol-specific manipulation |
| Woofi | 2024-03 | $8M | Internal oracle manipulation |
| Lodestar | 2022-12 | $4M | LP token price inflation |
| ResupplyFi | 2025-06 | $9.6M | Share price manipulation |

---

### Secure Implementation

**Fix 1: Use Chainlink or Other Trusted Oracle** [RECOMMENDED]
```solidity
// SECURE: External oracle with proper validation
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

function getPrice(address feed) public view returns (uint256) {
    AggregatorV3Interface priceFeed = AggregatorV3Interface(feed);
    (
        uint80 roundId,
        int256 answer,
        uint256 startedAt,
        uint256 updatedAt,
        uint80 answeredInRound
    ) = priceFeed.latestRoundData();
    
    // Validate freshness
    require(updatedAt > block.timestamp - MAX_STALENESS, "Stale price");
    require(answer > 0, "Invalid price");
    require(answeredInRound >= roundId, "Stale round");
    
    // Validate bounds
    require(answer >= MIN_PRICE && answer <= MAX_PRICE, "Price out of bounds");
    
    return uint256(answer);
}
```

**Fix 2: Use Proper TWAP Implementation**
```solidity
// SECURE: UniswapV3 TWAP with adequate window
function getTWAPPrice(
    address pool,
    uint32 twapPeriod // e.g., 1800 for 30 minutes
) public view returns (uint256) {
    require(twapPeriod >= MIN_TWAP_PERIOD, "TWAP period too short");
    
    uint32[] memory secondsAgos = new uint32[](2);
    secondsAgos[0] = twapPeriod;
    secondsAgos[1] = 0;
    
    (int56[] memory tickCumulatives,) = IUniswapV3Pool(pool).observe(secondsAgos);
    
    int56 tickCumulativesDelta = tickCumulatives[1] - tickCumulatives[0];
    int24 avgTick = int24(tickCumulativesDelta / int56(int32(twapPeriod)));
    
    return OracleLibrary.getQuoteAtTick(avgTick, amountIn, baseToken, quoteToken);
}
```

**Fix 3: Multi-Oracle with Deviation Check**
```solidity
// SECURE: Compare multiple sources, reject outliers
function getValidatedPrice() public view returns (uint256) {
    uint256 chainlinkPrice = getChainlinkPrice();
    uint256 twapPrice = getTWAPPrice();
    
    // Check deviation between sources
    uint256 deviation = calculateDeviation(chainlinkPrice, twapPrice);
    require(deviation < MAX_DEVIATION, "Price sources diverge");
    
    // Use average or primary source
    return (chainlinkPrice + twapPrice) / 2;
}
```

**Fix 4: Flash Loan Protection**
```solidity
// SECURE: Block same-transaction price reads after modifications
mapping(address => uint256) private lastModificationBlock;

modifier flashLoanProtection() {
    require(
        block.number > lastModificationBlock[msg.sender],
        "Cannot use in same block as modification"
    );
    _;
}

function swap(...) external {
    // ... swap logic
    lastModificationBlock[msg.sender] = block.number;
}

function getPrice() external view flashLoanProtection returns (uint256) {
    // Price cannot be read in same block as swap
}
```

**Fix 5: Virtual Price with Manipulation Resistance**
```solidity
// SECURE: Use virtual reserves for pricing (like Curve)
function getVirtualPrice() public view returns (uint256) {
    // Virtual price smoothly tracks actual price
    // Resistant to instantaneous manipulation
    uint256 xp0 = (reserves[0] * rates[0]) / PRECISION;
    uint256 xp1 = (reserves[1] * rates[1]) / PRECISION;
    
    uint256 D = getD([xp0, xp1], amp);
    return (D * PRECISION) / totalSupply;
}
```

**Fix 6: Minimum Amount and Slippage Protection**
```solidity
// SECURE: Prevent precision loss attacks
function swap(uint256 amountIn, uint256 minAmountOut) external {
    uint256 amountOut = calculateAmountOut(amountIn);
    
    // Minimum output prevents dust amounts
    require(amountOut >= MIN_SWAP_AMOUNT, "Amount too small");
    require(amountOut >= minAmountOut, "Slippage exceeded");
    
    // Round in protocol's favor
    amountOut = amountOut - 1; // Small haircut
}
```

---

### Detection Patterns

#### Code Patterns to Look For
```
- Direct use of getReserves() for pricing
- balanceOf() used in price/share calculations
- slot0 used instead of TWAP observe()
- Missing staleness checks on oracle data
- Single-source price feeds
- No deviation/sanity bounds on prices
- Price derivation in same transaction as state change
- totalAssets / totalSupply without donation protection
- Scaling factor operations without minimum amount checks
- Custom oracles with low staking requirements
```

#### Audit Checklist
- [ ] **Oracle Source**: Is price from manipulable on-chain source (reserves, balances)?
- [ ] **TWAP Usage**: If TWAP, is window long enough (>30 min)?
- [ ] **Multi-source**: Are multiple price sources compared?
- [ ] **Deviation Bounds**: Are there min/max price sanity checks?
- [ ] **Staleness**: Is there a maximum age for price data?
- [ ] **Flash Loan**: Can price be read and used in same block as manipulation?
- [ ] **Donation Attack**: Can assets be donated to inflate share price?
- [ ] **Economic Security**: Is manipulation cost > potential profit?
- [ ] **Precision**: Are there minimum amounts preventing dust attacks?
- [ ] **Sequencer Check**: For L2, is sequencer uptime verified?

#### Semgrep Patterns
```yaml
rules:
  - id: spot-price-from-reserves
    pattern: |
      $PAIR.getReserves()
    message: "Direct reserve access - check for price manipulation vulnerability"
    
  - id: slot0-price-usage
    pattern: |
      $POOL.slot0()
    message: "Using slot0 spot price - consider TWAP instead"
    
  - id: balance-based-pricing
    pattern: |
      $TOKEN.balanceOf($CONTRACT) / $SUPPLY
    message: "Balance-based pricing vulnerable to donation attacks"
```

---

### Real-World Examples

#### Major Exploits (2021-2025)

**2025:**
- **BalancerV2** - November 2025 - $120M - Precision loss in scaling
- **ResupplyFi** - June 2025 - $9.6M - Share price manipulation
- **GMX** - July 2025 - $41M - Share price manipulation

**2024:**
- **UwULend** - June 2024 - $19.3M - Price manipulation
- **Woofi** - March 2024 - $8M - Internal oracle manipulation
- **MorphoBlue** - October 2024 - $230K - Overpriced oracle asset

**2023:**
- **BonqDAO** - February 2023 - $88M - Cheap oracle manipulation
- **Jimbo** - May 2023 - $8M - Protocol-specific manipulation
- **Rodeo Finance** - July 2023 - $888K - TWAP manipulation
- **Zunami** - August 2023 - $2M - Donation attack

**2022:**
- **EGD Finance** - August 2022 - $36K - Flash loan reserve manipulation
- **Lodestar** - December 2022 - $4M - LP token price inflation
- **Elephant Money** - April 2022 - $11.2M - Flash loan oracle manipulation

**2021:**
- **Cream Finance** - October 2021 - $130M - Flash loan oracle manipulation
- **MonoX Finance** - November 2021 - $31M - Self-referential pricing
- **Indexed Finance** - October 2021 - $16M - Price manipulation

---

### Prevention Guidelines

#### Development Best Practices
1. **Never use spot prices** from AMMs for critical pricing
2. **Always use external oracles** (Chainlink, Pyth) with proper validation
3. **If TWAP required**, use minimum 30-minute window, ideally longer
4. **Implement multi-oracle design** with deviation checks
5. **Add minimum amounts** to prevent precision attacks
6. **Use virtual/smoothed prices** resistant to manipulation
7. **Block same-block price reads** after state modifications
8. **Implement circuit breakers** for extreme price movements

#### Testing Requirements
- **Unit tests**: Oracle staleness, bounds validation, deviation checks
- **Integration tests**: Flash loan attack simulations
- **Invariant tests**: Price sanity across all states
- **Fuzzing targets**: Price calculation functions with extreme inputs
- **Fork tests**: Replay known exploits against your implementation

#### Monitoring
- Alert on large price deviations (>5% in single block)
- Monitor flash loan usage targeting your protocol
- Track oracle price vs market price divergence
- Watch for unusual liquidation patterns

---

### References

#### Technical Documentation
- [Chainlink Price Feed Documentation](https://docs.chain.link/data-feeds)
- [Uniswap V3 TWAP Oracle Guide](https://docs.uniswap.org/concepts/protocol/oracle)
- [ERC4626 Security Considerations](https://eips.ethereum.org/EIPS/eip-4626#security-considerations)

#### Security Research
- [samczsun: Taking Undercollateralized Loans](https://samczsun.com/taking-undercollateralized-loans-for-fun-and-for-profit/)
- [Rekt News: Leaderboard](https://rekt.news/leaderboard/)
- [DeFiHackLabs Repository](https://github.com/SunWeb3Sec/DeFiHackLabs)

#### Post-Mortems
- [BonqDAO - Omniscia Analysis](https://medium.com/@omniscia.io/bonq-protocol-incident-post-mortem-4fd79fe5c932)
- [Lodestar - Official Post-Mortem](https://blog.lodestarfinance.io/post-mortem-summary-13f5fe0bb336)
- [Rodeo Finance - Post-Mortem](https://medium.com/@Rodeo_Finance/rodeo-post-mortem-overview-f35635c14101)

---

### Keywords for Search

`price manipulation`, `flash loan attack`, `oracle manipulation`, `spot price`, `TWAP manipulation`, `getReserves`, `slot0`, `LP token price`, `share price manipulation`, `exchange rate attack`, `donation attack`, `vault inflation`, `precision loss`, `scaling factor`, `first depositor attack`, `collateral manipulation`, `liquidation exploit`, `under-collateralized loan`, `reserve manipulation`, `balanceOf pricing`, `totalAssets manipulation`, `ERC4626 attack`, `AMM oracle`, `DEX price oracle`, `on-chain oracle`, `price feed manipulation`, `economic exploit`, `arbitrage attack`

---

### Related Vulnerabilities

- [DB/oracle/chainlink/CHAINLINK_PRICE_FEED_VULNERABILITIES.md](../chainlink/CHAINLINK_PRICE_FEED_VULNERABILITIES.md)
- [DB/oracle/pyth/PYTH_ORACLE_VULNERABILITIES.md](../pyth/PYTH_ORACLE_VULNERABILITIES.md)
- [DB/general/vault-inflation-attack/vault-inflation-attack.md](../../general/vault-inflation-attack/vault-inflation-attack.md)
- [DB/tokens/erc4626/ERC4626_VAULT_VULNERABILITIES.md](../../tokens/erc4626/ERC4626_VAULT_VULNERABILITIES.md)
- [DB/general/flash-loan-attacks/FLASH_LOAN_VULNERABILITIES.md](../../general/flash-loan-attacks/FLASH_LOAN_VULNERABILITIES.md)
- [DB/amm/concentrated-liquidity/price-oracle-manipulation.md](../../amm/concentrated-liquidity/price-oracle-manipulation.md)

---

## DeFiHackLabs Real-World Exploits (122 incidents)

**Category**: Price Manipulation, Oracle Issues | **Total Losses**: $440.5M | **Sub-variants**: 11

### Sub-variant Breakdown

#### Price-Manipulation/Generic (92 exploits, $317.5M)

- **CreamFinance** (2021-10, $130.0M, None) | PoC: `DeFiHackLabs/src/test/2021-10/Cream_2_exp.sol`
- **GMX** (2025-07, $41.0M, None) | PoC: `DeFiHackLabs/src/test/2025-07/gmx_exp.sol`
- **MonoX Finance** (2021-11, $31.0M, ethereum) | PoC: `DeFiHackLabs/src/test/2021-11/Mono_exp.sol`
- *... and 89 more exploits*

#### Price-Manipulation/Oracle Manipulation (13 exploits, $117.8M)

- **BonqDAO** (2023-02, $88.0M, polygon) | PoC: `DeFiHackLabs/src/test/2023-02/BonqDAO_exp.sol`
- **DEUS DAO** (2022-04, $13.0M, fantom) | PoC: `DeFiHackLabs/src/test/2022-04/deus_exp.sol`
- **ElephantMoney** (2022-04, $11.2M, bsc) | PoC: `DeFiHackLabs/src/test/2022-04/Elephant_Money_exp.sol`
- *... and 10 more exploits*

#### Price-Manipulation/Twap Oracle (1 exploits, $888K)

- **RodeoFinance** (2023-07, $888K, arbitrum) | PoC: `DeFiHackLabs/src/test/2023-07/RodeoFinance_exp.sol`

#### Price-Manipulation/Pair Balance (5 exploits, $1.2M)

- **YYDS** (2022-09, $742K, bsc) | PoC: `DeFiHackLabs/src/test/2022-09/Yyds_exp.sol`
- **RES** (2022-10, $291K, bsc) | PoC: `DeFiHackLabs/src/test/2022-10/RES_exp.sol`
- **RADT** (2022-09, $94K, bsc) | PoC: `DeFiHackLabs/src/test/2022-09/RADT_exp.sol`
- *... and 2 more exploits*

#### Price-Manipulation/Flash Loan Price (2 exploits, $300K)

- **ImpermaxV3** (2025-04, $300K, base) | PoC: `DeFiHackLabs/src/test/2025-04/ImpermaxV3_exp.sol`
- **NXUSD** (2022-09, N/A, avalanche) | PoC: `DeFiHackLabs/src/test/2022-09/NXUSD_exp.sol`

#### Price-Manipulation/Pool Manipulation (2 exploits, $78K)

- **KubSplit** (2023-09, $78K, bsc) | PoC: `DeFiHackLabs/src/test/2023-09/Kub_Split_exp.sol`
- **pSeudoEth** (2023-10, $1, ethereum) | PoC: `DeFiHackLabs/src/test/2023-10/pSeudoEth_exp.sol`

#### Oracle-Issues/Faulty Oracle (3 exploits, $1.5M)

- **Moonwell** (2025-11, $1.0M, base) | PoC: `DeFiHackLabs/src/test/2025-11/Moonwell_exp.sol`
- **CompoundUni** (2024-02, $440K, ethereum) | PoC: `DeFiHackLabs/src/test/2024-02/CompoundUni_exp.sol`
- **Paribus** (2025-01, $86K, arbitrum) | PoC: `DeFiHackLabs/src/test/2025-01/Paribus_exp.sol`

#### Oracle-Issues/Health Factor Check (1 exploits, $464K)

- **WiseLending** (2024-01, $464K, ethereum) | PoC: `DeFiHackLabs/src/test/2024-01/WiseLending03_exp.sol`

#### Oracle-Issues/Price Dependency (1 exploits, $447K)

- **vETH** (2024-11, $447K, ethereum) | PoC: `DeFiHackLabs/src/test/2024-11/vETH_exp.sol`

#### Oracle-Issues/Overpriced Asset (1 exploits, $230K)

- **MorphoBlue** (2024-10, $230K, None) | PoC: `DeFiHackLabs/src/test/2024-10/MorphoBlue_exp.sol`

#### Oracle-Issues/Stale Price (1 exploits, $21K)

- **Zenterest** (2024-08, $21K, ethereum) | PoC: `DeFiHackLabs/src/test/2024-08/Zenterest_exp.sol`

### Complete DeFiHackLabs Exploit Table

| Protocol | Date | Loss | Vulnerability Sub-type | Chain |
|----------|------|------|----------------------|-------|
| CreamFinance | 2021-10-27 | $130.0M | Price Manipulation | None |
| BonqDAO | 2023-02-02 | $88.0M | Price Oracle Manipulation | polygon |
| GMX | 2025-07-09 | $41.0M | Share price manipulation | None |
| MonoX Finance | 2021-11-30 | $31.0M | Price Manipulation | ethereum |
| CompounderFinance | 2023-06-07 | $27.2M | Manipulation of funds through fluctuations in the amount of exchangeable assets | ethereum |
| UwULend | 2024-06-10 | $19.3M | Price Manipulation | ethereum |
| Indexed Finance | 2021-10-15 | $16.0M | Price Manipulation | ethereum |
| DEUS DAO | 2022-04-28 | $13.0M | Flashloan & Price Oracle Manipulation | fantom |
| ElephantMoney | 2022-04-12 | $11.2M | Flashloan & Price Oracle Manipulation | bsc |
| ResupplyFi | 2025-06-26 | $9.6M | Share price manipulation | ethereum |
| Jimbo | 2023-05-29 | $8.0M | Protocol Specific Price Manipulation | None |
| Woofi | 2024-03-05 | $8.0M | Price Manipulation | arbitrum |
| Gamma | 2024-01-04 | $6.3M | Price manipulation | arbitrum |
| Lodestar | 2022-12-11 | $4.0M | FlashLoan price manipulation | arbitrum |
| Fortress Loans | 2022-05-08 | $3.0M | Malicious Proposal & Price Oracle Manipulation | None |
| MBUToken | 2025-05-11 | $2.2M | Price Manipulation not confirmed | bsc |
| ZunamiProtocol | 2023-08-14 | $2.0M | Price Manipulation | ethereum |
| 0vix | 2023-04-28 | $2.0M | FlashLoan Price Manipulation | polygon |
| NGP | 2025-09-18 | $2.0M | Price Manipulation | bsc |
| OneRing Finance | 2022-03-21 | $1.4M | Flashloan & Price Oracle Manipulation | fantom |
| Caterpillar_Coin_CUT | 2024-09-10 | $1.4M | Price Manipulation | None |
| BH | 2023-10-11 | $1.3M | Price manipulation | bsc |
| Rikkei Finance | 2022-04-15 | $1.1M | Access control & Price Oracle Manipulation | bsc |
| Moonwell | 2025-11-04 | $1.0M | Faulty Oracle | base |
| Conic Finance 02 | 2023-07-22 | $934K | Price Manipulation | ethereum |
| RodeoFinance | 2023-07-11 | $888K | TWAP Oracle Manipulation | arbitrum |
| YYDS | 2022-09-08 | $742K | pair manipulate | bsc |
| SASHAToken | 2024-10-06 | $600K | Price Manipulation | ethereum |
| Allbridge | 2023-04-02 | $550K | FlashLoan price manipulation | bsc |
| WiseLending | 2024-01-12 | $464K | Bad HealthFactor Check | ethereum |
| vETH | 2024-11-14 | $447K | Vulnerable Price Dependency | ethereum |
| CompoundUni | 2024-02-23 | $440K | Oracle bad price | ethereum |
| SVT | 2023-08-26 | $400K | flawed price calculation | bsc |
| Themis | 2023-06-28 | $370K | Manipulation of prices using Flashloan | arbitrum |
| P719Token | 2024-10-11 | $312K | Price Manipulation Inflate Attack | bsc |
| ImpermaxV3 | 2025-04-26 | $300K | FlashLoan Price Oracle Manipulation | base |
| RES | 2022-10-06 | $291K | Token - pair manipulate | bsc |
| MorphoBlue | 2024-10-13 | $230K | Overpriced Asset in Oracle | None |
| ZongZi | 2024-03-25 | $223K | Price Manipulation | bsc |
| SellToken02 | 2023-05-13 | $197K | Price Manipulation | bsc |
| BelugaDex | 2023-10-13 | $175K | Price manipulation | arbitrum |
| ElephantStatus | 2023-12-06 | $165K | Price Manipulation | bsc |
| Circle | 2022-08-16 | $152K | Price Manipulation | ethereum |
| Carson | 2023-07-26 | $150K | Price manipulation | bsc |
| Z123 | 2024-04-22 | $135K | price manipulation | bsc |
| LavaLending | 2024-10-02 | $130K | Price Manipulation | arbitrum |
| ATK | 2022-10-12 | $127K | FlashLoan manipulate price | bsc |
| ERC20TokenBank | 2023-05-31 | $111K | Price Manipulation | ethereum |
| Nalakuvara_LotteryTicket50 | 2025-05-09 | $105K | Price Manipulation | base |
| DRLVaultV3 | 2025-11-10 | $100K | Price Manipulation | ethereum |
| ... | ... | ... | +72 more exploits | ... |

### Top PoC References

- **CreamFinance** (2021-10, $130.0M): `DeFiHackLabs/src/test/2021-10/Cream_2_exp.sol`
- **BonqDAO** (2023-02, $88.0M): `DeFiHackLabs/src/test/2023-02/BonqDAO_exp.sol`
- **GMX** (2025-07, $41.0M): `DeFiHackLabs/src/test/2025-07/gmx_exp.sol`
- **MonoX Finance** (2021-11, $31.0M): `DeFiHackLabs/src/test/2021-11/Mono_exp.sol`
- **CompounderFinance** (2023-06, $27.2M): `DeFiHackLabs/src/test/2023-06/CompounderFinance_exp.sol`
- **UwULend** (2024-06, $19.3M): `DeFiHackLabs/src/test/2024-06/UwuLend_First_exp.sol`
- **Indexed Finance** (2021-10, $16.0M): `DeFiHackLabs/src/test/2021-10/IndexedFinance_exp.sol`
- **DEUS DAO** (2022-04, $13.0M): `DeFiHackLabs/src/test/2022-04/deus_exp.sol`
- **ElephantMoney** (2022-04, $11.2M): `DeFiHackLabs/src/test/2022-04/Elephant_Money_exp.sol`
- **ResupplyFi** (2025-06, $9.6M): `DeFiHackLabs/src/test/2025-06/ResupplyFi_exp.sol`
