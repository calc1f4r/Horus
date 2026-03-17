---
protocol: generic
chain: cosmos
category: fund_safety
vulnerability_type: fund_locking_insolvency

attack_type: logical_error|economic_exploit|dos
affected_component: fund_safety_logic

primitives:
  - lock_permanent
  - lock_conditional
  - insolvency_protocol
  - insolvency_slash
  - insolvency_rebase
  - bad_debt
  - withdrawal_blocked
  - unsafe_casting_loss

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - fund_safety
  - staking
  - defi

language: go|solidity|rust
version: all

# Pattern Identity (Required)
root_cause_family: logic_error
pattern_key: logic_error | fund_safety_logic | fund_locking_insolvency

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: multi_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - _lock
  - a
  - approve
  - bad_debt
  - balanceOf
  - before
  - blameOperator
  - block.timestamp
  - calcAndCacheStakes
  - deposit
  - getRewards
  - getTotalAssetTVL
  - insolvency_protocol
  - insolvency_rebase
  - insolvency_slash
  - lock_conditional
  - lock_permanent
  - locking
  - mint
  - of
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Funds Lock Permanent
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Future epoch cache manipulation via `calcAndCacheStakes` all | `reports/cosmos_cometbft_findings/future-epoch-cache-manipulation-via-calcandcachestakes-allows-reward-manipulatio.md` | HIGH | Cyfrin |
| [H-01] Slashing `NativeVault` will lead to locked ETH for th | `reports/cosmos_cometbft_findings/h-01-slashing-nativevault-will-lead-to-locked-eth-for-the-users.md` | HIGH | Code4rena |
| [H-01] Vesting account preemption attack preventing future c | `reports/cosmos_cometbft_findings/h-01-vesting-account-preemption-attack-preventing-future-contract-deployment.md` | HIGH | Code4rena |
| [H-05] Funds can be permanently locked due to unsafe type ca | `reports/cosmos_cometbft_findings/h-05-funds-can-be-permanently-locked-due-to-unsafe-type-casting.md` | HIGH | Pashov Audit Group |
| Illuminate redemptions don't account for protocol pauses/tem | `reports/cosmos_cometbft_findings/h-13-illuminate-redemptions-dont-account-for-protocol-pausestemporary-blocklisti.md` | HIGH | Sherlock |
| Adversary can break any bounty they wish by depositing an NF | `reports/cosmos_cometbft_findings/h-6-adversary-can-break-any-bounty-they-wish-by-depositing-an-nft-then-refunding.md` | HIGH | Sherlock |
| Insufficient validation in `AvalancheL1Middleware::removeOpe | `reports/cosmos_cometbft_findings/insufficient-validation-in-avalanchel1middlewareremoveoperator-can-create-perman.md` | MEDIUM | Cyfrin |
| [M-05] Last Holder Can’t Exit, Zero‑Supply Unstake Reverts | `reports/cosmos_cometbft_findings/m-05-last-holder-cant-exit-zerosupply-unstake-reverts.md` | MEDIUM | Code4rena |

### Funds Lock Conditional
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| A Relayer Can Avoid a Slash by Requesting a Withdrawal From  | `reports/cosmos_cometbft_findings/a-relayer-can-avoid-a-slash-by-requesting-a-withdrawal-from-the-bond.md` | HIGH | Quantstamp |
| [H-05] Funds can be permanently locked due to unsafe type ca | `reports/cosmos_cometbft_findings/h-05-funds-can-be-permanently-locked-due-to-unsafe-type-casting.md` | HIGH | Pashov Audit Group |
| Loans can exceed the maximum potential debt leading to vault | `reports/cosmos_cometbft_findings/h-24-loans-can-exceed-the-maximum-potential-debt-leading-to-vault-insolvency-and.md` | HIGH | Sherlock |
| Possible to fully block PublicVault.processEpoch function. N | `reports/cosmos_cometbft_findings/h-28-possible-to-fully-block-publicvaultprocessepoch-function-no-one-will-be-abl.md` | HIGH | Sherlock |
| Ignite fee is not returned for pre-validated `QI` stakes in  | `reports/cosmos_cometbft_findings/ignite-fee-is-not-returned-for-pre-validated-qi-stakes-in-the-event-of-registrat.md` | MEDIUM | Cyfrin |
| [M-01] `_safeMint` Will Fail Due To An Edge Case In Calculat | `reports/cosmos_cometbft_findings/m-01-_safemint-will-fail-due-to-an-edge-case-in-calculating-tokenid-using-the-_g.md` | MEDIUM | Code4rena |
| [M-01] `returnFunds()` can be frontrun to profit from an inc | `reports/cosmos_cometbft_findings/m-01-returnfunds-can-be-frontrun-to-profit-from-an-increase-in-share-price.md` | MEDIUM | Pashov Audit Group |
| [M-01] Vault creator can prevent users from claiming staking | `reports/cosmos_cometbft_findings/m-01-vault-creator-can-prevent-users-from-claiming-staking-rewards.md` | MEDIUM | Code4rena |

### Funds Insolvency Protocol
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| _checkBalance Returns an Incorrect Value During Insolvency | `reports/cosmos_cometbft_findings/_checkbalance-returns-an-incorrect-value-during-insolvency.md` | MEDIUM | OpenZeppelin |
| Dust limit attack on `forceUpdateNodes` allows DoS of rebala | `reports/cosmos_cometbft_findings/dust-limit-attack-on-forceupdatenodes-allows-dos-of-rebalancing-and-potential-va.md` | HIGH | Cyfrin |
| [H-04] Strategy allocation tracking errors affect TVL calcul | `reports/cosmos_cometbft_findings/h-04-strategy-allocation-tracking-errors-affect-tvl-calculations.md` | HIGH | Pashov Audit Group |
| [H-05] Withdrawals of rebasing tokens can lead to insolvency | `reports/cosmos_cometbft_findings/h-05-withdrawals-of-rebasing-tokens-can-lead-to-insolvency-and-unfair-distributi.md` | HIGH | Code4rena |
| [H-11] Protocol insolvent - Permanent freeze of funds | `reports/cosmos_cometbft_findings/h-11-protocol-insolvent-permanent-freeze-of-funds.md` | HIGH | Code4rena |
| Public vaults can become insolvent because of missing `yInte | `reports/cosmos_cometbft_findings/h-9-public-vaults-can-become-insolvent-because-of-missing-yintercept-update.md` | HIGH | Sherlock |
| Lido discounted withdrawals are not accounted for | `reports/cosmos_cometbft_findings/lido-discounted-withdrawals-are-not-accounted-for.md` | MEDIUM | Immunefi |
| [M-03] Potential protocol insolvency due to lido slashing ev | `reports/cosmos_cometbft_findings/m-03-potential-protocol-insolvency-due-to-lido-slashing-events.md` | MEDIUM | Pashov Audit Group |

### Funds Insolvency Slash
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| _checkBalance Returns an Incorrect Value During Insolvency | `reports/cosmos_cometbft_findings/_checkbalance-returns-an-incorrect-value-during-insolvency.md` | MEDIUM | OpenZeppelin |
| [H-04] Strategy allocation tracking errors affect TVL calcul | `reports/cosmos_cometbft_findings/h-04-strategy-allocation-tracking-errors-affect-tvl-calculations.md` | HIGH | Pashov Audit Group |
| [M-03] Potential protocol insolvency due to lido slashing ev | `reports/cosmos_cometbft_findings/m-03-potential-protocol-insolvency-due-to-lido-slashing-events.md` | MEDIUM | Pashov Audit Group |
| Possibly protocol insolvency during a LIDO slashing event on | `reports/cosmos_cometbft_findings/possibly-protocol-insolvency-during-a-lido-slashing-event-once-redeemwithdraw-is.md` | MEDIUM | Immunefi |
| Slash during a withdrawal from EigenLayer will break PufferV | `reports/cosmos_cometbft_findings/slash-during-a-withdrawal-from-eigenlayer-will-break-puffervault-accounting.md` | HIGH | Immunefi |

### Funds Insolvency Rebase
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Bond Curve is Not Reset Inside the `submitInitialSlashing` F | `reports/cosmos_cometbft_findings/bond-curve-is-not-reset-inside-the-submitinitialslashing-function.md` | MEDIUM | MixBytes |
| [H-05] Withdrawals of rebasing tokens can lead to insolvency | `reports/cosmos_cometbft_findings/h-05-withdrawals-of-rebasing-tokens-can-lead-to-insolvency-and-unfair-distributi.md` | HIGH | Code4rena |
| [M-03] Potential protocol insolvency due to lido slashing ev | `reports/cosmos_cometbft_findings/m-03-potential-protocol-insolvency-due-to-lido-slashing-events.md` | MEDIUM | Pashov Audit Group |
| `LidoVault::vaultEndedWithdraw` doesn't take into considerat | `reports/cosmos_cometbft_findings/m-1-lidovaultvaultendedwithdraw-doesnt-take-into-consideration-income-withdrawal.md` | MEDIUM | Sherlock |
| Withdrawing after a slash event before the vault has ended w | `reports/cosmos_cometbft_findings/m-2-withdrawing-after-a-slash-event-before-the-vault-has-ended-will-decrease-fix.md` | MEDIUM | Sherlock |
| Negative rebase of stETH could prevent a round from ending | `reports/cosmos_cometbft_findings/negative-rebase-of-steth-could-prevent-a-round-from-ending.md` | MEDIUM | OpenZeppelin |
| Possibly protocol insolvency during a LIDO slashing event on | `reports/cosmos_cometbft_findings/possibly-protocol-insolvency-during-a-lido-slashing-event-once-redeemwithdraw-is.md` | MEDIUM | Immunefi |
| Refund can be over-credited in a negative yield event | `reports/cosmos_cometbft_findings/refund-can-be-over-credited-in-a-negative-yield-event.md` | MEDIUM | OpenZeppelin |

### Funds Bad Debt
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Emergency Withdrawal Conditions Might Change Over Time | `reports/cosmos_cometbft_findings/emergency-withdrawal-conditions-might-change-over-time.md` | MEDIUM | OpenZeppelin |
| Loans can exceed the maximum potential debt leading to vault | `reports/cosmos_cometbft_findings/h-24-loans-can-exceed-the-maximum-potential-debt-leading-to-vault-insolvency-and.md` | HIGH | Sherlock |
| [M-01] No check for sequencer uptime can lead to dutch aucti | `reports/cosmos_cometbft_findings/m-01-no-check-for-sequencer-uptime-can-lead-to-dutch-auctions-failing-or-executi.md` | MEDIUM | Code4rena |
| [M-08] If the strategy incurs a loss the Active Pool will st | `reports/cosmos_cometbft_findings/m-08-if-the-strategy-incurs-a-loss-the-active-pool-will-stop-working-until-the-s.md` | MEDIUM | Code4rena |
| ChainlinkAdapterOracle will return the wrong price for asset | `reports/cosmos_cometbft_findings/m-16-chainlinkadapteroracle-will-return-the-wrong-price-for-asset-if-underlying-.md` | MEDIUM | Sherlock |
| [M-17] Bad debt can be permanently blocked from being moved  | `reports/cosmos_cometbft_findings/m-17-bad-debt-can-be-permanently-blocked-from-being-moved-to-backstop.md` | MEDIUM | Code4rena |
| Attacker can inflict losses to other Superpool user's during | `reports/cosmos_cometbft_findings/m-20-attacker-can-inflict-losses-to-other-superpool-users-during-a-bad-debt-liqu.md` | MEDIUM | Sherlock |
| [M-20] Inability to offboard term twice in a 7-day period ma | `reports/cosmos_cometbft_findings/m-20-inability-to-offboard-term-twice-in-a-7-day-period-may-lead-to-bad-debt-to-.md` | MEDIUM | Code4rena |

### Funds Withdrawal Blocked
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| A Relayer Can Avoid a Slash by Requesting a Withdrawal From  | `reports/cosmos_cometbft_findings/a-relayer-can-avoid-a-slash-by-requesting-a-withdrawal-from-the-bond.md` | HIGH | Quantstamp |
| [C-02] Stakes not forwarded post-delegation, positions unwit | `reports/cosmos_cometbft_findings/c-02-stakes-not-forwarded-post-delegation-positions-unwithdrawable.md` | HIGH | Pashov Audit Group |
| Cannot Blame Operator for Proposed Validator | `reports/cosmos_cometbft_findings/cannot-blame-operator-for-proposed-validator.md` | MEDIUM | ConsenSys |
| Direct Deposits Enable Theft Of A Validator’s Funds | `reports/cosmos_cometbft_findings/direct-deposits-enable-theft-of-a-validators-funds.md` | HIGH | SigmaPrime |
| Emergency Withdrawal Conditions Might Change Over Time | `reports/cosmos_cometbft_findings/emergency-withdrawal-conditions-might-change-over-time.md` | MEDIUM | OpenZeppelin |
| [H-01] `BlockBeforeSend` hook can be exploited to perform a  | `reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md` | HIGH | Code4rena |
| [H-01] `userTotalStaked` invariant will be broken due to vul | `reports/cosmos_cometbft_findings/h-01-usertotalstaked-invariant-will-be-broken-due-to-vulnerable-implementations-.md` | HIGH | Code4rena |
| [H-02] It is impossible to slash queued withdrawals that con | `reports/cosmos_cometbft_findings/h-02-it-is-impossible-to-slash-queued-withdrawals-that-contain-a-malicious-strat.md` | HIGH | Code4rena |

### Funds Unsafe Casting Loss
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-05] Funds can be permanently locked due to unsafe type ca | `reports/cosmos_cometbft_findings/h-05-funds-can-be-permanently-locked-due-to-unsafe-type-casting.md` | HIGH | Pashov Audit Group |

---

# Fund Locking Insolvency - Comprehensive Database

**A Complete Pattern-Matching Guide for Fund Locking Insolvency in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Funds Lock Permanent](#1-funds-lock-permanent)
2. [Funds Lock Conditional](#2-funds-lock-conditional)
3. [Funds Insolvency Protocol](#3-funds-insolvency-protocol)
4. [Funds Insolvency Slash](#4-funds-insolvency-slash)
5. [Funds Insolvency Rebase](#5-funds-insolvency-rebase)
6. [Funds Bad Debt](#6-funds-bad-debt)
7. [Funds Withdrawal Blocked](#7-funds-withdrawal-blocked)
8. [Funds Unsafe Casting Loss](#8-funds-unsafe-casting-loss)

---

## 1. Funds Lock Permanent

### Overview

Implementation flaw in funds lock permanent logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 17 audit reports with severity distribution: HIGH: 7, MEDIUM: 10.

> **Key Finding**: The `AvalancheL1Middleware::calcAndCacheStakes` function in the Suzaku network has a bug where it does not check if the epoch provided is in the future. This allows attackers to manipulate reward calculations by locking in current stake values for future epochs. This can lead to inflated reward shar



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of logic_error"
- Pattern key: `logic_error | fund_safety_logic | fund_locking_insolvency`
- Interaction scope: `multi_contract`
- Primary affected component(s): `fund_safety_logic`
- High-signal code keywords: `_lock`, `a`, `approve`, `bad_debt`, `balanceOf`, `before`, `blameOperator`, `block.timestamp`
- Typical sink / impact: `fund_loss|dos|state_corruption`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `H6.function -> bytecode.function -> can.function`
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

Implementation flaw in funds lock permanent logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies funds lock permanent in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to funds operations

### Vulnerable Pattern Examples

**Example 1: Future epoch cache manipulation via `calcAndCacheStakes` allows reward manipulat** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/future-epoch-cache-manipulation-via-calcandcachestakes-allows-reward-manipulatio.md`
```solidity
function calcAndCacheStakes(uint48 epoch, uint96 assetClassId) public returns (uint256 totalStake) {
    uint48 epochStartTs = getEpochStartTs(epoch); // No validation of epoch timing
    // ... rest of function caches values for any epoch, including future ones
}
```

**Example 2: [H-01] Slashing `NativeVault` will lead to locked ETH for the users** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-slashing-nativevault-will-lead-to-locked-eth-for-the-users.md`
```go
int256 balanceDeltaWei = self.validateSnapshotProof(
                nodeOwner, validatorDetails, balanceContainer.containerRoot, balanceProofs[i]
            );
```

**Example 3: [H-01] Vesting account preemption attack preventing future contract deployment** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-vesting-account-preemption-attack-preventing-future-contract-deployment.md`
```
// Vulnerable pattern from Nibiru:
This vulnerability allows an attacker to preemptively set a target address as a vesting account, permanently blocking contract deployments by Factory contracts or other users to that address. Once the address is marked as a vesting account, any deployment attempt stores the contract bytecode in the state without creating a `codeHash`, rendering the contract permanently inaccessible.

For example, an attacker could target critical ecosystem addresses, such as those planned for LayerZero or Uniswa
```

**Example 4: [H-05] Funds can be permanently locked due to unsafe type casting** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-05-funds-can-be-permanently-locked-due-to-unsafe-type-casting.md`
```go
l1Write.sendTokenDelegate(delegateTo, uint64(amount), false);
```

**Example 5: Illuminate redemptions don't account for protocol pauses/temporary blocklistings** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-13-illuminate-redemptions-dont-account-for-protocol-pausestemporary-blocklisti.md`
```go
// File: src/Redeemer.sol : Redeemer.redeem()   #1

325            // Calculate how much underlying was redeemed
326            uint256 redeemed = IERC20(u).balanceOf(address(this)) - starting;
327    
328            // Update the holding for this market
329:           holdings[u][m] = holdings[u][m] + redeemed;
```

**Variant: Funds Lock Permanent - MEDIUM Severity Cases** [MEDIUM]
> Found in 10 reports:
> - `reports/cosmos_cometbft_findings/insufficient-validation-in-avalanchel1middlewareremoveoperator-can-create-perman.md`
> - `reports/cosmos_cometbft_findings/m-05-last-holder-cant-exit-zerosupply-unstake-reverts.md`
> - `reports/cosmos_cometbft_findings/m-1-delegated-state-is-not-removed-after-it-reaches-zero-potentially-leading-to-.md`

**Variant: Funds Lock Permanent in Suzaku Core** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/future-epoch-cache-manipulation-via-calcandcachestakes-allows-reward-manipulatio.md`
> - `reports/cosmos_cometbft_findings/insufficient-validation-in-avalanchel1middlewareremoveoperator-can-create-perman.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in funds lock permanent logic allows exploitation through missing validation, in
func secureFundsLockPermanent(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 17 audit reports
- **Severity Distribution**: HIGH: 7, MEDIUM: 10
- **Affected Protocols**: KelpDAO, Blend, Stakehouse Protocol, OpenQ, Olas
- **Validation Strength**: Strong (3+ auditors)

---

## 2. Funds Lock Conditional

### Overview

Implementation flaw in funds lock conditional logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 23 audit reports with severity distribution: HIGH: 8, MEDIUM: 15.

> **Key Finding**: The team has fixed a previous issue, but a new issue still exists. The `bondWithdrawal` function can only track one type of token, but the `BondManager` can support multiple tokens. This can lead to unexpected behavior in the `withdraw()` function. The team has made a second round of fixes by adding

### Vulnerability Description

#### Root Cause

Implementation flaw in funds lock conditional logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies funds lock conditional in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to funds operations

### Vulnerable Pattern Examples

**Example 1: A Relayer Can Avoid a Slash by Requesting a Withdrawal From the Bond** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/a-relayer-can-avoid-a-slash-by-requesting-a-withdrawal-from-the-bond.md`
```
// Vulnerable pattern from Pheasant Network:
**Update**
The team fixed the described issue. However, an issue persisted: `bondWithdrawal` can only keep track of one token, but `BondManager` supports several tokens. `getBond()` receives a token ID as parameter (token A) and subtracts `bondWithdrawal.withdrawalAmount` (can be ANY token). This wrong accounting can lead to unexpected behavior in `PheasantNetworkBridgeChild.withdraw()`.

In a second round of fixes, the team solved this additional issue by adding a mapping to differentiate depos
```

**Example 2: [H-05] Funds can be permanently locked due to unsafe type casting** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-05-funds-can-be-permanently-locked-due-to-unsafe-type-casting.md`
```go
l1Write.sendTokenDelegate(delegateTo, uint64(amount), false);
```

**Example 3: Loans can exceed the maximum potential debt leading to vault insolvency and poss** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-24-loans-can-exceed-the-maximum-potential-debt-leading-to-vault-insolvency-and.md`
```
// Vulnerable pattern from Astaria:
Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/169
```

**Example 4: Ignite fee is not returned for pre-validated `QI` stakes in the event of registr** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/ignite-fee-is-not-returned-for-pre-validated-qi-stakes-in-the-event-of-registrat.md`
```
// Vulnerable pattern from Benqi Ignite:
**Description:** The `1 AVAX` [Ignite fee](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L387) applied to pre-validated `QI` stakes is [paid to the fee recipient](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L388) at the time of registration. If this registration fails (e.g. due to off-chain BLS proof validation), the registration will be [marked as withdrawable](https://githu
```

**Example 5: [M-01] `_safeMint` Will Fail Due To An Edge Case In Calculating `tokenId` Using ** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-01-_safemint-will-fail-due-to-an-edge-case-in-calculating-tokenid-using-the-_g.md`
```solidity
function _lock(uint256 amount_, uint256 duration_, address destination_) internal returns (uint256 tokenId_) {
    // Prevent locking 0 amount in order generate many score-less NFTs, even if it is inefficient, and such NFTs would be ignored.
    require(amount_ != uint256(0) && amount_ <= MAX_TOTAL_XDEFI_SUPPLY, "INVALID_AMOUNT");

    // Get bonus multiplier and check that it is not zero (which validates the duration).
    uint8 bonusMultiplier = bonusMultiplierOf[duration_];
    require(bonusMultiplier != uint8(0), "INVALID_DURATION");

    // Mint a locked staked position NFT to the destination.
    _safeMint(destination_, tokenId_ = _generateNewTokenId(_getPoints(amount_, duration_)));

    // Track deposits.
    totalDepositedXDEFI += amount_;

    // Create Position.
    uint96 units = uint96((amount_ * uint256(bonusMultiplier)) / uint256(100));
    totalUnits += units;
    positionOf[tokenId_] =
        Position({
            units: units,
            depositedXDEFI: uint88(amount_),
            expiry: uint32(block.timestamp + duration_),
            created: uint32(block.timestamp),
            bonusMultiplier: bonusMultiplier,
            pointsCorrection: -_toInt256Safe(_pointsPerUnit * units)
        });

    emit LockPositionCreated(tokenId_, destination_, amount_, duration_);
}
```

**Variant: Funds Lock Conditional - MEDIUM Severity Cases** [MEDIUM]
> Found in 15 reports:
> - `reports/cosmos_cometbft_findings/ignite-fee-is-not-returned-for-pre-validated-qi-stakes-in-the-event-of-registrat.md`
> - `reports/cosmos_cometbft_findings/m-01-_safemint-will-fail-due-to-an-edge-case-in-calculating-tokenid-using-the-_g.md`
> - `reports/cosmos_cometbft_findings/m-01-returnfunds-can-be-frontrun-to-profit-from-an-increase-in-share-price.md`

**Variant: Funds Lock Conditional in Pheasant Network** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/a-relayer-can-avoid-a-slash-by-requesting-a-withdrawal-from-the-bond.md`
> - `reports/cosmos_cometbft_findings/the-invariant-totalslashableamount-lockedamountinbond-is-not-enforced-in-the-cod.md`

**Variant: Funds Lock Conditional in Astaria** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h-24-loans-can-exceed-the-maximum-potential-debt-leading-to-vault-insolvency-and.md`
> - `reports/cosmos_cometbft_findings/h-28-possible-to-fully-block-publicvaultprocessepoch-function-no-one-will-be-abl.md`

**Variant: Funds Lock Conditional in Benqi Ignite** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/ignite-fee-is-not-returned-for-pre-validated-qi-stakes-in-the-event-of-registrat.md`
> - `reports/cosmos_cometbft_findings/redemption-of-slashed-registrations-could-result-in-dos-due-to-incorrect-state-u.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in funds lock conditional logic allows exploitation through missing validation, 
func secureFundsLockConditional(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 23 audit reports
- **Severity Distribution**: HIGH: 8, MEDIUM: 15
- **Affected Protocols**: ZetaChain Cross-Chain, Casimir, Lava, Pheasant Network, Ethereum Credit Guild
- **Validation Strength**: Strong (3+ auditors)

---

## 3. Funds Insolvency Protocol

### Overview

Implementation flaw in funds insolvency protocol logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 11 audit reports with severity distribution: HIGH: 6, MEDIUM: 5.

> **Key Finding**: The `_checkBalance` function in the OETHVaultCore.sol contract is not returning the correct balance in certain scenarios. Specifically, if the WETH in the withdrawal queue exceeds the total amount of workable assets, the function should return a balance of 0 but instead returns the amount of WETH in

### Vulnerability Description

#### Root Cause

Implementation flaw in funds insolvency protocol logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies funds insolvency protocol in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to funds operations

### Vulnerable Pattern Examples

**Example 1: _checkBalance Returns an Incorrect Value During Insolvency** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/_checkbalance-returns-an-incorrect-value-during-insolvency.md`
```
// Vulnerable pattern from OETH Withdrawal Queue Audit:
The [`_checkBalance`](https://github.com/OriginProtocol/origin-dollar/blob/eca6ffa74d9d0c5fb467551a30912cb722fab9c2/contracts/contracts/vault/OETHVaultCore.sol#L392-L407) function returns the balance of an asset held in the vault and all the strategies. If the requested asset is WETH, the amount of WETH reserved for the withdrawal queue is subtracted from this balance to reflect the correct amount of workable assets. In this specific case, the function returns the same result as [the `_totalValu
```

**Example 2: Dust limit attack on `forceUpdateNodes` allows DoS of rebalancing and potential ** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/dust-limit-attack-on-forceupdatenodes-allows-dos-of-rebalancing-and-potential-va.md`
```
// Vulnerable pattern from Suzaku Core:
**Description:** An attacker can exploit the `forceUpdateNodes()` function with minimal `limitStake` values to force all validator nodes into a pending update state. By exploiting precision loss in stake-to-weight conversion, an attacker can call `forceUpdateNodes` with a minimal limitStake (e.g., 1 wei), which sets the rebalancing flag without actually reducing any stake, effectively blocking legitimate rebalancing for the entire epoch.

Consider following scenario:
- Large vault undelegation r
```

**Example 3: [H-04] Strategy allocation tracking errors affect TVL calculations** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-04-strategy-allocation-tracking-errors-affect-tvl-calculations.md`
```solidity
function getTotalAssetTVL(address asset) public view returns (uint256 totalTVL) {
    uint256 poolBalance = IERC20(asset).balanceOf(address(this));
    uint256 strategyAllocated = assetsAllocatedToStrategies[asset];
    uint256 unstakingVaultBalance = _getUnstakingVaultBalance(asset);

    return poolBalance + strategyAllocated + unstakingVaultBalance;
}
```

**Example 4: [H-05] Withdrawals of rebasing tokens can lead to insolvency and unfair distribu** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-05-withdrawals-of-rebasing-tokens-can-lead-to-insolvency-and-unfair-distributi.md`
```solidity
pragma solidity ^0.8.19;

import "contracts/Errors/Errors.sol";
import "./Setup.sol";

contract H6 is Setup {

    function testH6() public {
        // we set the buffer to something reasonably high
        WithdrawQueueStorageV1.TokenWithdrawBuffer[] memory buffers = new WithdrawQueueStorageV1.TokenWithdrawBuffer[](2);

        buffers[0] = WithdrawQueueStorageV1.TokenWithdrawBuffer(address(stETH), 100e18 - 1);
        buffers[1] = WithdrawQueueStorageV1.TokenWithdrawBuffer(address(cbETH), 100e18 - 1);

        vm.startPrank(OWNER);
        withdrawQueue.updateWithdrawBufferTarget(buffers);

        // we'll be using stETH and cbETH with unitary price for simplicity
        stEthPriceOracle.setAnswer(1e18);
        cbEthPriceOracle.setAnswer(1e18);

        // and we start with 0 TVL
        (, , uint tvl) = restakeManager.calculateTVLs();
        assertEq(0, tvl);

        // let's then imagine that Alice and Bob hold 90 and 10 ezETH each
        address alice = address(1234567890);
        address bob = address(1234567891);
        stETH.mint(alice, 100e18);
        vm.startPrank(alice);
        stETH.approve(address(restakeManager), 100e18);
        restakeManager.deposit(IERC20(address(stETH)), 100e18);
        ezETH.transfer(bob, 10e18);

        // ✅ TVL and balance are as expected
// ... (truncated)
```

**Example 5: [H-11] Protocol insolvent - Permanent freeze of funds** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-11-protocol-insolvent-permanent-freeze-of-funds.md`
```solidity
function testLockStakersFunds() public {
        uint256 startAmount = 8 ether;
        // Create NodeRunner. Constructor registers two BLS Keys
        address nodeRunner = address(new NodeRunner{value: startAmount}(manager, blsPubKeyOne, blsPubKeyTwo, address(this)));
        
        // Simulate state transitions in lifecycle status to initials registered (value of 1)
        MockAccountManager(factory.accountMan()).setLifecycleStatus(blsPubKeyOne, 1);

        // savETHUser, feesAndMevUser funds used to deposit into validator BLS key #1
        address feesAndMevUser = accountTwo; vm.deal(feesAndMevUser, 4 ether);
        address savETHUser = accountThree; vm.deal(savETHUser, 24 ether);
        
        // deposit savETHUser, feesAndMevUser funds for validator #1
        depositIntoDefaultSavETHVault(savETHUser, blsPubKeyOne, 24 ether);
        depositIntoDefaultStakingFundsVault(feesAndMevUser, blsPubKeyOne, 4 ether);

        // withdraw ETH for first BLS key and reenter
        // This will perform a cross-function reentracy to call stake
        vm.startPrank(nodeRunner);
        manager.withdrawETHForKnot(nodeRunner, blsPubKeyOne);
        // Simulate state transitions in lifecycle status to ETH deposited (value of 2)
        // In real deployment, when stake is called TransactionRouter.registerValidator is called to change the state to DEPOSIT_COMPLETE 
        MockAccountManager(factory.accountMan()).setLifecycleStatus(blsPubKeyOne, 2);
        vm.stopPrank();
        
        // Validate mintDerivatives reverts because of banned public key 
        (,IDataStructures.ETH2DataReport[] memory reports) = getFakeBalanceReport();
        (,IDataStructures.EIP712Signature[] memory sigs) = getFakeEIP712Signature();
        vm.expectRevert("BLS public key is banned or not a part of LSD network");
        manager.mintDerivatives(
            getBytesArrayFromBytes(blsPubKeyOne),
            reports,
            sigs
        );

// ... (truncated)
```

**Variant: Funds Insolvency Protocol - HIGH Severity Cases** [HIGH]
> Found in 6 reports:
> - `reports/cosmos_cometbft_findings/dust-limit-attack-on-forceupdatenodes-allows-dos-of-rebalancing-and-potential-va.md`
> - `reports/cosmos_cometbft_findings/h-04-strategy-allocation-tracking-errors-affect-tvl-calculations.md`
> - `reports/cosmos_cometbft_findings/h-05-withdrawals-of-rebasing-tokens-can-lead-to-insolvency-and-unfair-distributi.md`

**Variant: Funds Insolvency Protocol in Puffer Finance** [MEDIUM]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/lido-discounted-withdrawals-are-not-accounted-for.md`
> - `reports/cosmos_cometbft_findings/possibly-protocol-insolvency-during-a-lido-slashing-event-once-redeemwithdraw-is.md`
> - `reports/cosmos_cometbft_findings/slash-during-a-withdrawal-from-eigenlayer-will-break-puffervault-accounting.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in funds insolvency protocol logic allows exploitation through missing validatio
func secureFundsInsolvencyProtocol(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 11 audit reports
- **Severity Distribution**: HIGH: 6, MEDIUM: 5
- **Affected Protocols**: Astaria, Stakehouse Protocol, Puffer Finance, OETH Withdrawal Queue Audit, Notional
- **Validation Strength**: Strong (3+ auditors)

---

## 4. Funds Insolvency Slash

### Overview

Implementation flaw in funds insolvency slash logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 5 audit reports with severity distribution: HIGH: 2, MEDIUM: 3.

> **Key Finding**: The `_checkBalance` function in the OETHVaultCore.sol contract is not returning the correct balance in certain scenarios. Specifically, if the WETH in the withdrawal queue exceeds the total amount of workable assets, the function should return a balance of 0 but instead returns the amount of WETH in

### Vulnerability Description

#### Root Cause

Implementation flaw in funds insolvency slash logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies funds insolvency slash in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to funds operations

### Vulnerable Pattern Examples

**Example 1: _checkBalance Returns an Incorrect Value During Insolvency** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/_checkbalance-returns-an-incorrect-value-during-insolvency.md`
```
// Vulnerable pattern from OETH Withdrawal Queue Audit:
The [`_checkBalance`](https://github.com/OriginProtocol/origin-dollar/blob/eca6ffa74d9d0c5fb467551a30912cb722fab9c2/contracts/contracts/vault/OETHVaultCore.sol#L392-L407) function returns the balance of an asset held in the vault and all the strategies. If the requested asset is WETH, the amount of WETH reserved for the withdrawal queue is subtracted from this balance to reflect the correct amount of workable assets. In this specific case, the function returns the same result as [the `_totalValu
```

**Example 2: [H-04] Strategy allocation tracking errors affect TVL calculations** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-04-strategy-allocation-tracking-errors-affect-tvl-calculations.md`
```solidity
function getTotalAssetTVL(address asset) public view returns (uint256 totalTVL) {
    uint256 poolBalance = IERC20(asset).balanceOf(address(this));
    uint256 strategyAllocated = assetsAllocatedToStrategies[asset];
    uint256 unstakingVaultBalance = _getUnstakingVaultBalance(asset);

    return poolBalance + strategyAllocated + unstakingVaultBalance;
}
```

**Example 3: [M-03] Potential protocol insolvency due to lido slashing events** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-03-potential-protocol-insolvency-due-to-lido-slashing-events.md`
```solidity
// LidoStrategy.sol
function getRewards(address receiver,IStrategyManager.StrategyStruct memory _strategyBalance) public override view returns(uint256){
    uint256 balance_strategy = _strategyBalance.valueDeposited +_strategyBalance.rewardsEarned -_strategyBalance.valueWithdrawn;
@>    if (IERC20(TOKEN_ADDRESS).balanceOf(receiver)>balance_strategy){
        return IERC20(TOKEN_ADDRESS).balanceOf(receiver) - balance_strategy;
    }
    else{
        return 0;
    }
}
```

**Example 4: Possibly protocol insolvency during a LIDO slashing event once redeem/withdraw i** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/possibly-protocol-insolvency-during-a-lido-slashing-event-once-redeemwithdraw-is.md`
```solidity
function totalAssets() public view virtual override returns (uint256) {
	return _ST_ETH.balanceOf(address(this)) + getELBackingEthAmount() + getPendingLidoETHAmount()
		+ address(this).balance;
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in funds insolvency slash logic allows exploitation through missing validation, 
func secureFundsInsolvencySlash(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 2, MEDIUM: 3
- **Affected Protocols**: Elytra_2025-07-10, Nexus_2024-11-29, OETH Withdrawal Queue Audit, Puffer Finance
- **Validation Strength**: Strong (3+ auditors)

---

## 5. Funds Insolvency Rebase

### Overview

Implementation flaw in funds insolvency rebase logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 9 audit reports with severity distribution: HIGH: 1, MEDIUM: 8.

> **Key Finding**: The report describes a bug in the `submitInitialSlashing` function of the `CSModule` contract. This bug causes the bond curve for a Node Operator to not be reset to the default after being penalized. This could lead to incorrect counting of unbonded validator keys. The severity of this bug is classi

### Vulnerability Description

#### Root Cause

Implementation flaw in funds insolvency rebase logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies funds insolvency rebase in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to funds operations

### Vulnerable Pattern Examples

**Example 1: Bond Curve is Not Reset Inside the `submitInitialSlashing` Function** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/bond-curve-is-not-reset-inside-the-submitinitialslashing-function.md`
```
// Vulnerable pattern from Lido:
##### Description
The issue is identified within the [`submitInitialSlashing`](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/CSModule.sol#L1174) function of the `CSModule` contract, where the initial slashing penalty is applied to the Node Operator bond. While this penalization occurs, the Bond Curve for that Node Operator is not reset to the default.

The issue is classified as **Medium** severity because it may lead to incorrect accou
```

**Example 2: [H-05] Withdrawals of rebasing tokens can lead to insolvency and unfair distribu** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-05-withdrawals-of-rebasing-tokens-can-lead-to-insolvency-and-unfair-distributi.md`
```solidity
pragma solidity ^0.8.19;

import "contracts/Errors/Errors.sol";
import "./Setup.sol";

contract H6 is Setup {

    function testH6() public {
        // we set the buffer to something reasonably high
        WithdrawQueueStorageV1.TokenWithdrawBuffer[] memory buffers = new WithdrawQueueStorageV1.TokenWithdrawBuffer[](2);

        buffers[0] = WithdrawQueueStorageV1.TokenWithdrawBuffer(address(stETH), 100e18 - 1);
        buffers[1] = WithdrawQueueStorageV1.TokenWithdrawBuffer(address(cbETH), 100e18 - 1);

        vm.startPrank(OWNER);
        withdrawQueue.updateWithdrawBufferTarget(buffers);

        // we'll be using stETH and cbETH with unitary price for simplicity
        stEthPriceOracle.setAnswer(1e18);
        cbEthPriceOracle.setAnswer(1e18);

        // and we start with 0 TVL
        (, , uint tvl) = restakeManager.calculateTVLs();
        assertEq(0, tvl);

        // let's then imagine that Alice and Bob hold 90 and 10 ezETH each
        address alice = address(1234567890);
        address bob = address(1234567891);
        stETH.mint(alice, 100e18);
        vm.startPrank(alice);
        stETH.approve(address(restakeManager), 100e18);
        restakeManager.deposit(IERC20(address(stETH)), 100e18);
        ezETH.transfer(bob, 10e18);

        // ✅ TVL and balance are as expected
// ... (truncated)
```

**Example 3: [M-03] Potential protocol insolvency due to lido slashing events** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-03-potential-protocol-insolvency-due-to-lido-slashing-events.md`
```solidity
// LidoStrategy.sol
function getRewards(address receiver,IStrategyManager.StrategyStruct memory _strategyBalance) public override view returns(uint256){
    uint256 balance_strategy = _strategyBalance.valueDeposited +_strategyBalance.rewardsEarned -_strategyBalance.valueWithdrawn;
@>    if (IERC20(TOKEN_ADDRESS).balanceOf(receiver)>balance_strategy){
        return IERC20(TOKEN_ADDRESS).balanceOf(receiver) - balance_strategy;
    }
    else{
        return 0;
    }
}
```

**Example 4: `LidoVault::vaultEndedWithdraw` doesn't take into consideration income withdrawa** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-1-lidovaultvaultendedwithdraw-doesnt-take-into-consideration-income-withdrawal.md`
```go
uint256 totalEarnings = vaultEndingETHBalance.mulDiv(withdrawnStakingEarningsInStakes, vaultEndingStakesAmount) - totalProtocolFee + vaultEndedStakingEarnings;
```

**Example 5: Negative rebase of stETH could prevent a round from ending** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/negative-rebase-of-steth-could-prevent-a-round-from-ending.md`
```
// Vulnerable pattern from Pods Finance Ethereum Volatility Vault Audit:
When a round ends, the amount of underlying assets currently in the vault is [subtracted](https://github.com/pods-finance/yield-contracts/blob/c4b401ce674c24798de5f9d02c82e466ee0a2600/contracts/vaults/STETHVault.sol#L97) from the amount of assets the vault contained in the previous round. This calculation assumes a positive yield, but the underlying asset stETH is able to rebase in both a positive and negative direction due to the potential for slashing. In the case where Lido is slashed, `total
```

**Variant: Funds Insolvency Rebase in Saffron Lido Vaults** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-1-lidovaultvaultendedwithdraw-doesnt-take-into-consideration-income-withdrawal.md`
> - `reports/cosmos_cometbft_findings/m-2-withdrawing-after-a-slash-event-before-the-vault-has-ended-will-decrease-fix.md`

**Variant: Funds Insolvency Rebase in Pods Finance Ethereum Volatility Vault Audit** [MEDIUM]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/negative-rebase-of-steth-could-prevent-a-round-from-ending.md`
> - `reports/cosmos_cometbft_findings/refund-can-be-over-credited-in-a-negative-yield-event.md`
> - `reports/cosmos_cometbft_findings/refunds-will-be-over-credited-in-a-negative-yield-event.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in funds insolvency rebase logic allows exploitation through missing validation,
func secureFundsInsolvencyRebase(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 1, MEDIUM: 8
- **Affected Protocols**: Lido, Saffron Lido Vaults, Puffer Finance, Pods Finance Ethereum Volatility Vault Audit, Renzo
- **Validation Strength**: Strong (3+ auditors)

---

## 6. Funds Bad Debt

### Overview

Implementation flaw in funds bad debt logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 10 audit reports with severity distribution: HIGH: 1, MEDIUM: 9.

> **Key Finding**: The report discusses an issue with the `shutdown` function in the `RizLendingPool` contract. This function takes a snapshot of prices and calculates a ratio for slashing remaining users in the market. However, the owner of the `BadDebtManager` contract can modify this snapshot data without any restr

### Vulnerability Description

#### Root Cause

Implementation flaw in funds bad debt logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies funds bad debt in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to funds operations

### Vulnerable Pattern Examples

**Example 1: Emergency Withdrawal Conditions Might Change Over Time** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/emergency-withdrawal-conditions-might-change-over-time.md`
```
// Vulnerable pattern from Radiant Riz Audit:
After a market has been [shut down](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/riz-lending/RizLendingPoolConfigurator.sol#L491), the `shutdown` function from the `RizLendingPool` contract [takes a snapshot](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/riz-lending/RizLendingPool.sol#L728) through the `BadDebtManager` contract. This is done to keep a record of the [prices in the particular lending pool and al
```

**Example 2: Loans can exceed the maximum potential debt leading to vault insolvency and poss** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-24-loans-can-exceed-the-maximum-potential-debt-leading-to-vault-insolvency-and.md`
```
// Vulnerable pattern from Astaria:
Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/169
```

**Example 3: [M-01] No check for sequencer uptime can lead to dutch auctions failing or execu** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-01-no-check-for-sequencer-uptime-can-lead-to-dutch-auctions-failing-or-executi.md`
```
// Vulnerable pattern from Ethereum Credit Guild:
The `AuctionHouse` contract implements a Dutch auction mechanism to recover debt from collateral. However, there is no check for sequencer uptime, which could lead to auctions failing or executing at unfavorable prices.

The current deployment parameters allow auctions to succeed without a loss to the protocol for a duration of 10m 50s. If there's no bid on the auction after this period, the protocol has no other option but to take a loss or forgive the loan. This could have serious consequences
```

**Example 4: [M-08] If the strategy incurs a loss the Active Pool will stop working until the** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-08-if-the-strategy-incurs-a-loss-the-active-pool-will-stop-working-until-the-s.md`
```go
vars.profit = vars.sharesToAssets.sub(vars.currentAllocated);
```

**Example 5: ChainlinkAdapterOracle will return the wrong price for asset if underlying aggre** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-16-chainlinkadapteroracle-will-return-the-wrong-price-for-asset-if-underlying-.md`
```go
This comment is true but in my submission I address this exact issue and why it's still an issue even if the aggregator has multiple sources:

> Note:
> Chainlink oracles are used a just one piece of the OracleAggregator system and it is assumed that using a combination of other oracles, a scenario like this can be avoided. However this is not the case because the other oracles also have their flaws that can still allow this to be exploited. As an example if the chainlink oracle is being used with a UniswapV3Oracle which uses a long TWAP then this will be exploitable when the TWAP is near the minPrice on the way down. In a scenario like that it wouldn't matter what the third oracle was because it would be bypassed with the two matching oracles prices. If secondary oracles like Band are used a malicious user could DDOS relayers to prevent update pricing. Once the price becomes stale the chainlink oracle would be the only oracle left and it's price would be used.
```

**Variant: Funds Bad Debt in Radiant Riz Audit** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/emergency-withdrawal-conditions-might-change-over-time.md`
> - `reports/cosmos_cometbft_findings/shutdown-is-not-irreversible.md`

**Variant: Funds Bad Debt in Ethereum Credit Guild** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-01-no-check-for-sequencer-uptime-can-lead-to-dutch-auctions-failing-or-executi.md`
> - `reports/cosmos_cometbft_findings/m-20-inability-to-offboard-term-twice-in-a-7-day-period-may-lead-to-bad-debt-to-.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in funds bad debt logic allows exploitation through missing validation, incorrec
func secureFundsBadDebt(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 10 audit reports
- **Severity Distribution**: HIGH: 1, MEDIUM: 9
- **Affected Protocols**: Astaria, Blend, Sentiment V2, Blueberry, Ethos Reserve
- **Validation Strength**: Strong (3+ auditors)

---

## 7. Funds Withdrawal Blocked

### Overview

Implementation flaw in funds withdrawal blocked logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 32 audit reports with severity distribution: HIGH: 14, MEDIUM: 18.

> **Key Finding**: The team has fixed a previous issue, but a new issue still exists. The `bondWithdrawal` function can only track one type of token, but the `BondManager` can support multiple tokens. This can lead to unexpected behavior in the `withdraw()` function. The team has made a second round of fixes by adding

### Vulnerability Description

#### Root Cause

Implementation flaw in funds withdrawal blocked logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies funds withdrawal blocked in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to funds operations

### Vulnerable Pattern Examples

**Example 1: A Relayer Can Avoid a Slash by Requesting a Withdrawal From the Bond** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/a-relayer-can-avoid-a-slash-by-requesting-a-withdrawal-from-the-bond.md`
```
// Vulnerable pattern from Pheasant Network:
**Update**
The team fixed the described issue. However, an issue persisted: `bondWithdrawal` can only keep track of one token, but `BondManager` supports several tokens. `getBond()` receives a token ID as parameter (token A) and subtracts `bondWithdrawal.withdrawalAmount` (can be ANY token). This wrong accounting can lead to unexpected behavior in `PheasantNetworkBridgeChild.withdraw()`.

In a second round of fixes, the team solved this additional issue by adding a mapping to differentiate depos
```

**Example 2: [C-02] Stakes not forwarded post-delegation, positions unwithdrawable** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/c-02-stakes-not-forwarded-post-delegation-positions-unwithdrawable.md`
```go
IERC20(_stakingToken).safeTransferFrom(_stakeMsgSender(), address(this), _amount);
stakers[receiver].amountStaked += _amount;
```

**Example 3: Cannot Blame Operator for Proposed Validator** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/cannot-blame-operator-for-proposed-validator.md`
```solidity
function blameOperator(
 PooledStaking storage self,
 DSML.IsolatedStorage storage DATASTORE,
 bytes calldata pk
) external {
 require(
 self.validators[pk].state == VALIDATOR\_STATE.ACTIVE,
 "SML:validator is never activated"
 );
 require(
 block.timestamp > self.validators[pk].createdAt + self.validators[pk].period,
 "SML:validator is active"
 );

 \_imprison(DATASTORE, self.validators[pk].operatorId, pk);
}
```

**Example 4: Direct Deposits Enable Theft Of A Validator’s Funds** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/direct-deposits-enable-theft-of-a-validators-funds.md`
```
// Vulnerable pattern from Swell:
## Description

If a node operator interacts with the deposit contract directly first, it is possible for them to set the withdrawal address to an arbitrary address. Then this node can be added to Swell and used normally. Once deposits are enabled on the Beacon chain, it is possible for this node operator to withdraw all the ETH deposited with this node. In addition to this, it is impossible for the normal withdrawal method specified by `swNFTUpgrade.sol` to work for deposits made to this node.

```

**Example 5: Emergency Withdrawal Conditions Might Change Over Time** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/emergency-withdrawal-conditions-might-change-over-time.md`
```
// Vulnerable pattern from Radiant Riz Audit:
After a market has been [shut down](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/riz-lending/RizLendingPoolConfigurator.sol#L491), the `shutdown` function from the `RizLendingPool` contract [takes a snapshot](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/riz-lending/RizLendingPool.sol#L728) through the `BadDebtManager` contract. This is done to keep a record of the [prices in the particular lending pool and al
```

**Variant: Funds Withdrawal Blocked - MEDIUM Severity Cases** [MEDIUM]
> Found in 18 reports:
> - `reports/cosmos_cometbft_findings/cannot-blame-operator-for-proposed-validator.md`
> - `reports/cosmos_cometbft_findings/emergency-withdrawal-conditions-might-change-over-time.md`
> - `reports/cosmos_cometbft_findings/improper-handling-of-staked-tokens-when-updating-the-gauge-in-defiappstaker.md`

**Variant: Funds Withdrawal Blocked in Pheasant Network** [HIGH]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/a-relayer-can-avoid-a-slash-by-requesting-a-withdrawal-from-the-bond.md`
> - `reports/cosmos_cometbft_findings/relayer-can-submit-undisputable-evidence-for-l2-l1-trades.md`
> - `reports/cosmos_cometbft_findings/using-abiencodepackedcan-lead-to-hash-collisions.md`

**Variant: Funds Withdrawal Blocked in EigenLayer** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h-02-it-is-impossible-to-slash-queued-withdrawals-that-contain-a-malicious-strat.md`
> - `reports/cosmos_cometbft_findings/middleware-can-deny-withdrawls-by-revoking-slashing-prior-to-queueing-withdrawal.md`

**Variant: Funds Withdrawal Blocked in Renzo** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md`
> - `reports/cosmos_cometbft_findings/m-07-lack-of-slippage-and-deadline-during-withdraw-and-deposit.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in funds withdrawal blocked logic allows exploitation through missing validation
func secureFundsWithdrawalBlocked(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 32 audit reports
- **Severity Distribution**: HIGH: 14, MEDIUM: 18
- **Affected Protocols**: Karak-June, Tokensfarm, Casimir, Karak, Carapace
- **Validation Strength**: Strong (3+ auditors)

---

## 8. Funds Unsafe Casting Loss

### Overview

Implementation flaw in funds unsafe casting loss logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: HIGH: 1.

> **Key Finding**: This report discusses a bug in the `StakingManager` contract that manages staking operations for HYPE tokens. This bug can cause the loss of staked tokens if the amount exceeds a certain limit. It is recommended to implement a library called SafeCast to prevent this issue.

### Vulnerability Description

#### Root Cause

Implementation flaw in funds unsafe casting loss logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies funds unsafe casting loss in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to funds operations

### Vulnerable Pattern Examples

**Example 1: [H-05] Funds can be permanently locked due to unsafe type casting** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-05-funds-can-be-permanently-locked-due-to-unsafe-type-casting.md`
```go
l1Write.sendTokenDelegate(delegateTo, uint64(amount), false);
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in funds unsafe casting loss logic allows exploitation through missing validatio
func secureFundsUnsafeCastingLoss(ctx sdk.Context) error {
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
- **Affected Protocols**: Kinetiq_2025-02-26
- **Validation Strength**: Single auditor

---

## Detection Patterns

### Automated Detection
```
# Funds Lock Permanent
grep -rn 'funds|lock|permanent' --include='*.go' --include='*.sol'
# Funds Lock Conditional
grep -rn 'funds|lock|conditional' --include='*.go' --include='*.sol'
# Funds Insolvency Protocol
grep -rn 'funds|insolvency|protocol' --include='*.go' --include='*.sol'
# Funds Insolvency Slash
grep -rn 'funds|insolvency|slash' --include='*.go' --include='*.sol'
# Funds Insolvency Rebase
grep -rn 'funds|insolvency|rebase' --include='*.go' --include='*.sol'
# Funds Bad Debt
grep -rn 'funds|bad|debt' --include='*.go' --include='*.sol'
# Funds Withdrawal Blocked
grep -rn 'funds|withdrawal|blocked' --include='*.go' --include='*.sol'
# Funds Unsafe Casting Loss
grep -rn 'funds|unsafe|casting|loss' --include='*.go' --include='*.sol'
```

## Keywords

`account`, `affect`, `allocation`, `allows`, `appchain`, `attack`, `auctions`, `avoid`, `bad`, `blame`, `blocked`, `bond`, `cache`, `calculations`, `cannot`, `casting`, `change`, `check`, `conditional`, `conditions`, `contract`, `cosmos`, `curve`, `debt`, `deployment`, `distribution`, `during`, `dust`, `dutch`, `emergency`

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

`_lock`, `a`, `appchain`, `approve`, `bad_debt`, `balanceOf`, `before`, `blameOperator`, `block.timestamp`, `calcAndCacheStakes`, `cosmos`, `defi`, `deposit`, `fund_locking_insolvency`, `fund_safety`, `getRewards`, `getTotalAssetTVL`, `insolvency_protocol`, `insolvency_rebase`, `insolvency_slash`, `lock_conditional`, `lock_permanent`, `locking`, `mint`, `of`, `staking`, `unsafe_casting_loss`, `withdrawal_blocked`
