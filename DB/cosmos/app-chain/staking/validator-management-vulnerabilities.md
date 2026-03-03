---
protocol: generic
chain: cosmos
category: staking
vulnerability_type: validator_management_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: staking_logic

primitives:
  - registration_bypass
  - removal_failure
  - set_manipulation
  - key_rotation
  - commission_exploit
  - status_transition
  - dust_collateral
  - score_manipulation
  - operator_mismatch
  - can_skip_exit

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - staking
  - staking
  - defi

language: go|solidity|rust
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Validator Registration Bypass
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Absence of IBC Channel Verification in UpdateEntry Function | `reports/cosmos_cometbft_findings/absence-of-ibc-channel-verification-in-updateentry-function.md` | MEDIUM | Halborn |
| Cannot Blame Operator for Proposed Validator | `reports/cosmos_cometbft_findings/cannot-blame-operator-for-proposed-validator.md` | MEDIUM | ConsenSys |
| [H-01] Lack of access control in `AgentNftV2::addValidator() | `reports/cosmos_cometbft_findings/h-01-lack-of-access-control-in-agentnftv2addvalidator-enables-unauthorized-valid.md` | HIGH | Code4rena |
| Rogue validators can manipulate funding rates and profit unf | `reports/cosmos_cometbft_findings/h-3-rogue-validators-can-manipulate-funding-rates-and-profit-unfairly-from-liqui.md` | HIGH | Sherlock |
| Lack Of Instruction Sysvar Validation | `reports/cosmos_cometbft_findings/lack-of-instruction-sysvar-validation.md` | HIGH | OtterSec |
| Lack Of Sysvar Account Validation | `reports/cosmos_cometbft_findings/lack-of-sysvar-account-validation.md` | HIGH | OtterSec |
| [M-04] Preventing balance updates by adding a new validator  | `reports/cosmos_cometbft_findings/m-04-preventing-balance-updates-by-adding-a-new-validator-in-the-current-block.md` | MEDIUM | Pashov Audit Group |
| Attacker will manipulate voting power calculations as `getOp | `reports/cosmos_cometbft_findings/m-1-attacker-will-manipulate-voting-power-calculations-as-getoperatorvotingpower.md` | MEDIUM | Sherlock |

### Validator Removal Failure
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Delegations might stuck in non-active validator  Pending | `reports/cosmos_cometbft_findings/delegations-might-stuck-in-non-active-validator-pending.md` | MEDIUM | ConsenSys |
| [H-02] ValidatorManager: missing fund withdrawal from valida | `reports/cosmos_cometbft_findings/h-02-validatormanager-missing-fund-withdrawal-from-validator-in-deactivatevalida.md` | HIGH | Pashov Audit Group |
| [M-01] Missing check in the `updateValset` function | `reports/cosmos_cometbft_findings/m-01-missing-check-in-the-updatevalset-function.md` | MEDIUM | Code4rena |
| [M-02] _depositEther Does Not Increment Validator Index,Caus | `reports/cosmos_cometbft_findings/m-02-_depositether-does-not-increment-validator-indexcausing-all-deposits-to-fun.md` | MEDIUM | Kann |
| Ether can stuck when an operators validators are removed due | `reports/cosmos_cometbft_findings/m-2-ether-can-stuck-when-an-operators-validators-are-removed-due-to-an-user-fron.md` | MEDIUM | Sherlock |
| when a validator is kicked out of the bonded validator set , | `reports/cosmos_cometbft_findings/m-5-when-a-validator-is-kicked-out-of-the-bonded-validator-set-unstake-funds-wil.md` | MEDIUM | Sherlock |
| Operator is not removed in Registry when validator has `owed | `reports/cosmos_cometbft_findings/operator-is-not-removed-in-registry-when-validator-has-owedamount-0.md` | HIGH | Cyfrin |
| Potential Misallocation of Validators in `_getDepositsAlloca | `reports/cosmos_cometbft_findings/potential-misallocation-of-validators-in-_getdepositsallocation-function.md` | MEDIUM | MixBytes |

### Validator Set Manipulation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Missing highestVotingPower Update in argmaxBlockByStake Resu | `reports/cosmos_cometbft_findings/h-6-missing-highestvotingpower-update-in-argmaxblockbystake-resulting-in-incorre.md` | HIGH | Sherlock |
| Incorrect Injected Vote Extensions Validation | `reports/cosmos_cometbft_findings/incorrect-injected-vote-extensions-validation.md` | HIGH | OtterSec |
| Key typo may allow store corruption | `reports/cosmos_cometbft_findings/key-typo-may-allow-store-corruption.md` | HIGH | Halborn |
| Lack Of Signature Verification | `reports/cosmos_cometbft_findings/lack-of-signature-verification.md` | HIGH | OtterSec |
| [M-01] Missing check in the `updateValset` function | `reports/cosmos_cometbft_findings/m-01-missing-check-in-the-updatevalset-function.md` | MEDIUM | Code4rena |
| Attacker will manipulate voting power calculations as `getOp | `reports/cosmos_cometbft_findings/m-1-attacker-will-manipulate-voting-power-calculations-as-getoperatorvotingpower.md` | MEDIUM | Sherlock |
| [M-14] `VotesUpgradeable::delegate` bypasses the `addValidat | `reports/cosmos_cometbft_findings/m-14-votesupgradeabledelegate-bypasses-the-addvalidator-call-leads-to-a-non-vali.md` | MEDIUM | Code4rena |
| A malicious operator will control consensus without risking  | `reports/cosmos_cometbft_findings/m-7-a-malicious-operator-will-control-consensus-without-risking-stake-stake-exit.md` | MEDIUM | Sherlock |

### Validator Key Rotation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| blockBuilderBLSKeyToAddress[] can be overwritten in Provider | `reports/cosmos_cometbft_findings/blockbuilderblskeytoaddress-can-be-overwritten-in-providerregistrysol_registeran.md` | HIGH | Cantina |
| [M-03] `xfeemarket` module is not wired up, resulting in non | `reports/cosmos_cometbft_findings/m-03-xfeemarket-module-is-not-wired-up-resulting-in-non-working-cli-commands-mes.md` | MEDIUM | Code4rena |
| Potential To Rotate Consensus Key Back To Initial Key | `reports/cosmos_cometbft_findings/potential-to-rotate-consensus-key-back-to-initial-key.md` | MEDIUM | OtterSec |

### Validator Commission Exploit
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Validators can Manipulate Commission Rates | `reports/cosmos_cometbft_findings/validators-can-manipulate-commission-rates.md` | MEDIUM | OtterSec |
| Validators Manipulating Commission Rates | `reports/cosmos_cometbft_findings/validators-manipulating-commission-rates.md` | MEDIUM | OtterSec |

### Validator Status Transition
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Deposited Stakes Can Be Locked in StakeManager if the Valida | `reports/cosmos_cometbft_findings/deposited-stakes-can-be-locked-in-stakemanager-if-the-validator-is-inactive.md` | HIGH | OpenZeppelin |
| [M-04] New stakes delegated even when validator is inactive | `reports/cosmos_cometbft_findings/m-04-new-stakes-delegated-even-when-validator-is-inactive.md` | MEDIUM | Pashov Audit Group |
| [PRST-4] Unbonding of validators does not give priority to i | `reports/cosmos_cometbft_findings/prst-4-unbonding-of-validators-does-not-give-priority-to-inactive-validators.md` | MEDIUM | Hexens |
| Validator State Desynchronization | `reports/cosmos_cometbft_findings/validator-state-desynchronization.md` | HIGH | OtterSec |

### Validator Dust Collateral
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Allowing the creation of "dust CDPs" could lead redeemers/li | `reports/cosmos_cometbft_findings/allowing-the-creation-of-dust-cdps-could-lead-redeemersliquidators-to-be-not-pro.md` | HIGH | Cantina |
| Dust limit attack on `forceUpdateNodes` allows DoS of rebala | `reports/cosmos_cometbft_findings/dust-limit-attack-on-forceupdatenodes-allows-dos-of-rebalancing-and-potential-va.md` | HIGH | Cyfrin |
| [M-17] Bad debt can be permanently blocked from being moved  | `reports/cosmos_cometbft_findings/m-17-bad-debt-can-be-permanently-blocked-from-being-moved-to-backstop.md` | MEDIUM | Code4rena |
| Validators with dust collateral can join the network | `reports/cosmos_cometbft_findings/validators-with-dust-collateral-can-join-the-network.md` | HIGH | Zokyo |

### Validator Score Manipulation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Activation of queued cutting board can be manipulated leadin | `reports/cosmos_cometbft_findings/activation-of-queued-cutting-board-can-be-manipulated-leading-to-redirection-of-.md` | MEDIUM | Spearbit |
| COIN DENOMINATION IS NOT CHECKED WHEN REMOVING VALIDATORS | `reports/cosmos_cometbft_findings/coin-denomination-is-not-checked-when-removing-validators.md` | MEDIUM | Halborn |
| Deposited Stakes Can Be Locked in StakeManager if the Valida | `reports/cosmos_cometbft_findings/deposited-stakes-can-be-locked-in-stakemanager-if-the-validator-is-inactive.md` | HIGH | OpenZeppelin |
| Dust limit attack on `forceUpdateNodes` allows DoS of rebala | `reports/cosmos_cometbft_findings/dust-limit-attack-on-forceupdatenodes-allows-dos-of-rebalancing-and-potential-va.md` | HIGH | Cyfrin |
| [H-01] Lack of access control in `AgentNftV2::addValidator() | `reports/cosmos_cometbft_findings/h-01-lack-of-access-control-in-agentnftv2addvalidator-enables-unauthorized-valid.md` | HIGH | Code4rena |
| [H-05] `ValidatorRegistry::validatorScore/getPastValidatorSc | `reports/cosmos_cometbft_findings/h-05-validatorregistryvalidatorscoregetpastvalidatorscore-allows-validator-to-ea.md` | HIGH | Code4rena |
| Missing highestVotingPower Update in argmaxBlockByStake Resu | `reports/cosmos_cometbft_findings/h-6-missing-highestvotingpower-update-in-argmaxblockbystake-resulting-in-incorre.md` | HIGH | Sherlock |
| Immediate stake cache updates enable reward distribution wit | `reports/cosmos_cometbft_findings/immediate-stake-cache-updates-enable-reward-distribution-without-p-chain-confirm.md` | HIGH | Cyfrin |

### Validator Operator Mismatch
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Direct Deposits Enable Theft Of A Validator’s Funds | `reports/cosmos_cometbft_findings/direct-deposits-enable-theft-of-a-validators-funds.md` | HIGH | SigmaPrime |
| Historical reward loss due to `NodeId` reuse in `AvalancheL1 | `reports/cosmos_cometbft_findings/historical-reward-loss-due-to-nodeid-reuse-in-avalanchel1middleware.md` | MEDIUM | Cyfrin |
| Node Operator Rewards Unevenly Leaked | `reports/cosmos_cometbft_findings/node-operator-rewards-unevenly-leaked.md` | MEDIUM | SigmaPrime |

### Validator Can Skip Exit
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| AnteHandler Skipped In Non-CheckTx Mode | `reports/cosmos_cometbft_findings/antehandler-skipped-in-non-checktx-mode.md` | HIGH | OtterSec |
| Validators Can Skip createEndRequest and Quickly Re-Register | `reports/cosmos_cometbft_findings/validators-can-skip-createendrequest-and-quickly-re-register.md` | HIGH | OpenZeppelin |

### Validator Governance Power
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-01] A staker with verified over-commitment can potentiall | `reports/cosmos_cometbft_findings/m-01-a-staker-with-verified-over-commitment-can-potentially-bypass-slashing-comp.md` | MEDIUM | Code4rena |
| [M03] Users can avoid some slashing penalties by front-runni | `reports/cosmos_cometbft_findings/m03-users-can-avoid-some-slashing-penalties-by-front-running.md` | MEDIUM | OpenZeppelin |

---

# Validator Management Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Validator Management Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Validator Registration Bypass](#1-validator-registration-bypass)
2. [Validator Removal Failure](#2-validator-removal-failure)
3. [Validator Set Manipulation](#3-validator-set-manipulation)
4. [Validator Key Rotation](#4-validator-key-rotation)
5. [Validator Commission Exploit](#5-validator-commission-exploit)
6. [Validator Status Transition](#6-validator-status-transition)
7. [Validator Dust Collateral](#7-validator-dust-collateral)
8. [Validator Score Manipulation](#8-validator-score-manipulation)
9. [Validator Operator Mismatch](#9-validator-operator-mismatch)
10. [Validator Can Skip Exit](#10-validator-can-skip-exit)
11. [Validator Governance Power](#11-validator-governance-power)

---

## 1. Validator Registration Bypass

### Overview

Implementation flaw in validator registration bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 14 audit reports with severity distribution: HIGH: 7, MEDIUM: 7.

> **Key Finding**: The provided UpdateEntry function in a system managing entries in IBC lacks verification for the correctness and validity of Inter-Blockchain Communication (IBC) channel identifiers. This can potentially lead to unauthorized access or incorrect updates to the system. The recommended solution is for 

### Vulnerability Description

#### Root Cause

Implementation flaw in validator registration bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies validator registration bypass in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to validator operations

### Vulnerable Pattern Examples

**Example 1: Absence of IBC Channel Verification in UpdateEntry Function** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/absence-of-ibc-channel-verification-in-updateentry-function.md`
```go
func (k msgServer) UpdateEntry(goCtx context.Context, msg *types.MsgUpdateEntry) (*types.MsgUpdateEntryResponse, error) {
	if k.authority != msg.Authority {
		return nil, errors.Wrapf(govtypes.ErrInvalidSigner, "invalid authority; expected %s, got %s", k.authority, msg.Authority)
	}

	ctx := sdk.UnwrapSDKContext(goCtx)

	// Check if the value exists
	entry, isFound := k.GetEntry(ctx, msg.BaseDenom)
	if !isFound {
		return nil, errorsmod.Wrap(sdkerrors.ErrKeyNotFound, "entry not set")
	}

	// Checks if the the msg authority is the same as the current owner
	if msg.Authority != entry.Authority {
		return nil, errorsmod.Wrap(sdkerrors.ErrUnauthorized, "incorrect owner")
	}

	entry = types.Entry{
		Authority:                msg.Authority,
		BaseDenom:                msg.BaseDenom,
		Decimals:                 msg.Decimals,
		Denom:                    msg.Denom,
		Path:                     msg.Path,
		IbcChannelId:             msg.IbcChannelId,
		IbcCounterpartyChannelId: msg.IbcCounterpartyChannelId,
		DisplayName:              msg.DisplayName,
		DisplaySymbol:            msg.DisplaySymbol,
		Network:                  msg.Network,
		Address:                  msg.Address,
		ExternalSymbol:           msg.ExternalSymbol,
		TransferLimit:            msg.TransferLimit,
		Permissions:              msg.Permissions,
		UnitDenom:                msg.UnitDenom,
		IbcCounterpartyDenom:     msg.IbcCounterpartyDenom,
// ... (truncated)
```

**Example 2: Cannot Blame Operator for Proposed Validator** [MEDIUM]
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

**Example 4: Rogue validators can manipulate funding rates and profit unfairly from liquidati** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-3-rogue-validators-can-manipulate-funding-rates-and-profit-unfairly-from-liqui.md`
```
// Vulnerable pattern from Hubble Exchange:
Source: https://github.com/sherlock-audit/2023-04-hubble-exchange-judging/issues/183
```

**Example 5: Lack Of Instruction Sysvar Validation** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/lack-of-instruction-sysvar-validation.md`
```rust
#[derive(Accounts)]
pub struct Deposit<'info> {
    #[account(mut)]
    pub depositor: Signer<'info>,
    [...]
    /// CHECK:
    pub instruction: AccountInfo<'info>,
    [...]
}
```

**Variant: Validator Registration Bypass - HIGH Severity Cases** [HIGH]
> Found in 7 reports:
> - `reports/cosmos_cometbft_findings/h-01-lack-of-access-control-in-agentnftv2addvalidator-enables-unauthorized-valid.md`
> - `reports/cosmos_cometbft_findings/h-3-rogue-validators-can-manipulate-funding-rates-and-profit-unfairly-from-liqui.md`
> - `reports/cosmos_cometbft_findings/lack-of-instruction-sysvar-validation.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in validator registration bypass logic allows exploitation through missing valid
func secureValidatorRegistrationBypass(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 7, MEDIUM: 7
- **Affected Protocols**: Composable Vaults, Virtuals Protocol, Karak-June, Symbiotic Relay, Convergent
- **Validation Strength**: Strong (3+ auditors)

---

## 2. Validator Removal Failure

### Overview

Implementation flaw in validator removal failure logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 8 audit reports with severity distribution: HIGH: 2, MEDIUM: 6.

> **Key Finding**: This bug report is about the issue that when a validator does not get enough funds to run a node (Minimum Staking Requirement, MSR), all token holders that delegated tokens to the validator cannot switch to a different validator, and might result in funds getting stuck with the nonfunctioning valida

### Vulnerability Description

#### Root Cause

Implementation flaw in validator removal failure logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies validator removal failure in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to validator operations

### Vulnerable Pattern Examples

**Example 1: Delegations might stuck in non-active validator  Pending** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/delegations-might-stuck-in-non-active-validator-pending.md`
```go
require((validatorNodes.length + 1) \* msr <= delegationsTotal, "Validator has to meet Minimum Staking Requirement");
```

**Example 2: [H-02] ValidatorManager: missing fund withdrawal from validator in `deactivateva** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-02-validatormanager-missing-fund-withdrawal-from-validator-in-deactivatevalida.md`
```solidity
function deactivateValidator(address validator) external whenNotPaused nonReentrant validatorExists(validator) {
        // Oracle manager will also call this, so limit the msg.sender to both MANAGER_ROLE and ORACLE_ROLE
        require(hasRole(MANAGER_ROLE, msg.sender) || hasRole(ORACLE_ROLE, msg.sender), "Not authorized");

        (bool exists, uint256 index) = _validatorIndexes.tryGet(validator);
        require(exists, "Validator does not exist");

        Validator storage validatorData = _validators[index];
        require(validatorData.active, "Validator already inactive");

        // Create withdrawal request before state changes
        if (validatorData.balance > 0) {
            _addRebalanceRequest(validator, validatorData.balance);
        }

        // Update state after withdrawal request
        validatorData.active = false;

        emit ValidatorDeactivated(validator);
    }
```

**Example 3: [M-01] Missing check in the `updateValset` function** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-01-missing-check-in-the-updatevalset-function.md`
```
// Vulnerable pattern from Cudos:
[Gravity.sol#L276-L358](https://github.com/code-423n4/2022-05-cudos/blob/de39cf3cd1f1e1cf211819b06d4acf6a043acda0/solidity/contracts/Gravity.sol#L276-L358)<br>

The `updateValset` function don't check that the sum of the powers of the new validators in the new valset is greater than the threshold, which can lead to unwanted behavior.

There are 2 main problems that can occur in that situation:

1.  The sum of the new validators' powers will be lower than the `state_powerThreshold`
2.  The sum of
```

**Example 4: [M-02] _depositEther Does Not Increment Validator Index,Causing All Deposits to ** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-02-_depositether-does-not-increment-validator-indexcausing-all-deposits-to-fun.md`
```
// Vulnerable pattern from Mystic Finance:
## Severity

Medium
```

**Example 5: Ether can stuck when an operators validators are removed due to an user front-ru** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-2-ether-can-stuck-when-an-operators-validators-are-removed-due-to-an-user-fron.md`
```go
if (validatorDetails.cap > 0 && newValidatorCap == 0) {
            // If there are active deposits, queue the operator for strategy exit.
            if (activeDeposits > 0) {
                -> operatorDetails.queueOperatorStrategyExit(operatorId, BEACON_CHAIN_STRATEGY);
                .
            }
           .
        } else if (validatorDetails.cap == 0 && newValidatorCap > 0) {
           .
        } else {
           .
        }
```

**Variant: Validator Removal Failure - HIGH Severity Cases** [HIGH]
> Found in 2 reports:
> - `reports/cosmos_cometbft_findings/h-02-validatormanager-missing-fund-withdrawal-from-validator-in-deactivatevalida.md`
> - `reports/cosmos_cometbft_findings/operator-is-not-removed-in-registry-when-validator-has-owedamount-0.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in validator removal failure logic allows exploitation through missing validatio
func secureValidatorRemovalFailure(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 2, MEDIUM: 6
- **Affected Protocols**: Cudos, Lido, Casimir, Andromeda – Validator Staking ADO and Vesting ADO, Kinetiq_2025-02-26
- **Validation Strength**: Strong (3+ auditors)

---

## 3. Validator Set Manipulation

### Overview

Implementation flaw in validator set manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 12 audit reports with severity distribution: HIGH: 6, MEDIUM: 6.

> **Key Finding**: This bug report discusses an issue with the argmaxBlockByStake function, which is used to identify the block height with the highest cumulative voting power based on the stakes of voting reputers. The calculation for highestVotingPower is flawed, as it fails to update when a new block with higher vo

### Vulnerability Description

#### Root Cause

Implementation flaw in validator set manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies validator set manipulation in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to validator operations

### Vulnerable Pattern Examples

**Example 1: Missing highestVotingPower Update in argmaxBlockByStake Resulting in Incorrect B** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-6-missing-highestvotingpower-update-in-argmaxblockbystake-resulting-in-incorre.md`
```go
func (ap *AppChain) argmaxBlockByStake(
	blockToReputer *map[int64][]string,
	stakesPerReputer map[string]cosmossdk_io_math.Int,
) int64 {
	// Find the current block height with the highest voting power
	firstIter := true
	highestVotingPower := cosmossdk_io_math.ZeroInt()
	blockOfMaxPower := int64(-1)
	for block, reputersWhoVotedForBlock := range *blockToReputer {
		// Calc voting power of this candidate block by total voting reputer stake
		blockVotingPower := cosmossdk_io_math.ZeroInt()
		for _, reputerAddr := range reputersWhoVotedForBlock {
			blockVotingPower = blockVotingPower.Add(stakesPerReputer[reputerAddr])
		}

		// Decide if voting power exceeds that of current front-runner
		if firstIter || blockVotingPower.GT(highestVotingPower) {
@>			blockOfMaxPower = block // Correctly updates the block
@>			// Missing highestVotingPower = blockVotingPower
		}

		firstIter = false
	}

	return blockOfMaxPower
}
```

**Example 2: Incorrect Injected Vote Extensions Validation** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/incorrect-injected-vote-extensions-validation.md`
```go
// Sample code for ValidateVoteExtensions function
func ValidateVoteExtensions(
[...]
) error {
    cp := ctx.ConsensusParams()
    // Start checking vote extensions only **after** the vote extensions enable height,
    // because when `currentHeight == VoteExtensionsEnableHeight`
    // PrepareProposal doesn't get any vote extensions in its request.
    extsEnabled := cp.Abci != nil && currentHeight > cp.Abci.VoteExtensionsEnableHeight &&
    cp.Abci.VoteExtensionsEnableHeight != 0

    marshalDelimitedFn := func(msg proto.Message) ([]byte, error) {
        var buf bytes.Buffer
        if err := protoio.NewDelimitedWriter(&buf).WriteMsg(msg); err != nil {
            return nil, err
        }
        return buf.Bytes(), nil
    }

    var (
        // Total voting power of all vote extensions.
        totalVP int64
        // Total voting power of all validators that submitted valid vote extensions.
        sumVP int64
    )
    [...]
}
```

**Example 3: Key typo may allow store corruption** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/key-typo-may-allow-store-corruption.md`
```go
var (
	// Keys for store prefixes
	// Last* values are constant during a block.
	LastValidatorPowerKey = []byte{0x11} // prefix for each key to a validator index, for bonded validators
	LastTotalPowerKey     = []byte{0x12} // prefix for the total power

	ValidatorsKey             = []byte{0x21} // prefix for each key to a validator
	ValidatorsByConsAddrKey   = []byte{0x22} // prefix for each key to a validator index, by pubkey
	ValidatorsByPowerIndexKey = []byte{0x23} // prefix for each key to a validator index, sorted by power

	DelegationKey                    = []byte{0x31} // key for a delegation
	UnbondingDelegationKey           = []byte{0x32} // key for an unbonding-delegation
	UnbondingDelegationByValIndexKey = []byte{0x33} // prefix for each key for an unbonding-delegation, by validator operator
	RedelegationKey                  = []byte{0x34} // key for a redelegation
	RedelegationByValSrcIndexKey     = []byte{0x35} // prefix for each key for an redelegation, by source validator operator
	RedelegationByValDstIndexKey     = []byte{0x36} // prefix for each key for an redelegation, by destination validator operator
	PeriodDelegationKey              = []byte{0x37} // key for a period delegation

	UnbondingIDKey    = []byte{0x37} // key for the counter for the incrementing id for UnbondingOperations
	UnbondingIndexKey = []byte{0x38} // prefix for an index for looking up unbonding operations by their IDs
	UnbondingTypeKey  = []byte{0x39} // prefix for an index containing the type of unbonding operations

	UnbondingQueueKey    = []byte{0x41} // prefix for the timestamps in unbonding queue
	RedelegationQueueKey = []byte{0x42} // prefix for the timestamps in redelegations queue
	ValidatorQueueKey    = []byte{0x43} // prefix for the timestamps in validator queue

	HistoricalInfoKey   = []byte{0x50} // prefix for the historical info
	ValidatorUpdatesKey = []byte{0x61} // prefix for the end block validator updates key

	ParamsKey = []byte{0x51} // prefix for parameters for module x/staking

	DelegationByValIndexKey = []byte{0x71} // key for delegations by a validator
)
```

**Example 4: [M-01] Missing check in the `updateValset` function** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-01-missing-check-in-the-updatevalset-function.md`
```
// Vulnerable pattern from Cudos:
[Gravity.sol#L276-L358](https://github.com/code-423n4/2022-05-cudos/blob/de39cf3cd1f1e1cf211819b06d4acf6a043acda0/solidity/contracts/Gravity.sol#L276-L358)<br>

The `updateValset` function don't check that the sum of the powers of the new validators in the new valset is greater than the threshold, which can lead to unwanted behavior.

There are 2 main problems that can occur in that situation:

1.  The sum of the new validators' powers will be lower than the `state_powerThreshold`
2.  The sum of
```

**Example 5: Attacker will manipulate voting power calculations as `getOperatorVotingPower()`** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-1-attacker-will-manipulate-voting-power-calculations-as-getoperatorvotingpower.md`
```go
// Add vault validation
if (!isSharedVaultRegistered(vault) && !isOperatorVaultRegistered(vault)) {
    return 0;
}
```

**Variant: Validator Set Manipulation - MEDIUM Severity Cases** [MEDIUM]
> Found in 6 reports:
> - `reports/cosmos_cometbft_findings/m-01-missing-check-in-the-updatevalset-function.md`
> - `reports/cosmos_cometbft_findings/m-1-attacker-will-manipulate-voting-power-calculations-as-getoperatorvotingpower.md`
> - `reports/cosmos_cometbft_findings/m-14-votesupgradeabledelegate-bypasses-the-addvalidator-call-leads-to-a-non-vali.md`

**Variant: Validator Set Manipulation in Ethos Cosmos** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/incorrect-injected-vote-extensions-validation.md`
> - `reports/cosmos_cometbft_findings/lack-of-signature-verification.md`

**Variant: Validator Set Manipulation in Cosmos SDK** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/key-typo-may-allow-store-corruption.md`
> - `reports/cosmos_cometbft_findings/vote-extension-risks.md`

**Variant: Validator Set Manipulation in Symbiotic Relay** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-1-attacker-will-manipulate-voting-power-calculations-as-getoperatorvotingpower.md`
> - `reports/cosmos_cometbft_findings/m-7-a-malicious-operator-will-control-consensus-without-risking-stake-stake-exit.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in validator set manipulation logic allows exploitation through missing validati
func secureValidatorSetManipulation(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 6, MEDIUM: 6
- **Affected Protocols**: Cudos, Symbiotic Relay, Virtuals Protocol, Skip Slinky Oracle, Ethos Cosmos
- **Validation Strength**: Strong (3+ auditors)

---

## 4. Validator Key Rotation

### Overview

Implementation flaw in validator key rotation logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: HIGH: 1, MEDIUM: 2.

> **Key Finding**: This bug report describes a vulnerability in the ProviderRegistry.sol and BlockTracker.sol contracts. The issue allows a malicious user to register as a provider and overwrite the blockBuilderBLSKeyToAddress[] mapping, which can lead to the loss of funds for honest providers. This vulnerability can 

### Vulnerability Description

#### Root Cause

Implementation flaw in validator key rotation logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies validator key rotation in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to validator operations

### Vulnerable Pattern Examples

**Example 1: blockBuilderBLSKeyToAddress[] can be overwritten in ProviderRegistry.sol::_regis** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/blockbuilderblskeytoaddress-can-be-overwritten-in-providerregistrysol_registeran.md`
```solidity
function _registerAndStake(address provider, bytes[] calldata blsPublicKeys) internal {
    require(!providerRegistered[provider], ProviderAlreadyRegistered(provider));
    require(msg.value >= minStake, InsufficientStake(msg.value, minStake));
    require(blsPublicKeys.length != 0, AtLeastOneBLSKeyRequired());
    
    uint256 numKeys = blsPublicKeys.length;
    for (uint256 i = 0; i < numKeys; ++i) {
        bytes memory key = blsPublicKeys[i];
        require(key.length == 48, InvalidBLSPublicKeyLength(key.length, 48));
        blockBuilderBLSKeyToAddress[key] = provider; // <<<
    }

    eoaToBlsPubkeys[provider] = blsPublicKeys;
    providerStakes[provider] = msg.value;
    providerRegistered[provider] = true;
    emit ProviderRegistered(provider, msg.value, blsPublicKeys);
}
```

**Example 2: [M-03] `xfeemarket` module is not wired up, resulting in non-working CLI command** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-03-xfeemarket-module-is-not-wired-up-resulting-in-non-working-cli-commands-mes.md`
```go
308: keys := storetypes.NewKVStoreKeys(
309: 	authtypes.StoreKey, banktypes.StoreKey, stakingtypes.StoreKey, crisistypes.StoreKey,
310: 	minttypes.StoreKey, distrtypes.StoreKey, slashingtypes.StoreKey,
311: 	govtypes.StoreKey, paramstypes.StoreKey, consensusparamtypes.StoreKey, upgradetypes.StoreKey, feegrant.StoreKey,
312: 	evidencetypes.StoreKey,
313: 	circuittypes.StoreKey,
314: 	authzkeeper.StoreKey,
315: 	nftkeeper.StoreKey,
316: 	group.StoreKey,
317: 	// non sdk store keys
318: 	capabilitytypes.StoreKey, ibcexported.StoreKey, ibctransfertypes.StoreKey, ibcfeetypes.StoreKey,
319: 	wasmtypes.StoreKey,
320: 	ratelimittypes.StoreKey,
321: 	tokenfactorytypes.StoreKey, taxtypes.StoreKey,
322: 	ibchookstypes.StoreKey,
323: 	feemarkettypes.StoreKey, oracletypes.StoreKey, marketmaptypes.StoreKey,
324: )
```

**Example 3: Potential To Rotate Consensus Key Back To Initial Key** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/potential-to-rotate-consensus-key-back-to-initial-key.md`
```go
func (k msgServer) RotateConsPubKey(ctx context.Context, msg *types.MsgRotateConsPubKey) (res *types.MsgRotateConsPubKeyResponse, err error) {
	// check cons key is already present in the key rotation history.
	rotatedTo, err := k.NewToOldConsKeyMap.Get(ctx, pk.Address())
	if err != nil && !errors.Is(err, collections.ErrNotFound) {
		return nil, err
	}
	if rotatedTo != nil {
		return nil, errorsmod.Wrap(sdkerrors.ErrInvalidAddress, "the new public key is already present in rotation history, please try with a different one")
	}
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in validator key rotation logic allows exploitation through missing validation, 
func secureValidatorKeyRotation(ctx sdk.Context) error {
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
- **Affected Protocols**: MANTRA, Primev, Cosmos SDK V3
- **Validation Strength**: Strong (3+ auditors)

---

## 5. Validator Commission Exploit

### Overview

Implementation flaw in validator commission exploit logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: MEDIUM: 2.

> **Key Finding**: The bug report discusses an issue with registered validators being able to drastically increase their commission percentage at any time. This can result in them profiting from a large commission for a long period of time, as the stakes are locked for 30 days. The report suggests implementing a simil

### Vulnerability Description

#### Root Cause

Implementation flaw in validator commission exploit logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies validator commission exploit in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to validator operations

### Vulnerable Pattern Examples

**Example 1: Validators can Manipulate Commission Rates** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/validators-can-manipulate-commission-rates.md`
```go
public entry fun change_commission(
    pool_owner: &signer,
    new_default_commission: u64,
    new_protocol_commission: u64,
) acquires ManagedStakePool {
    [...]
    assert_pool_exists(managed_pool_address);
    [...]
    assert!(
        new_default_commission <= managed_stake_pool.max_commission,
        error::invalid_argument(ECOMMISSION_EXCEEDS_MAX)
    );
    // (Input Assert, keep)
    assert!(
        new_protocol_commission <= new_default_commission,
        error::invalid_argument(EPROTOCOL_COMMISSION_EXCEEDS_DEFAULT)
    );
    [...]
    delegation_state::change_commission_internal(
        managed_pool_address,
        new_default_commission,
        new_protocol_commission,
    );
}
```

**Example 2: Validators Manipulating Commission Rates** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/validators-manipulating-commission-rates.md`
```go
public entry fun change_commission(
    pool_owner: &signer,
    new_default_commission: u64,
    new_protocol_commission: u64,
) acquires ManagedStakePool {
    [...]
    assert_pool_exists(managed_pool_address);
    [...]
    assert!(
        new_default_commission <= managed_stake_pool.max_commission,
        error::invalid_argument(ECOMMISSION_EXCEEDS_MAX)
    );
    // (Input Assert, keep)
    assert!(
        new_protocol_commission <= new_default_commission,
        error::invalid_argument(EPROTOCOL_COMMISSION_EXCEEDS_DEFAULT)
    );
    [...]
    delegation_state::change_commission_internal(
        managed_pool_address,
        new_default_commission,
        new_protocol_commission,
    );
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in validator commission exploit logic allows exploitation through missing valida
func secureValidatorCommissionExploit(ctx sdk.Context) error {
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
- **Severity Distribution**: MEDIUM: 2
- **Affected Protocols**: Tortuga, Tortugal TIP
- **Validation Strength**: Single auditor

---

## 6. Validator Status Transition

### Overview

Implementation flaw in validator status transition logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 4 audit reports with severity distribution: HIGH: 2, MEDIUM: 2.

> **Key Finding**: The initializeDeposit function in the StakeManager contract allows validators and delegators to deposit resources for validating nodes. However, the function does not check if the validator is active before accepting the deposit, leading to locked stakes and the inability to withdraw them. This bug 

### Vulnerability Description

#### Root Cause

Implementation flaw in validator status transition logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies validator status transition in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to validator operations

### Vulnerable Pattern Examples

**Example 1: Deposited Stakes Can Be Locked in StakeManager if the Validator Is Inactive** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/deposited-stakes-can-be-locked-in-stakemanager-if-the-validator-is-inactive.md`
```
// Vulnerable pattern from FCHAIN Validator and Staking Contracts Audit:
The [`initializeDeposit` function](https://github.com/0xFFoundation/fchain-contracts/blob/11ffd45bc95747b8d2432a2e8bb120d4a1dc19a2/src/StakeManager.sol#L303) is designed to accept licenses and staking amounts as stakes for a validating node within the system. This function can be called by the validators to increase their own weight or by delegators to increase the weight of their delegated validator. However, the function does not validate the active status of a validator before proceeding with
```

**Example 2: [M-04] New stakes delegated even when validator is inactive** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-04-new-stakes-delegated-even-when-validator-is-inactive.md`
```go
if (amount > 0) {
            address delegateTo = validatorManager.getDelegation(address(this));
            require(delegateTo != address(0), "No delegation set");

            // Send tokens to delegation
            l1Write.sendTokenDelegate(delegateTo, uint64(amount), false);

            emit Delegate(delegateTo, amount);
        }
```

**Example 3: [PRST-4] Unbonding of validators does not give priority to inactive validators** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/prst-4-unbonding-of-validators-does-not-give-priority-to-inactive-validators.md`
```
// Vulnerable pattern from Persistence:
**Severity:** Medium

**Path:** x/liquidstake/keeper/liquidstake.go:LiquidUnstake#L344-L459

**Description:**

When a user wants to withdraw their `stkXPRT` for `xprt`, they will call `LiquidUnstake`. In the function, the module will back out delegations for each validator according to their weight for a total of the unbonding amount. The module takes the whole set of validators and does not check their active status.

By not giving priority to unbonding inactive validators first, it will furthe
```

**Example 4: Validator State Desynchronization** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/validator-state-desynchronization.md`
```
// Vulnerable pattern from Jito Steward:
## Issue with Validator Removal and State Desynchronization

Removing validators immediately after a successful `EpochMaintenance` may result in the desynchronization of the internal state of the Steward Program with the external state of the stake pool validator list, particularly when handling delinquent validators. A validator may be removed from the list in the same epoch if there is no transient stake. 

The issue arises because the validator is marked for deactivation in one epoch but is n
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in validator status transition logic allows exploitation through missing validat
func secureValidatorStatusTransition(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 2, MEDIUM: 2
- **Affected Protocols**: Jito Steward, Persistence, FCHAIN Validator and Staking Contracts Audit, Kinetiq_2025-02-26
- **Validation Strength**: Strong (3+ auditors)

---

## 7. Validator Dust Collateral

### Overview

Implementation flaw in validator dust collateral logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 4 audit reports with severity distribution: HIGH: 3, MEDIUM: 1.

> **Key Finding**: The bug report discusses a potential issue with the BorrowerOperations and LiquidationLibrary contracts in the protocol. When the value of collateral in a CDP (collateralized debt position) falls below a certain threshold, it allows for the creation of "dust CDPs" where the collateral and debt amoun

### Vulnerability Description

#### Root Cause

Implementation flaw in validator dust collateral logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies validator dust collateral in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to validator operations

### Vulnerable Pattern Examples

**Example 1: Allowing the creation of "dust CDPs" could lead redeemers/liquidators to be not ** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/allowing-the-creation-of-dust-cdps-could-lead-redeemersliquidators-to-be-not-pro.md`
```go
collateral.getSharesByPooledEth((singleRedemption.eBtcToRedeem * DECIMAL_PRECISION) / _redeemColFromCdp._price)
```

**Example 2: Dust limit attack on `forceUpdateNodes` allows DoS of rebalancing and potential ** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/dust-limit-attack-on-forceupdatenodes-allows-dos-of-rebalancing-and-potential-va.md`
```
// Vulnerable pattern from Suzaku Core:
**Description:** An attacker can exploit the `forceUpdateNodes()` function with minimal `limitStake` values to force all validator nodes into a pending update state. By exploiting precision loss in stake-to-weight conversion, an attacker can call `forceUpdateNodes` with a minimal limitStake (e.g., 1 wei), which sets the rebalancing flag without actually reducing any stake, effectively blocking legitimate rebalancing for the entire epoch.

Consider following scenario:
- Large vault undelegation r
```

**Example 3: [M-17] Bad debt can be permanently blocked from being moved to backstop** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-17-bad-debt-can-be-permanently-blocked-from-being-moved-to-backstop.md`
```go
if !user_state.positions.collateral.is_empty() || user_state.positions.liabilities.is_empty() {
        panic_with_error!(e, PoolError::BadRequest);
    }
```

**Example 4: Validators with dust collateral can join the network** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/validators-with-dust-collateral-can-join-the-network.md`
```solidity
function depositWithConfirm(address validator, uint256 amount) internal {
        ...
        if (!s.bootstrapped) {
            // add to initial validators avoiding duplicates if it
            // is a genesis validator.
            bool alreadyValidator;
            uint256 length = s.genesisValidators.length;
            for (uint256 i; i < length; ) {
                if (s.genesisValidators[i].addr == validator) {
                    alreadyValidator = true;
                    break;
                }
                unchecked {
                    ++i;
                }
            }
            if (!alreadyValidator) {
                uint256 collateral = s.validatorSet.validators[validator].confirmedCollateral;
                Validator memory val = Validator({
                    addr: validator,
                    weight: collateral,
                    metadata: s.validatorSet.validators[validator].metadata
                });
                s.genesisValidators.push(val);
            }
        }
    }
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in validator dust collateral logic allows exploitation through missing validatio
func secureValidatorDustCollateral(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 3, MEDIUM: 1
- **Affected Protocols**: Suzaku Core, Blend, Interplanetary Consensus (Ipc), BadgerDAO
- **Validation Strength**: Strong (3+ auditors)

---

## 8. Validator Score Manipulation

### Overview

Implementation flaw in validator score manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 19 audit reports with severity distribution: HIGH: 9, MEDIUM: 10.

> **Key Finding**: This bug report discusses an issue with the Berachef.sol#158 code, where a validator operator can queue a new cutting board at any time and activate it after a certain delay. However, this system can be manipulated by a malicious validator by publicly queueing a cutting board to attract BGT stakes f

### Vulnerability Description

#### Root Cause

Implementation flaw in validator score manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies validator score manipulation in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to validator operations

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

**Example 2: COIN DENOMINATION IS NOT CHECKED WHEN REMOVING VALIDATORS** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/coin-denomination-is-not-checked-when-removing-validators.md`
```go
for i in 0..delegations.len() {
 if delegations[i].is_zero() {
  continue;
 }
 redelegations.push((
  validators[i].address.clone(),
  Coin::new(delegations[i].u128(), delegation.amount.denom.as_str()),
 ));
}
```

**Example 3: Deposited Stakes Can Be Locked in StakeManager if the Validator Is Inactive** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/deposited-stakes-can-be-locked-in-stakemanager-if-the-validator-is-inactive.md`
```
// Vulnerable pattern from FCHAIN Validator and Staking Contracts Audit:
The [`initializeDeposit` function](https://github.com/0xFFoundation/fchain-contracts/blob/11ffd45bc95747b8d2432a2e8bb120d4a1dc19a2/src/StakeManager.sol#L303) is designed to accept licenses and staking amounts as stakes for a validating node within the system. This function can be called by the validators to increase their own weight or by delegators to increase the weight of their delegated validator. However, the function does not validate the active status of a validator before proceeding with
```

**Example 4: Dust limit attack on `forceUpdateNodes` allows DoS of rebalancing and potential ** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/dust-limit-attack-on-forceupdatenodes-allows-dos-of-rebalancing-and-potential-va.md`
```
// Vulnerable pattern from Suzaku Core:
**Description:** An attacker can exploit the `forceUpdateNodes()` function with minimal `limitStake` values to force all validator nodes into a pending update state. By exploiting precision loss in stake-to-weight conversion, an attacker can call `forceUpdateNodes` with a minimal limitStake (e.g., 1 wei), which sets the rebalancing flag without actually reducing any stake, effectively blocking legitimate rebalancing for the entire epoch.

Consider following scenario:
- Large vault undelegation r
```

**Example 5: [H-01] Lack of access control in `AgentNftV2::addValidator()` enables unauthoriz** [HIGH]
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

**Variant: Validator Score Manipulation - HIGH Severity Cases** [HIGH]
> Found in 9 reports:
> - `reports/cosmos_cometbft_findings/deposited-stakes-can-be-locked-in-stakemanager-if-the-validator-is-inactive.md`
> - `reports/cosmos_cometbft_findings/dust-limit-attack-on-forceupdatenodes-allows-dos-of-rebalancing-and-potential-va.md`
> - `reports/cosmos_cometbft_findings/h-01-lack-of-access-control-in-agentnftv2addvalidator-enables-unauthorized-valid.md`

**Variant: Validator Score Manipulation in Protocol** [MEDIUM]
> Protocol-specific variant found in 4 reports:
> - `reports/cosmos_cometbft_findings/coin-denomination-is-not-checked-when-removing-validators.md`
> - `reports/cosmos_cometbft_findings/inadequate-tracking-of-pending-redelegations.md`
> - `reports/cosmos_cometbft_findings/redelegation-is-not-restricted-to-active-validators.md`

**Variant: Validator Score Manipulation in FCHAIN Validator and Staking Contracts Audit** [HIGH]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/deposited-stakes-can-be-locked-in-stakemanager-if-the-validator-is-inactive.md`
> - `reports/cosmos_cometbft_findings/locked-in-licenses-can-be-transferred.md`
> - `reports/cosmos_cometbft_findings/potential-stake-lock-and-inconsistency-due-to-validator-state-transitions.md`

**Variant: Validator Score Manipulation in Suzaku Core** [HIGH]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/dust-limit-attack-on-forceupdatenodes-allows-dos-of-rebalancing-and-potential-va.md`
> - `reports/cosmos_cometbft_findings/immediate-stake-cache-updates-enable-reward-distribution-without-p-chain-confirm.md`
> - `reports/cosmos_cometbft_findings/operator-can-over-allocate-the-same-stake-to-unlimited-nodes-within-one-epoch-ca.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in validator score manipulation logic allows exploitation through missing valida
func secureValidatorScoreManipulation(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 9, MEDIUM: 10
- **Affected Protocols**: Protocol, Skip Slinky Oracle, Virtuals Protocol, Dria, Berachain Pol
- **Validation Strength**: Strong (3+ auditors)

---

## 9. Validator Operator Mismatch

### Overview

Implementation flaw in validator operator mismatch logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: HIGH: 1, MEDIUM: 2.

> **Key Finding**: This bug report is about a possible security flaw in Swell Network's staking system. If a node operator interacts with the deposit contract directly first, they can set the withdrawal address to an arbitrary address. This means that once deposits are enabled on the Beacon chain, it is possible for t

### Vulnerability Description

#### Root Cause

Implementation flaw in validator operator mismatch logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies validator operator mismatch in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to validator operations

### Vulnerable Pattern Examples

**Example 1: Direct Deposits Enable Theft Of A Validator’s Funds** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/direct-deposits-enable-theft-of-a-validators-funds.md`
```
// Vulnerable pattern from Swell:
## Description

If a node operator interacts with the deposit contract directly first, it is possible for them to set the withdrawal address to an arbitrary address. Then this node can be added to Swell and used normally. Once deposits are enabled on the Beacon chain, it is possible for this node operator to withdraw all the ETH deposited with this node. In addition to this, it is impossible for the normal withdrawal method specified by `swNFTUpgrade.sol` to work for deposits made to this node.

```

**Example 2: Historical reward loss due to `NodeId` reuse in `AvalancheL1Middleware`** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/historical-reward-loss-due-to-nodeid-reuse-in-avalanchel1middleware.md`
```
// Vulnerable pattern from Suzaku Core:
**Description:** The `AvalancheL1Middleware` contract is vulnerable to misattributing stake to a former operator (Operator A) if a new, colluding or coordinated operator (Operator B) intentionally re-registers a node using the *exact same `bytes32 nodeId`* that Operator A previously used. This scenario assumes Operator B is aware of Operator A's historical `nodeId` and that the underlying P-Chain NodeID (`P_X`, derived from the shared `bytes32 nodeId`) has become available for re-registration on
```

**Example 3: Node Operator Rewards Unevenly Leaked** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/node-operator-rewards-unevenly-leaked.md`
```go
uint256 perValReward = _totalReward.div(effectiveStakeTotal);
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in validator operator mismatch logic allows exploitation through missing validat
func secureValidatorOperatorMismatch(ctx sdk.Context) error {
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
- **Affected Protocols**: Suzaku Core, Lido, Swell
- **Validation Strength**: Moderate (2 auditors)

---

## 10. Validator Can Skip Exit

### Overview

Implementation flaw in validator can skip exit logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 2.

> **Key Finding**: The Cosmos AnteHandlers are used to check the validity of transactions and prevent malicious transactions from being executed. However, some of the validators are skipped when not in CheckTx mode, allowing attackers to insert malformed transactions into block proposals. This can lead to incorrect ex

### Vulnerability Description

#### Root Cause

Implementation flaw in validator can skip exit logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies validator can skip exit in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to validator operations

### Vulnerable Pattern Examples

**Example 1: AnteHandler Skipped In Non-CheckTx Mode** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/antehandler-skipped-in-non-checktx-mode.md`
```go
// sei-tendermint/internal/mempool/mempool.go
func (fc EVMFeeCheckDecorator) AnteHandle(ctx sdk.Context, tx sdk.Tx, simulate bool, next sdk.AnteHandler) (sdk.Context, error) {
    // Only check fee in CheckTx (similar to normal Sei tx)
    if !ctx.IsCheckTx() || simulate {
        return next(ctx, tx, simulate)
    }
    [...]
    anteCharge := txData.Cost()
    senderEVMAddr := evmtypes.MustGetEVMTransactionMessage(tx).Derived.SenderEVMAddr
    if state.NewDBImpl(ctx, fc.evmKeeper, true).GetBalance(senderEVMAddr).Cmp(anteCharge) < 0 {
        return ctx, sdkerrors.ErrInsufficientFunds
    }
    [...]
}
```

**Example 2: Validators Can Skip createEndRequest and Quickly Re-Register** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/validators-can-skip-createendrequest-and-quickly-re-register.md`
```
// Vulnerable pattern from FCHAIN Validator and Staking Contracts Audit:
[Within the ACP-77 specification](https://github.com/avalanche-foundation/ACPs/blob/main/ACPs/77-reinventing-subnets/README.md#registerl1validatortx), it is identified that a validator can only be registered once:

> *When it is known that a given validationID is not and never will be registered, the P-Chain must be willing to sign an L1ValidatorRegistrationMessage for the validationID with registered set to false. This could be the case if the expiry time of the message has passed prior to the 
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in validator can skip exit logic allows exploitation through missing validation,
func secureValidatorCanSkipExit(ctx sdk.Context) error {
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
- **Affected Protocols**: Sei EVM, FCHAIN Validator and Staking Contracts Audit
- **Validation Strength**: Moderate (2 auditors)

---

## 11. Validator Governance Power

### Overview

Implementation flaw in validator governance power logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: MEDIUM: 2.

> **Key Finding**: In EigenLayer, a staker's balance on the Beacon chain can fall below the minimum restaked amount per validator. If this happens, their shares are decreased by the restaked amount. The staker can then plan a withdrawal, and the deducted shares will be credited back. However, if the staker has delegat

### Vulnerability Description

#### Root Cause

Implementation flaw in validator governance power logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies validator governance power in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to validator operations

### Vulnerable Pattern Examples

**Example 1: [M-01] A staker with verified over-commitment can potentially bypass slashing co** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-01-a-staker-with-verified-over-commitment-can-potentially-bypass-slashing-comp.md`
```
// Vulnerable pattern from EigenLayer:
<https://github.com/code-423n4/2023-04-eigenlayer/blob/5e4872358cd2bda1936c29f460ece2308af4def6/src/contracts/core/StrategyManager.sol#L197>
<br><https://github.com/code-423n4/2023-04-eigenlayer/blob/5e4872358cd2bda1936c29f460ece2308af4def6/src/contracts/core/StrategyManager.sol#L513>

In EigenLayer, watchers submit over-commitment proof in the event a staker's balance on the Beacon chain falls below the minimum restaked amount per validator. In such a scenario, stakers' shares are [decreased by
```

**Example 2: [M03] Users can avoid some slashing penalties by front-running** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m03-users-can-avoid-some-slashing-penalties-by-front-running.md`
```
// Vulnerable pattern from Celo Contracts Audit:
The `slash` function of the `LockedGold` contract is called whenever any type of slashing occurs. It will [decrement the account’s non-voting locked gold balance](https://github.com/celo-org/celo-monorepo/blob/7be22605e172ca536c028e408b147aab83202e4a/packages/protocol/contracts/governance/LockedGold.sol#L319), as well as [the accounts’ active and pending votes](https://github.com/celo-org/celo-monorepo/blob/7be22605e172ca536c028e408b147aab83202e4a/packages/protocol/contracts/governance/LockedGol
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in validator governance power logic allows exploitation through missing validati
func secureValidatorGovernancePower(ctx sdk.Context) error {
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
- **Severity Distribution**: MEDIUM: 2
- **Affected Protocols**: Celo Contracts Audit, EigenLayer
- **Validation Strength**: Moderate (2 auditors)

---

## Detection Patterns

### Automated Detection
```
# Validator Registration Bypass
grep -rn 'validator|registration|bypass' --include='*.go' --include='*.sol'
# Validator Removal Failure
grep -rn 'validator|removal|failure' --include='*.go' --include='*.sol'
# Validator Set Manipulation
grep -rn 'validator|set|manipulation' --include='*.go' --include='*.sol'
# Validator Key Rotation
grep -rn 'validator|key|rotation' --include='*.go' --include='*.sol'
# Validator Commission Exploit
grep -rn 'validator|commission|exploit' --include='*.go' --include='*.sol'
# Validator Status Transition
grep -rn 'validator|status|transition' --include='*.go' --include='*.sol'
# Validator Dust Collateral
grep -rn 'validator|dust|collateral' --include='*.go' --include='*.sol'
# Validator Score Manipulation
grep -rn 'validator|score|manipulation' --include='*.go' --include='*.sol'
# Validator Operator Mismatch
grep -rn 'validator|operator|mismatch' --include='*.go' --include='*.sol'
# Validator Can Skip Exit
grep -rn 'validator|can|skip|exit' --include='*.go' --include='*.sol'
```

## Keywords

`absence`, `access`, `accounting`, `activation`, `allow`, `allowing`, `allows`, `antehandler`, `appchain`, `argmaxblockbystake`, `attack`, `avoid`, `back`, `backstop`, `being`, `blame`, `block`, `blocked`, `board`, `bypass`, `can`, `cannot`, `causes`, `channel`, `check`, `checked`, `coin`, `collateral`, `commission`, `completely`
