---
# Core Classification (Required)
protocol: generic
chain: everychain
category: bonding_curve
vulnerability_type: token_launch_graduation

# Attack Vector Details (Required)
attack_type: economic_exploit|logical_error|griefing
affected_component: token_launch|graduation|pool_creation|pair_initialization|migration

# Technical Primitives (Required)
primitives:
  - bonding_curve
  - token_launch
  - graduation
  - uniswap_v2_pair
  - uniswap_v3_pool
  - createPool
  - createPair
  - addLiquidity
  - CREATE2
  - flash_loan
  - presale
  - fair_launch
  - dutch_auction
  - migration

# Impact Classification (Required)
severity: critical
impact: fund_loss|manipulation|dos|unfair_launch
exploitability: 0.80
financial_impact: high

# Context Tags
tags:
  - defi
  - bonding_curve
  - token_launch
  - fair_launch
  - graduation
  - pool_creation
  - meme_coin
  - launchpad

# Version Info
language: solidity|rust
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Premature Launch / Graduation Exploits
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Groupcoin - Tokens Launched Anytime | `reports/bonding_curve_findings/c-02-tokens-can-be-launched-to-uniswap-v3-anytime-allowing-to-drain-eth.md` | HIGH | Pashov Audit Group |
| Fei Protocol - Flash Loan Genesis Exploit | `reports/bonding_curve_findings/c05-anyone-with-enough-liquidity-to-reach-the-maxgenesisprice-can-make-profit-fr.md` | HIGH | OpenZeppelin |
| Virtuals - Flash Loan Premature Graduation | `reports/bonding_curve_findings/m-04-launched-tokens-are-vulnerable-to-flashloan-attacks-forcing-premature-gradu.md` | MEDIUM | Code4rena |
| Fei Protocol Phase 2 - New BondingCurve Volatility | `reports/bonding_curve_findings/h02-introduction-of-additional-bondingcurves-creates-period-of-volatility.md` | HIGH | OpenZeppelin |

### Pool/Pair Creation Griefing
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Groupcoin - Griefing UniswapV3 Launch | `reports/bonding_curve_findings/m-06-griefing-the-launch-to-uniswapv3-by-creating-the-pool-first.md` | MEDIUM | Pashov Audit Group |
| GTE - CREATE2 Address Mismatch | `reports/bonding_curve_findings/h-08-create2-address-of-the-uniswap-pair-used-by-launchpad-does-not-match-addres.md` | HIGH | Code4rena |
| MoonBound - Early Pair Creation Breaks Fair Launch | `reports/bonding_curve_findings/mnbd1-5-early-pair-creation-breaks-fair-launch-of-new-moon-tokens-and-gives-an-a.md` | HIGH | Hexens |
| GTE - Bypass Recipient Check Pre-seeding | `reports/bonding_curve_findings/m-21-bypass-of-recipient-check-allows-pre-seeding-the-real-pair-and-manipulating.md` | MEDIUM | Code4rena |

### Bootstrap / Migration Issues
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Goat Trading - Front-Running createPair | `reports/bonding_curve_findings/m-1-some-unusual-problems-arise-in-the-use-of-the-goatv1factorysolcreatepair-fun.md` | MEDIUM | Sherlock |
| Virtuals - Double-Stake Migration | `reports/bonding_curve_findings/m-22-founder-has-to-double-stake-during-migration-with-the-initial-lp-locked-in-.md` | MEDIUM | Code4rena |
| AragonOne - Presale Token Vesting | `reports/bonding_curve_findings/balanceredirectpresale-tokens-vest-during-the-presale-phase-wont-fix.md` | MEDIUM | ConsenSys |
| Malt Finance - Dutch Auction Manipulation | `reports/bonding_curve_findings/m-26-dutch-auction-can-be-manipulated.md` | MEDIUM | Code4rena |
| PartyDAO - NFT Crowdfund Rug Pull | `reports/bonding_curve_findings/m-01-attacker-can-list-an-nft-they-own-and-inflate-to-zero-all-users-contributio.md` | MEDIUM | Code4rena |

---

# Bonding Curve Token Launch & Graduation Vulnerabilities

**Comprehensive Patterns for Token Launch, Graduation, Pool Creation, and Fair Launch Exploits**

---

## Table of Contents

1. [Premature Launch via Default Value Bypass](#1-premature-launch-via-default-value-bypass)
2. [Flash Loan Genesis / Graduation Exploit](#2-flash-loan-genesis--graduation-exploit)
3. [Flash Loan Premature Graduation with Atomic Unwrap](#3-flash-loan-premature-graduation-with-atomic-unwrap)
4. [New Bonding Curve Launch Volatility Arbitrage](#4-new-bonding-curve-launch-volatility-arbitrage)
5. [Griefing UniswapV3 Launch by Pre-Creating Pool](#5-griefing-uniswapv3-launch-by-pre-creating-pool)
6. [CREATE2 Pair Address Mismatch Permanently Stuck](#6-create2-pair-address-mismatch-permanently-stuck)
7. [Early Pair Creation Breaks Fair Launch](#7-early-pair-creation-breaks-fair-launch)
8. [Donation Guard Bypass via Wrong Pair Address](#8-donation-guard-bypass-via-wrong-pair-address)
9. [Front-Running createPair Breaks Bootstrap](#9-front-running-createpair-breaks-bootstrap)
10. [Double-Stake Migration Locks Founder Tokens](#10-double-stake-migration-locks-founder-tokens)
11. [Presale Tokens Grant Premature Voting Power](#11-presale-tokens-grant-premature-voting-power)
12. [Dutch Auction Price Manipulation](#12-dutch-auction-price-manipulation)
13. [Crowdfund Rug Pull via Zero MaxPrice NFT Listing](#13-crowdfund-rug-pull-via-zero-maxprice-nft-listing)

---

## 1. Premature Launch via Default Value Bypass

### Overview

When a bonding curve guards its "launch to DEX" function with a two-step commit process, using a default value of 0 for the commit mapping means uninitialized entries pass the check, allowing tokens to be launched to the DEX at any time without meeting threshold criteria.

> 📖 Reference: `reports/bonding_curve_findings/c-02-tokens-can-be-launched-to-uniswap-v3-anytime-allowing-to-drain-eth.md`

### Vulnerability Description

#### Root Cause
The `commitLaunch[tokenId]` defaults to 0, so the check `block.number <= commitLaunch[tokenId]` always passes for uninitialized tokens—any block number > 0 passes the condition.

#### Attack Scenario
1. Attacker calls `launchGroupCoin()` to create a new token
2. Skips `enableUniswapV3Launch()` entirely (threshold check never executed)
3. Calls `launchGroupCoinToUniswapV3()` immediately — check passes since `block.number > 0`
4. Buys tokens cheaply at start of bonding curve, launches to Uniswap with protocol ETH, sells tokens at inflated price

### Vulnerable Pattern Examples

**Example 1: Default Zero Bypass** [HIGH]
```solidity
// ❌ VULNERABLE: commitLaunch[tokenId] defaults to 0, passes for any block > 0
if (block.number <= commitLaunch[tokenId]) {
    revert CantLaunchPoolYet();
}
```

**Example 2: Generic Uninitialized Mapping Guard** [HIGH]
```solidity
// ❌ VULNERABLE: Any uninitialized mapping entry returns 0
mapping(uint256 => uint256) public commitTimestamp;
function executeLaunch(uint256 id) external {
    require(block.timestamp > commitTimestamp[id], "Too early");
    // Passes immediately for any uncommitted id!
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Check that commit was actually set
if (block.number <= commitLaunch[tokenId] || commitLaunch[tokenId] == 0) {
    revert CantLaunchPoolYet();
}
```

### Detection Patterns
```
- block.number <= mapping[id] or block.timestamp > mapping[id] without checking != 0
- Two-step commit-execute patterns where the commit value defaults to 0
- Launch/graduation gated only by a timestamp/block comparison
```

---

## 2. Flash Loan Genesis / Graduation Exploit

### Overview

When a protocol allows launch, redemption, and DEX trading in the same transaction, an attacker can flash-loan enough capital to trigger the launch, redeem genesis tokens, sell them on the freshly-initialized DEX pools, and repay the loan with profit.

> 📖 Reference: `reports/bonding_curve_findings/c05-anyone-with-enough-liquidity-to-reach-the-maxgenesisprice-can-make-profit-fr.md`

### Vulnerability Description

#### Root Cause
All operations (deposit → launch → redeem → sell) can execute atomically in a single transaction with no time separation between launch and redemption.

#### Attack Scenario
1. Flash-borrow ETH to increase average price to `maxGenesisPrice`
2. Call `launch()` — initializes bonding curve oracle, purchases FEI, adds liquidity to Uniswap pools
3. Call `redeem()` — withdraw FEI and TRIBE proportional to deposited FGEN
4. Sell TRIBE for FEI in FEI/TRIBE pool, sell FEI for ETH in ETH/FEI pool
5. Repay flash loan, keep ~$800K profit

### Vulnerable Pattern Examples

**Example 1: Atomic Launch + Redeem** [CRITICAL]
```solidity
// ❌ VULNERABLE: launch() and redeem() can be called in the same transaction
function launch() external afterGenesisOrMaxPrice {
    // Initializes oracle, buys FEI, adds liquidity to Uniswap pools
    core.completeGenesisGroup();
}

function redeem(address to) external postGenesis {
    // Redeems FEI and TRIBE proportional to FGEN balance
    uint256 feiAmount = feiBalance() * balanceOf(to) / totalSupply();
    fei.transfer(to, feiAmount);
}
```

**Example 2: No Flash Loan Protection on Graduation** [HIGH]
```solidity
// ❌ VULNERABLE: No time delay between graduation trigger and token unwrap
function buy(uint256 amount, address token) external {
    // ... bonding curve buy logic ...
    if (tokensSold >= gradThreshold) {
        _graduate(token); // Creates Uniswap pair + adds liquidity
    }
}

function unwrapToken(address token, address[] memory accounts) public {
    require(tokenInfo[token].tradingOnUniswap, "Not graduated");
    // Atomic conversion — no time restriction!
    for (uint i = 0; i < accounts.length; i++) {
        agentToken.transferFrom(pairAddress, accounts[i], balances[i]);
    }
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Require time separation between launch and redemption
function launch() external {
    launchBlock = block.number;
    // ... launch logic ...
}

function redeem(address to) external {
    require(block.number > launchBlock, "Cannot redeem in same block as launch");
    // ... redemption logic ...
}
```

### Detection Patterns
```
- launch() and redeem() callable in same transaction/block
- Flash loan can trigger graduation threshold + immediate sell
- unwrapToken() with no time delay after graduation
- Genesis/presale without block separation between deposit and claim
```

---

## 3. Flash Loan Premature Graduation with Atomic Unwrap

### Overview

When `unwrapToken()` allows atomic conversion of bonding curve tokens to agent tokens without time restrictions, a flash loan attack can force premature graduation and manipulate reward distribution.

> 📖 Reference: `reports/bonding_curve_findings/m-04-launched-tokens-are-vulnerable-to-flashloan-attacks-forcing-premature-gradu.md`

### Vulnerability Description

#### Root Cause
`unwrapToken()` has no time-based restrictions—it allows converting memecoin to agentToken atomically upon graduation, closing the flash loan loop.

#### Vulnerable Code
```solidity
// ❌ VULNERABLE: No time restrictions on unwrapToken
function unwrapToken(address srcTokenAddress, address[] memory accounts) public {
    Token memory info = tokenInfo[srcTokenAddress];
    require(info.tradingOnUniswap, "Token is not graduated yet");

    FERC20 token = FERC20(srcTokenAddress);
    IERC20 agentToken = IERC20(info.agentToken);
    address pairAddress = factory.getPair(srcTokenAddress, router.assetToken());
    for (uint i = 0; i < accounts.length; i++) {
        address acc = accounts[i];
        uint256 balance = token.balanceOf(acc);
        if (balance > 0) {
            token.burnFrom(acc, balance);
            agentToken.transferFrom(pairAddress, acc, balance); // No time restrictions!
        }
    }
}
```

### Impact
- Premature graduation bypasses community support and liquidity building
- Forced graduated tokens gain LP value and steal reward shares from legitimate tokens
- Uniswap pair has unbalanced reserves, making price unstable

### Secure Implementation
```solidity
// ✅ SECURE: Enforce delay in unwrapToken
mapping(address => uint256) public graduationBlock;

function unwrapToken(address srcTokenAddress, address[] memory accounts) public {
    require(block.number > graduationBlock[srcTokenAddress] + UNWRAP_DELAY, "Too soon after graduation");
    // ... rest of unwrap logic ...
}
```

---

## 4. New Bonding Curve Launch Volatility Arbitrage

### Overview

Launching a new bonding curve with a discount creates a flash-loan-exploitable arbitrage opportunity that crashes the token price and drains protocol value.

> 📖 Reference: `reports/bonding_curve_findings/h02-introduction-of-additional-bondingcurves-creates-period-of-volatility.md`

### Vulnerability Description

#### Root Cause
New bonding curve offers discounted tokens (e.g., 5% off), and flash loans can atomically buy discounted tokens and sell on existing DEX pools for profit.

#### Attack Scenario
1. Flash-borrow $4.8M in DAI
2. Buy $5.053M FEI from new BondingCurve at 5% discount
3. Sell FEI for ETH on ETH/FEI Uniswap pool
4. Sell ETH for DAI on ETH/DAI pool
5. Repay loan, profit ~$137K per curve launch

### Vulnerable Pattern Examples

**Example: Discounted Bonding Curve with No Flash Loan Protection** [HIGH]
```solidity
// ❌ VULNERABLE: Discounted tokens + no flash loan protection = atomic arbitrage
contract BondingCurve {
    uint256 public scale;     // 1M-100M FEI to mint
    uint256 public buffer;    // 0-5% discount
    
    function purchase(address to, uint256 amountIn) external {
        // Mints FEI at discount until scale is reached
        uint256 amountOut = getAmountOut(amountIn);
        fei.mint(to, amountOut);
    }
}
```

### Detection Patterns
```
- New bonding curve contracts with discounted minting
- No flash loan protection on curve purchases
- Scale parameters that allow large single-transaction buys
- Immediate sellability on existing DEX pools after bonding curve purchase
```

---

## 5. Griefing UniswapV3 Launch by Pre-Creating Pool

### Overview

An attacker can front-run `launchToUniswapV3` by calling `uniswapV3Factory.createPool()` directly, permanently preventing the bonding curve from transitioning to the DEX.

> 📖 Reference: `reports/bonding_curve_findings/m-06-griefing-the-launch-to-uniswapv3-by-creating-the-pool-first.md`

### Vulnerability Description

#### Root Cause
`launchGroupCoinToUniswapV3()` calls `uniswapV3Factory.createPool()` which reverts if the pool already exists, and there's no fallback to `getPool()`.

#### Vulnerable Code
```solidity
// ❌ VULNERABLE: No check for existing pool before creating
address pool = uniswapV3Factory.createPool(address(token), WETH, config.fee);
IUniswapV3Pool(pool).initialize(config.sqrtPriceX96);
```

UniswapV3Factory requires the pool doesn't exist:
```solidity
function createPool(address tokenA, address tokenB, uint24 fee) external returns (address pool) {
    // ...
    require(getPool[token0][token1][fee] == address(0)); // Reverts if pool exists!
    pool = deploy(address(this), token0, token1, fee, tickSpacing);
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Check if pool exists before creating
function _initUniV3PoolIfNecessary(PoolAddress.PoolKey memory poolKey, uint160 sqrtPriceX96) 
    internal returns (address pool) 
{
    pool = IUniswapV3Factory(UNIV3_FACTORY).getPool(poolKey.token0, poolKey.token1, poolKey.fee);
    if (pool == address(0)) {
        pool = IUniswapV3Factory(UNIV3_FACTORY).createPool(poolKey.token0, poolKey.token1, poolKey.fee);
        IUniswapV3Pool(pool).initialize(sqrtPriceX96);
    } else {
        (uint160 sqrtPriceX96Existing, , , , , , ) = IUniswapV3Pool(pool).slot0();
        if (sqrtPriceX96Existing == 0) {
            IUniswapV3Pool(pool).initialize(sqrtPriceX96);
        } else {
            require(sqrtPriceX96Existing == sqrtPriceX96, "UV3P");
        }
    }
}
```

### Detection Patterns
```
- createPool() called without checking getPool() first
- No try/catch or existence check around Uniswap pool creation
- Graduation/launch functions that call createPool directly
```

---

## 6. CREATE2 Pair Address Mismatch Permanently Stuck

### Overview

When a custom factory uses additional salt components (e.g., LP address, fee distributor) beyond the standard `(token0, token1)`, but the launchpad's `pairFor()` function computes addresses using the standard formula, the computed address diverges from the actual deployed pair, permanently bricking graduation.

> 📖 Reference: `reports/bonding_curve_findings/h-08-create2-address-of-the-uniswap-pair-used-by-launchpad-does-not-match-addres.md`

### Vulnerability Description

#### Root Cause
The factory's salt includes `(token0, token1, launchpadLp, launchpadFeeDistributor)` but `pairFor()` only uses `(token0, token1)`.

#### Vulnerable Code
```solidity
// ❌ VULNERABLE: pairFor() uses standard salt, factory uses extended salt
// Launchpad.pairFor():
pair = IUniswapV2Pair(
    address(uint160(uint256(keccak256(abi.encodePacked(
        hex"ff",
        factory,
        keccak256(abi.encodePacked(token0, token1)),  // Missing lp and distributor!
        uniV2InitCodeHash
    )))))
);

// But factory actually uses:
bytes32 salt = keccak256(abi.encodePacked(
    token0, token1,
    _launchpadLp,            // Extra component
    _launchpadFeeDistributor // Extra component
));
```

### Impact
- System permanently stuck in bonding state—cannot graduate to AMM
- `endRewards()` also affected since it uses the same incorrect address

### Detection Patterns
```
- Custom Uniswap-style factories with non-standard CREATE2 salt
- pairFor() functions that don't match the factory's actual deployment parameters
- Init code hash mismatches between launchpad and factory
```

---

## 7. Early Pair Creation Breaks Fair Launch

### Overview

An attacker creates a DEX pair before the bonding curve graduates, pre-seeding it with manipulated reserves. When graduation occurs and `addLiquidity` is called, the existing reserves cause the protocol to add liquidity at a skewed price, allowing the attacker to drain all funds.

> 📖 Reference: `reports/bonding_curve_findings/mnbd1-5-early-pair-creation-breaks-fair-launch-of-new-moon-tokens-and-gives-an-a.md`

### Vulnerability Description

#### Root Cause
No restriction on creating a DEX pair for the token before graduation. The liquidity addition uses the existing pair's reserves to calculate token amounts.

#### Attack Scenario
1. Attacker buys tokens from bonding curve
2. Creates pair on DEX with 1e10 KAS and 1 wei of token → extremely low token price
3. When graduation triggers `addLiquidityKAS`, formula uses: `kasAmount = (moonTokenAmount * kasReserves) / moonTokenReserves`
4. Due to reserve imbalance, nearly all KAS deposited with negligible tokens
5. Attacker swaps their tokens to drain all the KAS

#### Vulnerable Code
```solidity
// ❌ VULNERABLE: No check if pair exists before adding liquidity
ERC20(token).approve(zealousSwapRouter, tokenForLiquidity);
IZealousSwapRouter02(zealousSwapRouter).addLiquidityKAS{ value: kasCollected }(
    token,
    tokenForLiquidity,
    0,    // amountTokenMin = 0!
    0,    // amountKASMin = 0!
    address(this),
    block.timestamp + 15 minutes
);
```

### Secure Implementation

```solidity
// ✅ SECURE: Only allow pair creation after graduation
function graduateToken() internal {
    // Mark as graduated FIRST
    tokenManager.graduateToken(token);
    
    // THEN add liquidity (pair creation now gated by graduated status)
    ERC20(token).approve(zealousSwapRouter, tokenForLiquidity);
    IZealousSwapRouter02(zealousSwapRouter).addLiquidityKAS{ value: kasCollected }(
        token,
        tokenForLiquidity,
        minTokenAmount,  // Enforce slippage!
        minKasAmount,    // Enforce slippage!
        address(this),
        block.timestamp + 15 minutes
    );
}
```

---

## 8. Donation Guard Bypass via Wrong Pair Address

### Overview

When a launchpad blocks token donations to the AMM pair during bonding by checking `recipient != pairFor(...)`, but `pairFor()` computes the wrong address (see Pattern 6), the check is ineffective and attackers can send tokens directly to the real pair.

> 📖 Reference: `reports/bonding_curve_findings/m-21-bypass-of-recipient-check-allows-pre-seeding-the-real-pair-and-manipulating.md`

### Vulnerable Code
```solidity
// ❌ VULNERABLE: pairFor() returns wrong address, so check always passes
function _assertValidRecipient(address recipient, address baseToken) internal view returns (IUniswapV2Pair pair) {
    pair = pairFor(address(uniV2Factory), baseToken, _launches[baseToken].quote);
    if (address(pair) == recipient) revert InvalidRecipient();
    // Attacker passes the REAL pair address → pairFor returns WRONG address → check passes!
}
```

### Detection Patterns
```
- Donation guards that compare recipient to computed pair address
- pairFor() that doesn't match the actual factory's CREATE2 formula
- buy() with recipient parameter that can be set to any address
```

---

## 9. Front-Running createPair Breaks Bootstrap

### Overview

An attacker front-runs `addLiquidity()` by calling `createPair()` first with different `initParams`, breaking the protocol's bootstrap logic and causing loss for initial LPs.

> 📖 Reference: `reports/bonding_curve_findings/m-1-some-unusual-problems-arise-in-the-use-of-the-goatv1factorysolcreatepair-fun.md`

### Vulnerable Code
```solidity
// ❌ VULNERABLE: If pair exists, falls through to AMM logic instead of bootstrap
function _addLiquidity(address token, uint256 tokenDesired, uint256 wethDesired, ...) internal {
    GoatV1Pair pair = GoatV1Pair(GoatV1Factory(FACTORY).getPool(token));
    if (address(pair) == address(0)) {
        pair = GoatV1Pair(GoatV1Factory(FACTORY).createPair(token, initParams));
        vars.isNewPair = true;
    }
    
    if (vars.isNewPair) {
        // Bootstrap logic
    } else {
        // AMM logic — attacker forced this path with different initParams!
        (uint256 wethReserve, uint256 tokenReserve) = pair.getReserves();
        uint256 tokenAmountOptimal = GoatLibrary.quote(wethDesired, wethReserve, tokenReserve);
    }
}
```

---

## 10. Double-Stake Migration Locks Founder Tokens

### Overview

During agent migration, founders must provide additional virtual tokens while their original LP tokens remain locked in the old `veToken` contract for 10 years, causing a double-staking problem.

> 📖 Reference: `reports/bonding_curve_findings/m-22-founder-has-to-double-stake-during-migration-with-the-initial-lp-locked-in-.md`

### Vulnerable Code
```solidity
// ❌ VULNERABLE: No mechanism to unlock old LP tokens during migration
function migrateAgent(uint256 id, string memory name, string memory symbol, bool canStake) external {
    // Creates new token, LP, veToken, and DAO
    address token = _createNewAgentToken(name, symbol);
    IERC20(_assetToken).transferFrom(founder, token, initialAmount); // Founder pays AGAIN
    
    // Old LP tokens stay locked in old veToken:
    // withdraw() requires: block.timestamp >= matureAt (10 years!)
}
```

### Detection Patterns
```
- Migration functions that create new staking without unlocking old positions
- veToken/lock contracts without emergency migration withdrawal
- Founder lock periods that span longer than expected migration cycles
```

---

## 11. Presale Tokens Grant Premature Voting Power

### Overview

Tokens minted directly to contributors during a presale may unintentionally grant DAO voting power before the presale is complete, allowing early contributors to influence governance.

> 📖 Reference: `reports/bonding_curve_findings/balanceredirectpresale-tokens-vest-during-the-presale-phase-wont-fix.md`

### Vulnerable Pattern
```solidity
// ❌ VULNERABLE: Directly minting tokens during presale grants immediate governance power
function contribute(uint256 amount) external duringPresale {
    token.mint(msg.sender, amount * rate); // Immediate mint = immediate voting power
}
```

### Secure Implementation
```solidity
// ✅ SECURE: Vest tokens and release only after presale
function contribute(uint256 amount) external duringPresale {
    pendingTokens[msg.sender] += amount * rate;
}

function claim() external afterPresale {
    token.mint(msg.sender, pendingTokens[msg.sender]);
    pendingTokens[msg.sender] = 0;
}
```

---

## 12. Dutch Auction Price Manipulation

### Overview

A Dutch auction for bonding curve tokens can be manipulated by purchasing `maxCommitments - 1 wei`, preventing the auction from finalizing and guaranteeing a purchase at the midpoint price or lower.

> 📖 Reference: `reports/bonding_curve_findings/m-26-dutch-auction-can-be-manipulated.md`

### Vulnerability Description

#### Root Cause
`_endAuction()` only triggers when commitments >= maxCommitments. Purchasing 1 wei shy prevents finalization, and the remaining 1 wei purchase will revert in AMMs due to rounding.

#### Attack Scenario
1. Attacker calls `purchaseArbitrageTokens` with `maxCommitments - 1 wei`
2. `_endAuction()` not triggered since commitments < maxCommitments
3. Any further 1 wei purchase reverts in AMM due to rounding
4. Wait for `stabilizeBackoffPeriod` (5 min) to pass
5. Attacker guaranteed purchase at `(startingPrice + endingPrice) / 2` or lower

### Detection Patterns
```
- Dutch auction with strict equality check for finalization
- No incentive for permissionless auction finalization
- Price not locked at time of commitment — keeps decreasing
```

---

## 13. Crowdfund Rug Pull via Zero MaxPrice NFT Listing

### Overview

When a crowdfund's `maximumPrice` is 0, an attacker can list their own NFT, flash-loan contributions to appear unanimous, buy the worthless NFT, then pass a proposal to extract all contribution funds.

> 📖 Reference: `reports/bonding_curve_findings/m-01-attacker-can-list-an-nft-they-own-and-inflate-to-zero-all-users-contributio.md`

### Vulnerable Pattern
```solidity
// ❌ VULNERABLE: maximumPrice of 0 allows any NFT to be "purchased"
function buy(uint256 tokenId, uint256 price) external {
    require(price <= maximumPrice || maximumPrice == 0, "Too expensive");
    // When maximumPrice == 0, this passes for ANY price including 0
}
```

### Detection Patterns
```
- Crowdfund with configurable maximumPrice that can be 0
- Flash-loaned contribution inflation
- Governance proposals that can distribute crowdfund treasury
```

---

## Prevention Guidelines

### Development Best Practices
1. **Enforce time separation** between graduation/launch and redemption/unwrap — at minimum a different block
2. **Check for existing pools/pairs** before calling `createPool()` / `createPair()`
3. **Verify CREATE2 salt components** match between launchpad's `pairFor()` and the actual factory
4. **Restrict pair creation** to only the bonding curve contract or after graduation
5. **Lock auction prices** at commitment time, not at finalization time
6. **Add flash loan protection** on all graduation-triggering operations
7. **Include slippage parameters** in `addLiquidity` calls during graduation

### Testing Requirements
- Test atomic flash loan graduation attack
- Test pre-creating pairs before graduation
- Test CREATE2 address computation matches factory
- Test default value bypass in commit mappings
- Test Dutch auction edge case at `maxCommitments - 1`

### Keywords for Search

`token launch`, `graduation`, `bonding curve`, `createPair`, `createPool`, `addLiquidity`, `fair launch`, `flash loan graduation`, `premature launch`, `pool creation griefing`, `CREATE2 mismatch`, `pairFor`, `presale`, `dutch auction`, `unwrapToken`, `migration`, `double stake`, `early pair creation`, `donation guard bypass`, `pre-seeding`, `bootstrap`, `maxGenesisPrice`, `gradThreshold`, `commitLaunch`
