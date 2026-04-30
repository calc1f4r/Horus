---
# Core Classification (Required)
protocol: generic
chain: everychain
category: perpetuals_derivatives
vulnerability_type: perpetuals_mechanism_flaws

# Pattern Identity (Required)
root_cause_family: perpetual_protocol_logic_error
pattern_key: missing_mechanism_validation | perpetual_position_engine | trade_execution | fund_loss_or_insolvency

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - PositionManager
  - LiquidationEngine
  - FundingRateCalculator
  - OrderBook
  - PerpVault
  - PriceOracle
path_keys:
  - missing_partial_liquidation | liquidation | {LiquidationEngine, PositionManager}
  - reversed_or_skewed_funding_rate | funding_settlement | {FundingRateCalculator, PositionManager}
  - order_price_exploitation | order_fill | {OrderBook, PriceOracle}
  - lp_vault_share_inflation | vault_deposit | {PerpVault, LPToken}
  - fee_precision_loss | fee_calculation | {FeeCalculator, PositionManager}
  - position_accounting_desync | position_update | {PositionManager, GlobalState}
  - bad_debt_accumulation | liquidation_failure | {LiquidationEngine, DebtTracker}
  - risk_free_trade_via_delay | order_execution | {OrderBook, DelayedExecution}

# Attack Vector Details (Required)
attack_type: economic_exploit|logical_error
affected_component: position_engine|liquidation_engine|funding_rate|order_execution|vault_accounting

# Technical Primitives (Required)
primitives:
  - funding_rate
  - open_interest
  - mark_price
  - index_price
  - collateral_ratio
  - leverage
  - margin
  - liquidation_threshold
  - position_size
  - unrealized_pnl
  - settlement
  - limit_order
  - stop_loss
  - bad_debt
  - partial_liquidation
  - initial_margin
  - maintenance_margin
  - price_impact

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - liquidate
  - openPosition
  - closePosition
  - fundingRate
  - getCurrentFundingRate
  - openInterest
  - markPrice
  - indexPrice
  - collateralRatio
  - collatRatio
  - leverage
  - marginRequirement
  - initialMargin
  - limitOrder
  - stopLoss
  - settleFunding
  - settlePosition
  - decreasePosition
  - increasePosition
  - executeOrder
  - getPrice
  - priceImpact

# Impact Classification (Required)
severity: critical
impact: fund_loss_or_insolvency
exploitability: 0.75
financial_impact: critical

# Context Tags
tags:
  - defi
  - perpetuals
  - derivatives
  - leverage
  - liquidation
  - funding_rate
  - margin_trading
  - gmx
  - perennial
  - synthetix

# Version Info
language: solidity|rust|vyper
version: all
---

## References & Source Reports

> **For Agents**: Read individual reports for code details. Each section references specific source files.

### Liquidation Mechanism Failures
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| DYAD - No Partial Liquidation | `reports/perpetuals_derivatives_findings/h-02-inability-to-perform-partial-liquidations-allows-huge-positions-to-accrue-b.md` | HIGH | Code4rena |
| DYAD - Ineffective Liquidation | `reports/perpetuals_derivatives_findings/h-05-current-liquidation-mechanism-is-ineffective-and-dangerous.md` | HIGH | Code4rena |
| Self-Liquidation Profitable | `reports/perpetuals_derivatives_findings/self-liquidations-are-profitable-under-certain-collateralization-ratios.md` | MEDIUM | Pashov Audit Group |
| Flash Loan Bypass Self-Liquidation | `reports/perpetuals_derivatives_findings/h-10-flash-loan-protection-mechanism-can-be-bypassed-via-self-liquidations.md` | HIGH | Sherlock |
| No Incentive Small Positions | `reports/perpetuals_derivatives_findings/no-incentive-to-liquidate-small-positions-could-result-in-protocol-going-underwa.md` | MEDIUM | Code4rena |
| Liquidation DoS by Frontrunning | `reports/perpetuals_derivatives_findings/dos-of-full-liquidations-are-possible-by-frontrunning-the-liquidators.md` | MEDIUM | Codehawks |
| Debt-Free Accounts Liquidated | `reports/perpetuals_derivatives_findings/h-03-debt-free-margin-accounts-can-be-liquidated.md` | HIGH | Pashov Audit Group |
| Spot Price Unfair Liquidation | `reports/perpetuals_derivatives_findings/spot-price-manipulation-can-lead-to-unfair-liquidations.md` | HIGH | Sherlock |
| Immediate Position Liquidation | `reports/perpetuals_derivatives_findings/h-04-some-positions-will-get-liquidated-immediately.md` | HIGH | Code4rena |
| Denial of Liquidation | `reports/perpetuals_derivatives_findings/denial-of-liquidation.md` | HIGH | OtterSec |

### Funding Rate Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Perpetual V3 - Skew-Only Funding | `reports/perpetuals_derivatives_findings/h-2-funding-fee-rate-is-calculated-based-only-on-the-oracle-makers-skew-but-appl.md` | HIGH | Sherlock |
| Wrong Token Funding Payments | `reports/perpetuals_derivatives_findings/funding-payments-are-made-in-the-wrong-token.md` | HIGH | Trail of Bits |
| Reversed Funding Rate | `reports/perpetuals_derivatives_findings/reversed-funding-rate.md` | HIGH | OtterSec |
| Funding Paid/Received Mismatch | `reports/perpetuals_derivatives_findings/m-7-funding-paid-funding-received.md` | MEDIUM | Sherlock |
| Extreme Funding Rate Manipulation | `reports/perpetuals_derivatives_findings/h-2-funding-fee-rate-is-calculated-based-only-on-the-oracle-makers-skew-but-appl.md` | HIGH | Sherlock |

### Position & Leverage Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Precision Loss → High Leverage | `reports/perpetuals_derivatives_findings/h-16-due-to-the-loss-of-precision-openposition-will-make-the-users-leverage-high.md` | HIGH | Sherlock |
| Zero Initial Margin via Leverage | `reports/perpetuals_derivatives_findings/h-10-increasing-leverage-can-make-the-position-have-0-initialmargin.md` | HIGH | Sherlock |
| OI Desync After Close | `reports/perpetuals_derivatives_findings/h-12-closing-positions-does-not-decrease-the-pools-entry-price-leading-to-mislea.md` | HIGH | Code4rena |
| Incorrect Next OI for PriceImpact | `reports/perpetuals_derivatives_findings/h-17-incorrect-nextopeninterest-values-set-for-priceimpact.md` | HIGH | Sherlock |
| Collateral Reduced Twice | `reports/perpetuals_derivatives_findings/collateral-is-reduced-twice-when-a-position-is-liquidated-by-a-user-different-fr.md` | HIGH | Zokyo |
| Position Desync Global vs Local | `reports/perpetuals_derivatives_findings/h-2-invalid-oracle-versions-can-cause-desync-of-global-and-local-positions-makin.md` | HIGH | Sherlock |

### Order Execution Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Limit Order Free Look | `reports/perpetuals_derivatives_findings/h-15-limit-orders-can-be-used-to-get-a-free-look-into-the-future.md` | HIGH | Sherlock |
| Riskless Trades via Delay | `reports/perpetuals_derivatives_findings/h-2-riskless-trades-due-to-delay-check.md` | HIGH | Sherlock |
| Stop-Loss Abuse for Risk-Free Trades | `reports/perpetuals_derivatives_findings/h-10-user-can-abuse-tight-stop-losses-and-high-leverage-to-make-risk-free-trades.md` | HIGH | Sherlock |
| Position Size Not Set on Decrease | `reports/perpetuals_derivatives_findings/position-size-is-not-set-when-creating-decrease-orders.md` | MEDIUM | OtterSec |
| Unrestricted Fill Validation | `reports/perpetuals_derivatives_findings/unrestricted-position-fulfillment-due-to-lack-of-initiator-validation.md` | HIGH | Sherlock |
| DoS All Offchain Orders | `reports/perpetuals_derivatives_findings/a-malicious-user-can-dos-all-offchain-orders-making-them-unexecutable-and-leavin.md` | HIGH | Sherlock |
| Stop-Loss Not Marketable | `reports/perpetuals_derivatives_findings/m-7-stop-loss-orders-do-not-become-marketable-orders.md` | MEDIUM | Sherlock |

### Fee & Reward System Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Fee Precision Loss → Liquidation Failure | `reports/perpetuals_derivatives_findings/h-1-fee-precision-loss-disrupts-liquidations-and-causes-loss-of-funds.md` | HIGH | Sherlock |
| Fee Bypass via Reentrancy | `reports/perpetuals_derivatives_findings/h-2-a-malicious-user-can-bypass-limit-order-trading-fees-via-cross-function-re-e.md` | HIGH | Sherlock |
| Reward Computation Wrong | `reports/perpetuals_derivatives_findings/h-01-reward-computation-is-wrong.md` | HIGH | Code4rena |
| Rewards Distributed with No Stakers | `reports/perpetuals_derivatives_findings/rewards-are-calculated-as-distributed-even-if-there-are-no-stakers-locking-the-r.md` | MEDIUM | Sherlock |
| Reward Manipulation in StabilityPool | `reports/perpetuals_derivatives_findings/reward-manipulation-vulnerability-in-stabilitypool.md` | HIGH | Sherlock |
| Fee Loss by Calling Compound | `reports/perpetuals_derivatives_findings/h-06-fee-loss-in-autopxgmx-and-autopxglp-and-reward-loss-in-autopxglp-by-calling.md` | HIGH | Code4rena |
| Reduced Borrow Fee on Reset | `reports/perpetuals_derivatives_findings/reduced-borrow-fee-due-to-resetting-of-accrued-interest.md` | MEDIUM | OtterSec |

### LP Vault Exploitation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| First Depositor Exchange Rate Steal | `reports/perpetuals_derivatives_findings/h-1-first-depositor-can-abuse-exchange-rate-to-steal-funds-from-later-depositors.md` | HIGH | Sherlock |
| ggAVAX Share Inflation | `reports/perpetuals_derivatives_findings/h-05-inflation-of-ggavax-share-price-by-first-depositor.md` | HIGH | Code4rena |
| Vault Inflation Attack | `reports/perpetuals_derivatives_findings/m-5-vault-inflation-attack.md` | MEDIUM | Sherlock |
| Vault Blocked by Malicious Actor | `reports/perpetuals_derivatives_findings/gmxvault-can-be-blocked-by-a-malicious-actor.md` | HIGH | Code4rena |
| KangarooVault Withdraw DoS | `reports/perpetuals_derivatives_findings/h-11-kangaroovault-queuedwithdraw-denial-of-service.md` | HIGH | Sherlock |
| LPPool Insolvency from Short Profit | `reports/perpetuals_derivatives_findings/h-17-lppools-can-become-insolvent-if-shorters-are-in-huge-profits.md` | HIGH | Sherlock |
| Gain Stolen from LMPVault | `reports/perpetuals_derivatives_findings/h-12-gain-from-lmpvault-can-be-stolen.md` | HIGH | Sherlock |

### Bad Debt & Insolvency
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| No Bad Debt Management | `reports/perpetuals_derivatives_findings/protocol-lacks-bad-debt-management-mechanisms-risking-permanent-insolvency.md` | HIGH | Sherlock |
| Persistent Debt Post-Liquidation | `reports/perpetuals_derivatives_findings/persistent-debt-post-liquidation.md` | HIGH | Sherlock |
| Bad Debt from Earnings Accumulation | `reports/perpetuals_derivatives_findings/m-9-profitable-liquidations-and-accumulation-of-bad-debt-due-to-earnings-accumul.md` | MEDIUM | Sherlock |
| Stablecoin Undercollateralized | `reports/perpetuals_derivatives_findings/usds-stablecoin-may-become-undercollateralized.md` | MEDIUM | Sherlock |

---

# Perpetuals & Derivatives Protocol Vulnerabilities — Comprehensive Database

**A Pattern-Matching Guide for Perpetual DEX and Derivatives Protocol Security Audits**

### Overview

Perpetual futures and derivatives protocols are among the most complex DeFi systems, involving position management, margin accounting, funding rates, liquidation engines, order execution, and LP vault mechanics. This entry catalogs recurring vulnerability patterns found across 378 audit reports from protocols including GMX, Perpetual Protocol, Perennial, Synthetix, Parcl, DYAD, and others.

#### Agent Quick View

- Root cause statement: "Perpetuals vulnerabilities exist because position engines, liquidation mechanisms, funding rate calculations, and order execution paths contain logic errors in margin accounting, collateral tracking, fee precision, or timing assumptions that allow fund extraction, insolvency, or unfair liquidations."
- Pattern key: `missing_mechanism_validation | perpetual_position_engine | trade_execution | fund_loss_or_insolvency`
- Interaction scope: `multi_contract`
- Primary affected component(s): `PositionManager, LiquidationEngine, FundingRateCalculator, OrderBook, PerpVault`
- Contracts / modules involved: `PositionManager, LiquidationEngine, FundingRateCalculator, OrderBook, PerpVault, PriceOracle`
- Path keys:
  - `missing_partial_liquidation | liquidation | {LiquidationEngine, PositionManager}`
  - `reversed_or_skewed_funding_rate | funding_settlement | {FundingRateCalculator, PositionManager}`
  - `order_price_exploitation | order_fill | {OrderBook, PriceOracle}`
  - `lp_vault_share_inflation | vault_deposit | {PerpVault, LPToken}`
  - `fee_precision_loss | fee_calculation | {FeeCalculator, PositionManager}`
  - `position_accounting_desync | position_update | {PositionManager, GlobalState}`
  - `bad_debt_accumulation | liquidation_failure | {LiquidationEngine, DebtTracker}`
- High-signal code keywords: `liquidate, openPosition, closePosition, fundingRate, openInterest, collatRatio, initialMargin, executeOrder, settlePosition, priceImpact`
- Typical sink / impact: `fund loss / protocol insolvency / unfair liquidation / risk-free trader profit`
- Validation strength: `strong` (44+ liquidation findings, 54+ position findings, 61+ fee findings across 20+ independent auditors)

#### Contract / Boundary Map

- Entry surface(s): `openPosition()`, `closePosition()`, `liquidate()`, `executeOrder()`, `deposit()`, `withdraw()`, `settleFunding()`
- Contract hop(s): `User -> OrderBook.executeOrder -> PositionManager.increasePosition -> Vault.updateMargin -> Oracle.getPrice`
- Trust boundary crossed: `oracle (external price feed)`, `delayed execution (keeper/relayer)`, `LP vault (share accounting)`, `cross-maker routing`
- Shared state or sync assumption: `global open interest must equal sum of all positions; funding rate must balance longs vs shorts; collateral ratio must be current before liquidation check`

#### Valid Bug Signals

- Signal 1: `liquidate()` function burns entire debt amount with no parameter for partial amount — partial liquidation impossible
- Signal 2: Funding rate calculated from one maker's skew but applied to all positions across all makers
- Signal 3: Limit/stop order can be updated (even by 1 wei) to reset execution block requirement — free look into future prices
- Signal 4: `openPosition()` loses precision in margin calculation such that `initialMargin` rounds to 0 at high leverage
- Signal 5: Open interest is not decremented when positions are closed, causing stale price impact calculations
- Signal 6: LP vault uses `totalSupply == 0` share path without dead shares or minimum deposit — first depositor inflation live

#### False Positive Guards

- Not this bug when: protocol uses a partial liquidation function that accepts an `amount` parameter
- Safe if: funding rate is calculated from aggregate market skew across all makers, not a single maker
- Safe if: order execution requires minimum delay AND update resets the delay timer
- Not this bug when: LP vault implements OpenZeppelin virtual shares (`_decimalsOffset() > 0`)
- Requires attacker control of: order timing, oracle price update timing, or first-deposit front-running

---

## Table of Contents

1. [Liquidation Mechanism Failures](#1-liquidation-mechanism-failures)
2. [Funding Rate Vulnerabilities](#2-funding-rate-vulnerabilities)
3. [Position & Leverage Accounting Bugs](#3-position--leverage-accounting-bugs)
4. [Order Execution Vulnerabilities](#4-order-execution-vulnerabilities)
5. [Fee & Reward System Exploits](#5-fee--reward-system-exploits)
6. [LP Vault Exploitation](#6-lp-vault-exploitation)
7. [Bad Debt & Protocol Insolvency](#7-bad-debt--protocol-insolvency)

---

## 1. Liquidation Mechanism Failures

### Overview

Liquidation engines in perpetual protocols must handle partial liquidations, prevent self-liquidation profit, incentivize small position cleanup, and resist DoS. Failures in any of these areas lead to bad debt accumulation or unfair user losses. Common (44/378 unique findings).

### Root Cause

Liquidation functions either force full position closure (blocking whale liquidation), allow the position holder to profit from their own liquidation, or can be DoS'd by frontrunning.

### Attack Scenario / Path Variants

**Path A: [No Partial Liquidation → Bad Debt Accumulation]**
Path key: `missing_partial_liquidation | liquidation | {LiquidationEngine, PositionManager}`
Entry surface: `liquidate()`
Contracts touched: `LiquidationEngine -> PositionManager -> CollateralVault`
Boundary crossed: `internal (position state)`
1. Whale opens massive position, minting large debt
2. Position becomes undercollateralized
3. Liquidator must match the ENTIRE debt amount to liquidate — no partial option
4. No liquidator has enough capital → position accrues bad debt indefinitely
5. System becomes insolvent

**Path B: [Profitable Self-Liquidation]**
Path key: `profitable_self_liquidation | liquidation | {LiquidationEngine, CollateralManager}`
Entry surface: `selfLiquidate()` or `liquidate(ownPosition)`
Contracts touched: `SelfLiquidate -> PositionManager -> CollateralVault`
Boundary crossed: `internal (collateral accounting)`
1. User opens position at specific collateralization ratio
2. At certain CR thresholds, `debtInCollateralToken` uses total debt not face value
3. Self-liquidation repays debt but returns more collateral than debt value
4. User profits from their own liquidation, extracting protocol value

**Path C: [Liquidation DoS via Frontrunning]**
Path key: `liquidation_dos | liquidation | {LiquidationEngine, Mempool}`
Entry surface: `liquidate()`
Contracts touched: `LiquidationEngine -> PositionManager`
Boundary crossed: `mempool (frontrun)`
1. Liquidator submits liquidation transaction
2. Position owner sees pending liquidation in mempool
3. Owner frontruns with minimal collateral deposit to push CR above threshold
4. Liquidation transaction reverts — `CrTooHigh()`
5. Owner immediately withdraws the added collateral

### Vulnerable Pattern Examples

**Example 1: Full-Amount-Only Liquidation** [HIGH]
> Reference: `reports/perpetuals_derivatives_findings/h-02-inability-to-perform-partial-liquidations-allows-huge-positions-to-accrue-b.md`
```solidity
// ❌ VULNERABLE: Burns entire minted amount — no partial liquidation
function liquidate(uint id, uint to) external isValidDNft(id) isValidDNft(to) {
    uint cr = collatRatio(id);
    if (cr >= MIN_COLLATERIZATION_RATIO) revert CrTooHigh();
    dyad.burn(id, msg.sender, dyad.mintedDyad(address(this), id)); // Full amount!
    // Liquidator must have enough capital to match entire position
}
```

**Example 2: Self-Liquidation Profit via Debt Calculation** [MEDIUM]
> Reference: `reports/perpetuals_derivatives_findings/self-liquidations-are-profitable-under-certain-collateralization-ratios.md`
```solidity
// ❌ VULNERABLE: debtInCollateralToken uses getTotalDebt() not faceValue
function validateSelfLiquidate(State storage state, SelfLiquidateParams calldata params) external view {
    DebtPosition storage debtPosition = state.getDebtPositionByCreditPositionId(params.creditPositionId);
    uint256 assignedCollateral = state.getCreditPositionProRataAssignedCollateral(creditPosition);
    uint256 debtInCollateralToken = state.debtTokenAmountToCollateralTokenAmount(
        debtPosition.getTotalDebt() // Should use faceValue, not total debt
    );
    if (!(assignedCollateral < debtInCollateralToken)) { // Can be exploited
        revert Errors.LOAN_NOT_SELF_LIQUIDATABLE(...);
    }
}
```

**Example 3: Debt-Free Accounts Can Be Liquidated** [HIGH]
> Reference: `reports/perpetuals_derivatives_findings/h-03-debt-free-margin-accounts-can-be-liquidated.md`
```solidity
// ❌ VULNERABLE: Liquidation check doesn't verify position actually has debt
function liquidate(address account) external {
    require(isUnderwater(account), "Not liquidatable");
    // Missing: require(getDebt(account) > 0, "No debt to liquidate");
    // A margin account with 0 debt but temporarily negative mark-to-market can be liquidated
}
```

**Example 4: Spot Price Manipulation for Unfair Liquidation** [HIGH]
> Reference: `reports/perpetuals_derivatives_findings/spot-price-manipulation-can-lead-to-unfair-liquidations.md`
```solidity
// ❌ VULNERABLE: Uses spot last-trade price instead of oracle for liquidation
function getUnderlyingPrice() public view returns (uint256) {
    if (oracleEnabled) return oracle.getPrice();
    return spotMarket.lastPrice(); // Manipulable via order book trades!
}
```

**Example 5: No Incentive for Small Position Liquidation** [MEDIUM]
> Reference: `reports/perpetuals_derivatives_findings/no-incentive-to-liquidate-small-positions-could-result-in-protocol-going-underwa.md`
```solidity
// ❌ VULNERABLE: Liquidation reward doesn't cover gas costs for small positions
function calculateLiquidationReward(uint256 positionSize) public view returns (uint256) {
    return positionSize * LIQUIDATION_BONUS / BASIS_POINTS;
    // For small positions, reward < gas cost → no one liquidates → bad debt
}
```

### Impact Analysis

#### Technical Impact
- Bad debt accrual from unliquidatable positions (8/44 findings)
- System insolvency from accumulated bad debt (6/44 findings)
- Unfair liquidation of healthy positions (5/44 findings)
- Liquidation DoS attacks (4/44 findings)

#### Business Impact
- Protocol insolvency — users cannot withdraw
- Loss of user funds via unfair liquidation
- Emergency governance intervention required

### Secure Implementation

**Fix 1: Partial Liquidation with Amount Parameter**
```solidity
// ✅ SECURE: Allows partial liquidation
function liquidate(uint id, uint to, uint256 amount) external {
    uint cr = collatRatio(id);
    if (cr >= MIN_COLLATERIZATION_RATIO) revert CrTooHigh();
    require(amount > 0 && amount <= mintedDyad(id), "Invalid amount");
    dyad.burn(id, msg.sender, amount);
    // Transfer proportional collateral to liquidator
    uint256 collateralShare = (amount * totalCollateral(id)) / mintedDyad(id);
    _transferCollateral(id, to, collateralShare);
}
```

**Fix 2: Minimum Liquidation Reward**
```solidity
// ✅ SECURE: Ensures minimum reward covers gas costs
function calculateLiquidationReward(uint256 positionSize) public view returns (uint256) {
    uint256 percentReward = positionSize * LIQUIDATION_BONUS / BASIS_POINTS;
    return percentReward > MIN_LIQUIDATION_REWARD ? percentReward : MIN_LIQUIDATION_REWARD;
}
```

### Detection Patterns

#### High-Signal Grep Seeds
```
liquidate
collatRatio
MIN_COLLATERIZATION_RATIO
selfLiquidate
burn(id, msg.sender
mintedDyad
isUnderwater
lastPrice
liquidationBonus
```

#### Contract / Call Graph Signals
```
- liquidate() burns full debt without amount parameter
- Self-liquidation path exists without profit check
- Liquidation reward is purely percentage-based with no minimum
- Price source for liquidation uses spot/last-trade instead of oracle
- No min-delay on collateral changes before liquidation check
```

#### Audit Checklist
- [ ] Can positions be partially liquidated?
- [ ] Is self-liquidation explicitly blocked or guaranteed unprofitable?
- [ ] Do small positions have minimum liquidation incentive?
- [ ] Can liquidation be frontrun/DoS'd?
- [ ] Does liquidation use oracle price, not spot price?

---

## 2. Funding Rate Vulnerabilities

### Overview

Funding rates balance long/short exposure by making the majority side pay the minority. Errors in calculation scope, token denomination, or rate direction lead to protocol losses or adversary-farmed funding. Common (10/378 unique findings).

### Root Cause

Funding rate is calculated from a subset of the market (e.g., one maker's skew) but applied globally, or the rate direction is inverted, or payments are denominated in the wrong token.

### Attack Scenario / Path Variants

**Path A: [Skew-Only Funding → Extreme Rate Manipulation]**
Path key: `reversed_or_skewed_funding_rate | funding_settlement | {FundingRateCalculator, PositionManager}`
Entry surface: `openPosition()` on OracleMaker, then `closePosition()` on SpotHedgeMaker
Contracts touched: `User -> OracleMaker -> FundingRateCalculator -> SpotHedgeMaker`
Boundary crossed: `cross-maker routing`
1. Funding rate is calculated from OracleMaker's skew only
2. Attacker opens large long on OracleMaker → extreme positive funding rate
3. Attacker immediately closes long on SpotHedgeMaker (funding rate unaffected)
4. All long holders across ALL makers now pay extreme funding rate
5. Attacker liquidates the affected positions or profits from short funding

**Path B: [Wrong Token Denomination]**
Path key: `wrong_token_funding | funding_settlement | {ClearingHouse, Vault}`
Entry surface: `_settleUserFundingPayments()`
Contracts touched: `ClearingHouse -> Vault.settlePnL`
Boundary crossed: `internal (token mismatch)`
1. Funding is calculated in base token (e.g., BTC) but should be in UA (accounting token)
2. When BTC price differs from UA, funding payments are wrong magnitude
3. Users receive less/more funding than owed

### Vulnerable Pattern Examples

**Example 1: Funding Rate from Single Maker Applied Globally** [HIGH]
> Reference: `reports/perpetuals_derivatives_findings/h-2-funding-fee-rate-is-calculated-based-only-on-the-oracle-makers-skew-but-appl.md`
```solidity
// ❌ VULNERABLE: Funding rate uses only one maker's skew
function getCurrentFundingRate(uint256 marketId) public view returns (int256) {
    uint256 totalDepositedAmount = uint256(
        _getVault().getSettledMargin(marketId, fundingConfig.basePool) // Only OracleMaker!
    );
    uint256 maxCapacity = FixedPointMathLib.divWad(
        totalDepositedAmount,
        uint256(OracleMaker(fundingConfig.basePool).minMarginRatio())
    );
    // Skew only considers OracleMaker positions, but rate applies to ALL positions
}
```

**Example 2: Reversed Funding Rate Direction** [HIGH]
> Reference: `reports/perpetuals_derivatives_findings/reversed-funding-rate.md`
```rust
// ❌ VULNERABLE: Majority side receives fees instead of paying them
fn get_funding_rate(oi_long: u64, oi_short: u64, oi_total: u64) -> i64 {
    let funding_rate = (oi_long - oi_short) / oi_total / SECONDS_PER_DAY;
    // get_accrued_funding() sends profits to majority side (inverted!)
}
```

**Example 3: Funding Payments in Wrong Token** [HIGH]
> Reference: `reports/perpetuals_derivatives_findings/funding-payments-are-made-in-the-wrong-token.md`
```solidity
// ❌ VULNERABLE: Funding calculated in vBase, settled in UA without conversion
function _settleUserFundingPayments(address user) internal {
    int256 fundingPayments = _calculateFundingPayments(user); // In vBase token
    vault.settlePnL(user, fundingPayments); // Applied directly to UA balance — wrong!
    // Missing: fundingPayments = fundingPayments * vBase.indexPrice() / UA_PRECISION
}
```

### Secure Implementation

**Fix: Aggregate Market Funding Rate**
```solidity
// ✅ SECURE: Funding rate from total market open interest across all makers
function getCurrentFundingRate(uint256 marketId) public view returns (int256) {
    int256 totalLongOI = getTotalLongOpenInterest(marketId);  // All makers
    int256 totalShortOI = getTotalShortOpenInterest(marketId); // All makers
    int256 skew = totalLongOI - totalShortOI;
    return (skew * FUNDING_RATE_FACTOR) / int256(totalLongOI + totalShortOI);
}
```

### Detection Patterns

#### High-Signal Grep Seeds
```
getCurrentFundingRate
fundingRate
fundingFee
settleFunding
basePool
oracleMaker
skew
openInterest
fundingPayments
settlePnL
```

#### Audit Checklist
- [ ] Is funding rate calculated from total market OI or just one maker?
- [ ] Is the funding rate direction correct (majority pays minority)?
- [ ] Are funding payments denominated in the correct token?
- [ ] Can an attacker create extreme funding rates via cross-maker positioning?

---

## 3. Position & Leverage Accounting Bugs

### Overview

Position accounting must stay consistent between local (per-user) and global state. Precision loss in margin calculations, failure to update open interest on close, and collateral double-counting create exploitable inconsistencies. Common (54/378 unique findings).

### Root Cause

Integer division precision loss in margin/leverage calculations, or missing state updates when positions are modified (open interest, entry price, collateral).

### Vulnerable Pattern Examples

**Example 1: Precision Loss Makes Leverage Higher Than Intended** [HIGH]
> Reference: `reports/perpetuals_derivatives_findings/h-16-due-to-the-loss-of-precision-openposition-will-make-the-users-leverage-high.md`
```solidity
// ❌ VULNERABLE: Division before multiplication causes precision loss in margin
function openPosition(uint256 size, uint256 leverage) external {
    uint256 initialMargin = size / leverage; // Precision loss here!
    // For size=100, leverage=33: margin = 100/33 = 3 (should be 3.03)
    // Effective leverage becomes 100/3 = 33.33x (exceeds intended 33x)
    positions[msg.sender].margin = initialMargin;
    positions[msg.sender].size = size;
}
```

**Example 2: Zero Initial Margin at High Leverage** [HIGH]
> Reference: `reports/perpetuals_derivatives_findings/h-10-increasing-leverage-can-make-the-position-have-0-initialmargin.md`
```solidity
// ❌ VULNERABLE: Margin rounds to zero with small size and high leverage
function _calculateMargin(uint256 positionSize, uint256 leverage) internal pure returns (uint256) {
    return positionSize / leverage; // If positionSize < leverage, returns 0!
    // Position with 0 margin → cannot be liquidated → risk-free position
}
```

**Example 3: Open Interest Not Updated on Close** [HIGH]
> Reference: `reports/perpetuals_derivatives_findings/h-12-closing-positions-does-not-decrease-the-pools-entry-price-leading-to-mislea.md`
```solidity
// ❌ VULNERABLE: Closing position doesn't update pool's entry price or OI
function closePosition(uint256 positionId) external {
    Position storage pos = positions[positionId];
    _settlePnL(pos);
    _transferCollateral(pos.owner, pos.margin);
    delete positions[positionId];
    // Missing: pool.openInterest -= pos.size;
    // Missing: pool.entryPrice recalculation
    // Result: stale OI → wrong price impact for new positions
}
```

**Example 4: Global vs Local Position Desync** [HIGH]
> Reference: `reports/perpetuals_derivatives_findings/h-2-invalid-oracle-versions-can-cause-desync-of-global-and-local-positions-makin.md`
```solidity
// ❌ VULNERABLE: Invalid oracle version updates global but not local position
function settle(address account) external {
    // Global position updated even when oracle version is invalid
    _updateGlobalPosition(latestVersion);
    // Local position NOT updated → global and local diverge
    if (!isValidOracleVersion(latestVersion)) return; // Exits without local sync
    _updateLocalPosition(account, latestVersion);
}
```

### Secure Implementation

**Fix: Multiply Before Divide for Margin Precision**
```solidity
// ✅ SECURE: Scale up before division to maintain precision
function _calculateMargin(uint256 positionSize, uint256 leverage) internal pure returns (uint256) {
    require(leverage > 0, "Zero leverage");
    uint256 margin = (positionSize * PRECISION) / (leverage * PRECISION / 1);
    require(margin > 0, "Margin too small");
    return margin;
}
```

### Detection Patterns

#### High-Signal Grep Seeds
```
openPosition
closePosition
increasePosition
decreasePosition
initialMargin
openInterest
entryPrice
globalPosition
localPosition
settlePosition
priceImpact
```

#### Audit Checklist
- [ ] Does margin calculation use multiply-before-divide?
- [ ] Can margin round to zero at maximum leverage?
- [ ] Is open interest decremented on position close?
- [ ] Are global and local position states always synced?
- [ ] Is entry price recalculated on partial close?

---

## 4. Order Execution Vulnerabilities

### Overview

Order execution in perpetuals involves delayed execution, off-chain price feeds, and keeper-based filling. Timing gaps between order placement and execution create free-look arbitrage opportunities. Common (23/378 unique findings).

### Root Cause

Order execution uses future prices, but order updates reset the execution window, allowing users to repeatedly delay execution until prices are favorable.

### Vulnerable Pattern Examples

**Example 1: Limit Order Free-Look via Update** [HIGH]
> Reference: `reports/perpetuals_derivatives_findings/h-15-limit-orders-can-be-used-to-get-a-free-look-into-the-future.md`
```solidity
// ❌ VULNERABLE: Order update resets execution block requirement
function updateOrder(bytes32 orderId, uint256 newSize) external {
    Order storage order = orders[orderId];
    require(order.owner == msg.sender);
    order.size = newSize; // Even +/- 1 wei change counts
    order.updatedBlock = block.number; // Resets execution eligibility!
    // Attacker sees future price → updates by 1 wei → delays execution → repeat
}
```

**Example 2: Riskless Trades via Delay Check Bypass** [HIGH]
> Reference: `reports/perpetuals_derivatives_findings/h-2-riskless-trades-due-to-delay-check.md`
```solidity
// ❌ VULNERABLE: Delay between order and execution lets user cancel if unfavorable
function executeOrder(bytes32 orderId, bytes calldata oracleData) external {
    Order storage order = orders[orderId];
    require(block.number > order.createdBlock + DELAY, "Too early");
    // User can cancel order at block order.createdBlock + DELAY - 1
    // They see the price at createdBlock + DELAY and decide
    // Profitable → let execute. Unprofitable → cancel. = Risk-free trade
}
```

**Example 3: Stop-Loss Abuse for Risk-Free Trades** [HIGH]
> Reference: `reports/perpetuals_derivatives_findings/h-10-user-can-abuse-tight-stop-losses-and-high-leverage-to-make-risk-free-trades.md`
```solidity
// ❌ VULNERABLE: Tight stop-loss with high leverage → capped downside, unlimited upside
// User opens 100x leveraged position with stop-loss 0.1% below entry
// If price moves up: profit = 100x * price_change (large)
// If price moves down: stop-loss triggers, loss capped at 0.1% * position
// Result: asymmetric payoff favoring attacker at protocol's expense
```

### Secure Implementation

**Fix: Update Resets Delay Timer**
```solidity
// ✅ SECURE: Order update restarts the full delay, no free look
function updateOrder(bytes32 orderId, uint256 newSize) external {
    Order storage order = orders[orderId];
    require(order.owner == msg.sender);
    require(block.number >= order.updatedBlock + MIN_UPDATE_DELAY, "Update too fast");
    order.size = newSize;
    order.updatedBlock = block.number;
    order.executableAfter = block.number + EXECUTION_DELAY; // Full delay reset
}
```

### Detection Patterns

#### High-Signal Grep Seeds
```
updateOrder
executeOrder
limitOrder
stopLoss
updatedBlock
createdBlock
EXECUTION_DELAY
cancelOrder
oracleData
minOracleBlockNumber
```

#### Audit Checklist
- [ ] Does order update reset execution eligibility window?
- [ ] Is there minimum delay between order updates?
- [ ] Can users cancel orders after seeing execution price?
- [ ] Are stop-loss + high leverage combinations rate-limited?

---

## 5. Fee & Reward System Exploits

### Overview

Fee precision loss, reward distribution timing, and token denomination errors cause direct fund losses or enable fee bypass. Common (61/378 unique findings).

### Vulnerable Pattern Examples

**Example 1: Fee Precision Loss Blocks Liquidations** [HIGH]
> Reference: `reports/perpetuals_derivatives_findings/h-1-fee-precision-loss-disrupts-liquidations-and-causes-loss-of-funds.md`
```vyper
# ❌ VULNERABLE: Two sources of precision loss in fee calculation
@internal
def apply(x: uint256, numerator: uint256, denominator: uint256) -> uint256:
    return (x * numerator) / DENOM / denominator  # Double division = compounded loss
    # For small numerators per block, fee can round to 0 for extended periods
    # Liquidation depends on accrued fees → delayed liquidation → bad debt
```

**Example 2: Rewards Distributed to Zero Stakers** [MEDIUM]
> Reference: `reports/perpetuals_derivatives_findings/rewards-are-calculated-as-distributed-even-if-there-are-no-stakers-locking-the-r.md`
```solidity
// ❌ VULNERABLE: Rewards counted as distributed even when totalStaked == 0
function distributeRewards(uint256 amount) external {
    rewardPerShare += (amount * PRECISION) / totalStaked; // Division by zero or lost rewards
    // If totalStaked == 0, rewards are lost permanently
}
```

**Example 3: Fee Bypass via Cross-Function Reentrancy** [HIGH]
> Reference: `reports/perpetuals_derivatives_findings/h-2-a-malicious-user-can-bypass-limit-order-trading-fees-via-cross-function-re-e.md`
```solidity
// ❌ VULNERABLE: Limit order fee can be bypassed via reentrancy from another function
function executeLimitOrder(uint256 orderId) external {
    Order storage order = orders[orderId];
    _executeSwap(order.tokenIn, order.tokenOut, order.amount);
    // Fee charged AFTER execution — reentrancy during _executeSwap can modify state
    _chargeFee(order.amount, LIMIT_ORDER_FEE);
}
```

### Secure Implementation

**Fix: Scale Up Before Fee Division**
```solidity
// ✅ SECURE: Single division with scaled numerator
function applyFee(uint256 amount, uint256 ratePerSecond, uint256 elapsed) internal pure returns (uint256) {
    return (amount * ratePerSecond * elapsed) / PRECISION; // One division, no compounded loss
}
```

### Detection Patterns

#### High-Signal Grep Seeds
```
rewardPerShare
distributeRewards
totalStaked
chargeFee
borrowingFee
fundingFee
DENOM
PRECISION
accruedFees
feeRate
```

#### Audit Checklist
- [ ] Do fee calculations have sufficient precision (multiply before divide)?
- [ ] Are rewards handled correctly when totalStaked == 0?
- [ ] Are fee charges applied before state changes (not after)?
- [ ] Is reentrancy guarded on fee-sensitive functions?

---

## 6. LP Vault Exploitation

### Overview

Perpetual protocol LP vaults (for providing trading liquidity) suffer from classic vault attacks plus perp-specific issues like insolvent pools from opposite-side profits. Common (56/378 unique findings).

### Vulnerable Pattern Examples

**Example 1: First Depositor Exchange Rate Theft** [HIGH]
> Reference: `reports/perpetuals_derivatives_findings/h-1-first-depositor-can-abuse-exchange-rate-to-steal-funds-from-later-depositors.md`
```solidity
// ❌ VULNERABLE: Classic first-depositor inflation in perp LP vault
function deposit(uint256 assets) external returns (uint256 shares) {
    if (totalSupply() == 0) {
        shares = assets; // 1:1 first deposit
    } else {
        shares = assets * totalSupply() / totalAssets();
    }
    _mint(msg.sender, shares);
    // Attacker: deposit 1 wei → donate large amount → subsequent depositors get 0 shares
}
```

**Example 2: LP Pool Insolvency from Short Profits** [HIGH]
> Reference: `reports/perpetuals_derivatives_findings/h-17-lppools-can-become-insolvent-if-shorters-are-in-huge-profits.md`
```solidity
// ❌ VULNERABLE: LP pool doesn't cap short trader PnL against pool solvency
function settlePnL(address trader) external {
    int256 pnl = calculatePnL(trader);
    if (pnl > 0) {
        // Pool pays trader — but what if pnl > pool.totalAssets?
        pool.transfer(trader, uint256(pnl)); // Pool can become insolvent!
    }
}
```

**Example 3: Vault Withdrawal DoS** [HIGH]
> Reference: `reports/perpetuals_derivatives_findings/h-11-kangaroovault-queuedwithdraw-denial-of-service.md`
```solidity
// ❌ VULNERABLE: Queued withdrawal can be blocked by manipulating vault state
function processWithdrawals() external {
    for (uint i = 0; i < withdrawalQueue.length; i++) {
        // If any withdrawal in queue reverts, all subsequent are blocked
        _processWithdrawal(withdrawalQueue[i]); // No try-catch
    }
}
```

### Secure Implementation

**Fix: Cap Trader PnL Against Pool Solvency**
```solidity
// ✅ SECURE: Trader PnL capped at available pool assets
function settlePnL(address trader) external {
    int256 pnl = calculatePnL(trader);
    if (pnl > 0) {
        uint256 maxPayout = pool.totalAssets() * MAX_PNL_PAYOUT_RATIO / BASIS_POINTS;
        uint256 payout = uint256(pnl) > maxPayout ? maxPayout : uint256(pnl);
        pool.transfer(trader, payout);
    }
}
```

### Detection Patterns

#### High-Signal Grep Seeds
```
totalSupply() == 0
totalAssets
deposit
withdraw
processWithdrawals
settlePnL
queuedWithdraw
exchange_rate
shares
inflat
```

#### Audit Checklist
- [ ] Does LP vault use virtual shares or minimum first deposit?
- [ ] Is trader PnL capped against pool solvency?
- [ ] Can withdrawal queues be DoS'd by a single reverting withdrawal?
- [ ] Does vault NAV accurately reflect unrealized PnL of open positions?

---

## 7. Bad Debt & Protocol Insolvency

### Overview

When liquidations fail (any of the reasons in Section 1) or losses exceed collateral, bad debt accumulates. Protocols without explicit bad debt socialization or insurance mechanisms risk permanent insolvency. Common (10/378 unique findings).

### Vulnerable Pattern Examples

**Example 1: No Bad Debt Management Mechanism** [HIGH]
> Reference: `reports/perpetuals_derivatives_findings/protocol-lacks-bad-debt-management-mechanisms-risking-permanent-insolvency.md`
```solidity
// ❌ VULNERABLE: No path to clear bad debt — accrues indefinitely
function liquidate(address account) external {
    int256 remainingDebt = getDebt(account) - getCollateral(account);
    if (remainingDebt > 0) {
        // Bad debt exists but nowhere to assign it
        // No insurance fund, no socialization, no write-off mechanism
        // Protocol is now permanently insolvent by this amount
    }
}
```

**Example 2: Persistent Debt After Liquidation** [HIGH]
> Reference: `reports/perpetuals_derivatives_findings/persistent-debt-post-liquidation.md`
```solidity
// ❌ VULNERABLE: Liquidation doesn't fully clear debt when collateral < debt
function liquidate(uint256 positionId) external {
    Position storage pos = positions[positionId];
    uint256 collateral = pos.collateral;
    uint256 debt = pos.debt;
    _transferCollateral(msg.sender, collateral); // All collateral to liquidator
    pos.collateral = 0;
    pos.debt = debt - collateral; // Remaining debt persists — who pays?
    // This debt fragment may never be cleared
}
```

### Secure Implementation

**Fix: Insurance Fund + Bad Debt Socialization**
```solidity
// ✅ SECURE: Bad debt cleared via insurance fund, then socialized
function liquidate(address account) external {
    int256 remainingDebt = getDebt(account) - getCollateral(account);
    _transferCollateral(msg.sender, getCollateral(account));
    if (remainingDebt > 0) {
        uint256 badDebt = uint256(remainingDebt);
        if (insuranceFund.balance() >= badDebt) {
            insuranceFund.coverBadDebt(badDebt);
        } else {
            uint256 covered = insuranceFund.balance();
            insuranceFund.coverBadDebt(covered);
            _socializeLoss(badDebt - covered); // Spread across all LPs
        }
    }
    _clearPosition(account);
}
```

### Detection Patterns

#### High-Signal Grep Seeds
```
badDebt
insuranceFund
socialize
insolvent
undercollateralized
remainingDebt
clearPosition
writeOff
```

#### Audit Checklist
- [ ] Does protocol have insurance fund for bad debt?
- [ ] Is bad debt socialized across LPs when insurance is exhausted?
- [ ] Are all debt positions fully cleared after liquidation?
- [ ] Is there a cap on maximum loss per position to limit bad debt?

---

## Keywords for Search

`perpetuals`, `derivatives`, `funding rate`, `liquidation`, `partial liquidation`, `self-liquidation`, `open interest`, `mark price`, `index price`, `leverage`, `margin`, `initial margin`, `maintenance margin`, `position accounting`, `limit order`, `stop loss`, `free look`, `risk-free trade`, `bad debt`, `insolvency`, `LP vault`, `exchange rate`, `first depositor`, `fee precision`, `reward distribution`, `collateral ratio`, `price impact`, `GMX`, `Perpetual Protocol`, `Perennial`, `Synthetix`, `perpetual DEX`, `derivatives protocol`

## Related Vulnerabilities

- `DB/tokens/erc4626/ERC4626_VAULT_VULNERABILITIES.md` — LP vault inflation attacks
- `DB/oracle/pyth/PYTH_ORACLE_VULNERABILITIES.md` — Oracle price feed issues
- `DB/general/precision/` — Precision loss patterns
- `DB/general/flash-loan/` — Flash loan amplification of liquidation attacks
