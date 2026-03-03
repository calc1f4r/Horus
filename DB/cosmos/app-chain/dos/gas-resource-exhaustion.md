---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: dos
vulnerability_type: gas_resource_exhaustion

# Attack Vector Details
attack_type: economic_exploit
affected_component: staking_module

# Technical Primitives
primitives:
  - gas_limit_exploit
  - gas_metering_bypass
  - memory_exhaustion
  - storage_exhaustion
  - large_payload_dos
  - gas_refund_exploit
  - precompile_gas_exploit
  - cross_chain_gas_mismatch

# Impact Classification
severity: medium
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - dos
  - gas_exhaustion
  - resource_exhaustion
  - DoS
  - gas_limit
  - memory_exhaustion
  - storage_bloat
  - payload_size
  - gas_metering
  
language: go
version: all
---

## References
- [dos-can-close-a-channel-by-abusing-different-gas-limits-between-chains.md](../../../../reports/cosmos_cometbft_findings/dos-can-close-a-channel-by-abusing-different-gas-limits-between-chains.md)
- [h-04-gas-is-not-consumed-when-precompile-method-fail-allowing-resource-consumpti.md](../../../../reports/cosmos_cometbft_findings/h-04-gas-is-not-consumed-when-precompile-method-fail-allowing-resource-consumpti.md)
- [h-06-explicit-gas-limit-on-low-level-solidity-calls-can-be-bypassed-by-dispatche.md](../../../../reports/cosmos_cometbft_findings/h-06-explicit-gas-limit-on-low-level-solidity-calls-can-be-bypassed-by-dispatche.md)
- [h-07-evm-stack-overflow-error-leads-to-no-gas-being-charged-which-can-be-exploit.md](../../../../reports/cosmos_cometbft_findings/h-07-evm-stack-overflow-error-leads-to-no-gas-being-charged-which-can-be-exploit.md)
- [h-07-failed-job-cant-be-recovered-nft-may-be-lost.md](../../../../reports/cosmos_cometbft_findings/h-07-failed-job-cant-be-recovered-nft-may-be-lost.md)
- [unchecked-block-gas-limit.md](../../../../reports/cosmos_cometbft_findings/unchecked-block-gas-limit.md)
- [h-2-malicious-user-can-use-an-excessively-large-_toaddress-in-oftcoresendfrom-to.md](../../../../reports/cosmos_cometbft_findings/h-2-malicious-user-can-use-an-excessively-large-_toaddress-in-oftcoresendfrom-to.md)
- [h-6-canceling-an-auction-does-not-refund-the-current-highest-bidder.md](../../../../reports/cosmos_cometbft_findings/h-6-canceling-an-auction-does-not-refund-the-current-highest-bidder.md)
- [raptorcast-combined-memory-exhaustion-attack.md](../../../../reports/cosmos_cometbft_findings/raptorcast-combined-memory-exhaustion-attack.md)
- [dos-with-block-gas-limit.md](../../../../reports/cosmos_cometbft_findings/dos-with-block-gas-limit.md)
- [m-03-gas-used-mismatch-in-failed-contract-calls-can-lead-to-wrong-gas-deductions.md](../../../../reports/cosmos_cometbft_findings/m-03-gas-used-mismatch-in-failed-contract-calls-can-lead-to-wrong-gas-deductions.md)
- [m-04-gas-refunds-use-block-gas-instead-of-transaction-gas-leading-to-incorrect-r.md](../../../../reports/cosmos_cometbft_findings/m-04-gas-refunds-use-block-gas-instead-of-transaction-gas-leading-to-incorrect-r.md)
- [dos-on-stake-accounting-functions-by-bloating-operatornodesarray-with-irremovabl.md](../../../../reports/cosmos_cometbft_findings/dos-on-stake-accounting-functions-by-bloating-operatornodesarray-with-irremovabl.md)
- [m-18-a-single-malicious-observer-can-fill-the-block-space-with-msggaspricevoter-.md](../../../../reports/cosmos_cometbft_findings/m-18-a-single-malicious-observer-can-fill-the-block-space-with-msggaspricevoter-.md)
- [m-26-zrc20-token-pause-check-bypass.md](../../../../reports/cosmos_cometbft_findings/m-26-zrc20-token-pause-check-bypass.md)
- [m-12-the-pool-verification-in-napierrouter-is-prone-to-collision-attacks.md](../../../../reports/cosmos_cometbft_findings/m-12-the-pool-verification-in-napierrouter-is-prone-to-collision-attacks.md)
- [misplaced-stake-limit-validation-in-stake-function-of-lockedstakingpools-contrac.md](../../../../reports/cosmos_cometbft_findings/misplaced-stake-limit-validation-in-stake-function-of-lockedstakingpools-contrac.md)

## Vulnerability Title

**Gas and Resource Exhaustion DoS Vulnerabilities**

### Overview

This entry documents 7 distinct vulnerability patterns extracted from 20 audit reports (9 HIGH, 10 MEDIUM severity) across 14 protocols by 9 independent audit firms. These patterns represent recurring security issues in Cosmos SDK appchains and related staking/infrastructure protocols, validated through cross-auditor analysis.

### Vulnerability Description

#### Root Cause

These vulnerabilities fundamentally stem from:

1. **Missing state transition guards**: Critical operations lack proper checks for concurrent or conflicting state changes
2. **Incomplete accounting**: Balance, share, or reward tracking fails to account for edge cases (slashing, rebasing, pending operations)
3. **Timing window exploitation**: Race conditions between mempool visibility and transaction execution enable frontrunning attacks
4. **Cross-module inconsistency**: State tracked independently across modules can become desynchronized
5. **Insufficient validation**: Input parameters, state preconditions, or return values not properly validated

#### Attack Scenarios

#### Pattern 1: Gas Limit Exploit

**Frequency**: 9/20 reports | **Severity**: HIGH | **Validation**: Strong (4 auditors)
**Protocols affected**: Datachain - IBC, Initia, Skip Protocol Block-SDK, Exchange Contracts, Nibiru

The client has acknowledged an important issue with the cross-chain protocol. The problem occurs when a packet times out instead of being executed, which can lead to a denial of service attack. This is because different chains have different gas limits, causing one chain to run out of gas while proc

**Example 1.1** [MEDIUM] — Exchange Contracts
Source: `dos-with-block-gas-limit.md`
```solidity
// ❌ VULNERABLE: Gas Limit Exploit
function distribute() public {
    require(vestingEnabled, "TreasuryVester::distribute: vesting is not enabled");
    require(
        block.timestamp >= lastUpdate + VESTING_CLIFF,
        "TreasuryVester::distribute: it is too early to distribute"
    );
    lastUpdate = block.timestamp;

    // defines a vesting schedule that lasts for 30 months
    if (step % STEPS_TO_SLASH == 0) {
        uint slash = step / STEPS_TO_SLASH;
        if (slash < 5) {
            _vestingPercentage = _initialVestingPercentages[slash];
        } else if (slash < 12) {
            _vestingPercentage -= 20;
        } else if (slash < 20) {
            _vestingPercentage -= 15;
        } else if (slash < 30) {
            _vestingPercentage -= 10;
        } else {
           revert("TreasuryVester::distribut
```

**Example 1.2** [HIGH] — Nibiru
Source: `h-04-gas-is-not-consumed-when-precompile-method-fail-allowing-resource-consumpti.md`
```solidity
// ❌ VULNERABLE: Gas Limit Exploit
if err != nil {
    return nil, err
}

// Gas consumed by a local gas meter
contract.UseGas(startResult.CacheCtx.GasMeter().GasConsumed())
```

#### Pattern 2: Memory Exhaustion

**Frequency**: 4/20 reports | **Severity**: MEDIUM | **Validation**: Strong (3 auditors)
**Protocols affected**: Napier, Blastoff, Monad

This report discusses a vulnerability found in the Shardeum blockchain repository on GitHub. This vulnerability can lead to a complete shutdown of the network, causing a direct loss of funds for users and preventing new transactions from being confirmed. The vulnerability is caused by a lack of inpu

**Example 2.1** [UNKNOWN] — unknown
Source: `improper-input-validation-in-fixdeserializedwra.md`
```solidity
// ❌ VULNERABLE: Memory Exhaustion
2.  Switch to NodeJS 18.16.1, which is the version used by Shardeum in `dev.Dockerfile` and its various library requirements. For example, using asdf (https://asdf-vm.com/):
```

**Example 2.2** [MEDIUM] — Napier
Source: `m-12-the-pool-verification-in-napierrouter-is-prone-to-collision-attacks.md`
```solidity
// ❌ VULNERABLE: Memory Exhaustion
And then use it in the `NapierRouter::_verifyCallback` function in place of the computed address comparison logic:
```

#### Pattern 3: Cross Chain Gas Mismatch

**Frequency**: 3/20 reports | **Severity**: MEDIUM | **Validation**: Moderate (2 auditors)
**Protocols affected**: UXD Protocol, ZetaChain

This bug report is about an issue found in the OFTCore#sendFrom contract, which is part of the LayerZero protocol. The issue is that malicious users can use an excessively large _toAddress input to OFTCore#sendFrom, which is a bytes calldata of any arbitrary size, to break communication between netw

**Example 3.1** [MEDIUM] — ZetaChain
Source: `m-18-a-single-malicious-observer-can-fill-the-block-space-with-msggaspricevoter-.md`
```solidity
// ❌ VULNERABLE: Cross Chain Gas Mismatch
125: func (k msgServer) GasPriceVoter(goCtx context.Context, msg *types.MsgGasPriceVoter) (*types.MsgGasPriceVoterResponse, error) {
... 	// [...]
173:
174: 	gasUsed, err := k.fungibleKeeper.SetGasPrice(
175: 		ctx,
176: 		chainIDBigINT,
177: 		math.NewUint(gasPrice.Prices[gasPrice.MedianIndex]).BigInt(),
178: 	)
179: 	if err != nil {
180: 		return nil, err
181: 	}
182:
183: 	// reset the gas count
184: ❌ k.ResetGasMeterAndConsumeGas(ctx, gasUsed)
185:
186: 	return &types.MsgGasPriceVoterResponse{}, nil
187: }
```

**Example 3.2** [MEDIUM] — ZetaChain
Source: `m-18-a-single-malicious-observer-can-fill-the-block-space-with-msggaspricevoter-.md`
```solidity
// ❌ VULNERABLE: Cross Chain Gas Mismatch
206: // ResetGasMeterAndConsumeGas reset first the gas meter consumed value to zero and set it back to the new value
207: // 'gasUsed'
208: func (k *Keeper) ResetGasMeterAndConsumeGas(ctx sdk.Context, gasUsed uint64) {
209: 	// reset the gas count
210: 	ctx.GasMeter().RefundGas(ctx.GasMeter().GasConsumed(), "reset the gas count")
211: 	ctx.GasMeter().ConsumeGas(gasUsed, "apply evm transaction")
212: }
```

#### Pattern 4: Large Payload Dos

**Frequency**: 1/20 reports | **Severity**: MEDIUM | **Validation**: Weak (1 auditors)
**Protocols affected**: Suzaku Core

This bug report describes an issue where an operator is unable to remove a node from the system, leading to an inconsistent state and potential denial of service attacks. This occurs when the removal of a node and the confirmation of that removal happen in the same epoch, causing the node to remain 

**Example 4.1** [MEDIUM] — Suzaku Core
Source: `dos-on-stake-accounting-functions-by-bloating-operatornodesarray-with-irremovabl.md`
```solidity
// ❌ VULNERABLE: Large Payload Dos
if (nodePendingRemoval[valID] && …) {
         _removeNodeFromArray(operator,nodeId);
         nodePendingRemoval[valID] = false;
     }
```

**Example 4.2** [MEDIUM] — Suzaku Core
Source: `dos-on-stake-accounting-functions-by-bloating-operatornodesarray-with-irremovabl.md`
```solidity
// ❌ VULNERABLE: Large Payload Dos
delete $._registeredValidators[validator.nodeID];
```

#### Pattern 5: Gas Refund Exploit

**Frequency**: 1/20 reports | **Severity**: HIGH | **Validation**: Weak (1 auditors)
**Protocols affected**: Astaria

This bug report is about an issue with the AuctionHouse.sol code in the 2022-10-astaria-judging project on Github. The issue is that when an auction is canceled and outstanding debt is repaid, the current highest bidder is not refunded and will lose their funds. This can be exploited by a malicious 

#### Pattern 6: Storage Exhaustion

**Frequency**: 1/20 reports | **Severity**: MEDIUM | **Validation**: Weak (1 auditors)
**Protocols affected**: Toki Bridge

The report highlights a bug in the bridge that allows an attacker to block cross-chain transfers by sending a malicious transaction. This happens when the bridge tries to store a 10KB payload on-chain, which requires a lot of gas and can cause the transaction to fail. This blocks the entire channel,

**Example 6.1** [MEDIUM] — Toki Bridge
Source: `m-02-denial-of-service-via-large-payload-storage-exhaustion.md`
```solidity
// ❌ VULNERABLE: Storage Exhaustion
function calcFee( uint256 peerChainId, uint256 peerPoolId, address from, uint256 amountLD ) external view returns (ITransferPoolFeeCalculator.FeeInfo memory feeInfo) {
    // code
    uint256 gas = gasUsed;
    if (
        messageType == MessageType._TYPE_TRANSFER_POOL ||
        messageType == MessageType._TYPE_TRANSFER_TOKEN
    ) {
        gas +=
            gasPerPayloadLength *
            externalInfo.payload.length +
            externalInfo.dstOuterGas;
    }
    relayerFee.fee =
        (gas *
            relayerFee.dstGasPrice *
            premiumBPS *
            relayerFee.dstTokenPrice *
            decimalRatioNumerator) /
        (10000 * relayerFee.srcTokenPrice * decimalRatioDenominator);
    // code
}
```

**Example 6.2** [MEDIUM] — Toki Bridge
Source: `m-02-denial-of-service-via-large-payload-storage-exhaustion.md`
```solidity
// ❌ VULNERABLE: Storage Exhaustion
function _outServiceCallCore(
    string memory dstChannel,
    uint256 srcChainId,
    uint64 sequence,
    address token,
    uint256 amount,
    address to,
    uint256 refuelAmount,
    IBCUtils.ExternalInfo memory externalInfo,
    bool doRefuel,
    uint256 lastValidHeightOrZero
) internal {
    // code

    // External call with user-specified gas limit
    if (externalInfo.payload.length > 0 && to.code.length > 0) {
        try
            ITokiOuterServiceReceiverV1_1(to).onReceivePool{
                gas: externalInfo.dstOuterGas  // Up to 5M gas
            }(dstChannel, sequence, token, amount, externalInfo.payload)
        returns (bool successOuter) {
            if (!successOuter) {
                errorFlag += 2;
            }
        } catch {
            errorFlag += 2;

```

#### Pattern 7: Gas Metering Bypass

**Frequency**: 1/20 reports | **Severity**: MEDIUM | **Validation**: Weak (1 auditors)
**Protocols affected**: ZetaChain

The ZetaChain blockchain can be disrupted by a single observer who can send a transaction that consumes a lot of gas, possibly preventing other transactions from being processed. This is due to the use of an infinite gas meter for certain types of messages, which can be exploited by including other 

**Example 7.1** [MEDIUM] — ZetaChain
Source: `m-10-a-single-malicious-observer-can-exploit-the-infinite-gas-meter-to-grief-zet.md`
```solidity
// ❌ VULNERABLE: Gas Metering Bypass
056: func NewAnteHandler(options ethante.HandlerOptions) (sdk.AnteHandler, error) {
... 		// [...]
092:
093: 		// handle as totally normal Cosmos SDK tx
094: 		switch tx.(type) {
095: 		case sdk.Tx:
096: 			found := false
097: 			for _, msg := range tx.GetMsgs() {
098: 				switch msg.(type) {
099: 				// treat these two msg types differently because they might call EVM which results in massive gas consumption
100: 				// For these two msg types, we don't check gas limit by using a different ante handler
101: 				case *cctxtypes.MsgGasPriceVoter, *cctxtypes.MsgVoteOnObservedInboundTx:
102: 					found = true
103: 					break
104: 				}
105: 			}
106: 			if found {
107: 				// this differs newCosmosAnteHandler only in that it doesn't check gas limit
108: 				// by using an Infinite Gas Meter.

```


### Impact Analysis

#### Technical Impact
- State corruption across staking/delegation modules
- Incorrect balance tracking leading to fund misallocation
- Protocol liveness degradation or complete halt
- Loss of economic security guarantees

#### Business Impact
- Direct financial loss for stakers/delegators: Documented in 9 HIGH severity findings
- Protocol insolvency risk due to accounting errors
- Erosion of trust in validator/operator incentive alignment
- Cascading effects across DeFi protocols built on affected infrastructure

#### Frequency Analysis
- Total reports analyzed: 20
- HIGH severity: 9 (45%)
- MEDIUM severity: 10 (50%)
- Unique protocols affected: 14
- Independent audit firms: 9
- Patterns with 3+ auditor validation (Strong): 2

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

> `gas-exhaustion`, `resource-exhaustion`, `DoS`, `gas-limit`, `memory-exhaustion`, `storage-bloat`, `payload-size`, `gas-metering`, `cosmos-sdk`, `appchain`, `CometBFT`, `staking-security`, `validator-security`

### Related Vulnerabilities

- Slashing evasion bypass patterns
- Epoch snapshot timing manipulation
- Chain halt DoS vectors
- EVM-Cosmos state synchronization issues
- IBC middleware vulnerabilities
