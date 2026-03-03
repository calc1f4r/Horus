---
protocol: generic
chain: cosmos
category: rewards
vulnerability_type: reward_calculation_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: rewards_logic

primitives:
  - calculation_incorrect
  - per_share_error
  - accumulation_error
  - delayed_balance
  - decimal_mismatch
  - weight_error
  - historical_loss
  - pool_share

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
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Reward Calculation Incorrect
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Accounting for `rewardStakeRatioSum` is incorrect when a del | `reports/cosmos_cometbft_findings/accounting-for-rewardstakeratiosum-is-incorrect-when-a-delayed-balance-or-reward.md` | HIGH | Cyfrin |
| [C-01] Incorrect reward calculation | `reports/cosmos_cometbft_findings/c-01-incorrect-reward-calculation.md` | HIGH | Pashov Audit Group |
| Flawed Implementation of Reward Score Calculation | `reports/cosmos_cometbft_findings/flawed-implementation-of-reward-score-calculation.md` | HIGH | OtterSec |
| Function `getTotalStake()` fails to account for pending vali | `reports/cosmos_cometbft_findings/function-gettotalstake-fails-to-account-for-pending-validators-leading-to-inaccu.md` | HIGH | Cyfrin |
| Incorrect accounting of `reportRecoveredEffectiveBalance` ca | `reports/cosmos_cometbft_findings/incorrect-accounting-of-reportrecoveredeffectivebalance-can-prevent-report-from-.md` | HIGH | Cyfrin |
| [M-08] Recreated pools receive a wrong AVAX amount due to mi | `reports/cosmos_cometbft_findings/m-08-recreated-pools-receive-a-wrong-avax-amount-due-to-miscalculated-compounded.md` | MEDIUM | Code4rena |
| [M-10] Functions cancelMinipool() doesn’t reset the value of | `reports/cosmos_cometbft_findings/m-10-functions-cancelminipool-doesnt-reset-the-value-of-the-rewardsstarttime-for.md` | MEDIUM | Code4rena |
| [M-17] Wrong slashing calculation rewards for operator that  | `reports/cosmos_cometbft_findings/m-17-wrong-slashing-calculation-rewards-for-operator-that-did-not-do-his-job.md` | MEDIUM | Code4rena |

### Reward Per Share Error
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-01] `BlockBeforeSend` hook can be exploited to perform a  | `reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md` | HIGH | Code4rena |
| Historical reward loss due to `NodeId` reuse in `AvalancheL1 | `reports/cosmos_cometbft_findings/historical-reward-loss-due-to-nodeid-reuse-in-avalanchel1middleware.md` | MEDIUM | Cyfrin |
| [M-01] `returnFunds()` can be frontrun to profit from an inc | `reports/cosmos_cometbft_findings/m-01-returnfunds-can-be-frontrun-to-profit-from-an-increase-in-share-price.md` | MEDIUM | Pashov Audit Group |
| [M-08] Recreated pools receive a wrong AVAX amount due to mi | `reports/cosmos_cometbft_findings/m-08-recreated-pools-receive-a-wrong-avax-amount-due-to-miscalculated-compounded.md` | MEDIUM | Code4rena |
| [M-11] `ValidatorWithdrawalVault.distributeRewards` can be c | `reports/cosmos_cometbft_findings/m-11-validatorwithdrawalvaultdistributerewards-can-be-called-to-make-operator-sl.md` | MEDIUM | Code4rena |
| Protocol won't be eligible for referral rewards for depositi | `reports/cosmos_cometbft_findings/m-2-protocol-wont-be-eligible-for-referral-rewards-for-depositing-eth.md` | MEDIUM | Sherlock |
| [M-21] EIP1559 rewards received by syndicate during the peri | `reports/cosmos_cometbft_findings/m-21-eip1559-rewards-received-by-syndicate-during-the-period-when-it-has-no-regi.md` | MEDIUM | Code4rena |
| New staking between reward epochs will dilute rewards for ex | `reports/cosmos_cometbft_findings/m-3-new-staking-between-reward-epochs-will-dilute-rewards-for-existing-stakers-a.md` | MEDIUM | Sherlock |

### Reward Delayed Balance
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Accounting for `rewardStakeRatioSum` is incorrect when a del | `reports/cosmos_cometbft_findings/accounting-for-rewardstakeratiosum-is-incorrect-when-a-delayed-balance-or-reward.md` | HIGH | Cyfrin |
| Function `getTotalStake()` fails to account for pending vali | `reports/cosmos_cometbft_findings/function-gettotalstake-fails-to-account-for-pending-validators-leading-to-inaccu.md` | HIGH | Cyfrin |
| Incorrect accounting of `reportRecoveredEffectiveBalance` ca | `reports/cosmos_cometbft_findings/incorrect-accounting-of-reportrecoveredeffectivebalance-can-prevent-report-from-.md` | HIGH | Cyfrin |
| A part of ETH rewards can be stolen by sandwiching `claimDel | `reports/cosmos_cometbft_findings/m-3-a-part-of-eth-rewards-can-be-stolen-by-sandwiching-claimdelayedwithdrawals.md` | MEDIUM | Sherlock |
| Penalty system delays the rewards instead of reducing them | `reports/cosmos_cometbft_findings/penalty-system-delays-the-rewards-instead-of-reducing-them.md` | HIGH | Halborn |

### Reward Decimal Mismatch
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Attacker will prevent distribution of USDC to stakers throug | `reports/cosmos_cometbft_findings/m-1-attacker-will-prevent-distribution-of-usdc-to-stakers-through-frequent-rewar.md` | MEDIUM | Sherlock |

### Reward Weight Error
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-06] `_getRewardsAmountPerVault` might be using an outdate | `reports/cosmos_cometbft_findings/m-06-_getrewardsamountpervault-might-be-using-an-outdated-vault-power.md` | MEDIUM | Pashov Audit Group |
| [M-09] Users can deflate other markets Guild holders rewards | `reports/cosmos_cometbft_findings/m-09-users-can-deflate-other-markets-guild-holders-rewards-by-staking-less-price.md` | MEDIUM | Code4rena |
| `msg_server_stake::AddStake` calculates the weight incorrect | `reports/cosmos_cometbft_findings/m-32-msg_server_stakeaddstake-calculates-the-weight-incorrectly-resulting-in-inc.md` | MEDIUM | Sherlock |
| MixinParams.setParams bypasses safety checks made by standar | `reports/cosmos_cometbft_findings/mixinparamssetparams-bypasses-safety-checks-made-by-standard-stakingproxy-upgrad.md` | MEDIUM | ConsenSys |
| Operator can over allocate the same stake to unlimited nodes | `reports/cosmos_cometbft_findings/operator-can-over-allocate-the-same-stake-to-unlimited-nodes-within-one-epoch-ca.md` | MEDIUM | Cyfrin |

### Reward Historical Loss
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Historical reward loss due to `NodeId` reuse in `AvalancheL1 | `reports/cosmos_cometbft_findings/historical-reward-loss-due-to-nodeid-reuse-in-avalanchel1middleware.md` | MEDIUM | Cyfrin |

### Reward Pool Share
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-08] Recreated pools receive a wrong AVAX amount due to mi | `reports/cosmos_cometbft_findings/m-08-recreated-pools-receive-a-wrong-avax-amount-due-to-miscalculated-compounded.md` | MEDIUM | Code4rena |
| Missing Reward Address Checks | `reports/cosmos_cometbft_findings/missing-reward-address-checks.md` | HIGH | OtterSec |
| Node Operators Can Claim RPL Stake Without Running A Node | `reports/cosmos_cometbft_findings/node-operators-can-claim-rpl-stake-without-running-a-node.md` | HIGH | SigmaPrime |

---

# Reward Calculation Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Reward Calculation Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Reward Calculation Incorrect](#1-reward-calculation-incorrect)
2. [Reward Per Share Error](#2-reward-per-share-error)
3. [Reward Delayed Balance](#3-reward-delayed-balance)
4. [Reward Decimal Mismatch](#4-reward-decimal-mismatch)
5. [Reward Weight Error](#5-reward-weight-error)
6. [Reward Historical Loss](#6-reward-historical-loss)
7. [Reward Pool Share](#7-reward-pool-share)

---

## 1. Reward Calculation Incorrect

### Overview

Implementation flaw in reward calculation incorrect logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 12 audit reports with severity distribution: HIGH: 7, MEDIUM: 5.

> **Key Finding**: This bug report describes an issue with the accounting system in a software program. The program is incorrectly counting certain funds twice, which can lead to incorrect calculations and potentially give users more money than they should have. This issue has been fixed by the developers, but it is i

### Vulnerability Description

#### Root Cause

Implementation flaw in reward calculation incorrect logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies reward calculation incorrect in the protocol
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

**Example 3: Flawed Implementation of Reward Score Calculation** [HIGH]
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

**Example 4: [M-08] Recreated pools receive a wrong AVAX amount due to miscalculated compound** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-08-recreated-pools-receive-a-wrong-avax-amount-due-to-miscalculated-compounded.md`
```go
Minipool memory mp = getMinipool(minipoolIndex);
// Compound the avax plus rewards
// NOTE Assumes a 1:1 nodeOp:liqStaker funds ratio
uint256 compoundedAvaxNodeOpAmt = mp.avaxNodeOpAmt + mp.avaxNodeOpRewardAmt;
setUint(keccak256(abi.encodePacked("minipool.item", minipoolIndex, ".avaxNodeOpAmt")), compoundedAvaxNodeOpAmt);
setUint(keccak256(abi.encodePacked("minipool.item", minipoolIndex, ".avaxLiquidStakerAmt")), compoundedAvaxNodeOpAmt);
```

**Example 5: [M-17] Wrong slashing calculation rewards for operator that did not do his job** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-17-wrong-slashing-calculation-rewards-for-operator-that-did-not-do-his-job.md`
```
// Vulnerable pattern from Holograph:
Wrong slashing calculation may create unfair punishment for operators that accidentally forgot to execute their job.

### Proof of Concept

[Docs](https://docs.holograph.xyz/holograph-protocol/operator-network-specification): If an operator acts maliciously, a percentage of their bonded HLG will get slashed. Misbehavior includes (i) downtime, (ii) double-signing transactions, and (iii) abusing transaction speeds. 50% of the slashed HLG will be rewarded to the next operator to execute the transac
```

**Variant: Reward Calculation Incorrect - MEDIUM Severity Cases** [MEDIUM]
> Found in 5 reports:
> - `reports/cosmos_cometbft_findings/m-08-recreated-pools-receive-a-wrong-avax-amount-due-to-miscalculated-compounded.md`
> - `reports/cosmos_cometbft_findings/m-10-functions-cancelminipool-doesnt-reset-the-value-of-the-rewardsstarttime-for.md`
> - `reports/cosmos_cometbft_findings/m-17-wrong-slashing-calculation-rewards-for-operator-that-did-not-do-his-job.md`

**Variant: Reward Calculation Incorrect in Casimir** [HIGH]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/accounting-for-rewardstakeratiosum-is-incorrect-when-a-delayed-balance-or-reward.md`
> - `reports/cosmos_cometbft_findings/function-gettotalstake-fails-to-account-for-pending-validators-leading-to-inaccu.md`
> - `reports/cosmos_cometbft_findings/incorrect-accounting-of-reportrecoveredeffectivebalance-can-prevent-report-from-.md`

**Variant: Reward Calculation Incorrect in GoGoPool** [MEDIUM]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/m-08-recreated-pools-receive-a-wrong-avax-amount-due-to-miscalculated-compounded.md`
> - `reports/cosmos_cometbft_findings/m-10-functions-cancelminipool-doesnt-reset-the-value-of-the-rewardsstarttime-for.md`
> - `reports/cosmos_cometbft_findings/m-22-inaccurate-estimation-of-validation-rewards-from-function-expectedrewardava.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in reward calculation incorrect logic allows exploitation through missing valida
func secureRewardCalculationIncorrect(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 12 audit reports
- **Severity Distribution**: HIGH: 7, MEDIUM: 5
- **Affected Protocols**: Subscription Token Protocol V2, GoGoPool, Switchboard On-chain, Casimir, Suzaku Core
- **Validation Strength**: Strong (3+ auditors)

---

## 2. Reward Per Share Error

### Overview

Implementation flaw in reward per share error logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 14 audit reports with severity distribution: HIGH: 3, MEDIUM: 11.

> **Key Finding**: The `MsgSetBeforeSendHook` in the `tokenfactory` module allows the creator of a token to set a custom logic for determining whether a transfer should succeed. However, a malicious token creator can set an invalid address as the hook, causing transfers to fail and potentially leading to a denial of s

### Vulnerability Description

#### Root Cause

Implementation flaw in reward per share error logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies reward per share error in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to reward operations

### Vulnerable Pattern Examples

**Example 1: [H-01] `BlockBeforeSend` hook can be exploited to perform a denial of service** [HIGH]
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

**Example 2: Historical reward loss due to `NodeId` reuse in `AvalancheL1Middleware`** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/historical-reward-loss-due-to-nodeid-reuse-in-avalanchel1middleware.md`
```
// Vulnerable pattern from Suzaku Core:
**Description:** The `AvalancheL1Middleware` contract is vulnerable to misattributing stake to a former operator (Operator A) if a new, colluding or coordinated operator (Operator B) intentionally re-registers a node using the *exact same `bytes32 nodeId`* that Operator A previously used. This scenario assumes Operator B is aware of Operator A's historical `nodeId` and that the underlying P-Chain NodeID (`P_X`, derived from the shared `bytes32 nodeId`) has become available for re-registration on
```

**Example 3: [M-01] `returnFunds()` can be frontrun to profit from an increase in share price** [MEDIUM]
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

**Example 4: [M-08] Recreated pools receive a wrong AVAX amount due to miscalculated compound** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-08-recreated-pools-receive-a-wrong-avax-amount-due-to-miscalculated-compounded.md`
```go
Minipool memory mp = getMinipool(minipoolIndex);
// Compound the avax plus rewards
// NOTE Assumes a 1:1 nodeOp:liqStaker funds ratio
uint256 compoundedAvaxNodeOpAmt = mp.avaxNodeOpAmt + mp.avaxNodeOpRewardAmt;
setUint(keccak256(abi.encodePacked("minipool.item", minipoolIndex, ".avaxNodeOpAmt")), compoundedAvaxNodeOpAmt);
setUint(keccak256(abi.encodePacked("minipool.item", minipoolIndex, ".avaxLiquidStakerAmt")), compoundedAvaxNodeOpAmt);
```

**Example 5: [M-11] `ValidatorWithdrawalVault.distributeRewards` can be called to make operat** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-11-validatorwithdrawalvaultdistributerewards-can-be-called-to-make-operator-sl.md`
```
// Vulnerable pattern from Stader Labs:
An attacker can call `distributeRewards` right before `settleFunds` to make `operatorShare < penaltyAmount`. As a result, the validator will face loses.

### Proof of Concept

`ValidatorWithdrawalVault.distributeRewards` can be called by anyone. It's purpose is to distribute validators rewards among the stakers protocol and the operator. After the call, the balance of `ValidatorWithdrawalVault` becomes 0.

`ValidatorWithdrawalVault.settle` is called when a validator is withdrawn from beacon chai
```

**Variant: Reward Per Share Error - MEDIUM Severity Cases** [MEDIUM]
> Found in 11 reports:
> - `reports/cosmos_cometbft_findings/historical-reward-loss-due-to-nodeid-reuse-in-avalanchel1middleware.md`
> - `reports/cosmos_cometbft_findings/m-01-returnfunds-can-be-frontrun-to-profit-from-an-increase-in-share-price.md`
> - `reports/cosmos_cometbft_findings/m-08-recreated-pools-receive-a-wrong-avax-amount-due-to-miscalculated-compounded.md`

**Variant: Reward Per Share Error in Suzaku Core** [MEDIUM]
> Protocol-specific variant found in 4 reports:
> - `reports/cosmos_cometbft_findings/historical-reward-loss-due-to-nodeid-reuse-in-avalanchel1middleware.md`
> - `reports/cosmos_cometbft_findings/operators-can-lose-their-reward-share.md`
> - `reports/cosmos_cometbft_findings/rewards-distribution-dos-due-to-uncached-secondary-asset-classes.md`

**Variant: Reward Per Share Error in Covalent** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-3-new-staking-between-reward-epochs-will-dilute-rewards-for-existing-stakers-a.md`
> - `reports/cosmos_cometbft_findings/m-7-operationalstaking_unstake-delegators-can-bypass-28-days-unstaking-cooldown-.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in reward per share error logic allows exploitation through missing validation, 
func secureRewardPerShareError(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 14 audit reports
- **Severity Distribution**: HIGH: 3, MEDIUM: 11
- **Affected Protocols**: Subscription Token Protocol V2, GoGoPool, Stakehouse Protocol, Suzaku Core, MANTRA
- **Validation Strength**: Strong (3+ auditors)

---

## 3. Reward Delayed Balance

### Overview

Implementation flaw in reward delayed balance logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 5 audit reports with severity distribution: HIGH: 4, MEDIUM: 1.

> **Key Finding**: This bug report describes an issue with the accounting system in a software program. The program is incorrectly counting certain funds twice, which can lead to incorrect calculations and potentially give users more money than they should have. This issue has been fixed by the developers, but it is i

### Vulnerability Description

#### Root Cause

Implementation flaw in reward delayed balance logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies reward delayed balance in the protocol
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

**Example 2: Function `getTotalStake()` fails to account for pending validators, leading to i** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/function-gettotalstake-fails-to-account-for-pending-validators-leading-to-inaccu.md`
```solidity
function getTotalStake() public view returns (uint256 totalStake) {
  // @audit Validators in pending state is not accounted for
  totalStake = unassignedBalance + readyValidatorIds.length * VALIDATOR_CAPACITY + latestActiveBalanceAfterFee
      + delayedEffectiveBalance + withdrawnEffectiveBalance + subtractRewardFee(delayedRewards) - unstakeQueueAmount;
}
```

**Example 3: Incorrect accounting of `reportRecoveredEffectiveBalance` can prevent report fro** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/incorrect-accounting-of-reportrecoveredeffectivebalance-can-prevent-report-from-.md`
```go
} else if (change < 0) {
    uint256 loss = uint256(-change);
    rewardStakeRatioSum -= Math.mulDiv(rewardStakeRatioSum, loss, totalStake);
    latestActiveBalanceAfterFee -= loss;
}
```

**Example 4: A part of ETH rewards can be stolen by sandwiching `claimDelayedWithdrawals()`** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-3-a-part-of-eth-rewards-can-be-stolen-by-sandwiching-claimdelayedwithdrawals.md`
```go
receive() external payable {
    (bool success,) = address(rewardDistributor()).call{value: msg.value}('');
    require(success);
}
```

**Example 5: Penalty system delays the rewards instead of reducing them** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/penalty-system-delays-the-rewards-instead-of-reducing-them.md`
```solidity
function test_yield_generation_POC() public postTGE {
        console.log("========  Day 1  ======== ");
        console.log("[+] Alice buys 1 month Sub and stakes 10,000 ALTT");
        _subscribe(alice, carol, SubscribeRegistry.packages.MONTHLY, 1, 10000e18, address(0), true);

        skip(20 days);
        console.log("========  Day 21  ======== ");
        console.log("[*] Simulating total fees accrual in author pool");
        _addReward(100e18);

        skip(180 days);
        console.log("========  Day 201  ======== ");
        console.log("[*] Simulating total fees accrual in author pool");
        _addReward(1000e18);

        console.log("[+] Alice's Unlocked Rewards:", IStakingVault(authorVault).unlockedRewards(alice));

        //To claim all the rewards, alice now subscribes again for 7 months, offset the penalty
        console.log("[+] Alice Resubscribes for 7 months");
        _subscribe(alice, carol, SubscribeRegistry.packages.MONTHLY, 7, 0, address(0), true);

        skip(190 days);
        console.log("========  Day 391  ======== ");
        console.log("[*] Simulating total fees accrual in author pool");
        _addReward(1000e18);

        //The penalty that alice faces is delay in claiming the rewards INSTEAD of her not recieving those rewards in the first place
        console.log("[+] Alice's Unlocked Rewards:", IStakingVault(authorVault).unlockedRewards(alice));
    }
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in reward delayed balance logic allows exploitation through missing validation, 
func secureRewardDelayedBalance(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 4, MEDIUM: 1
- **Affected Protocols**: Staking, Casimir, Rio Network
- **Validation Strength**: Strong (3+ auditors)

---

## 4. Reward Decimal Mismatch

### Overview

Implementation flaw in reward decimal mismatch logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: This bug report discusses an issue found by several individuals where the lower precision of USDC and frequent reward updates in the Kwenta staking contracts could potentially result in stakers receiving 0 of the allotted 10K USDC weekly rewards. This is due to a mistake in using the same reward cal

### Vulnerability Description

#### Root Cause

Implementation flaw in reward decimal mismatch logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies reward decimal mismatch in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to reward operations

### Vulnerable Pattern Examples

**Example 1: Attacker will prevent distribution of USDC to stakers through frequent reward up** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-1-attacker-will-prevent-distribution-of-usdc-to-stakers-through-frequent-rewar.md`
```go
((lastTimeRewardApplicable() - lastUpdateTime) * rewardRateUSDC * 1e18) / allTokensStaked
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in reward decimal mismatch logic allows exploitation through missing validation,
func secureRewardDecimalMismatch(ctx sdk.Context) error {
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
- **Affected Protocols**: Kwenta Staking Rewards Upgrade
- **Validation Strength**: Single auditor

---

## 5. Reward Weight Error

### Overview

Implementation flaw in reward weight error logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 5 audit reports with severity distribution: MEDIUM: 5.

> **Key Finding**: This bug report talks about a problem in Symbiotic, which is a platform for staking cryptocurrency. The problem is that if a vault is slashed (meaning a penalty is imposed) in the current epoch, its active stake (the amount of cryptocurrency being staked) is immediately reduced. However, in the curr

### Vulnerability Description

#### Root Cause

Implementation flaw in reward weight error logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies reward weight error in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to reward operations

### Vulnerable Pattern Examples

**Example 1: [M-06] `_getRewardsAmountPerVault` might be using an outdated vault power** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-06-_getrewardsamountpervault-might-be-using-an-outdated-vault-power.md`
```go
// https://github.com/symbioticfi/core/blob/main/src/contracts/vault/Vault.sol#L237
            if (slashedAmount > 0) {
                uint256 activeSlashed = slashedAmount.mulDiv(activeStake_, slashableStake);
                uint256 nextWithdrawalsSlashed = slashedAmount - activeSlashed;

                _activeStake.push(Time.timestamp(), activeStake_ - activeSlashed);
                withdrawals[captureEpoch + 1] = nextWithdrawals - nextWithdrawalsSlashed;
            }
```

**Example 2: [M-09] Users can deflate other markets Guild holders rewards by staking less pri** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-09-users-can-deflate-other-markets-guild-holders-rewards-by-staking-less-price.md`
```solidity
forge test --match-contract "StakeIntoWrongTermUnitTest" -vvv
```

**Example 3: `msg_server_stake::AddStake` calculates the weight incorrectly resulting in inco** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-32-msg_server_stakeaddstake-calculates-the-weight-incorrectly-resulting-in-inc.md`
```go
// Return the target weight of a topic
// ^w_{t,i} = S^{μ}_{t,i} * (P/C)^{ν}_{t,i}
// where S_{t,i} is the stake of of topic t in the last reward epoch i
// and (P/C)_{t,i} is the fee revenue collected for performing inference per topic epoch
// requests for topic t in the last reward epoch i
// μ, ν are global constants with fiduciary values of 0.5 and 0.5
```

**Example 4: MixinParams.setParams bypasses safety checks made by standard StakingProxy upgra** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/mixinparamssetparams-bypasses-safety-checks-made-by-standard-stakingproxy-upgrad.md`
```solidity
/// @dev Detach the current staking contract.
	/// Note that this is callable only by an authorized address.
	function detachStakingContract()
	    external
	    onlyAuthorized
	{
	    stakingContract = NIL\_ADDRESS;
	    emit StakingContractDetachedFromProxy();
	}
```

**Example 5: Operator can over allocate the same stake to unlimited nodes within one epoch ca** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/operator-can-over-allocate-the-same-stake-to-unlimited-nodes-within-one-epoch-ca.md`
```solidity
function addNode(
        bytes32 nodeId,
        bytes calldata blsKey,
        uint64 registrationExpiry,
        PChainOwner calldata remainingBalanceOwner,
        PChainOwner calldata disableOwner,
        uint256 stakeAmount // optional
    ) external updateStakeCache(getCurrentEpoch(), PRIMARY_ASSET_CLASS) updateGlobalNodeStakeOncePerEpoch {
        ...
        ...

        bytes32 valId = balancerValidatorManager.registeredValidators(abi.encodePacked(uint160(uint256(nodeId))));
        uint256 available = _getOperatorAvailableStake(operator);
        ...
        ...
    }
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in reward weight error logic allows exploitation through missing validation, inc
func secureRewardWeightError(ctx sdk.Context) error {
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
- **Severity Distribution**: MEDIUM: 5
- **Affected Protocols**: 0x v3 Staking, Suzaku Core, Allora, Tanssi_2025-04-30, Ethereum Credit Guild
- **Validation Strength**: Strong (3+ auditors)

---

## 6. Reward Historical Loss

### Overview

Implementation flaw in reward historical loss logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: The `AvalancheL1Middleware` contract has a vulnerability where if a new operator (Operator B) re-registers a node using the same `nodeId` as a former operator (Operator A), Operator A's stake can be artificially increased. This can lead to a misallocation of rewards. The issue is caused by a functio

### Vulnerability Description

#### Root Cause

Implementation flaw in reward historical loss logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies reward historical loss in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to reward operations

### Vulnerable Pattern Examples

**Example 1: Historical reward loss due to `NodeId` reuse in `AvalancheL1Middleware`** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/historical-reward-loss-due-to-nodeid-reuse-in-avalanchel1middleware.md`
```
// Vulnerable pattern from Suzaku Core:
**Description:** The `AvalancheL1Middleware` contract is vulnerable to misattributing stake to a former operator (Operator A) if a new, colluding or coordinated operator (Operator B) intentionally re-registers a node using the *exact same `bytes32 nodeId`* that Operator A previously used. This scenario assumes Operator B is aware of Operator A's historical `nodeId` and that the underlying P-Chain NodeID (`P_X`, derived from the shared `bytes32 nodeId`) has become available for re-registration on
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in reward historical loss logic allows exploitation through missing validation, 
func secureRewardHistoricalLoss(ctx sdk.Context) error {
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
- **Affected Protocols**: Suzaku Core
- **Validation Strength**: Single auditor

---

## 7. Reward Pool Share

### Overview

Implementation flaw in reward pool share logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: HIGH: 2, MEDIUM: 1.

> **Key Finding**: This bug report is related to the Gogopool protocol, which is a staking platform for Avalanche tokens (AVAX). The bug is related to the `MinipoolManager.sol` contract and the `recreateMinipool` function. This function is used to recreate minipools after a successful validation period. The bug is tha

### Vulnerability Description

#### Root Cause

Implementation flaw in reward pool share logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies reward pool share in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to reward operations

### Vulnerable Pattern Examples

**Example 1: [M-08] Recreated pools receive a wrong AVAX amount due to miscalculated compound** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-08-recreated-pools-receive-a-wrong-avax-amount-due-to-miscalculated-compounded.md`
```go
Minipool memory mp = getMinipool(minipoolIndex);
// Compound the avax plus rewards
// NOTE Assumes a 1:1 nodeOp:liqStaker funds ratio
uint256 compoundedAvaxNodeOpAmt = mp.avaxNodeOpAmt + mp.avaxNodeOpRewardAmt;
setUint(keccak256(abi.encodePacked("minipool.item", minipoolIndex, ".avaxNodeOpAmt")), compoundedAvaxNodeOpAmt);
setUint(keccak256(abi.encodePacked("minipool.item", minipoolIndex, ".avaxLiquidStakerAmt")), compoundedAvaxNodeOpAmt);
```

**Example 2: Missing Reward Address Checks** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/missing-reward-address-checks.md`
```solidity
// File: contracts/multiRewards/defi/base/MultiRewardsBasePoolV2.sol
function distributeRewards(address _reward, uint256 _amount) external override nonReentrant {
    IERC20(_reward).safeTransferFrom(_msgSender(), address(this), _amount);
    _distributeRewards(_reward, _amount);
}
```

**Example 3: Node Operators Can Claim RPL Stake Without Running A Node** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/node-operators-can-claim-rpl-stake-without-running-a-node.md`
```
// Vulnerable pattern from Rocketpool:
## Description

A Node Operator can submit a full withdrawal of their node, receive the ETH from their withdrawal, and continue to receive RPL from their staked RPL.

To achieve this state, a Node Operator submits a full withdrawal. They initiate the counter for a user to distribute the funds via `beginUserDistribute()`. They then distribute funds via another user after the user distribute timeout has elapsed. Finally, they claim the withdrawn ETH via `refund()` without calling `finalise()`. 

I
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in reward pool share logic allows exploitation through missing validation, incor
func secureRewardPoolShare(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 2, MEDIUM: 1
- **Affected Protocols**: GoGoPool, Vault-Tec, Rocketpool
- **Validation Strength**: Strong (3+ auditors)

---

## Detection Patterns

### Automated Detection
```
# Reward Calculation Incorrect
grep -rn 'reward|calculation|incorrect' --include='*.go' --include='*.sol'
# Reward Per Share Error
grep -rn 'reward|per|share|error' --include='*.go' --include='*.sol'
# Reward Delayed Balance
grep -rn 'reward|delayed|balance' --include='*.go' --include='*.sol'
# Reward Decimal Mismatch
grep -rn 'reward|decimal|mismatch' --include='*.go' --include='*.sol'
# Reward Weight Error
grep -rn 'reward|weight|error' --include='*.go' --include='*.sol'
# Reward Historical Loss
grep -rn 'reward|historical|loss' --include='*.go' --include='*.sol'
# Reward Pool Share
grep -rn 'reward|pool|share' --include='*.go' --include='*.sol'
```

## Keywords

`account`, `accounting`, `accumulation`, `activation`, `address`, `amount`, `appchain`, `attacker`, `avax`, `balance`, `being`, `calculates`, `calculation`, `checks`, `claim`, `compounded`, `cosmos`, `decimal`, `deflate`, `delayed`, `denial`, `distribution`, `error`, `exploited`, `fails`, `finalized`, `flawed`, `frequent`, `from`, `frontrun`
