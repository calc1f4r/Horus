---
protocol: generic
chain: cosmos
category: bridge
vulnerability_type: cross_chain_bridge_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: bridge_logic

primitives:
  - replay_attack
  - token_accounting
  - relayer_exploit
  - freeze_halt
  - observer_exploit
  - denom_handling
  - message_validation

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - bridge
  - staking
  - defi

language: go|solidity|rust
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Bridge Replay Attack
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Cross-chain transactions can be replayed when the chain unde | `reports/cosmos_cometbft_findings/cross-chain-transactions-can-be-replayed-when-the-chain-undergoes-a-hard-fork.md` | MEDIUM | Cantina |
| [H-07] Failed job can't be recovered. NFT may be lost. | `reports/cosmos_cometbft_findings/h-07-failed-job-cant-be-recovered-nft-may-be-lost.md` | HIGH | Code4rena |
| [M-04] Retry Payload Channel Collision | `reports/cosmos_cometbft_findings/m-04-retry-payload-channel-collision.md` | MEDIUM | Shieldify |

### Bridge Token Accounting
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Account Inconsistencies In Bridge Tokens Instruction | `reports/cosmos_cometbft_findings/account-inconsistencies-in-bridge-tokens-instruction.md` | HIGH | OtterSec |
| [H-06] The amount of `xezETH` in circulation will not repres | `reports/cosmos_cometbft_findings/h-06-the-amount-of-xezeth-in-circulation-will-not-represent-the-amount-of-ezeth-.md` | HIGH | Code4rena |
| Protocol Assumes Unlimited Relayer Liquidity on L2 | `reports/cosmos_cometbft_findings/protocol-assumes-unlimited-relayer-liquidity-on-l2.md` | MEDIUM | Quantstamp |

### Bridge Relayer Exploit
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| A Relayer Can Avoid a Slash by Requesting a Withdrawal From  | `reports/cosmos_cometbft_findings/a-relayer-can-avoid-a-slash-by-requesting-a-withdrawal-from-the-bond.md` | HIGH | Quantstamp |
| Relayer Can Submit Undisputable Evidence for L2->L1 Trades | `reports/cosmos_cometbft_findings/relayer-can-submit-undisputable-evidence-for-l2-l1-trades.md` | HIGH | Quantstamp |
| Relayer Can Use Valid Evidence of One Trade to Avoid Getting | `reports/cosmos_cometbft_findings/relayer-can-use-valid-evidence-of-one-trade-to-avoid-getting-slashed-for-another.md` | HIGH | Quantstamp |
| Using `abi.encodePacked()`can Lead to Hash Collisions | `reports/cosmos_cometbft_findings/using-abiencodepackedcan-lead-to-hash-collisions.md` | HIGH | Quantstamp |

### Bridge Freeze Halt
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-03] Freeze The Bridge Via Large ERC20 Names/Symbols/Denom | `reports/cosmos_cometbft_findings/h-03-freeze-the-bridge-via-large-erc20-namessymbolsdenoms.md` | HIGH | Code4rena |
| [H-04] Large Validator Sets/Rapid Validator Set Updates May  | `reports/cosmos_cometbft_findings/h-04-large-validator-setsrapid-validator-set-updates-may-freeze-the-bridge-or-re.md` | HIGH | Code4rena |

### Bridge Observer Exploit
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Malicious observer can drain Solana bridge by adding failed  | `reports/cosmos_cometbft_findings/h-1-malicious-observer-can-drain-solana-bridge-by-adding-failed-deposit-transact.md` | HIGH | Sherlock |
| [M-10] A single malicious observer can exploit the infinite  | `reports/cosmos_cometbft_findings/m-10-a-single-malicious-observer-can-exploit-the-infinite-gas-meter-to-grief-zet.md` | MEDIUM | Code4rena |
| Removing an observer doesn't update an active ballot's voter | `reports/cosmos_cometbft_findings/m-13-removing-an-observer-doesnt-update-an-active-ballots-voter-list-leading-to-.md` | MEDIUM | Sherlock |
| [M-18] A single malicious observer can fill the block space  | `reports/cosmos_cometbft_findings/m-18-a-single-malicious-observer-can-fill-the-block-space-with-msggaspricevoter-.md` | MEDIUM | Code4rena |
| [M-25] Observer Can Temporarily Halt Chain | `reports/cosmos_cometbft_findings/m-25-observer-can-temporarily-halt-chain.md` | MEDIUM | Code4rena |
| Malicious observer can block messages added through the inbo | `reports/cosmos_cometbft_findings/m-8-malicious-observer-can-block-messages-added-through-the-inbound-tracker.md` | MEDIUM | Sherlock |

### Bridge Denom Handling
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-03] Freeze The Bridge Via Large ERC20 Names/Symbols/Denom | `reports/cosmos_cometbft_findings/h-03-freeze-the-bridge-via-large-erc20-namessymbolsdenoms.md` | HIGH | Code4rena |
| [H-04] Large Validator Sets/Rapid Validator Set Updates May  | `reports/cosmos_cometbft_findings/h-04-large-validator-setsrapid-validator-set-updates-may-freeze-the-bridge-or-re.md` | HIGH | Code4rena |

---

# Cross Chain Bridge Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Cross Chain Bridge Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Bridge Replay Attack](#1-bridge-replay-attack)
2. [Bridge Token Accounting](#2-bridge-token-accounting)
3. [Bridge Relayer Exploit](#3-bridge-relayer-exploit)
4. [Bridge Freeze Halt](#4-bridge-freeze-halt)
5. [Bridge Observer Exploit](#5-bridge-observer-exploit)
6. [Bridge Denom Handling](#6-bridge-denom-handling)

---

## 1. Bridge Replay Attack

### Overview

Implementation flaw in bridge replay attack logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: HIGH: 1, MEDIUM: 2.

> **Key Finding**: The bug report discusses a potential issue with the NttManager.sol code, specifically in the function "completeInboundQueuedTransfer". During a hard fork, if there are still pending transactions in the InboundQueued, they can be replayed on another chain. This is due to the lack of a checkFork(evmCh

### Vulnerability Description

#### Root Cause

Implementation flaw in bridge replay attack logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies bridge replay attack in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to bridge operations

### Vulnerable Pattern Examples

**Example 1: Cross-chain transactions can be replayed when the chain undergoes a hard fork** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/cross-chain-transactions-can-be-replayed-when-the-chain-undergoes-a-hard-fork.md`
```
// Vulnerable pattern from Wormhole:
## Vulnerability Report
```

**Example 2: [H-07] Failed job can't be recovered. NFT may be lost.** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-07-failed-job-cant-be-recovered-nft-may-be-lost.md`
```solidity
function executeJob(bytes calldata bridgeInRequestPayload) external payable {
...
delete _operatorJobs[hash];
...
    try
      HolographOperatorInterface(address(this)).nonRevertingBridgeCall{value: msg.value}(
        msg.sender,
        bridgeInRequestPayload
      )
    {
      /// @dev do nothing
    } catch {
      _failedJobs[hash] = true;
      emit FailedOperatorJob(hash);
    }
}
```

**Example 3: [M-04] Retry Payload Channel Collision** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-04-retry-payload-channel-collision.md`
```go
mapping(uint256 => mapping(uint64 => bytes)) revertReceive; // [chainId][sequence] = payload
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in bridge replay attack logic allows exploitation through missing validation, in
func secureBridgeReplayAttack(ctx sdk.Context) error {
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
- **Affected Protocols**: Wormhole, Holograph, Toki Bridge
- **Validation Strength**: Strong (3+ auditors)

---

## 2. Bridge Token Accounting

### Overview

Implementation flaw in bridge token accounting logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: HIGH: 2, MEDIUM: 1.

> **Key Finding**: The report highlights a bug in the bridge_tokens instruction, where the token_mint is not being verified as the correct mint address associated with the receipt token at the time of deposit. This allows users to transfer tokens from any escrow account instead of just the intended one. Additionally, 

### Vulnerability Description

#### Root Cause

Implementation flaw in bridge token accounting logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies bridge token accounting in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to bridge operations

### Vulnerable Pattern Examples

**Example 1: Account Inconsistencies In Bridge Tokens Instruction** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/account-inconsistencies-in-bridge-tokens-instruction.md`
```rust
pub fn bridge_tokens<'a, 'info>(
    ctx: Context<'a, 'a, 'a, 'info, BridgeTokens<'info>>,
    deposit_index: u8,
) -> Result<()> {
    [...]
    let hashed_full_denom = 
    lib::hash::CryptoHash::digest(ctx.accounts.token_mint.key().to_string().as_ref());
    let denom = ibc::apps::transfer::types::PrefixedDenom::from_str(
        &ctx.accounts.token_mint.key().to_string(),
    )
    .unwrap();
    let token = ibc::apps::transfer::types::Coin {
        denom,
        amount: deposit.amount.into(),
    };
    [...]
}
```

**Example 2: [H-06] The amount of `xezETH` in circulation will not represent the amount of `e** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-06-the-amount-of-xezeth-in-circulation-will-not-represent-the-amount-of-ezeth-.md`
```
// Vulnerable pattern from Renzo:
The protocol allows to deposit `ETH`/`WETH` (or the specific chain native currency) on a supported L2 in order to mint `ezETH` tokens, this is the process:

1. User mints `xezETH` on L2s via [`xRenzoDeposit::deposit()`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/Bridge/L2/xRenzoDeposit.sol#L204) in exchange for either `ETH` or `WETH`. The `xezETH` are minted based on the **current** `ezETH` valuation.
2. After some time the bridge sweepers transfer the `ETH`/`WETH` collected
```

**Example 3: Protocol Assumes Unlimited Relayer Liquidity on L2** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/protocol-assumes-unlimited-relayer-liquidity-on-l2.md`
```
// Vulnerable pattern from Pheasant Network:
**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> We are aware of the mentioned risk, but due to the high gas fees on L1, we have decided not to deploy the contract on L1 for now. However, we may consider consolidating the bonds on L1 in the future to address this issue.

**File(s) affected:**`PheasantNetworkBridgeChild.sol`

**Description:** For the relayer, there is currently no way to throttle the trade requests for L1->L2 trades. All valid d
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in bridge token accounting logic allows exploitation through missing validation,
func secureBridgeTokenAccounting(ctx sdk.Context) error {
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
- **Affected Protocols**: Composable Bridge + PR, Pheasant Network, Renzo
- **Validation Strength**: Strong (3+ auditors)

---

## 3. Bridge Relayer Exploit

### Overview

Implementation flaw in bridge relayer exploit logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 4 audit reports with severity distribution: HIGH: 4.

> **Key Finding**: The team has fixed a previous issue, but a new issue still exists. The `bondWithdrawal` function can only track one type of token, but the `BondManager` can support multiple tokens. This can lead to unexpected behavior in the `withdraw()` function. The team has made a second round of fixes by adding

### Vulnerability Description

#### Root Cause

Implementation flaw in bridge relayer exploit logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies bridge relayer exploit in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to bridge operations

### Vulnerable Pattern Examples

**Example 1: A Relayer Can Avoid a Slash by Requesting a Withdrawal From the Bond** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/a-relayer-can-avoid-a-slash-by-requesting-a-withdrawal-from-the-bond.md`
```
// Vulnerable pattern from Pheasant Network:
**Update**
The team fixed the described issue. However, an issue persisted: `bondWithdrawal` can only keep track of one token, but `BondManager` supports several tokens. `getBond()` receives a token ID as parameter (token A) and subtracts `bondWithdrawal.withdrawalAmount` (can be ANY token). This wrong accounting can lead to unexpected behavior in `PheasantNetworkBridgeChild.withdraw()`.

In a second round of fixes, the team solved this additional issue by adding a mapping to differentiate depos
```

**Example 2: Relayer Can Submit Undisputable Evidence for L2->L1 Trades** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/relayer-can-submit-undisputable-evidence-for-l2-l1-trades.md`
```
// Vulnerable pattern from Pheasant Network:
**Update**
The issue is fixed due to a shift of responsibility. Now, the relayer has no reason to submit evidence with a wrong block hash because he will get slashed when he will have to defend himself.

![Image 63: Alert icon](https://certificate.quantstamp.com/full/pheasant-network/0b120935-78d1-45a1-88c4-f770c8e5fa52/static/media/info-icon-alert.3c9578483b1cf3181c9bfb6fec7dc641.svg)

**Update**
Addressed in: `64a96f0bec95007790f91ab71b054b38eb0e101a`. The client provided the following explana
```

**Example 3: Relayer Can Use Valid Evidence of One Trade to Avoid Getting Slashed for Another** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/relayer-can-use-valid-evidence-of-one-trade-to-avoid-getting-slashed-for-another.md`
```
// Vulnerable pattern from Pheasant Network:
**Update**
Addressed in: `0508a14eb93180ea7b313978248663a60ccb5faa`.

**File(s) affected:**`PheasantNetworkBridgeChild.sol`

**Description:** The evidence submitted by the Relayer is not checked at all in the function `withdraw()`. This may be explained by the fact that the system is an optimistic bridge and that if the evidence provided is incorrect, it will be detected, and the Relayer will get slashed.

However, the current system makes the following scenario possible:

1.   One user sends th
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in bridge relayer exploit logic allows exploitation through missing validation, 
func secureBridgeRelayerExploit(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 4
- **Affected Protocols**: Pheasant Network
- **Validation Strength**: Single auditor

---

## 4. Bridge Freeze Halt

### Overview

Implementation flaw in bridge freeze halt logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 2.

> **Key Finding**: This bug report is about the Ethereum Oracles watch for events on the Gravity.sol contract on the Ethereum blockchain, which is performed in the check_for_events and eth_oracle_main_loop functions. The code snippet leverages the web30 library to check for events from the starting_block to the latest

### Vulnerability Description

#### Root Cause

Implementation flaw in bridge freeze halt logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies bridge freeze halt in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to bridge operations

### Vulnerable Pattern Examples

**Example 1: [H-03] Freeze The Bridge Via Large ERC20 Names/Symbols/Denoms** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-03-freeze-the-bridge-via-large-erc20-namessymbolsdenoms.md`
```go
let erc20_deployed = web3
    .check_for_events(
        starting_block.clone(),
        Some(latest_block.clone()),
        vec![gravity_contract_address],
        vec![ERC20_DEPLOYED_EVENT_SIG],
    )
    .await;
```

**Example 2: [H-04] Large Validator Sets/Rapid Validator Set Updates May Freeze the Bridge or** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-04-large-validator-setsrapid-validator-set-updates-may-freeze-the-bridge-or-re.md`
```go
let mut all_valset_events = web3
    .check_for_events(
        end_search.clone(),
        Some(current_block.clone()),
        vec![gravity_contract_address],
        vec![VALSET_UPDATED_EVENT_SIG],
    )
    .await?;
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in bridge freeze halt logic allows exploitation through missing validation, inco
func secureBridgeFreezeHalt(ctx sdk.Context) error {
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
- **Affected Protocols**: Althea Gravity Bridge
- **Validation Strength**: Single auditor

---

## 5. Bridge Observer Exploit

### Overview

Implementation flaw in bridge observer exploit logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 6 audit reports with severity distribution: HIGH: 1, MEDIUM: 5.

> **Key Finding**: This bug report discusses a vulnerability in the Solana-Zetachain bridge that allows a single entity with admin or observer role to drain the bridge. This is due to a lack of validation on the Solana transaction's meta, which allows for spoofed deposits to be processed as valid. This can result in t

### Vulnerability Description

#### Root Cause

Implementation flaw in bridge observer exploit logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies bridge observer exploit in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to bridge operations

### Vulnerable Pattern Examples

**Example 1: Malicious observer can drain Solana bridge by adding failed deposit transaction ** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-1-malicious-observer-can-drain-solana-bridge-by-adding-failed-deposit-transact.md`
```
// Vulnerable pattern from ZetaChain Cross-Chain:
Source: https://github.com/sherlock-audit/2025-04-zetachain-cross-chain-judging/issues/58
```

**Example 2: [M-10] A single malicious observer can exploit the infinite gas meter to grief Z** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-10-a-single-malicious-observer-can-exploit-the-infinite-gas-meter-to-grief-zet.md`
```go
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
109: 				anteHandler = newCosmosAnteHandlerNoGasLimit(options)
110: 			} else {
111: 				anteHandler = newCosmosAnteHandler(options)
112: 			}
... 		// [...]
119: }
```

**Example 3: Removing an observer doesn't update an active ballot's voter list, leading to de** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-13-removing-an-observer-doesnt-update-an-active-ballots-voter-list-leading-to-.md`
```go
ballot = types.Ballot{
	Index:                "",
	BallotIdentifier:     index,
	VoterList:            observerSet.ObserverList,
	Votes:                types.CreateVotes(len(observerSet.ObserverList)),
	ObservationType:      observationType,
	BallotThreshold:      cp.BallotThreshold,
	BallotStatus:         types.BallotStatus_BallotInProgress,
	BallotCreationHeight: ctx.BlockHeight(),
}
```

**Variant: Bridge Observer Exploit - MEDIUM Severity Cases** [MEDIUM]
> Found in 5 reports:
> - `reports/cosmos_cometbft_findings/m-10-a-single-malicious-observer-can-exploit-the-infinite-gas-meter-to-grief-zet.md`
> - `reports/cosmos_cometbft_findings/m-13-removing-an-observer-doesnt-update-an-active-ballots-voter-list-leading-to-.md`
> - `reports/cosmos_cometbft_findings/m-18-a-single-malicious-observer-can-fill-the-block-space-with-msggaspricevoter-.md`

**Variant: Bridge Observer Exploit in ZetaChain Cross-Chain** [HIGH]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/h-1-malicious-observer-can-drain-solana-bridge-by-adding-failed-deposit-transact.md`
> - `reports/cosmos_cometbft_findings/m-13-removing-an-observer-doesnt-update-an-active-ballots-voter-list-leading-to-.md`
> - `reports/cosmos_cometbft_findings/m-8-malicious-observer-can-block-messages-added-through-the-inbound-tracker.md`

**Variant: Bridge Observer Exploit in ZetaChain** [MEDIUM]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/m-10-a-single-malicious-observer-can-exploit-the-infinite-gas-meter-to-grief-zet.md`
> - `reports/cosmos_cometbft_findings/m-18-a-single-malicious-observer-can-fill-the-block-space-with-msggaspricevoter-.md`
> - `reports/cosmos_cometbft_findings/m-25-observer-can-temporarily-halt-chain.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in bridge observer exploit logic allows exploitation through missing validation,
func secureBridgeObserverExploit(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 1, MEDIUM: 5
- **Affected Protocols**: ZetaChain, ZetaChain Cross-Chain
- **Validation Strength**: Moderate (2 auditors)

---

## 6. Bridge Denom Handling

### Overview

Implementation flaw in bridge denom handling logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 2.

> **Key Finding**: This bug report is about the Ethereum Oracles watch for events on the Gravity.sol contract on the Ethereum blockchain, which is performed in the check_for_events and eth_oracle_main_loop functions. The code snippet leverages the web30 library to check for events from the starting_block to the latest

### Vulnerability Description

#### Root Cause

Implementation flaw in bridge denom handling logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies bridge denom handling in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to bridge operations

### Vulnerable Pattern Examples

**Example 1: [H-03] Freeze The Bridge Via Large ERC20 Names/Symbols/Denoms** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-03-freeze-the-bridge-via-large-erc20-namessymbolsdenoms.md`
```go
let erc20_deployed = web3
    .check_for_events(
        starting_block.clone(),
        Some(latest_block.clone()),
        vec![gravity_contract_address],
        vec![ERC20_DEPLOYED_EVENT_SIG],
    )
    .await;
```

**Example 2: [H-04] Large Validator Sets/Rapid Validator Set Updates May Freeze the Bridge or** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-04-large-validator-setsrapid-validator-set-updates-may-freeze-the-bridge-or-re.md`
```go
let mut all_valset_events = web3
    .check_for_events(
        end_search.clone(),
        Some(current_block.clone()),
        vec![gravity_contract_address],
        vec![VALSET_UPDATED_EVENT_SIG],
    )
    .await?;
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in bridge denom handling logic allows exploitation through missing validation, i
func secureBridgeDenomHandling(ctx sdk.Context) error {
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
- **Affected Protocols**: Althea Gravity Bridge
- **Validation Strength**: Single auditor

---

## Detection Patterns

### Automated Detection
```
# Bridge Replay Attack
grep -rn 'bridge|replay|attack' --include='*.go' --include='*.sol'
# Bridge Token Accounting
grep -rn 'bridge|token|accounting' --include='*.go' --include='*.sol'
# Bridge Relayer Exploit
grep -rn 'bridge|relayer|exploit' --include='*.go' --include='*.sol'
# Bridge Freeze Halt
grep -rn 'bridge|freeze|halt' --include='*.go' --include='*.sol'
# Bridge Observer Exploit
grep -rn 'bridge|observer|exploit' --include='*.go' --include='*.sol'
# Bridge Denom Handling
grep -rn 'bridge|denom|handling' --include='*.go' --include='*.sol'
```

## Keywords

`account`, `accounting`, `active`, `adding`, `amount`, `another`, `appchain`, `assumes`, `attack`, `avoid`, `blocks`, `bond`, `bridge`, `chain`, `channel`, `circulation`, `collision`, `compensation`, `cosmos`, `deadlocks`, `denom`, `deposit`, `drain`, `evidence`, `exploit`, `failed`, `fork`, `freeze`, `from`, `getting`
