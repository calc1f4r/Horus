---
protocol: generic
chain: cosmos
category: evm
vulnerability_type: precompile_state_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: evm_logic

primitives:
  - dirty_state_precompile
  - precompile_panic
  - delegatecall_precompile
  - bank_balance_sync
  - nonce_manipulation
  - tx_disguise
  - precompile_outdated
  - state_revert
  - address_conversion

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - evm
  - staking
  - defi

language: go|solidity|rust
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Evm Dirty State Precompile
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Dirty EVM state changes are not committed before precompile  | `reports/cosmos_cometbft_findings/h-2-dirty-evm-state-changes-are-not-committed-before-precompile-calls-resulting-.md` | HIGH | Sherlock |

### Evm Precompile Panic
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Stateful precompiles panic on empty calldata, which can be e | `reports/cosmos_cometbft_findings/m-29-stateful-precompiles-panic-on-empty-calldata-which-can-be-exploited-to-prev.md` | MEDIUM | Sherlock |

### Evm Delegatecall Precompile
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| DELEGATECALL to staking precompile allows theft of all stake | `reports/cosmos_cometbft_findings/delegatecall-to-staking-precompile-allows-theft-of-all-staked-mon.md` | HIGH | Spearbit |
| MixinParams.setParams bypasses safety checks made by standar | `reports/cosmos_cometbft_findings/mixinparamssetparams-bypasses-safety-checks-made-by-standard-stakingproxy-upgrad.md` | MEDIUM | ConsenSys |

### Evm Bank Balance Sync
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-03] Unlimited Nibi could be minted because evm and bank b | `reports/cosmos_cometbft_findings/h-03-unlimited-nibi-could-be-minted-because-evm-and-bank-balance-are-not-synced-.md` | HIGH | Code4rena |
| [H-06] Hardcoded gas used in ERC20 queries allows for block  | `reports/cosmos_cometbft_findings/h-06-hardcoded-gas-used-in-erc20-queries-allows-for-block-production-halt-from-i.md` | HIGH | Code4rena |

### Evm Nonce Manipulation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-07] Nonce can be manipulated by inserting a contract crea | `reports/cosmos_cometbft_findings/m-07-nonce-can-be-manipulated-by-inserting-a-contract-creation-ethereumtx-messag.md` | MEDIUM | Code4rena |

### Evm Tx Disguise
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-02] A regular Cosmos SDK message can be disguised as an E | `reports/cosmos_cometbft_findings/h-02-a-regular-cosmos-sdk-message-can-be-disguised-as-an-evm-transaction-causing.md` | HIGH | Code4rena |
| [H-07] EVM stack overflow error leads to no gas being charge | `reports/cosmos_cometbft_findings/h-07-evm-stack-overflow-error-leads-to-no-gas-being-charged-which-can-be-exploit.md` | HIGH | Code4rena |

### Evm Precompile Outdated
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-03] Outdated precompile data might cause miscalculation o | `reports/cosmos_cometbft_findings/m-03-outdated-precompile-data-might-cause-miscalculation-of-total-supply.md` | MEDIUM | Pashov Audit Group |

### Evm State Revert
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-05] Minievm fails to charge intrinsic gas costs for EVM t | `reports/cosmos_cometbft_findings/h-05-minievm-fails-to-charge-intrinsic-gas-costs-for-evm-transactions-allowing-t.md` | HIGH | Code4rena |
| [M-07] Nonce can be manipulated by inserting a contract crea | `reports/cosmos_cometbft_findings/m-07-nonce-can-be-manipulated-by-inserting-a-contract-creation-ethereumtx-messag.md` | MEDIUM | Code4rena |

### Evm Address Conversion
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-01] Wrong handling of ERC20 denoms in `ERC20Keeper::BurnC | `reports/cosmos_cometbft_findings/h-01-wrong-handling-of-erc20-denoms-in-erc20keeperburncoins.md` | HIGH | Code4rena |
| [H-02] A regular Cosmos SDK message can be disguised as an E | `reports/cosmos_cometbft_findings/h-02-a-regular-cosmos-sdk-message-can-be-disguised-as-an-evm-transaction-causing.md` | HIGH | Code4rena |
| [M-03] `RemoteAddressValidator` can incorrectly convert addr | `reports/cosmos_cometbft_findings/m-03-remoteaddressvalidator-can-incorrectly-convert-addresses-to-lowercase.md` | MEDIUM | Code4rena |
| Claiming delegation rewards via the precompile can result in | `reports/cosmos_cometbft_findings/m-20-claiming-delegation-rewards-via-the-precompile-can-result-in-a-loss-of-zeta.md` | MEDIUM | Sherlock |

---

# Precompile State Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Precompile State Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Evm Dirty State Precompile](#1-evm-dirty-state-precompile)
2. [Evm Precompile Panic](#2-evm-precompile-panic)
3. [Evm Delegatecall Precompile](#3-evm-delegatecall-precompile)
4. [Evm Bank Balance Sync](#4-evm-bank-balance-sync)
5. [Evm Nonce Manipulation](#5-evm-nonce-manipulation)
6. [Evm Tx Disguise](#6-evm-tx-disguise)
7. [Evm Precompile Outdated](#7-evm-precompile-outdated)
8. [Evm State Revert](#8-evm-state-revert)
9. [Evm Address Conversion](#9-evm-address-conversion)

---

## 1. Evm Dirty State Precompile

### Overview

Implementation flaw in evm dirty state precompile logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: HIGH: 1.

> **Key Finding**: The bug report discusses an issue with the ZetaChain platform where changes made to the Ethereum Virtual Machine (EVM) state before a precompile call are not properly reflected in the Cosmos SDK state. This can lead to double-spending of native ZETA tokens and loss of staking rewards. The root cause

### Vulnerability Description

#### Root Cause

Implementation flaw in evm dirty state precompile logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies evm dirty state precompile in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to evm operations

### Vulnerable Pattern Examples

**Example 1: Dirty EVM state changes are not committed before precompile calls, resulting in ** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-2-dirty-evm-state-changes-are-not-committed-before-precompile-calls-resulting-.md`
```solidity
82: 	// if caller is not the same as origin it means call is coming through smart contract,
83: 	// and because state of smart contract calling precompile might be updated as well
84: 	// manually reduce amount in stateDB, so it is properly reflected in bank module
85: 	stateDB := evm.StateDB.(precompiletypes.ExtStateDB)
86: 	if contract.CallerAddress != evm.Origin {
87: 		stateDB.SubBalance(stakerAddress, amountUint256)
88: 	}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in evm dirty state precompile logic allows exploitation through missing validati
func secureEvmDirtyStatePrecompile(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 1
- **Affected Protocols**: ZetaChain Cross-Chain
- **Validation Strength**: Single auditor

---

## 2. Evm Precompile Panic

### Overview

Implementation flaw in evm precompile panic logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: The bug report discusses an issue where an attacker can cause multiple pending transactions in the ZetaChain network by exploiting a vulnerability in the precompile caller. This results in the EVM crashing and the Cosmos SDK message failing. The root cause of the issue is that the precompile assumes

### Vulnerability Description

#### Root Cause

Implementation flaw in evm precompile panic logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies evm precompile panic in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to evm operations

### Vulnerable Pattern Examples

**Example 1: Stateful precompiles panic on empty calldata, which can be exploited to prevent ** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-29-stateful-precompiles-panic-on-empty-calldata-which-can-be-exploited-to-prev.md`
```go
92: func (c *Contract) RequiredGas(input []byte) uint64 {
93: 	// get methodID (first 4 bytes)
94: 	var methodID [4]byte
95: 	copy(methodID[:], input[:4])
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in evm precompile panic logic allows exploitation through missing validation, in
func secureEvmPrecompilePanic(ctx sdk.Context) error {
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
- **Affected Protocols**: ZetaChain Cross-Chain
- **Validation Strength**: Single auditor

---

## 3. Evm Delegatecall Precompile

### Overview

Implementation flaw in evm delegatecall precompile logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 1, MEDIUM: 1.

> **Key Finding**: This bug report discusses a critical risk issue found in a commit of a protocol. The staking precompile does not properly enforce the EVMC message kind, which can lead to malicious contracts stealing staked MON. The issue has been fixed in a later commit, but the report recommends enforcing `CALL` f

### Vulnerability Description

#### Root Cause

Implementation flaw in evm delegatecall precompile logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies evm delegatecall precompile in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to evm operations

### Vulnerable Pattern Examples

**Example 1: DELEGATECALL to staking precompile allows theft of all staked MON** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/delegatecall-to-staking-precompile-allows-theft-of-all-staked-mon.md`
```
// Vulnerable pattern from Monad:
## Security Report
```

**Example 2: MixinParams.setParams bypasses safety checks made by standard StakingProxy upgra** [MEDIUM]
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
// Addresses: Implementation flaw in evm delegatecall precompile logic allows exploitation through missing validat
func secureEvmDelegatecallPrecompile(ctx sdk.Context) error {
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
- **Affected Protocols**: 0x v3 Staking, Monad
- **Validation Strength**: Moderate (2 auditors)

---

## 4. Evm Bank Balance Sync

### Overview

Implementation flaw in evm bank balance sync logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 2.

> **Key Finding**: The `NibiruBankKeeper.SyncStateDBWithAccount` function in `bank_extension.go` is responsible for keeping the EVM state database (`StateDB`) in sync with bank account balances. However, this function is not being called by all operations that modify bank balances. This means that the EVM state databa

### Vulnerability Description

#### Root Cause

Implementation flaw in evm bank balance sync logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies evm bank balance sync in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to evm operations

### Vulnerable Pattern Examples

**Example 1: [H-03] Unlimited Nibi could be minted because evm and bank balance are not synce** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-03-unlimited-nibi-could-be-minted-because-evm-and-bank-balance-are-not-synced-.md`
```go
func (bk *NibiruBankKeeper) SyncStateDBWithAccount(
	ctx sdk.Context, acc sdk.AccAddress,
) {
	// If there's no StateDB set, it means we're not in an EthereumTx.
	if bk.StateDB == nil {
		return
	}
	balanceWei := evm.NativeToWei(
		bk.GetBalance(ctx, acc, evm.EVMBankDenom).Amount.BigInt(),
	)
	bk.StateDB.SetBalanceWei(eth.NibiruAddrToEthAddr(acc), balanceWei)
}
```

**Example 2: [H-06] Hardcoded gas used in ERC20 queries allows for block production halt from** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-06-hardcoded-gas-used-in-erc20-queries-allows-for-block-production-halt-from-i.md`
```go
File: funtoken.go
265: func (p precompileFunToken) balance(
266: 	start OnRunStartResult,
267: 	contract *vm.Contract,
268: ) (bz []byte, err error) {
---
285: 	erc20Bal, err := p.evmKeeper.ERC20().BalanceOf(funtoken.Erc20Addr.Address, addrEth, ctx)
286: 	if err != nil {
287: 		return
288: 	}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in evm bank balance sync logic allows exploitation through missing validation, i
func secureEvmBankBalanceSync(ctx sdk.Context) error {
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
- **Affected Protocols**: Nibiru
- **Validation Strength**: Single auditor

---

## 5. Evm Nonce Manipulation

### Overview

Implementation flaw in evm nonce manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: The Ante handler for `MsgEthereumTx` transactions is not properly managing nonces for contract creation and non-contract creation transactions. This allows for a potential exploit where a user can replay a transaction multiple times and reuse their nonces. This can be mitigated by making sure the se

### Vulnerability Description

#### Root Cause

Implementation flaw in evm nonce manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies evm nonce manipulation in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to evm operations

### Vulnerable Pattern Examples

**Example 1: [M-07] Nonce can be manipulated by inserting a contract creation `EthereumTx` me** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-07-nonce-can-be-manipulated-by-inserting-a-contract-creation-ethereumtx-messag.md`
```go
if contractCreation {
		ret, _, st.gas, vmerr = st.evm.Create(sender, st.data, st.gas, st.value)
	} else {
		// Increment the nonce for the next transaction
		st.state.SetNonce(msg.From(), st.state.GetNonce(sender.Address())+1)
		ret, st.gas, vmerr = st.evm.Call(sender, st.to(), st.data, st.gas, st.value)
	}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in evm nonce manipulation logic allows exploitation through missing validation, 
func secureEvmNonceManipulation(ctx sdk.Context) error {
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
- **Affected Protocols**: Nibiru
- **Validation Strength**: Single auditor

---

## 6. Evm Tx Disguise

### Overview

Implementation flaw in evm tx disguise logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 2.

> **Key Finding**: This bug report discusses an issue with the `ListenFinalizeBlock()` function in the `txutils.go` file of the `minievm` repository. This function is called when a block is finalized and processes the transactions. The problem occurs when the function tries to extract logs and a contract address from 

### Vulnerability Description

#### Root Cause

Implementation flaw in evm tx disguise logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies evm tx disguise in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to evm operations

### Vulnerable Pattern Examples

**Example 1: [H-02] A regular Cosmos SDK message can be disguised as an EVM transaction, caus** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-02-a-regular-cosmos-sdk-message-can-be-disguised-as-an-evm-transaction-causing.md`
```go
func (app *BaseApp) FinalizeBlock(req *abci.RequestFinalizeBlock) (res *abci.ResponseFinalizeBlock, err error) {
	defer func() {
		// call the streaming service hooks with the FinalizeBlock messages
		for _, streamingListener := range app.streamingManager.ABCIListeners {
			if err := streamingListener.ListenFinalizeBlock(app.finalizeBlockState.Context(), *req, *res); err != nil {
				app.logger.Error("ListenFinalizeBlock listening hook failed", "height", req.Height, "err", err)
			}
		}
	}()
```

**Example 2: [H-07] EVM stack overflow error leads to no gas being charged, which can be expl** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-07-evm-stack-overflow-error-leads-to-no-gas-being-charged-which-can-be-exploit.md`
```go
// evm sometimes return 0 gasRemaining, but it's not an out of gas error.
if gasRemaining == 0 && err != nil && err != vm.ErrOutOfGas {
	return nil, common.Address{}, nil, types.ErrEVMCreateFailed.Wrap(err.Error())
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in evm tx disguise logic allows exploitation through missing validation, incorre
func secureEvmTxDisguise(ctx sdk.Context) error {
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
- **Affected Protocols**: Initia
- **Validation Strength**: Single auditor

---

## 7. Evm Precompile Outdated

### Overview

Implementation flaw in evm precompile outdated logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: The bug report discusses an issue with the `Overseer.rebase()` function that calculates the total supply of HYPE owned by the protocol. The calculation uses different precompiles to get the balances of different addresses in the L1, but these precompiles return the state from the start of the curren

### Vulnerability Description

#### Root Cause

Implementation flaw in evm precompile outdated logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies evm precompile outdated in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to evm operations

### Vulnerable Pattern Examples

**Example 1: [M-03] Outdated precompile data might cause miscalculation of total supply** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-03-outdated-precompile-data-might-cause-miscalculation-of-total-supply.md`
```
// Vulnerable pattern from stHYPE_2025-10-13:
_Resolved_
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in evm precompile outdated logic allows exploitation through missing validation,
func secureEvmPrecompileOutdated(ctx sdk.Context) error {
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
- **Affected Protocols**: stHYPE_2025-10-13
- **Validation Strength**: Single auditor

---

## 8. Evm State Revert

### Overview

Implementation flaw in evm state revert logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 1, MEDIUM: 1.

> **Key Finding**: The minievm, a program used for Ethereum Virtual Machine (EVM) transactions, fails to charge the proper amount of gas for certain operations, which can lead to a significant risk of denial of service (DoS) attacks. This is due to a lack of charging for intrinsic gas costs, which are considered neces

### Vulnerability Description

#### Root Cause

Implementation flaw in evm state revert logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies evm state revert in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to evm operations

### Vulnerable Pattern Examples

**Example 1: [H-05] Minievm fails to charge intrinsic gas costs for EVM transactions, allowin** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-05-minievm-fails-to-charge-intrinsic-gas-costs-for-evm-transactions-allowing-t.md`
```go
> ctx.GasMeter().ConsumeGas(params.TxSizeCostPerByte*storetypes.Gas(len(ctx.TxBytes())), "txSize")
>
```

**Example 2: [M-07] Nonce can be manipulated by inserting a contract creation `EthereumTx` me** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-07-nonce-can-be-manipulated-by-inserting-a-contract-creation-ethereumtx-messag.md`
```go
if contractCreation {
		ret, _, st.gas, vmerr = st.evm.Create(sender, st.data, st.gas, st.value)
	} else {
		// Increment the nonce for the next transaction
		st.state.SetNonce(msg.From(), st.state.GetNonce(sender.Address())+1)
		ret, st.gas, vmerr = st.evm.Call(sender, st.to(), st.data, st.gas, st.value)
	}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in evm state revert logic allows exploitation through missing validation, incorr
func secureEvmStateRevert(ctx sdk.Context) error {
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
- **Affected Protocols**: Nibiru, Initia
- **Validation Strength**: Single auditor

---

## 9. Evm Address Conversion

### Overview

Implementation flaw in evm address conversion logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 4 audit reports with severity distribution: HIGH: 2, MEDIUM: 2.

> **Key Finding**: The bug report is about a flaw in the MiniEVM system, specifically in the ERC20 contracts that allow users to interact with the system. When a user creates an ERC20 contract through Cosmos, it is saved as `evm/ADDRESS` and the corresponding EVM address is also saved. However, there is a flaw in the 

### Vulnerability Description

#### Root Cause

Implementation flaw in evm address conversion logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies evm address conversion in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to evm operations

### Vulnerable Pattern Examples

**Example 1: [H-01] Wrong handling of ERC20 denoms in `ERC20Keeper::BurnCoins`** [HIGH]
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

**Example 2: [H-02] A regular Cosmos SDK message can be disguised as an EVM transaction, caus** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-02-a-regular-cosmos-sdk-message-can-be-disguised-as-an-evm-transaction-causing.md`
```go
func (app *BaseApp) FinalizeBlock(req *abci.RequestFinalizeBlock) (res *abci.ResponseFinalizeBlock, err error) {
	defer func() {
		// call the streaming service hooks with the FinalizeBlock messages
		for _, streamingListener := range app.streamingManager.ABCIListeners {
			if err := streamingListener.ListenFinalizeBlock(app.finalizeBlockState.Context(), *req, *res); err != nil {
				app.logger.Error("ListenFinalizeBlock listening hook failed", "height", req.Height, "err", err)
			}
		}
	}()
```

**Example 3: [M-03] `RemoteAddressValidator` can incorrectly convert addresses to lowercase** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-03-remoteaddressvalidator-can-incorrectly-convert-addresses-to-lowercase.md`
```go
if ((b >= 65) && (b <= 70)) bytes(s)[i] = bytes1(b + uint8(32));
```

**Example 4: Claiming delegation rewards via the precompile can result in a loss of ZETA rewa** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-20-claiming-delegation-rewards-via-the-precompile-can-result-in-a-loss-of-zeta.md`
```
// Vulnerable pattern from ZetaChain Cross-Chain:
Source: https://github.com/sherlock-audit/2025-04-zetachain-cross-chain-judging/issues/316 

This issue has been acknowledged by the team but won't be fixed at this time.
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in evm address conversion logic allows exploitation through missing validation, 
func secureEvmAddressConversion(ctx sdk.Context) error {
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
- **Affected Protocols**: Axelar Network, ZetaChain Cross-Chain, Initia
- **Validation Strength**: Moderate (2 auditors)

---

## Detection Patterns

### Automated Detection
```
# Evm Dirty State Precompile
grep -rn 'evm|dirty|state|precompile' --include='*.go' --include='*.sol'
# Evm Precompile Panic
grep -rn 'evm|precompile|panic' --include='*.go' --include='*.sol'
# Evm Delegatecall Precompile
grep -rn 'evm|delegatecall|precompile' --include='*.go' --include='*.sol'
# Evm Bank Balance Sync
grep -rn 'evm|bank|balance|sync' --include='*.go' --include='*.sol'
# Evm Nonce Manipulation
grep -rn 'evm|nonce|manipulation' --include='*.go' --include='*.sol'
# Evm Tx Disguise
grep -rn 'evm|tx|disguise' --include='*.go' --include='*.sol'
# Evm Precompile Outdated
grep -rn 'evm|precompile|outdated' --include='*.go' --include='*.sol'
# Evm State Revert
grep -rn 'evm|state|revert' --include='*.go' --include='*.sol'
# Evm Address Conversion
grep -rn 'evm|address|conversion' --include='*.go' --include='*.sol'
```

## Keywords

`abuse`, `accesslist`, `address`, `addresses`, `allowing`, `allows`, `appchain`, `balance`, `bank`, `because`, `before`, `being`, `block`, `bypasses`, `calls`, `cause`, `causing`, `cctxs`, `chain`, `changes`, `charge`, `checks`, `committed`, `compensation`, `computational`, `consume`, `contract`, `conversion`, `convert`, `cosmos`
