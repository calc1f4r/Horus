---
# Core Classification
protocol: Maia DAO Ecosystem
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26074
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-maia
source_link: https://code4rena.com/reports/2023-05-maia
github_link: https://github.com/code-423n4/2023-05-maia-findings/issues/786

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cross_chain
  - liquidity_manager
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Koolex
  - 1
  - 2
---

## Vulnerability Title

[M-05] Replenishing gas is missing in `_payFallbackGas` of `RootBridgeAgent`

### Overview


A bug was discovered in the call `_payFallbackGas` used to update the user deposit with the amount of gas needed to pay for the `fallback` function execution. This bug results in the `executionGasSpent` not being deposited into the `AnycallConfig` execution budget. This was found by looking at the method body of `_payFallbackGas`, which does not contain a gas replenishing call. This is called at the end of `anyFallback` after reopening a user's settlement. To mitigate this, the user must withdraw gas from the port, unwrap it, and call `_replenishGas` to top up the execution budget. This bug will not be rectified due to the upcoming migration of this section to LayerZero.

### Original Finding Content


The call `_payFallbackGas` is used to update the user deposit with the amount of gas needed to pay for the `fallback` function execution. However, it doesn't replenish gas. In other words, it doesn't deposit the `executionGasSpent` into `AnycallConfig` execution budget.

### Proof of Concept

Here is the method body:

```solidity
	function _payFallbackGas(uint32 _settlementNonce, uint256 _initialGas) internal virtual {
		//Save gasleft
		uint256 gasLeft = gasleft();

		//Get Branch Environment Execution Cost
		uint256 minExecCost = tx.gasprice * (MIN_FALLBACK_RESERVE + _initialGas - gasLeft);

		//Check if sufficient balance
		if (minExecCost > getSettlement[_settlementNonce].gasToBridgeOut) {
			_forceRevert();
			return;
		}

		//Update user deposit reverts if not enough gas
		getSettlement[_settlementNonce].gasToBridgeOut -= minExecCost.toUint128();
	}
```

<https://github.com/code-423n4/2023-05-maia/blob/main/src/ulysses-omnichain/RootBridgeAgent.sol#L831-L846>

As you can see, there is no gas replenishing call.

`_payFallbackGas` is called at the end in `anyFallback` after reopening a user's settlement.

```solidity
	function anyFallback(bytes calldata data)
		external
		virtual
		requiresExecutor
		returns (bool success, bytes memory result)
	{
		//Get Initial Gas Checkpoint
		uint256 _initialGas = gasleft();

		//Get fromChain
		(, uint256 _fromChainId) = _getContext();
		uint24 fromChainId = _fromChainId.toUint24();

		//Save Flag
		bytes1 flag = data[0];

		//Deposit nonce
		uint32 _settlementNonce;

		/// SETTLEMENT FLAG: 1 (single asset settlement)
		if (flag == 0x00) {
			_settlementNonce = uint32(bytes4(data[PARAMS_START_SIGNED:25]));
			_reopenSettlemment(_settlementNonce);

			/// SETTLEMENT FLAG: 1 (single asset settlement)
		} else if (flag == 0x01) {
			_settlementNonce = uint32(bytes4(data[PARAMS_START_SIGNED:25]));
			_reopenSettlemment(_settlementNonce);

			/// SETTLEMENT FLAG: 2 (multiple asset settlement)
		} else if (flag == 0x02) {
			_settlementNonce = uint32(bytes4(data[22:26]));
			_reopenSettlemment(_settlementNonce);
		}
		emit LogCalloutFail(flag, data, fromChainId);

		_payFallbackGas(_settlementNonce, _initialGas);

		return (true, "");
	}
```

<https://github.com/code-423n4/2023-05-maia/blob/main/src/ulysses-omnichain/RootBridgeAgent.sol#L1177>

### Recommended Mitigation Steps

Withdraw Gas from he port, unwrap it, then call `_replenishGas` to top up the execution budget.

**[0xBugsy (Maia) confirmed](https://github.com/code-423n4/2023-05-maia-findings/issues/786#issuecomment-1632885521)**

**[0xBugsy (Maia) commented](https://github.com/code-423n4/2023-05-maia-findings/issues/786#issuecomment-1655898791):**
 > We recognize the audit's findings on Anycall Gas Management. These will not be rectified due to the upcoming migration of this section to LayerZero.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Maia DAO Ecosystem |
| Report Date | N/A |
| Finders | Koolex, 1, 2 |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-maia
- **GitHub**: https://github.com/code-423n4/2023-05-maia-findings/issues/786
- **Contest**: https://code4rena.com/reports/2023-05-maia

### Keywords for Search

`vulnerability`

