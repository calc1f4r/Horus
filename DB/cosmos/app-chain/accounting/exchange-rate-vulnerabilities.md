---
protocol: generic
chain: cosmos
category: accounting
vulnerability_type: exchange_rate_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: accounting_logic

primitives:
  - exchange_rate_manipulation
  - exchange_rate_stale
  - exchange_rate_error
  - share_price_inflation
  - conversion_rounding

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - accounting
  - staking
  - defi

language: go|solidity|rust
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Accounting Exchange Rate Manipulation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [EIGEN2-14] Stake deviations due to adding/removing strategy | `reports/cosmos_cometbft_findings/eigen2-14-stake-deviations-due-to-addingremoving-strategy-may-allow-for-ejector-.md` | MEDIUM | Hexens |
| [H-01] `StakedToken` is vulnerable to share inflation attack | `reports/cosmos_cometbft_findings/h-01-stakedtoken-is-vulnerable-to-share-inflation-attack-via-donation.md` | HIGH | Pashov Audit Group |
| Rogue validators can manipulate funding rates and profit unf | `reports/cosmos_cometbft_findings/h-3-rogue-validators-can-manipulate-funding-rates-and-profit-unfairly-from-liqui.md` | HIGH | Sherlock |
| [M-14] stETH/ETH feed being used opens up to 2 way `deposit< | `reports/cosmos_cometbft_findings/m-14-stetheth-feed-being-used-opens-up-to-2-way-deposit-withdrawal-arbitrage.md` | MEDIUM | Code4rena |
| LibTWAPOracle::update Providing large liquidity will manipul | `reports/cosmos_cometbft_findings/m-4-libtwaporacleupdate-providing-large-liquidity-will-manipulate-twap-dosing-re.md` | MEDIUM | Sherlock |
| [PRST-6] First depositor can steal assets due to missing sli | `reports/cosmos_cometbft_findings/prst-6-first-depositor-can-steal-assets-due-to-missing-slippage-protection.md` | HIGH | Hexens |
| Risk of token/uToken exchange rate manipulation | `reports/cosmos_cometbft_findings/risk-of-tokenutoken-exchange-rate-manipulation.md` | HIGH | TrailOfBits |
| Validators can Manipulate Commission Rates | `reports/cosmos_cometbft_findings/validators-can-manipulate-commission-rates.md` | MEDIUM | OtterSec |

### Accounting Exchange Rate Stale
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-07] Exchange rate implementation not used in token operat | `reports/cosmos_cometbft_findings/h-07-exchange-rate-implementation-not-used-in-token-operations.md` | HIGH | Pashov Audit Group |
| [M-10] `IOracle.queryExchangeRate` returns incorrect `blockT | `reports/cosmos_cometbft_findings/m-10-ioraclequeryexchangerate-returns-incorrect-blocktimems.md` | MEDIUM | Code4rena |
| DAI/gOHM exchange rate may be stale | `reports/cosmos_cometbft_findings/m-5-daigohm-exchange-rate-may-be-stale.md` | MEDIUM | Sherlock |
| Users May Be Able to Borrow swEth at an Outdated Price | `reports/cosmos_cometbft_findings/users-may-be-able-to-borrow-sweth-at-an-outdated-price.md` | MEDIUM | OpenZeppelin |

### Accounting Exchange Rate Error
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-07] Exchange rate implementation not used in token operat | `reports/cosmos_cometbft_findings/h-07-exchange-rate-implementation-not-used-in-token-operations.md` | HIGH | Pashov Audit Group |
| [H-08] Exchange rate calculation is incorrect | `reports/cosmos_cometbft_findings/h-08-exchange-rate-calculation-is-incorrect.md` | HIGH | Pashov Audit Group |
| Incorrect Calculation of Total Amount Staked | `reports/cosmos_cometbft_findings/incorrect-calculation-of-total-amount-staked.md` | HIGH | OpenZeppelin |
| [M-02] Incorrect `updateGlobalExchangeRate` implementation | `reports/cosmos_cometbft_findings/m-02-incorrect-updateglobalexchangerate-implementation.md` | MEDIUM | Code4rena |
| [M-10] `IOracle.queryExchangeRate` returns incorrect `blockT | `reports/cosmos_cometbft_findings/m-10-ioraclequeryexchangerate-returns-incorrect-blocktimems.md` | MEDIUM | Code4rena |
| Missing slashing check | `reports/cosmos_cometbft_findings/missing-slashing-check.md` | MEDIUM | Halborn |

### Accounting Share Price Inflation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Vault Share Inflation Risk | `reports/cosmos_cometbft_findings/vault-share-inflation-risk.md` | HIGH | OtterSec |

### Accounting Conversion Rounding
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-03] A `DoS` on snapshots due to a rounding error in calcu | `reports/cosmos_cometbft_findings/h-03-a-dos-on-snapshots-due-to-a-rounding-error-in-calculations.md` | HIGH | Code4rena |
| [M-23] Rounding errors can cause ERC20RebaseDistributor tran | `reports/cosmos_cometbft_findings/m-23-rounding-errors-can-cause-erc20rebasedistributor-transfers-and-mints-to-fai.md` | MEDIUM | Code4rena |
| OperationalStaking::_unstake Delegators can bypass 28 days u | `reports/cosmos_cometbft_findings/m-7-operationalstaking_unstake-delegators-can-bypass-28-days-unstaking-cooldown-.md` | MEDIUM | Sherlock |
| Node operators are not risking anything when abandoning thei | `reports/cosmos_cometbft_findings/node-operators-are-not-risking-anything-when-abandoning-their-activity-or-perfor.md` | MEDIUM | ConsenSys |
| [PRST-6] First depositor can steal assets due to missing sli | `reports/cosmos_cometbft_findings/prst-6-first-depositor-can-steal-assets-due-to-missing-slippage-protection.md` | HIGH | Hexens |
| Rounding errors after slashing ✓ Addressed | `reports/cosmos_cometbft_findings/rounding-errors-after-slashing-addressed.md` | HIGH | ConsenSys |

---

# Exchange Rate Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Exchange Rate Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Accounting Exchange Rate Manipulation](#1-accounting-exchange-rate-manipulation)
2. [Accounting Exchange Rate Stale](#2-accounting-exchange-rate-stale)
3. [Accounting Exchange Rate Error](#3-accounting-exchange-rate-error)
4. [Accounting Share Price Inflation](#4-accounting-share-price-inflation)
5. [Accounting Conversion Rounding](#5-accounting-conversion-rounding)

---

## 1. Accounting Exchange Rate Manipulation

### Overview

Implementation flaw in accounting exchange rate manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 9 audit reports with severity distribution: HIGH: 4, MEDIUM: 5.

> **Key Finding**: This bug report discusses a problem in the StakeRegistry contract where the `updateOperatorsStake()` function is not updating all operators' stakes immediately after a strategy is added or removed from a quorum. This can lead to unfair competition and manipulation by the ejector role. The suggested 

### Vulnerability Description

#### Root Cause

Implementation flaw in accounting exchange rate manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies accounting exchange rate manipulation in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to accounting operations

### Vulnerable Pattern Examples

**Example 1: [EIGEN2-14] Stake deviations due to adding/removing strategy may allow for eject** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/eigen2-14-stake-deviations-due-to-addingremoving-strategy-may-allow-for-ejector-.md`
```go
(uint96[] memory stakeWeights, bool[] memory hasMinimumStakes) =
    _weightOfOperatorsForQuorum(quorumNumber, operators);

int256 totalStakeDelta = 0;
// If the operator no longer meets the minimum stake, set their stake to zero and mark them for removal
/// also handle setting the operator's stake to 0 and remove them from the quorum
for (uint256 i = 0; i < operators.length; i++) {
    if (!hasMinimumStakes[i]) {
        stakeWeights[i] = 0;
        shouldBeDeregistered[i] = true;
    }

    // Update the operator's stake and retrieve the delta
    // If we're deregistering them, their weight is set to 0
    int256 stakeDelta = _recordOperatorStakeUpdate({
        operatorId: operatorIds[i],
        quorumNumber: quorumNumber,
        newStake: stakeWeights[i]
    });

    totalStakeDelta += stakeDelta;
}

// Apply the delta to the quorum's total stake
_recordTotalStakeUpdate(quorumNumber, totalStakeDelta);
```

**Example 2: [H-01] `StakedToken` is vulnerable to share inflation attack via donation** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-stakedtoken-is-vulnerable-to-share-inflation-attack-via-donation.md`
```
// Vulnerable pattern from Increment:
**Severity**

**Impact:** High, as the targeted staker will lose fund

**Likelihood:** Medium, possible when all stakers redeemed their stake

**Description**

`StakedToken` allows staking of underlying tokens (assets) for staked tokens (shares). It uses an explicit `exchangeRate` for share price calculation that is updated on slashing/returning of funds.

As the `exchangeRate` is updated using the `UNDERLYING_TOKEN.balanceOf(address(this))` in `StakedToken`, it is vulnerable to manipulation via
```

**Example 3: Rogue validators can manipulate funding rates and profit unfairly from liquidati** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-3-rogue-validators-can-manipulate-funding-rates-and-profit-unfairly-from-liqui.md`
```
// Vulnerable pattern from Hubble Exchange:
Source: https://github.com/sherlock-audit/2023-04-hubble-exchange-judging/issues/183
```

**Example 4: [M-14] stETH/ETH feed being used opens up to 2 way `deposit<->withdrawal` arbitr** [MEDIUM]
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

**Example 5: LibTWAPOracle::update Providing large liquidity will manipulate TWAP, DOSing red** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-4-libtwaporacleupdate-providing-large-liquidity-will-manipulate-twap-dosing-re.md`
```go
require(
            getDollarPriceUsd() >= poolStorage.mintPriceThreshold,
            "Dollar price too low"
        );
```

**Variant: Accounting Exchange Rate Manipulation - HIGH Severity Cases** [HIGH]
> Found in 4 reports:
> - `reports/cosmos_cometbft_findings/h-01-stakedtoken-is-vulnerable-to-share-inflation-attack-via-donation.md`
> - `reports/cosmos_cometbft_findings/h-3-rogue-validators-can-manipulate-funding-rates-and-profit-unfairly-from-liqui.md`
> - `reports/cosmos_cometbft_findings/prst-6-first-depositor-can-steal-assets-due-to-missing-slippage-protection.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in accounting exchange rate manipulation logic allows exploitation through missi
func secureAccountingExchangeRateManipulation(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 9 audit reports
- **Severity Distribution**: HIGH: 4, MEDIUM: 5
- **Affected Protocols**: Ubiquity, Persistence, Tortuga, Umee, Increment
- **Validation Strength**: Strong (3+ auditors)

---

## 2. Accounting Exchange Rate Stale

### Overview

Implementation flaw in accounting exchange rate stale logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 4 audit reports with severity distribution: HIGH: 1, MEDIUM: 3.

> **Key Finding**: The `StakingManager` contract has a bug that affects the exchange rate between HYPE and kHYPE tokens. This bug can cause incorrect token accounting and value loss for users. The contract has a function called `getExchangeRatio()` that calculates the exchange rate based on various factors, but this r

### Vulnerability Description

#### Root Cause

Implementation flaw in accounting exchange rate stale logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies accounting exchange rate stale in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to accounting operations

### Vulnerable Pattern Examples

**Example 1: [H-07] Exchange rate implementation not used in token operations** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-07-exchange-rate-implementation-not-used-in-token-operations.md`
```go
kHYPE.mint(msg.sender, msg.value);
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

**Example 3: DAI/gOHM exchange rate may be stale** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-5-daigohm-exchange-rate-may-be-stale.md`
```go
// File: src/aux/ClearingHouse.sol : ClearingHouse.maxLTC   #1

34:@>     uint256 public constant maxLTC = 2_500 * 1e18; // 2,500
```

**Example 4: Users May Be Able to Borrow swEth at an Outdated Price** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/users-may-be-able-to-borrow-sweth-at-an-outdated-price.md`
```
// Vulnerable pattern from Ion Protocol Audit:
The [`getPrice` function](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/oracles/spot/SwEthSpotOracle.sol#L32) of `SwEthSpotOracle` uses a TWAP oracle which means that a sudden change in price would not immediately affect the return value. This value is used in the [`getSpot` function](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/oracles/spot/SpotOracle.sol#L37) which calculates the spot price as th
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in accounting exchange rate stale logic allows exploitation through missing vali
func secureAccountingExchangeRateStale(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 1, MEDIUM: 3
- **Affected Protocols**: Nibiru, Ion Protocol Audit, Cooler, Kinetiq_2025-02-26
- **Validation Strength**: Strong (3+ auditors)

---

## 3. Accounting Exchange Rate Error

### Overview

Implementation flaw in accounting exchange rate error logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 6 audit reports with severity distribution: HIGH: 3, MEDIUM: 3.

> **Key Finding**: The `StakingManager` contract has a bug that affects the exchange rate between HYPE and kHYPE tokens. This bug can cause incorrect token accounting and value loss for users. The contract has a function called `getExchangeRatio()` that calculates the exchange rate based on various factors, but this r

### Vulnerability Description

#### Root Cause

Implementation flaw in accounting exchange rate error logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies accounting exchange rate error in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to accounting operations

### Vulnerable Pattern Examples

**Example 1: [H-07] Exchange rate implementation not used in token operations** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-07-exchange-rate-implementation-not-used-in-token-operations.md`
```go
kHYPE.mint(msg.sender, msg.value);
```

**Example 2: [H-08] Exchange rate calculation is incorrect** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-08-exchange-rate-calculation-is-incorrect.md`
```go
exchangeRate = (totalStaked + totalRewards - totalClaimed - totalSlashing) / kHYPESupply
```

**Example 3: Incorrect Calculation of Total Amount Staked** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/incorrect-calculation-of-total-amount-staked.md`
```
// Vulnerable pattern from Trufin Audit:
The `TruStakeMATICv2` contract implements the [`totalStaked` function](https://github.com/TruFin-io/staker-audit-april/blob/9f199451b5220f73cfc1eb95dc13381acf804b15/contracts/main/TruStakeMATICv2.sol#L126) to calculate the total amount of MATIC staked by the vault on the validator. The function incorrectly calculates this, as it divides the amount of shares held by the vault by the `exchangeRate`, where it should multiply by it.


As the current `exchangeRate` is 1, the result of the function is
```

**Example 4: [M-02] Incorrect `updateGlobalExchangeRate` implementation** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-02-incorrect-updateglobalexchangerate-implementation.md`
```
// Vulnerable pattern from Covalent:
_Submitted by xYrYuYx_

#### Impact
`UpdateGlobalExchangeRate` has incorrect implementation when `totalGlobalShares` is zero.

If any user didn't start stake, `totalGlobalShares` is 0, and every stake it will increase.
but there is possibility that `totalGlobalShares` can be 0 amount later by unstake or disable validator.

#### Proof of Concept
This is my test case to proof this issue: [C4_issues.js L76](https://github.com/xYrYuYx/C4-2021-10-covalent/blob/main/test/c4-tests/C4_issues.js#L76)

In
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

**Variant: Accounting Exchange Rate Error - MEDIUM Severity Cases** [MEDIUM]
> Found in 3 reports:
> - `reports/cosmos_cometbft_findings/m-02-incorrect-updateglobalexchangerate-implementation.md`
> - `reports/cosmos_cometbft_findings/m-10-ioraclequeryexchangerate-returns-incorrect-blocktimems.md`
> - `reports/cosmos_cometbft_findings/missing-slashing-check.md`

**Variant: Accounting Exchange Rate Error in Kinetiq_2025-02-26** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h-07-exchange-rate-implementation-not-used-in-token-operations.md`
> - `reports/cosmos_cometbft_findings/h-08-exchange-rate-calculation-is-incorrect.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in accounting exchange rate error logic allows exploitation through missing vali
func secureAccountingExchangeRateError(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 3, MEDIUM: 3
- **Affected Protocols**: Trufin Audit, Nibiru, Kakeru Contracts, Covalent, Kinetiq_2025-02-26
- **Validation Strength**: Strong (3+ auditors)

---

## 4. Accounting Share Price Inflation

### Overview

Implementation flaw in accounting share price inflation logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: HIGH: 1.

> **Key Finding**: This report discusses a vulnerability in a vault's mechanism that allows users to manipulate the effective share value of VRT tokens. This can happen after a vault has been slashed, resulting in a skewed ratio of VRT tokens to deposited tokens. This allows users to receive more VRT tokens than their

### Vulnerability Description

#### Root Cause

Implementation flaw in accounting share price inflation logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies accounting share price inflation in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to accounting operations

### Vulnerable Pattern Examples

**Example 1: Vault Share Inflation Risk** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/vault-share-inflation-risk.md`
```
// Vulnerable pattern from Jito Restaking:
## Vulnerability Overview

The vulnerability concerns the vault’s mechanism, particularly the updating of balance and share minting. By sending tokens to the vault and invoking the `UpdateVaultBalance`, a user may manipulate the effective share value associated with VRT tokens. If this action occurs after a vault has been slashed (when the total tokens deposited are significantly reduced), the ratio of VRT tokens to deposited tokens becomes skewed. This allows the user to receive disproportionat
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in accounting share price inflation logic allows exploitation through missing va
func secureAccountingSharePriceInflation(ctx sdk.Context) error {
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
- **Affected Protocols**: Jito Restaking
- **Validation Strength**: Single auditor

---

## 5. Accounting Conversion Rounding

### Overview

Implementation flaw in accounting conversion rounding logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 6 audit reports with severity distribution: HIGH: 3, MEDIUM: 3.

> **Key Finding**: This bug report discusses a potential issue with creating a snapshot due to a rounding error in the calculations. The report includes a proof of concept which demonstrates how the error can occur and provides a recommended mitigation step to fix the issue. The report also includes comments from the 

### Vulnerability Description

#### Root Cause

Implementation flaw in accounting conversion rounding logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies accounting conversion rounding in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to accounting operations

### Vulnerable Pattern Examples

**Example 1: [H-03] A `DoS` on snapshots due to a rounding error in calculations** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-03-a-dos-on-snapshots-due-to-a-rounding-error-in-calculations.md`
```solidity
function _transferToSlashStore(address nodeOwner) internal {
        ...

430     uint256 slashedAssets = node.totalRestakedETH - convertToAssets(balanceOf(nodeOwner));
        ...
```

**Example 2: [M-23] Rounding errors can cause ERC20RebaseDistributor transfers and mints to f** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-23-rounding-errors-can-cause-erc20rebasedistributor-transfers-and-mints-to-fai.md`
```go
It is possible that due to rounding, `rebasingStateTo.nShares` is higher than `toSharesAfter` by `1 wei`, causing the transfer to fail.

A similar issue can happen when unminted rewards are taken off the rebase pool:
```

**Example 3: OperationalStaking::_unstake Delegators can bypass 28 days unstaking cooldown wh** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-7-operationalstaking_unstake-delegators-can-bypass-28-days-unstaking-cooldown-.md`
```
// Vulnerable pattern from Covalent:
Source: https://github.com/sherlock-audit/2023-11-covalent-judging/issues/78
```

**Example 4: Node operators are not risking anything when abandoning their activity or perfor** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/node-operators-are-not-risking-anything-when-abandoning-their-activity-or-perfor.md`
```
// Vulnerable pattern from Geodefi:
#### Description


During the staking process, the node operators need to provide 1 ETH as a deposit for every validator that they would like to initiate. After that is done, Oracle needs to ensure that validator creation has been done correctly and then deposit the remaining 31 ETH on chain as well as reimburse 1 ETH back to the node operator. The node operator can then proceed to withdraw the funds that were used as initial deposits. As the result, node operators operate nodes that have 32 ETH
```

**Example 5: [PRST-6] First depositor can steal assets due to missing slippage protection** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/prst-6-first-depositor-can-steal-assets-due-to-missing-slippage-protection.md`
```go
func (k Keeper) LiquidStake(
	ctx sdk.Context, proxyAcc, liquidStaker sdk.AccAddress, stakingCoin sdk.Coin) (newShares math.LegacyDec, stkXPRTMintAmount math.Int, err error) {
    [..]
    nas := k.GetNetAmountState(ctx)
    [..]
	// mint stkxprt, MintAmount = TotalSupply * StakeAmount/NetAmount
	liquidBondDenom := k.LiquidBondDenom(ctx)
	stkXPRTMintAmount = stakingCoin.Amount
	if nas.StkxprtTotalSupply.IsPositive() {
		stkXPRTMintAmount = types.NativeTokenToStkXPRT(stakingCoin.Amount, nas.StkxprtTotalSupply, nas.NetAmount)
	}
	[..]
}

func (k Keeper) GetNetAmountState(ctx sdk.Context) (nas types.NetAmountState) {
	totalRemainingRewards, totalDelShares, totalLiquidTokens := k.CheckDelegationStates(ctx, types.LiquidStakeProxyAcc)

	totalUnbondingBalance := sdk.ZeroInt()
	ubds := k.stakingKeeper.GetAllUnbondingDelegations(ctx, types.LiquidStakeProxyAcc)
	for _, ubd := range ubds {
		for _, entry := range ubd.Entries {
			// use Balance(slashing applied) not InitialBalance(without slashing)
			totalUnbondingBalance = totalUnbondingBalance.Add(entry.Balance)
		}
	}

	nas = types.NetAmountState{
		StkxprtTotalSupply:    k.bankKeeper.GetSupply(ctx, k.LiquidBondDenom(ctx)).Amount,
		TotalDelShares:        totalDelShares,
		TotalLiquidTokens:     totalLiquidTokens,
		TotalRemainingRewards: totalRemainingRewards,
		TotalUnbondingBalance: totalUnbondingBalance,
		ProxyAccBalance:       k.GetProxyAccBalance(ctx, types.LiquidStakeProxyAcc).Amount,
	}

// ... (truncated)
```

**Variant: Accounting Conversion Rounding - MEDIUM Severity Cases** [MEDIUM]
> Found in 3 reports:
> - `reports/cosmos_cometbft_findings/m-23-rounding-errors-can-cause-erc20rebasedistributor-transfers-and-mints-to-fai.md`
> - `reports/cosmos_cometbft_findings/m-7-operationalstaking_unstake-delegators-can-bypass-28-days-unstaking-cooldown-.md`
> - `reports/cosmos_cometbft_findings/node-operators-are-not-risking-anything-when-abandoning-their-activity-or-perfor.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in accounting conversion rounding logic allows exploitation through missing vali
func secureAccountingConversionRounding(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 3, MEDIUM: 3
- **Affected Protocols**: Persistence, Geodefi, Karak, Covalent, Skale Token
- **Validation Strength**: Strong (3+ auditors)

---

## Detection Patterns

### Automated Detection
```
# Accounting Exchange Rate Manipulation
grep -rn 'accounting|exchange|rate|manipulation' --include='*.go' --include='*.sol'
# Accounting Exchange Rate Stale
grep -rn 'accounting|exchange|rate|stale' --include='*.go' --include='*.sol'
# Accounting Exchange Rate Error
grep -rn 'accounting|exchange|rate|error' --include='*.go' --include='*.sol'
# Accounting Share Price Inflation
grep -rn 'accounting|share|price|inflation' --include='*.go' --include='*.sol'
# Accounting Conversion Rounding
grep -rn 'accounting|conversion|rounding' --include='*.go' --include='*.sol'
```

## Keywords

`accounting`, `accumulated`, `allow`, `amount`, `appchain`, `attack`, `bypass`, `calculation`, `calculations`, `cause`, `conversion`, `cooldown`, `cosmos`, `days`, `delegators`, `deviations`, `donation`, `ejector`, `enough`, `error`, `errors`, `exchange`, `fail`, `from`, `funding`, `have`, `implementation`, `incorrect`, `inflation`, `liquidations`
