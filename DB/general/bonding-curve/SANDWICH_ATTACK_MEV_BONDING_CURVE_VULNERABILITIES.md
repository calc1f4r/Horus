---
# Core Classification
protocol: generic
chain: everychain
category: economic
vulnerability_type: sandwich_attack_mev

# Attack Vector Details
attack_type: economic_exploit
affected_component: swap_functions, bonding_curves, reward_distribution, liquidity_management

# Technical Primitives
primitives:
  - slippage_protection
  - amountOutMin
  - spot_price
  - oracle_price
  - mempool_monitoring
  - front_running
  - back_running
  - flash_loan
  - liquidity_manipulation

# Impact Classification
severity: high
impact: fund_loss
exploitability: 0.85
financial_impact: high

# Context Tags
tags:
  - sandwich_attack
  - mev
  - front_running
  - bonding_curve
  - slippage
  - price_manipulation
  - defi
  - dex
  - amm
  - uniswap

# Version Info
language: solidity
version: ">=0.6.0"

# Pattern Identity (Required)
root_cause_family: missing_frontrun_protection
pattern_key: missing_frontrun_protection | swap_functions, bonding_curves, reward_distribution, liquidity_management | sandwich_attack_mev

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - _setTicks
  - _swap
  - addLiquidity
  - amountOutMin
  - approve
  - atomic
  - back_running
  - balanceOf
  - block.timestamp
  - borrow
  - burn
  - buyPrincipalToken
  - buyUnderlying
  - deposit
  - flash_loan
  - front
  - front_running
  - function
  - getPrice
  - harvest
---

## References
- [Report-01]: reports/bonding_curve_findings/h-01-_swap-is-vulnerable-to-sandwich-attacks.md
- [Report-02]: reports/bonding_curve_findings/attacker-can-drain-protocol-tokens-by-sandwich-attacking-owner-call-to-setpositi.md
- [Report-03]: reports/bonding_curve_findings/exploiting-zero-amountoutmin-in-dexwrappers-for-mev-attacks.md
- [Report-04]: reports/bonding_curve_findings/m-02-mev-risk-in-periods-of-high-volatility.md
- [Report-05]: reports/bonding_curve_findings/m-14-uniswaphelperbuyflanandburn-is-a-subject-to-sandwich-attacks.md
- [Report-06]: reports/bonding_curve_findings/sandwich-attacks-and-price-manipulation.md
- [Report-07]: reports/bonding_curve_findings/use-of-spot-price-in-sponsorvault-leads-to-sandwich-attack.md
- [Report-08]: reports/bonding_curve_findings/m-12-sandwich-attacks-are-possible-as-there-is-no-slippage-control-option-in-mar.md
- [Report-09]: reports/bonding_curve_findings/idlecdoharvest-allows-price-manipulation-in-certain-circumstances.md
- [Report-10]: reports/bonding_curve_findings/c01-attacker-can-steal-a-portion-of-the-reward-tokens-and-accrued-yield.md
- [Report-11]: reports/bonding_curve_findings/reward-disbursement-can-be-front-run.md
- [Report-12]: reports/bonding_curve_findings/zbanc-dynamicliquidtokenconverter-frontrunner-can-grief-owner-when-calling-reduc.md
- [Report-13]: reports/bonding_curve_findings/oracle-front-running-could-deplete-reserves-over-time-addressed.md
- [Report-14]: reports/bonding_curve_findings/slippage-and-fees-can-be-manipulated-by-a-trader-addressed.md
- [Report-15]: reports/bonding_curve_findings/m-3-malicious-user-may-frontrun-gooddollarexpansioncontrollermintubifromreserveb.md

## Vulnerability Title

**Sandwich Attacks, MEV Exploitation, and Front-Running on Bonding Curves and Swap Functions**

### Overview

Bonding curves, on-chain swaps, and reward distribution mechanisms are systematically exploitable through sandwich attacks, MEV extraction, and front-running when they lack proper slippage protection, use dynamically-computed minimums on-chain, rely on spot prices from AMMs, or have predictable state-changing admin operations. These vulnerabilities allow attackers to manipulate prices before/after victim transactions and extract value from protocols and users.



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of missing_frontrun_protection"
- Pattern key: `missing_frontrun_protection | swap_functions, bonding_curves, reward_distribution, liquidity_management | sandwich_attack_mev`
- Interaction scope: `single_contract`
- Primary affected component(s): `swap_functions, bonding_curves, reward_distribution, liquidity_management`
- High-signal code keywords: `_setTicks`, `_swap`, `addLiquidity`, `amountOutMin`, `approve`, `atomic`, `back_running`, `balanceOf`
- Typical sink / impact: `fund_loss`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `SponsorVault.function -> sells.function -> strategy.function`
- Trust boundary crossed: `internal`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: Transaction can be frontrun by MEV bots observing the mempool
- Signal 2: No commit-reveal or private mempool protection for sensitive operations
- Signal 3: Slippage tolerance set too high or user-controllable without minimum enforcement
- Signal 4: Swap execution lacks deadline parameter or uses block.timestamp as deadline

#### False Positive Guards

- Not this bug when: Transaction uses private mempool (Flashbots) or commit-reveal scheme
- Safe if: Slippage protection with reasonable bounds is enforced
- Requires attacker control of: specific conditions per pattern

### Vulnerability Description

#### Root Cause

The fundamental issues across all 15 findings fall into these categories:

1. **On-chain dynamic slippage calculation** — Computing `minTokens` from current reserves inside the same transaction allows sandwiching since the reserves can be manipulated before execution (Reports 1, 3, 9)
2. **Zero or missing `amountOutMin`** — Setting minimum output to zero in swap calls removes all slippage protection (Reports 3, 5, 10)
3. **Spot price reliance** — Using AMM spot price (easily manipulable) instead of oracle/TWAP price for pricing decisions (Reports 7, 13, 14)
4. **Unprotected admin state changes** — Admin operations that redeploy liquidity or change weights can be sandwiched if they lack manipulation checks (Reports 2, 6, 12)
5. **Minimum buy amount vs minimum price** — Enforcing a minimum buy amount instead of minimum price allows manipulation when the sell amount increases (Report 9)
6. **Missing buy-sell cooldown** — No time delay between buy and sell allows atomic sandwich within same block (Report 4)
7. **Front-runnable reward distribution** — Reward accrual that can be entered/exited atomically around distribution events (Reports 11, 15)
8. **Predictable oracle updates** — Chainlink updates visible in mempool allow front-running the rebalancing (Report 13)

---

### Vulnerable Pattern Examples

---

#### **Pattern 1: On-Chain Dynamic Slippage Calculation** [HIGH]
**Protocol**: Gacha | **Auditor**: Pashov Audit Group | **Severity**: High

```solidity
// ❌ VULNERABLE: minTokens calculated dynamically on-chain from current reserves — sandwichable
function _swap(
    address token,
    uint256 cost
) private returns (uint256 actualTokens) {
    Storage storage $ = _getOwnStorage();
    IUniswapV2Router01 uni = IUniswapV2Router01($.uniswapRouter);
    IUniswapV2Factory factory = IUniswapV2Factory($.uniswapFactory);

    address pair = factory.getPair($.paymentToken, token);
    (uint256 wethReserve, uint256 tokenReserve, ) = IUniswapV2Pair(pair)
        .getReserves();
    if (wethReserve == 0 || tokenReserve == 0) revert InvalidPair();

    uint256 maxTokens = uni.getAmountOut(cost, wethReserve, tokenReserve); // includes 0.3%
    uint256 minTokens = Math.mulDiv(maxTokens, 95, 100); // 5% slippage

    address[] memory path = new address[](2);
    path[0] = $.paymentToken;
    path[1] = token;

    IERC20($.paymentToken).approve($.uniswapRouter, cost);
    uint256[] memory amounts = uni.swapExactTokensForTokens(
        cost,
        minTokens,
        path,
        address(this),
        block.timestamp + 1
    );
    actualTokens = amounts[amounts.length - 1];
}
```

**Root Cause**: Before swapping for meme tokens using `uni.swapExactTokensForTokens()`, a `minTokens` amount is calculated. This value serves as a slippage protection measure. However it is calculated dynamically, attackers can manipulate the price by front-running the meme token purchase, buying the token before the ticket purchase, and then selling it immediately after, profiting from the price movement.

**Attack Steps**:
1. Attacker monitors mempool for `purchase()` transactions
2. Attacker front-runs by buying the meme token, pushing its price up
3. Victim's `_swap()` executes — `getAmountOut` reads already-manipulated reserves, so `minTokens` is calculated from the inflated price
4. Attacker back-runs by selling the meme token at the inflated price
5. Attacker profits from the price differential; victim receives fewer tokens

**Recommended Fix**: `minTokens` should be calculated on the frontend and passed as an input parameter to `GachaTickets#purchase()`.

---

#### **Pattern 2: Sandwich Attack on Admin Liquidity Redeployment** [HIGH]
**Protocol**: Beefy Finance | **Auditor**: Cyfrin | **Severity**: High | **Finders**: Dacian, carlitox477

```solidity
// ❌ VULNERABLE: setPositionWidth and unpause redeploy liquidity based on current tick
// without onlyCalmPeriods modifier — sandwichable
// In StrategyPassiveManagerUniswap contract:

// These functions redeploy Beefy's liquidity into a new range based off the current
// tick and don't check the onlyCalmPeriods modifier
function setPositionWidth(int24 _width) external; // callable by owner
function unpause() external;                       // callable by owner
```

**Full Proof of Concept** (Foundry test — verbatim):
```solidity
function test_AttackerDrainsProtocolViaSetPositionWidth() public {
    // user deposits and beefy sets up its LP position
    uint256 BEEFY_INIT_WBTC = 10e8;
    uint256 BEEFY_INIT_USDC = 600000e6;
    deposit(user, true, BEEFY_INIT_WBTC, BEEFY_INIT_USDC);

    (uint256 beefyBeforeWBTCBal, uint256 beefyBeforeUSDCBal) = strategy.balances();

    // record beefy WBTC & USDC amounts before attack
    console.log("%s : %d", "LP WBTC Before Attack", beefyBeforeWBTCBal); // 999999998
    console.log("%s : %d", "LP USDC Before Attack", beefyBeforeUSDCBal); // 599999999999
    console.log();

    // attacker front-runs owner call to `setPositionWidth` using
    // a large amount of USDC to buy all the WBTC. This:
    // 1) results in Beefy LP having 0 WBTC and lots of USDC
    // 2) massively pushes up the price of WBTC
    //
    // Attacker has forced Beefy to sell WBTC "low"
    uint256 ATTACKER_USDC = 100000000e6;
    trade(attacker, true, false, ATTACKER_USDC);

    // owner calls `StrategyPassiveManagerUniswap::setPositionWidth`
    // This is the transaction that the attacker sandwiches. The reason is that
    // `setPositionWidth` makes Beefy change its LP position. This will
    // cause Beefy to deploy its USDC at the now much higher price range
    strategy.setPositionWidth(width);

    // attacker back-runs the sandwiched transaction to sell their WBTC
    // to Beefy who has deployed their USDC at the inflated price range,
    // and also sells the rest of their WBTC position to the remaining LPs
    // unwinding the front-run transaction
    //
    // Attacker has forced Beefy to buy WBTC "high"
    trade(attacker, false, true, IERC20(token0).balanceOf(attacker));

    // record beefy WBTC & USDC amounts after attack
    (uint256 beefyAfterWBTCBal, uint256 beefyAfterUSDCBal) = strategy.balances();

    // beefy has been almost completely drained of WBTC & USDC
    console.log("%s  : %d", "LP WBTC After Attack", beefyAfterWBTCBal); // 2
    console.log("%s  : %d", "LP USDC After Attack", beefyAfterUSDCBal); // 0
    console.log();

    uint256 attackerUsdcBal = IERC20(token1).balanceOf(attacker);
    console.log("%s  : %d", "Attacker USDC profit", attackerUsdcBal-ATTACKER_USDC);
    // attacker original USDC: 100000000 000000
    // attacker now      USDC: 101244330 209974
    // attacker profit = $1,244,330 USDC
}

function test_AttackerDrainsProtocolViaUnpause() public {
    // user deposits and beefy sets up its LP position
    uint256 BEEFY_INIT_WBTC = 0;
    uint256 BEEFY_INIT_USDC = 600000e6;
    deposit(user, true, BEEFY_INIT_WBTC, BEEFY_INIT_USDC);

    // owner pauses contract
    strategy.panic(0, 0);

    (uint256 beefyBeforeWBTCBal, uint256 beefyBeforeUSDCBal) = strategy.balances();

    // record beefy WBTC & USDC amounts before attack
    console.log("%s : %d", "LP WBTC Before Attack", beefyBeforeWBTCBal); // 0
    console.log("%s : %d", "LP USDC Before Attack", beefyBeforeUSDCBal); // 599999999999

    // attacker front-runs owner call to `unpause` using
    // a large amount of USDC to buy all the WBTC
    uint256 ATTACKER_USDC = 100000000e6;
    trade(attacker, true, false, ATTACKER_USDC);

    // owner calls `StrategyPassiveManagerUniswap::unpause`
    // This is the transaction that the attacker sandwiches
    strategy.unpause();

    // attacker back-runs the sandwiched transaction
    trade(attacker, false, true, IERC20(token0).balanceOf(attacker));

    (uint256 beefyAfterWBTCBal, uint256 beefyAfterUSDCBal) = strategy.balances();

    // beefy has been almost completely drained of USDC
    console.log("%s  : %d", "LP WBTC After Attack", beefyAfterWBTCBal); // 0
    console.log("%s  : %d", "LP USDC After Attack", beefyAfterUSDCBal); // 126790
    // attacker profit = $548,527 USDC
}
```

**Impact**: Attacker can drain protocol tokens — PoC showed **$1,244,330 profit** via `setPositionWidth` and **$548,527 profit** via `unpause`.

**Recommended Fix**:
```solidity
// ✅ SECURE: Add onlyCalmPeriods modifier to _setTicks function
// Option 1: Add modifier to setPositionWidth and unpause
// Option 2 (preferred): Add modifier to _setTicks and remove from other functions
// This prevents any intra-function pool manipulation
```

---

#### **Pattern 3: Zero `amountOutMin` in DexWrappers** [HIGH]
**Protocol**: Entangle Trillion | **Auditor**: Halborn | **Severity**: High

**Root Cause**: `swapExactTokensForTokens` and `removeLiquidity` functions called with `amountOutMin` set to zero — no slippage protection at all.

**Attack Steps**:
1. Attacker monitors the mempool for `swapExactTokensForTokens` calls made by `UniswapHandler` with `amountOutMin` set to zero
2. **Front-run**: Upon spotting a vulnerable swap transaction from DAI to MemeToken, the attacker buys MemeToken before the `UniswapHandler` transaction is processed
3. **Back-run**: The attacker prepares to sell MemeToken back into DAI after the `UniswapHandler` transaction
4. The attacker submits the front-run transaction with a higher gas fee to ensure it is executed before the `UniswapHandler` transaction
5. The `UniswapHandler` transaction executes, swapping DAI for MemeToken at an unfavorable rate due to the price manipulation
6. The attacker executes the back-run transaction, selling MemeToken for DAI at the inflated price

**Recommended Fixes**:
- Modify the `removeLiquidity` and `swapExactTokensForTokens` functions to require a non-zero `amountOutMin` parameter
- Utilize on-chain data to dynamically calculate an appropriate `amountOutMin` based on current market conditions

---

#### **Pattern 4: MEV on Bonding Curves Without Buy-Sell Cooldown** [MEDIUM]
**Protocol**: Sound.Xyz | **Auditor**: Zach Obront | **Severity**: Medium

**Root Cause**: Bonding curves allow atomic buy-then-sell in same block. Even with `msg.value` as max slippage on `buy()` and `minimumPayout` parameter on `sell()`, users must set buffer for volatility — MEV bots capture all consumer surplus.

**Attack Description**:
Any transaction along the curve can be sandwich attacked by a bot that creates the following Flashbots bundles:

`buy X tokens => ORIGINAL BUY TX => sell X tokens` (where X is the maximum number of tokens that can be bought without causing the original transaction to revert).

In periods of high volatility, users add sufficient buffer to slippage parameters. MEV bots capitalize on all of the consumer surplus between what a user is willing to pay and what the market requires they pay.

**Recommended Fix**:
```solidity
// ✅ SECURE: Implement a 1 block freeze between buying and selling
// In the samBurn() function, check that block.timestamp is greater than
// the timestamp of the last mint/transfer stored in the ERC721A packed storage slot
// This removes the risk-free profit that MEV bots can earn
```

---

#### **Pattern 5: No Slippage Control on Swap Results** [MEDIUM]
**Protocol**: Behodler | **Auditor**: Code4rena | **Severity**: Medium | **Finder**: hyh

```solidity
// ❌ VULNERABLE: buyFlanAndBurn doesn't control for swap results
// executing swaps with exchange pool provided amounts which can be manipulated
// https://github.com/code-423n4/2022-01-behodler/blob/main/contracts/UniswapHelper.sol#L231
```

**Root Cause**: `buyFlanAndBurn` doesn't control for swap results, executing swaps with exchange pool provided amounts, which can be manipulated. A malicious bot buys Flan pushing price from 0.8 to 0.9 before UniswapHelper's order, then sells right after.

**Attack Steps**:
1. Flan trades at 0.8 in input token terms
2. Flan buy order seen by malicious bot
3. Bot buys Flan pushing price to 0.9 before UniswapHelper's order
4. UniswapHelper order executes at 0.9 (overspending input token)
5. Bot sells Flan back after
6. Input token holdings of the system are overspent

**Recommended Fix**: Add minimum accepted price as a function argument so user can limit effective slippage. Also add a relative version of the parameter to control percentage based slippage with TWAP Oracle price as a benchmark.

---

#### **Pattern 6: Sandwich Attack on Bond Deposits with Swap** [MEDIUM]
**Protocol**: Vector Reserve | **Auditor**: Quantstamp | **Severity**: Medium | **Finders**: Julio Aguilar, Mostafa Yassin, Guillermo Escobero

**Root Cause**: The swap performed in `swapETHForTokens()` and `addLiquidity()` for LP bonds (`WETHTOLP` type) currently accept any amount of tokens in return, making them vulnerable to sandwich attacks.

**Attack Steps** (verbatim):
1. An attacker takes a flash loan for a lot of WETH
2. The attacker swaps that WETH for VEC, inflating the price of VEC
3. The attacker deposits WETH on any of the bond contracts of type `WETHTOLP`. This transaction will:
   1. Buy more VEC with half of the deposited WETH, further increasing the price of VEC
   2. Use that VEC plus the other WETH half to add liquidity to the pool. This is done in proportion to the reserves of the pool
4. Finally, the attacker swaps the VEC from step 2 for WETH. Since the price was inflated, the amount of WETH back could be greater than the initial swap generating a profit
5. The final attacker balance will decrease less than expected: e.g. he buys a 25 WETH bond with a net payment of 18 WETH

**Recommended Fix**: Add slippage protection to that bond type. Alternatively, allow users to deposit the LP tokens directly, without providing swapping and providing liquidity from the bond contract.

---

#### **Pattern 7: Spot AMM Price in SponsorVault** [CRITICAL]
**Protocol**: Connext | **Auditor**: Spearbit | **Severity**: Critical Risk | **Finders**: 0xLeastwood, Jonah1005

```solidity
// ❌ VULNERABLE: Spot AMM price used — attacker can manipulate getInGivenExpectedOut
contract SponsorVault is ISponsorVault, ReentrancyGuard, Ownable {
    ...
    function reimburseLiquidityFees(
        address _token,
        uint256 _liquidityFee,
        address _receiver
    ) external override onlyConnext returns (uint256) {
        ...
        uint256 amountIn = tokenExchange.getInGivenExpectedOut(_token, _liquidityFee);
        amountIn = currentBalance >= amountIn ? amountIn : currentBalance;
        // sponsored fee may end being less than _liquidityFee due to slippage
        sponsoredFee = tokenExchange.swapExactIn{value: amountIn}(_token, msg.sender);
        ...
    }
}
```

**Root Cause**: The spot AMM price is used when doing the swap. Attackers can manipulate the value of `getInGivenExpectedOut` and make `SponsorVault` sell the native token at a bad price. By executing a sandwich attack, the exploiters can drain all native tokens in the sponsor vault.

**Attack Steps** (assume `_token` is USDC and the native token is ETH, sponsor tries to sponsor 100 USDC):
1. Attacker first manipulates the DEX and makes the exchange of 1 ETH = 0.1 USDC
2. `getInGivenExpectedOut` returns 100/0.1 = 1000
3. `tokenExchange.swapExactIn` buys 100 USDC with 1000 ETH, causing the ETH price to decrease even lower
4. Attacker buys ETH at a lower price and realizes a profit

**Impact**: Attacker can drain all native tokens in the SponsorVault.

**Recommended Fix**: Instead of relying on DEX's spot price, the sponsor vault should rely instead on price quotes which are harder to manipulate, like those provided by an oracle (e.g., Chainlink price, Uniswap TWAP). The `SponsorVault` should fetch the oracle price and compare it against the spot price. The `SponsorVault` should either revert or use the oracle price when the spot price deviates from the oracle price.

---

#### **Pattern 8: No Slippage Control in Marketplace Swap Functions** [MEDIUM]
**Protocol**: Illuminate | **Auditor**: Code4rena | **Severity**: Medium | **Finder**: hyh (also datapunk, Alex the Entreprenerd, unforgiven)

```solidity
// ❌ VULNERABLE: All four swapping functions of Marketplace do not allow for slippage control
/// @notice sells the PT for the PT via the pool
function sellPrincipalToken(
    address u,
    uint256 m,
    uint128 a
) external returns (uint128) {
    IPool pool = IPool(pools[u][m]);
    Safe.transfer(IERC20(address(pool.fyToken())), address(pool), a);
    return pool.sellFYToken(msg.sender, pool.sellFYTokenPreview(a));
}

/// @notice buys the underlying for the PT via the pool
function buyPrincipalToken(
    address u,
    uint256 m,
    uint128 a
) external returns (uint128) {
    IPool pool = IPool(pools[u][m]);
    Safe.transfer(IERC20(address(pool.base())), address(pool), a);
    return pool.buyFYToken(msg.sender, pool.buyFYTokenPreview(a), a);
}

/// @notice sells the underlying for the PT via the pool
function sellUnderlying(
    address u,
    uint256 m,
    uint128 a
) external returns (uint128) {
    IPool pool = IPool(pools[u][m]);
    Safe.transfer(IERC20(address(pool.base())), address(pool), a);
    return pool.sellBase(msg.sender, pool.sellBasePreview(a));
}

/// @notice buys the underlying for the PT via the pool
function buyUnderlying(
    address u,
    uint256 m,
    uint128 a
) external returns (uint128) {
    IPool pool = IPool(pools[u][m]);
    Safe.transfer(IERC20(address(pool.fyToken())), address(pool), a);
    return pool.buyBase(msg.sender, pool.buyBasePreview(a), a);
}
```

```solidity
// ❌ VULNERABLE: Lender's yield() swapping without ability to control slippage
/// @notice transfers excess funds to yield pool after principal tokens have been lent out
/// @dev this method is only used by the yield, illuminate and swivel protocols
function yield(
    address u,
    address y,
    uint256 a,
    address r
) internal returns (uint256) {
    // preview exact swap slippage on yield
    uint128 returned = IYield(y).sellBasePreview(Cast.u128(a));

    // send the remaing amount to the given yield pool
    Safe.transfer(IERC20(u), y, a);

    // lend out the remaining tokens in the yield pool
    IYield(y).sellBase(r, returned);

    return returned;
}
```

**Root Cause**: All swap functions use preview amounts (`sellFYTokenPreview`, `buyFYTokenPreview`, `sellBasePreview`, `buyBasePreview`) as the minimum output. These preview values read current pool state which can be manipulated. No user-provided slippage parameter exists.

**Recommended Fix**: Add minimum accepted return argument to the five mentioned functions and condition execution success on it so the caller can control for the realized slippage.

---

#### **Pattern 9: Minimum Buy Amount Instead of Minimum Price** [MEDIUM]
**Protocol**: Idle Finance | **Auditor**: ConsenSys | **Severity**: Medium | **Finders**: Nicholas Ward, Shayan Eskandari

```solidity
// ❌ VULNERABLE: harvest() enforces minimum buy amount, not minimum price
// If balance of rewards increases between submission and execution,
// sandwich attack can be profitable while satisfying minimum buy amounts
function harvest(bool _skipRedeem, bool _skipIncentivesUpdate, bool[] calldata _skipReward, uint256[] calldata _minAmount) external {
  require(msg.sender == rebalancer || msg.sender == owner(), "IDLE:!AUTH");
```

```solidity
// ❌ VULNERABLE: sells entire balance with only minimum buy amount protection
// approve the uniswap router to spend our reward
IERC20Detailed(rewardToken).safeIncreaseAllowance(address(_uniRouter), _currentBalance);
// do the uniswap trade
_uniRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens(
  _currentBalance,
  _minAmount[i],
  _path,
  address(this),
  block.timestamp + 1
);
```

**Root Cause**: Because the contract sells its entire balance of redeemed rewards for the specified minimum buy amount, this approach does not enforce a minimum *price* for the executed trades. If the balance of `IdleCDO` or the amount of claimable rewards increases between the submission of the `harvest()` transaction and its execution, it may be possible to perform a profitable sandwiching attack while still satisfying the required minimum buy amounts.

**Attack Vector**: The viability depends on how effectively an attacker can increase the amount of rewards tokens to be sold without incurring an offsetting loss. Could be done either through direct interaction with the protocol or as part of a flashbots bundle containing a large position adjustment from an honest user.

**Recommended Fix**: Update `IdleCDO.harvest()` to enforce a minimum price rather than a minimum buy amount. One method: take an additional array parameter indicating the amount of each token to sell in exchange for the respective buy amount.

---

#### **Pattern 10: Zero Slippage on Reward Token Liquidation** [CRITICAL]
**Protocol**: Origin Dollar | **Auditor**: OpenZeppelin | **Severity**: Critical (C01)

**Root Cause**: The protocol uses `swapExactTokensForTokens` on Uniswap's `UniswapV2Router02` and sets the minimum number of tokens to receive to **zero**. No slippage protection on reward harvesting and buyback operations.

**Attack Steps** (verbatim):
1. Flash-borrow a huge amount of COMP and sell it in the COMP/WETH Uniswap pool to significantly lower the COMP price
2. Call the `mint` or `mintMultiple` functions to trigger an allocation and swap the harvested COMP tokens. Due to the price movement in step 1, the contract will receive less than the market value. This also lowers the COMP price further.
3. Sell the WETH back in the Uniswap pool to recover the COMP, which will be even cheaper due to step 2.
4. Repay the loan. Since the attacker buys COMP at a cheaper rate than it was initially sold, they profit the difference.

Similarly, the attacker can perform a flash-loan to borrow OUSD and manipulate the OUSD/OGN price in Uniswap, to extract some of the value of the OUSD swapped by the `Buyback` contract. This same attack can be performed without using a flash-loan, by sandwiching a call to the `allocate` function (callable by anyone) or `harvest` function (callable by governor/strategist).

**Impact**: Profit depends on amount of money deposited in the strategies. Feasibility increases as the platform's investments grow.

**Recommended Fix**: Add slippage protection to all calls to the `swapExactTokensForTokens` function from the `UniswapV2Router02` contract.

---

#### **Pattern 11: Front-Runnable Reward Disbursement** [MEDIUM]
**Protocol**: Vaporware | **Auditor**: Quantstamp | **Severity**: Medium | **Finders**: Nikita Belenkov, Zeeshan Meghji, Danny Aksenov

**Root Cause**: Rewards may be added to the `Rewards` contract via: (1) minting liquid accessories through `LiquidAccessories.mintAccessories()`, (2) adding rewards directly through `Rewards.addRewardsForAccessory()`. No protection against front-running these reward additions.

**Attack Steps**:
1. Attacker monitors mempool for calls that add rewards
2. Attacker front-runs by equipping the item immediately before the reward is added (may also acquire the accessory as part of the front-running)
3. Reward is distributed — attacker receives disproportionate share
4. Attacker unequips immediately after

**Recommended Fixes**:
1. When adding rewards, consider using a private mempool such as with Flashbots
2. Ensure that the rewards being added do not provide sufficient incentive for front-running (e.g., adding fewer rewards on each call makes the front-running more expensive)

---

#### **Pattern 12: Griefing Admin Weight Reduction via Sandwich** [MEDIUM]
**Protocol**: Zer0 - zBanc | **Auditor**: ConsenSys | **Severity**: Medium | **Finders**: David Oz Kashi, Martin Ortner

```solidity
// ❌ VULNERABLE: reduceWeight success depends on manipulable marketcap
// reserveBalance can be manipulated by buying/selling liquidity tokens
function reduceWeight(IERC20Token _reserveToken)
    public
    validReserve(_reserveToken)
    ownerOnly
{
    _protected();
    uint256 currentMarketCap = getMarketCap(_reserveToken);
    require(currentMarketCap > (lastWeightAdjustmentMarketCap.add(marketCapThreshold)), "ERR_MARKET_CAP_BELOW_THRESHOLD");
```

**Root Cause**: The `reserveBalance` can be manipulated by buying (adding reserve token) or selling liquidity tokens (removing reserve token). The success of a call to `reduceWeight` is highly dependent on the marketcap.

**Attack Vectors**:
- **(a) Raise barrier**: Attacker sandwiches with buy calls to artificially inflate marketcap, causing `lastWeightAdjustmentMarketCap` to be stored higher, raising the threshold for the next call
- **(b) Block call**: Major token holder temporarily lowers marketcap by selling liquidity tokens to fail the `reduceWeights` call
- **(c) Owner exploit**: Owner as major holder can lower marketcap to the absolute minimum (old+threshold) by selling liquidity, then buying back right after reducing weights

---

#### **Pattern 13: Oracle Front-Running Depletes Reserves** [HIGH]
**Protocol**: Bancor V2 AMM | **Auditor**: ConsenSys | **Severity**: High

**Root Cause**: Bancor's weight rebalancing mechanism uses Chainlink price oracles to dynamically update weights. Oracle price updates are visible in the mempool before they are included in a block, making it possible to front-run the rebalancing.

**Full Example** (verbatim):
```
Initial state (amplification factor = 20, zero fees):
converter TKN balance = 100,000,000
converter TKN weight = 500,000
converter BNT balance = 100,000,000
converter BNT weight = 500,000
frontrunner TKN balance = 100,000,000
frontrunner BNT balance = 0
Oracle A rate = 10,000
Oracle B rate = 10,000

Step 1: Frontrunner sees Oracle B rate changing to 10,500 in mempool.
        Sends higher gas tx: Convert 1,000,000 TKN into 999,500 BNT.

Intermediate state:
converter TKN balance = 101,000,000
converter BNT balance = 99,000,500
frontrunner TKN balance = 99,000,000
frontrunner BNT balance = 999,500

Step 2: In following block, frontrunner converts 999,500 BNT back into TKN.

State:
converter TKN balance = 99,995,006
converter TKN weight = 498,754
converter BNT balance = 100,000,000
converter BNT weight = 501,246
frontrunner TKN balance = 100,004,994
frontrunner BNT balance = 0

Step 3: Frontrunner leverages incentive to rebalance: Convert 4,994 TKN to BNT.

Final state:
converter TKN balance = 100,000,000
converter TKN weight = 498,754
converter BNT balance = 99,995,031
converter BNT weight = 501,246
frontrunner TKN balance = 100,000,000
frontrunner BNT balance = 4,969

Result: Pool balanced, frontrunner gained 4,969 BNT.
```

**Impact**: Over time, this could deplete the secondary reserve as the formula compensates by rebalancing the weights such that the secondary token is sold slightly below its market rate.

**Mitigation Applied**: Bancor added a mechanism that adjusts the effective weights once per block based on its internal price feed. The conversion rate re-anchors to the external oracle price once the next oracle update comes in.

---

#### **Pattern 14: Slippage Reduction via Temporary Liquidity Addition** [HIGH]
**Protocol**: Bancor V2 AMM | **Auditor**: ConsenSys | **Severity**: High

**Root Cause**: Users can reduce slippage by adding liquidity before trading and removing it after. The trader also receives a part of the fees for the trade.

**Attack Steps** (verbatim):
1. Instead of just making a trade, a user can add a lot of liquidity (of both tokens, or only one of them) to the pool after taking a flash loan
2. Make the trade
3. Remove the added liquidity

**Example** (verbatim):
```
Initial state (amplification factor = 20, zero fees):
converter TKN balance = 10000000
converter TKN weight = 500000
converter BNT balance = 10000000
converter BNT weight = 500000

Normal trade:
-> Convert 9000000 TKN into 8612440 BNT.

With 100% liquidity added in both tokens before trade:
-> Convert 9000000 TKN into 8801955 BNT.
```

**Impact**: Extra 189,515 BNT gained (2.2% improvement). Technique can amplify any frontrunning/arbitrage opportunity and help deplete reserves.

**Mitigation Applied**: Exit fee mechanism — returns fewer tokens if primary reserve is not in balanced state. In some cases traders may still have incentive to add/remove liquidity around trades.

---

#### **Pattern 15: Front-Running Bonding Curve Expansion with Zero Token Supply** [MEDIUM]
**Protocol**: Mento x Good$ Integration | **Auditor**: Sherlock | **Severity**: Medium | **Finder**: 0x73696d616f

```solidity
// ❌ VULNERABLE: mintUBIFromInterest does not check if amountToMint is null
function mintUBIFromInterest(bytes32 exchangeId, uint256 reserveInterest) external {
  require(reserveInterest > 0, "Reserve interest must be greater than 0");
  IBancorExchangeProvider.PoolExchange memory exchange = IBancorExchangeProvider(address(goodDollarExchangeProvider))
    .getPoolExchange(exchangeId);

  uint256 amountToMint = goodDollarExchangeProvider.mintFromInterest(exchangeId, reserveInterest);

  require(IERC20(exchange.reserveAsset).transferFrom(msg.sender, reserve, reserveInterest), "Transfer failed");
  IGoodDollar(exchange.tokenAddress).mint(address(distributionHelper), amountToMint);

  emit InterestUBIMinted(exchangeId, amountToMint);
}

function mintUBIFromReserveBalance(bytes32 exchangeId) external returns (uint256 amountMinted) {
  IBancorExchangeProvider.PoolExchange memory exchange = IBancorExchangeProvider(address(goodDollarExchangeProvider))
    .getPoolExchange(exchangeId);

  uint256 contractReserveBalance = IERC20(exchange.reserveAsset).balanceOf(reserve);
  uint256 additionalReserveBalance = contractReserveBalance - exchange.reserveBalance;
  if (additionalReserveBalance > 0) {
    amountMinted = goodDollarExchangeProvider.mintFromInterest(exchangeId, additionalReserveBalance);
    IGoodDollar(exchange.tokenAddress).mint(address(distributionHelper), amountMinted);

    emit InterestUBIMinted(exchangeId, amountMinted);
  }
}
```

```solidity
// ❌ VULNERABLE: mintFromInterest returns 0 when exchange.tokenSupply is 0
function mintFromInterest(
  bytes32 exchangeId,
  uint256 reserveInterest
) external onlyExpansionController whenNotPaused returns (uint256 amountToMint) {
  PoolExchange memory exchange = getPoolExchange(exchangeId);

  uint256 reserveinterestScaled = reserveInterest * tokenPrecisionMultipliers[exchange.reserveAsset];
  uint256 amountToMintScaled = unwrap(
    wrap(reserveinterestScaled).mul(wrap(exchange.tokenSupply)).div(wrap(exchange.reserveBalance))
  );
  amountToMint = amountToMintScaled / tokenPrecisionMultipliers[exchange.tokenAddress];

  exchanges[exchangeId].tokenSupply += amountToMintScaled;
  exchanges[exchangeId].reserveBalance += reserveinterestScaled;

  return amountToMint;
}
```

**Root Cause**: `amountMinted` is not checked for a null value. `mintFromInterest()` returns 0 if `exchange.tokenSupply` is 0 due to `wrap(exchange.tokenSupply)` being zero in the multiplication.

**Attack Steps**:
1. Attacker calls `Bancor::swapIn()` or `Bancor::swapOut()`, buying all $G in the exchange, making `PoolExchange.tokenSupply` null
2. `GoodDollarExpansionController::mintUBIFromReserveBalance()` or `mintUBIFromInterest()` is called, adding reserve asset funds without minting $G

**Impact**: Funds are added to the reserve without the corresponding amount of $G being minted — permanent loss.

**Recommended Fix**: Revert if the `amountToMint` from the `GoodDollarExchangeProvider::mintFromInterest()` call is null. Same for `mintUBIFromExpansion()`.

---

### Impact Analysis

#### Technical Impact
- Complete draining of protocol liquidity through sandwich attacks on admin operations (Pattern 2: $1.2M+ in PoC)
- Gradual reserve depletion via oracle front-running (Pattern 13)
- Reward token theft through front-running distribution events (Patterns 10, 11)
- Slippage manipulation allowing trades at unfavorable prices (all patterns)
- Permanent fund lock when supply driven to zero (Pattern 15)

#### Business Impact
- Direct financial loss to protocol treasuries and users
- Loss of user trust when sandwich attacks consistently extract value
- Protocol insolvency through gradual reserve depletion
- MEV extraction creating negative-sum environment for honest users

#### Affected Scenarios
- Any on-chain swap with dynamically computed slippage
- Admin operations that redeploy liquidity or change pool weights
- Reward harvesting that liquidates tokens via DEX
- Bonding curve operations without buy-sell cooldowns
- Oracle-driven weight rebalancing with mempool-visible updates

### Secure Implementation

**Fix 1: User-Provided Slippage from Frontend**
```solidity
// ✅ SECURE: minTokens passed from frontend, computed off-chain from real oracle price
function purchase(
    uint256 poolId,
    uint256 amount,
    uint256 minTokensOut  // caller-provided slippage protection
) external {
    // ... swap logic ...
    uint256[] memory amounts = router.swapExactTokensForTokens(
        amount,
        minTokensOut,  // not dynamically computed on-chain
        path,
        address(this),
        block.timestamp
    );
}
```

**Fix 2: Oracle Price + Deviation Check**
```solidity
// ✅ SECURE: Use oracle price with max deviation tolerance
function swapWithOracleProtection(
    address tokenIn,
    address tokenOut,
    uint256 amountIn
) external {
    uint256 oraclePrice = chainlinkOracle.getPrice(tokenIn, tokenOut);
    uint256 spotPrice = dex.getSpotPrice(tokenIn, tokenOut);

    uint256 deviation = spotPrice > oraclePrice
        ? ((spotPrice - oraclePrice) * 1e18) / oraclePrice
        : ((oraclePrice - spotPrice) * 1e18) / oraclePrice;

    require(deviation <= MAX_DEVIATION, "Price deviation too high");

    uint256 minOut = (amountIn * oraclePrice * (10000 - SLIPPAGE_BPS)) / (10000 * 1e18);
    router.swapExactTokensForTokens(amountIn, minOut, path, address(this), block.timestamp);
}
```

**Fix 3: Calm Period / TWAP Check for Admin Operations**
```solidity
// ✅ SECURE: Verify pool is not manipulated before redeploying liquidity
modifier onlyCalmPeriods() {
    // Compare spot price against TWAP
    (uint160 sqrtPriceX96, , , , , , ) = pool.slot0();
    uint256 spotPrice = _priceFromSqrtX96(sqrtPriceX96);
    uint256 twapPrice = _getTWAP(TWAP_PERIOD);

    uint256 deviation = spotPrice > twapPrice
        ? ((spotPrice - twapPrice) * 1e18) / twapPrice
        : ((twapPrice - spotPrice) * 1e18) / twapPrice;

    require(deviation <= MAX_ALLOWED_DEVIATION, "Pool not calm");
    _;
}

function _setTicks() internal onlyCalmPeriods {
    // ... redeploy liquidity ...
}
```

**Fix 4: Buy-Sell Cooldown**
```solidity
// ✅ SECURE: 1 block freeze between buying and selling
function sell(uint256 tokenId, uint256 minimumPayout) external {
    // ERC721A packed storage already stores last mint/transfer timestamp
    uint256 lastAction = _ownershipOf(tokenId).startTimestamp;
    require(block.timestamp > lastAction, "Must wait 1 block");

    // ... sell logic ...
}
```

**Fix 5: Minimum Price Instead of Minimum Amount**
```solidity
// ✅ SECURE: Enforce minimum price, not just minimum amount
function harvest(
    uint256[] calldata _minAmount,
    uint256[] calldata _maxSellAmount  // new: limits amount sold per token
) external {
    for (uint i = 0; i < rewardTokens.length; i++) {
        uint256 balance = IERC20(rewardTokens[i]).balanceOf(address(this));
        uint256 sellAmount = balance > _maxSellAmount[i] ? _maxSellAmount[i] : balance;

        router.swapExactTokensForTokens(
            sellAmount,
            _minAmount[i],
            path,
            address(this),
            block.timestamp
        );
    }
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern: getAmountOut() or getAmountsOut() result used as minAmountOut in same transaction
- Pattern: amountOutMin set to 0 in any swap call
- Pattern: sellBasePreview() / sellFYTokenPreview() used as min output
- Pattern: Admin functions that redeploy liquidity without TWAP/calm check
- Pattern: harvest/liquidation functions using swapExactTokensForTokens with _currentBalance
- Pattern: Bonding curve buy+sell possible in same block without cooldown
- Pattern: Reward distribution callable without commit-reveal or time lock
- Pattern: Oracle-driven rebalancing without front-run protection
- Pattern: reserveBalance used in threshold check that is manipulable via trades
```

#### Audit Checklist
- [ ] Does any swap function compute minAmountOut dynamically on-chain from current pool state?
- [ ] Is amountOutMin ever set to 0 in swap calls?
- [ ] Do admin/privileged operations trigger liquidity redeployment without manipulation checks?
- [ ] Can bonding curve tokens be bought and sold in the same block?
- [ ] Does reward harvesting enforce minimum price or just minimum amount?
- [ ] Are oracle-driven rebalancing operations vulnerable to mempool front-running?
- [ ] Can reward distribution events be front-run by entering/exiting just before/after?
- [ ] Do swap functions accept user-provided slippage parameters?
- [ ] Are flash loans usable to amplify any of these attacks?
- [ ] Is there a TWAP or calm-period check before liquidity operations?

### Real-World Examples

#### Known Exploits / Audit Findings
- **Gacha (2025)** — [H-01] `_swap()` vulnerable to sandwich — Pashov Audit Group
- **Beefy Finance (2024)** — Drain protocol via sandwich on `setPositionWidth`/`unpause` — Cyfrin — ~$1.2M+ in PoC
- **Entangle Trillion** — Zero amountOutMin in DexWrappers — Halborn
- **Sound.Xyz (2023)** — [M-02] MEV on bonding curve — Zach Obront
- **Behodler (2022)** — [M-14] buyFlanAndBurn sandwich — Code4rena — hyh
- **Vector Reserve** — Sandwich on bond deposits — Quantstamp
- **Connext** — Spot price in SponsorVault — Critical — Spearbit
- **Illuminate (2022)** — [M-12] No slippage in Marketplace — Code4rena — hyh
- **Idle Finance (2021)** — harvest() price manipulation — ConsenSys
- **Origin Dollar** — [C01] Steal rewards via zero slippage — OpenZeppelin — Critical
- **Vaporware** — Front-runnable reward disbursement — Quantstamp
- **Zer0 zBanc (2021)** — Griefing reduceWeight via sandwich — ConsenSys
- **Bancor V2 (2020)** — Oracle front-running depletes reserves — ConsenSys — High
- **Bancor V2 (2020)** — Slippage manipulation via liquidity — ConsenSys — High
- **Mento GoodDollar (2024)** — [M-3] Front-run mintUBI with zero supply — Sherlock

### Prevention Guidelines

#### Development Best Practices
1. **Never compute slippage protection on-chain from current pool state** — always accept user-provided minimums
2. **Never set amountOutMin to 0** — always enforce meaningful slippage bounds
3. **Use oracle prices (Chainlink/TWAP) as sanity checks** against spot prices for all DEX interactions
4. **Add calm-period/TWAP checks** to any admin function that redeploys liquidity or changes pool parameters
5. **Enforce minimum price, not just minimum buy amount** in harvest/liquidation functions
6. **Add buy-sell cooldowns** (at least 1 block) on bonding curves to prevent atomic sandwiches
7. **Use commit-reveal or time-locks** for reward distributions to prevent front-running
8. **Consider private mempools** (e.g., Flashbots Protect) for sensitive admin transactions
9. **Accept LP tokens directly** instead of swapping inside bond/deposit contracts
10. **Limit sell amounts** in harvest functions rather than selling entire balance

#### Testing Requirements
- Unit tests for: sandwich attack simulation (front-run → target tx → back-run)
- Integration tests for: flash loan amplified sandwich attacks
- Fuzzing targets: slippage parameters, swap amounts near pool boundaries, admin operation timing
- Invariant tests: protocol token balance should not decrease through external sandwich attacks

### Keywords for Search

`sandwich attack`, `MEV`, `front-running`, `back-running`, `slippage`, `amountOutMin`, `minTokens`, `getAmountOut`, `swapExactTokensForTokens`, `bonding curve`, `price manipulation`, `flash loan`, `oracle front-running`, `TWAP`, `calm period`, `reward distribution`, `harvest`, `liquidation`, `spot price`, `pool manipulation`, `Flashbots`, `mempool`, `buy-sell cooldown`, `weight rebalancing`, `liquidity redeployment`, `zero slippage`, `consumer surplus`, `sellBasePreview`, `getInGivenExpectedOut`, `reduceWeight`, `onlyCalmPeriods`, `setPositionWidth`, `unpause`

### Related Vulnerabilities

- Oracle manipulation / stale price vulnerabilities
- Flash loan attack vectors 
- Reentrancy on token swaps
- ERC4626 vault inflation attacks (similar front-running vector)
- Governance proposal front-running
- Liquidity pool share manipulation

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

`_setTicks`, `_swap`, `addLiquidity`, `amm`, `amountOutMin`, `approve`, `atomic`, `back_running`, `balanceOf`, `block.timestamp`, `bonding_curve`, `borrow`, `burn`, `buyPrincipalToken`, `buyUnderlying`, `defi`, `deposit`, `dex`, `economic`, `flash_loan`, `front`, `front_running`, `function`, `getPrice`, `harvest`, `liquidity_manipulation`, `mempool_monitoring`, `mev`, `oracle_price`, `price_manipulation`, `sandwich_attack`, `sandwich_attack_mev`, `slippage`, `slippage_protection`, `spot_price`, `uniswap`
