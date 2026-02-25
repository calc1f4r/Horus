---
# Core Classification
protocol: generic
chain: zksync|scroll|optimism|arbitrum|taiko|linea|base
category: zk_rollup_messaging
vulnerability_type: l1_l2_message_failure|l2_l1_withdrawal_block|gas_theft|address_aliasing|message_ordering|eth_locked

# Attack Vector Details
attack_type: fund_loss|dos|gas_theft|message_ordering|eth_lock
affected_component: l1_l2_bridge|mailbox|bootloader|l2_to_l1_message_passer|messenger|value_simulator

# Technical Primitives
primitives:
  - L1ToL2Transaction
  - bootloader
  - MsgValueSimulator
  - address_aliasing
  - requestL2Transaction
  - l2ToL1Log
  - MessagePasser
  - OutputRoot
  - SpentOnPubdata
  - paymaster
  - forwardedEther
  - CrossDomainMessenger
  - forced_inclusion
  - message_ordering

# Impact Classification
severity: high
impact: fund_loss|dos|gas_theft|eth_locked
exploitability: 0.40
financial_impact: high

# Context Tags
tags:
  - zk_rollup
  - l1_l2_bridge
  - messaging
  - zksync
  - optimism
  - arbitrum
  - bootloader
  - address_aliasing
  - withdrawal
  - eth_locked
  - message_passer
  - paymaster

language: solidity
version: all
---

## References & Source Reports

### L1 → L2 Transaction Failures

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Loss of Funds When L1→L2 Tx Fails in Bootloader | `reports/zk_rollup_findings/m-03-loss-of-funds-for-the-sender-when-l1-l2-tx-fails-in-the-bootloader-on-l2.md` | MEDIUM | Spearbit |
| No Access to ETH on L2 via L1→L2 Transactions | `reports/zk_rollup_findings/m-09-lack-of-access-to-eth-on-l2-through-l1-l2-transactions.md` | MEDIUM | Multiple |
| Operator Steals Gas for L1→L2 Transactions | `reports/zk_rollup_findings/m-14-operator-can-steal-all-gas-provided-by-any-user-for-l1l2-transactions.md` | MEDIUM | Spearbit |
| MailboxRequestL2Transaction Checks Wrong Sender's Deposit Limit | `reports/zk_rollup_findings/m-15-mailboxrequestl2transaction-checks-the-deposit-limit-of-msgsender-l1wethbri.md` | MEDIUM | Spearbit |
| Gasless ETH Bridging from L1 to L2 | `reports/zk_rollup_findings/m-11-gasless-eth-bridging-from-l1-to-l2.md` | MEDIUM | Spearbit |
| Valid Transactions Cannot be Enqueued | `reports/zk_rollup_findings/h01-valid-transactions-cannot-be-enqueued.md` | HIGH | Multiple |

### Paymaster and Value Simulator Issues

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Paymaster Refunds spentOnPubdata to User (Should Burn) | `reports/zk_rollup_findings/h-01-paymaster-will-refund-spentonpubdata-to-user.md` | HIGH | Spearbit |
| MsgValueSimulator Non-Zero Value Calls Sender Itself | `reports/zk_rollup_findings/h-01-the-call-to-msgvaluesimulator-with-non-zero-msgvalue-will-call-to-sender-it.md` | HIGH | Spearbit |

### Address Aliasing Issues

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| ETH Locked via Address Aliasing | `reports/zk_rollup_findings/eth-can-be-locked-through-address-aliasing.md` | MEDIUM | Multiple |
| Preservation of msg.sender in ZKSync Breaks Trust | `reports/zk_rollup_findings/preservation-of-msgsender-in-zksync-could-break-certain-trust-assumption.md` | MEDIUM | Multiple |

### L2 → L1 Withdrawal Issues

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| BurnAmount from L2 to L1 Doesn't Account for Pending Withdrawals | `reports/zk_rollup_findings/burnamount-sent-from-l2-to-l1-may-not-be-accurate-as-it-does-not-account-for-pen.md` | MEDIUM | Multiple |
| Attacker Fills L2ToL1MessagePasser Merkle Tree Blocking Withdrawals | `reports/zk_rollup_findings/m-9-attacker-can-fill-merkle-tree-in-l2tol1messagepasser-blocking-any-future-wit.md` | MEDIUM | Sherlock |
| Multiple L3 Withdrawals Not Provable via OP Withdrawal | `reports/zk_rollup_findings/multiple-withdrawals-in-a-single-l3-transaction-are-not-provable-through-op-with.md` | MEDIUM | Multiple |
| Withdrawal Transactions Stuck if Output Root Reproposed | `reports/zk_rollup_findings/m-13-withdrawal-transactions-can-get-stuck-if-output-root-is-reproposed.md` | MEDIUM | Sherlock |
| Failed L1→L2 Transfers Lock Tokens if Replayed After Migration | `reports/zk_rollup_findings/temporary-failed-l1-to-l2-token-transfers-might-lock-tokens-in-l1-if-replayed-af.md` | MEDIUM | Multiple |
| L2 Bridge Hook Events Discarded | `reports/zk_rollup_findings/m-03-events-emitted-by-l2-bridge-hooks-are-discarded.md` | MEDIUM | Spearbit |
| Messages Destined for ZKSync Cannot be Processed | `reports/zk_rollup_findings/messages-destined-for-zksync-cannot-be-processed.md` | HIGH | Multiple |
| Message Channels Can Be Blocked | `reports/zk_rollup_findings/m-09-message-channels-can-be-blocked-resulting-in-dos.md` | MEDIUM | Multiple |
| CrossDomainMessenger Cannot Guarantee Replayability | `reports/zk_rollup_findings/m-1-crossdomainmessenger-does-not-successfully-guarantee-replayability-can-lose-.md` | MEDIUM | Sherlock |

---

## Vulnerability Title

**L1↔L2 Cross-Layer Messaging Vulnerabilities — Fund Loss, Gas Theft, and Withdrawal Blocks**

### Overview

L1→L2 and L2→L1 messaging is the critical infrastructure of rollup systems. Vulnerabilities here range from losing funds when L2 transactions fail during bootloader execution, to operators stealing gas, to ETH being permanently locked via address aliasing. L2→L1 withdrawals can be blocked by filling Merkle trees, stuck when output roots are reproposed, or made unprovable due to multi-layer architecture quirks.

---

### Vulnerability Description

#### Root Cause

1. **Failed bootloader handling**: When an L1→L2 tx fails mid-execution on the L2 bootloader, the refund logic may not correctly return all ETH/gas to the original sender
2. **Address aliasing**: Ethereum adds `0x1111...1111` to contract addresses when they initiate L1→L2 messages, breaking protocols that assume `msg.sender == L1_contract_address`
3. **Unbounded Merkle tree**: L2ToL1MessagePasser has a fixed-depth Merkle tree; once full, no new withdrawal proofs can be added
4. **Output root reproposal**: When an output root is disputed and reproposed, all pending withdrawal proofs for the old root become invalid
5. **Gas estimation mismatch**: L1→L2 gas limits may be insufficient, causing execution failure on L2 while ETH is already debited on L1

---

### Pattern 1: Loss of Funds When L1→L2 Transaction Fails in Bootloader

**Frequency**: 3/431 reports | **Validation**: Strong (ZKSync Spearbit audit)

#### Attack Scenario

1. User sends ETH + L1→L2 message via `requestL2Transaction()` on L1
2. The transaction is successfully included in an L2 batch but **fails during bootloader execution** (out-of-gas or contract revert)
3. On failure, the bootloader should refund ETH to the original L1 sender
4. Due to a bug, the refund is either not sent or sent to the wrong address (the aliased address, not the actual sender)
5. ETH is permanently lost — user sees their L1 ETH debited with nothing received on L2

**Example 1: Bootloader Failure Loses User ETH** [MEDIUM]
```solidity
// ❌ VULNERABLE: L1 Mailbox doesn't guarantee refund on L2 execution failure
// L2 transaction can fail in bootloader; refund goes to aliased address

// On L1:
function requestL2Transaction(
    address _contractL2,
    uint256 _l2Value,
    bytes calldata _calldata,
    uint256 _l2GasLimit,
    uint256 _l2GasPerPubdataByteLimit,
    bytes[] calldata _factoryDeps,
    address _refundRecipient
) external payable returns (bytes32 canonicalTxHash) {
    // ETH is taken from msg.sender on L1
    // If L2 execution fails: refund goes to _refundRecipient on L2
    // But if _refundRecipient is a contract, their address is ALIASED on L2
    // → refund arrives at alias address, not the real contract
}
```

**Fix:**
```solidity
// ✅ SECURE: Ensure refund recipient is explicitly set to an EOA or
// the L2 operator applies aliasing correction when sending refunds to L1 contracts
// Set _refundRecipient to an EOA address when calling from a contract
function requestL2TransactionSafe(...) external payable {
    address safeRefundRecipient = _isContract(_refundRecipient) 
        ? _undoL1ToL2Alias(_refundRecipient) 
        : _refundRecipient;
    return mailbox.requestL2Transaction{value: msg.value}(
        _contractL2, _l2Value, _calldata, _l2GasLimit,
        _l2GasPerPubdataByteLimit, _factoryDeps, safeRefundRecipient
    );
}
```

---

### Pattern 2: MsgValueSimulator Non-Zero Value Calls Sender Itself

**Frequency**: 1/431 reports | **Validation**: Strong (ZKSync Spearbit audit)

#### Root Cause

In ZKSync's system contract `MsgValueSimulator`, when a call is made with non-zero `msg.value`, the simulator is supposed to forward ETH and then call the target contract. Due to a bug in the implementation, the call target was set to `msg.sender` (the caller of `MsgValueSimulator`) rather than the intended `to` address. This causes infinite recursion or calls the wrong contract.

**Example 2: MsgValueSimulator Calls Wrong Target** [HIGH]
```solidity
// ❌ VULNERABLE: MsgValueSimulator.sol (ZKSync Era)
// When msg.value != 0, the call should go to `to` address
// But due to a bug, `msg.sender` was used as the call target
function simulate(
    address to,
    uint256 value,
    bool isSystemCall,
    bytes calldata data
) external payable {
    if (value != 0) {
        // BUG: calls msg.sender instead of `to`
        // This causes call to go BACK to the calling contract
        bool success = EfficientCall.rawCall(gasleft(), msg.sender, data);
        // Should be: EfficientCall.rawCall(gasleft(), to, data);
    }
}
```

---

### Pattern 3: Address Aliasing Locks ETH

**Frequency**: 3/431 reports | **Validation**: Strong

#### Root Cause

When L1 contracts send ETH to L2 via `requestL2Transaction`, Ethereum applies "address aliasing": the L2 `msg.sender` is the L1 contract address + `0x1111000000000000000000000000000000001111`. If an L2 contract checks `msg.sender == L1_contract`, this check fails because the aliased address is used. ETH arrives at an address no contract expects, and may be permanently locked.

**Example 3: Address Aliasing Breaks msg.sender Check** [MEDIUM]
```solidity
// ❌ VULNERABLE: L2 contract assumes msg.sender == L1 contract address
// But L1 contracts have their address aliased on L2
contract L2BridgeReceiver {
    address immutable L1_BRIDGE; // L1 bridge contract address
    
    function onL1Deposit(uint256 amount) external payable {
        // BUG: msg.sender is aliased address, NOT L1_BRIDGE
        // This check ALWAYS fails for L1 contract senders
        require(msg.sender == L1_BRIDGE, "Only L1 bridge");
        // ETH is received but locked — the check blocks any processing
    }
}
```

**Fix:**
```solidity
// ✅ SECURE: Apply address alias correction when receiving from L1 contracts
address constant ADDRESS_ALIAS_OFFSET = 0x1111000000000000000000000000000000001111;

function undoL1ToL2Alias(address l1Address) internal pure returns (address) {
    unchecked { return address(uint160(l1Address) + uint160(ADDRESS_ALIAS_OFFSET)); }
}

contract L2BridgeReceiver {
    address immutable L1_BRIDGE_ALIASED; // Pre-computed aliased address
    
    constructor(address l1Bridge) {
        L1_BRIDGE_ALIASED = undoL1ToL2Alias(l1Bridge);
    }
    
    function onL1Deposit(uint256 amount) external payable {
        require(msg.sender == L1_BRIDGE_ALIASED, "Only L1 bridge (aliased)");
        // Correctly handles L1 contract address aliasing
    }
}
```

---

### Pattern 4: Attacker Fills L2ToL1MessagePasser Merkle Tree

**Frequency**: 1/431 reports | **Validation**: Strong (Optimism - Sherlock)

#### Root Cause

The Optimism `L2ToL1MessagePasser` contract stores all L2→L1 withdrawal messages in a Merkle trie for later L1 proof verification. This trie has a maximum depth (or fixed array size). An attacker can spam cheap L2 messages to completely fill the Merkle trie. Once full, all new withdrawal attempts revert — no user can withdraw from L2 to L1 permanently.

**Example 4: DoS on L2→L1 Withdrawals** [MEDIUM]
```solidity
// ❌ VULNERABLE: L2ToL1MessagePasser has finite capacity
// An attacker can send enough cheap L2→L1 messages to fill the Merkle tree
// After filling, all new withdrawals revert with "Merkle tree full"

contract L2ToL1MessagePasser {
    MerkleTrie internal withdrawalTree;  // Fixed capacity!
    
    function initiateWithdrawal(address target, bytes calldata data) external payable {
        // Attacker spams this with near-zero value, filling the tree
        bytes32 messageHash = keccak256(abi.encode(...));
        withdrawalTree.insert(messageHash); // Reverts when tree is full
    }
}
```

---

### Pattern 5: Paymaster Refunds spentOnPubdata to User

**Frequency**: 1/431 reports | **Validation**: Strong (ZKSync Spearbit)

#### Root Cause

In ZKSync, `spentOnPubdata` represents gas consumed for L1 data availability publishing. This amount should be **burned** (not refunded) since the L2 operator already paid the corresponding L1 cost. A bug in the paymaster system caused `spentOnPubdata` to be included in the user refund, effectively double-spending — users pay for pubdata but receive it back, while the protocol absorbs the cost.

**Example 5: Pubdata Cost Erroneously Refunded** [HIGH]
```solidity
// ❌ VULNERABLE: Paymaster incorrectly includes spentOnPubdata in user refund
function _refundUser(
    address user,
    uint256 gasUsed,
    uint256 spentOnPubdata,
    uint256 gasPrice
) internal {
    // BUG: spentOnPubdata should be burned, not refunded
    uint256 refund = (gasUsed + spentOnPubdata) * gasPrice; // WRONG
    payable(user).transfer(refund);
    // Protocol is paying L1 pubdata cost twice
}
```

**Fix:**
```solidity
// ✅ SECURE: Burn spentOnPubdata; only refund unused computation gas
function _refundUser(
    address user,
    uint256 gasUsed,
    uint256 spentOnPubdata,
    uint256 gasPrice
) internal {
    // Only refund gas that wasn't used for computation (not pubdata)
    uint256 refund = gasUsed * gasPrice; // Exclude spentOnPubdata
    payable(user).transfer(refund);
    // spentOnPubdata is burned separately (sent to 0x0 or operator)
}
```

---

### Pattern 6: CrossDomainMessenger Cannot Guarantee Replayability

**Frequency**: 2/431 reports | **Validation**: Strong (Optimism - Sherlock)

#### Root Cause

The `CrossDomainMessenger` is supposed to allow failed L1→L2 messages to be replayed. However, if the message consumes more gas than estimated, it fails the `require(gasleft() >= gasLimit)` check and is marked as failed. Due to incorrect handling, the failed message is removed from the replay queue without being stored for future retry. The user's ETH is burned and the message is permanently lost.

**Example 6: Failed Message Not Replayable** [MEDIUM]
```solidity
// ❌ VULNERABLE: Failed L1→L2 messages not stored for replay
contract CrossDomainMessenger {
    function relayMessage(
        address target,
        address sender,
        bytes calldata message,
        uint256 messageNonce,
        uint256 gasLimit
    ) external {
        // If execution fails, the message nonce is consumed
        bool success = target.call{gas: gasLimit}(abi.encodeWithSelector(...));
        if (!success) {
            // BUG: message is marked as failed but NOT stored for retry
            failedMessages[hash] = false; // Should store for future replay
        }
    }
}
```

---

### Impact Analysis

#### Technical Impact
- ETH permanently lost/locked in aliased addresses or failed L1→L2 messages
- L2→L1 withdrawals completely blocked by Merkle tree exhaustion
- Double-spending via protocol subsidizing pubdata refunds incorrectly
- Failed messages unrecoverable if replay mechanism is broken

#### Business Impact
- Users lose bridged ETH with no recourse
- Protocol insolvency from incorrect pubdata accounting
- L2 chain becomes un-withdrawable (funds trapped)
- Reputation damage from permanent fund loss

---

### Secure Implementation

```solidity
// ✅ COMPLETE L1→L2 MESSAGE SAFETY CHECKLIST:
// 1. Always set an EOA as _refundRecipient when calling from a contract
// 2. Account for address aliasing when receiving messages from L1 contracts on L2  
// 3. Provide enough gas — use estimateGas before broadcasting L1→L2 transaction
// 4. Implement retry mechanism for failed L2 messages
// 5. Monitor L2ToL1MessagePasser capacity (add rate limiting to prevent exhaustion)

// ✅ Address aliasing check helper:
function applyL1ToL2Alias(address l1Address) internal pure returns (address l2Address) {
    unchecked {
        l2Address = address(uint160(l1Address) + uint160(0x1111000000000000000000000000000000001111));
    }
}
```

---

### Detection Patterns

```
1. L2 contracts checking msg.sender == hardcoded_L1_contract_address (missing alias offset)
2. requestL2Transaction() calls with contract as _refundRecipient
3. L1→L2 messages without explicit gas limit calculation (using arbitrary values)
4. Paymaster contracts including pubdata costs in user refunds
5. CrossDomainMessenger implementations without storage of failed messages for replay
6. L2ToL1MessagePasser without overflow/capacity protection
7. MsgValueSimulator calls where target address comes from msg.sender not the intended recipient
```

### Keywords for Search

`L1 to L2 message failure`, `bootloader execution failed`, `address aliasing ZKSync`, `address alias offset`, `L2ToL1MessagePasser full`, `withdrawal blocked Merkle tree`, `paymaster pubdata refund`, `spentOnPubdata refund bug`, `MsgValueSimulator wrong target`, `requestL2Transaction`, `CrossDomainMessenger replayability`, `L2 bridge ETH locked`, `failed L2 message unreplayable`, `output root reproposed withdrawal stuck`, `l2 to l1 withdrawal proof`, `forced inclusion`, `message ordering L2`, `ETH locked through aliasing`
