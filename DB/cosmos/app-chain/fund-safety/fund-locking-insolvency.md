---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: fund-safety
vulnerability_type: fund_locking_insolvency

# Attack Vector Details
attack_type: economic_exploit
affected_component: staking_module

# Technical Primitives
primitives:
  - permanent_fund_lock
  - conditional_fund_lock
  - insolvency_slash
  - insolvency_rebase
  - insolvency_bad_debt
  - withdrawal_blocked
  - upgrade_fund_lock
  - griefing_fund_lock

# Impact Classification
severity: medium
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - fund_safety
  - fund_locking
  - insolvency
  - bad_debt
  - permanent_lock
  - stuck_funds
  - withdrawal_blocked
  - protocol_insolvency
  - negative_rebase
  
language: go
version: all
---

## References
- [deadlock-due-to-abort-channel-flood.md](../../../../reports/cosmos_cometbft_findings/deadlock-due-to-abort-channel-flood.md)
- [due-diligence-into-farm-managers.md](../../../../reports/cosmos_cometbft_findings/due-diligence-into-farm-managers.md)
- [evidence-validation-can-fail-after-256-blocks.md](../../../../reports/cosmos_cometbft_findings/evidence-validation-can-fail-after-256-blocks.md)
- [h-01-recipient-bytes-silent-burn-when-non-20-byte-payloads-pass-validation.md](../../../../reports/cosmos_cometbft_findings/h-01-recipient-bytes-silent-burn-when-non-20-byte-payloads-pass-validation.md)
- [h-02-a-regular-cosmos-sdk-message-can-be-disguised-as-an-evm-transaction-causing.md](../../../../reports/cosmos_cometbft_findings/h-02-a-regular-cosmos-sdk-message-can-be-disguised-as-an-evm-transaction-causing.md)
- [h-02-if-user-sets-a-low-gasprice-the-operator-would-have-to-choose-between-being.md](../../../../reports/cosmos_cometbft_findings/h-02-if-user-sets-a-low-gasprice-the-operator-would-have-to-choose-between-being.md)
- [h-02-user-can-lose-up-to-whole-stake-on-vault-withdrawal-when-there-are-funds-lo.md](../../../../reports/cosmos_cometbft_findings/h-02-user-can-lose-up-to-whole-stake-on-vault-withdrawal-when-there-are-funds-lo.md)
- [h-03-a-vault-can-be-locked-from-marketplacezap-and-stakingzap.md](../../../../reports/cosmos_cometbft_findings/h-03-a-vault-can-be-locked-from-marketplacezap-and-stakingzap.md)
- [h-03-freeze-the-bridge-via-large-erc20-namessymbolsdenoms.md](../../../../reports/cosmos_cometbft_findings/h-03-freeze-the-bridge-via-large-erc20-namessymbolsdenoms.md)
- [h-06-the-amount-of-xezeth-in-circulation-will-not-represent-the-amount-of-ezeth-.md](../../../../reports/cosmos_cometbft_findings/h-06-the-amount-of-xezeth-in-circulation-will-not-represent-the-amount-of-ezeth-.md)
- [h-1-the-renewal-grace-period-gives-users-insurance-for-no-premium.md](../../../../reports/cosmos_cometbft_findings/h-1-the-renewal-grace-period-gives-users-insurance-for-no-premium.md)
- [h-1-unlimited-mint-of-illuminate-pts-is-possible-whenever-any-market-is-uninitia.md](../../../../reports/cosmos_cometbft_findings/h-1-unlimited-mint-of-illuminate-pts-is-possible-whenever-any-market-is-uninitia.md)
- [absence-of-ibc-channel-verification-in-updateentry-function.md](../../../../reports/cosmos_cometbft_findings/absence-of-ibc-channel-verification-in-updateentry-function.md)
- [burn-address-should-be-defined-as-different-than-system-contracts.md](../../../../reports/cosmos_cometbft_findings/burn-address-should-be-defined-as-different-than-system-contracts.md)
- [delayed-staking-transaction-will-not-be-unbondable-letting-staker-s-funds-locked.md](../../../../reports/cosmos_cometbft_findings/delayed-staking-transaction-will-not-be-unbondable-letting-staker-s-funds-locked.md)
- [failure-to-validate-locked-stake-initialization.md](../../../../reports/cosmos_cometbft_findings/failure-to-validate-locked-stake-initialization.md)
- [insufficient-validation-on-locktype-when-staking-may-cause-negligent-users-to-te.md](../../../../reports/cosmos_cometbft_findings/insufficient-validation-on-locktype-when-staking-may-cause-negligent-users-to-te.md)
- [m-01-_safemint-will-fail-due-to-an-edge-case-in-calculating-tokenid-using-the-_g.md](../../../../reports/cosmos_cometbft_findings/m-01-_safemint-will-fail-due-to-an-edge-case-in-calculating-tokenid-using-the-_g.md)
- [m-01-an-attacker-can-dos-a-coinswap-pool.md](../../../../reports/cosmos_cometbft_findings/m-01-an-attacker-can-dos-a-coinswap-pool.md)
- [m-02-block_period-is-incorrect.md](../../../../reports/cosmos_cometbft_findings/m-02-block_period-is-incorrect.md)

## Vulnerability Title

**Fund Locking and Protocol Insolvency Vulnerabilities**

### Overview

This entry documents 5 distinct vulnerability patterns extracted from 82 audit reports (28 HIGH, 49 MEDIUM severity) across 61 protocols by 15 independent audit firms. These patterns represent recurring security issues in Cosmos SDK appchains and related staking/infrastructure protocols, validated through cross-auditor analysis.

### Vulnerability Description

#### Root Cause

These vulnerabilities fundamentally stem from:

1. **Missing state transition guards**: Critical operations lack proper checks for concurrent or conflicting state changes
2. **Incomplete accounting**: Balance, share, or reward tracking fails to account for edge cases (slashing, rebasing, pending operations)
3. **Timing window exploitation**: Race conditions between mempool visibility and transaction execution enable frontrunning attacks
4. **Cross-module inconsistency**: State tracked independently across modules can become desynchronized
5. **Insufficient validation**: Input parameters, state preconditions, or return values not properly validated

#### Attack Scenarios

#### Pattern 1: Conditional Fund Lock

**Frequency**: 61/82 reports | **Severity**: MEDIUM | **Validation**: Strong (14 auditors)
**Protocols affected**: Ubiquity, Adrena, Toki Bridge, Cosmos Module, zkSync

The provided UpdateEntry function in a system managing entries in IBC lacks verification for the correctness and validity of Inter-Blockchain Communication (IBC) channel identifiers. This can potentially lead to unauthorized access or incorrect updates to the system. The recommended solution is for 

**Example 1.1** [MEDIUM] — Elys Modules
Source: `absence-of-ibc-channel-verification-in-updateentry-function.md`
```solidity
// ❌ VULNERABLE: Conditional Fund Lock
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
		Decimals: 
```

**Example 1.2** [MEDIUM] — Genesis
Source: `burn-address-should-be-defined-as-different-than-system-contracts.md`
```solidity
// ❌ VULNERABLE: Conditional Fund Lock
address public constant VALIDATOR_CONTRACT_ADDR = 0x0000000000000000000000000000000000001000;
  address public constant SLASH_CONTRACT_ADDR = 0x0000000000000000000000000000000000001001;
  address public constant SYSTEM_REWARD_ADDR = 0x0000000000000000000000000000000000001002;
  address public constant LIGHT_CLIENT_ADDR = 0x0000000000000000000000000000000000001003;
  address public constant RELAYER_HUB_ADDR = 0x0000000000000000000000000000000000001004;
  address public constant CANDIDATE_HUB_ADDR = 0x0000000000000000000000000000000000001005;
  address public constant GOV_HUB_ADDR = 0x0000000000000000000000000000000000001006;
  address public constant PLEDGE_AGENT_ADDR = 0x0000000000000000000000000000000000001007;
  address public constant BURN_ADDR = 0x00000000000000000000000000000000000010
```

#### Pattern 2: Permanent Fund Lock

**Frequency**: 9/82 reports | **Severity**: MEDIUM | **Validation**: Strong (4 auditors)
**Protocols affected**: OpenQ, FrankenDAO, Opyn Crab Netting, Kinetiq_2025-02-26, Illuminate

This report discusses a vulnerability that allows an attacker to block contract deployments to a specific address by marking it as a vesting account. This renders the contract permanently inaccessible and any funds deployed with it will also be irretrievable. The severity increases if this is done t

**Example 2.1** [HIGH] — Kinetiq_2025-02-26
Source: `h-05-funds-can-be-permanently-locked-due-to-unsafe-type-casting.md`
```solidity
// ❌ VULNERABLE: Permanent Fund Lock
l1Write.sendTokenDelegate(delegateTo, uint64(amount), false);
```

**Example 2.2** [MEDIUM] — Suzaku Core
Source: `insufficient-validation-in-avalanchel1middlewareremoveoperator-can-create-perman.md`
```solidity
// ❌ VULNERABLE: Permanent Fund Lock
// AvalancheL1Middleware.sol
  function disableOperator(
        address operator
    ) external onlyOwner updateGlobalNodeStakeOncePerEpoch {
        operators.disable(operator); //@note disable an operator - this only works if operator exists
    }
function removeOperator(
    address operator
) external onlyOwner updateGlobalNodeStakeOncePerEpoch {
    (, uint48 disabledTime) = operators.getTimes(operator);
    if (disabledTime == 0 || disabledTime + SLASHING_WINDOW > Time.timestamp()) {
        revert AvalancheL1Middleware__OperatorGracePeriodNotPassed(disabledTime, SLASHING_WINDOW);
    }
    operators.remove(operator); // @audit no check
}
```

#### Pattern 3: Withdrawal Blocked

**Frequency**: 6/82 reports | **Severity**: MEDIUM | **Validation**: Strong (4 auditors)
**Protocols affected**: Rio Network, Exceed Finance Liquid Staking & Early Purchase, Taurus, Karak-June, Andromeda – Validator Staking ADO and Vesting ADO

This bug report discusses an issue with the withdrawal process for a user's funds. Currently, the user needs to make a withdrawal request and wait for a specific time period before being able to call the "finishWithdrawal" function to receive their funds. However, the problem is that this function d

**Example 3.1** [MEDIUM] — DefiApp
Source: `improper-handling-of-staked-tokens-when-updating-the-gauge-in-defiappstaker.md`
```solidity
// ❌ VULNERABLE: Withdrawal Blocked
function setGauge(IGauge _gauge) external onlyRole(DEFAULT_ADMIN_ROLE) {
    require(address(_gauge) != address(0), AddressZero());
    require(
        _gauge.isPool() && _gauge.stakingToken() == _getMFDBaseStorage().stakeToken,
        DefiAppStaker_invalidGauge()
    );
    DefiAppStakerStorage storage $ = _getDefiAppStakerStorage();
    IGauge lastGauge = $.gauge;
    IGauge newGauge = IGauge(_gauge);
    address prevRewardToken = address(lastGauge) != address(0) ? lastGauge.rewardToken() : address(0);
    address newRewardToken = newGauge.rewardToken();
    MultiFeeDistributionStorage storage $m = _getMFDBaseStorage();
    if (prevRewardToken == address(0)) {
        _addReward($m, newRewardToken);
    } else if (prevRewardToken != address(0) && prevRewardToken != newRewardToken) {
  
```

**Example 3.2** [MEDIUM] — DefiApp
Source: `improper-handling-of-staked-tokens-when-updating-the-gauge-in-defiappstaker.md`
```solidity
// ❌ VULNERABLE: Withdrawal Blocked
function test_gaugeCanChangeEvenProtocolHasDeposit() external {
    // non-null time
    uint256 timestamp = 1_728_370_800;
    vm.warp(timestamp);
    // a user stakes his token
    uint256 user1Amount = 80 ether;
    stake_in_mfd(User1.addr, user1Amount, ONE_MONTH_TYPE_INDEX);
    // admin decides to change gauge
    MockToken homeToken2 = new MockToken("Home Token2", "HT2");
    MockGauge gauge2 = MockGauge(create_gauge(Admin.addr, address(homeToken2), address(weth9), address(poolFactory)));
    vm.startPrank(Admin.addr);
    staker.setGauge(gauge2);
    vm.stopPrank();
    console.log("The protocol balance in old gauge", gauge.balanceOf(address(staker)));
    // admin decides to change back to old gauge
    vm.startPrank(Admin.addr);
    staker.setGauge(gauge);
    vm.stopPrank();
    
```

#### Pattern 4: Insolvency Bad Debt

**Frequency**: 5/82 reports | **Severity**: MEDIUM | **Validation**: Moderate (2 auditors)
**Protocols affected**: Blueberry, Illuminate, Ethereum Credit Guild

The `AuctionHouse` contract has a bug that can cause auctions to fail or execute at unfavorable prices. This is because there is no check for sequencer uptime, which can lead to issues if there is a network outage. This can result in a loss for the protocol and the slashing of all users with weight 

**Example 4.1** [MEDIUM] — Blueberry
Source: `m-16-chainlinkadapteroracle-will-return-the-wrong-price-for-asset-if-underlying-.md`
```solidity
// ❌ VULNERABLE: Insolvency Bad Debt
This comment is true but in my submission I address this exact issue and why it's still an issue even if the aggregator has multiple sources:

> Note:
> Chainlink oracles are used a just one piece of the OracleAggregator system and it is assumed that using a combination of other oracles, a scenario like this can be avoided. However this is not the case because the other oracles also have their flaws that can still allow this to be exploited. As an example if the chainlink oracle is being used with a UniswapV3Oracle which uses a long TWAP then this will be exploitable when the TWAP is near the minPrice on the way down. In a scenario like that it wouldn't matter what the third oracle was because it would be bypassed with the two matching oracles prices. If secondary oracles like Band are use
```

**Example 4.2** [MEDIUM] — Blueberry
Source: `m-16-chainlinkadapteroracle-will-return-the-wrong-price-for-asset-if-underlying-.md`
```solidity
// ❌ VULNERABLE: Insolvency Bad Debt
> 
> This comment is true but in my submission I address this exact issue and why it's still an issue even if the aggregator has multiple sources:
> 
> > Note:
> > Chainlink oracles are used a just one piece of the OracleAggregator system and it is assumed that using a combination of other oracles, a scenario like this can be avoided. However this is not the case because the other oracles also have their flaws that can still allow this to be exploited. As an example if the chainlink oracle is being used with a UniswapV3Oracle which uses a long TWAP then this will be exploitable when the TWAP is near the minPrice on the way down. In a scenario like that it wouldn't matter what the third oracle was because it would be bypassed with the two matching oracles prices. If secondary oracles like B
```

#### Pattern 5: Insolvency Slash

**Frequency**: 1/82 reports | **Severity**: HIGH | **Validation**: Weak (1 auditors)
**Protocols affected**: Elytra_2025-07-10

The Elytra protocol has a bug that affects how it tracks the amount of assets it owns. This can lead to incorrect calculations of the total value of assets and the price of its token, called `elyAsset`. This bug can also create opportunities for malicious users to profit and potentially cause the pr

**Example 5.1** [HIGH] — Elytra_2025-07-10
Source: `h-04-strategy-allocation-tracking-errors-affect-tvl-calculations.md`
```solidity
// ❌ VULNERABLE: Insolvency Slash
function getTotalAssetTVL(address asset) public view returns (uint256 totalTVL) {
    uint256 poolBalance = IERC20(asset).balanceOf(address(this));
    uint256 strategyAllocated = assetsAllocatedToStrategies[asset];
    uint256 unstakingVaultBalance = _getUnstakingVaultBalance(asset);

    return poolBalance + strategyAllocated + unstakingVaultBalance;
}
```

**Example 5.2** [HIGH] — Elytra_2025-07-10
Source: `h-04-strategy-allocation-tracking-errors-affect-tvl-calculations.md`
```solidity
// ❌ VULNERABLE: Insolvency Slash
// Called during allocation
assetsAllocatedToStrategies[asset] += amount;

// Called during deallocation
uint256 withdrawn = IElytraStrategy(strategy).withdraw(asset, amount);
if (withdrawn <= assetsAllocatedToStrategies[asset]) {
    assetsAllocatedToStrategies[asset] -= withdrawn;
} else {
    assetsAllocatedToStrategies[asset] = 0;
}
```


### Impact Analysis

#### Technical Impact
- State corruption across staking/delegation modules
- Incorrect balance tracking leading to fund misallocation
- Protocol liveness degradation or complete halt
- Loss of economic security guarantees

#### Business Impact
- Direct financial loss for stakers/delegators: Documented in 28 HIGH severity findings
- Protocol insolvency risk due to accounting errors
- Erosion of trust in validator/operator incentive alignment
- Cascading effects across DeFi protocols built on affected infrastructure

#### Frequency Analysis
- Total reports analyzed: 82
- HIGH severity: 28 (34%)
- MEDIUM severity: 49 (59%)
- Unique protocols affected: 61
- Independent audit firms: 15
- Patterns with 3+ auditor validation (Strong): 4

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

> `fund-locking`, `insolvency`, `bad-debt`, `permanent-lock`, `stuck-funds`, `withdrawal-blocked`, `protocol-insolvency`, `negative-rebase`, `cosmos-sdk`, `appchain`, `CometBFT`, `staking-security`, `validator-security`

### Related Vulnerabilities

- Slashing evasion bypass patterns
- Epoch snapshot timing manipulation
- Chain halt DoS vectors
- EVM-Cosmos state synchronization issues
- IBC middleware vulnerabilities
