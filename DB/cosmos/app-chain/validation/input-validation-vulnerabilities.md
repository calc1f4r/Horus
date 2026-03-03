---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: validation
vulnerability_type: input_validation_vulnerabilities

# Attack Vector Details
attack_type: economic_exploit
affected_component: staking_module

# Technical Primitives
primitives:
  - missing_zero_check
  - missing_bounds_check
  - missing_state_check
  - percentage_overflow
  - address_validation_missing
  - type_validation_missing
  - duplicate_validation_missing
  - configuration_validation

# Impact Classification
severity: medium
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - validation
  - input_validation
  - missing_check
  - zero_check
  - bounds_check
  - parameter_validation
  - address_validation
  - type_check
  - configuration
  
language: go
version: all
---

## References
- [every-node-gets-a-full-validators-bounty-fixed.md](../../../../reports/cosmos_cometbft_findings/every-node-gets-a-full-validators-bounty-fixed.md)
- [h-02-a-registered-contract-wont-earn-fees-if-_recipient-is-a-fresh-address.md](../../../../reports/cosmos_cometbft_findings/h-02-a-registered-contract-wont-earn-fees-if-_recipient-is-a-fresh-address.md)
- [h-30-any-public-vault-without-a-delegate-can-be-drained.md](../../../../reports/cosmos_cometbft_findings/h-30-any-public-vault-without-a-delegate-can-be-drained.md)
- [h-4-boughtpurchased-token-can-be-sent-to-attackers-wallet-using-0x-adaptor.md](../../../../reports/cosmos_cometbft_findings/h-4-boughtpurchased-token-can-be-sent-to-attackers-wallet-using-0x-adaptor.md)
- [liquidity-pool-can-be-set-multiple-times-in-myshare.md](../../../../reports/cosmos_cometbft_findings/liquidity-pool-can-be-set-multiple-times-in-myshare.md)
- [h-03-settlementsignatureverifier-is-missing-check-for-duplicate-validator-signat.md](../../../../reports/cosmos_cometbft_findings/h-03-settlementsignatureverifier-is-missing-check-for-duplicate-validator-signat.md)
- [attackers-can-prevent-new-challengeslistingsbackends-parameter-changes-and-stake.md](../../../../reports/cosmos_cometbft_findings/attackers-can-prevent-new-challengeslistingsbackends-parameter-changes-and-stake.md)
- [m-03-invalid-max-stake-amount-validation-prevents-setting-when-no-staking-limit-.md](../../../../reports/cosmos_cometbft_findings/m-03-invalid-max-stake-amount-validation-prevents-setting-when-no-staking-limit-.md)
- [m-04-lack-of-deadline-for-uniswap-amm.md](../../../../reports/cosmos_cometbft_findings/m-04-lack-of-deadline-for-uniswap-amm.md)
- [m-24-staking-presign-could-use-some-basic-validations.md](../../../../reports/cosmos_cometbft_findings/m-24-staking-presign-could-use-some-basic-validations.md)
- [risk-of-server-side-request-forgery-attacks.md](../../../../reports/cosmos_cometbft_findings/risk-of-server-side-request-forgery-attacks.md)
- [lack-of-validation.md](../../../../reports/cosmos_cometbft_findings/lack-of-validation.md)
- [m-02-insufficient-input-validation.md](../../../../reports/cosmos_cometbft_findings/m-02-insufficient-input-validation.md)
- [m-03-funding-cycles-that-use-jbxbuybackdelegate-as-a-redeem-data-source-or-any-d.md](../../../../reports/cosmos_cometbft_findings/m-03-funding-cycles-that-use-jbxbuybackdelegate-as-a-redeem-data-source-or-any-d.md)

## Vulnerability Title

**Missing Input Validation and Parameter Check Vulnerabilities**

### Overview

This entry documents 6 distinct vulnerability patterns extracted from 20 audit reports (6 HIGH, 13 MEDIUM severity) across 19 protocols by 9 independent audit firms. These patterns represent recurring security issues in Cosmos SDK appchains and related staking/infrastructure protocols, validated through cross-auditor analysis.

### Vulnerability Description

#### Root Cause

These vulnerabilities fundamentally stem from:

1. **Missing state transition guards**: Critical operations lack proper checks for concurrent or conflicting state changes
2. **Incomplete accounting**: Balance, share, or reward tracking fails to account for edge cases (slashing, rebasing, pending operations)
3. **Timing window exploitation**: Race conditions between mempool visibility and transaction execution enable frontrunning attacks
4. **Cross-module inconsistency**: State tracked independently across modules can become desynchronized
5. **Insufficient validation**: Input parameters, state preconditions, or return values not properly validated

#### Attack Scenarios

#### Pattern 1: Missing Zero Check

**Frequency**: 9/20 reports | **Severity**: HIGH | **Validation**: Strong (6 auditors)
**Protocols affected**: Astaria, Notional, Tokemak, Magic Yearn, Canto

The bug report is about a calculation issue related to the bounty of each validator in the Skale Network. The main change is related to how bounties are calculated for each validator. The problem is that the amount a validator should get is being divided among all nodes, rather than the validator re

**Example 1.1** [HIGH] — Skale Network
Source: `every-node-gets-a-full-validators-bounty-fixed.md`
```solidity
// ❌ VULNERABLE: Missing Zero Check
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

**Example 1.2** [HIGH] — Canto
Source: `h-02-a-registered-contract-wont-earn-fees-if-_recipient-is-a-fresh-address.md`
```solidity
// ❌ VULNERABLE: Missing Zero Check
function register(address _recipient) public onlyUnregistered returns (uint256 tokenId) {
    address smartContract = msg.sender;

    if (_recipient == address(0)) revert InvalidRecipient();

    tokenId = _tokenIdTracker.current();
    _mint(_recipient, tokenId);
    _tokenIdTracker.increment();

    emit Register(smartContract, _recipient, tokenId);

    feeRecipient[smartContract] = NftData({
        tokenId: tokenId,
        registered: true
    });
}
```

#### Pattern 2: Configuration Validation

**Frequency**: 5/20 reports | **Severity**: MEDIUM | **Validation**: Strong (3 auditors)
**Protocols affected**: Umee, Yieldy, Asymmetry Finance, Kinetiq_2025-02-26, The Computable Protocol

This bug report is related to Data Validation in Datatrust. It is classified as a low difficulty bug. The addCandidate function enables users to propose new challenges, listings, or Backend and parameter changes. However, this can be exploited by attackers to block essential operations performed by 

**Example 2.1** [MEDIUM] — The Computable Protocol
Source: `attackers-can-prevent-new-challengeslistingsbackends-parameter-changes-and-stake.md`
```solidity
// ❌ VULNERABLE: Configuration Validation
def addCandidate(hash: bytes32, kind: uint256, owner: address, stake: wei_value, vote_by: timedelta):
    """
    @notice Given a listing or parameter hash, create a new voting candidate
    @dev Only privileged contracts may call this method
    @param hash The identifier for the listing or reparameterization candidate
    @param kind The type of candidate we are adding
    @param owner The address which owns this created candidate
    @param stake How much, in wei, must be staked to vote or challenge
    @param vote_by How long into the future until polls for this candidate close
    """
    assert self.hasPrivilege(msg.sender)
    assert self.candidates[hash].owner == ZERO_ADDRESS
    
    if kind == CHALLENGE:  # a challenger must successfully stake a challenge
        self.market_toke
```

**Example 2.2** [MEDIUM] — Kinetiq_2025-02-26
Source: `m-03-invalid-max-stake-amount-validation-prevents-setting-when-no-staking-limit-.md`
```solidity
// ❌ VULNERABLE: Configuration Validation
if (newMaxStakeAmount > 0) {
            require(newMaxStakeAmount > minStakeAmount, "Max stake must be greater than min");
            require(newMaxStakeAmount < stakingLimit, "Max stake must be less than limit");
        }
```

#### Pattern 3: Missing State Check

**Frequency**: 3/20 reports | **Severity**: MEDIUM | **Validation**: Strong (3 auditors)
**Protocols affected**: Rio Network, GoGoPool, Numerai

This bug report is about an issue in the MinipoolManager.sol contract of the 2022-12-gogopool repository. The Multisig can call ```MinipoolManager.sol::recordStakingError()``` if there is an error while registering the node as a validator. Also the Multisig can call [MinipoolManager.sol::finishFaile

**Example 3.1** [MEDIUM] — Rio Network
Source: `m-11-eth-withdrawers-do-not-earn-yield-while-waiting-for-a-withdrawal.md`
```solidity
// ❌ VULNERABLE: Missing State Check
sharesOwed = convertToSharesFromRestakingTokens(asset, amountIn);
```

**Example 3.2** [MEDIUM] — Rio Network
Source: `m-11-eth-withdrawers-do-not-earn-yield-while-waiting-for-a-withdrawal.md`
```solidity
// ❌ VULNERABLE: Missing State Check
epochWithdrawals.assetsReceived = SafeCast.toUint120(assetsReceived);
```

#### Pattern 4: Type Validation Missing

**Frequency**: 1/20 reports | **Severity**: MEDIUM | **Validation**: Weak (0 auditors)
**Protocols affected**: Multiple

This bug report discusses a vulnerability in the Shardus Core software, which is used for blockchain and distributed ledger technology. The vulnerability allows an attacker to send a malicious message that can disconnect active nodes from the network, potentially causing a loss of funds. The attack 

**Example 4.1** [UNKNOWN] — unknown
Source: `a-missing-check-for-the-type-of-a-variable-allows-a-maliciously-crafted-message-.md`
```solidity
// ❌ VULNERABLE: Type Validation Missing
// USER-CONTROLLED INPUT
let greetings = ["hi", "hey", "hello"]

// SERVER-SIDE CODE
for (let i = 0; i < greetings.length; i++) {

    if (greetings[i] === "hello") {
        // do something here...
    }

}
```

**Example 4.2** [UNKNOWN] — unknown
Source: `a-missing-check-for-the-type-of-a-variable-allows-a-maliciously-crafted-message-.md`
```solidity
// ❌ VULNERABLE: Type Validation Missing
// USER-CONTROLLED INPUT
let greetings = { "length": "10000000000000001" }

// SERVER-SIDE CODE
for (let i = 0; i < greetings.length; i++) {

    if (greetings[i] === "hello") {
        // do something here...
    }

}
```

#### Pattern 5: Duplicate Validation Missing

**Frequency**: 1/20 reports | **Severity**: HIGH | **Validation**: Weak (1 auditors)
**Protocols affected**: Chakra

The bug report identifies a problem with two functions, SettlementSignatureVerifier::verifyECDSA and settlement::check_chakra_signatures, in the Chakra protocol. These functions lack checks for duplicate validators, meaning that a single valid signature can pass the threshold and potentially harm th

**Example 5.1** [HIGH] — Chakra
Source: `h-03-settlementsignatureverifier-is-missing-check-for-duplicate-validator-signat.md`
```solidity
// ❌ VULNERABLE: Duplicate Validation Missing
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

**Example 5.2** [HIGH] — Chakra
Source: `h-03-settlementsignatureverifier-is-missing-check-for-duplicate-validator-signat.md`
```solidity
// ❌ VULNERABLE: Duplicate Validation Missing
ERC20TransferPayload memory payload = ERC20TransferPayload(
        ERC20Method.Transfer,
        AddressCast.to_uint256(msg.sender),
        to,//his own address on the destination chain
        AddressCast.to_uint256(token),
        to_token,
        //if SettlementMode: LockMint or MintBurn
        (type(uint256).max - IERC20(token).totalSupply())
        //if SettlementMode: LockUnlock or BurnUnlock
        IERC20(token).balanceOf(address(from_handler))
    );
```

#### Pattern 6: Missing Bounds Check

**Frequency**: 1/20 reports | **Severity**: MEDIUM | **Validation**: Weak (1 auditors)
**Protocols affected**: LMCV part 2

The report highlights a bug in the `StakingVault` contract, where the `setStakedAmountLimit` function does not validate its input, allowing the administrator to set a limit lower than the currently staked amount. This can prevent users from unstaking or claiming their rewards. The bug is demonstrate

**Example 6.1** [MEDIUM] — LMCV part 2
Source: `users-may-not-be-able-to-unstake-or-claim-rewards-when-stakedamountlimit-is-decr.md`
```solidity
// ❌ VULNERABLE: Missing Bounds Check
function setStakedAmountLimit(uint256 wad) external auth {
    stakedAmountLimit = wad;
    emit StakedAmountLimit(wad);
}
```

**Example 6.2** [MEDIUM] — LMCV part 2
Source: `users-may-not-be-able-to-unstake-or-claim-rewards-when-stakedamountlimit-is-decr.md`
```solidity
// ❌ VULNERABLE: Missing Bounds Check
function stake(int256 wad, address user) external stakeAlive { // [wad]
    require(approval(user, msg.sender), "StakingVault/Owner must consent");
    require(getOwnedDDPrime(user) >= lockedStakeable[user] * stakedMintRatio, "StakingVault/Need to own ddPRIME to cover locked amount");

    //1. Add locked tokens
    uint256 prevStakedAmount    = lockedStakeable[user]; //[wad]
    unlockedStakeable[user]     = _sub(unlockedStakeable[user], wad);
    lockedStakeable[user]       = _add(lockedStakeable[user], wad);
    stakedAmount                = _add(stakedAmount, wad);
    require(stakedAmount <= stakedAmountLimit, "StakingVault/Cannot be over staked token limit");
[...]
```


### Impact Analysis

#### Technical Impact
- State corruption across staking/delegation modules
- Incorrect balance tracking leading to fund misallocation
- Protocol liveness degradation or complete halt
- Loss of economic security guarantees

#### Business Impact
- Direct financial loss for stakers/delegators: Documented in 6 HIGH severity findings
- Protocol insolvency risk due to accounting errors
- Erosion of trust in validator/operator incentive alignment
- Cascading effects across DeFi protocols built on affected infrastructure

#### Frequency Analysis
- Total reports analyzed: 20
- HIGH severity: 6 (30%)
- MEDIUM severity: 13 (65%)
- Unique protocols affected: 19
- Independent audit firms: 9
- Patterns with 3+ auditor validation (Strong): 3

### Detection Patterns

#### Code Patterns to Look For
```
- Missing balance update before/after token transfers
- Unchecked return values from staking/delegation operations
- State reads without freshness validation
- Arithmetic operations without overflow/precision checks
- Missing access control on state-modifying functions
- Linear iterations over unbounded collections
- Race condition windows in multi-step operations
```

#### Audit Checklist
- [ ] Verify all staking state transitions update balances atomically
- [ ] Check that slashing affects all relevant state (pending, queued, active)
- [ ] Ensure withdrawal requests cannot bypass cooldown periods
- [ ] Validate that reward calculations handle all edge cases (zero stake, partial periods)
- [ ] Confirm access control on all administrative and state-modifying functions
- [ ] Test for frontrunning vectors in all two-step operations
- [ ] Verify iteration bounds on all loops processing user-controlled data
- [ ] Check cross-module state consistency after complex operations

### Keywords for Search

> `input-validation`, `missing-check`, `zero-check`, `bounds-check`, `parameter-validation`, `address-validation`, `type-check`, `configuration`, `cosmos-sdk`, `appchain`, `CometBFT`, `staking-security`, `validator-security`

### Related Vulnerabilities

- Slashing evasion bypass patterns
- Epoch snapshot timing manipulation
- Chain halt DoS vectors
- EVM-Cosmos state synchronization issues
- IBC middleware vulnerabilities
