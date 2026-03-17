---
protocol: generic
chain: cosmos
category: liquidity
vulnerability_type: liquidity_pool_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: liquidity_logic

primitives:
  - pool_manipulation
  - imbalance
  - removal_dos
  - fee_error
  - concentrated

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - liquidity
  - staking
  - defi

language: go|solidity|rust
version: all

# Pattern Identity (Required)
root_cause_family: logic_error
pattern_key: logic_error | liquidity_logic | liquidity_pool_vulnerabilities

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - block.timestamp
  - concentrated
  - deposit
  - fee_error
  - imbalance
  - mint
  - pool_manipulation
  - rebalanceBadDebt
  - receive
  - recordStakingStart
  - removal_dos
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Liquidity Pool Manipulation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| CVGT Staking Pool State Manipulation | `reports/cosmos_cometbft_findings/cvgt-staking-pool-state-manipulation.md` | HIGH | OtterSec |
| [H-01] AVAX Assigned High Water is updated incorrectly | `reports/cosmos_cometbft_findings/h-01-avax-assigned-high-water-is-updated-incorrectly.md` | HIGH | Code4rena |
| H-01 wstETH-ETH Curve LP Token Price can be manipulated to C | `reports/cosmos_cometbft_findings/h-1-h-01-wsteth-eth-curve-lp-token-price-can-be-manipulated-to-cause-unexpected-.md` | HIGH | Sherlock |
| Attacker can inflict losses to other Superpool user's during | `reports/cosmos_cometbft_findings/m-20-attacker-can-inflict-losses-to-other-superpool-users-during-a-bad-debt-liqu.md` | MEDIUM | Sherlock |
| Deposit Theft by Crashing LP Spot Prices Through MEV | `reports/cosmos_cometbft_findings/m-4-deposit-theft-by-crashing-lp-spot-prices-through-mev.md` | MEDIUM | Sherlock |
| LibTWAPOracle::update Providing large liquidity will manipul | `reports/cosmos_cometbft_findings/m-4-libtwaporacleupdate-providing-large-liquidity-will-manipulate-twap-dosing-re.md` | MEDIUM | Sherlock |
| RocketMinipoolDelegateOld - Node operator may reenter finali | `reports/cosmos_cometbft_findings/rocketminipooldelegateold-node-operator-may-reenter-finalise-to-manipulate-accou.md` | HIGH | ConsenSys |
| The pool owner can manipulate users to steal all of their st | `reports/cosmos_cometbft_findings/the-pool-owner-can-manipulate-users-to-steal-all-of-their-stake-amounts-by-using.md` | HIGH | Cantina |

### Liquidity Imbalance
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-04] Unstaking from LP pools will cause underflow and lock | `reports/cosmos_cometbft_findings/m-04-unstaking-from-lp-pools-will-cause-underflow-and-lock-user-funds.md` | MEDIUM | Code4rena |
| Attacker can inflict losses to other Superpool user's during | `reports/cosmos_cometbft_findings/m-20-attacker-can-inflict-losses-to-other-superpool-users-during-a-bad-debt-liqu.md` | MEDIUM | Sherlock |
| Node Operators Can Claim RPL Stake Without Running A Node | `reports/cosmos_cometbft_findings/node-operators-can-claim-rpl-stake-without-running-a-node.md` | HIGH | SigmaPrime |

---

# Liquidity Pool Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Liquidity Pool Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Liquidity Pool Manipulation](#1-liquidity-pool-manipulation)
2. [Liquidity Imbalance](#2-liquidity-imbalance)

---

## 1. Liquidity Pool Manipulation

### Overview

Implementation flaw in liquidity pool manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 8 audit reports with severity distribution: HIGH: 5, MEDIUM: 3.

> **Key Finding**: The report highlights a potential vulnerability in the CVGT staking state that can be exploited by manipulating the CVGT mint and CVGTStakingPoolState accounts. This allows attackers to set any CVGT on a poolstate and stability_pool_state, as well as spoof the CVGTStakingPoolState, potentially enabl



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of logic_error"
- Pattern key: `logic_error | liquidity_logic | liquidity_pool_vulnerabilities`
- Interaction scope: `single_contract`
- Primary affected component(s): `liquidity_logic`
- High-signal code keywords: `block.timestamp`, `concentrated`, `deposit`, `fee_error`, `imbalance`, `mint`, `pool_manipulation`, `rebalanceBadDebt`
- Typical sink / impact: `fund_loss|dos|state_corruption`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `N/A`
- Trust boundary crossed: `internal`
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

Implementation flaw in liquidity pool manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies liquidity pool manipulation in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to liquidity operations

### Vulnerable Pattern Examples

**Example 1: CVGT Staking Pool State Manipulation** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/cvgt-staking-pool-state-manipulation.md`
```rust
pub struct Initialize<'info> {
    #[account()]
    pub cvgt: Box<Account<'info, Mint>>,
}
```

**Example 2: [H-01] AVAX Assigned High Water is updated incorrectly** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-avax-assigned-high-water-is-updated-incorrectly.md`
```solidity
MinipoolManager.sol
349: 	function recordStakingStart(
350: 		address nodeID,
351: 		bytes32 txID,
352: 		uint256 startTime
353: 	) external {
354: 		int256 minipoolIndex = onlyValidMultisig(nodeID);
355: 		requireValidStateTransition(minipoolIndex, MinipoolStatus.Staking);
356: 		if (startTime > block.timestamp) {
357: 			revert InvalidStartTime();
358: 		}
359:
360: 		setUint(keccak256(abi.encodePacked("minipool.item", minipoolIndex, ".status")), uint256(MinipoolStatus.Staking));
361: 		setBytes32(keccak256(abi.encodePacked("minipool.item", minipoolIndex, ".txID")), txID);
362: 		setUint(keccak256(abi.encodePacked("minipool.item", minipoolIndex, ".startTime")), startTime);
363:
364: 		// If this is the first of many cycles, set the initialStartTime
365: 		uint256 initialStartTime = getUint(keccak256(abi.encodePacked("minipool.item", minipoolIndex, ".initialStartTime")));
366: 		if (initialStartTime == 0) {
367: 			setUint(keccak256(abi.encodePacked("minipool.item", minipoolIndex, ".initialStartTime")), startTime);
368: 		}
369:
370: 		address owner = getAddress(keccak256(abi.encodePacked("minipool.item", minipoolIndex, ".owner")));
371: 		uint256 avaxLiquidStakerAmt = getUint(keccak256(abi.encodePacked("minipool.item", minipoolIndex, ".avaxLiquidStakerAmt")));
372: 		Staking staking = Staking(getContractAddress("Staking"));
373: 		if (staking.getAVAXAssignedHighWater(owner) < staking.getAVAXAssigned(owner)) {
374: 			staking.increaseAVAXAssignedHighWater(owner, avaxLiquidStakerAmt);//@audit wrong
375: 		}
376:
377: 		emit MinipoolStatusChanged(nodeID, MinipoolStatus.Staking);
378: 	}
```

**Example 3: H-01 wstETH-ETH Curve LP Token Price can be manipulated to Cause Unexpected Liqu** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-1-h-01-wsteth-eth-curve-lp-token-price-can-be-manipulated-to-cause-unexpected-.md`
```go
>>> history[-1].events
{'Debug': [OrderedDict([('name', 'Virtual Price 1'), ('value', 1005466094471744332)]), OrderedDict([('name', 'fakeSentimentPrice 1'), ('value', 1005466094471744332)]), OrderedDict([('name', 'Virtual Price 3'), ('value', 1005497298777214105)]), OrderedDict([('name', 'fakeSentimentPrice 3'), ('value', 1005497298777214105)]), OrderedDict([('name', 'Virtual Price 5'), ('value', 890315892210177531)]), OrderedDict([('name', 'fakeSentimentPrice 5'), ('value', 890315892210177531)]), OrderedDict([('name', 'Virtual Price 6'), ('value', 1005497298777214105)]), OrderedDict([('name', 'fakeSentimentPrice 6'), ('value', 1005497298777214105)]), OrderedDict([('name', 'Msg.value'), ('value', 1452330000000000000000)]), OrderedDict([('name', 'This Balance'), ('value', 713314090131700921245)]), OrderedDict([('name', 'Delta'), ('value', 739015909868299078755)]), OrderedDict([('name', 'WstEthBalance'), ('value', 677574531693017948098)])], 'Transfer': [OrderedDict([('_from', '0x0000000000000000000000000000000000000000'), ('_to', '0xE7eD6747FaC5360f88a2EFC03E00d25789F69291'), ('_value', 1449753409949781400798)]), OrderedDict([('from', '0x6eB2dc694eB516B16Dc9FBc678C60052BbdD7d80'), ('to', '0xE7eD6747FaC5360f88a2EFC03E00d25789F69291'), ('value', 677574531693017948098)]), OrderedDict([('_from', '0xE7eD6747FaC5360f88a2EFC03E00d25789F69291'), ('_to', '0x0000000000000000000000000000000000000000'), ('_value', 1449753409949781400798)])], 'AddLiquidity': [OrderedDict([('provider', '0xE7eD6747FaC5360f88a2EFC03E00d25789F69291'), ('token_amounts', (1452330000000000000000, 0)), ('fees', (192842135570862938, 176890872766115807)), ('invariant', 6238313797265075968081), ('token_supply', 6204014881865700809814)])], 'RemoveLiquidity': [OrderedDict([('provider', '0xE7eD6747FaC5360f88a2EFC03E00d25789F69291'), ('token_amounts', (713314090131700921245, 677574531693017948098)), ('fees', (0, 0)), ('token_supply', 4754261471915919409016)])]}
>>> 890315892210177531 / 1005466094471744332
## Around 11.2% Price Manipulation with 14.5k ETH used
0.8854757978467043
```

**Example 4: Attacker can inflict losses to other Superpool user's during a bad debt liquidat** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-20-attacker-can-inflict-losses-to-other-superpool-users-during-a-bad-debt-liqu.md`
```solidity
function rebalanceBadDebt(uint256 poolId, address position) external {
        
        .....

        pool.totalDepositAssets = (totalDepositAssets > borrowAssets) ? totalDepositAssets - borrowAssets : 0;
```

**Example 5: Deposit Theft by Crashing LP Spot Prices Through MEV** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-4-deposit-theft-by-crashing-lp-spot-prices-through-mev.md`
```
// Vulnerable pattern from Blueberry:
Source: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/220
```

**Variant: Liquidity Pool Manipulation - MEDIUM Severity Cases** [MEDIUM]
> Found in 3 reports:
> - `reports/cosmos_cometbft_findings/m-20-attacker-can-inflict-losses-to-other-superpool-users-during-a-bad-debt-liqu.md`
> - `reports/cosmos_cometbft_findings/m-4-deposit-theft-by-crashing-lp-spot-prices-through-mev.md`
> - `reports/cosmos_cometbft_findings/m-4-libtwaporacleupdate-providing-large-liquidity-will-manipulate-twap-dosing-re.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in liquidity pool manipulation logic allows exploitation through missing validat
func secureLiquidityPoolManipulation(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 8 audit reports
- **Severity Distribution**: HIGH: 5, MEDIUM: 3
- **Affected Protocols**: Sentiment Update, GoGoPool, Goat Tech, Ubiquity, Convergent
- **Validation Strength**: Strong (3+ auditors)

---

## 2. Liquidity Imbalance

### Overview

Implementation flaw in liquidity imbalance logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: HIGH: 1, MEDIUM: 2.

> **Key Finding**: This bug report describes an issue with the `initiate_unstake` function in the `pool_router` contract. When users unstake their LP tokens, the `unstaked_pending_amounts` variable is increased, and an admin or user can call `batch_undelegate_pending_lps` to undelegate these tokens. However, there is 

### Vulnerability Description

#### Root Cause

Implementation flaw in liquidity imbalance logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies liquidity imbalance in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to liquidity operations

### Vulnerable Pattern Examples

**Example 1: [M-04] Unstaking from LP pools will cause underflow and lock user funds** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-04-unstaking-from-lp-pools-will-cause-underflow-and-lock-user-funds.md`
```go
for (i in 0..vector::length(&m_store.unbond_period)) {
	// undelegate
	pool_router::unlock(m_store.stake_token_metadata[i], m_store.unstaked_pending_amounts[i]);
	// clear pending
	m_store.unstaked_pending_amounts[i] = 0;
};
```

**Example 2: Attacker can inflict losses to other Superpool user's during a bad debt liquidat** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-20-attacker-can-inflict-losses-to-other-superpool-users-during-a-bad-debt-liqu.md`
```solidity
function rebalanceBadDebt(uint256 poolId, address position) external {
        
        .....

        pool.totalDepositAssets = (totalDepositAssets > borrowAssets) ? totalDepositAssets - borrowAssets : 0;
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
// Addresses: Implementation flaw in liquidity imbalance logic allows exploitation through missing validation, inc
func secureLiquidityImbalance(ctx sdk.Context) error {
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
- **Affected Protocols**: Cabal, Rocketpool, Sentiment V2
- **Validation Strength**: Strong (3+ auditors)

---

## Detection Patterns

### Automated Detection
```
# Liquidity Pool Manipulation
grep -rn 'liquidity|pool|manipulation' --include='*.go' --include='*.sol'
# Liquidity Imbalance
grep -rn 'liquidity|imbalance' --include='*.go' --include='*.sol'
```

## Keywords

`appchain`, `assigned`, `attacker`, `avax`, `cause`, `claim`, `concentrated`, `cosmos`, `curve`, `cvgt`, `debt`, `depending`, `dos`, `during`, `error`, `fee`, `from`, `funds`, `high`, `imbalance`, `incorrectly`, `inflict`, `liquidation`, `liquidations`, `liquidity`, `lock`, `losses`, `manipulated`, `manipulation`, `node`

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

`appchain`, `block.timestamp`, `concentrated`, `cosmos`, `defi`, `deposit`, `fee_error`, `imbalance`, `liquidity`, `liquidity_pool_vulnerabilities`, `mint`, `pool_manipulation`, `rebalanceBadDebt`, `receive`, `recordStakingStart`, `removal_dos`, `staking`
