---
protocol: generic
chain: cosmos
category: rewards
vulnerability_type: reward_distribution_failures

attack_type: logical_error|economic_exploit|dos
affected_component: rewards_logic

primitives:
  - stuck_locked
  - distribution_dos
  - missing_update
  - after_removal
  - unclaimed_loss
  - distribution_unfair
  - epoch_timing

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - rewards
  - staking
  - defi

language: go|solidity|rust
version: all

# Pattern Identity (Required)
root_cause_family: arithmetic_error
pattern_key: arithmetic_error | rewards_logic | reward_distribution_failures

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: multi_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - _calculateOperatorShare
  - _checkOnERC721Received
  - _ethTOeEth
  - _initValidatorScore
  - _safeMint
  - _unstakeNFTs
  - addValidator
  - after_removal
  - balanceOf
  - block.number
  - block.timestamp
  - calcAndCacheStakes
  - claimRewards
  - deRegisterKnotFromSyndicate
  - deposit
  - distribution_dos
  - distribution_unfair
  - epoch_timing
  - for
  - getExpectedAVAXRewardsAmt
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Reward Stuck Locked
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [C-02] Operator can still claim rewards after being removed  | `reports/cosmos_cometbft_findings/c-02-operator-can-still-claim-rewards-after-being-removed-from-governance.md` | HIGH | Pashov Audit Group |
| Funds Allocated for Rewards Can Be Locked in the Contract | `reports/cosmos_cometbft_findings/funds-allocated-for-rewards-can-be-locked-in-the-contract.md` | HIGH | Quantstamp |
| [H-01] `BlockBeforeSend` hook can be exploited to perform a  | `reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md` | HIGH | Code4rena |
| [H-01] Slashing `NativeVault` will lead to locked ETH for th | `reports/cosmos_cometbft_findings/h-01-slashing-nativevault-will-lead-to-locked-eth-for-the-users.md` | HIGH | Code4rena |
| [H-02] Invalid validation in `_farmPlots` function allowing  | `reports/cosmos_cometbft_findings/h-02-invalid-validation-in-_farmplots-function-allowing-a-malicious-user-repeate.md` | HIGH | Code4rena |
| [H-06] BGT stake rewards are locked | `reports/cosmos_cometbft_findings/h-06-bgt-stake-rewards-are-locked.md` | HIGH | Pashov Audit Group |
| [H-09] Attackers can force the rewards to be stuck in the co | `reports/cosmos_cometbft_findings/h-09-attackers-can-force-the-rewards-to-be-stuck-in-the-contract-with-malicious-.md` | HIGH | Code4rena |
| Non-functional vote() if there is one bribe rewarder for thi | `reports/cosmos_cometbft_findings/h-1-non-functional-vote-if-there-is-one-bribe-rewarder-for-this-pool.md` | HIGH | Sherlock |

### Reward Distribution Dos
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Assignment Of Incorrect Reward Escrow | `reports/cosmos_cometbft_findings/assignment-of-incorrect-reward-escrow.md` | HIGH | OtterSec |
| [H-01] `BlockBeforeSend` hook can be exploited to perform a  | `reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md` | HIGH | Code4rena |
| [H-01] Lack of access control in `AgentNftV2::addValidator() | `reports/cosmos_cometbft_findings/h-01-lack-of-access-control-in-agentnftv2addvalidator-enables-unauthorized-valid.md` | HIGH | Code4rena |
| Lack of input validation | `reports/cosmos_cometbft_findings/lack-of-input-validation.md` | MEDIUM | OpenZeppelin |
| Rewards distribution DoS due to uncached secondary asset cla | `reports/cosmos_cometbft_findings/rewards-distribution-dos-due-to-uncached-secondary-asset-classes.md` | MEDIUM | Cyfrin |

### Reward Missing Update
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Any decrease in slashed or rewarded amounts reported will ma | `reports/cosmos_cometbft_findings/any-decrease-in-slashed-or-rewarded-amounts-reported-will-make-validatormanager-.md` | MEDIUM | Spearbit |
| Future epoch cache manipulation via `calcAndCacheStakes` all | `reports/cosmos_cometbft_findings/future-epoch-cache-manipulation-via-calcandcachestakes-allows-reward-manipulatio.md` | HIGH | Cyfrin |
| [H-02] The reentrancy vulnerability in _safeMint can allow a | `reports/cosmos_cometbft_findings/h-02-the-reentrancy-vulnerability-in-_safemint-can-allow-an-attacker-to-steal-al.md` | HIGH | Code4rena |
| Protocol won't be eligible for referral rewards for depositi | `reports/cosmos_cometbft_findings/m-2-protocol-wont-be-eligible-for-referral-rewards-for-depositing-eth.md` | MEDIUM | Sherlock |
| [M-21] EIP1559 rewards received by syndicate during the peri | `reports/cosmos_cometbft_findings/m-21-eip1559-rewards-received-by-syndicate-during-the-period-when-it-has-no-regi.md` | MEDIUM | Code4rena |
| Missing Balance Deduction in Unstaking Functions Allows Cont | `reports/cosmos_cometbft_findings/missing-balance-deduction-in-unstaking-functions-allows-contract-drainage-and-lo.md` | HIGH | Quantstamp |
| Missing Tick and Liquidity Checks in _decodeAndReward (curre | `reports/cosmos_cometbft_findings/missing-tick-and-liquidity-checks-in-_decodeandreward-currentonlytrue-enables-fr.md` | MEDIUM | Cantina |
| Oracle’s _sanityCheck for prices will not work with slashing | `reports/cosmos_cometbft_findings/oracles-_sanitycheck-for-prices-will-not-work-with-slashing.md` | HIGH | ConsenSys |

### Reward After Removal
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [C-02] Operator can still claim rewards after being removed  | `reports/cosmos_cometbft_findings/c-02-operator-can-still-claim-rewards-after-being-removed-from-governance.md` | HIGH | Pashov Audit Group |
| [M-01] `returnFunds()` can be frontrun to profit from an inc | `reports/cosmos_cometbft_findings/m-01-returnfunds-can-be-frontrun-to-profit-from-an-increase-in-share-price.md` | MEDIUM | Pashov Audit Group |
| An earner can still continue earning even after being remove | `reports/cosmos_cometbft_findings/m-1-an-earner-can-still-continue-earning-even-after-being-removed-from-the-appro.md` | MEDIUM | Sherlock |
| Stakers lose their commission if they unstake as they cannot | `reports/cosmos_cometbft_findings/m-8-stakers-lose-their-commission-if-they-unstake-as-they-cannot-claim-their-pen.md` | MEDIUM | Sherlock |
| Operators can lose their reward share | `reports/cosmos_cometbft_findings/operators-can-lose-their-reward-share.md` | MEDIUM | Cyfrin |

### Reward Unclaimed Loss
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Accounting for `rewardStakeRatioSum` is incorrect when a del | `reports/cosmos_cometbft_findings/accounting-for-rewardstakeratiosum-is-incorrect-when-a-delayed-balance-or-reward.md` | HIGH | Cyfrin |
| [C-01] Incorrect reward calculation | `reports/cosmos_cometbft_findings/c-01-incorrect-reward-calculation.md` | HIGH | Pashov Audit Group |
| [C-02] Operator can still claim rewards after being removed  | `reports/cosmos_cometbft_findings/c-02-operator-can-still-claim-rewards-after-being-removed-from-governance.md` | HIGH | Pashov Audit Group |
| Execution failure of `\_updateReward` function due to uninit | `reports/cosmos_cometbft_findings/execution-failure-of-_updatereward-function-due-to-uninitialized-_rewarddistribu.md` | MEDIUM | Halborn |
| Execution of `stake` and `unstake` operations blocked due to | `reports/cosmos_cometbft_findings/execution-of-stake-and-unstake-operations-blocked-due-to-uninitialized-_methods-.md` | MEDIUM | Halborn |
| Fixed exchange rate at unstaking fails to socialize slashing | `reports/cosmos_cometbft_findings/fixed-exchange-rate-at-unstaking-fails-to-socialize-slashing-and-distorts-reward.md` | MEDIUM | MixBytes |
| [H-10] missing `isEpochClaimed` validation | `reports/cosmos_cometbft_findings/h-10-missing-isepochclaimed-validation.md` | HIGH | Code4rena |
| [M-01] User can earn rewards by frontrunning the new rewards | `reports/cosmos_cometbft_findings/m-01-user-can-earn-rewards-by-frontrunning-the-new-rewards-accumulation-in-ron-s.md` | MEDIUM | Code4rena |

### Reward Distribution Unfair
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Fixed exchange rate at unstaking fails to socialize slashing | `reports/cosmos_cometbft_findings/fixed-exchange-rate-at-unstaking-fails-to-socialize-slashing-and-distorts-reward.md` | MEDIUM | MixBytes |
| Funds Allocated for Rewards Can Be Locked in the Contract | `reports/cosmos_cometbft_findings/funds-allocated-for-rewards-can-be-locked-in-the-contract.md` | HIGH | Quantstamp |
| [H-02] Invalid validation in `_farmPlots` function allowing  | `reports/cosmos_cometbft_findings/h-02-invalid-validation-in-_farmplots-function-allowing-a-malicious-user-repeate.md` | HIGH | Code4rena |
| [H-03] Node operator is getting slashed for full duration ev | `reports/cosmos_cometbft_findings/h-03-node-operator-is-getting-slashed-for-full-duration-even-though-rewards-are-.md` | HIGH | Code4rena |
| [H-05] Failure to update dirty flag in `transferToUnoccupied | `reports/cosmos_cometbft_findings/h-05-failure-to-update-dirty-flag-in-transfertounoccupiedplot-prevents-reward-ac.md` | HIGH | Code4rena |
| [H-05] `ValidatorRegistry::validatorScore/getPastValidatorSc | `reports/cosmos_cometbft_findings/h-05-validatorregistryvalidatorscoregetpastvalidatorscore-allows-validator-to-ea.md` | HIGH | Code4rena |
| [H-05] Withdrawals of rebasing tokens can lead to insolvency | `reports/cosmos_cometbft_findings/h-05-withdrawals-of-rebasing-tokens-can-lead-to-insolvency-and-unfair-distributi.md` | HIGH | Code4rena |
| [M-02] Unstaking calculates user share at request time, igno | `reports/cosmos_cometbft_findings/m-02-unstaking-calculates-user-share-at-request-time-ignoring-slashing-leading-t.md` | MEDIUM | Code4rena |

### Reward Epoch Timing
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Activation of queued cutting board can be manipulated leadin | `reports/cosmos_cometbft_findings/activation-of-queued-cutting-board-can-be-manipulated-leading-to-redirection-of-.md` | MEDIUM | Spearbit |
| Flawed Implementation of Reward Score Calculation | `reports/cosmos_cometbft_findings/flawed-implementation-of-reward-score-calculation.md` | HIGH | OtterSec |
| Future epoch cache manipulation via `calcAndCacheStakes` all | `reports/cosmos_cometbft_findings/future-epoch-cache-manipulation-via-calcandcachestakes-allows-reward-manipulatio.md` | HIGH | Cyfrin |
| [H-03] Incorrect boost management leads to staking reward lo | `reports/cosmos_cometbft_findings/h-03-incorrect-boost-management-leads-to-staking-reward-loss.md` | HIGH | Pashov Audit Group |
| [H-10] missing `isEpochClaimed` validation | `reports/cosmos_cometbft_findings/h-10-missing-isepochclaimed-validation.md` | HIGH | Code4rena |
| Immediate stake cache updates enable reward distribution wit | `reports/cosmos_cometbft_findings/immediate-stake-cache-updates-enable-reward-distribution-without-p-chain-confirm.md` | HIGH | Cyfrin |
| [M-05] Changing VoteWeighting contract can result in lost st | `reports/cosmos_cometbft_findings/m-05-changing-voteweighting-contract-can-result-in-lost-staking-incentives.md` | MEDIUM | Code4rena |
| [M-06] `_getRewardsAmountPerVault` might be using an outdate | `reports/cosmos_cometbft_findings/m-06-_getrewardsamountpervault-might-be-using-an-outdated-vault-power.md` | MEDIUM | Pashov Audit Group |

---

# Reward Distribution Failures - Comprehensive Database

**A Complete Pattern-Matching Guide for Reward Distribution Failures in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Reward Stuck Locked](#1-reward-stuck-locked)
2. [Reward Distribution Dos](#2-reward-distribution-dos)
3. [Reward Missing Update](#3-reward-missing-update)
4. [Reward After Removal](#4-reward-after-removal)
5. [Reward Unclaimed Loss](#5-reward-unclaimed-loss)
6. [Reward Distribution Unfair](#6-reward-distribution-unfair)
7. [Reward Epoch Timing](#7-reward-epoch-timing)

---

## 1. Reward Stuck Locked

### Overview

Implementation flaw in reward stuck locked logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 21 audit reports with severity distribution: HIGH: 12, MEDIUM: 9.

> **Key Finding**: A bug has been identified in the `deleteOperators` method, which is used when operators must be slashed. This bug leaves the `operatorRewards` mapping untouched when an operator is removed, meaning they can still claim their accrued rewards, even if they are acting maliciously or are inactive. This 



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of arithmetic_error"
- Pattern key: `arithmetic_error | rewards_logic | reward_distribution_failures`
- Interaction scope: `multi_contract`
- Primary affected component(s): `rewards_logic`
- High-signal code keywords: `_calculateOperatorShare`, `_checkOnERC721Received`, `_ethTOeEth`, `_initValidatorScore`, `_safeMint`, `_unstakeNFTs`, `addValidator`, `after_removal`
- Typical sink / impact: `fund_loss|dos|state_corruption`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `can.function -> owner.function -> that.function`
- Trust boundary crossed: `callback / external call`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: Arithmetic operation on user-controlled input without overflow protection
- Signal 2: Casting between different-width integer types without bounds check
- Signal 3: Multiplication before division where intermediate product can exceed type max
- Signal 4: Accumulator variable can wrap around causing incorrect accounting

#### False Positive Guards

- Not this bug when: Solidity >= 0.8.0 with default checked arithmetic
- Safe if: SafeMath library used for all arithmetic on user-controlled values
- Requires attacker control of: specific conditions per pattern

### Vulnerability Description

#### Root Cause

Implementation flaw in reward stuck locked logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies reward stuck locked in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to reward operations

### Vulnerable Pattern Examples

**Example 1: [C-02] Operator can still claim rewards after being removed from governance** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/c-02-operator-can-still-claim-rewards-after-being-removed-from-governance.md`
```
// Vulnerable pattern from Smoothly:
**Severity**

**Impact:**
High, as rewards shouldn't be claimable for operators that were removed from governance

**Likelihood:**
High, as this will happen every time this functionality is used and an operator has unclaimed rewards

**Description**

The `deleteOperators` method removes an operator account from the `PoolGovernance` but it still leaves the `operatorRewards` mapping untouched, meaning even if an operator is acting maliciously and is removed he can still claim his accrued rewards. 
```

**Example 2: Funds Allocated for Rewards Can Be Locked in the Contract** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/funds-allocated-for-rewards-can-be-locked-in-the-contract.md`
```go
uint256 slashed = (sub.rewardPoints * bps) / _MAX_BIPS; <=== rewardPoints can be greater than 0 but if bps is not big enough, slashed will be 0. 

uint256 slashedValue = (sub.rewardsWithdrawn * bps) / _MAX_BIPS; <=== another instance where `rewardsWithdrawn` might also be a positive value but not large enough, this can result in a 0 value.
```

**Example 3: [H-01] `BlockBeforeSend` hook can be exploited to perform a denial of service** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md`
```go
poc: build
   	@echo "starting POC.."

   	# clear port 26657 if old process still running
   	@if lsof -i :26657; then \
   		kill -9 $$(lsof -t -i :26657) || echo "cannot kill process"; \
   	fi

   	# remove old setup and init new one
   	@rm -rf .mantrapoc
   	@mkdir -p .mantrapoc

   	./build/mantrachaind init poc-test --chain-id test-chain --home .mantrapoc
   	./build/mantrachaind keys add validator --keyring-backend test --home .mantrapoc
   	./build/mantrachaind keys add validator2 --keyring-backend test --home .mantrapoc

   	# create alice and bob account
   	./build/mantrachaind keys add alice --keyring-backend test --home .mantrapoc
   	./build/mantrachaind keys add bob --keyring-backend test --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show validator -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show validator2 -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show alice -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show bob -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc

   	./build/mantrachaind genesis gentx validator 100000000stake --chain-id test-chain --keyring-backend test --home .mantrapoc
   	# ./build/mantrachaind genesis gentx validator2 100000000stake --chain-id test-chain --keyring-backend test --home .mantrapoc

   	./build/mantrachaind genesis collect-gentxs --home .mantrapoc

   	# start node
   	./build/mantrachaind start --home .mantrapoc --minimum-gas-prices 0stake
```

**Example 4: [H-01] Slashing `NativeVault` will lead to locked ETH for the users** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-slashing-nativevault-will-lead-to-locked-eth-for-the-users.md`
```go
int256 balanceDeltaWei = self.validateSnapshotProof(
                nodeOwner, validatorDetails, balanceContainer.containerRoot, balanceProofs[i]
            );
```

**Example 5: [H-02] Invalid validation in `_farmPlots` function allowing a malicious user rep** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-02-invalid-validation-in-_farmplots-function-allowing-a-malicious-user-repeate.md`
```go
if (_getNumPlots(landlord) < _toiler.plotId) {
                timestamp = plotMetadata[landlord].lastUpdated;
                toilerState[tokenId].dirty = true;
            }
```

**Variant: Reward Stuck Locked - MEDIUM Severity Cases** [MEDIUM]
> Found in 9 reports:
> - `reports/cosmos_cometbft_findings/m-01-vault-creator-can-prevent-users-from-claiming-staking-rewards.md`
> - `reports/cosmos_cometbft_findings/m-02-incorrect-updateglobalexchangerate-implementation.md`
> - `reports/cosmos_cometbft_findings/m-05-admin-can-break-all-functionality-through-weth-address.md`

**Variant: Reward Stuck Locked in MANTRA** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md`
> - `reports/cosmos_cometbft_findings/h-09-attackers-can-force-the-rewards-to-be-stuck-in-the-contract-with-malicious-.md`

**Variant: Reward Stuck Locked in Popcorn** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-01-vault-creator-can-prevent-users-from-claiming-staking-rewards.md`
> - `reports/cosmos_cometbft_findings/m-27-faulty-escrow-config-will-lock-up-reward-tokens-in-staking-contract.md`

**Variant: Reward Stuck Locked in Andromeda – Validator Staking ADO and Vesting ADO** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-11-attacker-can-freeze-users-first-rewards.md`
> - `reports/cosmos_cometbft_findings/m-14-lockup-of-vestings-or-completion-time-can-be-bypassed-due-to-missing-check-.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in reward stuck locked logic allows exploitation through missing validation, inc
func secureRewardStuckLocked(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 21 audit reports
- **Severity Distribution**: HIGH: 12, MEDIUM: 9
- **Affected Protocols**: KelpDAO, Munchables, MagicSea - the native DEX on the IotaEVM, Canto, Stakehouse Protocol
- **Validation Strength**: Strong (3+ auditors)

---

## 2. Reward Distribution Dos

### Overview

Implementation flaw in reward distribution dos logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 5 audit reports with severity distribution: HIGH: 3, MEDIUM: 2.

> **Key Finding**: The vulnerability in the maybe_execute_stake_rewards function in OracleHeartbeat arises from incorrect utilization of the remaining_accounts.oracle_switch_reward_escrow account for distributing rewards. This results in the oracle's WSOL reward escrow failing to set up properly and no funds being tra

### Vulnerability Description

#### Root Cause

Implementation flaw in reward distribution dos logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies reward distribution dos in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to reward operations

### Vulnerable Pattern Examples

**Example 1: Assignment Of Incorrect Reward Escrow** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/assignment-of-incorrect-reward-escrow.md`
```rust
pub fn maybe_execute_stake_rewards(
    [...]
) -> Result<()> {
    [...]
    if let Some(oracle_wsol_reward_escrow) = &remaining_accounts.oracle_switch_reward_escrow {
        let res = NativeEscrow::spl_transfer(
            &ctx.accounts.token_program,
            &ctx.accounts.queue_escrow.to_account_info(),
            &oracle_wsol_reward_escrow.to_account_info(),
            &ctx.accounts.program_state.to_account_info(),
            &[&[STATE_SEED, &[state.bump]]],
            std::cmp::min(
                reward.saturating_sub(slash),
                oracle_wsol_reward_escrow.amount,
            ),
        );
        [...]
    }
}
```

**Example 2: [H-01] `BlockBeforeSend` hook can be exploited to perform a denial of service** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md`
```go
poc: build
   	@echo "starting POC.."

   	# clear port 26657 if old process still running
   	@if lsof -i :26657; then \
   		kill -9 $$(lsof -t -i :26657) || echo "cannot kill process"; \
   	fi

   	# remove old setup and init new one
   	@rm -rf .mantrapoc
   	@mkdir -p .mantrapoc

   	./build/mantrachaind init poc-test --chain-id test-chain --home .mantrapoc
   	./build/mantrachaind keys add validator --keyring-backend test --home .mantrapoc
   	./build/mantrachaind keys add validator2 --keyring-backend test --home .mantrapoc

   	# create alice and bob account
   	./build/mantrachaind keys add alice --keyring-backend test --home .mantrapoc
   	./build/mantrachaind keys add bob --keyring-backend test --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show validator -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show validator2 -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show alice -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show bob -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc

   	./build/mantrachaind genesis gentx validator 100000000stake --chain-id test-chain --keyring-backend test --home .mantrapoc
   	# ./build/mantrachaind genesis gentx validator2 100000000stake --chain-id test-chain --keyring-backend test --home .mantrapoc

   	./build/mantrachaind genesis collect-gentxs --home .mantrapoc

   	# start node
   	./build/mantrachaind start --home .mantrapoc --minimum-gas-prices 0stake
```

**Example 3: [H-01] Lack of access control in `AgentNftV2::addValidator()` enables unauthoriz** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-lack-of-access-control-in-agentnftv2addvalidator-enables-unauthorized-valid.md`
```solidity
// AgentNftV2::mint()
    function mint(
        uint256 virtualId,
        address to,
        string memory newTokenURI,
        address payable theDAO,
        address founder,
        uint8[] memory coreTypes,
        address pool,
        address token
    ) external onlyRole(MINTER_ROLE) returns (uint256) {
        require(virtualId == _nextVirtualId, "Invalid virtualId");
        _nextVirtualId++;
        _mint(to, virtualId);
        _setTokenURI(virtualId, newTokenURI);
        VirtualInfo storage info = virtualInfos[virtualId];
        info.dao = theDAO;
        info.coreTypes = coreTypes;
        info.founder = founder;
        IERC5805 daoToken = GovernorVotes(theDAO).token();
        info.token = token;

VirtualLP storage lp = virtualLPs[virtualId];
        lp.pool = pool;
        lp.veToken = address(daoToken);

_stakingTokenToVirtualId[address(daoToken)] = virtualId;
@>        _addValidator(virtualId, founder);
@>        _initValidatorScore(virtualId, founder);
        return virtualId;
    }
    // AgentNftV2::addValidator()
    // Expected to be called by `AgentVeToken::stake()` function
    function addValidator(uint256 virtualId, address validator) public {
        if (isValidator(virtualId, validator)) {
// ... (truncated)
```

**Example 4: Lack of input validation** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/lack-of-input-validation.md`
```
// Vulnerable pattern from Across Token and Token Distributor Audit:
The codebase generally lacks sufficient input validation.


In the [`AcceleratingDistributor`](https://github.com/across-protocol/across-token/blob/42130387f81debf2a20d2f7b40d9f0ccc1dcd06a/contracts/AcceleratingDistributor.sol) contract, the [`enableStaking`](https://github.com/across-protocol/across-token/blob/42130387f81debf2a20d2f7b40d9f0ccc1dcd06a/contracts/AcceleratingDistributor.sol#L93) function allows the contract owner to configure several parameters associated with a `stakedToken`. Sev
```

**Example 5: Rewards distribution DoS due to uncached secondary asset classes** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/rewards-distribution-dos-due-to-uncached-secondary-asset-classes.md`
```solidity
function _calculateOperatorShare(uint48 epoch, address operator) internal {
  // code..

  uint96[] memory assetClasses = l1Middleware.getAssetClassIds();
  for (uint256 i = 0; i < assetClasses.length; i++) {
       uint256 totalStake = l1Middleware.totalStakeCache(epoch, assetClasses[i]); //@audit directly accesses totalStakeCache
  }
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in reward distribution dos logic allows exploitation through missing validation,
func secureRewardDistributionDos(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 3, MEDIUM: 2
- **Affected Protocols**: Virtuals Protocol, Switchboard On-chain, Suzaku Core, MANTRA, Across Token and Token Distributor Audit
- **Validation Strength**: Strong (3+ auditors)

---

## 3. Reward Missing Update

### Overview

Implementation flaw in reward missing update logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 10 audit reports with severity distribution: HIGH: 6, MEDIUM: 4.

> **Key Finding**: This bug report describes a problem in the code of a smart contract that could cause permanent corruption. The problem occurs when the oracle reports a decrease in the amount of rewards or penalties for a validator. This is not accounted for in the code, so the validator manager's accounting becomes

### Vulnerability Description

#### Root Cause

Implementation flaw in reward missing update logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies reward missing update in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to reward operations

### Vulnerable Pattern Examples

**Example 1: Any decrease in slashed or rewarded amounts reported will make validatorManager ** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/any-decrease-in-slashed-or-rewarded-amounts-reported-will-make-validatormanager-.md`
```solidity
// ValidatorManager.sol#L469-L503

/// @notice Report a reward event for a validator
/// @param validator Address of the validator to be rewarded
/// @param amount Amount of rewards for the validator
function reportRewardEvent(address validator, uint256 amount) external onlyRole(ORACLE_ROLE) validatorActive(validator) {
    require(amount > 0, "Invalid reward amount");
    // Update reward amounts
    totalRewards += amount; // @audit has to follow Oracle updates
    validatorRewards[validator] += amount;
    emit RewardEventReported(validator, amount);
}

/* ========== SLASHING ========== */

/// @notice Report a slashing event for a validator
/// @param validator Address of the validator to be slashed
/// @param amount Amount to slash from the validator
function reportSlashingEvent(address validator, uint256 amount) external onlyRole(ORACLE_ROLE) validatorActive(validator) {
    require(amount > 0, "Invalid slash amount");
    // Update slashing amounts
    totalSlashing += amount; // @audit has to follow Oracle updates
    validatorSlashing[validator] += amount;
    emit SlashingEventReported(validator, amount);
}
```

**Example 2: Future epoch cache manipulation via `calcAndCacheStakes` allows reward manipulat** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/future-epoch-cache-manipulation-via-calcandcachestakes-allows-reward-manipulatio.md`
```solidity
function calcAndCacheStakes(uint48 epoch, uint96 assetClassId) public returns (uint256 totalStake) {
    uint48 epochStartTs = getEpochStartTs(epoch); // No validation of epoch timing
    // ... rest of function caches values for any epoch, including future ones
}
```

**Example 3: [H-02] The reentrancy vulnerability in _safeMint can allow an attacker to steal ** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-02-the-reentrancy-vulnerability-in-_safemint-can-allow-an-attacker-to-steal-al.md`
```solidity
function _safeMint(
    address to,
    uint256 tokenId,
    bytes memory _data
) internal virtual {
    _mint(to, tokenId);
    require(
        _checkOnERC721Received(address(0), to, tokenId, _data),
        "ERC721: transfer to non ERC721Receiver implementer"
    );
}
...
function _checkOnERC721Received(
    address from,
    address to,
    uint256 tokenId,
    bytes memory _data
) private returns (bool) {
    if (to.isContract()) {
        try IERC721Receiver(to).onERC721Received(_msgSender(), from, tokenId, _data) returns (bytes4 retval) {
            return retval == IERC721Receiver.onERC721Received.selector;
```

**Example 4: Protocol won't be eligible for referral rewards for depositing ETH** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-2-protocol-wont-be-eligible-for-referral-rewards-for-depositing-eth.md`
```solidity
function _ethTOeEth(uint256 _amount) internal returns (uint256) {
        // deposit returns exact amount of eETH
        return IeETHLiquidityPool(eETHLiquidityPool).deposit{value: _amount}(address(this));
    }
```

**Example 5: [M-21] EIP1559 rewards received by syndicate during the period when it has no re** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-21-eip1559-rewards-received-by-syndicate-during-the-period-when-it-has-no-regi.md`
```solidity
function deRegisterKnotFromSyndicate(bytes[] calldata _blsPublicKeys) external onlyDAO {
        Syndicate(payable(syndicate)).deRegisterKnots(_blsPublicKeys);
    }
```

**Variant: Reward Missing Update - HIGH Severity Cases** [HIGH]
> Found in 6 reports:
> - `reports/cosmos_cometbft_findings/future-epoch-cache-manipulation-via-calcandcachestakes-allows-reward-manipulatio.md`
> - `reports/cosmos_cometbft_findings/h-02-the-reentrancy-vulnerability-in-_safemint-can-allow-an-attacker-to-steal-al.md`
> - `reports/cosmos_cometbft_findings/missing-balance-deduction-in-unstaking-functions-allows-contract-drainage-and-lo.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in reward missing update logic allows exploitation through missing validation, i
func secureRewardMissingUpdate(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 6, MEDIUM: 4
- **Affected Protocols**: Stakehouse Protocol, Staking, XDEFI, Geodefi, Kinetiq LST
- **Validation Strength**: Strong (3+ auditors)

---

## 4. Reward After Removal

### Overview

Implementation flaw in reward after removal logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 5 audit reports with severity distribution: HIGH: 1, MEDIUM: 4.

> **Key Finding**: A bug has been identified in the `deleteOperators` method, which is used when operators must be slashed. This bug leaves the `operatorRewards` mapping untouched when an operator is removed, meaning they can still claim their accrued rewards, even if they are acting maliciously or are inactive. This 

### Vulnerability Description

#### Root Cause

Implementation flaw in reward after removal logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies reward after removal in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to reward operations

### Vulnerable Pattern Examples

**Example 1: [C-02] Operator can still claim rewards after being removed from governance** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/c-02-operator-can-still-claim-rewards-after-being-removed-from-governance.md`
```
// Vulnerable pattern from Smoothly:
**Severity**

**Impact:**
High, as rewards shouldn't be claimable for operators that were removed from governance

**Likelihood:**
High, as this will happen every time this functionality is used and an operator has unclaimed rewards

**Description**

The `deleteOperators` method removes an operator account from the `PoolGovernance` but it still leaves the `operatorRewards` mapping untouched, meaning even if an operator is acting maliciously and is removed he can still claim his accrued rewards. 
```

**Example 2: [M-01] `returnFunds()` can be frontrun to profit from an increase in share price** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-01-returnfunds-can-be-frontrun-to-profit-from-an-increase-in-share-price.md`
```
// Vulnerable pattern from Increment:
**Severity**

**Impact:** High, an attacker can profit from the share price increase

**Likelihood:** Low, only profitable if a large amount of funds are returned

**Description**

`SafetyModule.returnFunds()` is used by governance to inject funds back into `StakedToken`, in the form of underlying tokens. For example, when there are excess funds raised from the auction, they can be returned back to compensate the stakers.

The issue is that anyone can frontrun `returnFunds()` with a `stake()` to
```

**Example 3: An earner can still continue earning even after being removed from the approved ** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-1-an-earner-can-still-continue-earning-even-after-being-removed-from-the-appro.md`
```solidity
function test_AliceStillEarnAfterDisapproved() external {

        _registrar.updateConfig(MAX_EARNER_RATE, 40000);
        _minterGateway.activateMinter(_minters[0]);

        uint256 collateral = 1_000_000e6;
        _updateCollateral(_minters[0], collateral);

        _mintM(_minters[0], 400e6, _bob);
        _mintM(_minters[0], 400e6, _alice);
        uint aliceInitialBalance = _mToken.balanceOf(_alice);
        uint bobInitialBalance = _mToken.balanceOf(_bob);
        //@audit-info alice and bob had the same M balance
        assertEq(aliceInitialBalance, bobInitialBalance);
        //@audit-info alice and bob started earning
        vm.prank(_alice);
        _mToken.startEarning();
        vm.prank(_bob);
        _mToken.startEarning();

        vm.warp(block.timestamp + 1 days);
        uint aliceEarningDay1 = _mToken.balanceOf(_alice) - aliceInitialBalance;
        uint bobEarningDay1 = _mToken.balanceOf(_bob) - bobInitialBalance;
        //@audit-info Alice and Bob have earned the same M in day 1
        assertNotEq(aliceEarningDay1, 0);
        assertEq(aliceEarningDay1, bobEarningDay1);
        //@audit-info Alice was removed from earner list
        _registrar.removeFromList(TTGRegistrarReader.EARNERS_LIST, _alice);
        vm.warp(block.timestamp + 1 days);
        uint aliceEarningDay2 = _mToken.balanceOf(_alice) - aliceInitialBalance - aliceEarningDay1;
        uint bobEarningDay2 = _mToken.balanceOf(_bob) - bobInitialBalance - bobEarningDay1;
        //@audit-info Alice still earned M in day 2 even she was removed from earner list, the amount of which is same as Bob's earning
        assertNotEq(aliceEarningDay2, 0);
        assertEq(aliceEarningDay2, bobEarningDay2);

// ... (truncated)
```

**Example 4: Stakers lose their commission if they unstake as they cannot claim their pending** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-8-stakers-lose-their-commission-if-they-unstake-as-they-cannot-claim-their-pen.md`
```
// Vulnerable pattern from MorphL2:
Source: https://github.com/sherlock-audit/2024-08-morphl2-judging/issues/168
```

**Example 5: Operators can lose their reward share** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/operators-can-lose-their-reward-share.md`
```solidity
function test_distributeRewards_removedOperator() public {
	uint48 epoch = 1;
	uint256 uptime = 4 hours;

	// Set up stakes for operators in epoch 1
	_setupStakes(epoch, uptime);

	// Get the list of operators
	address[] memory operators = middleware.getAllOperators();
	address removedOperator = operators[0]; // Operator to be removed
	address activeOperator = operators[1]; // Operator to remain active

	// Disable operator[0] at the start of epoch 2
	uint256 epoch2Start = middleware.getEpochStartTs(epoch + 1); // T = 8h
	vm.warp(epoch2Start);
	middleware.disableOperator(removedOperator);

	// Warp to after the slashing window to allow removal
	uint256 removalTime = epoch2Start + middleware.SLASHING_WINDOW(); // T = 13h (8h + 5h)
	vm.warp(removalTime);
	middleware.removeOperator(removedOperator);

	// Warp to epoch 4 to distribute rewards for epoch 1
	uint256 distributionTime = middleware.getEpochStartTs(epoch + 3); // T = 16h
	vm.warp(distributionTime);

	// Distribute rewards in batches
	uint256 batchSize = 3;
	uint256 remainingOperators = middleware.getAllOperators().length; // Now 9 operators
	while (remainingOperators > 0) {
		vm.prank(REWARDS_DISTRIBUTOR_ROLE);
		rewards.distributeRewards(epoch, uint48(batchSize));
		remainingOperators = remainingOperators > batchSize ? remainingOperators - batchSize : 0;
	}

// ... (truncated)
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in reward after removal logic allows exploitation through missing validation, in
func secureRewardAfterRemoval(ctx sdk.Context) error {
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
- **Affected Protocols**: MorphL2, Suzaku Core, Smoothly, Increment, M^ZERO
- **Validation Strength**: Strong (3+ auditors)

---

## 5. Reward Unclaimed Loss

### Overview

Implementation flaw in reward unclaimed loss logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 21 audit reports with severity distribution: HIGH: 7, MEDIUM: 14.

> **Key Finding**: This bug report describes an issue with the accounting system in a software program. The program is incorrectly counting certain funds twice, which can lead to incorrect calculations and potentially give users more money than they should have. This issue has been fixed by the developers, but it is i

### Vulnerability Description

#### Root Cause

Implementation flaw in reward unclaimed loss logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies reward unclaimed loss in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to reward operations

### Vulnerable Pattern Examples

**Example 1: Accounting for `rewardStakeRatioSum` is incorrect when a delayed balance or rewa** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/accounting-for-rewardstakeratiosum-is-incorrect-when-a-delayed-balance-or-reward.md`
```go
// Before start
latestActiveBalanceAfterFee = 32 ETH
latestActiveRewards = 0

// startReport()
reportSweptBalance = 0 (rewards is in BeaconChain)

// syncValidators()
reportActiveBalance = 32.105 ETH

// finalizeReport()
rewards = 0.105 ETH
change = rewards - latestActiveRewards = 0.105 ETH
gainAfterFee = 0.1 ETH
=> rewardStakeRatioSum is increased
=> latestActiveBalanceAfterFee = 32.1

sweptRewards = 0
=> latestActiveRewards = 0.105
```

**Example 2: [C-01] Incorrect reward calculation** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/c-01-incorrect-reward-calculation.md`
```solidity
File: NFTStaking.sol
82:     function unstakeNFTsRouter(address _sender, uint256[] calldata _tokenIds) external {
83:         require(msg.sender == stakingRouterAddress, "Only router");
84: 
85:@>       _unstakeNFTs(_sender, _tokenIds);
86:     }
...
88:     function claimRewards() public {
89:@>       _claimRewards(msg.sender);
90:     }
...
182:     function _unstakeNFTs(address _sender, uint256[] calldata _tokenIds) internal {
183:@>     claimRewards();
```

**Example 3: [C-02] Operator can still claim rewards after being removed from governance** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/c-02-operator-can-still-claim-rewards-after-being-removed-from-governance.md`
```
// Vulnerable pattern from Smoothly:
**Severity**

**Impact:**
High, as rewards shouldn't be claimable for operators that were removed from governance

**Likelihood:**
High, as this will happen every time this functionality is used and an operator has unclaimed rewards

**Description**

The `deleteOperators` method removes an operator account from the `PoolGovernance` but it still leaves the `operatorRewards` mapping untouched, meaning even if an operator is acting maliciously and is removed he can still claim his accrued rewards. 
```

**Example 4: Execution failure of `\_updateReward` function due to uninitialized `\_rewardDis** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/execution-failure-of-_updatereward-function-due-to-uninitialized-_rewarddistribu.md`
```solidity
function stake(address account, bytes32 method, uint256 amount) external {
        if (amount <= 0) {
            revert CustomErrors.ZeroStakeAmount();
        }

        // Calculate unclaimed reward before balance update
        _updateReward(account);
```

**Example 5: Fixed exchange rate at unstaking fails to socialize slashing and distorts reward** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/fixed-exchange-rate-at-unstaking-fails-to-socialize-slashing-and-distorts-reward.md`
```
// Vulnerable pattern from Mantle Network:
##### Description
When `Staking.unstakeRequest()` is called, the mETH/ETH rate is fixed and does not reflect slashing or rewards that may occur by the time `Staking.claimUnstakeRequest()` is executed. If two users create requests concurrently and losses arrive afterward, those losses are not socialized across them. One request may be fully paid while the other may revert on claim due to insufficient allocated funds.

This can be exacerbated by frontrunning updates to `LiquidityBuffer.cumulativeD
```

**Variant: Reward Unclaimed Loss - MEDIUM Severity Cases** [MEDIUM]
> Found in 14 reports:
> - `reports/cosmos_cometbft_findings/execution-failure-of-_updatereward-function-due-to-uninitialized-_rewarddistribu.md`
> - `reports/cosmos_cometbft_findings/execution-of-stake-and-unstake-operations-blocked-due-to-uninitialized-_methods-.md`
> - `reports/cosmos_cometbft_findings/fixed-exchange-rate-at-unstaking-fails-to-socialize-slashing-and-distorts-reward.md`

**Variant: Reward Unclaimed Loss in Qoda DAO** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/execution-failure-of-_updatereward-function-due-to-uninitialized-_rewarddistribu.md`
> - `reports/cosmos_cometbft_findings/execution-of-stake-and-unstake-operations-blocked-due-to-uninitialized-_methods-.md`

**Variant: Reward Unclaimed Loss in Stakehouse Protocol** [MEDIUM]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/m-18-node-runners-can-lose-all-their-stake-rewards-due-to-how-the-dao-commission.md`
> - `reports/cosmos_cometbft_findings/m-21-eip1559-rewards-received-by-syndicate-during-the-period-when-it-has-no-regi.md`
> - `reports/cosmos_cometbft_findings/m-28-funds-are-not-claimed-from-syndicate-for-valid-bls-keys-of-first-key-is-inv.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in reward unclaimed loss logic allows exploitation through missing validation, i
func secureRewardUnclaimedLoss(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 21 audit reports
- **Severity Distribution**: HIGH: 7, MEDIUM: 14
- **Affected Protocols**: Ajna Protocol, Stakehouse Protocol, ZetaChain Cross-Chain, Vault-Tec, Olas
- **Validation Strength**: Strong (3+ auditors)

---

## 6. Reward Distribution Unfair

### Overview

Implementation flaw in reward distribution unfair logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 19 audit reports with severity distribution: HIGH: 6, MEDIUM: 13.

> **Key Finding**: The `Staking.unstakeRequest()` function is causing issues with the mETH/ETH rate being fixed and not reflecting any losses or rewards that may occur while waiting for `Staking.claimUnstakeRequest()` to be executed. This can result in unequal distribution of losses and rewards among users who submit 

### Vulnerability Description

#### Root Cause

Implementation flaw in reward distribution unfair logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies reward distribution unfair in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to reward operations

### Vulnerable Pattern Examples

**Example 1: Fixed exchange rate at unstaking fails to socialize slashing and distorts reward** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/fixed-exchange-rate-at-unstaking-fails-to-socialize-slashing-and-distorts-reward.md`
```
// Vulnerable pattern from Mantle Network:
##### Description
When `Staking.unstakeRequest()` is called, the mETH/ETH rate is fixed and does not reflect slashing or rewards that may occur by the time `Staking.claimUnstakeRequest()` is executed. If two users create requests concurrently and losses arrive afterward, those losses are not socialized across them. One request may be fully paid while the other may revert on claim due to insufficient allocated funds.

This can be exacerbated by frontrunning updates to `LiquidityBuffer.cumulativeD
```

**Example 2: Funds Allocated for Rewards Can Be Locked in the Contract** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/funds-allocated-for-rewards-can-be-locked-in-the-contract.md`
```go
uint256 slashed = (sub.rewardPoints * bps) / _MAX_BIPS; <=== rewardPoints can be greater than 0 but if bps is not big enough, slashed will be 0. 

uint256 slashedValue = (sub.rewardsWithdrawn * bps) / _MAX_BIPS; <=== another instance where `rewardsWithdrawn` might also be a positive value but not large enough, this can result in a 0 value.
```

**Example 3: [H-02] Invalid validation in `_farmPlots` function allowing a malicious user rep** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-02-invalid-validation-in-_farmplots-function-allowing-a-malicious-user-repeate.md`
```go
if (_getNumPlots(landlord) < _toiler.plotId) {
                timestamp = plotMetadata[landlord].lastUpdated;
                toilerState[tokenId].dirty = true;
            }
```

**Example 4: [H-03] Node operator is getting slashed for full duration even though rewards ar** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-03-node-operator-is-getting-slashed-for-full-duration-even-though-rewards-are-.md`
```solidity
File: MinipoolManager.sol

557:	function getExpectedAVAXRewardsAmt(uint256 duration, uint256 avaxAmt) public view returns (uint256) {
558:		ProtocolDAO dao = ProtocolDAO(getContractAddress("ProtocolDAO"));
559:		uint256 rate = dao.getExpectedAVAXRewardsRate();
560:		return (avaxAmt.mulWadDown(rate) * duration) / 365 days; // full duration used when calculating expected reward
561:	}

...

670:	function slash(int256 index) private {

...

673:		uint256 duration = getUint(keccak256(abi.encodePacked("minipool.item", index, ".duration")));
674:		uint256 avaxLiquidStakerAmt = getUint(keccak256(abi.encodePacked("minipool.item", index, ".avaxLiquidStakerAmt")));
675:		uint256 expectedAVAXRewardsAmt = getExpectedAVAXRewardsAmt(duration, avaxLiquidStakerAmt); // full duration
676:		uint256 slashGGPAmt = calculateGGPSlashAmt(expectedAVAXRewardsAmt);
```

**Example 5: [H-05] `ValidatorRegistry::validatorScore/getPastValidatorScore` allows validato** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-05-validatorregistryvalidatorscoregetpastvalidatorscore-allows-validator-to-ea.md`
```solidity
function _initValidatorScore(
    uint256 virtualId,
    address validator
) internal {
    _baseValidatorScore[validator][virtualId] = _getMaxScore(virtualId);
}
```

**Variant: Reward Distribution Unfair - HIGH Severity Cases** [HIGH]
> Found in 6 reports:
> - `reports/cosmos_cometbft_findings/funds-allocated-for-rewards-can-be-locked-in-the-contract.md`
> - `reports/cosmos_cometbft_findings/h-02-invalid-validation-in-_farmplots-function-allowing-a-malicious-user-repeate.md`
> - `reports/cosmos_cometbft_findings/h-03-node-operator-is-getting-slashed-for-full-duration-even-though-rewards-are-.md`

**Variant: Reward Distribution Unfair in Munchables** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h-02-invalid-validation-in-_farmplots-function-allowing-a-malicious-user-repeate.md`
> - `reports/cosmos_cometbft_findings/h-05-failure-to-update-dirty-flag-in-transfertounoccupiedplot-prevents-reward-ac.md`

**Variant: Reward Distribution Unfair in Virtuals Protocol** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h-05-validatorregistryvalidatorscoregetpastvalidatorscore-allows-validator-to-ea.md`
> - `reports/cosmos_cometbft_findings/m-04-launched-tokens-are-vulnerable-to-flashloan-attacks-forcing-premature-gradu.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in reward distribution unfair logic allows exploitation through missing validati
func secureRewardDistributionUnfair(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 19 audit reports
- **Severity Distribution**: HIGH: 6, MEDIUM: 13
- **Affected Protocols**: GoGoPool, Virtuals Protocol, Munchables, MagicSea - the native DEX on the IotaEVM, Stakehouse Protocol
- **Validation Strength**: Strong (3+ auditors)

---

## 7. Reward Epoch Timing

### Overview

Implementation flaw in reward epoch timing logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 15 audit reports with severity distribution: HIGH: 6, MEDIUM: 9.

> **Key Finding**: This bug report discusses an issue with the Berachef.sol#158 code, where a validator operator can queue a new cutting board at any time and activate it after a certain delay. However, this system can be manipulated by a malicious validator by publicly queueing a cutting board to attract BGT stakes f

### Vulnerability Description

#### Root Cause

Implementation flaw in reward epoch timing logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies reward epoch timing in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to reward operations

### Vulnerable Pattern Examples

**Example 1: Activation of queued cutting board can be manipulated leading to redirection of ** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/activation-of-queued-cutting-board-can-be-manipulated-leading-to-redirection-of-.md`
```
// Vulnerable pattern from Berachain Pol:
Severity: Medium Risk
Context: Berachef.sol#158
Description: A validator operator can queue a new cutting board at any time. Once thecuttingBoardBlockDelay
has passed, the queued cutting board is ready for activation. The activation of a cutting board occurs viadistrib-
utor.distributeFor() which calls beraChef.activateReadyQueuedCuttingBoard(pubkey, blockNumber); .
The validator is incentivized to emit the BGT reward to reward vaults that will provide the best financial incentives
while also in
```

**Example 2: Flawed Implementation of Reward Score Calculation** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/flawed-implementation-of-reward-score-calculation.md`
```rust
pub fn calculate_slash(stats: &OracleStatsAccountData, reward: u64) -> u64 {
    let slash_score = stats.finalized_epoch.slash_score;
    if slash_score == 0 {
        return 0;
    }
    let reward_score = stats.finalized_epoch.reward_score;
    Decimal::from(reward)
        .saturating_mul(reward_score.into())
        .checked_div(slash_score.into())
        .unwrap()
        .to_u64()
        .unwrap_or(0)
}
```

**Example 3: Future epoch cache manipulation via `calcAndCacheStakes` allows reward manipulat** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/future-epoch-cache-manipulation-via-calcandcachestakes-allows-reward-manipulatio.md`
```solidity
function calcAndCacheStakes(uint48 epoch, uint96 assetClassId) public returns (uint256 totalStake) {
    uint48 epochStartTs = getEpochStartTs(epoch); // No validation of epoch timing
    // ... rest of function caches values for any epoch, including future ones
}
```

**Example 4: [H-03] Incorrect boost management leads to staking reward loss** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-03-incorrect-boost-management-leads-to-staking-reward-loss.md`
```solidity
function queueDropBoost(bytes calldata pubkey, uint128 amount) external {
@>      QueuedDropBoost storage qdb = dropBoostQueue[msg.sender][pubkey];
        uint128 dropBalance = qdb.balance + amount;
        // check if the user has enough boosted balance to drop
        if (boosted[msg.sender][pubkey] < dropBalance) NotEnoughBoostedBalance.selector.revertWith();
@>      (qdb.balance, qdb.blockNumberLast) = (dropBalance, uint32(block.number));
        emit QueueDropBoost(msg.sender, pubkey, amount);
    }
```

**Example 5: [H-10] missing `isEpochClaimed` validation** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-10-missing-isepochclaimed-validation.md`
```
// Vulnerable pattern from Ajna Protocol:
User can claim rewards even when is already claimed

### Proof of Concept

The \_claimRewards function is using to calculate and send the reward to the caller but this function is no validating if isEpochClaimed mapping is true due that in claimRewards function is validated, see the stament in the following lines:

    file: ajna-core/src/RewardsManager.sol
    function claimRewards(
            uint256 tokenId_,
            uint256 epochToClaim_ 
        ) external override {
            StakeI
```

**Variant: Reward Epoch Timing - HIGH Severity Cases** [HIGH]
> Found in 6 reports:
> - `reports/cosmos_cometbft_findings/flawed-implementation-of-reward-score-calculation.md`
> - `reports/cosmos_cometbft_findings/future-epoch-cache-manipulation-via-calcandcachestakes-allows-reward-manipulatio.md`
> - `reports/cosmos_cometbft_findings/h-03-incorrect-boost-management-leads-to-staking-reward-loss.md`

**Variant: Reward Epoch Timing in Suzaku Core** [HIGH]
> Protocol-specific variant found in 6 reports:
> - `reports/cosmos_cometbft_findings/future-epoch-cache-manipulation-via-calcandcachestakes-allows-reward-manipulatio.md`
> - `reports/cosmos_cometbft_findings/immediate-stake-cache-updates-enable-reward-distribution-without-p-chain-confirm.md`
> - `reports/cosmos_cometbft_findings/operator-can-over-allocate-the-same-stake-to-unlimited-nodes-within-one-epoch-ca.md`

**Variant: Reward Epoch Timing in Ajna Protocol** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h-10-missing-isepochclaimed-validation.md`
> - `reports/cosmos_cometbft_findings/m-10-unsafe-casting-from-uint256-to-uint128-in-rewardsmanager.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in reward epoch timing logic allows exploitation through missing validation, inc
func secureRewardEpochTiming(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 15 audit reports
- **Severity Distribution**: HIGH: 6, MEDIUM: 9
- **Affected Protocols**: Maia DAO Ecosystem, Ajna Protocol, Switchboard On-chain, Berachain Pol, Olas
- **Validation Strength**: Strong (3+ auditors)

---

## Detection Patterns

### Automated Detection
```
# Reward Stuck Locked
grep -rn 'reward|stuck|locked' --include='*.go' --include='*.sol'
# Reward Distribution Dos
grep -rn 'reward|distribution|dos' --include='*.go' --include='*.sol'
# Reward Missing Update
grep -rn 'reward|missing|update' --include='*.go' --include='*.sol'
# Reward After Removal
grep -rn 'reward|after|removal' --include='*.go' --include='*.sol'
# Reward Unclaimed Loss
grep -rn 'reward|unclaimed|loss' --include='*.go' --include='*.sol'
# Reward Distribution Unfair
grep -rn 'reward|distribution|unfair' --include='*.go' --include='*.sol'
# Reward Epoch Timing
grep -rn 'reward|epoch|timing' --include='*.go' --include='*.sol'
```

## Keywords

`access`, `accounting`, `activation`, `after`, `allocated`, `allow`, `allowing`, `allows`, `amounts`, `appchain`, `approved`, `assignment`, `attacker`, `balance`, `being`, `board`, `cache`, `calculation`, `causes`, `claim`, `continue`, `contract`, `control`, `cosmos`, `cutting`, `decrease`, `delayed`, `denial`, `distorts`, `distribution`

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

`_calculateOperatorShare`, `_checkOnERC721Received`, `_ethTOeEth`, `_initValidatorScore`, `_safeMint`, `_unstakeNFTs`, `addValidator`, `after_removal`, `appchain`, `balanceOf`, `block.number`, `block.timestamp`, `calcAndCacheStakes`, `claimRewards`, `cosmos`, `deRegisterKnotFromSyndicate`, `defi`, `deposit`, `distribution_dos`, `distribution_unfair`, `epoch_timing`, `for`, `getExpectedAVAXRewardsAmt`, `missing_update`, `reward_distribution_failures`, `rewards`, `staking`, `stuck_locked`, `unclaimed_loss`
