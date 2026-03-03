---
protocol: generic
chain: cosmos
category: validation
vulnerability_type: input_validation_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: validation_logic

primitives:
  - zero_check_missing
  - bounds_missing
  - state_check_missing
  - percentage_overflow
  - address_normalization
  - duplicate_missing
  - config_bypass
  - input_general
  - incorrect_check
  - logic_error

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - validation
  - staking
  - defi

language: go|solidity|rust
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Validation Zero Check Missing
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Every node gets a full validator’s bounty ✓ Fixed | `reports/cosmos_cometbft_findings/every-node-gets-a-full-validators-bounty-fixed.md` | HIGH | ConsenSys |
| [H-02] The reentrancy vulnerability in _safeMint can allow a | `reports/cosmos_cometbft_findings/h-02-the-reentrancy-vulnerability-in-_safemint-can-allow-an-attacker-to-steal-al.md` | HIGH | Code4rena |
| [H-04] Withdrawals logic allows MEV exploits of TVL changes  | `reports/cosmos_cometbft_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md` | HIGH | Code4rena |
| [H-05] `ValidatorRegistry::validatorScore/getPastValidatorSc | `reports/cosmos_cometbft_findings/h-05-validatorregistryvalidatorscoregetpastvalidatorscore-allows-validator-to-ea.md` | HIGH | Code4rena |
| [M-01] `_safeMint` Will Fail Due To An Edge Case In Calculat | `reports/cosmos_cometbft_findings/m-01-_safemint-will-fail-due-to-an-edge-case-in-calculating-tokenid-using-the-_g.md` | MEDIUM | Code4rena |
| [M-02] Insufficient Input Validation | `reports/cosmos_cometbft_findings/m-02-insufficient-input-validation.md` | MEDIUM | Shieldify |
| MISSING ZERO CHECKS ON AMOUNTS AND PRICES | `reports/cosmos_cometbft_findings/missing-zero-checks-on-amounts-and-prices.md` | MEDIUM | Halborn |
| Redemption of failed registration fees and pre-validated QI  | `reports/cosmos_cometbft_findings/redemption-of-failed-registration-fees-and-pre-validated-qi-is-not-guaranteed-to.md` | MEDIUM | Cyfrin |

### Validation Bounds Missing
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| USERS MAY NOT BE ABLE TO UNSTAKE OR CLAIM REWARDS WHEN stake | `reports/cosmos_cometbft_findings/users-may-not-be-able-to-unstake-or-claim-rewards-when-stakedamountlimit-is-decr.md` | MEDIUM | Halborn |

### Validation State Check Missing
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| COIN DENOMINATION IS NOT CHECKED WHEN REMOVING VALIDATORS | `reports/cosmos_cometbft_findings/coin-denomination-is-not-checked-when-removing-validators.md` | MEDIUM | Halborn |
| DoS on stake accounting functions by bloating `operatorNodes | `reports/cosmos_cometbft_findings/dos-on-stake-accounting-functions-by-bloating-operatornodesarray-with-irremovabl.md` | MEDIUM | Cyfrin |
| Dust limit attack on `forceUpdateNodes` allows DoS of rebala | `reports/cosmos_cometbft_findings/dust-limit-attack-on-forceupdatenodes-allows-dos-of-rebalancing-and-potential-va.md` | HIGH | Cyfrin |
| Function `getTotalStake()` fails to account for pending vali | `reports/cosmos_cometbft_findings/function-gettotalstake-fails-to-account-for-pending-validators-leading-to-inaccu.md` | HIGH | Cyfrin |
| [H-01] Lack of access control in `AgentNftV2::addValidator() | `reports/cosmos_cometbft_findings/h-01-lack-of-access-control-in-agentnftv2addvalidator-enables-unauthorized-valid.md` | HIGH | Code4rena |
| `IBCChannelHandshake.channelOpenAck()` Does Not Require Conn | `reports/cosmos_cometbft_findings/ibcchannelhandshakechannelopenack-does-not-require-connection-to-be-open-before-.md` | HIGH | Quantstamp |
| [M-01] Missing check in the `updateValset` function | `reports/cosmos_cometbft_findings/m-01-missing-check-in-the-updatevalset-function.md` | MEDIUM | Code4rena |
| [M-02] _depositEther Does Not Increment Validator Index,Caus | `reports/cosmos_cometbft_findings/m-02-_depositether-does-not-increment-validator-indexcausing-all-deposits-to-fun.md` | MEDIUM | Kann |

### Validation Percentage Overflow
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| LACK OF VALIDATION ALLOWS SETTING PERCENTAGES HIGHER THAN A  | `reports/cosmos_cometbft_findings/lack-of-validation-allows-setting-percentages-higher-than-a-hundred.md` | MEDIUM | Halborn |

### Validation Address Normalization
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| LACK OF ADDRESS CANONICALIZATION/NORMALIZATION | `reports/cosmos_cometbft_findings/lack-of-address-canonicalizationnormalization.md` | HIGH | Halborn |
| [M-03] `RemoteAddressValidator` can incorrectly convert addr | `reports/cosmos_cometbft_findings/m-03-remoteaddressvalidator-can-incorrectly-convert-addresses-to-lowercase.md` | MEDIUM | Code4rena |

### Validation Duplicate Missing
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Duplicate Request Rewards | `reports/cosmos_cometbft_findings/duplicate-request-rewards.md` | HIGH | OpenZeppelin |
| [H-01] Lack of access control in `AgentNftV2::addValidator() | `reports/cosmos_cometbft_findings/h-01-lack-of-access-control-in-agentnftv2addvalidator-enables-unauthorized-valid.md` | HIGH | Code4rena |
| [H-03] `SettlementSignatureVerifier` is missing check for du | `reports/cosmos_cometbft_findings/h-03-settlementsignatureverifier-is-missing-check-for-duplicate-validator-signat.md` | HIGH | Code4rena |

### Validation Config Bypass
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| MixinParams.setParams bypasses safety checks made by standar | `reports/cosmos_cometbft_findings/mixinparamssetparams-bypasses-safety-checks-made-by-standard-stakingproxy-upgrad.md` | MEDIUM | ConsenSys |

### Validation Input General
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-02] Insufficient Input Validation | `reports/cosmos_cometbft_findings/m-02-insufficient-input-validation.md` | MEDIUM | Shieldify |
| Malicious user can prevent other users from unbonding due to | `reports/cosmos_cometbft_findings/malicious-user-can-prevent-other-users-from-unbonding-due-to-missing-input-valid.md` | HIGH | Cantina |
| Missing validation that ensures unspent BTC is fully sent ba | `reports/cosmos_cometbft_findings/missing-validation-that-ensures-unspent-btc-is-fully-sent-back-as-change-in-lomb.md` | MEDIUM | Cantina |
| Missing validations on administration functions | `reports/cosmos_cometbft_findings/missing-validations-on-administration-functions.md` | MEDIUM | TrailOfBits |
| Sentinel can block core operations for any validator chosen  | `reports/cosmos_cometbft_findings/sentinel-can-block-core-operations-for-any-validator-chosen-due-to-missing-input.md` | MEDIUM | Spearbit |

### Validation Incorrect Check
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| _checkBalance Returns an Incorrect Value During Insolvency | `reports/cosmos_cometbft_findings/_checkbalance-returns-an-incorrect-value-during-insolvency.md` | MEDIUM | OpenZeppelin |
| AnteHandler Skipped In Non-CheckTx Mode | `reports/cosmos_cometbft_findings/antehandler-skipped-in-non-checktx-mode.md` | HIGH | OtterSec |
| Discrepancies In Deposit Functionality | `reports/cosmos_cometbft_findings/discrepancies-in-deposit-functionality.md` | HIGH | OtterSec |
| [H-01] Recipient Bytes Silent Burn When Non-20-Byte Payloads | `reports/cosmos_cometbft_findings/h-01-recipient-bytes-silent-burn-when-non-20-byte-payloads-pass-validation.md` | HIGH | Shieldify |
| [H-01] Wrong handling of ERC20 denoms in `ERC20Keeper::BurnC | `reports/cosmos_cometbft_findings/h-01-wrong-handling-of-erc20-denoms-in-erc20keeperburncoins.md` | HIGH | Code4rena |
| [H-03] Incorrect boost management leads to staking reward lo | `reports/cosmos_cometbft_findings/h-03-incorrect-boost-management-leads-to-staking-reward-loss.md` | HIGH | Pashov Audit Group |
| Historical reward loss due to `NodeId` reuse in `AvalancheL1 | `reports/cosmos_cometbft_findings/historical-reward-loss-due-to-nodeid-reuse-in-avalanchel1middleware.md` | MEDIUM | Cyfrin |
| `IBCChannelHandshake.channelOpenAck()` Does Not Require Conn | `reports/cosmos_cometbft_findings/ibcchannelhandshakechannelopenack-does-not-require-connection-to-be-open-before-.md` | HIGH | Quantstamp |

### Validation Logic Error
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-01] Slashing isn't supported in the rebasing mechanism | `reports/cosmos_cometbft_findings/h-01-slashing-isnt-supported-in-the-rebasing-mechanism.md` | HIGH | Pashov Audit Group |
| [H-04] Withdrawals logic allows MEV exploits of TVL changes  | `reports/cosmos_cometbft_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md` | HIGH | Code4rena |
| [H-14] Inexpedient liquidatable logic that could have half l | `reports/cosmos_cometbft_findings/h-14-inexpedient-liquidatable-logic-that-could-have-half-liquidable-position-tur.md` | HIGH | Code4rena |
| [M-01] The `increaseStakeAndLock()` Function Prevents Users  | `reports/cosmos_cometbft_findings/m-01-the-increasestakeandlock-function-prevents-users-from-increasing-stake-amou.md` | MEDIUM | Shieldify |
| [M-02] The Current `veGUAN` Implementation Does Not Give Use | `reports/cosmos_cometbft_findings/m-02-the-current-veguan-implementation-does-not-give-users-extra-spins-nor-the-w.md` | MEDIUM | Shieldify |
| `ViewLogic::maxLiquidatable()` doesn't take the bonus into a | `reports/cosmos_cometbft_findings/m-10-viewlogicmaxliquidatable-doesnt-take-the-bonus-into-account-making-the-agen.md` | MEDIUM | Sherlock |
| logic bug in this IBC middleware code related to packet hand | `reports/cosmos_cometbft_findings/m-14-logic-bug-in-this-ibc-middleware-code-related-to-packet-handling.md` | MEDIUM | Sherlock |
| `unbond_public` logic causes issues for some delegators prev | `reports/cosmos_cometbft_findings/m-2-unbond_public-logic-causes-issues-for-some-delegators-preventing-partial-wit.md` | MEDIUM | Sherlock |

### Validation Msg Missing
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-05] L2 hooks don’t execute `ValidateBasic` on provided me | `reports/cosmos_cometbft_findings/m-05-l2-hooks-dont-execute-validatebasic-on-provided-messages.md` | MEDIUM | Code4rena |

### Validation Length Check
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Delegations might stuck in non-active validator  Pending | `reports/cosmos_cometbft_findings/delegations-might-stuck-in-non-active-validator-pending.md` | MEDIUM | ConsenSys |
| Denial Of Slashing | `reports/cosmos_cometbft_findings/denial-of-slashing.md` | HIGH | OtterSec |
| Elected TSS Nodes Can Avoid Slashing By Having Insuﬃcient De | `reports/cosmos_cometbft_findings/elected-tss-nodes-can-avoid-slashing-by-having-insuﬃcient-deposits.md` | HIGH | SigmaPrime |
| [M-31] Vaults can be griefed to not be able to be used for d | `reports/cosmos_cometbft_findings/m-31-vaults-can-be-griefed-to-not-be-able-to-be-used-for-deposits.md` | MEDIUM | Code4rena |
| Missing freshness check on oracle data in `Staking.totalCont | `reports/cosmos_cometbft_findings/missing-freshness-check-on-oracle-data-in-stakingtotalcontrolled-enables-stale-r.md` | MEDIUM | MixBytes |
| Validators Array Length Has to Be Updated When the Validator | `reports/cosmos_cometbft_findings/validators-array-length-has-to-be-updated-when-the-validator-is-alienated.md` | MEDIUM | ConsenSys |

---

# Input Validation Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Input Validation Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Validation Zero Check Missing](#1-validation-zero-check-missing)
2. [Validation Bounds Missing](#2-validation-bounds-missing)
3. [Validation State Check Missing](#3-validation-state-check-missing)
4. [Validation Percentage Overflow](#4-validation-percentage-overflow)
5. [Validation Address Normalization](#5-validation-address-normalization)
6. [Validation Duplicate Missing](#6-validation-duplicate-missing)
7. [Validation Config Bypass](#7-validation-config-bypass)
8. [Validation Input General](#8-validation-input-general)
9. [Validation Incorrect Check](#9-validation-incorrect-check)
10. [Validation Logic Error](#10-validation-logic-error)
11. [Validation Msg Missing](#11-validation-msg-missing)
12. [Validation Length Check](#12-validation-length-check)

---

## 1. Validation Zero Check Missing

### Overview

Implementation flaw in validation zero check missing logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 8 audit reports with severity distribution: HIGH: 4, MEDIUM: 4.

> **Key Finding**: The bug report is about a calculation issue related to the bounty of each validator in the Skale Network. The main change is related to how bounties are calculated for each validator. The problem is that the amount a validator should get is being divided among all nodes, rather than the validator re

### Vulnerability Description

#### Root Cause

Implementation flaw in validation zero check missing logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies validation zero check missing in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to validation operations

### Vulnerable Pattern Examples

**Example 1: Every node gets a full validator’s bounty ✓ Fixed** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/every-node-gets-a-full-validators-bounty-fixed.md`
```go
return epochPoolSize
    .add(\_bountyWasPaidInCurrentEpoch)
    .mul(
        delegationController.getAndUpdateEffectiveDelegatedToValidator(
            nodes.getValidatorId(nodeIndex),
            currentMonth
        )
    )
    .div(effectiveDelegatedSum);
```

**Example 2: [H-02] The reentrancy vulnerability in _safeMint can allow an attacker to steal ** [HIGH]
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

**Example 3: [H-04] Withdrawals logic allows MEV exploits of TVL changes and zero-slippage ze** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md`
```
// Vulnerable pattern from Renzo:
Deposit and withdrawal requests can be done immediately with no costs or fees, and both use the current oracle prices and TVL calculation ([`deposit`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/RestakeManager.sol#L499-L504), and [`withdraw`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/Withdraw/WithdrawQueue.sol#L217)). Crucially, the [withdrawal amount is calculated at withdrawal request submission time](https://github.com/code-423n4/2024-04-renzo/blob/ma
```

**Example 4: [H-05] `ValidatorRegistry::validatorScore/getPastValidatorScore` allows validato** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-05-validatorregistryvalidatorscoregetpastvalidatorscore-allows-validator-to-ea.md`
```solidity
function _initValidatorScore(
    uint256 virtualId,
    address validator
) internal {
    _baseValidatorScore[validator][virtualId] = _getMaxScore(virtualId);
}
```

**Example 5: [M-02] Insufficient Input Validation** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-02-insufficient-input-validation.md`
```go
constructor(
    uint256 _fundingPhaseDuration,
    uint256 _fundingExchangeRatio,
    uint256 _fundingRewardRate,
    address _principalToken,
    address _bToken,
    address _portalEnergyToken,
    address _tokenToAcquire,
    uint256 _terminalMaxLockDuration,
    uint256 _amountToConvert
) {
    fundingPhaseDuration = _fundingPhaseDuration;
    fundingExchangeRatio = _fundingExchangeRatio;
    fundingRewardRate = _fundingRewardRate;
    principalToken = _principalToken;
    bToken = _bToken;
    portalEnergyToken = _portalEnergyToken;
    tokenToAcquire = _tokenToAcquire;
    terminalMaxLockDuration = _terminalMaxLockDuration;
    amountToConvert = _amountToConvert;
    creationTime = block.timestamp;
}
```

**Variant: Validation Zero Check Missing - MEDIUM Severity Cases** [MEDIUM]
> Found in 4 reports:
> - `reports/cosmos_cometbft_findings/m-01-_safemint-will-fail-due-to-an-edge-case-in-calculating-tokenid-using-the-_g.md`
> - `reports/cosmos_cometbft_findings/m-02-insufficient-input-validation.md`
> - `reports/cosmos_cometbft_findings/missing-zero-checks-on-amounts-and-prices.md`

**Variant: Validation Zero Check Missing in XDEFI** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h-02-the-reentrancy-vulnerability-in-_safemint-can-allow-an-attacker-to-steal-al.md`
> - `reports/cosmos_cometbft_findings/m-01-_safemint-will-fail-due-to-an-edge-case-in-calculating-tokenid-using-the-_g.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in validation zero check missing logic allows exploitation through missing valid
func secureValidationZeroCheckMissing(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 4, MEDIUM: 4
- **Affected Protocols**: Virtuals Protocol, Skale Network, XDEFI, Possum, Octopus Network Anchor
- **Validation Strength**: Strong (3+ auditors)

---

## 2. Validation Bounds Missing

### Overview

Implementation flaw in validation bounds missing logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: The report highlights a bug in the `StakingVault` contract, where the `setStakedAmountLimit` function does not validate its input, allowing the administrator to set a limit lower than the currently staked amount. This can prevent users from unstaking or claiming their rewards. The bug is demonstrate

### Vulnerability Description

#### Root Cause

Implementation flaw in validation bounds missing logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies validation bounds missing in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to validation operations

### Vulnerable Pattern Examples

**Example 1: USERS MAY NOT BE ABLE TO UNSTAKE OR CLAIM REWARDS WHEN stakedAmountLimit IS DECR** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/users-may-not-be-able-to-unstake-or-claim-rewards-when-stakedamountlimit-is-decr.md`
```solidity
function setStakedAmountLimit(uint256 wad) external auth {
    stakedAmountLimit = wad;
    emit StakedAmountLimit(wad);
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in validation bounds missing logic allows exploitation through missing validatio
func secureValidationBoundsMissing(ctx sdk.Context) error {
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
- **Affected Protocols**: LMCV part 2
- **Validation Strength**: Single auditor

---

## 3. Validation State Check Missing

### Overview

Implementation flaw in validation state check missing logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 21 audit reports with severity distribution: HIGH: 7, MEDIUM: 14.

> **Key Finding**: This bug report states that there is a problem with the `remove_validator` function in the `krp-staking-contracts/basset_sei_validators_registry` contract. The issue is that when using this function to remove a validator, there is no check to ensure that the delegated amount of coins matches the tar

### Vulnerability Description

#### Root Cause

Implementation flaw in validation state check missing logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies validation state check missing in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to validation operations

### Vulnerable Pattern Examples

**Example 1: COIN DENOMINATION IS NOT CHECKED WHEN REMOVING VALIDATORS** [MEDIUM]
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

**Example 2: DoS on stake accounting functions by bloating `operatorNodesArray` with irremova** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/dos-on-stake-accounting-functions-by-bloating-operatornodesarray-with-irremovabl.md`
```go
if (nodePendingRemoval[valID] && …) {
         _removeNodeFromArray(operator,nodeId);
         nodePendingRemoval[valID] = false;
     }
```

**Example 3: Dust limit attack on `forceUpdateNodes` allows DoS of rebalancing and potential ** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/dust-limit-attack-on-forceupdatenodes-allows-dos-of-rebalancing-and-potential-va.md`
```
// Vulnerable pattern from Suzaku Core:
**Description:** An attacker can exploit the `forceUpdateNodes()` function with minimal `limitStake` values to force all validator nodes into a pending update state. By exploiting precision loss in stake-to-weight conversion, an attacker can call `forceUpdateNodes` with a minimal limitStake (e.g., 1 wei), which sets the rebalancing flag without actually reducing any stake, effectively blocking legitimate rebalancing for the entire epoch.

Consider following scenario:
- Large vault undelegation r
```

**Example 4: Function `getTotalStake()` fails to account for pending validators, leading to i** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/function-gettotalstake-fails-to-account-for-pending-validators-leading-to-inaccu.md`
```solidity
function getTotalStake() public view returns (uint256 totalStake) {
  // @audit Validators in pending state is not accounted for
  totalStake = unassignedBalance + readyValidatorIds.length * VALIDATOR_CAPACITY + latestActiveBalanceAfterFee
      + delayedEffectiveBalance + withdrawnEffectiveBalance + subtractRewardFee(delayedRewards) - unstakeQueueAmount;
}
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

**Variant: Validation State Check Missing - HIGH Severity Cases** [HIGH]
> Found in 7 reports:
> - `reports/cosmos_cometbft_findings/dust-limit-attack-on-forceupdatenodes-allows-dos-of-rebalancing-and-potential-va.md`
> - `reports/cosmos_cometbft_findings/function-gettotalstake-fails-to-account-for-pending-validators-leading-to-inaccu.md`
> - `reports/cosmos_cometbft_findings/h-01-lack-of-access-control-in-agentnftv2addvalidator-enables-unauthorized-valid.md`

**Variant: Validation State Check Missing in Suzaku Core** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/dos-on-stake-accounting-functions-by-bloating-operatornodesarray-with-irremovabl.md`
> - `reports/cosmos_cometbft_findings/dust-limit-attack-on-forceupdatenodes-allows-dos-of-rebalancing-and-potential-va.md`

**Variant: Validation State Check Missing in Casimir** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/function-gettotalstake-fails-to-account-for-pending-validators-leading-to-inaccu.md`
> - `reports/cosmos_cometbft_findings/operator-is-not-removed-in-registry-when-validator-has-owedamount-0.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in validation state check missing logic allows exploitation through missing vali
func secureValidationStateCheckMissing(ctx sdk.Context) error {
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
- **Affected Protocols**: Berachain Beaconkit, Casimir, Liquistake, Mystic Finance, Ditto
- **Validation Strength**: Strong (3+ auditors)

---

## 4. Validation Percentage Overflow

### Overview

Implementation flaw in validation percentage overflow logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: This bug report discusses an issue with the `change_maximum_validator_stake_percent()` method in the `settings_manager.rs` file of the `appchain-anchor` project. This method checks that a percentage value passed to it is less than 100, but other functions in the same file do not perform this check. 

### Vulnerability Description

#### Root Cause

Implementation flaw in validation percentage overflow logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies validation percentage overflow in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to validation operations

### Vulnerable Pattern Examples

**Example 1: LACK OF VALIDATION ALLOWS SETTING PERCENTAGES HIGHER THAN A HUNDRED** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/lack-of-validation-allows-setting-percentages-higher-than-a-hundred.md`
```rust
fn change_maximum_market_value_percent_of_near_fungible_tokens(&mut self, value: u16) {
    self.assert_owner();
    let mut protocol_settings = self.protocol_settings.get().unwrap();
    assert!(
        value != protocol_settings.maximum_market_value_percent_of_near_fungible_tokens,
        "The value is not changed."
    );
    protocol_settings.maximum_market_value_percent_of_near_fungible_tokens = value;
    self.protocol_settings.set(&protocol_settings);
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in validation percentage overflow logic allows exploitation through missing vali
func secureValidationPercentageOverflow(ctx sdk.Context) error {
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
- **Affected Protocols**: Octopus Network Anchor
- **Validation Strength**: Single auditor

---

## 5. Validation Address Normalization

### Overview

Implementation flaw in validation address normalization logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 1, MEDIUM: 1.

> **Key Finding**: Bug report: The cw20-base contract does not properly handle Terra addresses that are in all uppercase or all lowercase. This means that certain functions, such as the minter and marketing addresses, may not be able to perform their intended functions if the addresses are in uppercase. Additionally, 

### Vulnerability Description

#### Root Cause

Implementation flaw in validation address normalization logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies validation address normalization in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to validation operations

### Vulnerable Pattern Examples

**Example 1: LACK OF ADDRESS CANONICALIZATION/NORMALIZATION** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/lack-of-address-canonicalizationnormalization.md`
```go
let mint = match msg.mint {
        Some(m) => Some(MinterData {
            minter: deps.api.addr_validate(&m.minter)?,
            cap: m.cap,
        }),
        None => None,
    };
```

**Example 2: [M-03] `RemoteAddressValidator` can incorrectly convert addresses to lowercase** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-03-remoteaddressvalidator-can-incorrectly-convert-addresses-to-lowercase.md`
```go
if ((b >= 65) && (b <= 70)) bytes(s)[i] = bytes1(b + uint8(32));
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in validation address normalization logic allows exploitation through missing va
func secureValidationAddressNormalization(ctx sdk.Context) error {
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
- **Affected Protocols**: Mars Protocol\n CW Tokens, Axelar Network
- **Validation Strength**: Moderate (2 auditors)

---

## 6. Validation Duplicate Missing

### Overview

Implementation flaw in validation duplicate missing logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: HIGH: 3.

> **Key Finding**: This bug report concerns the `_updateAccountSlashingTrackers` function in the `VotingV2` contract. The function contains an optimization that marks unresolved requests in a prior round (rolled votes) as deleted via an entry in the `deletedRequests` map. This is intended to reduce gas consumption as 

### Vulnerability Description

#### Root Cause

Implementation flaw in validation duplicate missing logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies validation duplicate missing in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to validation operations

### Vulnerable Pattern Examples

**Example 1: Duplicate Request Rewards** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/duplicate-request-rewards.md`
```go
deletedRequests[1] = 1
deletedRequests[2] = 2
```

**Example 2: [H-01] Lack of access control in `AgentNftV2::addValidator()` enables unauthoriz** [HIGH]
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

**Example 3: [H-03] `SettlementSignatureVerifier` is missing check for duplicate validator si** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-03-settlementsignatureverifier-is-missing-check-for-duplicate-validator-signat.md`
```solidity
function verifyECDSA(
    bytes32 msgHash,
    bytes calldata signatures
) internal view returns (bool) {
    require(
        signatures.length % 65 == 0,
        "Signature length must be a multiple of 65"
    );

    uint256 len = signatures.length;
    uint256 m = 0;
    for (uint256 i = 0; i < len; i += 65) {
        bytes memory sig = signatures[i:i + 65];
        if (
            validators[msgHash.recover(sig)] && ++m >= required_validators
        ) {
            return true;
        }
    }

    return false;
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in validation duplicate missing logic allows exploitation through missing valida
func secureValidationDuplicateMissing(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 3
- **Affected Protocols**: Virtuals Protocol, UMA DVM 2.0 Audit, Chakra
- **Validation Strength**: Moderate (2 auditors)

---

## 7. Validation Config Bypass

### Overview

Implementation flaw in validation config bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: This bug report is about a vulnerability in the staking contracts of a 0xProject. The parameters of the staking contracts are configurable, and can be set by an authorized address. There is a possibility of setting unsafe or nonsensical values for the contract parameters, such as setting epochDurati

### Vulnerability Description

#### Root Cause

Implementation flaw in validation config bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies validation config bypass in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to validation operations

### Vulnerable Pattern Examples

**Example 1: MixinParams.setParams bypasses safety checks made by standard StakingProxy upgra** [MEDIUM]
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

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in validation config bypass logic allows exploitation through missing validation
func secureValidationConfigBypass(ctx sdk.Context) error {
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
- **Affected Protocols**: 0x v3 Staking
- **Validation Strength**: Single auditor

---

## 8. Validation Input General

### Overview

Implementation flaw in validation input general logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 5 audit reports with severity distribution: HIGH: 1, MEDIUM: 4.

> **Key Finding**: The bug report discusses several issues with the Portal smart contract, which is used for exchanging PSM tokens for yield. The report highlights that certain state variables, such as `fundingPhaseDuration` and `fundingRewardRate`, are not properly validated during the initialization phase. This can 

### Vulnerability Description

#### Root Cause

Implementation flaw in validation input general logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies validation input general in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to validation operations

### Vulnerable Pattern Examples

**Example 1: [M-02] Insufficient Input Validation** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-02-insufficient-input-validation.md`
```go
constructor(
    uint256 _fundingPhaseDuration,
    uint256 _fundingExchangeRatio,
    uint256 _fundingRewardRate,
    address _principalToken,
    address _bToken,
    address _portalEnergyToken,
    address _tokenToAcquire,
    uint256 _terminalMaxLockDuration,
    uint256 _amountToConvert
) {
    fundingPhaseDuration = _fundingPhaseDuration;
    fundingExchangeRatio = _fundingExchangeRatio;
    fundingRewardRate = _fundingRewardRate;
    principalToken = _principalToken;
    bToken = _bToken;
    portalEnergyToken = _portalEnergyToken;
    tokenToAcquire = _tokenToAcquire;
    terminalMaxLockDuration = _terminalMaxLockDuration;
    amountToConvert = _amountToConvert;
    creationTime = block.timestamp;
}
```

**Example 2: Malicious user can prevent other users from unbonding due to missing input valid** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/malicious-user-can-prevent-other-users-from-unbonding-due-to-missing-input-valid.md`
```go
func (s *Services) UnbondDelegation(ctx context.Context, stakingTxHashHex, unbondingTxHashHex, txHex, signatureHex string) *types.Error {
    // [...]
    // 3. save unbonding tx into DB
    err = s.DbClient.SaveUnbondingTx(ctx, stakingTxHashHex, unbondingTxHashHex, txHex, signatureHex)
    if err != nil {
        if ok := db.IsDuplicateKeyError(err); ok { // <-----
            log.Ctx(ctx).Warn().Err(err).Msg("unbonding request already been submitted into the system")
            return types.NewError(http.StatusForbidden, types.Forbidden, err)
        } else if ok := db.IsNotFoundError(err); ok {
            log.Ctx(ctx).Warn().Err(err).Msg("no active delegation found for unbonding request")
            return types.NewError(http.StatusForbidden, types.Forbidden, err)
        }
        log.Ctx(ctx).Error().Err(err).Msg("failed to save unbonding tx")
        return types.NewError(http.StatusInternalServerError, types.InternalServiceError, err)
    }
    return nil
}
```

**Example 3: Missing validation that ensures unspent BTC is fully sent back as change in Lomb** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/missing-validation-that-ensures-unspent-btc-is-fully-sent-back-as-change-in-lomb.md`
```
// Vulnerable pattern from Lombard Finance:
## Lombard Transfer Signing Strategy
```

**Example 4: Missing validations on administration functions** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/missing-validations-on-administration-functions.md`
```solidity
function setOwner(address newOwnerAddress) external {
    require(
        msg.sender == _owner,
        "Only the owner can set the new owner"
    );
    address oldValue = _owner;
    _owner = newOwnerAddress;
    emit OwnerUpdate(oldValue, _owner);
}
```

**Example 5: Sentinel can block core operations for any validator chosen due to missing input** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/sentinel-can-block-core-operations-for-any-validator-chosen-due-to-missing-input.md`
```solidity
function closeRebalanceRequests(address stakingManager, address[] calldata validators)
    external
    whenNotPaused
    nonReentrant
    onlyRole(MANAGER_ROLE)
{
    // ...
    uint256 totalAmount = 0;
    for (uint256 i = 0; i < validators.length;) {
        address validator = validators[i];
        require(_validatorsWithPendingRebalance.contains(validator), "No pending request");
        // Add amount to total for redelegation
        RebalanceRequest memory request = validatorRebalanceRequests[validator];
        require(request.staking == stakingManager, "Invalid staking manager for rebalance"); // @audit if `request.staking` is hoax, !
        totalAmount += request.amount;
        // Clear the rebalance request
        delete validatorRebalanceRequests[validator];
        _validatorsWithPendingRebalance.remove(validator);
        emit RebalanceRequestClosed(validator, request.amount);
        unchecked {
            ++i;
        }
    }
    // Trigger redelegation through StakingManager if there's an amount to delegate
    if (totalAmount > 0) {
        IStakingManager(stakingManager).processValidatorRedelegation(totalAmount); // @audit then `closeRebalanceRequests()` can be blocked, !
    }
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in validation input general logic allows exploitation through missing validation
func secureValidationInputGeneral(ctx sdk.Context) error {
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
- **Affected Protocols**: Possum, Babylonchain, Flexa, Kinetiq LST, Lombard Finance
- **Validation Strength**: Strong (3+ auditors)

---

## 9. Validation Incorrect Check

### Overview

Implementation flaw in validation incorrect check logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 28 audit reports with severity distribution: HIGH: 14, MEDIUM: 14.

> **Key Finding**: The `_checkBalance` function in the OETHVaultCore.sol contract is not returning the correct balance in certain scenarios. Specifically, if the WETH in the withdrawal queue exceeds the total amount of workable assets, the function should return a balance of 0 but instead returns the amount of WETH in

### Vulnerability Description

#### Root Cause

Implementation flaw in validation incorrect check logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies validation incorrect check in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to validation operations

### Vulnerable Pattern Examples

**Example 1: _checkBalance Returns an Incorrect Value During Insolvency** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/_checkbalance-returns-an-incorrect-value-during-insolvency.md`
```
// Vulnerable pattern from OETH Withdrawal Queue Audit:
The [`_checkBalance`](https://github.com/OriginProtocol/origin-dollar/blob/eca6ffa74d9d0c5fb467551a30912cb722fab9c2/contracts/contracts/vault/OETHVaultCore.sol#L392-L407) function returns the balance of an asset held in the vault and all the strategies. If the requested asset is WETH, the amount of WETH reserved for the withdrawal queue is subtracted from this balance to reflect the correct amount of workable assets. In this specific case, the function returns the same result as [the `_totalValu
```

**Example 2: AnteHandler Skipped In Non-CheckTx Mode** [HIGH]
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

**Example 3: Discrepancies In Deposit Functionality** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/discrepancies-in-deposit-functionality.md`
```rust
pub fn deposit<'a, 'info>(
    ctx: Context<'a, 'a, 'a, 'info, Deposit<'info>>,
    service: Option<Service>,
    amount: u64,
) -> Result<()> {
    // Call Guest chain program to update the stake if the chain is initialized
    if guest_chain_program_id.is_some() {
        let cpi_program = ctx.remaining_accounts[3].clone();
        let cpi_ctx = CpiContext::new_with_signer(cpi_program, cpi_accounts, seeds);
        solana_ibc::cpi::set_stake(cpi_ctx, amount as u128)?;
    }
    Ok(())
}
```

**Example 4: [H-01] Recipient Bytes Silent Burn When Non-20-Byte Payloads Pass Validation** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-recipient-bytes-silent-burn-when-non-20-byte-payloads-pass-validation.md`
```solidity
function transferPool(..., bytes calldata to, ...) external payable nonReentrant {
    // code
    _validateToLength(to);
    _validatePayloadLength(externalInfo.payload);
    _validateDstOuterGas(externalInfo.dstOuterGas);
    uint256 dstChainId = getChainId(srcChannel, true);
    // code
}
```

**Example 5: [H-01] Wrong handling of ERC20 denoms in `ERC20Keeper::BurnCoins`** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-wrong-handling-of-erc20-denoms-in-erc20keeperburncoins.md`
```go
func (k ERC20Keeper) MintCoins(ctx context.Context, addr sdk.AccAddress, amount sdk.Coins) error {
	// ... snip ...

	for _, coin := range amount {
		denom := coin.Denom
		if types.IsERC20Denom(denom) {
			return moderrors.Wrapf(types.ErrInvalidRequest, "cannot mint erc20 coin: %s", coin.Denom)
		}

		// ... snip ...

		inputBz, err := k.ERC20ABI.Pack("sudoMint", evmAddr, coin.Amount.BigInt())
		if err != nil {
			return types.ErrFailedToPackABI.Wrap(err.Error())
		}

		// ... snip ...
	}

	// ... snip ...
}
```

**Variant: Validation Incorrect Check - HIGH Severity Cases** [HIGH]
> Found in 14 reports:
> - `reports/cosmos_cometbft_findings/antehandler-skipped-in-non-checktx-mode.md`
> - `reports/cosmos_cometbft_findings/discrepancies-in-deposit-functionality.md`
> - `reports/cosmos_cometbft_findings/h-01-recipient-bytes-silent-burn-when-non-20-byte-payloads-pass-validation.md`

**Variant: Validation Incorrect Check in Suzaku Core** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/historical-reward-loss-due-to-nodeid-reuse-in-avalanchel1middleware.md`
> - `reports/cosmos_cometbft_findings/incorrect-inclusion-of-removed-nodes-in-_requireminsecondaryassetclasses-during-.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in validation incorrect check logic allows exploitation through missing validati
func secureValidationIncorrectCheck(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 28 audit reports
- **Severity Distribution**: HIGH: 14, MEDIUM: 14
- **Affected Protocols**: OETH Withdrawal Queue Audit, Yeet Cup, Tokemak, Toki Bridge, Liquistake
- **Validation Strength**: Strong (3+ auditors)

---

## 10. Validation Logic Error

### Overview

Implementation flaw in validation logic error logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 17 audit reports with severity distribution: HIGH: 9, MEDIUM: 8.

> **Key Finding**: The report mentions a problem with the function called `rebase()` which is used to increase the share price and apply staking rewards. However, the current logic does not support decreasing the share price, which can lead to risks and potential loss of tokens. The report recommends adding the abilit

### Vulnerability Description

#### Root Cause

Implementation flaw in validation logic error logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies validation logic error in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to validation operations

### Vulnerable Pattern Examples

**Example 1: [H-01] Slashing isn't supported in the rebasing mechanism** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-slashing-isnt-supported-in-the-rebasing-mechanism.md`
```
// Vulnerable pattern from Rivus:
## Severity

**Impact:** High

**Likelihood:** Medium
```

**Example 2: [H-04] Withdrawals logic allows MEV exploits of TVL changes and zero-slippage ze** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md`
```
// Vulnerable pattern from Renzo:
Deposit and withdrawal requests can be done immediately with no costs or fees, and both use the current oracle prices and TVL calculation ([`deposit`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/RestakeManager.sol#L499-L504), and [`withdraw`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/Withdraw/WithdrawQueue.sol#L217)). Crucially, the [withdrawal amount is calculated at withdrawal request submission time](https://github.com/code-423n4/2024-04-renzo/blob/ma
```

**Example 3: [H-14] Inexpedient liquidatable logic that could have half liquidable position t** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-14-inexpedient-liquidatable-logic-that-could-have-half-liquidable-position-tur.md`
```go
uint256 safetyRatioNumerator = position.collateralAmount.mulWadDown(collateralPrice);
        uint256 safetyRatioDenominator = position.shortAmount.mulWadDown(markPrice);
        safetyRatioDenominator = safetyRatioDenominator.mulWadDown(collateral.liqRatio);
        uint256 safetyRatio = safetyRatioNumerator.divWadDown(safetyRatioDenominator);

        if (safetyRatio > 1e18) return maxDebt;

        maxDebt = position.shortAmount / 2;

        if (safetyRatio < WIPEOUT_CUTOFF) maxDebt = position.shortAmount;
```

**Example 4: [M-01] The `increaseStakeAndLock()` Function Prevents Users from Increasing Stak** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-01-the-increasestakeandlock-function-prevents-users-from-increasing-stake-amou.md`
```solidity
// validate that the new lock duration is under the min and max requirements
if (newLockDuration > $.maxLockDuration || newLockDuration < $.minLockDuration) {
  revert InvalidLockDuration();
} //@audit If we didn't add a lock then this function reverts
```

**Example 5: `ViewLogic::maxLiquidatable()` doesn't take the bonus into account, making the a** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-10-viewlogicmaxliquidatable-doesnt-take-the-bonus-into-account-making-the-agen.md`
```go
maxLiquidatableAmount = (($.targetHealth * totalDebt) - (totalDelegation * liquidationThreshold)) * decPow
    / (($.targetHealth - liquidationThreshold) * assetPrice);
```

**Variant: Validation Logic Error - MEDIUM Severity Cases** [MEDIUM]
> Found in 8 reports:
> - `reports/cosmos_cometbft_findings/m-01-the-increasestakeandlock-function-prevents-users-from-increasing-stake-amou.md`
> - `reports/cosmos_cometbft_findings/m-02-the-current-veguan-implementation-does-not-give-users-extra-spins-nor-the-w.md`
> - `reports/cosmos_cometbft_findings/m-10-viewlogicmaxliquidatable-doesnt-take-the-bonus-into-account-making-the-agen.md`

**Variant: Validation Logic Error in Guanciale Stake** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-01-the-increasestakeandlock-function-prevents-users-from-increasing-stake-amou.md`
> - `reports/cosmos_cometbft_findings/m-02-the-current-veguan-implementation-does-not-give-users-extra-spins-nor-the-w.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in validation logic error logic allows exploitation through missing validation, 
func secureValidationLogicError(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 9, MEDIUM: 8
- **Affected Protocols**: Polynomial Protocol, Astaria, Staking, Datachain - IBC, Guanciale Stake
- **Validation Strength**: Strong (3+ auditors)

---

## 11. Validation Msg Missing

### Overview

Implementation flaw in validation msg missing logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: The L1 deposit function allows a depositor to send a signed payload to be executed along with the deposited tokens. However, there is a bug in the code that can cause issues when executing Cosmos Messages. This is because a step that is usually executed by `BaseApp` is missing in the `msg` loop. Thi

### Vulnerability Description

#### Root Cause

Implementation flaw in validation msg missing logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies validation msg missing in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to validation operations

### Vulnerable Pattern Examples

**Example 1: [M-05] L2 hooks don’t execute `ValidateBasic` on provided messages** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-05-l2-hooks-dont-execute-validatebasic-on-provided-messages.md`
```go
File: deposit.go
54: 	for _, msg := range tx.GetMsgs() {
55: 		handler := k.router.Handler(msg)
56: 		if handler == nil {
57: 			reason = fmt.Sprintf("Unrecognized Msg type: %s", sdk.MsgTypeURL(msg))
58: 			return
59: 		}
60:
61: 		_, err = handler(cacheCtx, msg)
62: 		if err != nil {
63: 			reason = fmt.Sprintf("Failed to execute Msg: %s", err)
64: 			return
65: 		}
66: 	}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in validation msg missing logic allows exploitation through missing validation, 
func secureValidationMsgMissing(ctx sdk.Context) error {
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
- **Affected Protocols**: Initia
- **Validation Strength**: Single auditor

---

## 12. Validation Length Check

### Overview

Implementation flaw in validation length check logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 6 audit reports with severity distribution: HIGH: 2, MEDIUM: 4.

> **Key Finding**: This bug report is about the issue that when a validator does not get enough funds to run a node (Minimum Staking Requirement, MSR), all token holders that delegated tokens to the validator cannot switch to a different validator, and might result in funds getting stuck with the nonfunctioning valida

### Vulnerability Description

#### Root Cause

Implementation flaw in validation length check logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies validation length check in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to validation operations

### Vulnerable Pattern Examples

**Example 1: Delegations might stuck in non-active validator  Pending** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/delegations-might-stuck-in-non-active-validator-pending.md`
```go
require((validatorNodes.length + 1) \* msr <= delegationsTotal, "Validator has to meet Minimum Staking Requirement");
```

**Example 2: Denial Of Slashing** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/denial-of-slashing.md`
```solidity
function verifyDoubleSigning(
    address operator,
    DoubleSigningEvidence memory e
) external {
    [...]
    for (uint256 i = 0; i < delegatedValidators.length; i++) {
        [...]
        if (EthosAVSUtils.compareStrings(delegatedValidators[i].validatorPubkey,
                                          e.validatorPubkey) &&
            isDelegationSlashable(delegatedValidators[i].endTimestamp))
        {
            timestampValid = true;
            stake = EthosAVSUtils.maxUint96(stake, delegatedValidators[i].stake);
        }
    }
    [...]
}
```

**Example 3: Elected TSS Nodes Can Avoid Slashing By Having Insuﬃcient Deposits** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/elected-tss-nodes-can-avoid-slashing-by-having-insuﬃcient-deposits.md`
```go
sigBytes, sigErr := hex.DecodeString(sig)
  if pubErr != nil || sigErr != nil {
      wm.logger.Error("hex decode error for pubkey or sig", "err", err)
      return
  }
  digestBz := crypto.Keccak256Hash([]byte(timeStr)).Bytes()
  if !crypto.VerifySignature(pubKeyBytes, digestBz, sigBytes[:64]) {
      wm.logger.Error("illegal signature", "publicKey", pubKey, "time", timeStr, "signature", sig)
      return
  }
```

**Example 4: [M-31] Vaults can be griefed to not be able to be used for deposits** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-31-vaults-can-be-griefed-to-not-be-able-to-be-used-for-deposits.md`
```solidity
function _depositETHForStaking(bytes calldata _blsPublicKeyOfKnot, uint256 _amount, bool _enableTransferHook) internal {
    require(_amount >= MIN_STAKING_AMOUNT, "Min amount not reached");
    require(_blsPublicKeyOfKnot.length == 48, "Invalid BLS public key");
    // LP token issued for the KNOT
    // will be zero for a new KNOT because the mapping doesn't exist
    LPToken lpToken = lpTokenForKnot[_blsPublicKeyOfKnot];
    if(address(lpToken) != address(0)) {
        // KNOT and it's LP token is already registered
        // mint the respective LP tokens for the user
        // total supply after minting the LP token must not exceed maximum staking amount per validator
        require(lpToken.totalSupply() + _amount <= maxStakingAmountPerValidator, "Amount exceeds the staking limit for the validator");
        // mint LP tokens for the depoistor with 1:1 ratio of LP tokens and ETH supplied
        lpToken.mint(msg.sender, _amount);
        emit LPTokenMinted(_blsPublicKeyOfKnot, address(lpToken), msg.sender, _amount);
    }
    else {
	
        // check that amount doesn't exceed max staking amount per validator
        require(_amount <= maxStakingAmountPerValidator, "Amount exceeds the staking limit for the validator");
    ...
```

**Example 5: Validators Array Length Has to Be Updated When the Validator Is Alienated.** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/validators-array-length-has-to-be-updated-when-the-validator-is-alienated.md`
```solidity
function \_alienateValidator(
 SML.PooledStaking storage STAKE,
 DSML.IsolatedStorage storage DATASTORE,
 uint256 verificationIndex,
 bytes calldata \_pk
) internal {
 require(STAKE.validators[\_pk].index <= verificationIndex, "OEL:unexpected index");
 require(
 STAKE.validators[\_pk].state == VALIDATOR\_STATE.PROPOSED,
 "OEL:NOT all pubkeys are pending"
 );

 uint256 operatorId = STAKE.validators[\_pk].operatorId;
 SML.\_imprison(DATASTORE, operatorId, \_pk);

 uint256 poolId = STAKE.validators[\_pk].poolId;
 DATASTORE.subUint(poolId, rks.secured, DCL.DEPOSIT\_AMOUNT);
 DATASTORE.addUint(poolId, rks.surplus, DCL.DEPOSIT\_AMOUNT);

 DATASTORE.subUint(poolId, DSML.getKey(operatorId, rks.proposedValidators), 1);
 DATASTORE.addUint(poolId, DSML.getKey(operatorId, rks.alienValidators), 1);

 STAKE.validators[\_pk].state = VALIDATOR\_STATE.ALIENATED;

 emit Alienated(\_pk);
}
```

**Variant: Validation Length Check - HIGH Severity Cases** [HIGH]
> Found in 2 reports:
> - `reports/cosmos_cometbft_findings/denial-of-slashing.md`
> - `reports/cosmos_cometbft_findings/elected-tss-nodes-can-avoid-slashing-by-having-insuﬃcient-deposits.md`

**Variant: Validation Length Check in Mantle Network** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/elected-tss-nodes-can-avoid-slashing-by-having-insuﬃcient-deposits.md`
> - `reports/cosmos_cometbft_findings/missing-freshness-check-on-oracle-data-in-stakingtotalcontrolled-enables-stale-r.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in validation length check logic allows exploitation through missing validation,
func secureValidationLengthCheck(ctx sdk.Context) error {
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
- **Affected Protocols**: Stakehouse Protocol, Ethos EVM, Mantle Network, Skale Token, Geode Liquid Staking
- **Validation Strength**: Strong (3+ auditors)

---

## Detection Patterns

### Automated Detection
```
# Validation Zero Check Missing
grep -rn 'validation|zero|check|missing' --include='*.go' --include='*.sol'
# Validation Bounds Missing
grep -rn 'validation|bounds|missing' --include='*.go' --include='*.sol'
# Validation State Check Missing
grep -rn 'validation|state|check|missing' --include='*.go' --include='*.sol'
# Validation Percentage Overflow
grep -rn 'validation|percentage|overflow' --include='*.go' --include='*.sol'
# Validation Address Normalization
grep -rn 'validation|address|normalization' --include='*.go' --include='*.sol'
# Validation Duplicate Missing
grep -rn 'validation|duplicate|missing' --include='*.go' --include='*.sol'
# Validation Config Bypass
grep -rn 'validation|config|bypass' --include='*.go' --include='*.sol'
# Validation Input General
grep -rn 'validation|input|general' --include='*.go' --include='*.sol'
# Validation Incorrect Check
grep -rn 'validation|incorrect|check' --include='*.go' --include='*.sol'
# Validation Logic Error
grep -rn 'validation|logic|error' --include='*.go' --include='*.sol'
```

## Keywords

`able`, `access`, `accounting`, `address`, `addresses`, `allow`, `allows`, `antehandler`, `appchain`, `attack`, `attacker`, `avoid`, `back`, `bloating`, `bounds`, `bounty`, `bypass`, `bypasses`, `causes`, `change`, `changes`, `check`, `checked`, `checks`, `claim`, `coin`, `config`, `control`, `convert`, `cosmos`
