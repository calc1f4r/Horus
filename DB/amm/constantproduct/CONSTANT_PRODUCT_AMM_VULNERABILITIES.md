---
# Core Classification (Required)
protocol: generic
chain: everychain
category: amm
vulnerability_type: constant_product_amm_integration

# Attack Vector Details (Required)
attack_type: economic_exploit|price_manipulation|liquidity_attack|dos
affected_component: liquidity_pool|swap_router|price_feed|reserves

# AMM-Specific Fields
amm_type: constant_product
amm_formula: x*y=k
amm_attack_vector: slippage|sandwich|first_depositor|reserve_manipulation|spot_price|deadline

# Technical Primitives (Required)
primitives:
  - constant_product
  - liquidity_provision
  - swap_execution
  - price_calculation
  - reserves
  - k_invariant
  - slippage_protection
  - deadline_check
  - minimum_liquidity
  - LP_tokens
  - getReserves
  - slot0
  - sqrtPriceX96
  - TWAP
  - spot_price

# Impact Classification (Required)
severity: critical
impact: fund_loss|price_manipulation|dos|unfair_exchange
exploitability: 0.75
financial_impact: high

# Context Tags
tags:
  - defi
  - dex
  - amm
  - uniswap
  - liquidity
  - swap
  - mev
  - sandwich_attack
  - front_running

# Version Info
language: solidity|rust|move
version: all

# Pattern Identity (Required)
root_cause_family: logic_error
pattern_key: logic_error | liquidity_pool | constant_product_amm_integration

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: multi_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - LP_tokens
  - TWAP
  - _addLiquidity
  - _deployToken
  - _executeTrade
  - _existsPairPool
  - _findSlice
  - _getSwapAmt
  - _getTimeWeightedPrimaryBalance
  - _graduate
  - _tokenToPodLp
  - _transfer
  - _unstakeAndExitPool
  - addDividend
  - addLiquidity
  - addQuote
  - addTradeFee
  - approve
  - balanceOf
  - block.timestamp
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### First Depositor / Inflation Attacks
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Caviar - First Depositor Attack | `reports/constantproduct/h-03-first-depositor-can-break-minting-of-shares.md` | HIGH | Code4rena |
| Caviar - First Depositor Variant | `reports/constantproduct/h-04-first-depositor-can-break-minting-of-shares.md` | HIGH | Code4rena |
| Initial Mint Front-Run Inflation | `reports/constantproduct/initial-mint-front-run-inflation-attack.md` | HIGH | MixBytes |
| 1 Wei Donation DOS | `reports/constantproduct/c-03-blocking-the-initial-liquidity-seed-with-a-1-wei-donation.md` | CRITICAL | Pashov Audit Group |
| Hijack Pool by Burning LP | `reports/constantproduct/h-10-hijack-token-pool-by-burning-liquidity-token.md` | HIGH | Code4rena |

### Slippage Protection Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Missing Slippage Checks | `reports/constantproduct/missing-slippage-checks.md` | HIGH | OtterSec |
| No Slippage Protection | `reports/constantproduct/no-slippage-protection.md` | HIGH | Various |
| Missing Slippage on SyncSwap | `reports/constantproduct/missing-slippage-protection-on-syncswap-swaps.md` | MEDIUM | Various |
| Slippage Higher Than Expected | `reports/constantproduct/slippage-higher-than-expected-in-curveadapterexecuteswapexactinput-and-feedistri.md` | MEDIUM | Various |
| Slippage Vulnerability Primex | `reports/constantproduct/slippage-vulnerability-in-primex-protocol-for-swap-and-spot-trade-positions.md` | HIGH | Various |
| Zero amountOutMin MEV Exploit | `reports/constantproduct/exploiting-zero-amountoutmin-in-dexwrappers-for-mev-attacks.md` | HIGH | Various |

### Sandwich & MEV Attacks
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Sandwich Attack on Withdrawal | `reports/constantproduct/sandwich-attack-on-user-withdrawal.md` | HIGH | MixBytes |
| Sandwich Attacks and Price Manipulation | `reports/constantproduct/sandwich-attacks-and-price-manipulation.md` | HIGH | Various |
| RELP Sandwich Attack | `reports/constantproduct/m-08-relpcontractrelp-is-susceptible-to-sandwich-attack-due-to-user-control-over.md` | MEDIUM | Sherlock |
| UniswapHelper Sandwich | `reports/constantproduct/m-14-uniswaphelperbuyflanandburn-is-a-subject-to-sandwich-attacks.md` | MEDIUM | Various |

### Spot Price Manipulation (slot0)
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| slot0 Manipulation | `reports/constantproduct/h-3-usage-of-slot0-is-extremely-easy-to-manipulate.md` | HIGH | Sherlock |
| Spot Price in CoreSaltFeed | `reports/constantproduct/h-03-the-use-of-spot-price-by-coresaltyfeed-can-lead-to-price-manipulation-and-u.md` | HIGH | Various |
| Uniswap Liquidity Manipulation | `reports/constantproduct/h-1-attacker-can-profit-by-manipulating-uniswap-liquidity.md` | HIGH | Sherlock |
| Intra-Transaction Oracle Tampering | `reports/constantproduct/intra-transaction-oracle-tampering-possible-with-lp-pricing-using-flashloans.md` | HIGH | Spearbit |

### Deadline Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Missing Deadline Checks | `reports/constantproduct/m-01-missing-deadline-checks-allow-pending-transactions-to-be-maliciously-execut.md` | MEDIUM | Code4rena |

### Reserve Manipulation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| LP Reserve Manipulation | `reports/constantproduct/h-06-lps-of-vaderpoolv2-can-manipulate-pool-reserves-to-extract-funds-from-the-r.md` | HIGH | Code4rena |
| Token Reserves Per LP Manipulation | `reports/constantproduct/m-08-zeroswapuniswapv2pairsol-token-reserves-per-lp-token-can-be-manipulated-due.md` | MEDIUM | Code4rena |
| Pair Price Direct Transfer Manipulation | `reports/constantproduct/m-05-pair-price-may-be-manipulated-by-direct-transfers.md` | MEDIUM | Various |

### Fee Calculation Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Fee Calculation Steal Reserves | `reports/constantproduct/h-05-attacker-can-steal-entire-reserves-by-abusing-fee-calculation.md` | HIGH | Code4rena |
| Fee-In Always Beneficial | `reports/constantproduct/m-01-choosing-feein-is-always-more-beneficial-than-feeout.md` | MEDIUM | Various |

### LP Token Calculation Issues
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Flawed LP Token Calculation | `reports/constantproduct/flawed-calculation-of-lp-tokens-in-liquidity-swap-pbc.md` | HIGH | Various |
| Fewer LP Tokens Imbalanced Pool | `reports/constantproduct/h-4-fewer-than-expected-lp-tokens-if-the-pool-is-imbalanced-during-vault-restora.md` | HIGH | Various |
| LP Tokens Never Burned | `reports/constantproduct/the-lp-tokens-are-never-burned-by-the-stream-pool-contract.md` | HIGH | Various |
| Oracle Decimal Mismatch | `reports/constantproduct/h-5-univ2lporacle-will-malfunction-if-token0-or-token1s-decimals-18.md` | HIGH | Sherlock |

### Callback & Reentrancy Attacks
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Unrestricted Mint Callback | `reports/constantproduct/c-04-draining-approved-tokens-by-unrestricted-uniswapv3mintcallback.md` | CRITICAL | Pashov Audit Group |
| Reentrancy Fund Freeze | `reports/constantproduct/redeemnative-reentrancy-enables-permanent-fund-freeze-systemic-misaccounting-and.md` | HIGH | MixBytes |
| Flash Loan Reentrancy Lock | `reports/constantproduct/m-04-berachain-users-cannot-use-flashloans-from-uni-v2-wberaberabottoken-pool.md` | MEDIUM | Shieldify |
| Nested Swap Bypass | `reports/constantproduct/incorrect-calculation-of-the-received-swap-amount-allows-guardians-to-bypass-the.md` | HIGH | Spearbit |

### Factory & Pool Creation Attacks
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Deterministic Address DoS | `reports/constantproduct/h-02-lambofactory-can-be-permanently-dos-ed-due-to-createpair-call-reversal.md` | HIGH | Code4rena |
| False Pool Detection | `reports/constantproduct/m-8-false-pool-exists-detection-via-balanceof-leads-to-broken-swap-paths.md` | MEDIUM | Sherlock |
| Wrong Init Code Hash | `reports/constantproduct/m-04-wrong-init-code-hash.md` | MEDIUM | Code4rena |
| Pool Initialization Front-Run | `reports/constantproduct/m-01-routergetorcreatepoolandaddliquidity-can-be-frontrunned-which-leads-to-pric.md` | MEDIUM | Code4rena |
| Griefing Pool Creation | `reports/constantproduct/m-05-griefing-attack-on-genesispoolmanagersoldepositnativetoken-leading-to-denia.md` | MEDIUM | Code4rena |
| Incorrect Pool Init | `reports/constantproduct/risk-of-incorrect-pool-initialization.md` | HIGH | OtterSec |

### Decimal & Math Calculation Issues
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| LP Token Decimal Mismatch | `reports/constantproduct/h-6-curve-vault-will-undervalue-or-overvalue-the-lp-pool-tokens-if-it-comprises-.md` | HIGH | Sherlock |
| Missing Power of 10 | `reports/constantproduct/h-3-ctokenoraclesolgetcerc20price-contains-critical-math-error.md` | HIGH | Sherlock |
| Wrong Output Amount Formula | `reports/constantproduct/h-02-incorrect-output-amount-calculation-for-trader-joe-v1-pools.md` | HIGH | Code4rena |
| Incorrect Deposit Calculations | `reports/constantproduct/m-07-incorrect-calculations-in-deposit-function-in-tokenisablerangesol-can-make-.md` | MEDIUM | Code4rena |

### Liquidity Migration & Upgrade Attacks
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Migration DoS via Balance Manipulation | `reports/constantproduct/m-02-attacker-can-dos-liquidity-migration-in-liquiditymanagersol.md` | MEDIUM | Code4rena |
| Wrong Ownership Assumption | `reports/constantproduct/h-09-relpcontract-wrongfully-assumes-protocol-owns-all-of-the-liquidity-in-the-u.md` | HIGH | Code4rena |

### Flash Loan Graduation Attacks
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Flash Loan Graduation Bypass | `reports/constantproduct/m-04-launched-tokens-are-vulnerable-to-flashloan-attacks-forcing-premature-gradu.md` | MEDIUM | Code4rena |
| Flash Loan Price Manipulation | `reports/constantproduct/h-05-flash-loan-price-manipulation-in-purchasepyroflan.md` | HIGH | Various |

### Protocol-Specific Issues
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Dividend Gaming | `reports/constantproduct/h-08-dividend-reward-can-be-gamed.md` | HIGH | Code4rena |
| Constant Sum AMM Arbitrage | `reports/constantproduct/unlimited-arbitrage-in-ccfrax1to1amm.md` | HIGH | TrailOfBits |
| IchiVault slot0 Manipulation | `reports/constantproduct/h-10-ichilporacle-is-extemely-easy-to-manipulate-due-to-how-ichivault-calculates.md` | HIGH | Sherlock |
| Imbalanced Pool Reinvest | `reports/constantproduct/h-5-reinvest-will-return-sub-optimal-return-if-the-pool-is-imbalanced.md` | HIGH | Sherlock |
| Thin Liquidity Fee Exploit | `reports/constantproduct/m-7-attacker-can-exploit-thin-liquidity-in-xyk-pool-to-save-on-fees.md` | MEDIUM | Sherlock |

### Imbalanced Liquidity Addition Exploitation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| LP Pair Overpayment via Sandwich | `reports/constant_product/overpayment-of-one-side-of-lp-pair-onjoinpool-due-to-sandwich-or-user-error.md` | HIGH | Spearbit |
| LP Fund Loss on Add Liquidity | `reports/constant_product/h-02-liquidity-providers-may-lose-funds-when-adding-liquidity.md` | HIGH | Code4rena |
| Imbalanced Pool Manipulation | `reports/constant_product/m-5-uniswap-pool-price-can-be-manipulated-so-stnxm-adds-liquidity-to-a-super-imb.md` | MEDIUM | Sherlock |

### Rebasing Token Integration Issues
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Aave Share Token Rebasing | `reports/constant_product/h-05-aaves-share-tokens-are-rebasing-breaking-current-strategy-code.md` | HIGH | Code4rena |

### Impermanent Loss Protection Abuse
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| IL Protection Reserve Drain | `reports/constant_product/h-06-paying-il-protection-for-all-vaderpool-pairs-allows-the-reserve-to-be-drain.md` | HIGH | Code4rena |

### Protocol Invariant Breaking
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Invariant Broken via Valid Txns | `reports/constant_product/protocols-invariants-can-be-broken.md` | HIGH | Cyfrin |
| Well Function Logic Ignored | `reports/constant_product/ignoring-the-well-function-logic-for-a-ratio-of-reserves-calculation.md` | MEDIUM | Codehawks |

### DEX Swap Slippage Accounting Issues
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Vault Slippage Not Accounted | `reports/constant_product/rebalancevaultsassets-incorrectly-accounts-vaults-depositedusdc.md` | MEDIUM | Codehawks |
| Incorrect Swap Amount Calculation | `reports/constant_product/incorrect-swap-amount-in-creditdelegationbranchsettlevaultsdebt-improperly-infla.md` | MEDIUM | Codehawks |

### Leftover Token Accumulation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Autocompound Leftover pTKNs | `reports/constant_product/h-4-autocompoundingpodlp-_pairedlptokentopodlp-does-not-correctly-handle-leftove.md` | HIGH | Sherlock |
| ReLP Dust Tokens Stuck | `reports/constant_product/m-16-inaccurate-swap-amount-calculation-in-relp-leads-to-stuck-tokens-and-lost-l.md` | MEDIUM | Code4rena |

### WETH/ETH Pool Mismatch
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| WETH Asset with ETH Pool | `reports/constant_product/m-22-setup-with-asset-weth-and-a-curve-pool-that-contains-native-eth-will-lead-t.md` | MEDIUM | Sherlock |

### Exit Type Confusion
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Single-Sided Emergency Exit | `reports/constant_product/h-9-single-sided-instead-of-proportional-exit-is-performed-during-emergency-exit.md` | HIGH | Sherlock |
| Remove Liquidity Token Tracking | `reports/constant_product/h-7-tokens-received-from-curves-remove_liquidity-should-be-added-to-the-assets-l.md` | HIGH | Sherlock |

### Type Casting & Integer Overflow Issues
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Unchecked Type Casting u64 to i64 | `reports/constant_product/unchecked-type-casting.md` | HIGH | OtterSec |
| DoS via uint8 Array Index Overflow | `reports/constant_product/denial-of-service-conditions-caused-by-the-use-of-more-than-256-slices.md` | HIGH | TrailOfBits |

### Spot Price Abuse in Protocol Swaps
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| SponsorVault Sandwich Attack | `reports/constant_product/use-of-spot-price-in-sponsorvault-leads-to-sandwich-attack.md` | HIGH | Spearbit |
| Spot DEX Price Repay Attack | `reports/constant_product/use-of-spot-dex-price-when-repay-portal-debt-leads-to-sandwich-attacks.md` | HIGH | Various |

### LP Token Burn/Hijack Attacks
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Hijack Pool by Burning LP | `reports/constant_product/h-10-hijack-token-pool-by-burning-liquidity-token.md` | HIGH | Code4rena |
| LP Tokens Never Burned | `reports/constant_product/the-lp-tokens-are-never-burned-by-the-stream-pool-contract.md` | HIGH | TrailOfBits |

### Constant Sum AMM Arbitrage
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Unlimited Arbitrage 1:1 AMM | `reports/constant_product/unlimited-arbitrage-in-ccfrax1to1amm.md` | HIGH | TrailOfBits |

### State Accounting Discrepancies
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| ohmMinted vs ohmRemoved Tracking | `reports/constant_product/m-8-singlesidedliquidityvaultwithdraw-will-decreases-ohmminted-which-will-make-t.md` | MEDIUM | Sherlock |
| Parameter Misordering in Fee Collection | `reports/constant_product/h-05-parameter-misordering-in-fee-collection-function-causes-denial-of-service-a.md` | HIGH | Code4rena |

### Incorrect Liquidity Ownership Assumptions
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Assumes Protocol Owns All LP | `reports/constant_product/h-09-relpcontract-wrongfully-assumes-protocol-owns-all-of-the-liquidity-in-the-u.md` | HIGH | Code4rena |

### Dividend/Reward Gaming
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Dividend Reward Gaming via Small Trades | `reports/constant_product/h-08-dividend-reward-can-be-gamed.md` | HIGH | Code4rena |

### Missing Account Validation (Solana-Specific)
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Missing TokenAccount Checks | `reports/constant_product/missing-tokenaccount-checks.md` | HIGH | OtterSec |

---

# Constant Product AMM Integration Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for x*y=k AMM Security Audits**

---

## Table of Contents

1. [First Depositor / Inflation Attacks](#1-first-depositor--inflation-attacks)
2. [Slippage Protection Vulnerabilities](#2-slippage-protection-vulnerabilities)
3. [Sandwich & MEV Attacks](#3-sandwich--mev-attacks)
4. [Spot Price Manipulation (slot0)](#4-spot-price-manipulation-slot0)
5. [Deadline Vulnerabilities](#5-deadline-vulnerabilities)
6. [Reserve Manipulation Attacks](#6-reserve-manipulation-attacks)
7. [LP Token Calculation Issues](#7-lp-token-calculation-issues)
8. [Callback & Reentrancy Attacks](#8-callback--reentrancy-attacks)
9. [Factory & Pool Creation Attacks](#9-factory--pool-creation-attacks)
10. [Decimal & Math Calculation Issues](#10-decimal--math-calculation-issues)
11. [Liquidity Migration & Protocol Upgrade Attacks](#11-liquidity-migration--protocol-upgrade-attacks)
12. [Flash Loan-Based Graduation/Threshold Manipulation](#12-flash-loan-based-graduationthreshold-manipulation)
13. [Imbalanced Liquidity Addition Exploitation](#13-imbalanced-liquidity-addition-exploitation)
14. [Rebasing Token Integration Issues](#14-rebasing-token-integration-issues)
15. [Impermanent Loss Protection Abuse](#15-impermanent-loss-protection-abuse)
16. [Protocol Invariant Breaking](#16-protocol-invariant-breaking)
17. [DEX Swap Slippage Accounting Discrepancies](#17-dex-swap-slippage-accounting-discrepancies)
18. [Leftover Token Accumulation in Autocompounding](#18-leftover-token-accumulation-in-autocompounding)
19. [WETH/ETH Pool Asset Mismatch](#19-wetheth-pool-asset-mismatch)
20. [Single-Sided vs Proportional Exit Confusion](#20-single-sided-vs-proportional-exit-confusion)
21. [Type Casting & Integer Overflow Issues](#21-type-casting--integer-overflow-issues)
22. [Spot Price Abuse in Protocol Swaps](#22-spot-price-abuse-in-protocol-swaps)
23. [LP Token Burn/Hijack Attacks](#23-lp-token-burnhijack-attacks)
24. [Constant Sum AMM Arbitrage](#24-constant-sum-amm-arbitrage)
25. [State Accounting Discrepancies](#25-state-accounting-discrepancies)
26. [Incorrect Liquidity Ownership Assumptions](#26-incorrect-liquidity-ownership-assumptions)
27. [Dividend/Reward Gaming](#27-dividendreward-gaming)
28. [Missing Account Validation (Solana-Specific)](#28-missing-account-validation-solana-specific)
29. [Detection Patterns & Audit Checklist](#29-detection-patterns--audit-checklist)

---

## 1. First Depositor / Inflation Attacks

### Overview

Constant product AMMs (x*y=k) calculate LP token amounts based on the ratio of deposited assets to existing reserves. When a pool has zero or minimal liquidity, the first depositor can manipulate the LP token price to either steal funds from subsequent depositors or permanently brick the pool.

> **📚 Source Reports for Deep Dive:**
> - `reports/constantproduct/h-03-first-depositor-can-break-minting-of-shares.md` (Caviar - Code4rena)
> - `reports/constantproduct/initial-mint-front-run-inflation-attack.md` (NUTS Finance - MixBytes)
> - `reports/constantproduct/c-03-blocking-the-initial-liquidity-seed-with-a-1-wei-donation.md` (Moarcandy - Pashov)



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of logic_error"
- Pattern key: `logic_error | liquidity_pool | constant_product_amm_integration`
- Interaction scope: `multi_contract`
- Primary affected component(s): `liquidity_pool|swap_router|price_feed|reserves`
- High-signal code keywords: `LP_tokens`, `TWAP`, `_addLiquidity`, `_deployToken`, `_executeTrade`, `_existsPairPool`, `_findSlice`, `_getSwapAmt`
- Typical sink / impact: `fund_loss|price_manipulation|dos|unfair_exchange`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `CCFrax1to1AMM.function -> JettonFactory.function -> Pool.function`
- Trust boundary crossed: `callback / external call`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: State variable updated after external interaction instead of before (CEI violation)
- Signal 2: Withdrawal path produces different accounting than deposit path for same principal
- Signal 3: Reward accrual continues during paused/emergency state
- Signal 4: Edge case in state machine transition allows invalid state

#### False Positive Guards

- Not this bug when: Standard security patterns (access control, reentrancy guards, input validation) are in place
- Safe if: Protocol behavior matches documented specification
- Requires attacker control of: specific conditions per pattern

### Vulnerability Description

#### Root Cause

LP tokens are calculated as:
```
liquidity = sqrt(amount0 * amount1)                    // First deposit
liquidity = min(amount0 * totalSupply / reserve0,      // Subsequent deposits
                amount1 * totalSupply / reserve1)
```

When `totalSupply` is very small (e.g., 1 wei) and reserves are artificially inflated, the calculation rounds down to zero for normal depositors.

#### Attack Scenario

1. Attacker creates pool and deposits minimal amount (1 wei of each token)
2. Attacker receives 1 wei of LP tokens: `sqrt(1 * 1) = 1`
3. Attacker transfers large amounts directly to pool (donation): e.g., 1e18 of each token
4. Calls `sync()` to update reserves
5. Now: 1 LP token = 1e18 of each token
6. Victim deposits 0.99e18: `shares = (0.99e18 * 1) / 1e18 = 0` (rounds down)
7. Victim loses entire deposit, attacker profits

### Vulnerable Pattern Examples

**Example 1: No MINIMUM_LIQUIDITY Protection** [HIGH]
> 📖 Reference: `reports/constantproduct/h-03-first-depositor-can-break-minting-of-shares.md`
```solidity
// ❌ VULNERABLE: No minimum liquidity lock
function addQuote(uint256 baseTokenAmount, uint256 fractionalTokenAmount) public view returns (uint256) {
    uint256 lpTokenSupply = lpToken.totalSupply();
    if (lpTokenSupply > 0) {
        uint256 baseTokenShare = (baseTokenAmount * lpTokenSupply) / baseTokenReserves();
        uint256 fractionalTokenShare = (fractionalTokenAmount * lpTokenSupply) / fractionalTokenReserves();
        return Math.min(baseTokenShare, fractionalTokenShare);
    } else {
        // No minimum liquidity burned - vulnerable!
        return Math.sqrt(baseTokenAmount * fractionalTokenAmount);
    }
}
```

**Example 2: Migrator Bypasses MINIMUM_LIQUIDITY** [MEDIUM]
> 📖 Reference: `reports/constantproduct/m-08-zeroswapuniswapv2pairsol-token-reserves-per-lp-token-can-be-manipulated-due.md`
```solidity
// ❌ VULNERABLE: Migrator can bypass MINIMUM_LIQUIDITY
if (_totalSupply == 0) {
    address migrator = IUniswapV2Factory(factory).migrator();
    if (msg.sender == migrator) {
        liquidity = IMigrator(migrator).desiredLiquidity();
        // No MINIMUM_LIQUIDITY burned when using migrator!
    } else {
        liquidity = Math.sqrt(amount0.mul(amount1)).sub(MINIMUM_LIQUIDITY);
        _mint(address(0), MINIMUM_LIQUIDITY);
    }
}
```

**Example 3: 1 Wei Donation Attack** [CRITICAL]
> 📖 Reference: `reports/constantproduct/c-03-blocking-the-initial-liquidity-seed-with-a-1-wei-donation.md`
```solidity
// Attack sequence:
// 1. Attacker creates empty pair on Uniswap before protocol
// 2. Donates 1 wei of WETH to pair
// 3. Calls sync() - one reserve becomes non-zero

// When protocol tries to add liquidity via router:
function _addLiquidity(...) internal returns (uint amountA, uint amountB) {
    (uint reserveA, uint reserveB) = UniswapV2Library.getReserves(factory, tokenA, tokenB);
    if (reserveA == 0 && reserveB == 0) {
        (amountA, amountB) = (amountADesired, amountBDesired);
    } else {
        // This branch executes because reserveB > 0!
        uint amountBOptimal = UniswapV2Library.quote(amountADesired, reserveA, reserveB);
        // quote() reverts: "INSUFFICIENT_LIQUIDITY" because reserveA == 0
    }
}
```

**Example 4: Burn Function Enables Pool Hijacking** [HIGH]
> 📖 Reference: `reports/constantproduct/h-10-hijack-token-pool-by-burning-liquidity-token.md`
```solidity
// ❌ VULNERABLE: Unrestricted burn allows pool hijacking
function burn(uint256 amount) external {
    _burn(msg.sender, amount);
}

// Attack:
// 1. Create pool, deposit minimal amount
// 2. Burn LP tokens until totalSupply = 1
// 3. Massive reserves / tiny supply = expensive LP tokens
// 4. All future depositors get 0 LP tokens due to rounding
```

### Impact Analysis

#### Technical Impact
- Complete loss of deposited funds for victims
- Pool becomes permanently unusable (bricked)
- LP token price manipulation
- Protocol reserves can be drained

#### Business Impact
- **Financial Loss**: Victims lose 100% of deposits
- **Protocol Reputation**: Trust completely destroyed
- **TVL Impact**: Pool becomes worthless

#### Affected Scenarios
- New pool deployments
- Pools with migrator functionality
- Pools without minimum liquidity mechanisms
- Protocols that allow permissionless pool creation

### Secure Implementation

**Fix 1: Burn MINIMUM_LIQUIDITY on First Deposit**
```solidity
// ✅ SECURE: Uniswap V2 pattern
uint public constant MINIMUM_LIQUIDITY = 10**3;

function mint(address to) external returns (uint liquidity) {
    (uint112 _reserve0, uint112 _reserve1,) = getReserves();
    uint balance0 = IERC20(token0).balanceOf(address(this));
    uint balance1 = IERC20(token1).balanceOf(address(this));
    uint amount0 = balance0.sub(_reserve0);
    uint amount1 = balance1.sub(_reserve1);
    
    uint _totalSupply = totalSupply;
    if (_totalSupply == 0) {
        liquidity = Math.sqrt(amount0.mul(amount1)).sub(MINIMUM_LIQUIDITY);
        _mint(address(0), MINIMUM_LIQUIDITY); // Permanently lock
    } else {
        liquidity = Math.min(
            amount0.mul(_totalSupply) / _reserve0,
            amount1.mul(_totalSupply) / _reserve1
        );
    }
    require(liquidity > 0, 'INSUFFICIENT_LIQUIDITY_MINTED');
    _mint(to, liquidity);
}
```

**Fix 2: Require Minimum Initial Deposit**
```solidity
// ✅ SECURE: Enforce minimum initial deposit
function addLiquidity(uint256 amount0, uint256 amount1) external {
    if (totalSupply == 0) {
        require(amount0 >= MIN_INITIAL_DEPOSIT, "Initial deposit too small");
        require(amount1 >= MIN_INITIAL_DEPOSIT, "Initial deposit too small");
    }
    // ... rest of logic
}
```

**Fix 3: Admin-Only First Deposit**
```solidity
// ✅ SECURE: Only admin can initialize pool
function initializePool(uint256 amount0, uint256 amount1) external onlyAdmin {
    require(totalSupply == 0, "Pool already initialized");
    require(amount0 >= SAFE_INITIAL_AMOUNT, "Insufficient initial liquidity");
    // ... initialize with safe amounts
}
```

---

## 2. Slippage Protection Vulnerabilities

### Overview

Slippage protection prevents users from receiving fewer tokens than expected during swaps or liquidity operations. Missing or inadequate slippage checks allow MEV bots and attackers to extract value from users through sandwich attacks or by executing trades at unfavorable prices.

> **📚 Source Reports for Deep Dive:**
> - `reports/constantproduct/missing-slippage-checks.md` (Eternal Finance - OtterSec)
> - `reports/constantproduct/no-slippage-protection.md` (Various)
> - `reports/constantproduct/exploiting-zero-amountoutmin-in-dexwrappers-for-mev-attacks.md`

### Vulnerability Description

#### Root Cause

Functions that swap tokens or add/remove liquidity don't validate that the received amount meets user expectations. This occurs when:
- `amountOutMin` is set to 0 or not enforced
- No oracle price comparison
- Relying on spot price without bounds

#### Attack Scenario

1. User submits swap: 100 ETH → USDC, expects ~$200,000
2. MEV bot sees pending transaction
3. Bot front-runs: buys USDC, pushing price up
4. User's transaction executes at worse price: gets $180,000
5. Bot back-runs: sells USDC, profits ~$20,000

### Vulnerable Pattern Examples

**Example 1: Zero amountOutMin** [HIGH]
> 📖 Reference: `reports/constantproduct/exploiting-zero-amountoutmin-in-dexwrappers-for-mev-attacks.md`
```solidity
// ❌ VULNERABLE: amountOutMin hardcoded to 0
function swap(address tokenIn, address tokenOut, uint256 amountIn) external {
    router.swapExactTokensForTokens(
        amountIn,
        0,  // amountOutMin = 0, accepts any output!
        path,
        address(this),
        block.timestamp
    );
}
```

**Example 2: No Slippage Check After Swap** [HIGH]
> 📖 Reference: `reports/constantproduct/missing-slippage-checks.md`
```solidity
// ❌ VULNERABLE: No validation of swap output
function reinvest(uint256 cakeAmount) external {
    // Swap without slippage protection
    uint256 received = router.swap_exact_x_to_y(cakeAmount);
    // No check: require(received >= expectedMin, "Slippage too high");
    stake(received);
}
```

**Example 3: Slippage Check Bypassed** [MEDIUM]
```solidity
// ❌ VULNERABLE: Slippage parameter ignored in execution
function executeTrade(uint256 amountIn, uint256 minOut) external {
    uint256 received = _swap(amountIn);
    // minOut parameter exists but is never checked!
    emit TradeExecuted(received);
}
```

### Impact Analysis

#### Technical Impact
- Users receive significantly less tokens than expected
- MEV extraction from every unprotected transaction
- Arbitrage opportunities created for attackers

#### Business Impact
- **Typical Loss**: 1-10% per transaction to MEV
- **Extreme Cases**: Up to 50%+ loss in low liquidity pools
- **User Trust**: Users avoid protocol after losses

### Secure Implementation

**Fix 1: Enforce Minimum Output**
```solidity
// ✅ SECURE: Validate minimum output
function swap(
    address tokenIn,
    address tokenOut,
    uint256 amountIn,
    uint256 amountOutMin  // User-specified minimum
) external returns (uint256 amountOut) {
    amountOut = router.swapExactTokensForTokens(
        amountIn,
        amountOutMin,  // Enforced by router
        path,
        address(this),
        block.timestamp
    );
    require(amountOut >= amountOutMin, "Slippage exceeded");
}
```

**Fix 2: Oracle-Based Slippage Protection**
```solidity
// ✅ SECURE: Compare against oracle price
function swap(uint256 amountIn, uint256 maxSlippageBps) external {
    uint256 oraclePrice = oracle.getPrice(tokenIn, tokenOut);
    uint256 expectedOut = amountIn * oraclePrice / 1e18;
    uint256 minOut = expectedOut * (10000 - maxSlippageBps) / 10000;
    
    uint256 received = router.swap(amountIn);
    require(received >= minOut, "Price deviation too high");
}
```

---

## 3. Sandwich & MEV Attacks

### Overview

Sandwich attacks occur when an attacker front-runs and back-runs a user's AMM transaction, profiting from the price impact. This is particularly devastating in constant product AMMs where large trades cause significant price movement.

> **📚 Source Reports for Deep Dive:**
> - `reports/constantproduct/sandwich-attack-on-user-withdrawal.md` (Yearn - MixBytes)
> - `reports/constantproduct/m-08-relpcontractrelp-is-susceptible-to-sandwich-attack-due-to-user-control-over.md`
> - `reports/constantproduct/sandwich-attacks-and-price-manipulation.md`

### Vulnerable Pattern Examples

**Example 1: Withdrawal Without Protection** [HIGH]
> 📖 Reference: `reports/constantproduct/sandwich-attack-on-user-withdrawal.md`
```solidity
// ❌ VULNERABLE: Withdrawal swaps without protection
function withdraw(uint256 shares) external {
    uint256 assets = convertToAssets(shares);
    // Swap to output token - vulnerable to sandwich
    uint256 received = dex.swap(token0, outputToken, assets);
    IERC20(outputToken).transfer(msg.sender, received);
}
```

**Example 2: User-Controlled Swap Parameters** [MEDIUM]
> 📖 Reference: `reports/constantproduct/m-08-relpcontractrelp-is-susceptible-to-sandwich-attack-due-to-user-control-over.md`
```solidity
// ❌ VULNERABLE: Users can set exploitable parameters
function rebalance(
    uint256 minTokenAOut,  // User can set to 0
    uint256 minTokenBOut   // User can set to 0
) external {
    // Even legitimate users might set low values
    // MEV bots exploit any unprotected transactions
}
```

### Secure Implementation

**Fix 1: Private Mempool / Flashbots**
```solidity
// ✅ SECURE: Use private transaction submission
// Submit via Flashbots Protect or similar MEV protection
// Transactions not visible in public mempool
```
---

## 4. Spot Price Manipulation (slot0)

### Overview

Using Uniswap V3's `slot0()` or equivalent spot price data in price calculations is extremely dangerous because the current price can be manipulated within a single transaction using flash loans.

> **📚 Source Reports for Deep Dive:**
> - `reports/constantproduct/h-3-usage-of-slot0-is-extremely-easy-to-manipulate.md` (RealWagmi - Sherlock)
> - `reports/constantproduct/h-1-attacker-can-profit-by-manipulating-uniswap-liquidity.md` (stNXM - Sherlock)
> - `reports/constantproduct/intra-transaction-oracle-tampering-possible-with-lp-pricing-using-flashloans.md` (Sense - Spearbit)

### Vulnerability Description

#### Root Cause

`slot0` returns the current tick and sqrtPriceX96 which reflect the most recent swap. An attacker can:
1. Flash loan large amounts
2. Swap to move price
3. Exploit the manipulated price in victim protocol
4. Swap back
5. Repay flash loan with profit

### Vulnerable Pattern Examples

**Example 1: Direct slot0 Usage** [HIGH]
> 📖 Reference: `reports/constantproduct/h-3-usage-of-slot0-is-extremely-easy-to-manipulate.md`
```solidity
// ❌ VULNERABLE: Using slot0 for price calculation
function getReserves() public view returns (uint256 reserve0, uint256 reserve1) {
    (uint160 sqrtPriceX96, , , , , , ) = pool.slot0();  // Manipulatable!
    
    for (uint256 i = 0; i < positions.length; i++) {
        (uint256 amount0, uint256 amount1) = LiquidityAmounts.getAmountsForLiquidity(
            sqrtPriceX96,  // Used directly
            // ...
        );
        reserve0 += amount0;
        reserve1 += amount1;
    }
}
```

**Example 2: LP Token Valuation with Spot Price** [HIGH]
> 📖 Reference: `reports/constantproduct/intra-transaction-oracle-tampering-possible-with-lp-pricing-using-flashloans.md`
```solidity
// ❌ VULNERABLE: LP pricing using current balances
function getLPValue() public view returns (uint256) {
    uint256 balanceA = tokenA.balanceOf(address(pool));
    uint256 balanceB = tokenB.balanceOf(address(pool));
    // Balances can be manipulated via flash loan + swap
    return PriceOracle.price(tokenA) * balanceA + PriceOracle.price(tokenB) * balanceB;
}
```

### Secure Implementation

**Fix 1: Use TWAP Instead of Spot Price**
```solidity
// ✅ SECURE: Time-weighted average price
function getPrice() public view returns (uint256) {
    uint32[] memory secondsAgos = new uint32[](2);
    secondsAgos[0] = TWAP_PERIOD;  // e.g., 1800 seconds (30 min)
    secondsAgos[1] = 0;
    
    (int56[] memory tickCumulatives, ) = pool.observe(secondsAgos);
    int56 tickCumulativesDelta = tickCumulatives[1] - tickCumulatives[0];
    int24 arithmeticMeanTick = int24(tickCumulativesDelta / int56(uint56(TWAP_PERIOD)));
    
    return TickMath.getSqrtRatioAtTick(arithmeticMeanTick);
}
```

**Fix 2: Price Deviation Check**
```solidity
// ✅ SECURE: Compare spot to TWAP
function validatePrice() internal view {
    (uint160 sqrtPriceX96, , , , , , ) = pool.slot0();
    uint160 twapPrice = getTWAP();
    
    uint256 deviation = sqrtPriceX96 > twapPrice 
        ? (sqrtPriceX96 - twapPrice) * 10000 / twapPrice
        : (twapPrice - sqrtPriceX96) * 10000 / twapPrice;
    
    require(deviation <= MAX_DEVIATION_BPS, "Price manipulation detected");
}
```

---

## 5. Deadline Vulnerabilities

### Overview

Missing deadline parameters allow pending transactions to be executed at unfavorable times, enabling MEV extraction from stale transactions.

> **📚 Source Reports for Deep Dive:**
> - `reports/constantproduct/m-01-missing-deadline-checks-allow-pending-transactions-to-be-maliciously-execut.md` (Backed - Code4rena)

### Vulnerable Pattern Examples

**Example 1: No Deadline Parameter** [MEDIUM]
> 📖 Reference: `reports/constantproduct/m-01-missing-deadline-checks-allow-pending-transactions-to-be-maliciously-execut.md`
```solidity
// ❌ VULNERABLE: No deadline - transaction can execute anytime
function swap(uint256 amountIn, uint256 amountOutMin) external {
    // If transaction is pending for days/weeks in mempool,
    // price conditions may have changed dramatically
    router.swapExactTokensForTokens(
        amountIn,
        amountOutMin,
        path,
        msg.sender,
        block.timestamp  // Uses current time, not user's intended deadline!
    );
}
```

### Secure Implementation

**Fix: User-Specified Deadline**
```solidity
// ✅ SECURE: User controls execution deadline
function swap(
    uint256 amountIn,
    uint256 amountOutMin,
    uint256 deadline  // User specifies when tx should expire
) external {
    require(block.timestamp <= deadline, "Transaction expired");
    
    router.swapExactTokensForTokens(
        amountIn,
        amountOutMin,
        path,
        msg.sender,
        deadline
    );
}
```

---

## 6. Reserve Manipulation Attacks

### Overview

Attackers can manipulate pool reserves through flash loans to exploit mechanisms that rely on current reserve values, such as impermanent loss protection or collateral valuation.

> **📚 Source Reports for Deep Dive:**
> - `reports/constantproduct/h-06-lps-of-vaderpoolv2-can-manipulate-pool-reserves-to-extract-funds-from-the-r.md` (Vader - Code4rena)
> - `reports/constantproduct/m-05-pair-price-may-be-manipulated-by-direct-transfers.md`

### Vulnerable Pattern Examples

**Example 1: IL Protection Based on Current Reserves** [HIGH]
> 📖 Reference: `reports/constantproduct/h-06-lps-of-vaderpoolv2-can-manipulate-pool-reserves-to-extract-funds-from-the-r.md`
```solidity
// ❌ VULNERABLE: IL calculation uses manipulatable reserves
function calculateImpermanentLoss() internal view returns (uint256) {
    (uint256 reserve0, uint256 reserve1) = getReserves();  // Current reserves
    // Attacker flash-loans to manipulate reserves before calling
    // Returns artificially high IL, gets compensated from reserve
    return _calculateIL(reserve0, reserve1, originalReserve0, originalReserve1);
}
```

### Secure Implementation

**Fix: Use TWAP for Reserve Calculations**
```solidity
// ✅ SECURE: Time-weighted reserves
function calculateImpermanentLoss() internal view returns (uint256) {
    (uint256 twapReserve0, uint256 twapReserve1) = getTWAPReserves();
    // Cannot be manipulated within single transaction
    return _calculateIL(twapReserve0, twapReserve1, originalReserve0, originalReserve1);
}
```

---

## 7. LP Token Calculation Issues

### Overview

Incorrect LP token calculations can lead to loss of funds for liquidity providers or enable attacks where users receive disproportionate shares.

> **📚 Source Reports for Deep Dive:**
> - `reports/constantproduct/flawed-calculation-of-lp-tokens-in-liquidity-swap-pbc.md`
> - `reports/constantproduct/h-5-univ2lporacle-will-malfunction-if-token0-or-token1s-decimals-18.md`

### Vulnerable Pattern Examples

**Example 1: Decimal Mismatch** [HIGH]
> 📖 Reference: `reports/constantproduct/h-5-univ2lporacle-will-malfunction-if-token0-or-token1s-decimals-18.md`
```solidity
// ❌ VULNERABLE: Assumes 18 decimals for all tokens
function getLPValue() external view returns (uint256) {
    (uint112 reserve0, uint112 reserve1, ) = pair.getReserves();
    // If token0 has 6 decimals (USDC), calculation is wrong!
    uint256 value = reserve0 * price0 / 1e18 + reserve1 * price1 / 1e18;
    return value * totalSupply / (reserve0 + reserve1);
}
```

### Secure Implementation

**Fix: Handle Variable Decimals**
```solidity
// ✅ SECURE: Normalize decimals
function getLPValue() external view returns (uint256) {
    (uint112 reserve0, uint112 reserve1, ) = pair.getReserves();
    uint8 decimals0 = IERC20Metadata(pair.token0()).decimals();
    uint8 decimals1 = IERC20Metadata(pair.token1()).decimals();
    
    uint256 normalized0 = uint256(reserve0) * 10**(18 - decimals0);
    uint256 normalized1 = uint256(reserve1) * 10**(18 - decimals1);
    
    return (normalized0 * price0 + normalized1 * price1) / 1e18;
}
```

---

## 8. Callback & Reentrancy Attacks

### Overview

AMM integrations often expose callback functions (like Uniswap V3's `mintCallback` and `swapCallback`) that, if not properly protected, can be exploited to drain user funds or manipulate state. Additionally, reentrancy through these callbacks can corrupt internal accounting.

> **📚 Source Reports for Deep Dive:**
> - `reports/constantproduct/c-04-draining-approved-tokens-by-unrestricted-uniswapv3mintcallback.md` (Burve - Pashov)
> - `reports/constantproduct/redeemnative-reentrancy-enables-permanent-fund-freeze-systemic-misaccounting-and.md` (Notional - MixBytes)
> - `reports/constantproduct/m-04-berachain-users-cannot-use-flashloans-from-uni-v2-wberaberabottoken-pool.md` (Berabot - Shieldify)

### Vulnerability Description

#### Root Cause 1: Unrestricted Callbacks

Uniswap V3 callbacks (`uniswapV3MintCallback`, `uniswapV3SwapCallback`) are called by the pool during operations. If a contract implements these without access control, any caller can invoke them with arbitrary data.

#### Root Cause 2: Reentrancy in Swap Paths

When swapping through DEXes, tokens with callbacks (ERC-777, malicious ERC-20s) can reenter the protocol mid-swap, corrupting state that was calculated before the reentry.

### Vulnerable Pattern Examples

**Example 1: Unrestricted Mint Callback** [CRITICAL]
> 📖 Reference: `reports/constantproduct/c-04-draining-approved-tokens-by-unrestricted-uniswapv3mintcallback.md`
```solidity
// ❌ VULNERABLE: No access control on callback
function uniswapV3MintCallback(uint256 amount0Owed, uint256 amount1Owed, bytes calldata data) external {
    address source = abi.decode(data, (address));
    // ANYONE can call this - attacker provides victim's address in data!
    TransferHelper.safeTransferFrom(token0, source, address(pool), amount0Owed);
    TransferHelper.safeTransferFrom(token1, source, address(pool), amount1Owed);
}

// Attack: Attacker calls this directly with data = victim's address
// Drains all tokens victim approved to this contract
```

**Example 2: Reentrancy via Malicious Token** [HIGH]
> 📖 Reference: `reports/constantproduct/redeemnative-reentrancy-enables-permanent-fund-freeze-systemic-misaccounting-and.md`
```solidity
// ❌ VULNERABLE: Swap through untrusted token path
function _executeTrade(bytes memory exchangeData) internal {
    uint256 balanceBefore = IERC20(yieldToken).balanceOf(address(this));
    
    // Swap through path that includes attacker's token
    // Attacker's token.transfer() reenters during swap!
    router.exactInput(exchangeData);
    
    uint256 balanceAfter = IERC20(yieldToken).balanceOf(address(this));
    uint256 received = balanceAfter - balanceBefore;  // Corrupted if reentered!
}
```

**Example 3: Fee-On-Transfer Token Reentrancy Lock** [MEDIUM]
> 📖 Reference: `reports/constantproduct/m-04-berachain-users-cannot-use-flashloans-from-uni-v2-wberaberabottoken-pool.md`
```solidity
// ❌ PROBLEMATIC: Auto-swap in transfer triggers reentrancy lock
function _transfer(address from, address to, uint256 amount) internal override {
    if (canSwap && !swapping && !isAmmPair[from]) {
        swapping = true;
        swapBack();  // Calls pool.swap() internally
        swapping = false;
    }
    super._transfer(from, to, amount);
}

// Impact: Flash loans from this pool's pair become impossible
// because transfer triggers swap which hits Uniswap's reentrancy lock
```

### Impact Analysis

#### Technical Impact
- **Fund Drainage**: Unrestricted callbacks allow draining approved tokens
- **State Corruption**: Reentrancy corrupts balance calculations
- **Permanent Freezes**: Accounting mismatches can lock funds
- **Flash Loan Blocking**: Legitimate operations fail due to reentrancy guards

### Secure Implementation

**Fix 1: Restrict Callback to Pool Only**
```solidity
// ✅ SECURE: Only pool can call callback
function uniswapV3MintCallback(uint256 amount0Owed, uint256 amount1Owed, bytes calldata data) external {
    require(msg.sender == address(pool), "Only pool");
    // Safe: Only the legitimate pool can trigger this
    IERC20(token0).safeTransfer(address(pool), amount0Owed);
    IERC20(token1).safeTransfer(address(pool), amount1Owed);
}
```

**Fix 2: Nonreentrant Guards on All Entry Points**
```solidity
// ✅ SECURE: Reentrancy protection
function redeemNative(uint256 shares, bytes calldata exchangeData) external nonReentrant {
    // Protected from reentry via malicious tokens
}

function initiateWithdraw(uint256 amount) external nonReentrant {
    // Also protected
}
```

**Fix 3: Validate Swap Paths**
```solidity
// ✅ SECURE: Only allow whitelisted tokens in path
function swap(bytes calldata path) external {
    address[] memory tokens = decodePath(path);
    for (uint i = 0; i < tokens.length; i++) {
        require(whitelistedTokens[tokens[i]], "Token not whitelisted");
    }
}
```

---

## 9. Factory & Pool Creation Attacks

### Overview

Permissionless pool creation in AMMs enables various attack vectors including front-running pool initialization, deterministic address exploitation, and fake pool detection issues.

> **📚 Source Reports for Deep Dive:**
> - `reports/constantproduct/h-02-lambofactory-can-be-permanently-dos-ed-due-to-createpair-call-reversal.md` (Lambo.win - Code4rena)
> - `reports/constantproduct/m-05-griefing-attack-on-genesispoolmanagersoldepositnativetoken-leading-to-denia.md` (Blackhole - Code4rena)
> - `reports/constantproduct/m-04-wrong-init-code-hash.md` (Numoen - Code4rena)
> - `reports/constantproduct/m-8-false-pool-exists-detection-via-balanceof-leads-to-broken-swap-paths.md` (DODO - Sherlock)
> - `reports/constantproduct/risk-of-incorrect-pool-initialization.md` (LMAO - OtterSec)

### Vulnerability Description

#### Root Cause 1: Deterministic Address Front-Running

When using `CREATE` opcode, new contract addresses are predictable. Attackers can pre-calculate the next token address and create a pool for it before the token exists.

#### Root Cause 2: False Pool Existence Detection

Using `balanceOf()` to check if a pool exists is flawed - any address can hold tokens without being a deployed contract.

#### Root Cause 3: Wrong Init Code Hash

Hardcoded init code hashes for pair address calculation may not match the actual factory, leading to incorrect pool detection.

### Vulnerable Pattern Examples

**Example 1: Deterministic Address DoS** [HIGH]
> 📖 Reference: `reports/constantproduct/h-02-lambofactory-can-be-permanently-dos-ed-due-to-createpair-call-reversal.md`
```solidity
// ❌ VULNERABLE: Deterministic token address
function _deployToken(string memory name) internal returns (address) {
    // Uses CREATE - address is predictable!
    return Clones.clone(tokenImplementation);
}

function createLaunchPad() external {
    address token = _deployToken(name);
    // Attacker already created pair for this address!
    IUniswapV2Factory(factory).createPair(token, WETH);  // Reverts: PAIR_EXISTS
}

// Attack:
// 1. Calculate next token address: keccak256(rlp([factory, nonce]))[12:]
// 2. Call factory.createPair(calculatedAddress, WETH)
// 3. Legitimate createLaunchPad() now permanently fails
```

**Example 2: False Pool Detection via BalanceOf** [MEDIUM]
> 📖 Reference: `reports/constantproduct/m-8-false-pool-exists-detection-via-balanceof-leads-to-broken-swap-paths.md`
```solidity
// ❌ VULNERABLE: Checking pool existence by balance
function _existsPairPool(address tokenA, address tokenB) internal view returns (bool) {
    address pool = computePairAddress(tokenA, tokenB);
    // Just because an address holds tokens doesn't mean pool exists!
    return IERC20(tokenA).balanceOf(pool) > 0 && IERC20(tokenB).balanceOf(pool) > 0;
}

// Attack: Send 1 wei of each token to computed address
// _existsPairPool returns true but no pool contract exists
// Swaps routing through this "pool" will revert
```

**Example 3: Wrong Init Code Hash** [MEDIUM]
> 📖 Reference: `reports/constantproduct/m-04-wrong-init-code-hash.md`
```solidity
// ❌ VULNERABLE: Hardcoded hash doesn't match actual factory
function pairFor(address tokenA, address tokenB) internal pure returns (address) {
    return address(uint160(uint256(keccak256(abi.encodePacked(
        hex"ff",
        factory,
        keccak256(abi.encodePacked(token0, token1)),
        hex"e18a34eb0e04b04f7a0ac29a6e80748dca96319b42c54d679cb821dca90c6303"  // Wrong!
    )))));
}
// Computed address won't match actual Uniswap pair address
```

**Example 4: Pool Initialization Front-Running** [MEDIUM]
> 📖 Reference: `reports/constantproduct/m-01-routergetorcreatepoolandaddliquidity-can-be-frontrunned-which-leads-to-pric.md`
```solidity
// ❌ VULNERABLE: Create + initialize in one tx
function getOrCreatePoolAndAddLiquidity(
    PoolParams calldata params,
    AddLiquidityParams[] calldata addParams
) external {
    IPool pool = getOrCreatePool(params);  // Can be front-run!
    addLiquidity(pool, addParams);
}

// Attack:
// 1. See pending tx with desired initial tick
// 2. Front-run: create pool with different initial tick
// 3. Victim's liquidity added at wrong price
```

### Impact Analysis

#### Technical Impact
- **Permanent DoS**: Factory permanently blocked from creating pairs
- **Swap Failures**: False pool detection causes routing failures
- **Price Manipulation**: Front-run pool creation with bad initial price
- **Wrong Pool Interaction**: Init hash mismatch routes to wrong address

### Secure Implementation

**Fix 1: Use CREATE2 with Salt**
```solidity
// ✅ SECURE: Unpredictable address with user-controlled salt
function deployToken(bytes32 salt) external returns (address) {
    return Clones.cloneDeterministic(implementation, salt);
}
```

**Fix 2: Check Pool Existence Properly**
```solidity
// ✅ SECURE: Verify pool contract exists and has code
function poolExists(address tokenA, address tokenB) internal view returns (bool) {
    address pool = IFactory(factory).getPair(tokenA, tokenB);
    if (pool == address(0)) return false;
    
    // Verify it's a contract with code
    uint256 codeSize;
    assembly { codeSize := extcodesize(pool) }
    return codeSize > 0;
}
```

**Fix 3: Use Factory's getPair Instead of Computing**
```solidity
// ✅ SECURE: Let factory tell us the real pair address
function getPool(address tokenA, address tokenB) internal view returns (address) {
    return IUniswapV2Factory(factory).getPair(tokenA, tokenB);
}
```

**Fix 4: Separate Pool Creation from Liquidity Add**
```solidity
// ✅ SECURE: Two-step process prevents front-running impact
function createPool(PoolParams calldata params) external returns (address) {
    return IFactory(factory).createPair(params.tokenA, params.tokenB);
}

function addLiquidity(address pool, uint256 amount0, uint256 amount1, uint256 minLP) external {
    // Verify pool state matches expectations
    (uint112 reserve0, uint112 reserve1, ) = IPool(pool).getReserves();
    // User can verify price before committing
}
```

---

## 10. Decimal & Math Calculation Issues

### Overview

Token decimal mismatches and arithmetic errors in AMM calculations can lead to severe over/under-valuation of assets, enabling fund extraction or causing protocol insolvency.

> **📚 Source Reports for Deep Dive:**
> - `reports/constantproduct/h-6-curve-vault-will-undervalue-or-overvalue-the-lp-pool-tokens-if-it-comprises-.md` (Notional - Sherlock)
> - `reports/constantproduct/h-3-ctokenoraclesolgetcerc20price-contains-critical-math-error.md` (Sentiment - Sherlock)
> - `reports/constantproduct/h-02-incorrect-output-amount-calculation-for-trader-joe-v1-pools.md` (Trader Joe - Code4rena)

### Vulnerable Pattern Examples

**Example 1: Missing Decimal Normalization** [HIGH]
> 📖 Reference: `reports/constantproduct/h-6-curve-vault-will-undervalue-or-overvalue-the-lp-pool-tokens-if-it-comprises-.md`
```solidity
// ❌ VULNERABLE: Assumes both tokens have same decimals
function _getTimeWeightedPrimaryBalance(
    uint256 primaryBalance,
    uint256 secondaryBalance,
    uint256 oraclePrice
) internal view returns (uint256 primaryAmount) {
    // If primary=DAI(18 decimals), secondary=USDC(6 decimals)
    // This calculation is completely wrong!
    uint256 secondaryAmountInPrimary = secondaryBalance * poolClaimPrecision / oraclePrice;
    
    // 50 USDC (50 * 10^6) valued as 0.00000000005 DAI instead of 50 DAI!
    primaryAmount = primaryBalance + secondaryAmountInPrimary;
}
```

**Example 2: Missing Power of 10** [CRITICAL]
> 📖 Reference: `reports/constantproduct/h-3-ctokenoraclesolgetcerc20price-contains-critical-math-error.md`
```solidity
// ❌ VULNERABLE: decimals() returns 6, not 10^6!
function getCErc20Price(ICToken cToken, address underlying) internal view returns (uint) {
    return cToken.exchangeRateStored()
        .mulDivDown(1e8, IERC20(underlying).decimals())  // Should be 10**decimals()!
        .mulWadDown(oracle.getPrice(underlying));
}

// If underlying has 6 decimals:
// Wrong: divides by 6
// Correct: divides by 10^6 = 1,000,000
// Result: Price is 166,666x higher than it should be!
```

**Example 3: Wrong Output Amount Formula** [HIGH]
> 📖 Reference: `reports/constantproduct/h-02-incorrect-output-amount-calculation-for-trader-joe-v1-pools.md`
```solidity
// ❌ VULNERABLE: Wrong AMM output formula
function getAmountOut(uint256 amountIn, uint256 reserveIn, uint256 reserveOut) {
    // Wrong formula:
    uint256 amountOut = (reserveOut * amountIn * 997) / (reserveIn * 1000);
    
    // Correct Uniswap V2 formula:
    // amountOut = (amountIn * 997 * reserveOut) / (reserveIn * 1000 + amountIn * 997);
}
```

### Secure Implementation

**Fix: Proper Decimal Handling**
```solidity
// ✅ SECURE: Normalize decimals before calculation
function _getTimeWeightedPrimaryBalance(
    uint256 primaryBalance,
    uint256 secondaryBalance,
    uint256 oraclePrice,
    uint8 primaryDecimals,
    uint8 secondaryDecimals
) internal pure returns (uint256) {
    // Scale secondary to primary precision
    uint256 scaledSecondary;
    if (secondaryDecimals < primaryDecimals) {
        scaledSecondary = secondaryBalance * (10 ** (primaryDecimals - secondaryDecimals));
    } else {
        scaledSecondary = secondaryBalance / (10 ** (secondaryDecimals - primaryDecimals));
    }
    
    uint256 secondaryInPrimary = scaledSecondary * 1e18 / oraclePrice;
    return primaryBalance + secondaryInPrimary;
}
```

---

## 11. Liquidity Migration & Protocol Upgrade Attacks

### Overview

Protocol migrations, liquidity movements, and upgrade processes are vulnerable to front-running, DoS attacks, and balance manipulation if not properly protected.

> **📚 Source Reports for Deep Dive:**
> - `reports/constantproduct/m-02-attacker-can-dos-liquidity-migration-in-liquiditymanagersol.md` (IQ AI - Code4rena)
> - `reports/constantproduct/h-09-relpcontract-wrongfully-assumes-protocol-owns-all-of-the-liquidity-in-the-u.md` (Dopex - Code4rena)

### Vulnerable Pattern Examples

**Example 1: External Balance Manipulation DoS** [HIGH]
> 📖 Reference: `reports/constantproduct/m-02-attacker-can-dos-liquidity-migration-in-liquiditymanagersol.md`
```solidity
// ❌ VULNERABLE: Uses raw balanceOf for calculations
function moveLiquidity(uint256 price) external {
    // Attacker can donate tokens to inflate currencyAmount!
    uint256 currencyAmount = currencyToken.balanceOf(address(this));
    uint256 liquidityAmount = (currencyAmount * 1e18) / price;
    
    // If liquidityAmount > actual agentToken balance, this reverts!
    agentToken.safeTransfer(address(fraxswapPair), liquidityAmount);
}

// Attack:
// 1. Transfer extra currency tokens directly to LiquidityManager
// 2. liquidityAmount inflated beyond available agent tokens
// 3. Migration permanently DoS'd
```

**Example 2: Wrong Ownership Assumption** [HIGH]
> 📖 Reference: `reports/constantproduct/h-09-relpcontract-wrongfully-assumes-protocol-owns-all-of-the-liquidity-in-the-u.md`
```solidity
// ❌ VULNERABLE: Assumes protocol owns all pool reserves
function reLP(uint256 _amount) external {
    (uint256 reserveA, uint256 reserveB) = UniswapV2Library.getReserves(
        factory, tokenA, tokenB
    );
    
    // tokenALpReserve = total pool reserves, not just protocol's share!
    uint256 tokenAToRemove = (_amount * tokenALpReserve) / tokenAReserve;
    
    // lpToRemove may exceed protocol's actual LP balance!
    uint256 lpToRemove = (tokenAToRemove * totalLpSupply) / tokenALpReserve;
    
    // REVERTS if protocol doesn't own 100% of pool liquidity
    IERC20(pair).transferFrom(amo, address(this), lpToRemove);
}
```

### Secure Implementation

**Fix 1: Track Internal Balances**
```solidity
// ✅ SECURE: Use tracked internal balance
uint256 internal trackedCurrencyBalance;

function moveLiquidity(uint256 price) external {
    uint256 liquidityAmount = (trackedCurrencyBalance * 1e18) / price;
    // Cannot be inflated by external donations
}

function receiveFromBootstrap(uint256 amount) external {
    currencyToken.safeTransferFrom(msg.sender, address(this), amount);
    trackedCurrencyBalance += amount;  // Track only legitimate deposits
}
```

**Fix 2: Use Protocol's LP Balance**
```solidity
// ✅ SECURE: Calculate based on actual LP ownership
function reLP(uint256 _amount) external {
    uint256 protocolLpBalance = IERC20(pair).balanceOf(address(amo));
    uint256 totalLpSupply = IERC20(pair).totalSupply();
    
    // Calculate protocol's share of reserves
    uint256 protocolReserveA = (reserveA * protocolLpBalance) / totalLpSupply;
    
    // Now calculations are based on actual ownership
    uint256 tokenAToRemove = (_amount * protocolReserveA) / tokenAReserve;
}
```

---

## 12. Flash Loan-Based Graduation/Threshold Manipulation

### Overview

Bonding curves and launchpad mechanisms that graduate tokens based on liquidity thresholds can be manipulated using flash loans to bypass community participation requirements.

> **📚 Source Reports for Deep Dive:**
> - `reports/constantproduct/m-04-launched-tokens-are-vulnerable-to-flashloan-attacks-forcing-premature-gradu.md` (Virtuals Protocol - Code4rena)
> - `reports/constantproduct/h-05-flash-loan-price-manipulation-in-purchasepyroflan.md`

### Vulnerable Pattern Examples

**Example 1: Flash Loan Graduation Bypass** [MEDIUM]
> 📖 Reference: `reports/constantproduct/m-04-launched-tokens-are-vulnerable-to-flashloan-attacks-forcing-premature-gradu.md`
```solidity
// ❌ VULNERABLE: Atomic unwrap allows flash loan closure
function buy(uint256 amount) external {
    // Buy tokens from bonding curve
    _mint(msg.sender, tokensOut);
    
    if (totalSold >= gradThreshold) {
        _graduate();  // Create Uniswap pair and migrate liquidity
    }
}

function unwrapToken(address[] memory accounts) public {
    require(tokenInfo[srcToken].tradingOnUniswap, "Not graduated");
    
    // No time lock - can unwrap immediately after graduation!
    for (uint i = 0; i < accounts.length; i++) {
        token.burnFrom(accounts[i], balance);
        agentToken.transferFrom(pairAddress, accounts[i], balance);
    }
}

// Attack:
// 1. Flash loan virtual tokens
// 2. Buy memecoin to trigger graduation
// 3. Unwrap to agent tokens (atomic)
// 4. Sell agent tokens in new Uniswap pair
// 5. Repay flash loan
// Result: Force graduation with no community, manipulate rewards
```

### Secure Implementation

**Fix: Time-Locked Unwrapping**
```solidity
// ✅ SECURE: Enforce delay after graduation
uint256 public graduationTime;

function _graduate() internal {
    graduationTime = block.timestamp;
    // Create pair...
}

function unwrapToken() external {
    require(block.timestamp >= graduationTime + UNWRAP_DELAY, "Too soon");
    // Flash loan can't close within same block
}
```

---

## 13. Detection Patterns & Audit Checklist

### Code Patterns to Look For

```
- Pattern 1: `slot0()` or `getReserves()` used for pricing without TWAP
- Pattern 2: Missing `amountOutMin` or set to 0
- Pattern 3: No `deadline` parameter in swap functions
- Pattern 4: First deposit without MINIMUM_LIQUIDITY burn
- Pattern 5: `balanceOf(address(this))` used in critical calculations
- Pattern 6: Missing decimal normalization in multi-token calculations
- Pattern 7: Unrestricted `burn()` function on LP tokens
- Pattern 8: Unrestricted callback functions (mintCallback, swapCallback)
- Pattern 9: Deterministic addresses with CREATE opcode
- Pattern 10: Pool existence checked via balanceOf instead of factory.getPair
- Pattern 11: Hardcoded init_code_hash for pair address computation
- Pattern 12: Migration functions using raw balanceOf
- Pattern 13: Atomic graduation + unwrap without time locks
- Pattern 14: Missing nonReentrant modifiers on swap paths
```

### Audit Checklist

- [ ] First depositor attack: Is MINIMUM_LIQUIDITY burned?
- [ ] Slippage: Is amountOutMin enforced and non-zero?
- [ ] Deadline: Can users specify transaction expiry?
- [ ] Price source: Is TWAP used instead of spot price?
- [ ] Reserve manipulation: Are reserves time-weighted?
- [ ] LP calculation: Are token decimals handled correctly?
- [ ] MEV protection: Are critical operations protected?
- [ ] Donation attack: Does balanceOf include donated tokens?
- [ ] Burn function: Is LP burning restricted?
- [ ] Sync function: Can attackers manipulate reserves via sync()?

### Keywords for Search

`constant_product`, `x*y=k`, `amm`, `uniswap`, `liquidity_pool`, `swap`, `slippage`, `sandwich_attack`, `mev`, `front_running`, `back_running`, `flash_loan`, `price_manipulation`, `slot0`, `sqrtPriceX96`, `twap`, `reserves`, `getReserves`, `first_depositor`, `inflation_attack`, `minimum_liquidity`, `lp_token`, `deadline`, `amountOutMin`, `price_impact`, `impermanent_loss`, `arbitrage`, `dex`, `swap_router`, `pair`, `factory`

---

## 13. Imbalanced Liquidity Addition Exploitation

### Overview

When adding liquidity to a constant product pool, LP tokens are minted based on the minimum ratio of the two tokens provided. Attackers can manipulate pool prices to cause LPs to overpay on one side, losing the excess tokens to the pool.

> **📚 Source Reports for Deep Dive:**
> - `reports/constant_product/overpayment-of-one-side-of-lp-pair-onjoinpool-due-to-sandwich-or-user-error.md` (Cron Finance - Spearbit)
> - `reports/constant_product/h-02-liquidity-providers-may-lose-funds-when-adding-liquidity.md` (Caviar - Code4rena)
> - `reports/constant_product/m-5-uniswap-pool-price-can-be-manipulated-so-stnxm-adds-liquidity-to-a-super-imb.md` (stNXM - Sherlock)

### Vulnerability Description

#### Root Cause

LP token calculation uses the minimum of two ratios:
```solidity
liquidity = min(amount0 * totalSupply / reserve0, amount1 * totalSupply / reserve1)
```

If tokens are provided in different proportions, the excess from the larger ratio is not refunded - it becomes a donation to the pool.

### Vulnerable Pattern Examples

**Example 1: Sandwich During Join** [HIGH]
> 📖 Reference: `reports/constant_product/overpayment-of-one-side-of-lp-pair-onjoinpool-due-to-sandwich-or-user-error.md`
```solidity
// ❌ VULNERABLE: Only minimum ratio determines LP tokens
function onJoinPool(...) {
    amountLP = Math.min(
        _token0InU112.mul(supplyLP).divDown(_token0ReserveU112),
        _token1InU112.mul(supplyLP).divDown(_token1ReserveU112)
    );
    // Excess of one token is lost to the pool!
}
```

**Example 2: Add Liquidity to Manipulated Pool** [HIGH]
> 📖 Reference: `reports/constant_product/m-5-uniswap-pool-price-can-be-manipulated-so-stnxm-adds-liquidity-to-a-super-imb.md`
```solidity
// ❌ VULNERABLE: No slippage checks on liquidity initialization
function initializeExternals() external {
    // Attacker front-runs to push tick to extreme value
    dex.mint(...);  // Adds only one token due to extreme price
    // Attacker swaps tiny amount to steal all the other token
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Calculate optimal amounts first
function addLiquidity(uint256 amount0Desired, uint256 amount1Desired, uint256 amount0Min, uint256 amount1Min) {
    (uint256 reserve0, uint256 reserve1) = getReserves();
    
    // Calculate optimal amounts to avoid overpayment
    uint256 amount1Optimal = amount0Desired * reserve1 / reserve0;
    uint256 amount0, amount1;
    
    if (amount1Optimal <= amount1Desired) {
        require(amount1Optimal >= amount1Min, "Insufficient B");
        (amount0, amount1) = (amount0Desired, amount1Optimal);
    } else {
        uint256 amount0Optimal = amount1Desired * reserve0 / reserve1;
        require(amount0Optimal >= amount0Min, "Insufficient A");
        (amount0, amount1) = (amount0Optimal, amount1Desired);
    }
    // Only use optimal amounts
}
```

---

## 14. Rebasing Token Integration Issues

### Overview

Rebasing tokens (like aTokens from Aave) automatically adjust balances to reflect accrued interest. When protocols cache share amounts instead of tracking the rebasing behavior, users lose accrued yield or calculations become incorrect.

> **📚 Source Reports for Deep Dive:**
> - `reports/constant_product/h-05-aaves-share-tokens-are-rebasing-breaking-current-strategy-code.md` (Sublime - Code4rena)

### Vulnerability Description

#### Root Cause

When depositing rebasing tokens, the initial balance equals the deposit amount. If this static balance is cached, it doesn't reflect interest accrual, while the actual token balance continues to grow.

### Vulnerable Pattern Examples

**Example 1: Cached Share Balance** [HIGH]
> 📖 Reference: `reports/constant_product/h-05-aaves-share-tokens-are-rebasing-breaking-current-strategy-code.md`
```solidity
// ❌ VULNERABLE: Caching rebasing token shares
function deposit(uint256 _amount, address _strategy) external {
    uint256 _sharesReceived = _deposit(_amount, _token, _strategy);
    // This is STATIC - doesn't track rebase!
    balanceInShares[_to][_token][_strategy] += _sharesReceived;
}

function getTokensForShares(uint256 shares, address asset) public view returns (uint256) {
    // Uses rebasing total supply but static user shares
    amount = scaledBalance * liquidityIndex * shares / IERC20(aToken).balanceOf(this);
    // Incorrect calculation!
}
```

### Impact

- Users don't receive accrued interest on deposits
- Collateral valuation is incorrect, leading to early liquidations
- Protocol accounting becomes inconsistent over time

### Secure Implementation

```solidity
// ✅ SECURE: Use wrapper token or track scaled balances
function deposit(uint256 amount) external returns (uint256 shares) {
    uint256 scaledBalanceBefore = aToken.scaledBalanceOf(address(this));
    underlying.safeTransferFrom(msg.sender, address(this), amount);
    aavePool.deposit(underlying, amount, address(this), 0);
    uint256 scaledBalanceAfter = aToken.scaledBalanceOf(address(this));
    
    // Track SCALED balance which is non-rebasing
    shares = scaledBalanceAfter - scaledBalanceBefore;
    scaledShares[msg.sender] += shares;
}

function getBalance(address user) public view returns (uint256) {
    // Convert scaled shares back to actual balance
    return scaledShares[user] * pool.getReserveNormalizedIncome(underlying) / 1e27;
}
```

---

## 15. Impermanent Loss Protection Abuse

### Overview

Some AMM protocols offer impermanent loss (IL) protection to incentivize liquidity provision. When IL protection is offered for all token pairs without whitelisting, attackers can create synthetic pools designed to maximize IL protection payouts.

> **📚 Source Reports for Deep Dive:**
> - `reports/constant_product/h-06-paying-il-protection-for-all-vaderpool-pairs-allows-the-reserve-to-be-drain.md` (Vader Protocol - Code4rena)

### Vulnerability Description

#### Root Cause

IL protection calculates losses by comparing initial deposit ratios to withdrawal ratios. If an attacker controls a synthetic token, they can manipulate the price to maximize the calculated IL and drain the protection reserve.

### Vulnerable Pattern Examples

**Example 1: Synthetic Token IL Exploit** [HIGH]
> 📖 Reference: `reports/constant_product/h-06-paying-il-protection-for-all-vaderpool-pairs-allows-the-reserve-to-be-drain.md`
```solidity
// ❌ VULNERABLE: IL protection for ALL pairs
function burn() external {
    // Calculate IL based on reserves
    uint256 ilLoss = VaderMath.calculateIL(
        originalAmount0, originalAmount1,
        removedAmount0, removedAmount1
    );
    // Pay IL protection from reserve for ANY token pair!
    reserve.reimburse(msg.sender, ilLoss);
}

// Attack:
// 1. Flashloan VADER
// 2. Deploy mintable TKN token
// 3. Add liquidity: lots of VADER, tiny TKN
// 4. Mint TKN to buy all VADER from pool
// 5. Claim massive IL protection
// 6. Repay flashloan with profit
```

### Secure Implementation

```solidity
// ✅ SECURE: Whitelist tokens eligible for IL protection
mapping(address => bool) public ilProtectionEligible;

function burn() external {
    // Only whitelisted pairs get IL protection
    require(ilProtectionEligible[token0] && ilProtectionEligible[token1], 
            "Not eligible for IL protection");
    // Calculate and pay IL...
}
```

---

## 16. Protocol Invariant Breaking

### Overview

Constant product AMMs maintain the invariant `totalSupply() == calcLpTokenSupply(reserves)`. When this invariant is broken through edge cases in add/remove liquidity operations, valid transactions may revert, leading to protocol insolvency.

> **📚 Source Reports for Deep Dive:**
> - `reports/constant_product/protocols-invariants-can-be-broken.md` (Beanstalk Wells - Cyfrin)
> - `reports/constant_product/ignoring-the-well-function-logic-for-a-ratio-of-reserves-calculation.md` (Beanstalk - Codehawks)

### Vulnerable Pattern Examples

**Example 1: Invariant Violation Leading to Reverts** [HIGH]
> 📖 Reference: `reports/constant_product/protocols-invariants-can-be-broken.md`
```solidity
// ❌ VULNERABLE: Rounding errors accumulate to break invariant
function test_invariantBroken() public {
    // After specific sequence of add/remove operations:
    // totalSupply() != calcLpTokenSupply(reserves)
    
    // Valid liquidity removal now reverts!
    removeLiquidityOneToken(lpAmount, 0); // REVERTS
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Add invariant check after operations
function checkInvariant() internal view {
    uint256 calculatedSupply = wellFunction.calcLpTokenSupply(reserves);
    require(totalSupply() == calculatedSupply, "Invariant broken");
}

function removeLiquidity(uint256 lpTokens) external {
    // ... removal logic
    checkInvariant();
}
```

---

## 17. DEX Swap Slippage Accounting Discrepancies

### Overview

When protocols perform internal rebalancing between vaults via DEX swaps, the actual output may differ from expected due to slippage. If the protocol doesn't account for this difference, internal accounting becomes incorrect.

> **📚 Source Reports for Deep Dive:**
> - `reports/constant_product/rebalancevaultsassets-incorrectly-accounts-vaults-depositedusdc.md` (Zaros - Codehawks)
> - `reports/constant_product/incorrect-swap-amount-in-creditdelegationbranchsettlevaultsdebt-improperly-infla.md` (Zaros - Codehawks)

### Vulnerable Pattern Examples

**Example 1: Expected vs Actual Output Mismatch** [MEDIUM]
> 📖 Reference: `reports/constant_product/rebalancevaultsassets-incorrectly-accounts-vaults-depositedusdc.md`
```solidity
// ❌ VULNERABLE: Uses expected amount, not actual received
function rebalanceVaultsAssets() external {
    uint256 assetInputNative = dexAdapter.getExpectedOutput(usdc, collateralAsset, amount);
    
    dexSwapStrategy.executeSwapExactInputSingle(swapCallData); // Actual output differs!
    
    // Uses expected amount for accounting, not actual!
    uint128 usdDelta = depositAmountUsdX18.toUint128();
    inCreditVault.depositedUsdc += usdDelta;  // Wrong!
    inDebtVault.depositedUsdc -= usdDelta;    // Wrong!
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Track actual swap output
function rebalanceVaultsAssets() external {
    uint256 balanceBefore = IERC20(usdc).balanceOf(address(this));
    
    dexSwapStrategy.executeSwapExactInputSingle(swapCallData);
    
    uint256 actualReceived = IERC20(usdc).balanceOf(address(this)) - balanceBefore;
    
    // Use actual amounts for accounting
    inCreditVault.depositedUsdc += actualReceived;
    inDebtVault.depositedUsdc -= actualReceived;
}
```

---

## 18. Leftover Token Accumulation in Autocompounding

### Overview

Autocompounding vaults that swap reward tokens to LP tokens can accumulate leftover tokens when add liquidity operations fail due to slippage. If subsequent operations don't account for existing balances, the problem compounds over time.

> **📚 Source Reports for Deep Dive:**
> - `reports/constant_product/h-4-autocompoundingpodlp-_pairedlptokentopodlp-does-not-correctly-handle-leftove.md` (Peapods - Sherlock)
> - `reports/constant_product/m-16-inaccurate-swap-amount-calculation-in-relp-leads-to-stuck-tokens-and-lost-l.md` (Dopex - Code4rena)

### Vulnerable Pattern Examples

**Example 1: Snowballing Token Imbalance** [HIGH]
> 📖 Reference: `reports/constant_product/h-4-autocompoundingpodlp-_pairedlptokentopodlp-does-not-correctly-handle-leftove.md`
```solidity
// ❌ VULNERABLE: Doesn't consider existing balance before swap
function _getSwapAmt(uint256 pairedBalance) internal view returns (uint256) {
    // Ignores existing pTKN balance!
    return pairedBalance / 2;  // Always swaps half
}

// Problem:
// Epoch 1: 10000 pairedLpTKN → swap 5000 → 5000 pairedLpTKN, 5000 pTKN
// Add LP fails due to slippage
// Epoch 2: Still 5000 pairedLpTKN → swap 2500 → 2500 pairedLpTKN, 7500 pTKN
// Ratio becomes more imbalanced each epoch!
```

### Secure Implementation

```solidity
// ✅ SECURE: Account for existing balances
function _tokenToPodLp(address _token, uint256 _amountIn) internal returns (uint256) {
    uint256 existingPtknBalance = IERC20(ptkn).balanceOf(address(this));
    uint256 pairedBalance = _tokenToPairedLpToken(_token, _amountIn);
    
    // First pair existing pTKN with pairedLpTKN
    uint256 pairedForExisting = calculateOptimalPairing(existingPtknBalance, pairedBalance);
    
    // Only swap remaining after pairing
    uint256 remainingPaired = pairedBalance - pairedForExisting;
    uint256 swapAmount = _getSwapAmt(remainingPaired);
    // ...
}
```

---

## 19. WETH/ETH Pool Asset Mismatch

### Overview

When vaults interact with pools that use native ETH (like some Curve pools) but the vault's asset is WETH, unwrap/wrap operations can fail or cause accounting issues.

> **📚 Source Reports for Deep Dive:**
> - `reports/constant_product/m-22-setup-with-asset-weth-and-a-curve-pool-that-contains-native-eth-will-lead-t.md` (Notional - Sherlock)

### Vulnerable Pattern Examples

**Example 1: Native ETH Pool with WETH Asset** [MEDIUM]
> 📖 Reference: `reports/constant_product/m-22-setup-with-asset-weth-and-a-curve-pool-that-contains-native-eth-will-lead-t.md`
```solidity
// ❌ VULNERABLE: Pool uses ETH but vault holds WETH
function _unstakeAndExitPool() internal {
    // Curve pool returns native ETH
    pool.remove_liquidity(lpAmount, minAmounts);
    
    // Vault tries to use WETH balance - fails!
    uint256 balance = IERC20(WETH).balanceOf(address(this));
    // balance is 0, but we have ETH!
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Handle WETH/ETH conversion
function _unstakeAndExitPool() internal {
    pool.remove_liquidity(lpAmount, minAmounts);
    
    // If pool returns ETH, wrap it
    uint256 ethBalance = address(this).balance;
    if (ethBalance > 0 && asset == address(WETH)) {
        WETH.deposit{value: ethBalance}();
    }
}
```

---

## 20. Single-Sided vs Proportional Exit Confusion

### Overview

AMM exit types have different characteristics: proportional exits maintain token ratios with minimal slippage, while single-sided exits swap internally and incur slippage. Using the wrong exit type in emergency situations can result in significant fund loss.

> **📚 Source Reports for Deep Dive:**
> - `reports/constant_product/h-9-single-sided-instead-of-proportional-exit-is-performed-during-emergency-exit.md` (Notional - Sherlock)
> - `reports/constant_product/h-7-tokens-received-from-curves-remove_liquidity-should-be-added-to-the-assets-l.md` (Sentiment - Sherlock)

### Vulnerable Pattern Examples

**Example 1: Wrong Exit Type for Emergency** [HIGH]
> 📖 Reference: `reports/constant_product/h-9-single-sided-instead-of-proportional-exit-is-performed-during-emergency-exit.md`
```solidity
// ❌ VULNERABLE: Uses single-sided exit during emergency
function emergencyExit(uint256 claimToExit) external {
    // Comment says proportional, but isSingleSided = true!
    _unstakeAndExitPool(claimToExit, new uint256[](NUM_TOKENS()), true);
    // Single-sided exit incurs unnecessary slippage
    // Subject to front-running despite comment claiming otherwise
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Use proportional exit for emergencies
function emergencyExit(uint256 claimToExit) external {
    // Proportional exit - no slippage from internal swaps
    _unstakeAndExitPool(claimToExit, minAmounts, false); // isSingleSided = false
}

function _unstakeAndExitPool(uint256 poolClaim, uint256[] memory minAmounts, bool isSingleSided) internal {
    if (isSingleSided) {
        // EXACT_BPT_IN_FOR_ONE_TOKEN_OUT - has slippage
        customData = abi.encode(ExitKind.EXACT_BPT_IN_FOR_ONE_TOKEN_OUT, poolClaim, primaryIndex);
    } else {
        // EXACT_BPT_IN_FOR_TOKENS_OUT - proportional, minimal slippage
        customData = abi.encode(ExitKind.EXACT_BPT_IN_FOR_TOKENS_OUT, poolClaim);
    }
}
```

---

## 21. Type Casting & Integer Overflow Issues

### Overview

AMM implementations often require type conversions between different integer sizes (e.g., u64 to i64, uint256 to uint128). Unchecked type casting can lead to silent overflow/underflow, causing incorrect calculations, DoS conditions, or fund loss. This is particularly critical in price calculations and liquidity amount computations.

> **📚 Source Reports for Deep Dive:**
> - `reports/constant_product/unchecked-type-casting.md` (Raydium AMM V3 - OtterSec)
> - `reports/constant_product/denial-of-service-conditions-caused-by-the-use-of-more-than-256-slices.md` (Shell Protocol - TrailOfBits)

### Vulnerability Description

#### Root Cause

When casting from larger integer types to smaller ones without validation:
- `u64::MAX` cast to `i64` produces a negative number
- `uint256` values exceeding type limits silently truncate
- Loop counters with `uint8` overflow at 256 iterations

### Vulnerable Pattern Examples

**Example 1: Unchecked u64 to i64 Conversion** [HIGH]
> 📖 Reference: `reports/constant_product/unchecked-type-casting.md`
```rust
// ❌ VULNERABLE: u64 may exceed i64::MAX
pub fn get_delta_amount_0_signed(
    sqrt_ratio_a_x64: u128,
    sqrt_ratio_b_x64: u128,
    liquidity: i128,
) -> i64 {
    if liquidity < 0 {
        -(get_delta_amount_0_unsigned(
            sqrt_ratio_a_x64,
            sqrt_ratio_b_x64,
            -liquidity as u128,
            false,
        ) as i64)  // ❌ Unchecked cast - can overflow!
    } else {
        get_delta_amount_0_unsigned(sqrt_ratio_a_x64, sqrt_ratio_b_x64,
            liquidity as u128, true) as i64  // ❌ u64::MAX > i64::MAX
    }
}
```

**Example 2: uint8 Loop Counter Overflow** [HIGH]
> 📖 Reference: `reports/constant_product/denial-of-service-conditions-caused-by-the-use-of-more-than-256-slices.md`
```solidity
// ❌ VULNERABLE: uint8 can only go up to 255
function _findSlice(int128 m) internal view returns (uint8 i) {
    i = 0;
    while (i < slices.length) {  // If slices.length > 256, infinite loop!
        if (m <= slices[i].mLeft && m > slices[i].mRight) return i;
        unchecked {
            ++i;  // Overflows at 256, restarts from 0
        }
    }
    return i - 1;
}
```

### Secure Implementation

```rust
// ✅ SECURE: Use try_from with error handling
pub fn get_delta_amount_0_signed(
    sqrt_ratio_a_x64: u128,
    sqrt_ratio_b_x64: u128,
    liquidity: i128,
) -> Result<i64, Error> {
    let unsigned_result = get_delta_amount_0_unsigned(
        sqrt_ratio_a_x64,
        sqrt_ratio_b_x64,
        liquidity.unsigned_abs(),
        liquidity >= 0,
    );
    
    // Safe conversion with error handling
    let signed_result = i64::try_from(unsigned_result)
        .map_err(|_| Error::Overflow)?;
    
    if liquidity < 0 {
        Ok(-signed_result)
    } else {
        Ok(signed_result)
    }
}
```

```solidity
// ✅ SECURE: Use uint256 for array iteration
function _findSlice(int128 m) internal view returns (uint256 i) {
    require(slices.length <= type(uint256).max, "Too many slices");
    
    for (i = 0; i < slices.length; i++) {
        if (m <= slices[i].mLeft && m > slices[i].mRight) return i;
    }
    return slices.length - 1;
}
```

---

## 22. Spot Price Abuse in Protocol Swaps

### Overview

When protocols perform internal swaps using DEX spot prices without oracle validation, attackers can manipulate the spot price via sandwich attacks to drain protocol funds. This is especially critical for sponsor vaults, debt repayment, and other protocol-initiated swaps.

> **📚 Source Reports for Deep Dive:**
> - `reports/constant_product/use-of-spot-price-in-sponsorvault-leads-to-sandwich-attack.md` (Connext - Spearbit)
> - `reports/constant_product/use-of-spot-dex-price-when-repay-portal-debt-leads-to-sandwich-attacks.md` (Various)

### Vulnerability Description

#### Root Cause

Protocol contracts that:
1. Calculate swap amounts using current DEX spot price
2. Execute swaps without comparing to oracle price
3. Don't have slippage protection on protocol-initiated swaps

### Vulnerable Pattern Examples

**Example 1: Sponsor Vault Spot Price Swap** [CRITICAL]
> 📖 Reference: `reports/constant_product/use-of-spot-price-in-sponsorvault-leads-to-sandwich-attack.md`
```solidity
// ❌ VULNERABLE: Uses spot price for swap amount calculation
contract SponsorVault {
    function reimburseLiquidityFees(
        address _token,
        uint256 _liquidityFee,
        address _receiver
    ) external onlyConnext returns (uint256) {
        // Spot price can be manipulated!
        uint256 amountIn = tokenExchange.getInGivenExpectedOut(_token, _liquidityFee);
        amountIn = currentBalance >= amountIn ? amountIn : currentBalance;
        
        // Attacker manipulates DEX: 1 ETH = 0.1 USDC
        // Protocol pays 1000 ETH for 100 USDC
        sponsoredFee = tokenExchange.swapExactIn{value: amountIn}(_token, msg.sender);
    }
}
```

**Attack Scenario:**
1. Attacker manipulates DEX to make native token (ETH) appear cheap: 1 ETH = 0.1 USDC
2. `getInGivenExpectedOut` returns 1000 (ETH needed for 100 USDC)
3. SponsorVault buys 100 USDC with 1000 ETH
4. Price drops further, attacker buys cheap ETH
5. Repeat until vault is drained

### Secure Implementation

```solidity
// ✅ SECURE: Validate spot price against oracle
contract SponsorVault {
    uint256 public constant MAX_DEVIATION = 500; // 5%
    
    function reimburseLiquidityFees(
        address _token,
        uint256 _liquidityFee,
        address _receiver
    ) external onlyConnext returns (uint256) {
        // Get oracle price
        uint256 oraclePrice = priceOracle.getPrice(_token, USDC);
        
        // Get spot price
        uint256 spotPrice = tokenExchange.getSpotPrice(_token);
        
        // Compare and revert if deviation too high
        uint256 deviation = _calculateDeviation(oraclePrice, spotPrice);
        require(deviation <= MAX_DEVIATION, "Price deviation too high");
        
        // Use oracle price for calculation
        uint256 amountIn = (_liquidityFee * 1e18) / oraclePrice;
        
        // Execute with slippage protection
        uint256 minOut = _liquidityFee * (10000 - MAX_DEVIATION) / 10000;
        sponsoredFee = tokenExchange.swapExactIn{value: amountIn}(
            _token, 
            msg.sender,
            minOut  // Slippage protection
        );
    }
}
```

---

## 23. LP Token Burn/Hijack Attacks

### Overview

When LP token `burn()` functions are unrestricted or LP tokens are sent to the wrong contract during redemption, attackers can manipulate total supply to steal deposits or permanently lock funds. This includes scenarios where burning reduces total supply to manipulate share prices.

> **📚 Source Reports for Deep Dive:**
> - `reports/constant_product/h-10-hijack-token-pool-by-burning-liquidity-token.md` (Spartan Protocol - Code4rena)
> - `reports/constant_product/the-lp-tokens-are-never-burned-by-the-stream-pool-contract.md` (PixelSwap - TrailOfBits)

### Vulnerability Description

#### Root Cause

1. Public `burn()` function without withdrawal logic
2. Sending burn message to master contract instead of wallet
3. No minimum supply enforcement after burns

### Vulnerable Pattern Examples

**Example 1: Pool Hijack via LP Burn** [HIGH]
> 📖 Reference: `reports/constant_product/h-10-hijack-token-pool-by-burning-liquidity-token.md`
```solidity
// ❌ VULNERABLE: Unrestricted burn allows totalSupply manipulation
contract Pool {
    // Public burn without requiring liquidity withdrawal
    function burn(uint256 amount) external {
        _burn(msg.sender, amount);
        // No tokens are withdrawn - just LP destroyed
    }
}

// Attack scenario:
// 1. Attacker creates pool, deposits minimal (1 wei each token)
// 2. Receives 1 LP token
// 3. Burns all but 1 wei of LP: burn(init_amount - 1)
// 4. Now totalSupply = 1, but reserves can be inflated via donation
// 5. New deposits round to 0 LP tokens
// Formula: units = P * (part1 + part2) / part3
// When P (totalSupply) = 1, all calculations round down
```

**Example 2: LP Tokens Never Burned** [HIGH]
> 📖 Reference: `reports/constant_product/the-lp-tokens-are-never-burned-by-the-stream-pool-contract.md`
```solidity
// ❌ VULNERABLE: Burn message sent to master, not wallet
contract JettonFactory {
    function burn(uint256 amount, address user) internal {
        // Wrong! Sending to Jetton master instead of Jetton wallet
        send(
            jettonMaster,  // ❌ Should be jettonWallet
            TokenBurn { amount: amount, ... }
        );
        // Burn fails silently (bounce = false), LP tokens remain
    }
}
// Impact: Users remove liquidity but LP tokens accumulate in pool
```

### Secure Implementation

```solidity
// ✅ SECURE: Burn only through withdrawal with minimum enforced
contract Pool {
    uint256 public constant MINIMUM_LIQUIDITY = 1000;
    
    // No public burn - only through withdraw
    function withdraw(uint256 lpAmount) external {
        require(totalSupply() - lpAmount >= MINIMUM_LIQUIDITY, "Below minimum");
        
        // Calculate tokens to return
        uint256 token0Out = (lpAmount * reserve0) / totalSupply();
        uint256 token1Out = (lpAmount * reserve1) / totalSupply();
        
        // Burn LP tokens
        _burn(msg.sender, lpAmount);
        
        // Transfer underlying tokens
        token0.transfer(msg.sender, token0Out);
        token1.transfer(msg.sender, token1Out);
    }
}
```

---

## 24. Constant Sum AMM Arbitrage

### Overview

Constant sum AMMs (x + y = k) maintain a fixed exchange rate regardless of reserve imbalance. While simple, they are fundamentally vulnerable to unlimited arbitrage when token prices diverge in external markets, allowing attackers to completely drain one side of the pool.

> **📚 Source Reports for Deep Dive:**
> - `reports/constant_product/unlimited-arbitrage-in-ccfrax1to1amm.md` (Frax - TrailOfBits)

### Vulnerability Description

#### Root Cause

Constant sum invariant: `k = a + b`

Unlike x*y=k (constant product), the price doesn't change with reserves. If external markets show even slight price deviation:
- Buy the relatively cheaper token from AMM at 1:1
- Sell on external market for profit
- Repeat until pool is fully imbalanced

### Vulnerable Pattern Examples

**Example 1: 1:1 Stablecoin AMM Drain** [HIGH]
> 📖 Reference: `reports/constant_product/unlimited-arbitrage-in-ccfrax1to1amm.md`
```solidity
// ❌ VULNERABLE: Constant sum AMM with 1:1 rate
contract CCFrax1to1AMM {
    // Invariant: k = frax_balance + token_balance
    // Price is always 1:1 regardless of reserves!
    
    function swap(address tokenIn, uint256 amountIn) external {
        // Always swaps 1:1 (minus fees)
        uint256 amountOut = amountIn * (10000 - swapFee) / 10000;
        // No price impact from reserve ratio!
    }
}

// Attack scenario with price_tolerance = 0.05:
// 1. External market: FRAX = 1.005 USD, Token T = 0.995 USD
// 2. Attacker buys 100,000 T from external market
// 3. Swaps all T for FRAX at 1:1 in AMM
// 4. Sells FRAX on external market at 1.005
// 5. Profit: ~$960 per 100k, pool is now 100% T
// 6. AMM is completely drained of FRAX
```

### Secure Implementation

```solidity
// ✅ SECURE: Use constant product or stableswap invariant
contract StableSwapAMM {
    // Curve-style stableswap invariant provides:
    // - Low slippage near peg
    // - High slippage when imbalanced (arbitrage limiting)
    
    function swap(address tokenIn, uint256 amountIn) external {
        // Calculate using stableswap invariant
        uint256 amountOut = _calculateStableSwap(amountIn);
        
        // Price impact increases as pool becomes imbalanced
        // This naturally limits arbitrage profitability
    }
}

// Alternative: Don't use constant sum for significant funds
// Use Curve pools or proven stableswap implementations
```

---

## 25. State Accounting Discrepancies

### Overview

AMM protocols track various state variables (minted tokens, removed tokens, fees, balances) that must remain synchronized. When update logic incorrectly modifies these variables, the protocol's invariants break, leading to incorrect emissions, limit calculations, or fund access issues.

> **📚 Source Reports for Deep Dive:**
> - `reports/constant_product/m-8-singlesidedliquidityvaultwithdraw-will-decreases-ohmminted-which-will-make-t.md` (Olympus - Sherlock)
> - `reports/constant_product/h-05-parameter-misordering-in-fee-collection-function-causes-denial-of-service-a.md` (Superposition - Code4rena)

### Vulnerability Description

#### Root Cause

State variables are updated incorrectly:
- Subtraction from wrong counter (e.g., reducing `minted` instead of increasing `removed`)
- Parameter misordering in function calls
- Missing state updates in certain code paths

### Vulnerable Pattern Examples

**Example 1: Wrong Counter Updated on Withdraw** [MEDIUM]
> 📖 Reference: `reports/constant_product/m-8-singlesidedliquidityvaultwithdraw-will-decreases-ohmminted-which-will-make-t.md`
```solidity
// ❌ VULNERABLE: Decreases ohmMinted instead of increasing ohmRemoved
contract SingleSidedLiquidityVault {
    uint256 public ohmMinted;   // Should only increase on deposit
    uint256 public ohmRemoved;  // Should only increase on withdraw
    
    function withdraw(uint256 lpAmount) external {
        (uint256 ohmReceived, ) = _withdraw(lpAmount, minTokenAmounts);
        
        // ❌ Wrong! This decreases minted instead of increasing removed
        ohmMinted -= ohmReceived > ohmMinted ? ohmMinted : ohmReceived;
        ohmRemoved += ohmReceived > ohmMinted ? ohmReceived - ohmMinted : 0;
        
        // Result: After deposit 100, withdraw 100:
        // ohmMinted = 0, ohmRemoved = 0
        // But should be: ohmMinted = 100, ohmRemoved = 100
        // _canDeposit and getOhmEmissions now return wrong values
    }
}
```

**Example 2: Parameter Misordering in Fee Transfer** [HIGH]
> 📖 Reference: `reports/constant_product/h-05-parameter-misordering-in-fee-collection-function-causes-denial-of-service-a.md`
```rust
// ❌ VULNERABLE: Token and recipient swapped
pub fn collect_protocol_fees(pool: Address, recipient: Address) {
    // Function signature: transfer_to_addr(token, recipient, amount)
    // But called with: (recipient, pool, amount) ← WRONG!
    erc20::transfer_to_addr(recipient, pool, token_0)?;  // ❌
    erc20::transfer_to_addr(recipient, FUSDC_ADDR, token_1)?;  // ❌
    // Transaction reverts, fees permanently stuck
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Clear separation of minted vs removed tracking
contract SingleSidedLiquidityVault {
    uint256 public ohmMinted;
    uint256 public ohmRemoved;
    
    function deposit(uint256 pairTokenAmount) external {
        uint256 ohmToMint = _calculateOhmAmount(pairTokenAmount);
        ohmMinted += ohmToMint;  // Only minted increases here
    }
    
    function withdraw(uint256 lpAmount) external {
        (uint256 ohmReceived, ) = _withdraw(lpAmount, minTokenAmounts);
        ohmRemoved += ohmReceived;  // Only removed increases here
        // ohmMinted stays unchanged!
    }
    
    function getOhmEmissions() external view returns (uint256 emitted, uint256 removed) {
        // Now correctly reflects: minted - removed = net emissions
        return (ohmMinted, ohmRemoved);
    }
}
```

---

## 26. Incorrect Liquidity Ownership Assumptions

### Overview

Protocols that integrate with external AMMs sometimes incorrectly assume they own all liquidity in a pool. This leads to calculations based on total pool reserves rather than the protocol's actual LP share, causing DoS or fund loss when other LPs exist.

> **📚 Source Reports for Deep Dive:**
> - `reports/constant_product/h-09-relpcontract-wrongfully-assumes-protocol-owns-all-of-the-liquidity-in-the-u.md` (Dopex - Code4rena)

### Vulnerability Description

#### Root Cause

Protocol calculates:
```
lpToRemove = (tokenToRemove * totalLpSupply) / totalReserve
```

But if protocol only owns a fraction of the pool, `lpToRemove` exceeds protocol's LP balance.

### Vulnerable Pattern Examples

**Example 1: Assuming 100% Pool Ownership** [HIGH]
> 📖 Reference: `reports/constant_product/h-09-relpcontract-wrongfully-assumes-protocol-owns-all-of-the-liquidity-in-the-u.md`
```solidity
// ❌ VULNERABLE: Uses total pool reserves, not owned portion
contract ReLPContract {
    function reLP(uint256 _amount) external {
        // Gets TOTAL pool reserves (all LPs combined)
        (uint256 reserveA, uint256 reserveB) = UniswapV2Library.getReserves(
            addresses.ammFactory,
            tokenASorted,
            tokenBSorted
        );
        
        // Calculate based on total reserves
        uint256 tokenAToRemove = ((_amount * tokenALpReserve * baseReLpRatio) / ...);
        
        // Calculate LP needed - based on TOTAL supply!
        uint256 totalLpSupply = IUniswapV2Pair(addresses.pair).totalSupply();
        uint256 lpToRemove = (tokenAToRemove * totalLpSupply) / tokenALpReserve;
        
        // ❌ REVERTS if lpToRemove > protocol's actual LP balance!
        IERC20(addresses.pair).transferFrom(addresses.amo, address(this), lpToRemove);
    }
}

// Attack scenario:
// 1. Protocol owns 10% of pool LP (100 LP of 1000 total)
// 2. User deposits enough to trigger reLP requiring 200 LP removal
// 3. Protocol tries to transferFrom 200 LP but only has 100
// 4. Transaction reverts - complete DoS of bonding functionality
```

### Secure Implementation

```solidity
// ✅ SECURE: Base calculations on protocol's actual LP holdings
contract ReLPContract {
    function reLP(uint256 _amount) external {
        uint256 protocolLpBalance = IERC20(addresses.pair).balanceOf(addresses.amo);
        uint256 totalLpSupply = IUniswapV2Pair(addresses.pair).totalSupply();
        
        // Calculate protocol's SHARE of reserves
        (uint256 totalReserveA, ) = UniswapV2Library.getReserves(...);
        uint256 protocolReserveA = (totalReserveA * protocolLpBalance) / totalLpSupply;
        
        // Calculate based on OWNED reserves only
        uint256 tokenAToRemove = ((_amount * protocolReserveA * baseReLpRatio) / ...);
        
        // LP to remove from owned balance
        uint256 lpToRemove = (tokenAToRemove * protocolLpBalance) / protocolReserveA;
        
        // Sanity check
        require(lpToRemove <= protocolLpBalance, "Insufficient LP");
        
        IERC20(addresses.pair).transferFrom(addresses.amo, address(this), lpToRemove);
    }
}
```

---

## 27. Dividend/Reward Gaming

### Overview

AMM protocols with dividend or reward distribution based on recent trading activity can be gamed by manipulating the baseline metrics. Attackers execute many tiny trades to skew the average fee calculation, then capture inflated dividends.

> **📚 Source Reports for Deep Dive:**
> - `reports/constant_product/h-08-dividend-reward-can-be-gamed.md` (Spartan Protocol - Code4rena)

### Vulnerability Description

#### Root Cause

Dividend calculation uses short-term fee averages:
- Only last N trades (e.g., 20) are considered
- Zero-fee trades can reset the average to 0
- Large dividend allocated relative to manipulated baseline

### Vulnerable Pattern Examples

**Example 1: Gaming Dividend via Small Trades** [HIGH]
> 📖 Reference: `reports/constant_product/h-08-dividend-reward-can-be-gamed.md`
```solidity
// ❌ VULNERABLE: normalAverageFee based on last 20 trades only
contract Router {
    uint256 constant arrayFeeSize = 20;
    uint256 public normalAverageFee;
    
    function addTradeFee(uint256 fee) internal {
        fees[feeIndex] = fee;
        feeIndex = (feeIndex + 1) % arrayFeeSize;
        normalAverageFee = _calculateAverage(fees);
    }
    
    function addDividend(uint256 _fees) external {
        // Dividend = _fees * dailyAllocation / (_fees + normalAverageFee)
        uint256 feeDividend = (_fees * dailyAllocation) / (_fees + normalAverageFee);
        // If normalAverageFee = 0, feeDividend = dailyAllocation!
        reserve.sendDividend(pool, feeDividend);
    }
}

// Attack:
// 1. Become large LP holder in smallest curated pool
// 2. Execute 20 trades of 1 wei each (0 fees) → normalAverageFee = 0
// 3. Execute trade with some fees → feeDividend = _fees * daily / (2 * _fees) = daily/2
// 4. Capture half of daily allocation per attack
// 5. Repeat until reserve is drained
```

### Secure Implementation

```solidity
// ✅ SECURE: Use time-weighted volume, not individual trade count
contract Router {
    mapping(address => uint256) public poolVolumeDaily;
    mapping(address => uint256) public poolLastUpdate;
    
    function recordTrade(address pool, uint256 volume) internal {
        // Reset daily volume if new day
        if (block.timestamp / 1 days > poolLastUpdate[pool] / 1 days) {
            poolVolumeDaily[pool] = 0;
        }
        poolVolumeDaily[pool] += volume;
        poolLastUpdate[pool] = block.timestamp;
    }
    
    function addDividend(address pool, uint256 _fees) external {
        // Base dividend on actual 24h volume, not manipulable averages
        uint256 poolVolume = poolVolumeDaily[pool];
        uint256 totalVolume = getTotalDailyVolume();
        
        // Pool gets proportional share of daily allocation
        uint256 feeDividend = (dailyAllocation * poolVolume) / totalVolume;
        
        // Minimum threshold to prevent gaming
        require(poolVolume >= MIN_VOLUME_THRESHOLD, "Volume too low");
        
        reserve.sendDividend(pool, feeDividend);
    }
}
```

---

## 28. Missing Account Validation (Solana-Specific)

### Overview

Solana programs must validate all passed accounts to ensure they are the expected PDAs or token accounts. Missing validation on reward vault or LP token accounts allows attackers to substitute arbitrary accounts and drain funds.

> **📚 Source Reports for Deep Dive:**
> - `reports/constant_product/missing-tokenaccount-checks.md` (Raydium Staking - OtterSec)

### Vulnerability Description

#### Root Cause

Solana accounts are passed as parameters; the program must verify:
- Account derivation (PDA seeds)
- Account ownership
- Token mint matches expected

### Vulnerable Pattern Examples

**Example 1: Unvalidated Reward Vault in Withdrawal** [HIGH]
> 📖 Reference: `reports/constant_product/missing-tokenaccount-checks.md`
```rust
// ❌ VULNERABLE: No validation on vault_reward_token_b_info
pub fn withdraw_v2(ctx: Context<WithdrawV2>) -> Result<()> {
    let dest_reward_token_b_info = next_account_info(account_info_iter)?;
    let vault_reward_token_b_info = next_account_info(account_info_iter)?;
    // ❌ No checks on vault_reward_token_b_info!
    
    if pending_b > 0 {
        // Attacker passes LP token vault as vault_reward_token_b_info
        Self::token_transfer_with_authority(
            stake_pool_info.key,
            token_program_info.clone(),
            vault_reward_token_b_info.clone(),  // ❌ Could be any vault!
            dest_reward_token_b_info.clone(),
            authority_info.clone(),
            stake_pool.nonce as u8,
            pending_b
        )?;
    }
}

// Attack:
// 1. Deposit 1000 LP tokens to farm
// 2. Wait for rewards to accumulate (any amount works)
// 3. Call withdraw with vault_reward_token_b = LP_token_vault
// 4. Receive LP tokens instead of reward tokens
// 5. In one day, attacker can 20x their deposit in BTC-stSOL farm
```

### Secure Implementation

```rust
// ✅ SECURE: Validate all accounts against expected PDAs
#[derive(Accounts)]
pub struct WithdrawV2<'info> {
    #[account(
        mut,
        seeds = [b"reward_vault_a", stake_pool.key().as_ref()],
        bump,
        token::mint = reward_mint_a,
        token::authority = pool_authority,
    )]
    pub vault_reward_a: Account<'info, TokenAccount>,
    
    #[account(
        mut,
        seeds = [b"reward_vault_b", stake_pool.key().as_ref()],
        bump,
        token::mint = reward_mint_b,  // ✅ Validates mint matches
        token::authority = pool_authority,  // ✅ Validates authority
    )]
    pub vault_reward_b: Account<'info, TokenAccount>,
    
    #[account(
        seeds = [b"lp_vault", stake_pool.key().as_ref()],
        bump,
        token::mint = lp_mint,
        token::authority = pool_authority,
    )]
    pub lp_vault: Account<'info, TokenAccount>,  // ✅ Separate from reward vaults
}
```

---

## 29. Detection Patterns & Audit Checklist

### Code Patterns to Look For

```
- Pattern 1: `slot0()` or `getReserves()` used for pricing without TWAP
- Pattern 2: Missing `amountOutMin` or set to 0
- Pattern 3: No `deadline` parameter in swap functions
- Pattern 4: First deposit without MINIMUM_LIQUIDITY burn
- Pattern 5: `balanceOf(address(this))` used in critical calculations
- Pattern 6: Missing decimal normalization in multi-token calculations
- Pattern 7: Unrestricted `burn()` function on LP tokens
- Pattern 8: Unrestricted callback functions (mintCallback, swapCallback)
- Pattern 9: Deterministic addresses with CREATE opcode
- Pattern 10: Pool existence checked via balanceOf instead of factory.getPair
- Pattern 11: Hardcoded init_code_hash for pair address computation
- Pattern 12: Migration functions using raw balanceOf
- Pattern 13: Atomic graduation + unwrap without time locks
- Pattern 14: Missing nonReentrant modifiers on swap paths
- Pattern 15: LP token minting without checking optimal amounts
- Pattern 16: Rebasing tokens stored as static balances
- Pattern 17: IL protection without token whitelisting
- Pattern 18: Expected swap output used instead of actual received
- Pattern 19: Existing token balances ignored before swap calculations
- Pattern 20: WETH vault interacting with native ETH pools
- Pattern 21: Single-sided exit used where proportional is needed
- Pattern 22: `as i64` or `as uint128` without try_from validation
- Pattern 23: uint8 used as loop counter for arrays > 255 elements
- Pattern 24: Protocol swaps using getInGivenExpectedOut without oracle check
- Pattern 25: Public burn() without corresponding withdrawal
- Pattern 26: Constant sum (x+y=k) invariant used for stablecoins
- Pattern 27: State counters modified with wrong operation (+/- confusion)
- Pattern 28: Parameter ordering swapped in transfer/approve calls
- Pattern 29: Calculations using pool.totalSupply when protocol owns partial LP
- Pattern 30: Dividend based on last N trades instead of time-weighted volume
- Pattern 31: (Solana) next_account_info without seed/mint validation
```

### Audit Checklist

- [ ] First depositor attack: Is MINIMUM_LIQUIDITY burned?
- [ ] Slippage: Is amountOutMin enforced and non-zero?
- [ ] Deadline: Can users specify transaction expiry?
- [ ] Price source: Is TWAP used instead of spot price?
- [ ] Reserve manipulation: Are reserves time-weighted?
- [ ] LP calculation: Are token decimals handled correctly?
- [ ] MEV protection: Are critical operations protected?
- [ ] Donation attack: Does balanceOf include donated tokens?
- [ ] Burn function: Is LP burning restricted?
- [ ] Sync function: Can attackers manipulate reserves via sync()?
- [ ] Imbalanced LP addition: Are optimal amounts calculated before adding liquidity?
- [ ] Rebasing tokens: Are rebasing token balances tracked properly?
- [ ] IL protection: Is token pair whitelisted for protection?
- [ ] Swap accounting: Is actual output used, not expected?
- [ ] Leftover tokens: Are existing balances considered in autocompounding?
- [ ] ETH/WETH: Does vault handle native ETH pool interactions?
- [ ] Exit types: Is proportional exit used for emergency withdrawals?
- [ ] Protocol invariants: Is totalSupply consistent with calculated LP from reserves?
- [ ] **NEW**: Type casting: Are u64→i64, uint256→uint128 casts checked?
- [ ] **NEW**: Loop bounds: Are loop counters sized for array lengths?
- [ ] **NEW**: Spot price swaps: Do protocol-initiated swaps validate against oracle?
- [ ] **NEW**: LP burn hijack: Is burn() tied to withdrawal only?
- [ ] **NEW**: AMM curve: Is constant-sum avoided for real assets?
- [ ] **NEW**: State counters: Are mint/burn/remove counters updated correctly?
- [ ] **NEW**: Parameter order: Are token/recipient parameters in correct order?
- [ ] **NEW**: LP ownership: Does protocol track its own LP share vs total pool?
- [ ] **NEW**: Dividend gaming: Is reward calculation resistant to small trades?
- [ ] **NEW**: (Solana) Account validation: Are all PDAs and mints verified?

### Keywords for Search

`constant_product`, `x*y=k`, `amm`, `uniswap`, `liquidity_pool`, `swap`, `slippage`, `sandwich_attack`, `mev`, `front_running`, `back_running`, `flash_loan`, `price_manipulation`, `slot0`, `sqrtPriceX96`, `twap`, `reserves`, `getReserves`, `first_depositor`, `inflation_attack`, `minimum_liquidity`, `lp_token`, `deadline`, `amountOutMin`, `price_impact`, `impermanent_loss`, `arbitrage`, `dex`, `swap_router`, `pair`, `factory`, `rebasing_token`, `atoken`, `autocompound`, `emergency_exit`, `proportional_exit`, `single_sided_exit`, `invariant`, `weth_eth_mismatch`, `leftover_tokens`, `type_casting`, `overflow`, `uint8_loop`, `constant_sum`, `sponsor_vault`, `lp_burn`, `hijack`, `dividend_gaming`, `parameter_order`, `ownership_assumption`, `pda_validation`, `token_account`

---

## Related Vulnerabilities

- [ERC4626 First Depositor Attack](../../tokens/erc4626/FIRST_DEPOSITOR_INFLATION_ATTACK.md) - Similar pattern in vault shares
- [Oracle Price Manipulation](../../oracle/chainlink/CHAINLINK_VULNERABILITIES.md) - Price feed attacks
- [Flash Loan Attacks](../../economic/FLASH_LOAN_ATTACKS.md) - Enabling mechanism for many AMM attacks

---

## DeFiHackLabs Real-World Exploits (2 incidents)

**Category**: K Value Manipulation | **Total Losses**: $498K | **Sub-variants**: 1

### Sub-variant Breakdown

#### K-Value-Manipulation/Generic (2 exploits, $498K)

- **Swapos V2** (2023-04, $468K, ethereum) | PoC: `DeFiHackLabs/src/test/2023-04/Swapos_exp.sol`
- **LinkDAO** (2023-11, $30K, bsc) | PoC: `DeFiHackLabs/src/test/2023-11/LinkDao_exp.sol`

### Complete DeFiHackLabs Exploit Table

| Protocol | Date | Loss | Vulnerability Sub-type | Chain |
|----------|------|------|----------------------|-------|
| Swapos V2 | 2023-04-16 | $468K | error k value Attack | ethereum |
| LinkDAO | 2023-11-15 | $30K | Bad `K` Value Verification | bsc |

### Top PoC References

- **Swapos V2** (2023-04, $468K): `DeFiHackLabs/src/test/2023-04/Swapos_exp.sol`
- **LinkDAO** (2023-11, $30K): `DeFiHackLabs/src/test/2023-11/LinkDao_exp.sol`

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

`LP_tokens`, `TWAP`, `_addLiquidity`, `_deployToken`, `_executeTrade`, `_existsPairPool`, `_findSlice`, `_getSwapAmt`, `_getTimeWeightedPrimaryBalance`, `_graduate`, `_tokenToPodLp`, `_transfer`, `_unstakeAndExitPool`, `addDividend`, `addLiquidity`, `addQuote`, `addTradeFee`, `amm`, `approve`, `balanceOf`, `block.timestamp`, `constant_product`, `constant_product_amm_integration`, `deadline_check`, `defi`, `dex`, `front_running`, `getReserves`, `k_invariant`, `liquidity`, `liquidity_provision`, `mev`, `minimum_liquidity`, `price_calculation`, `reserves`, `sandwich_attack`, `slippage_protection`, `slot0`, `spot_price`, `sqrtPriceX96`, `swap`, `swap_execution`, `uniswap`
