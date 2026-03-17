---
protocol: generic
chain: cosmos
category: oracle
vulnerability_type: oracle_price_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: oracle_logic

primitives:
  - stale_price
  - price_manipulation
  - dos
  - deviation_exploit
  - frontrunning
  - missing_stake
  - chainlink_specific
  - wrong_price_usage

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - oracle
  - staking
  - defi

language: go|solidity|rust
version: all

# Pattern Identity (Required)
root_cause_family: missing_validation
pattern_key: missing_validation | oracle_logic | oracle_price_vulnerabilities

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: multi_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - borrow
  - burn
  - chainlink_specific
  - deposit
  - deviation_exploit
  - dos
  - frontrunning
  - getPrice
  - mint
  - missing_stake
  - msg.sender
  - price
  - price_manipulation
  - queryExchangeRate
  - stale_price
  - update
  - withdraw
  - wrong_price_usage
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Oracle Stale Price
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-04] Withdrawals logic allows MEV exploits of TVL changes  | `reports/cosmos_cometbft_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md` | HIGH | Code4rena |
| [M-10] `IOracle.queryExchangeRate` returns incorrect `blockT | `reports/cosmos_cometbft_findings/m-10-ioraclequeryexchangerate-returns-incorrect-blocktimems.md` | MEDIUM | Code4rena |
| [M-22] Lagging median gas price when the set of observers ch | `reports/cosmos_cometbft_findings/m-22-lagging-median-gas-price-when-the-set-of-observers-changes.md` | MEDIUM | Code4rena |
| Missing freshness check on oracle data in `Staking.totalCont | `reports/cosmos_cometbft_findings/missing-freshness-check-on-oracle-data-in-stakingtotalcontrolled-enables-stale-r.md` | MEDIUM | MixBytes |
| Users May Be Able to Borrow swEth at an Outdated Price | `reports/cosmos_cometbft_findings/users-may-be-able-to-borrow-sweth-at-an-outdated-price.md` | MEDIUM | OpenZeppelin |

### Oracle Price Manipulation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-04] Withdrawals logic allows MEV exploits of TVL changes  | `reports/cosmos_cometbft_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md` | HIGH | Code4rena |
| LibTWAPOracle::update Providing large liquidity will manipul | `reports/cosmos_cometbft_findings/m-4-libtwaporacleupdate-providing-large-liquidity-will-manipulate-twap-dosing-re.md` | MEDIUM | Sherlock |
| Users May Be Able to Borrow swEth at an Outdated Price | `reports/cosmos_cometbft_findings/users-may-be-able-to-borrow-sweth-at-an-outdated-price.md` | MEDIUM | OpenZeppelin |

### Oracle Dos
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-03] Freeze The Bridge Via Large ERC20 Names/Symbols/Denom | `reports/cosmos_cometbft_findings/h-03-freeze-the-bridge-via-large-erc20-namessymbolsdenoms.md` | HIGH | Code4rena |
| [H-04] Large Validator Sets/Rapid Validator Set Updates May  | `reports/cosmos_cometbft_findings/h-04-large-validator-setsrapid-validator-set-updates-may-freeze-the-bridge-or-re.md` | HIGH | Code4rena |
| Lack of prioritization of oracle messages | `reports/cosmos_cometbft_findings/lack-of-prioritization-of-oracle-messages.md` | MEDIUM | TrailOfBits |
| [M-01] No check for sequencer uptime can lead to dutch aucti | `reports/cosmos_cometbft_findings/m-01-no-check-for-sequencer-uptime-can-lead-to-dutch-auctions-failing-or-executi.md` | MEDIUM | Code4rena |
| [M-10] `IOracle.queryExchangeRate` returns incorrect `blockT | `reports/cosmos_cometbft_findings/m-10-ioraclequeryexchangerate-returns-incorrect-blocktimems.md` | MEDIUM | Code4rena |
| LibTWAPOracle::update Providing large liquidity will manipul | `reports/cosmos_cometbft_findings/m-4-libtwaporacleupdate-providing-large-liquidity-will-manipulate-twap-dosing-re.md` | MEDIUM | Sherlock |
| TRST-H-1 User fee  token  balance  can  be  drained in  a  s | `reports/cosmos_cometbft_findings/trst-h-1-user-fee-token-balance-can-be-drained-in-a-single-operation-by-a-malici.md` | HIGH | Trust Security |

### Oracle Deviation Exploit
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-01] Possible arbitrage from Chainlink price discrepancy | `reports/cosmos_cometbft_findings/h-01-possible-arbitrage-from-chainlink-price-discrepancy.md` | HIGH | Code4rena |
| Lack of on-chain deviation check for LST can lead to loss of | `reports/cosmos_cometbft_findings/m-1-lack-of-on-chain-deviation-check-for-lst-can-lead-to-loss-of-assets.md` | MEDIUM | Sherlock |

### Oracle Frontrunning
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-04] Withdrawals logic allows MEV exploits of TVL changes  | `reports/cosmos_cometbft_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md` | HIGH | Code4rena |
| Users can frontrun LSTs/LRTs tokens prices decrease in order | `reports/cosmos_cometbft_findings/h-2-users-can-frontrun-lstslrts-tokens-prices-decrease-in-order-to-avoid-losses.md` | HIGH | Sherlock |

### Oracle Missing Stake
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Failure to enforce minimum oracle stake requirement | `reports/cosmos_cometbft_findings/failure-to-enforce-minimum-oracle-stake-requirement.md` | HIGH | TrailOfBits |

### Oracle Chainlink Specific
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-01] Possible arbitrage from Chainlink price discrepancy | `reports/cosmos_cometbft_findings/h-01-possible-arbitrage-from-chainlink-price-discrepancy.md` | HIGH | Code4rena |

### Oracle Wrong Price Usage
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| ChainlinkAdapterOracle will return the wrong price for asset | `reports/cosmos_cometbft_findings/m-16-chainlinkadapteroracle-will-return-the-wrong-price-for-asset-if-underlying-.md` | MEDIUM | Sherlock |
| Wrong capTokenDecimals value used in StakedCapAdapter.price  | `reports/cosmos_cometbft_findings/wrong-captokendecimals-value-used-in-stakedcapadapterprice-causes-inaccurate-pri.md` | HIGH | TrailOfBits |

---

# Oracle Price Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Oracle Price Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Oracle Stale Price](#1-oracle-stale-price)
2. [Oracle Price Manipulation](#2-oracle-price-manipulation)
3. [Oracle Dos](#3-oracle-dos)
4. [Oracle Deviation Exploit](#4-oracle-deviation-exploit)
5. [Oracle Frontrunning](#5-oracle-frontrunning)
6. [Oracle Missing Stake](#6-oracle-missing-stake)
7. [Oracle Chainlink Specific](#7-oracle-chainlink-specific)
8. [Oracle Wrong Price Usage](#8-oracle-wrong-price-usage)

---

## 1. Oracle Stale Price

### Overview

Implementation flaw in oracle stale price logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 5 audit reports with severity distribution: HIGH: 1, MEDIUM: 4.

> **Key Finding**: This bug report discusses a vulnerability in the Renzo protocol that allows for exploitation of the system by manipulating asset prices. This can result in value being lost to malicious actors and causing losses for ezETH holders. The report outlines three possible scenarios in which this vulnerabil



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of missing_validation"
- Pattern key: `missing_validation | oracle_logic | oracle_price_vulnerabilities`
- Interaction scope: `multi_contract`
- Primary affected component(s): `oracle_logic`
- High-signal code keywords: `borrow`, `burn`, `chainlink_specific`, `deposit`, `deviation_exploit`, `dos`, `frontrunning`, `getPrice`
- Typical sink / impact: `fund_loss|dos|state_corruption`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `implements.function -> on.function`
- Trust boundary crossed: `callback / external call`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: Critical input parameter not validated against expected range or format
- Signal 2: Oracle data consumed without staleness check or sanity bounds
- Signal 3: User-supplied address or calldata forwarded without validation
- Signal 4: Missing check allows operation under invalid or stale state

#### False Positive Guards

- Not this bug when: Validation exists but is in an upstream function caller
- Safe if: Parameter range is inherently bounded by the type or protocol invariant
- Requires attacker control of: specific conditions per pattern

### Vulnerability Description

#### Root Cause

Implementation flaw in oracle stale price logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies oracle stale price in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to oracle operations

### Vulnerable Pattern Examples

**Example 1: [H-04] Withdrawals logic allows MEV exploits of TVL changes and zero-slippage ze** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md`
```
// Vulnerable pattern from Renzo:
Deposit and withdrawal requests can be done immediately with no costs or fees, and both use the current oracle prices and TVL calculation ([`deposit`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/RestakeManager.sol#L499-L504), and [`withdraw`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/Withdraw/WithdrawQueue.sol#L217)). Crucially, the [withdrawal amount is calculated at withdrawal request submission time](https://github.com/code-423n4/2024-04-renzo/blob/ma
```

**Example 2: [M-10] `IOracle.queryExchangeRate` returns incorrect `blockTimeMs`** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-10-ioraclequeryexchangerate-returns-incorrect-blocktimems.md`
```solidity
/// @notice Queries the dated exchange rate for a given pair
    /// @param pair The asset pair to query. For example, "ubtc:uusd" is the
    /// USD price of BTC and "unibi:uusd" is the USD price of NIBI.
    /// @return price The exchange rate for the given pair
    /// @return blockTimeMs The block time in milliseconds when the price was
    /// last updated
    /// @return blockHeight The block height when the price was last updated
    /// @dev This function is view-only and does not modify state.
    function queryExchangeRate(
        string memory pair
    ) external view returns (uint256 price, uint64 blockTimeMs, uint64 blockHeight);
```

**Example 3: [M-22] Lagging median gas price when the set of observers changes** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-22-lagging-median-gas-price-when-the-set-of-observers-changes.md`
```
// Vulnerable pattern from ZetaChain:
The median gas price used within ZetaChain may be inaccurate and lagging, causing outbound transactions to be underpriced and pending in the mempool and gas fees to be underpaid by users.

### Proof of Concept

ZetaChain observers, i.e., zetaclients, watch the gas prices of the external chains and submit the current prices to ZetaChain by broadcasting the `MsgGasPriceVoter` message. This message is processed by the `GasPriceVoter` function in [node/x/crosschain/keeper/keeper_gas_price.go#L125-L1
```

**Example 4: Missing freshness check on oracle data in `Staking.totalControlled()` enables st** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/missing-freshness-check-on-oracle-data-in-stakingtotalcontrolled-enables-stale-r.md`
```
// Vulnerable pattern from Mantle Network:
##### Description
`Staking.totalControlled()` derives the mETH/ETH exchange rate inputs from `oracle.latestRecord()` without validating the record timestamp.

If the oracle lags significant state changes (e.g., validator rewards or slashing), the resulting rate becomes stale. An attacker can exploit this by timing mint/burn operations against outdated totals: redeeming mETH for excess ETH when a slashing is not yet reflected (overstated `totalControlled()`), or depositing ETH to mint excess mETH
```

**Example 5: Users May Be Able to Borrow swEth at an Outdated Price** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/users-may-be-able-to-borrow-sweth-at-an-outdated-price.md`
```
// Vulnerable pattern from Ion Protocol Audit:
The [`getPrice` function](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/oracles/spot/SwEthSpotOracle.sol#L32) of `SwEthSpotOracle` uses a TWAP oracle which means that a sudden change in price would not immediately affect the return value. This value is used in the [`getSpot` function](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/oracles/spot/SpotOracle.sol#L37) which calculates the spot price as th
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in oracle stale price logic allows exploitation through missing validation, inco
func secureOracleStalePrice(ctx sdk.Context) error {
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
- **Affected Protocols**: Ion Protocol Audit, Nibiru, Renzo, ZetaChain, Mantle Network
- **Validation Strength**: Strong (3+ auditors)

---

## 2. Oracle Price Manipulation

### Overview

Implementation flaw in oracle price manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: HIGH: 1, MEDIUM: 2.

> **Key Finding**: This bug report discusses a vulnerability in the Renzo protocol that allows for exploitation of the system by manipulating asset prices. This can result in value being lost to malicious actors and causing losses for ezETH holders. The report outlines three possible scenarios in which this vulnerabil

### Vulnerability Description

#### Root Cause

Implementation flaw in oracle price manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies oracle price manipulation in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to oracle operations

### Vulnerable Pattern Examples

**Example 1: [H-04] Withdrawals logic allows MEV exploits of TVL changes and zero-slippage ze** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md`
```
// Vulnerable pattern from Renzo:
Deposit and withdrawal requests can be done immediately with no costs or fees, and both use the current oracle prices and TVL calculation ([`deposit`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/RestakeManager.sol#L499-L504), and [`withdraw`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/Withdraw/WithdrawQueue.sol#L217)). Crucially, the [withdrawal amount is calculated at withdrawal request submission time](https://github.com/code-423n4/2024-04-renzo/blob/ma
```

**Example 2: LibTWAPOracle::update Providing large liquidity will manipulate TWAP, DOSing red** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-4-libtwaporacleupdate-providing-large-liquidity-will-manipulate-twap-dosing-re.md`
```go
require(
            getDollarPriceUsd() >= poolStorage.mintPriceThreshold,
            "Dollar price too low"
        );
```

**Example 3: Users May Be Able to Borrow swEth at an Outdated Price** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/users-may-be-able-to-borrow-sweth-at-an-outdated-price.md`
```
// Vulnerable pattern from Ion Protocol Audit:
The [`getPrice` function](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/oracles/spot/SwEthSpotOracle.sol#L32) of `SwEthSpotOracle` uses a TWAP oracle which means that a sudden change in price would not immediately affect the return value. This value is used in the [`getSpot` function](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/oracles/spot/SpotOracle.sol#L37) which calculates the spot price as th
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in oracle price manipulation logic allows exploitation through missing validatio
func secureOraclePriceManipulation(ctx sdk.Context) error {
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
- **Affected Protocols**: Renzo, Ubiquity, Ion Protocol Audit
- **Validation Strength**: Strong (3+ auditors)

---

## 3. Oracle Dos

### Overview

Implementation flaw in oracle dos logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 7 audit reports with severity distribution: HIGH: 3, MEDIUM: 4.

> **Key Finding**: This bug report is about the Ethereum Oracles watch for events on the Gravity.sol contract on the Ethereum blockchain, which is performed in the check_for_events and eth_oracle_main_loop functions. The code snippet leverages the web30 library to check for events from the starting_block to the latest

### Vulnerability Description

#### Root Cause

Implementation flaw in oracle dos logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies oracle dos in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to oracle operations

### Vulnerable Pattern Examples

**Example 1: [H-03] Freeze The Bridge Via Large ERC20 Names/Symbols/Denoms** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-03-freeze-the-bridge-via-large-erc20-namessymbolsdenoms.md`
```go
let erc20_deployed = web3
    .check_for_events(
        starting_block.clone(),
        Some(latest_block.clone()),
        vec![gravity_contract_address],
        vec![ERC20_DEPLOYED_EVENT_SIG],
    )
    .await;
```

**Example 2: [H-04] Large Validator Sets/Rapid Validator Set Updates May Freeze the Bridge or** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-04-large-validator-setsrapid-validator-set-updates-may-freeze-the-bridge-or-re.md`
```go
let mut all_valset_events = web3
    .check_for_events(
        end_search.clone(),
        Some(current_block.clone()),
        vec![gravity_contract_address],
        vec![VALSET_UPDATED_EVENT_SIG],
    )
    .await?;
```

**Example 3: Lack of prioritization of oracle messages** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/lack-of-prioritization-of-oracle-messages.md`
```
// Vulnerable pattern from Umee:
## Umee Security Assessment

**Difficulty:** Medium

**Type:** Undefined Behavior

**Target:** umee/x/oracle
```

**Example 4: [M-01] No check for sequencer uptime can lead to dutch auctions failing or execu** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-01-no-check-for-sequencer-uptime-can-lead-to-dutch-auctions-failing-or-executi.md`
```
// Vulnerable pattern from Ethereum Credit Guild:
The `AuctionHouse` contract implements a Dutch auction mechanism to recover debt from collateral. However, there is no check for sequencer uptime, which could lead to auctions failing or executing at unfavorable prices.

The current deployment parameters allow auctions to succeed without a loss to the protocol for a duration of 10m 50s. If there's no bid on the auction after this period, the protocol has no other option but to take a loss or forgive the loan. This could have serious consequences
```

**Example 5: [M-10] `IOracle.queryExchangeRate` returns incorrect `blockTimeMs`** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-10-ioraclequeryexchangerate-returns-incorrect-blocktimems.md`
```solidity
/// @notice Queries the dated exchange rate for a given pair
    /// @param pair The asset pair to query. For example, "ubtc:uusd" is the
    /// USD price of BTC and "unibi:uusd" is the USD price of NIBI.
    /// @return price The exchange rate for the given pair
    /// @return blockTimeMs The block time in milliseconds when the price was
    /// last updated
    /// @return blockHeight The block height when the price was last updated
    /// @dev This function is view-only and does not modify state.
    function queryExchangeRate(
        string memory pair
    ) external view returns (uint256 price, uint64 blockTimeMs, uint64 blockHeight);
```

**Variant: Oracle Dos - MEDIUM Severity Cases** [MEDIUM]
> Found in 4 reports:
> - `reports/cosmos_cometbft_findings/lack-of-prioritization-of-oracle-messages.md`
> - `reports/cosmos_cometbft_findings/m-01-no-check-for-sequencer-uptime-can-lead-to-dutch-auctions-failing-or-executi.md`
> - `reports/cosmos_cometbft_findings/m-10-ioraclequeryexchangerate-returns-incorrect-blocktimems.md`

**Variant: Oracle Dos in Althea Gravity Bridge** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h-03-freeze-the-bridge-via-large-erc20-namessymbolsdenoms.md`
> - `reports/cosmos_cometbft_findings/h-04-large-validator-setsrapid-validator-set-updates-may-freeze-the-bridge-or-re.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in oracle dos logic allows exploitation through missing validation, incorrect st
func secureOracleDos(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 7 audit reports
- **Severity Distribution**: HIGH: 3, MEDIUM: 4
- **Affected Protocols**: Brahma, Althea Gravity Bridge, Ubiquity, Umee, Nibiru
- **Validation Strength**: Strong (3+ auditors)

---

## 4. Oracle Deviation Exploit

### Overview

Implementation flaw in oracle deviation exploit logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 1, MEDIUM: 1.

> **Key Finding**: KelpDAO is a staking protocol that relies on Chainlink price feeds to calculate the rsETH/ETH exchange rate. The price feed has an acceptable deviation of [-2% 2%], meaning that the nodes will not update an on-chain price if the boundaries are not reached within the 24 hour period. This creates an a

### Vulnerability Description

#### Root Cause

Implementation flaw in oracle deviation exploit logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies oracle deviation exploit in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to oracle operations

### Vulnerable Pattern Examples

**Example 1: [H-01] Possible arbitrage from Chainlink price discrepancy** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-possible-arbitrage-from-chainlink-price-discrepancy.md`
```go
*   `test_DepositAsset()`:
        *
```

**Example 2: Lack of on-chain deviation check for LST can lead to loss of assets** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-1-lack-of-on-chain-deviation-check-for-lst-can-lead-to-loss-of-assets.md`
```go
120 ETH - 50 ETH (Cost) = 70 ETH (Profit)
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in oracle deviation exploit logic allows exploitation through missing validation
func secureOracleDeviationExploit(ctx sdk.Context) error {
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
- **Affected Protocols**: Usual ETH0, Kelp DAO
- **Validation Strength**: Moderate (2 auditors)

---

## 5. Oracle Frontrunning

### Overview

Implementation flaw in oracle frontrunning logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 2.

> **Key Finding**: This bug report discusses a vulnerability in the Renzo protocol that allows for exploitation of the system by manipulating asset prices. This can result in value being lost to malicious actors and causing losses for ezETH holders. The report outlines three possible scenarios in which this vulnerabil

### Vulnerability Description

#### Root Cause

Implementation flaw in oracle frontrunning logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies oracle frontrunning in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to oracle operations

### Vulnerable Pattern Examples

**Example 1: [H-04] Withdrawals logic allows MEV exploits of TVL changes and zero-slippage ze** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md`
```
// Vulnerable pattern from Renzo:
Deposit and withdrawal requests can be done immediately with no costs or fees, and both use the current oracle prices and TVL calculation ([`deposit`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/RestakeManager.sol#L499-L504), and [`withdraw`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/Withdraw/WithdrawQueue.sol#L217)). Crucially, the [withdrawal amount is calculated at withdrawal request submission time](https://github.com/code-423n4/2024-04-renzo/blob/ma
```

**Example 2: Users can frontrun LSTs/LRTs tokens prices decrease in order to avoid losses** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-2-users-can-frontrun-lstslrts-tokens-prices-decrease-in-order-to-avoid-losses.md`
```
// Vulnerable pattern from Napier Finance - LST/LRT Integrations:
Source: https://github.com/sherlock-audit/2024-05-napier-update-judging/issues/65 

The protocol has acknowledged this issue.
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in oracle frontrunning logic allows exploitation through missing validation, inc
func secureOracleFrontrunning(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 2
- **Affected Protocols**: Renzo, Napier Finance - LST/LRT Integrations
- **Validation Strength**: Moderate (2 auditors)

---

## 6. Oracle Missing Stake

### Overview

Implementation flaw in oracle missing stake logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: HIGH: 1.

> **Key Finding**: This bug report is about data validation in the runtime/picasso/src/weights/balances.rs and runtime/picasso/src/weights/democracy.rs files. When a user requests the price of an asset, oracles submit prices by calling the submit_price function. This function checks whether the oracle has staked the m

### Vulnerability Description

#### Root Cause

Implementation flaw in oracle missing stake logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies oracle missing stake in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to oracle operations

### Vulnerable Pattern Examples

**Example 1: Failure to enforce minimum oracle stake requirement** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/failure-to-enforce-minimum-oracle-stake-requirement.md`
```rust
pub fn handle_payout(
    pre_prices: &[PrePrice<T::PriceValue, T::BlockNumber, T::AccountId>],
    price: T::PriceValue,
    asset_id: T::AssetId,
) {
    for answer in pre_prices {
        let accuracy: Percent;
        if answer.price < price {
            accuracy = PerThing::from_rational(answer.price, price);
        } else {
            let adjusted_number = price.saturating_sub(answer.price - price);
            accuracy = PerThing::from_rational(adjusted_number, price);
        }
        let min_accuracy = AssetsInfo::<T>::get(asset_id).threshold;
        if accuracy < min_accuracy {
            let slash_amount = T::SlashAmount::get();
            let try_slash = T::Currency::can_slash(&answer.who, slash_amount);
            if !try_slash {
                log::warn!("Failed to slash {:?}", answer.who);
            }
            T::Currency::slash(&answer.who, slash_amount);
            Self::deposit_event(Event::UserSlashed(
                answer.who.clone(),
                asset_id,
                slash_amount,
            ));
        }
    }
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in oracle missing stake logic allows exploitation through missing validation, in
func secureOracleMissingStake(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 1
- **Affected Protocols**: Advanced Blockchain
- **Validation Strength**: Single auditor

---

## 7. Oracle Chainlink Specific

### Overview

Implementation flaw in oracle chainlink specific logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: HIGH: 1.

> **Key Finding**: KelpDAO is a staking protocol that relies on Chainlink price feeds to calculate the rsETH/ETH exchange rate. The price feed has an acceptable deviation of [-2% 2%], meaning that the nodes will not update an on-chain price if the boundaries are not reached within the 24 hour period. This creates an a

### Vulnerability Description

#### Root Cause

Implementation flaw in oracle chainlink specific logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies oracle chainlink specific in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to oracle operations

### Vulnerable Pattern Examples

**Example 1: [H-01] Possible arbitrage from Chainlink price discrepancy** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-possible-arbitrage-from-chainlink-price-discrepancy.md`
```go
*   `test_DepositAsset()`:
        *
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in oracle chainlink specific logic allows exploitation through missing validatio
func secureOracleChainlinkSpecific(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 1
- **Affected Protocols**: Kelp DAO
- **Validation Strength**: Single auditor

---

## 8. Oracle Wrong Price Usage

### Overview

Implementation flaw in oracle wrong price usage logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 1, MEDIUM: 1.

> **Key Finding**: This bug report is about an issue found in the ChainlinkAdapterOracle which could return the wrong price for an asset if the underlying aggregator hits minAnswer. The issue was found by 0x52 and is related to the ChainlinkFeedRegistry which pulls the associated aggregator and requests round data fro

### Vulnerability Description

#### Root Cause

Implementation flaw in oracle wrong price usage logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies oracle wrong price usage in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to oracle operations

### Vulnerable Pattern Examples

**Example 1: ChainlinkAdapterOracle will return the wrong price for asset if underlying aggre** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-16-chainlinkadapteroracle-will-return-the-wrong-price-for-asset-if-underlying-.md`
```go
This comment is true but in my submission I address this exact issue and why it's still an issue even if the aggregator has multiple sources:

> Note:
> Chainlink oracles are used a just one piece of the OracleAggregator system and it is assumed that using a combination of other oracles, a scenario like this can be avoided. However this is not the case because the other oracles also have their flaws that can still allow this to be exploited. As an example if the chainlink oracle is being used with a UniswapV3Oracle which uses a long TWAP then this will be exploitable when the TWAP is near the minPrice on the way down. In a scenario like that it wouldn't matter what the third oracle was because it would be bypassed with the two matching oracles prices. If secondary oracles like Band are used a malicious user could DDOS relayers to prevent update pricing. Once the price becomes stale the chainlink oracle would be the only oracle left and it's price would be used.
```

**Example 2: Wrong capTokenDecimals value used in StakedCapAdapter.price causes inaccurate pr** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/wrong-captokendecimals-value-used-in-stakedcapadapterprice-causes-inaccurate-pri.md`
```solidity
function price(address _asset) external view returns (uint256 latestAnswer, uint256 lastUpdated) {
    address capToken = IERC4626(_asset).asset();
    (latestAnswer, lastUpdated) = IOracle(msg.sender).getPrice(capToken);
    uint256 capTokenDecimals = IERC20Metadata(capToken).decimals();
    uint256 pricePerFullShare = IERC4626(_asset).convertToAssets(capTokenDecimals);
    latestAnswer = latestAnswer * pricePerFullShare / capTokenDecimals;
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in oracle wrong price usage logic allows exploitation through missing validation
func secureOracleWrongPriceUsage(ctx sdk.Context) error {
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
- **Affected Protocols**: CAP Labs Covered Agent Protocol, Blueberry
- **Validation Strength**: Moderate (2 auditors)

---

## Detection Patterns

### Automated Detection
```
# Oracle Stale Price
grep -rn 'oracle|stale|price' --include='*.go' --include='*.sol'
# Oracle Price Manipulation
grep -rn 'oracle|price|manipulation' --include='*.go' --include='*.sol'
# Oracle Dos
grep -rn 'oracle|dos' --include='*.go' --include='*.sol'
# Oracle Deviation Exploit
grep -rn 'oracle|deviation|exploit' --include='*.go' --include='*.sol'
# Oracle Frontrunning
grep -rn 'oracle|frontrunning' --include='*.go' --include='*.sol'
# Oracle Missing Stake
grep -rn 'oracle|missing|stake' --include='*.go' --include='*.sol'
# Oracle Chainlink Specific
grep -rn 'oracle|chainlink|specific' --include='*.go' --include='*.sol'
# Oracle Wrong Price Usage
grep -rn 'oracle|wrong|price|usage' --include='*.go' --include='*.sol'
```

## Keywords

`able`, `aggregator`, `allows`, `appchain`, `arbitrage`, `asset`, `assets`, `avoid`, `borrow`, `bridge`, `captokendecimals`, `causes`, `chainlink`, `chainlinkadapteroracle`, `changes`, `check`, `cosmos`, `decrease`, `deviation`, `discrepancy`, `dos`, `dosing`, `enforce`, `exploit`, `exploits`, `failure`, `freeze`, `from`, `frontrun`, `frontrunning`

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

`appchain`, `borrow`, `burn`, `chainlink_specific`, `cosmos`, `defi`, `deposit`, `deviation_exploit`, `dos`, `frontrunning`, `getPrice`, `mint`, `missing_stake`, `msg.sender`, `oracle`, `oracle_price_vulnerabilities`, `price`, `price_manipulation`, `queryExchangeRate`, `staking`, `stale_price`, `update`, `withdraw`, `wrong_price_usage`
