---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: staking
vulnerability_type: validator_management_vulnerabilities

# Attack Vector Details
attack_type: economic_exploit
affected_component: staking_module

# Technical Primitives
primitives:
  - validator_registration_bypass
  - validator_removal_failure
  - validator_set_manipulation
  - validator_key_rotation
  - validator_commission_exploit
  - validator_status_transition
  - validator_dust_collateral
  - operator_key_mismatch

# Impact Classification
severity: medium
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - staking
  - validator
  - registration
  - deregistration
  - commission
  - voting_power
  - validator_set
  - key_rotation
  - jailing
  
language: go
version: all
---

## References
- [h-3-rogue-validators-can-manipulate-funding-rates-and-profit-unfairly-from-liqui.md](../../../../reports/cosmos_cometbft_findings/h-3-rogue-validators-can-manipulate-funding-rates-and-profit-unfairly-from-liqui.md)
- [allowing-the-creation-of-dust-cdps-could-lead-redeemersliquidators-to-be-not-pro.md](../../../../reports/cosmos_cometbft_findings/allowing-the-creation-of-dust-cdps-could-lead-redeemersliquidators-to-be-not-pro.md)
- [blockbuilderblskeytoaddress-can-be-overwritten-in-providerregistrysol_registeran.md](../../../../reports/cosmos_cometbft_findings/blockbuilderblskeytoaddress-can-be-overwritten-in-providerregistrysol_registeran.md)
- [lightclient-forced-ﬁnalization-could-allow-bad-updates-in-case-of-a-dos.md](../../../../reports/cosmos_cometbft_findings/lightclient-forced-ﬁnalization-could-allow-bad-updates-in-case-of-a-dos.md)
- [h-01-permissionless-sendcurrentoperatorskeys.md](../../../../reports/cosmos_cometbft_findings/h-01-permissionless-sendcurrentoperatorskeys.md)
- [operatorsregistry_getnextvalidatorsfromactiveoperators-can-dos-alluvial-staking-.md](../../../../reports/cosmos_cometbft_findings/operatorsregistry_getnextvalidatorsfromactiveoperators-can-dos-alluvial-staking-.md)
- [incorrect-injected-vote-extensions-validation.md](../../../../reports/cosmos_cometbft_findings/incorrect-injected-vote-extensions-validation.md)
- [mismatch-between-proposer-selection-algorithm.md](../../../../reports/cosmos_cometbft_findings/mismatch-between-proposer-selection-algorithm.md)
- [vote-extension-risks.md](../../../../reports/cosmos_cometbft_findings/vote-extension-risks.md)
- [penalty-system-delays-the-rewards-instead-of-reducing-them.md](../../../../reports/cosmos_cometbft_findings/penalty-system-delays-the-rewards-instead-of-reducing-them.md)
- [cannot-blame-operator-for-proposed-validator.md](../../../../reports/cosmos_cometbft_findings/cannot-blame-operator-for-proposed-validator.md)
- [m-3-new-staking-between-reward-epochs-will-dilute-rewards-for-existing-stakers-a.md](../../../../reports/cosmos_cometbft_findings/m-3-new-staking-between-reward-epochs-will-dilute-rewards-for-existing-stakers-a.md)
- [unrestricted-validator-registration-may-lead-to-dos.md](../../../../reports/cosmos_cometbft_findings/unrestricted-validator-registration-may-lead-to-dos.md)
- [m-17-bad-debt-can-be-permanently-blocked-from-being-moved-to-backstop.md](../../../../reports/cosmos_cometbft_findings/m-17-bad-debt-can-be-permanently-blocked-from-being-moved-to-backstop.md)
- [m-9-missing-slippage-protection-in-liquidation-allows-unexpected-collateral-loss.md](../../../../reports/cosmos_cometbft_findings/m-9-missing-slippage-protection-in-liquidation-allows-unexpected-collateral-loss.md)
- [m-03-xfeemarket-module-is-not-wired-up-resulting-in-non-working-cli-commands-mes.md](../../../../reports/cosmos_cometbft_findings/m-03-xfeemarket-module-is-not-wired-up-resulting-in-non-working-cli-commands-mes.md)
- [m-21-eip1559-rewards-received-by-syndicate-during-the-period-when-it-has-no-regi.md](../../../../reports/cosmos_cometbft_findings/m-21-eip1559-rewards-received-by-syndicate-during-the-period-when-it-has-no-regi.md)
- [potential-to-rotate-consensus-key-back-to-initial-key.md](../../../../reports/cosmos_cometbft_findings/potential-to-rotate-consensus-key-back-to-initial-key.md)

## Vulnerability Title

**Validator Registration and Management Vulnerabilities**

### Overview

This entry documents 8 distinct vulnerability patterns extracted from 32 audit reports (10 HIGH, 20 MEDIUM severity) across 29 protocols by 12 independent audit firms. These patterns represent recurring security issues in Cosmos SDK appchains and related staking/infrastructure protocols, validated through cross-auditor analysis.

### Vulnerability Description

#### Root Cause

These vulnerabilities fundamentally stem from:

1. **Missing state transition guards**: Critical operations lack proper checks for concurrent or conflicting state changes
2. **Incomplete accounting**: Balance, share, or reward tracking fails to account for edge cases (slashing, rebasing, pending operations)
3. **Timing window exploitation**: Race conditions between mempool visibility and transaction execution enable frontrunning attacks
4. **Cross-module inconsistency**: State tracked independently across modules can become desynchronized
5. **Insufficient validation**: Input parameters, state preconditions, or return values not properly validated

#### Attack Scenarios

#### Pattern 1: Operator Key Mismatch

**Frequency**: 7/32 reports | **Severity**: MEDIUM | **Validation**: Strong (5 auditors)
**Protocols affected**: Tanssi_2025-04-30, ZetaChain, Lido, Axelar Network, Suzaku Core

The report describes a bug in the `submitInitialSlashing` function of the `CSModule` contract. This bug causes the bond curve for a Node Operator to not be reset to the default after being penalized. This could lead to incorrect counting of unbonded validator keys. The severity of this bug is classi

**Example 1.1** [HIGH] — Tanssi_2025-04-30
Source: `h-01-permissionless-sendcurrentoperatorskeys.md`
```solidity
// ❌ VULNERABLE: Operator Key Mismatch
// Middleware.sol
    function sendCurrentOperatorsKeys() external returns (bytes32[] memory sortedKeys) {
        address gateway = getGateway();
        if (gateway == address(0)) {
            revert Middleware__GatewayNotSet();
        }

        uint48 epoch = getCurrentEpoch();
        sortedKeys = IOBaseMiddlewareReader(address(this)).sortOperatorsByPower(epoch);
        IOGateway(gateway).sendOperatorsData(sortedKeys, epoch);
    }
```

**Example 1.2** [HIGH] — Tanssi_2025-04-30
Source: `h-01-permissionless-sendcurrentoperatorskeys.md`
```solidity
// ❌ VULNERABLE: Operator Key Mismatch
function sendOperatorsData(bytes32[] calldata data, uint48 epoch) external onlyMiddleware {
        Ticket memory ticket = Operators.encodeOperatorsData(data, epoch);
        _submitOutboundToChannel(PRIMARY_GOVERNANCE_CHANNEL_ID, ticket.payload);
    }
```

#### Pattern 2: Validator Registration Bypass

**Frequency**: 5/32 reports | **Severity**: MEDIUM | **Validation**: Strong (3 auditors)
**Protocols affected**: Covalent, Ditto, Hubble Exchange, Geode Liquid Staking

This bug report is about a vulnerability in the Shardeum blockchain code, which can be found on GitHub. The bug allows for an attacker to abuse a quirk in Javascript to send a request that can take down a single node or the entire network. This is caused by a loss of precision when doing math with l

**Example 2.1** [UNKNOWN] — unknown
Source: `a-math-quirk-in-javascript-allows-anyone-to-take-down-any-validator-or-the-full-.md`
```solidity
// ❌ VULNERABLE: Validator Registration Bypass
let a_number = Number(9999999999999999);

console.log(`a_number: ${a_number}`);

// Output: "a_number: 10000000000000000"
```

**Example 2.2** [UNKNOWN] — unknown
Source: `a-math-quirk-in-javascript-allows-anyone-to-take-down-any-validator-or-the-full-.md`
```solidity
// ❌ VULNERABLE: Validator Registration Bypass
let a_number = parseInt("9999999999999999");

console.log(`a_number: ${a_number}`);

// Output: "a_number: 10000000000000000"
```

#### Pattern 3: Validator Key Rotation

**Frequency**: 5/32 reports | **Severity**: MEDIUM | **Validation**: Strong (4 auditors)
**Protocols affected**: Succinct Labs Telepathy, Cosmos SDK V3, MANTRA, Stakehouse Protocol, Primev

This bug report describes a vulnerability in the ProviderRegistry.sol and BlockTracker.sol contracts. The issue allows a malicious user to register as a provider and overwrite the blockBuilderBLSKeyToAddress[] mapping, which can lead to the loss of funds for honest providers. This vulnerability can 

**Example 3.1** [HIGH] — Primev
Source: `blockbuilderblskeytoaddress-can-be-overwritten-in-providerregistrysol_registeran.md`
```solidity
// ❌ VULNERABLE: Validator Key Rotation
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

**Example 3.2** [HIGH] — Primev
Source: `blockbuilderblskeytoaddress-can-be-overwritten-in-providerregistrysol_registeran.md`
```solidity
// ❌ VULNERABLE: Validator Key Rotation
function recordL1Block(
    uint256 _blockNumber,
    bytes calldata _winnerBLSKey
) external onlyOracle whenNotPaused {
    address _winner = providerRegistry.getEoaFromBLSKey(_winnerBLSKey); // <<<
    _recordBlockWinner(_blockNumber, _winner);
    
    uint256 newWindow = (_blockNumber - 1) / WindowFromBlockNumber.BLOCKS_PER_WINDOW + 1;
    if (newWindow > currentWindow) {
        // We've entered a new window
        currentWindow = newWindow;
        emit NewWindow(currentWindow);
    }
    
    emit NewL1Block(_blockNumber, _winner, currentWindow);
}

function getEoaFromBLSKey(bytes calldata blsKey) external view returns (address) {
    return blockBuilderBLSKeyToAddress[blsKey];
}
```

#### Pattern 4: Validator Set Manipulation

**Frequency**: 5/32 reports | **Severity**: HIGH | **Validation**: Strong (3 auditors)
**Protocols affected**: Layer 1 Assessment, Cosmos SDK, Symbiotic Relay, Ethos Cosmos

The bug report is about a function called ValidateVoteExtensions that relies on data injected by the proposer, which can be manipulated to misrepresent the voting power of validators. This can lead to incorrect consensus decisions and compromised voting process. The report recommends applying a patc

**Example 4.1** [HIGH] — Ethos Cosmos
Source: `incorrect-injected-vote-extensions-validation.md`
```solidity
// ❌ VULNERABLE: Validator Set Manipulation
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
        // Total voting power of all vote extens
```

**Example 4.2** [UNKNOWN] — unknown
Source: `lack-of-vote-validation-in-sync_trie_hashes-lea.md`
```solidity
// ❌ VULNERABLE: Validator Set Manipulation
2.  Switch to NodeJS 18.16.1, which is the version used by Shardeum in `dev.Dockerfile` and its various library requirements. For example, using asdf (https://asdf-vm.com/):
```

#### Pattern 5: Validator Dust Collateral

**Frequency**: 3/32 reports | **Severity**: MEDIUM | **Validation**: Strong (3 auditors)
**Protocols affected**: BadgerDAO, Blend, Cap

The bug report discusses a potential issue with the BorrowerOperations and LiquidationLibrary contracts in the protocol. When the value of collateral in a CDP (collateralized debt position) falls below a certain threshold, it allows for the creation of "dust CDPs" where the collateral and debt amoun

**Example 5.1** [HIGH] — BadgerDAO
Source: `allowing-the-creation-of-dust-cdps-could-lead-redeemersliquidators-to-be-not-pro.md`
```solidity
// ❌ VULNERABLE: Validator Dust Collateral
collateral.getSharesByPooledEth((singleRedemption.eBtcToRedeem * DECIMAL_PRECISION) / _redeemColFromCdp._price)
```

**Example 5.2** [HIGH] — BadgerDAO
Source: `allowing-the-creation-of-dust-cdps-could-lead-redeemersliquidators-to-be-not-pro.md`
```solidity
// ❌ VULNERABLE: Validator Dust Collateral
collateral.getSharesByPooledEth(cdp.debt * DECIMAL_PRECISION / price) >= ~0.0207 ETH of stETH shares
```

#### Pattern 6: Validator Removal Failure

**Frequency**: 3/32 reports | **Severity**: MEDIUM | **Validation**: Strong (3 auditors)
**Protocols affected**: Cudos, Andromeda – Validator Staking ADO and Vesting ADO, Skale Token

This bug report is about the issue that when a validator does not get enough funds to run a node (Minimum Staking Requirement, MSR), all token holders that delegated tokens to the validator cannot switch to a different validator, and might result in funds getting stuck with the nonfunctioning valida

**Example 6.1** [MEDIUM] — Skale Token
Source: `delegations-might-stuck-in-non-active-validator-pending.md`
```solidity
// ❌ VULNERABLE: Validator Removal Failure
require((validatorNodes.length + 1) \* msr <= delegationsTotal, "Validator has to meet Minimum Staking Requirement");
```

#### Pattern 7: Validator Status Transition

**Frequency**: 3/32 reports | **Severity**: MEDIUM | **Validation**: Strong (3 auditors)
**Protocols affected**: Berachain Beaconkit, Staking, Forta Protocol Audit

The bug report discusses issues with the current economic security and consensus safety model in the mod/state-transition/pkg/core/state_processor.go file. The report notes that the current model allows for easy bypassing of deposit barriers and has no penalties or slashing mechanisms. This can lead

**Example 7.1** [HIGH] — Staking
Source: `penalty-system-delays-the-rewards-instead-of-reducing-them.md`
```solidity
// ❌ VULNERABLE: Validator Status Transition
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

        //To claim all the rewards, alice now subscribes
```

#### Pattern 8: Validator Commission Exploit

**Frequency**: 1/32 reports | **Severity**: MEDIUM | **Validation**: Weak (1 auditors)
**Protocols affected**: Tortuga

The bug report discusses an issue with registered validators being able to drastically increase their commission percentage at any time. This can result in them profiting from a large commission for a long period of time, as the stakes are locked for 30 days. The report suggests implementing a simil

**Example 8.1** [MEDIUM] — Tortuga
Source: `validators-can-manipulate-commission-rates.md`
```solidity
// ❌ VULNERABLE: Validator Commission Exploit
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


### Impact Analysis

#### Technical Impact
- State corruption across staking/delegation modules
- Incorrect balance tracking leading to fund misallocation
- Protocol liveness degradation or complete halt
- Loss of economic security guarantees

#### Business Impact
- Direct financial loss for stakers/delegators: Documented in 10 HIGH severity findings
- Protocol insolvency risk due to accounting errors
- Erosion of trust in validator/operator incentive alignment
- Cascading effects across DeFi protocols built on affected infrastructure

#### Frequency Analysis
- Total reports analyzed: 32
- HIGH severity: 10 (31%)
- MEDIUM severity: 20 (62%)
- Unique protocols affected: 29
- Independent audit firms: 12
- Patterns with 3+ auditor validation (Strong): 7

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

> `validator`, `registration`, `deregistration`, `commission`, `voting-power`, `validator-set`, `key-rotation`, `jailing`, `unjailing`, `operator`, `cosmos-sdk`, `appchain`, `CometBFT`, `staking-security`, `validator-security`

### Related Vulnerabilities

- Slashing evasion bypass patterns
- Epoch snapshot timing manipulation
- Chain halt DoS vectors
- EVM-Cosmos state synchronization issues
- IBC middleware vulnerabilities
