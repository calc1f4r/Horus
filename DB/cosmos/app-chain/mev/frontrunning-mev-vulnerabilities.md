---
protocol: generic
chain: cosmos
category: mev
vulnerability_type: frontrunning_mev_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: mev_logic

primitives:
  - staking_frontrun
  - price_update
  - slippage_exploit
  - sandwich
  - block_stuffing
  - arbitrage
  - priority
  - jit_liquidity

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - mev
  - staking
  - defi

language: go|solidity|rust
version: all

# Pattern Identity (Required)
root_cause_family: missing_frontrun_protection
pattern_key: missing_frontrun_protection | mev_logic | frontrunning_mev_vulnerabilities

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - _decodeAndReward
  - addLiquidityOneETHKeepYt
  - arbitrage
  - balanceOf
  - block.number
  - block.timestamp
  - block_stuffing
  - checkpointProtection
  - deposit
  - getPrice
  - jit_liquidity
  - liquidate
  - mint
  - msg.sender
  - price_update
  - priority
  - receive
  - repay
  - safeTransferFrom
  - sandwich
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Mev Staking Frontrun
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-01] User can earn rewards by frontrunning the new rewards | `reports/cosmos_cometbft_findings/m-01-user-can-earn-rewards-by-frontrunning-the-new-rewards-accumulation-in-ron-s.md` | MEDIUM | Code4rena |
| `slash` calls can be blocked, allowing malicious users to by | `reports/cosmos_cometbft_findings/m-2-slash-calls-can-be-blocked-allowing-malicious-users-to-bypass-the-slashing-m.md` | MEDIUM | Sherlock |
| [M-27] rotateNodeRunnerOfSmartWallet is vulnerable to a fron | `reports/cosmos_cometbft_findings/m-27-rotatenoderunnerofsmartwallet-is-vulnerable-to-a-frontrun-attack.md` | MEDIUM | Code4rena |
| `slash()` can be frontrunned to avoid the penalty imposed on | `reports/cosmos_cometbft_findings/m-5-slash-can-be-frontrunned-to-avoid-the-penalty-imposed-on-them.md` | MEDIUM | Sherlock |

### Mev Slippage Exploit
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-04] Withdrawals logic allows MEV exploits of TVL changes  | `reports/cosmos_cometbft_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md` | HIGH | Code4rena |
| [M-01] Missing slippage protection in `AerodromeDexter.sol`  | `reports/cosmos_cometbft_findings/m-01-missing-slippage-protection-in-aerodromedextersol-swapexacttokensfortokens.md` | MEDIUM | Code4rena |
| Slippage on `MetapoolRouter.addLiquidityOneETHKeepYt` | `reports/cosmos_cometbft_findings/m-5-slippage-on-metapoolrouteraddliquidityoneethkeepyt.md` | MEDIUM | Sherlock |
| Missing slippage protection in liquidation allows unexpected | `reports/cosmos_cometbft_findings/m-9-missing-slippage-protection-in-liquidation-allows-unexpected-collateral-loss.md` | MEDIUM | Sherlock |
| Missing Tick and Liquidity Checks in _decodeAndReward (curre | `reports/cosmos_cometbft_findings/missing-tick-and-liquidity-checks-in-_decodeandreward-currentonlytrue-enables-fr.md` | MEDIUM | Cantina |
| [PRST-6] First depositor can steal assets due to missing sli | `reports/cosmos_cometbft_findings/prst-6-first-depositor-can-steal-assets-due-to-missing-slippage-protection.md` | HIGH | Hexens |

### Mev Sandwich
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-04] Withdrawals logic allows MEV exploits of TVL changes  | `reports/cosmos_cometbft_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md` | HIGH | Code4rena |
| [M-01] Missing slippage protection in `AerodromeDexter.sol`  | `reports/cosmos_cometbft_findings/m-01-missing-slippage-protection-in-aerodromedextersol-swapexacttokensfortokens.md` | MEDIUM | Code4rena |
| A part of ETH rewards can be stolen by sandwiching `claimDel | `reports/cosmos_cometbft_findings/m-3-a-part-of-eth-rewards-can-be-stolen-by-sandwiching-claimdelayedwithdrawals.md` | MEDIUM | Sherlock |

### Mev Block Stuffing
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-16] Auction manipulation by block stuffing and reverting  | `reports/cosmos_cometbft_findings/m-16-auction-manipulation-by-block-stuffing-and-reverting-on-erc-777-hooks.md` | MEDIUM | Code4rena |

### Mev Arbitrage
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-01] Possible arbitrage from Chainlink price discrepancy | `reports/cosmos_cometbft_findings/h-01-possible-arbitrage-from-chainlink-price-discrepancy.md` | HIGH | Code4rena |
| [H-08] Exchange rate calculation is incorrect | `reports/cosmos_cometbft_findings/h-08-exchange-rate-calculation-is-incorrect.md` | HIGH | Pashov Audit Group |
| [M-02] `MsgSwapOrder` will never work for Canto nodes | `reports/cosmos_cometbft_findings/m-02-msgswaporder-will-never-work-for-canto-nodes.md` | MEDIUM | Code4rena |
| [M-04] Arbitrage on `stake()` | `reports/cosmos_cometbft_findings/m-04-arbitrage-on-stake.md` | MEDIUM | Code4rena |
| [M-14] stETH/ETH feed being used opens up to 2 way `deposit< | `reports/cosmos_cometbft_findings/m-14-stetheth-feed-being-used-opens-up-to-2-way-deposit-withdrawal-arbitrage.md` | MEDIUM | Code4rena |
| Missing freshness check on oracle data in `Staking.totalCont | `reports/cosmos_cometbft_findings/missing-freshness-check-on-oracle-data-in-stakingtotalcontrolled-enables-stale-r.md` | MEDIUM | MixBytes |

### Mev Priority
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Lack of prioritization of oracle messages | `reports/cosmos_cometbft_findings/lack-of-prioritization-of-oracle-messages.md` | MEDIUM | TrailOfBits |
| TRST-H-1 User fee  token  balance  can  be  drained in  a  s | `reports/cosmos_cometbft_findings/trst-h-1-user-fee-token-balance-can-be-drained-in-a-single-operation-by-a-malici.md` | HIGH | Trust Security |

### Mev Jit Liquidity
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Emergency Withdrawal Conditions Might Change Over Time | `reports/cosmos_cometbft_findings/emergency-withdrawal-conditions-might-change-over-time.md` | MEDIUM | OpenZeppelin |
| [M-01] Missing slippage protection in `AerodromeDexter.sol`  | `reports/cosmos_cometbft_findings/m-01-missing-slippage-protection-in-aerodromedextersol-swapexacttokensfortokens.md` | MEDIUM | Code4rena |
| [M-03] When malicious behavior occurs and DSS requests slash | `reports/cosmos_cometbft_findings/m-03-when-malicious-behavior-occurs-and-dss-requests-slashing-against-vault-duri.md` | MEDIUM | Code4rena |
| OracleManager.setBeaconData possible front running attacks | `reports/cosmos_cometbft_findings/oraclemanagersetbeacondata-possible-front-running-attacks.md` | MEDIUM | Spearbit |
| Quick buy and sell allows vote manipulation | `reports/cosmos_cometbft_findings/quick-buy-and-sell-allows-vote-manipulation.md` | HIGH | TrailOfBits |

---

# Frontrunning Mev Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Frontrunning Mev Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Mev Staking Frontrun](#1-mev-staking-frontrun)
2. [Mev Slippage Exploit](#2-mev-slippage-exploit)
3. [Mev Sandwich](#3-mev-sandwich)
4. [Mev Block Stuffing](#4-mev-block-stuffing)
5. [Mev Arbitrage](#5-mev-arbitrage)
6. [Mev Priority](#6-mev-priority)
7. [Mev Jit Liquidity](#7-mev-jit-liquidity)

---

## 1. Mev Staking Frontrun

### Overview

Implementation flaw in mev staking frontrun logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 4 audit reports with severity distribution: MEDIUM: 4.

> **Key Finding**: The report discusses a bug in the LiquidProxy.sol contract, which is part of the Ron staking contract. The bug allows users to earn rewards without actually staking their tokens for a long period of time. This is done by frontrunning the new rewards arrival and immediately withdrawing them. The repo



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of missing_frontrun_protection"
- Pattern key: `missing_frontrun_protection | mev_logic | frontrunning_mev_vulnerabilities`
- Interaction scope: `single_contract`
- Primary affected component(s): `mev_logic`
- High-signal code keywords: `_decodeAndReward`, `addLiquidityOneETHKeepYt`, `arbitrage`, `balanceOf`, `block.number`, `block.timestamp`, `block_stuffing`, `checkpointProtection`
- Typical sink / impact: `fund_loss|dos|state_corruption`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `can.function -> if.function`
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

Implementation flaw in mev staking frontrun logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies mev staking frontrun in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to mev operations

### Vulnerable Pattern Examples

**Example 1: [M-01] User can earn rewards by frontrunning the new rewards accumulation in Ron** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-01-user-can-earn-rewards-by-frontrunning-the-new-rewards-accumulation-in-ron-s.md`
```go
User -> delegate -> RonStaking -> Wait atleast a day -> New Rewards
```

**Example 2: `slash` calls can be blocked, allowing malicious users to bypass the slashing me** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-2-slash-calls-can-be-blocked-allowing-malicious-users-to-bypass-the-slashing-m.md`
```go
modifier checkpointProtection(address account) {
    uint256 numCheckpoints = _stakes[account]._checkpoints.length;
    require(numCheckpoints == 0 || _stakes[account]._checkpoints[numCheckpoints - 1]._blockNumber != block.number, "StakingModule: Cannot exit in the same block as another stake or exit");
    _;
}
```

**Example 3: [M-27] rotateNodeRunnerOfSmartWallet is vulnerable to a frontrun attack** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-27-rotatenoderunnerofsmartwallet-is-vulnerable-to-a-frontrun-attack.md`
```go
if (msg.sender == dao && _wasPreviousNodeRunnerMalicious) {
    bannedNodeRunners[_current] = true;
    emit NodeRunnerBanned(_current);
}
```

**Example 4: `slash()` can be frontrunned to avoid the penalty imposed on them** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-5-slash-can-be-frontrunned-to-avoid-the-penalty-imposed-on-them.md`
```
// Vulnerable pattern from Telcoin:
Source: https://github.com/sherlock-audit/2022-11-telcoin-judging/issues/45
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in mev staking frontrun logic allows exploitation through missing validation, in
func secureMevStakingFrontrun(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 4 audit reports
- **Severity Distribution**: MEDIUM: 4
- **Affected Protocols**: Telcoin, Stakehouse Protocol, Liquid Ron, Telcoin Update
- **Validation Strength**: Moderate (2 auditors)

---

## 2. Mev Slippage Exploit

### Overview

Implementation flaw in mev slippage exploit logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 6 audit reports with severity distribution: HIGH: 2, MEDIUM: 4.

> **Key Finding**: This bug report discusses a vulnerability in the Renzo protocol that allows for exploitation of the system by manipulating asset prices. This can result in value being lost to malicious actors and causing losses for ezETH holders. The report outlines three possible scenarios in which this vulnerabil

### Vulnerability Description

#### Root Cause

Implementation flaw in mev slippage exploit logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies mev slippage exploit in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to mev operations

### Vulnerable Pattern Examples

**Example 1: [H-04] Withdrawals logic allows MEV exploits of TVL changes and zero-slippage ze** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md`
```
// Vulnerable pattern from Renzo:
Deposit and withdrawal requests can be done immediately with no costs or fees, and both use the current oracle prices and TVL calculation ([`deposit`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/RestakeManager.sol#L499-L504), and [`withdraw`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/Withdraw/WithdrawQueue.sol#L217)). Crucially, the [withdrawal amount is calculated at withdrawal request submission time](https://github.com/code-423n4/2024-04-renzo/blob/ma
```

**Example 2: [M-01] Missing slippage protection in `AerodromeDexter.sol` `swapExactTokensForT** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-01-missing-slippage-protection-in-aerodromedextersol-swapexacttokensfortokens.md`
```go
uint256 _balanceBefore = ERC20(_tokenOut).balanceOf(address(this));
@>>        router.swapExactTokensForTokens(_amountIn, 0, routeOf[_tokenIn][_tokenOut], address(this), block.timestamp);
```

**Example 3: Slippage on `MetapoolRouter.addLiquidityOneETHKeepYt`** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-5-slippage-on-metapoolrouteraddliquidityoneethkeepyt.md`
```solidity
File: 2024-05-napier-update\metapool-router\src\MetapoolRouter.sol

371:     function addLiquidityOneETHKeepYt(address metapool, uint256 minLiquidity, address recipient, uint256 deadline)
372:         external payable nonReentrant checkDeadline(deadline) checkMetapool(metapool) returns (uint256 liquidity)
378:     {
379:         // Steps:
380:         // 1. Issue PT and YT using the received ETH
381:         // 2. Add liquidity to the Curve metapool
382:         // 3. Send the received LP token and YT to the recipient
383: 
...SNIP...
393:         uint256 pyAmount = pt.issue({to: address(this), underlyingAmount: msg.value}); 
395: 
...SNIP...
401:         liquidity = Twocrypto(metapool).add_liquidity({
402:             amounts: [pyAmount, 0],
403:             min_mint_amount: minLiquidity,
404:             receiver: recipient
405:         });
406: 
407:   >>>   IERC20(pt.yieldToken()).transfer(recipient, pyAmount); 
409:     }
```

**Example 4: Missing slippage protection in liquidation allows unexpected collateral loss** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-9-missing-slippage-protection-in-liquidation-allows-unexpected-collateral-loss.md`
```solidity
function liquidate(ILender.LenderStorage storage $, ILender.RepayParams memory params)
        external
        returns (uint256 liquidatedValue)
    {
        (uint256 totalDelegation, uint256 totalSlashableCollateral, uint256 totalDebt,,, uint256 health) =
            ViewLogic.agent($, params.agent);


        ValidationLogic.validateLiquidation(
            health,
            totalDelegation * $.emergencyLiquidationThreshold / totalDebt,
            $.liquidationStart[params.agent],
            $.grace,
            $.expiry
        );


        (uint256 assetPrice,) = IOracle($.oracle).getPrice(params.asset);
        uint256 bonus = ViewLogic.bonus($, params.agent);
        uint256 maxLiquidation = ViewLogic.maxLiquidatable($, params.agent, params.asset);
        uint256 liquidated = params.amount > maxLiquidation ? maxLiquidation : params.amount;


        liquidated = BorrowLogic.repay(
            $,
            ILender.RepayParams({ agent: params.agent, asset: params.asset, amount: liquidated, caller: params.caller })
        );


        (,,,,, health) = ViewLogic.agent($, params.agent);
        if (health >= 1e27) _closeLiquidation($, params.agent);


@>      liquidatedValue =
            (liquidated + (liquidated * bonus / 1e27)) * assetPrice / (10 ** $.reservesData[params.asset].decimals);
// ... (truncated)
```

**Example 5: Missing Tick and Liquidity Checks in _decodeAndReward (currentOnly=true ) Enable** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/missing-tick-and-liquidity-checks-in-_decodeandreward-currentonlytrue-enables-fr.md`
```solidity
function _decodeAndReward(
    bool currentOnly,
    calldataReader reader,
    PoolRewards storage poolRewards_,
    PoolId id,
    int24 tickSpacing,
    int24 currentTick
) internal returns (CalldataReader, uint256) {
    int24 expectedTick;
    (reader, expectedTick) = reader.readI24();
    if (currentTick != expectedTick) {
        revert WrongTick(currentTick, expectedTick);
    }
    if (currentOnly) {
        uint128 amount;
        (reader, amount) = reader.readU128();
        uint128 expectedLiquidity;
        (reader, expectedLiquidity) = reader.readU128();
        uint128 actualLiquidity = UNI_V4.getPoolLiquidity(id);
        // Add a check to ensure the actual liquidity matches the expected liquidity
        if (actualLiquidity != expectedLiquidity) {
            revert WrongEndLiquidity(expectedLiquidity, actualLiquidity);
        }
        unchecked {
            poolRewards_.globalGrowth += X128MathLib.flatDivX128(amount, actualLiquidity);
        }
        return (reader, amount);
    }
    // ...
}
```

**Variant: Mev Slippage Exploit - MEDIUM Severity Cases** [MEDIUM]
> Found in 4 reports:
> - `reports/cosmos_cometbft_findings/m-01-missing-slippage-protection-in-aerodromedextersol-swapexacttokensfortokens.md`
> - `reports/cosmos_cometbft_findings/m-5-slippage-on-metapoolrouteraddliquidityoneethkeepyt.md`
> - `reports/cosmos_cometbft_findings/m-9-missing-slippage-protection-in-liquidation-allows-unexpected-collateral-loss.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in mev slippage exploit logic allows exploitation through missing validation, in
func secureMevSlippageExploit(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 6 audit reports
- **Severity Distribution**: HIGH: 2, MEDIUM: 4
- **Affected Protocols**: Persistence, Napier Finance - LST/LRT Integrations, Sorella Labs, Flex Perpetuals, Renzo
- **Validation Strength**: Strong (3+ auditors)

---

## 3. Mev Sandwich

### Overview

Implementation flaw in mev sandwich logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: HIGH: 1, MEDIUM: 2.

> **Key Finding**: This bug report discusses a vulnerability in the Renzo protocol that allows for exploitation of the system by manipulating asset prices. This can result in value being lost to malicious actors and causing losses for ezETH holders. The report outlines three possible scenarios in which this vulnerabil

### Vulnerability Description

#### Root Cause

Implementation flaw in mev sandwich logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies mev sandwich in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to mev operations

### Vulnerable Pattern Examples

**Example 1: [H-04] Withdrawals logic allows MEV exploits of TVL changes and zero-slippage ze** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md`
```
// Vulnerable pattern from Renzo:
Deposit and withdrawal requests can be done immediately with no costs or fees, and both use the current oracle prices and TVL calculation ([`deposit`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/RestakeManager.sol#L499-L504), and [`withdraw`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/Withdraw/WithdrawQueue.sol#L217)). Crucially, the [withdrawal amount is calculated at withdrawal request submission time](https://github.com/code-423n4/2024-04-renzo/blob/ma
```

**Example 2: [M-01] Missing slippage protection in `AerodromeDexter.sol` `swapExactTokensForT** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-01-missing-slippage-protection-in-aerodromedextersol-swapexacttokensfortokens.md`
```go
uint256 _balanceBefore = ERC20(_tokenOut).balanceOf(address(this));
@>>        router.swapExactTokensForTokens(_amountIn, 0, routeOf[_tokenIn][_tokenOut], address(this), block.timestamp);
```

**Example 3: A part of ETH rewards can be stolen by sandwiching `claimDelayedWithdrawals()`** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-3-a-part-of-eth-rewards-can-be-stolen-by-sandwiching-claimdelayedwithdrawals.md`
```go
receive() external payable {
    (bool success,) = address(rewardDistributor()).call{value: msg.value}('');
    require(success);
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in mev sandwich logic allows exploitation through missing validation, incorrect 
func secureMevSandwich(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 3 audit reports
- **Severity Distribution**: HIGH: 1, MEDIUM: 2
- **Affected Protocols**: Flex Perpetuals, Renzo, Rio Network
- **Validation Strength**: Moderate (2 auditors)

---

## 4. Mev Block Stuffing

### Overview

Implementation flaw in mev block stuffing logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: This bug report highlights a potential vulnerability in the deployment script of the Ethereum Credit Guild protocol. The script sets a low immutable auction duration, which could lead to profitable block stuffing attacks on certain Layer 2 chains. This attack can be further improved if the collatera

### Vulnerability Description

#### Root Cause

Implementation flaw in mev block stuffing logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies mev block stuffing in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to mev operations

### Vulnerable Pattern Examples

**Example 1: [M-16] Auction manipulation by block stuffing and reverting on ERC-777 hooks** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-16-auction-manipulation-by-block-stuffing-and-reverting-on-erc-777-hooks.md`
```go
AuctionHouse auctionHouse = new AuctionHouse(
    AddressLib.get("CORE"),
    650, // midPoint = 10m50s
    1800 // auctionDuration = 30m
);
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in mev block stuffing logic allows exploitation through missing validation, inco
func secureMevBlockStuffing(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 1 audit reports
- **Severity Distribution**: MEDIUM: 1
- **Affected Protocols**: Ethereum Credit Guild
- **Validation Strength**: Single auditor

---

## 5. Mev Arbitrage

### Overview

Implementation flaw in mev arbitrage logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 6 audit reports with severity distribution: HIGH: 2, MEDIUM: 4.

> **Key Finding**: KelpDAO is a staking protocol that relies on Chainlink price feeds to calculate the rsETH/ETH exchange rate. The price feed has an acceptable deviation of [-2% 2%], meaning that the nodes will not update an on-chain price if the boundaries are not reached within the 24 hour period. This creates an a

### Vulnerability Description

#### Root Cause

Implementation flaw in mev arbitrage logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies mev arbitrage in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to mev operations

### Vulnerable Pattern Examples

**Example 1: [H-01] Possible arbitrage from Chainlink price discrepancy** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-possible-arbitrage-from-chainlink-price-discrepancy.md`
```go
*   `test_DepositAsset()`:
        *
```

**Example 2: [H-08] Exchange rate calculation is incorrect** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-08-exchange-rate-calculation-is-incorrect.md`
```go
exchangeRate = (totalStaked + totalRewards - totalClaimed - totalSlashing) / kHYPESupply
```

**Example 3: [M-02] `MsgSwapOrder` will never work for Canto nodes** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-02-msgswaporder-will-never-work-for-canto-nodes.md`
```go
message Input {
  string address = 1;
  cosmos.base.v1beta1.Coin coin = 2 [ (gogoproto.nullable) = false ];
}
```

**Example 4: [M-04] Arbitrage on `stake()`** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-04-arbitrage-on-stake.md`
```solidity
File: Staking.sol
406:     function stake(uint256 _amount, address _recipient) public { // @audit-info [HIGH] 
407:         // if override staking, then don't allow stake
408:         require(!isStakingPaused, "Staking is paused");
409:         // amount must be non zero
410:         require(_amount > 0, "Must have valid amount");
411: 
412:         uint256 yieldyTotalSupply = IYieldy(YIELDY_TOKEN).totalSupply();
413: 
414:         // Don't rebase unless tokens are already staked or could get locked out of staking
415:         if (yieldyTotalSupply > 0) {
416:             rebase();
417:         }
418: 
419:         IERC20Upgradeable(STAKING_TOKEN).safeTransferFrom(
420:             msg.sender,
421:             address(this),
422:             _amount
423:         );
424: 
425:         Claim storage info = warmUpInfo[_recipient];
426: 
427:         // if claim is available then auto claim tokens
428:         if (_isClaimAvailable(_recipient)) {
429:             claim(_recipient);
430:         }
431: 
432:         _depositToTokemak(_amount);
433: 
434:         // skip adding to warmup contract if period is 0
435:         if (warmUpPeriod == 0) {
436:             IYieldy(YIELDY_TOKEN).mint(_recipient, _amount);
437:         } else {
438:             // create a claim and mint tokens so a user can claim them once warm up has passed
439:             warmUpInfo[_recipient] = Claim({
// ... (truncated)
```

**Example 5: [M-14] stETH/ETH feed being used opens up to 2 way `deposit<->withdrawal` arbitr** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-14-stetheth-feed-being-used-opens-up-to-2-way-deposit-withdrawal-arbitrage.md`
```
// Vulnerable pattern from Renzo:
The stETH/ETH oracle is not a exchange rate feed, it's a Market Rate Feed, while other feeds are exchange rate feeds.

This opens up ezETH to be vulnerable to:
- Market Rate Manipulations.
- Sentiment based Price Action.
- Duration based discounts.

### POC

This opens up to arbitrage anytime stETH trades at a discount (see Liquidations on the 13th of April).

Had withdrawals been open, the following could have been possible:
- Deposit stETH before the Depeg (front-run oracle update).
- Get ezET
```

**Variant: Mev Arbitrage - MEDIUM Severity Cases** [MEDIUM]
> Found in 4 reports:
> - `reports/cosmos_cometbft_findings/m-02-msgswaporder-will-never-work-for-canto-nodes.md`
> - `reports/cosmos_cometbft_findings/m-04-arbitrage-on-stake.md`
> - `reports/cosmos_cometbft_findings/m-14-stetheth-feed-being-used-opens-up-to-2-way-deposit-withdrawal-arbitrage.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in mev arbitrage logic allows exploitation through missing validation, incorrect
func secureMevArbitrage(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 6 audit reports
- **Severity Distribution**: HIGH: 2, MEDIUM: 4
- **Affected Protocols**: Canto, Yieldy, Renzo, Kelp DAO, Kinetiq_2025-02-26
- **Validation Strength**: Strong (3+ auditors)

---

## 6. Mev Priority

### Overview

Implementation flaw in mev priority logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 1, MEDIUM: 1.

> **Key Finding**: This bug report is about an issue in the Umee system where Oracle messages are not prioritized over other transactions for inclusion in a block. This can be a problem if the network is congested, as the messages may not be included in a block. To address this, Tactics for prioritizing important tran

### Vulnerability Description

#### Root Cause

Implementation flaw in mev priority logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies mev priority in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to mev operations

### Vulnerable Pattern Examples

**Example 1: Lack of prioritization of oracle messages** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/lack-of-prioritization-of-oracle-messages.md`
```
// Vulnerable pattern from Umee:
## Umee Security Assessment

**Difficulty:** Medium

**Type:** Undefined Behavior

**Target:** umee/x/oracle
```

**Example 2: TRST-H-1 User fee  token  balance  can  be  drained in  a  single  operation  by** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/trst-h-1-user-fee-token-balance-can-be-drained-in-a-single-operation-by-a-malici.md`
```go
if (feeToken == ETH) 
   {uint256 totalFee = (gasUsed + GAS_OVERHEAD_NATIVE) * tx.gasprice;
     totalFee = _applyMultiplier(totalFee);
       return (totalFee, recipient, TokenTransfer._nativeTransferExec(recipient, totalFee));
            } else {uint256 totalFee = (gasUsed + GAS_OVERHEAD_ERC20) * tx.gasprice;
      // Convert fee amount value in fee tokenuint256 feeToCollect =PriceFeedManager(_addressProvider.priceFeedManager()).getTokenXPriceInY(totalFee, ETH, feeToken);
  feeToCollect = _applyMultiplier(feeToCollect);
 return (feeToCollect, recipient, TokenTransfer._erc20TransferExec(feeToken, recipient, feeToCollect));}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in mev priority logic allows exploitation through missing validation, incorrect 
func secureMevPriority(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 2 audit reports
- **Severity Distribution**: HIGH: 1, MEDIUM: 1
- **Affected Protocols**: Brahma, Umee
- **Validation Strength**: Moderate (2 auditors)

---

## 7. Mev Jit Liquidity

### Overview

Implementation flaw in mev jit liquidity logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 5 audit reports with severity distribution: HIGH: 1, MEDIUM: 4.

> **Key Finding**: The report discusses an issue with the `shutdown` function in the `RizLendingPool` contract. This function takes a snapshot of prices and calculates a ratio for slashing remaining users in the market. However, the owner of the `BadDebtManager` contract can modify this snapshot data without any restr

### Vulnerability Description

#### Root Cause

Implementation flaw in mev jit liquidity logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies mev jit liquidity in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to mev operations

### Vulnerable Pattern Examples

**Example 1: Emergency Withdrawal Conditions Might Change Over Time** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/emergency-withdrawal-conditions-might-change-over-time.md`
```
// Vulnerable pattern from Radiant Riz Audit:
After a market has been [shut down](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/riz-lending/RizLendingPoolConfigurator.sol#L491), the `shutdown` function from the `RizLendingPool` contract [takes a snapshot](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/riz-lending/RizLendingPool.sol#L728) through the `BadDebtManager` contract. This is done to keep a record of the [prices in the particular lending pool and al
```

**Example 2: [M-01] Missing slippage protection in `AerodromeDexter.sol` `swapExactTokensForT** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-01-missing-slippage-protection-in-aerodromedextersol-swapexacttokensfortokens.md`
```go
uint256 _balanceBefore = ERC20(_tokenOut).balanceOf(address(this));
@>>        router.swapExactTokensForTokens(_amountIn, 0, routeOf[_tokenIn][_tokenOut], address(this), block.timestamp);
```

**Example 3: [M-03] When malicious behavior occurs and DSS requests slashing against vault du** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-03-when-malicious-behavior-occurs-and-dss-requests-slashing-against-vault-duri.md`
```go
uint256 public constant SLASHING_WINDOW = 7 days;
    uint256 public constant SLASHING_VETO_WINDOW = 2 days;
    uint256 public constant MIN_STAKE_UPDATE_DELAY = SLASHING_WINDOW + SLASHING_VETO_WINDOW;
    uint256 public constant MIN_WITHDRAWAL_DELAY = SLASHING_WINDOW + SLASHING_VETO_WINDOW;
```

**Example 4: OracleManager.setBeaconData possible front running attacks** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/oraclemanagersetbeacondata-possible-front-running-attacks.md`
```
// Vulnerable pattern from Liquid Collective:
## Medium Risk Assessment
```

**Example 5: Quick buy and sell allows vote manipulation** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/quick-buy-and-sell-allows-vote-manipulation.md`
```
// Vulnerable pattern from The Computable Protocol:
## Data Validation

**Type:** Data Validation  
**Target:** Reserve  

**Difficulty:** Low
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in mev jit liquidity logic allows exploitation through missing validation, incor
func secureMevJitLiquidity(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 5 audit reports
- **Severity Distribution**: HIGH: 1, MEDIUM: 4
- **Affected Protocols**: Flex Perpetuals, Karak, Radiant Riz Audit, The Computable Protocol, Liquid Collective
- **Validation Strength**: Strong (3+ auditors)

---

## Detection Patterns

### Automated Detection
```
# Mev Staking Frontrun
grep -rn 'mev|staking|frontrun' --include='*.go' --include='*.sol'
# Mev Slippage Exploit
grep -rn 'mev|slippage|exploit' --include='*.go' --include='*.sol'
# Mev Sandwich
grep -rn 'mev|sandwich' --include='*.go' --include='*.sol'
# Mev Block Stuffing
grep -rn 'mev|block|stuffing' --include='*.go' --include='*.sol'
# Mev Arbitrage
grep -rn 'mev|arbitrage' --include='*.go' --include='*.sol'
# Mev Priority
grep -rn 'mev|priority' --include='*.go' --include='*.sol'
# Mev Jit Liquidity
grep -rn 'mev|jit|liquidity' --include='*.go' --include='*.sol'
```

## Keywords

`accumulation`, `actually`, `after`, `against`, `allowing`, `allows`, `amount`, `appchain`, `arbitrage`, `attack`, `auction`, `balance`, `behavior`, `block`, `bypass`, `calculated`, `calculation`, `calls`, `canto`, `chainlink`, `change`, `changes`, `conditions`, `cosmos`, `days`, `delegating`, `discrepancy`, `drained`, `during`, `earn`

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

`_decodeAndReward`, `addLiquidityOneETHKeepYt`, `appchain`, `arbitrage`, `balanceOf`, `block.number`, `block.timestamp`, `block_stuffing`, `checkpointProtection`, `cosmos`, `defi`, `deposit`, `frontrunning_mev_vulnerabilities`, `getPrice`, `jit_liquidity`, `liquidate`, `mev`, `mint`, `msg.sender`, `price_update`, `priority`, `receive`, `repay`, `safeTransferFrom`, `sandwich`, `slippage_exploit`, `staking`, `staking_frontrun`
