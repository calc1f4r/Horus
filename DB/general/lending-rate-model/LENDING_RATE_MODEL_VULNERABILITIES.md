---
# Core Classification
protocol: generic
chain: everychain
category: interest_rate_model
vulnerability_type: lending_rate_miscalculation

# Pattern Identity
root_cause_family: interest_rate_accounting_error
pattern_key: flawed_rate_calculation | interest_rate_model | utilization_manipulation | incorrect_rates_or_dos

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - InterestRateModel
  - LendingPool
  - Market
  - DebtToken
  - ReserveLogic
  - AMO
path_keys:
  - flawed_rate_calculation | utilization_formula | InterestRateModel | wrong_reserves_in_denominator
  - wrong_chain_constant | blocksPerYear | InterestRateModel | 5x_rate_multiplier
  - missing_utilization_cap | withdrawal | LendingPool→InterestRateModel | unbounded_rates_dos
  - manipulable_utilization | spot_balances | InterestRateModel | rate_gaming
  - incorrect_debt_scaling | debtToken_totalSupply | Market→InterestRateModel | inflated_rates
  - amo_utilization_manipulation | update_function | AMO→LendingPool | forced_reduced_rates

# Attack Vector Details
attack_type: economic_exploit
affected_component: interest_rate_calculation

# Technical Primitives
primitives:
  - utilization_rate
  - blocksPerYear
  - baseRatePerBlock
  - multiplierPerBlock
  - kink
  - optimal_utilization
  - reserves
  - accrueInterest
  - borrowRatePerBlock
  - supplyRatePerBlock
  - debtToken_scaling
  - totalDeposits
  - totalBorrows

# Grep / Hunt-Card Seeds
code_keywords:
  - utilizationRate
  - blocksPerYear
  - baseRatePerBlock
  - multiplierPerBlock
  - accrueInterest
  - borrowRatePerBlock
  - getBorrowRate
  - getSupplyRate
  - totalBorrows
  - totalDeposits
  - totalReserves
  - optimalUtilization
  - kink
  - updateInterestRates
  - scaledTotalSupply
  - previewFloatingAssetsAverage

# Impact Classification
severity: high
impact: incorrect_interest_rates
exploitability: 0.70
financial_impact: high

# Context Tags
tags:
  - defi
  - lending
  - interest_rate
  - compound
  - aave
  - utilization
  - rate_model
  - borrowing
  - yield

# Version Info
language: solidity
version: ">=0.8.0"
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [wrong-blocksPerYear] | reports/lending_rate_model_findings/h-01-incorrect-blocksperyear-constant-in-whitepaperinterestratemodel.md | HIGH | Code4rena | 20769 |
| [reserves-in-utilization] | reports/lending_rate_model_findings/h-02-erc721-interest-model-miscalculates-utilization-rate-due-to-reserves.md | HIGH | ZachObront | 31811 |
| [utilization-over-100] | reports/lending_rate_model_findings/h-03-utilization-ratio-can-exceed-100-due-to-missing-validation-in-withdrawal-fu.md | HIGH | Code4rena | 62063 |
| [amo-utilization-manip] | reports/lending_rate_model_findings/h-01-siloamo-can-be-forced-to-fund-reduced-interest-rates-by-manipulating-utiliz.md | HIGH | ZachObront | 18686 |
| [prime-vs-optimal] | reports/lending_rate_model_findings/interest-rate-model-uses-prime-rate-instead-of-optimal-rate-at-optimal-utilizati.md | MEDIUM | Codehawks | 57275 |
| [pi-model-manipulable] | reports/lending_rate_model_findings/pi-interest-rate-model-is-manipulatable-due-to-current-balances-used.md | MEDIUM | — | — |
| [zero-avg-gaming] | reports/lending_rate_model_findings/m-13-utilization-rates-are-0-when-average-assets-are-0-which-may-be-used-to-game.md | MEDIUM | Sherlock | 33166 |
| [incorrect-liquidate-rates] | reports/lending_rate_model_findings/m-14-incorrect-accounting-of-utilization-supplyborrow-rates-due-to-vulnerable-im.md | MEDIUM | Code4rena | 36896 |
| [accrueInterest-revert] | reports/lending_rate_model_findings/m-15-accrueinterest-is-expected-to-revert-when-the-rate-is-higher-than-the-maxim.md | MEDIUM | Code4rena | 26851 |
| [debttoken-scaling] | reports/lending_rate_model_findings/incorrect-debttoken-totalsupply-scaling-breaks-interest-rate-calculations.md | HIGH | — | — |
| [fix-utilization-reserves] | reports/lending_rate_model_findings/fix-utilization-rate-computation-and-respect-reserves-when-lending.md | MEDIUM | — | — |
| [low-liquidity-inflate] | reports/lending_rate_model_findings/users-can-take-advantage-of-low-liquidity-markets-to-inﬂate-the-interest-rate.md | MEDIUM | — | — |
| [amo-treasury-risk] | reports/lending_rate_model_findings/h-04-amo-model-opens-up-ohm-treasury-to-increased-risk.md | HIGH | ZachObront | — |
| [system-halt-interest] | reports/lending_rate_model_findings/if-base_updateinterest-fails-the-entire-system-will-halt.md | MEDIUM | — | — |
| [denial-liquidation-borrow] | reports/lending_rate_model_findings/m-06-denial-of-liquidations-and-redemptions-by-borrowing-all-reserves-from-aave.md | MEDIUM | — | — |

## Vulnerability Title

**Lending Interest Rate Model Vulnerabilities** — Miscalculations, manipulation, and DoS patterns in lending protocol interest rate systems covering utilization formula errors, chain-specific constants, rate manipulation, and accrual failures.

### Overview

Lending protocols use interest rate models (Compound-style WhitePaper models, jump rate models, PI controllers, etc.) to calculate borrow/supply rates based on utilization ratios. This entry covers 6 vulnerability families with 15+ unique findings from 8+ independent auditors across 10+ protocols. Core patterns include incorrect utilization formulas, wrong chain constants, manipulable rate inputs, missing utilization caps, and debt scaling errors that break rate calculations.

#### Agent Quick View

- Root cause statement: "These vulnerabilities exist because lending interest rate models use incorrect utilization formulas (wrong reserves handling, chain-specific constants), lack utilization bounds checking, accept manipulable spot inputs, or have debt token scaling errors — leading to incorrect interest rates, protocol DoS, or economic exploitation."
- Pattern key: `flawed_rate_calculation | interest_rate_model | utilization_manipulation | incorrect_rates_or_dos`
- Interaction scope: `multi_contract`
- Primary affected component(s): `InterestRateModel, LendingPool/Market, DebtToken, AMO`
- Contracts / modules involved: `InterestRateModel, LendingPool, Market, DebtToken, ReserveLogic, AMO`
- Path keys: `utilization_formula | InterestRateModel`, `blocksPerYear | InterestRateModel`, `withdrawal | LendingPool→InterestRateModel`, `spot_balances | InterestRateModel`, `debtToken | Market→InterestRateModel`, `AMO | AMO→LendingPool`
- High-signal code keywords: `utilizationRate, blocksPerYear, baseRatePerBlock, getBorrowRate, accrueInterest, kink, optimalUtilization, totalReserves, scaledTotalSupply`
- Typical sink / impact: `incorrect interest rates / protocol DoS / rate manipulation / unfair liquidation / treasury drain`
- Validation strength: `strong` (15+ unique findings, 8+ auditors, 10+ protocols)

#### Contract / Boundary Map

```
LendingPool / Market
     │
     ├── accrueInterest() ──→ InterestRateModel.getBorrowRate(cash, borrows, reserves)
     │                              │
     │                              ├── utilizationRate(cash, borrows, reserves)
     │                              │       └── borrows / (cash + borrows - reserves)
     │                              │
     │                              └── rate = baseRate + multiplier * utilization
     │                                   └── (if util > kink): rate += jumpMultiplier * (util - kink)
     │
     ├── DebtToken.scaledTotalSupply() ──→ used as borrows input
     │
     └── AMO.update() ──→ deposits/withdraws to manipulate utilization
```

- Entry surface(s): `Market.accrueInterest()`, `LendingPool.withdraw()`, `AMO.update()`, `Market.borrow()`
- Contract hop(s): `LendingPool → InterestRateModel.getBorrowRate()`, `Market.accrueInterest → InterestRateModel`, `AMO → LendingPool deposits/withdrawals`
- Trust boundary crossed: `rate model inputs (cash/borrows/reserves) come from pool state that may be stale or manipulable`
- Shared state or sync assumption: `utilization must reflect actual borrowing vs available liquidity`, `reserves must be correctly categorized`, `chain block timing must match model constants`

#### Valid Bug Signals

- `blocksPerYear`, per-block multiplier, or annual-to-block conversion is copied from another chain and does not match deployment block cadence.
- Utilization denominator includes reserves/protocol fees/non-lendable accounting units or omits cash/borrows in a way that can make utilization exceed 100% or revert.
- `withdraw`, `redeem`, reserve seizure, or collateral removal can push utilization above the borrow-time maximum without rechecking the cap.
- Rate model uses spot `balanceOf`, current pool cash, or zero/empty averages that can be gamed around `accrueInterest`/`updateInterestRates`.
- Debt token `totalSupply`, scaled balances, indexes, or shares are used without converting to underlying debt units.
- AMO/treasury update logic can be triggered after manipulating utilization, forcing deposits/withdrawals that subsidize borrowers or increase treasury risk.

#### False Positive Guards

- Not this bug merely because rates are per-second; still inspect utilization units, debt scaling, caps, and manipulable inputs.
- Safe if chain timing constants are deployment-specific or configurable with governance controls and tests for the target chain.
- Safe if utilization formula uses actual lendable cash and actual borrows, caps or reverts cleanly above max utilization, and all withdrawal-like paths enforce the same invariant.
- Safe if rate inputs are time-weighted or otherwise manipulation-resistant and debt shares are converted through the current index before use.
- Requires attacker capital, liquidity timing, low-liquidity market access, AMO update influence, or a public path that can trigger accrual/rate updates after state manipulation.

---

## Section 1: Utilization Formula Errors

### Root Cause

The standard Compound utilization formula is `borrows / (cash + borrows - reserves)`. When `reserves` doesn't represent tokens actually held by the market (e.g., in ERC721 markets where reserves counts cTokens), or when reserves grow unboundedly, the formula produces incorrect utilization rates — potentially exceeding 100% or reverting.

### Attack Scenario / Path Variants

**Path A: Wrong Reserves in Utilization Denominator**
Path key: `flawed_rate_calculation | utilization_formula | InterestRateModel | wrong_reserves_in_denominator`
Entry surface: `InterestRateModel.utilizationRate()`
Contracts touched: `InterestRateModel (internal)`
1. Standard formula: `utilization = borrows / (cash + borrows - reserves)`
2. In ERC721 markets, `reserves` is incremented as interest accrues, representing cToken claims
3. Unlike ERC20 markets, these reserves are NOT part of `cash` (not actual tokens in the contract)
4. As reserves grow, denominator shrinks → utilization approaches infinity
5. When `reserves > cash + borrows`, the function reverts, bricking the market
6. **Impact**: Interest rates grow uncontrollably, then market becomes non-functional

**Path B: Utilization Exceeds 100% on Withdrawal**
Path key: `missing_utilization_cap | withdrawal | LendingPool→InterestRateModel | unbounded_rates_dos`
Entry surface: `LendingPool.withdraw()` / `LendingPool.withdrawCollateral()`
Contracts touched: `LendingPool → InterestRateModel`
1. `require_utilization_below_max` is enforced on `borrow()` but NOT on `withdraw()`
2. Large withdrawal reduces `total_supply` (cash) in utilization denominator
3. Utilization ratio exceeds 100% → backstop interest or donated amounts count
4. Interest rate model produces extreme values → cascading liquidations
5. **Impact**: Unbounded interest rates, market instability, bad debt accumulation

### Vulnerable Pattern Examples

**Example 1: Reserves Incorrectly in ERC721 Utilization** [HIGH]
```solidity
// ❌ VULNERABLE: reserves represents cToken claims, not actual cash — denominator shrinks unboundedly
// Source: reports/lending_rate_model_findings/h-02-erc721-interest-model-miscalculates-utilization-rate-due-to-reserves.md
function utilizationRate(uint cash, uint borrows, uint reserves) public pure returns (uint) {
    if (borrows == 0) return 0;
    return borrows * BASE / (cash + borrows - reserves);
    // ↑ In ERC721 markets, reserves != actual held tokens
    // As reserves grows → denominator shrinks → utilization → ∞
    // When reserves > cash + borrows → REVERTS
}
```

**Example 2: Missing Utilization Cap on Withdrawal** [HIGH]
```rust
// ❌ VULNERABLE: apply_withdraw does not enforce utilization max (Blend V2 - Soroban/Rust)
// Source: reports/lending_rate_model_findings/h-03-utilization-ratio-can-exceed-100-due-to-missing-validation-in-withdrawal-fu.md
fn apply_withdraw(pool: &mut Pool, amount: i128) {
    pool.total_supply -= amount;
    // Missing: require_utilization_below_max(pool);
    // Withdrawal reduces denominator → utilization can exceed 100%
    // Interest rate model produces extreme values
}
```

---

## Section 2: Chain-Specific Constant Errors

### Root Cause

Compound-forked interest rate models use `blocksPerYear` to convert annualized rates to per-block rates. When deployed on chains with different block times (BNB Chain: 3s, Ethereum: 12-15s, L2s: 2s), the hardcoded constant produces rates that are N× higher or lower than intended.

### Attack Scenario / Path Variants

**Path A: Wrong blocksPerYear for Deployment Chain**
Path key: `wrong_chain_constant | blocksPerYear | InterestRateModel | Nx_rate_multiplier`
Entry surface: `InterestRateModel constructor` / deployment configuration
Contracts touched: `InterestRateModel (internal)`
1. WhitePaperInterestRateModel hardcodes `blocksPerYear = 2102400` (assumes 15s block time)
2. Venus Protocol deploys on BNB Chain (3s block time → actual blocks/year = 10512000)
3. `baseRatePerBlock = baseRatePerYear / blocksPerYear` → 5× too large
4. `multiplierPerBlock = multiplierPerYear / blocksPerYear` → 5× too large
5. Both components scale: total interest rate is 5× intended at every utilization level
6. Pool also 5× more sensitive to utilization changes
7. Arbitrageurs deposit to exploit high supply rate → utilization drops to ~0
8. **Impact**: Interest rates 5× higher than intended, market cannot self-correct via arbitrage

### Vulnerable Pattern Examples

**Example 3: Hardcoded blocksPerYear for Wrong Chain** [HIGH]
```solidity
// ❌ VULNERABLE: blocksPerYear assumes 15s blocks (Ethereum), but deployed on BNB (3s blocks)
// Source: reports/lending_rate_model_findings/h-01-incorrect-blocksperyear-constant-in-whitepaperinterestratemodel.md
contract WhitePaperInterestRateModel {
    uint public constant blocksPerYear = 2102400; // ← assumes 15s blocks
    // On BNB chain: actual blocks/year = 10512000 (3s blocks)
    // Result: baseRatePerBlock and multiplierPerBlock are 5x too high

    constructor(uint baseRatePerYear, uint multiplierPerYear) {
        baseRatePerBlock = baseRatePerYear / blocksPerYear;      // 5x too high
        multiplierPerBlock = multiplierPerYear / blocksPerYear;   // 5x too high
    }
}
```

---

## Section 3: Utilization Manipulation & Rate Gaming

### Root Cause

Interest rate models that use spot (instantaneous) balances for utilization calculation are vulnerable to manipulation. Attackers can temporarily alter pool state (via flash loans, large deposits/withdrawals, or AMO manipulation) to force favorable rates during their transaction.

### Attack Scenario / Path Variants

**Path A: AMO Forced to Fund Reduced Rates**
Path key: `amo_utilization_manipulation | update_function | AMO→LendingPool | forced_reduced_rates`
Entry surface: `AMO.update()` (permissionless)
Contracts touched: `AMO → LendingPool`
1. SiloAMO's `update()` compares `totalDeposits` to `targetDeploymentAmount = totalBorrows / uopt`
2. Attacker temporarily borrows a large amount → spikes totalBorrows
3. `targetDeploymentAmount` increases proportionally
4. AMO deposits more funds to bring utilization to optimal
5. Attacker repays borrow → utilization drops far below optimal
6. AMO's deposit is now locked for a full day (update frequency limit)
7. **Impact**: Interest rates forced down for 24h, subsidized by AMO/treasury

**Path B: Zero Average Assets Allows Lowest Rate Borrow**
Path key: `manipulable_utilization | spot_balances | InterestRateModel | rate_gaming`
Entry surface: `Market.borrow()`
Contracts touched: `Market → InterestRateModel`
1. At protocol launch, `floatingAssetsAverage = 0` and `lastAverageUpdate = block.timestamp`
2. When `block.timestamp == lastAverageUpdate`, `averageFactor = 0`
3. `previewFloatingAssetsAverage()` returns 0 regardless of actual deposits
4. Utilization calculated as 0 even with substantial borrows
5. User gets borrow at lowest possible interest rate
6. **Impact**: Risk-free near-full utilization borrowing at launch

**Path C: Spot Balance Manipulation in PI Controller**
Path key: `manipulable_utilization | spot_balances | InterestRateModel | rate_gaming`
Entry surface: `InterestRateModel.calculateRate()`
Contracts touched: `InterestRateModel (internal)`
1. PI (proportional-integral) rate model uses `currentBalances` to determine `errorTerm`
2. `errorTerm = targetUtilization - currentUtilization`
3. Attacker flash-deposits large amount → utilization drops → rate decreases
4. Attacker borrows at reduced rate in same transaction
5. **Impact**: Systematic underpayment of interest

### Vulnerable Pattern Examples

**Example 4: AMO Update Manipulated via Temporary Borrowing** [HIGH]
```solidity
// ❌ VULNERABLE: update() uses spot totalBorrows, permissionlessly callable
// Source: reports/lending_rate_model_findings/h-01-siloamo-can-be-forced-to-fund-reduced-interest-rates-by-manipulating-utiliz.md
function _update() internal {
    ISilo(market).accrueInterest(address(OHM));
    ISilo.AssetStorage memory assetStorage = ISilo(market).assetStorage(address(OHM));
    uint256 totalDeposits = assetStorage.totalDeposits;
    uint256 targetDeploymentAmount = getTargetDeploymentAmount();
    // ↑ = totalBorrows / uopt — uses spot totalBorrows, manipulable
    if (targetDeploymentAmount < totalDeposits) {
        uint256 amountToWithdraw = totalDeposits - targetDeploymentAmount;
        // AMO withdraws
    } else {
        uint256 amountToDeposit = targetDeploymentAmount - totalDeposits;
        // AMO deposits — can be forced by spiking totalBorrows
    }
}
```

**Example 5: Zero Average Assets at Launch** [MEDIUM]
```solidity
// ❌ VULNERABLE: averageFactor = 0 when block.timestamp == lastAverageUpdate
// Source: reports/lending_rate_model_findings/m-13-utilization-rates-are-0-when-average-assets-are-0-which-may-be-used-to-game.md
function previewFloatingAssetsAverage() public view returns (uint256) {
    uint256 dampSpeedFactor = memFloatingAssets < memFloatingAssetsAverage ? dampSpeedDown : dampSpeedUp;
    uint256 averageFactor = uint256(1e18 - (-int256(dampSpeedFactor * (block.timestamp - lastAverageUpdate))).expWad());
    // When block.timestamp == lastAverageUpdate: averageFactor = 1 - e^0 = 0
    return memFloatingAssetsAverage.mulWadDown(1e18 - averageFactor) + averageFactor.mulWadDown(memFloatingAssets);
    // Returns memFloatingAssetsAverage = 0 → utilization = 0 → lowest rate
}
```

---

## Section 4: Debt Token Scaling & Rate Accounting Errors

### Root Cause

When interest rate calculations use `debtToken.totalSupply()` or `debtToken.scaledTotalSupply()` as the borrows input, scaling mismatches between the debt token's internal representation and the actual borrowed amount produce incorrect utilization rates and therefore incorrect interest rates.

### Attack Scenario / Path Variants

**Path A: Debt Token Total Supply Scaling Mismatch**
Path key: `incorrect_debt_scaling | debtToken_totalSupply | Market→InterestRateModel | inflated_rates`
Entry surface: `Market.accrueInterest()`
Contracts touched: `Market → DebtToken → InterestRateModel`
1. `debtToken.scaledTotalSupply()` returns a normalized/index-divided value
2. Rate model expects actual borrow amounts, not scaled amounts
3. Mismatch inflates or deflates utilization depending on direction
4. **Impact**: Incorrect borrow/supply rates for all market participants

**Path B: Incorrect Liquidity Input in Liquidation Flow**
Path key: `incorrect_liquidation_accounting | liquidate | IsolateLogic→InterestRateModel | inflated_rates`
Entry surface: `IsolateLogic.executeIsolateLiquidate()`
Contracts touched: `IsolateLogic → InterestRateModel`
1. When bid amount doesn't cover full debt, liquidator pays extra (`vars.totalExtraAmount`)
2. `updateInterestRates` called with `liquidityAdded = totalBorrowAmount + totalExtraAmount`
3. But actual liquidity added to pool is only `totalBorrowAmount` (bid proceeds)
4. Inflated `liquidityAdded` input → utilization calculated incorrectly → wrong rates
5. **Impact**: Inflated borrow and supply rates until next rate update

### Vulnerable Pattern Examples

**Example 6: Incorrect Liquidity Input in Liquidation** [MEDIUM]
```solidity
// ❌ VULNERABLE: liquidityAdded double-counts extraAmount
// Source: reports/lending_rate_model_findings/m-14-incorrect-accounting-of-utilization-supplyborrow-rates-due-to-vulnerable-im.md
function executeIsolateLiquidate(...) internal {
    // vars.borrowAmount = loanData.bidAmount + extraAmount
    if (loanData.bidAmount < vars.borrowAmount) {
        vars.extraBorrowAmounts[idx] = vars.borrowAmount - loanData.bidAmount;
    }
    // ← BUG: totalBorrowAmount already includes extraAmount
    InterestLogic.updateInterestRates(poolData, debtAssetData,
        (vars.totalBorrowAmount + vars.totalExtraAmount), // double-counted
        0
    );
    // Only totalBorrowAmount is actually added to liquidity:
    VaultLogic.erc20TransferOutBidAmountToLiqudity(debtAssetData, vars.totalBorrowAmount);
}
```

---

## Section 5: Rate Model DoS & System Halt

### Root Cause

When interest rates grow beyond expected bounds (due to utilization >100%, compounding errors, or external rate caps), the `accrueInterest()` function can revert, halting all market operations (borrow, repay, liquidate, withdraw).

### Attack Scenario / Path Variants

**Path A: accrueInterest Reverts at Max Rate**
Path key: `rate_exceeds_max | accrueInterest | Market | system_halt_dos`
Entry surface: `Market.accrueInterest()`
Contracts touched: `Market → InterestRateModel`
1. Utilization reaches extreme levels (via manipulation or organic demand)
2. Rate model returns rate above `borrowRateMaxMantissa` threshold
3. `accrueInterest()` reverts: `require(borrowRateMantissa <= borrowRateMaxMantissa)`
4. ALL market operations depend on `accrueInterest` succeeding as a precondition
5. **Impact**: Complete market freeze — no borrows, repays, liquidations, or withdrawals possible

**Path B: Borrowing All Reserves Blocks Liquidations**
Path key: `missing_reserve_protection | borrow_all_reserves | LendingPool→external | dos_liquidation`
Entry surface: `LendingPool.borrow()` on external protocol (Aave)
Contracts touched: `Protocol → Aave/external lending pool`
1. Protocol borrows from Aave to manage its reserves
2. Attacker borrows remaining Aave reserves → Aave utilization = 100%
3. Protocol cannot withdraw from Aave to fund liquidations or redemptions
4. **Impact**: Liquidations and redemptions blocked

### Vulnerable Pattern Examples

**Example 7: accrueInterest Revert at Max Rate** [MEDIUM]
```solidity
// ❌ VULNERABLE: Market halts when rate exceeds max — no graceful degradation
// Source: reports/lending_rate_model_findings/m-15-accrueinterest-is-expected-to-revert-when-the-rate-is-higher-than-the-maxim.md
function accrueInterest() public returns (uint) {
    uint borrowRateMantissa = interestRateModel.getBorrowRate(cash, borrows, reserves);
    require(borrowRateMantissa <= borrowRateMaxMantissa, "borrow rate too high");
    // ↑ If rate model returns extreme value, ALL operations halt
    // No repay, no liquidation, no withdrawal possible
}
```

---

## Impact Analysis

### Technical Impact
- **Incorrect interest rates**: 5× multiplier from wrong chain constants, inflated rates from reserve miscounting (Common — 6/15 unique findings)
- **Market DoS / freeze**: accrueInterest reverts block all operations (Moderate — 3/15 unique findings)
- **Rate manipulation**: AMO manipulation, spot balance gaming allow unfair borrowing costs (Common — 4/15 unique findings)
- **Cascading liquidations**: Extreme utilization ratios trigger unwarranted liquidations (Moderate — 2/15 unique findings)

### Business Impact
- **Financial**: Borrowers pay 5× intended interest (Venus), or get near-zero rates at launch (Exactly)
- **Protocol stability**: Market freeze prevents liquidations → bad debt accumulation
- **Treasury risk**: AMO manipulation forces treasury to subsidize reduced rates (OlympusDAO)

### Affected Scenarios
- All Compound-forked lending protocols deployed on non-Ethereum chains
- ERC721/NFT lending markets using standard Compound utilization formulas
- Protocols with AMO modules managing lending pool liquidity
- PI controller rate models using spot balances
- Lending protocols allowing external reserve borrowing

---

## Secure Implementation

**Fix 1: Chain-Specific blocksPerYear**
```solidity
// ✅ SECURE: Use chain-specific block time or switch to per-second rate model
contract InterestRateModel {
    // Option A: Chain-specific constant
    uint public immutable blocksPerYear;  // set in constructor per chain

    constructor(uint _blocksPerYear, uint baseRatePerYear, uint multiplierPerYear) {
        blocksPerYear = _blocksPerYear;  // 10512000 for BNB (3s), 2628000 for Ethereum (12s)
        baseRatePerBlock = baseRatePerYear / blocksPerYear;
        multiplierPerBlock = multiplierPerYear / blocksPerYear;
    }

    // Option B: Time-based rates (preferred for multi-chain)
    // uint public immutable baseRatePerSecond = baseRatePerYear / 365.25 days;
}
```

**Fix 2: Correct Utilization for Non-Standard Reserve Types**
```solidity
// ✅ SECURE: Exclude non-cash reserves from utilization calculation
function utilizationRate(uint cash, uint borrows, uint reserves) public pure returns (uint) {
    if (borrows == 0) return 0;
    // For markets where reserves don't represent held tokens:
    return borrows * BASE / (cash + borrows);  // exclude reserves entirely
}
```

**Fix 3: Utilization Cap on Withdrawals**
```rust
// ✅ SECURE: Enforce utilization cap after withdrawal
fn apply_withdraw(pool: &mut Pool, amount: i128) {
    pool.total_supply -= amount;
    require_utilization_below_max(pool);  // enforce cap
}
```

---

## Detection Patterns

### Contract / Call Graph Signals
```
- InterestRateModel with hardcoded blocksPerYear deployed on non-Ethereum chain
- utilizationRate() using reserves in denominator for non-standard asset types
- withdraw() path that doesn't enforce utilization ceiling
- AMO.update() permissionlessly callable and using spot totalBorrows
- accrueInterest() with hard revert on rate exceeding maximum
- debtToken.scaledTotalSupply() used directly as borrows input in rate calc
```

### High-Signal Grep Seeds
```
- blocksPerYear
- utilizationRate
- baseRatePerBlock
- multiplierPerBlock
- getBorrowRate
- accrueInterest
- borrowRateMaxMantissa
- totalReserves
- optimalUtilization
- kink
- updateInterestRates
- scaledTotalSupply
- previewFloatingAssetsAverage
- getTargetDeploymentAmount
```

### Code Patterns to Look For
```
- Pattern 1: blocksPerYear constant that doesn't match deployment chain block time
- Pattern 2: reserves in utilization denominator for asset types where reserves ≠ held tokens
- Pattern 3: Missing require_utilization_below_max after withdraw operations
- Pattern 4: Spot balances (not TWAP) feeding rate model inputs
- Pattern 5: accrueInterest with hard revert on rate cap (no graceful degradation)
- Pattern 6: debtToken.totalSupply() or scaledTotalSupply() used directly as borrows
```

### Audit Checklist
- [ ] Verify blocksPerYear matches the deployment chain's actual block production rate
- [ ] Verify utilization formula correctly handles the specific reserve accounting model
- [ ] Verify withdrawals enforce maximum utilization ratio
- [ ] Verify rate model uses time-weighted or EMA-smoothed inputs, not spot balances
- [ ] Verify accrueInterest handles extreme rates gracefully (cap instead of revert)
- [ ] Verify debtToken totalSupply is properly de-scaled before use in rate calculations
- [ ] Verify AMO update functions are not exploitable via temporary utilization manipulation
- [ ] Verify protocol can still liquidate when external lending pool reserves are exhausted

---

## Real-World Examples

### Known Exploits & Audit Findings
- **Venus Protocol** — 5× interest rate from wrong blocksPerYear (BNB chain) — Code4rena (2023)
- **Fungify** — ERC721 reserves in utilization bricking market — ZachObront (2023)
- **Blend V2** — Utilization >100% via withdrawal without cap — Code4rena (2025)
- **OlympusDAO** — SiloAMO forced to fund reduced rates via utilization manipulation — ZachObront (2023)
- **Exactly Protocol** — Zero avg assets allows lowest-rate borrow at launch — Sherlock (2024)
- **BendDAO** — Incorrect liquidation rate accounting — Code4rena (2024)
- **Moonwell** — accrueInterest revert halting all operations — Code4rena (2023)
- **RAAC** — Prime rate vs optimal rate at kink — Codehawks (2025)

---

## Prevention Guidelines

### Development Best Practices
1. Use per-second rate models instead of per-block for multi-chain deployments
2. If using per-block: make blocksPerYear an immutable constructor parameter, not a constant
3. Audit utilization formula for every asset type — ERC721, ERC1155, rebasing tokens may need different formulas
4. Enforce utilization caps on ALL paths that reduce supply (withdraw, borrow, liquidate)
5. Use TWAP or EMA for rate model inputs instead of spot balances
6. Cap rates gracefully (return max rate) instead of reverting in accrueInterest
7. Validate rate model outputs in integration tests across full utilization range [0, 100%+]

### Testing Requirements
- Unit tests for: Rate calculation at 0%, 50%, optimal, 99%, 100%, >100% utilization
- Integration tests for: Deposit-borrow-withdraw-liquidate cycle with rate consistency checks
- Fuzz tests for: Random sequences of deposits/borrows/withdrawals verifying rate bounds
- Invariant tests for: `utilizationRate <= MAX_UTILIZATION`, `accrueInterest never reverts`

---

## Keywords for Search

`interest rate model`, `utilization rate`, `blocksPerYear`, `baseRatePerBlock`, `multiplierPerBlock`, `kink`, `optimal utilization`, `jump rate`, `compound fork`, `whitepaper rate model`, `accrueInterest`, `getBorrowRate`, `getSupplyRate`, `reserves`, `totalBorrows`, `totalDeposits`, `rate manipulation`, `AMO`, `PI controller`, `EMA`, `time weighted`, `debtToken`, `scaledTotalSupply`, `borrowRateMaxMantissa`, `rate cap`, `utilization cap`, `lending rate`, `borrow rate`, `supply rate`, `interest accrual`, `rate model DoS`

---

## Related Vulnerabilities

- [DB/general/lending-rate-model/](.) — This entry
- [DB/tokens/erc4626/ERC4626_VAULT_VULNERABILITIES.md](../../tokens/erc4626/ERC4626_VAULT_VULNERABILITIES.md) — Vault share accounting (related to lending pool shares)
- [DB/oracle/](../../oracle/) — Oracle price feeds (input to liquidation thresholds affected by rate errors)
