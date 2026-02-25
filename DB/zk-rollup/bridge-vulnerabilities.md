---
# Core Classification
protocol: generic
chain: everychain
category: zk_rollup_bridge
vulnerability_type: bridge_reentrancy|token_accounting|message_replay|wrong_token_order|censorship|owner_rug|selector_mismatch

# Attack Vector Details
attack_type: reentrancy|replay_attack|fund_theft|signature_replay|censorship|dos
affected_component: token_bridge|l1_bridge|l2_bridge|message_channel|router|relayer|adapter

# Technical Primitives
primitives:
  - token_bridge
  - l1_bridge
  - l2_bridge
  - bridge_adapter
  - message_relay
  - signature_replay
  - domain_separator
  - remote_token
  - ERC1155_selector
  - USDC_adapter
  - starknet_bridge
  - withdrawal_helper
  - bridge_suspension
  - token_order

# Impact Classification
severity: high
impact: fund_theft|accounting_corruption|bridge_dos|censorship|locked_funds
exploitability: 0.35
financial_impact: high

# Context Tags
tags:
  - zk_rollup
  - bridge
  - token_bridge
  - reentrancy
  - signature_replay
  - fund_theft
  - ZKSync
  - Optimism
  - LayerZero
  - starknet
  - ERC1155
  - USDC

language: solidity
version: all
---

## References & Source Reports

### Token Accounting and Token Mapping Errors

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Token Bridge Reentrancy Corrupts Token Accounting | `reports/zk_rollup_findings/token-bridge-reentrancy-can-corrupt-token-accounting.md` | HIGH | Multiple |
| L1BlastBridge Wrong Token Order for USD Yield Tokens | `reports/zk_rollup_findings/l1blastbridge-uses-wrong-token-order-when-bridging-usd-yield-tokens.md` | HIGH | Sherlock |
| Owner Changes remote_token to Steal Bridged Funds | `reports/zk_rollup_findings/m-02-owner-can-steal-all-funds-locked-in-bridge-by-changing-remote_token-value.md` | MEDIUM | Multiple |
| ERC-20 Representation of Native Currency Drains Pool | `reports/zk_rollup_findings/erc-20-representation-of-native-currency-can-be-used-to-drain-native-currency-po.md` | HIGH | Multiple |
| Wrong ERC1155 Selector Causes Token Loss During Bridging | `reports/zk_rollup_findings/using-the-wrong-selector-causes-token-loss-during-erc1155-bridging.md` | HIGH | Multiple |
| stale inflationMultiplier in L1EcoBridge | `reports/zk_rollup_findings/h-1-stale-inflationmultiplier-in-l1ecobridge.md` | HIGH | Sherlock |
| Not All ERC20 Tokens Can Be Bridged (hardcoded predicate) | `reports/zk_rollup_findings/m-2-not-all-erc20-tokens-can-be-bridged-because-of-hardcoded-predicate_address.md` | MEDIUM | Multiple |

### Signature Replay and Message Replay

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Router Signatures Replayed on Destination Domain | `reports/zk_rollup_findings/router-signatures-can-be-replayed-when-executing-messages-on-the-destination-dom.md` | HIGH | Multiple |
| Verifier Signatures Can Be Replayed | `reports/zk_rollup_findings/verifier-signatures-can-be-replayed.md` | HIGH | Multiple |
| Signed Swap Digest Lacks Domain Separator | `reports/zk_rollup_findings/signed-swap-digest-lacks-a-domain-separator.md` | HIGH | Multiple |
| Relayer Uses Valid Evidence of One Trade for Another | `reports/zk_rollup_findings/relayer-can-use-valid-evidence-of-one-trade-to-avoid-getting-slashed-for-another.md` | HIGH | Multiple |

### USDC and Adapter Vulnerabilities

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| USDC Sent Locked if _to Is Blacklisted | `reports/zk_rollup_findings/usdc-sent-may-be-permanently-lockedburnt-inby-the-adapter-if-the-_to-address-is-.md` | MEDIUM | Multiple |
| SyncSwap swapFrom Doesn't Encode Native ETH Correctly | `reports/zk_rollup_findings/syncswap_swapfrom-does-not-encode-native-eth-correctly.md` | HIGH | Multiple |

### Message Channel DoS and Censorship

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| DoS Attack Can Prevent Teleports | `reports/zk_rollup_findings/a-dos-attack-can-prevent-teleports.md` | MEDIUM | Multiple |
| Design Flaw in Bridge Contract Suspension Mechanism | `reports/zk_rollup_findings/design-flaw-in-bridge-contract-suspension-mechanism-phase-1.md` | MEDIUM | Multiple |
| Malicious Proposer Can DoS Bridge Withdrawals | `reports/zk_rollup_findings/m-06-malicious-proposer-can-dos-bridge-withdrawals.md` | MEDIUM | Multiple |
| Rate Limiters Can Lead to DoS | `reports/zk_rollup_findings/rate-limiters-can-lead-to-a-denial-of-service-attack.md` | MEDIUM | Multiple |
| Single Reverting Withdrawal Blocks Queue | `reports/zk_rollup_findings/single-reverting-withdrawal-can-block-the-basistradevault-withdrawal-queue.md` | HIGH | Multiple |
| Potential Blockage of User Withdrawals When Bridge Disabled | `reports/zk_rollup_findings/potential-blockage-of-user-withdrawals-when-bridge-is-disabled-in-withdrawtokens.md` | MEDIUM | Multiple |

### Starknet-Specific Bridge Issues

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Starknet Tokens with use_withdraw_auto Unrecoverable | `reports/zk_rollup_findings/starknet-tokens-deposited-with-use_withdraw_auto-can-never-be-withdrawn.md` | HIGH | Multiple |
| Tokens Irrecoverable if L1 Not ERC721 Receiver | `reports/zk_rollup_findings/tokens-irrecoverable-by-owner-on-l1-if-not-an-erc721-receiver.md` | HIGH | Multiple |

---

## Vulnerability Title

**Cross-Chain Bridge Vulnerabilities — Reentrancy, Token Accounting, Signature Replay, and Withdrawal DoS**

### Overview

Bridge vulnerabilities are among the most economically devastating in DeFi, with billions lost to exploits. ZK rollup bridges are particularly complex: they must maintain accurate token accounting across two chains, handle ETH/ERC20/ERC721/ERC1155 differently, implement replay protection for cross-chain messages, and provide uncensorable withdrawal paths. Common issues include accounting corruption via reentrancy, wrong token order in swap-based bridges, signature replay across chains, and withdrawal queue DoS via a single reverting transaction.

---

### Vulnerability Description

#### Root Cause

1. **Reentrancy in token accounting**: Bridge contracts update internal accounting after external calls, allowing re-entrant calls to exploit inconsistent state
2. **Token pair ordering**: Bridges that swap token pairs may reverse A and B, causing incorrect routing
3. **No domain separator**: Signed messages without domain separator can be replayed across chains
4. **Hardcoded remote_token**: Using a mutable remote_token for bridge token mapping allows owner-controlled theft
5. **Wrong function selector**: Using incorrect ERC1155 `safeTransferFrom` selector causes token loss during bridging
6. **USDC blacklist**: Bridges that can't handle USDC blacklisted address scenarios permanently lock/burn USDC

---

### Pattern 1: Token Bridge Reentrancy Corrupts Accounting

**Frequency**: 3/431 reports | **Validation**: Strong

#### Attack Scenario

1. User calls bridge with an ERC777 or callback-capable token (e.g., ERC1363)
2. Bridge receives tokens and starts processing the deposit
3. Before updating internal balance accounting, bridge makes an external call (e.g., callback notification)
4. Attacker's token contract re-enters the bridge's deposit function
5. Since accounting isn't updated, the second deposit appears legitimate at the pre-attack balance
6. Attacker drains the bridge pool

**Example 1: Reentrancy in Token Bridge** [HIGH]
```solidity
// ❌ VULNERABLE: Bridge processes deposit with external call before state update
contract TokenBridge {
    mapping(address => uint256) public tokenSupply; // Token supply on L2
    
    function deposit(address token, uint256 amount) external {
        // Transfer tokens first
        IERC20(token).transferFrom(msg.sender, address(this), amount);
        
        // ❌ External call (ERC777 hook fires here) → re-enter before state update
        _notifyL2(msg.sender, token, amount); // External call!
        
        // State update happens AFTER external call → too late, re-entrant call already exploited
        tokenSupply[token] += amount;  // BUG: should be first
    }
}
```

**Fix:**
```solidity
// ✅ SECURE: Update state BEFORE making any external calls (CEI pattern)
contract TokenBridge {
    mapping(address => uint256) public tokenSupply;
    bool private _bridgeLock;
    
    modifier nonReentrant() {
        require(!_bridgeLock, "Reentrant call");
        _bridgeLock = true;
        _;
        _bridgeLock = false;
    }
    
    function deposit(address token, uint256 amount) external nonReentrant {
        // Update state FIRST
        tokenSupply[token] += amount;
        // Then do external interactions
        IERC20(token).transferFrom(msg.sender, address(this), amount);
        _notifyL2(msg.sender, token, amount);
    }
}
```

---

### Pattern 2: Wrong Token Order in Bridge Causes Incorrect Routing

**Frequency**: 2/431 reports | **Validation**: Strong (Sherlock - Blast)

#### Root Cause

Bridges that handle token pairs (e.g., yield-bearing USD tokens: USDB/USDW) sometimes accept token A and B as arguments but switch their positions internally. When bridging from L1 to L2, the bridge must map L1 token → L2 token correctly. Swapping the order causes users to receive the wrong token on the destination chain.

**Example 2: L1BlastBridge Wrong USD Yield Token Order** [HIGH]
```solidity
// ❌ VULNERABLE: L1BlastBridge swaps token order when emitting event
// Users think they're bridging USDB → L2, but actually bridge USDW → L2
function _initiateERC20Deposit(
    address _l1Token,
    address _l2Token,
    address _from,
    address _to,
    uint256 _amount,
    uint32 _l2Gas,
    bytes memory _data
) internal {
    // ...
    // BUG: _l1Token and _l2Token are swapped in the cross-domain message
    sendCrossDomainMessage(
        l2TokenBridge,
        _l2Gas,
        abi.encodeWithSelector(IL2ERC20Bridge.finalizeDeposit.selector,
            _l2Token, // Should be _l1Token (the token being deposited)
            _l1Token, // Should be _l2Token (the L2 counterpart)
            _from, _to, _amount, _data)
    );
}
```

**Fix:**
```solidity
// ✅ SECURE: Verify token arguments are in correct order
sendCrossDomainMessage(
    l2TokenBridge,
    _l2Gas,
    abi.encodeWithSelector(IL2ERC20Bridge.finalizeDeposit.selector,
        _l1Token, // L1 source token (first)
        _l2Token, // L2 destination token (second)
        _from, _to, _amount, _data)
);
```

---

### Pattern 3: Router Signatures Replay Across Chains

**Frequency**: 3/431 reports | **Validation**: Strong

#### Root Cause

Cross-chain routers use off-chain signatures to authorize message execution. If the signed message digest doesn't include a domain separator (containing `chainId` + `verifyingContract`), the same signature valid on chain A can be submitted on chain B where the same router contract is deployed, re-executing the message on the wrong chain.

**Example 3: Signature Replay via Missing Domain Separator** [HIGH]
```solidity
// ❌ VULNERABLE: Signed message has no domain separator
// Signature created for Optimism can be replayed on Arbitrum
function executeMessage(
    address target,
    bytes calldata data,
    bytes calldata signature
) external {
    // Hash doesn't include chainId or verifyingContract!
    bytes32 msgHash = keccak256(abi.encode(target, data, nonce));
    address signer = recoverSigner(msgHash, signature);
    require(signer == authorizedRelayer, "Invalid signer");
    nonce++;
    (bool success,) = target.call(data);
}
```

**Fix:**
```solidity
// ✅ SECURE: Include EIP-712 domain separator in signed digest
bytes32 constant DOMAIN_TYPEHASH = keccak256(
    "EIP712Domain(string name,uint256 chainId,address verifyingContract)"
);

function _domainSeparator() internal view returns (bytes32) {
    return keccak256(abi.encode(DOMAIN_TYPEHASH, 
        keccak256("CrossChainRouter"), 
        block.chainid,           // Chain-specific
        address(this)            // Contract-specific
    ));
}

function executeMessage(
    address target, bytes calldata data, bytes calldata signature
) external {
    bytes32 structHash = keccak256(abi.encode(MESSAGE_TYPEHASH, target, keccak256(data), nonce));
    bytes32 digest = keccak256(abi.encodePacked("\x19\x01", _domainSeparator(), structHash));
    address signer = recoverSigner(digest, signature);
    require(signer == authorizedRelayer, "Invalid signer");
    nonce++;
    (bool success,) = target.call(data);
}
```

---

### Pattern 4: Wrong ERC1155 Selector Locks Tokens in Bridge

**Frequency**: 1/431 reports | **Validation**: Strong

#### Root Cause

ERC1155 has two transfer functions: `safeTransferFrom(address,address,uint256,uint256,bytes)` and `safeBatchTransferFrom(...)`. If a bridge uses the wrong 4-byte function selector when calling the token contract during withdrawal, the call reverts. All ERC1155 tokens bridged with that token ID become permanently locked in the bridge.

**Example 4: Wrong Selector for ERC1155 Transfer** [HIGH]
```solidity
// ❌ VULNERABLE: Bridge uses wrong selector for ERC1155 safeTransferFrom
function withdrawERC1155(address token, address to, uint256 id, uint256 amount) internal {
    // BUG: .transfer.selector is ERC20's transfer(address,uint256)
    // This selector doesn't match ERC1155's safeTransferFrom signature
    bytes memory data = abi.encodeWithSelector(
        IERC20.transfer.selector, // WRONG: 0xa9059cbb
        to, amount
        // Missing: id, bytes("") parameters for ERC1155
    );
    (bool success,) = token.call(data);
    require(success, "Transfer failed"); // Always fails for ERC1155
}
```

**Fix:**
```solidity
// ✅ SECURE: Use correct ERC1155 function signature
function withdrawERC1155(address token, address to, uint256 id, uint256 amount) internal {
    IERC1155(token).safeTransferFrom(
        address(this), // from: the bridge contract
        to,            // recipient
        id,            // token ID
        amount,        // amount
        ""             // data: empty bytes
    );
}
```

---

### Pattern 5: USDC Blacklist Permanently Locks Bridge Funds

**Frequency**: 2/431 reports | **Validation**: Strong

#### Root Cause

USDC has a blacklist mechanism: blacklisted addresses cannot receive USDC transfers (the `transfer` call reverts). Bridge adapters that forward USDC to a `_to` address without checking whether `_to` is blacklisted will permanently lock (or burn) USDC in the adapter contract, with no recovery mechanism.

**Example 5: USDC Sent to Blacklisted Address Locks Funds** [MEDIUM]
```solidity
// ❌ VULNERABLE: Bridge adapter doesn't handle USDC blacklist
contract BridgeAdapter {
    address constant USDC = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;
    
    function withdrawTokens(address to, uint256 amount) external {
        // If `to` is blacklisted by USDC, this transfer REVERTS
        // The funds are permanently locked in this adapter
        USDC.transfer(to, amount); // Can revert if `to` is blacklisted
        // No fallback — user's USDC is stuck forever
    }
}
```

**Fix:**
```solidity
// ✅ SECURE: Implement fallback for USDC transfer failures
contract BridgeAdapter {
    mapping(address => uint256) public claimable; // Store failed transfers
    
    function withdrawTokens(address to, uint256 amount) external {
        (bool success,) = USDC.call(
            abi.encodeWithSignature("transfer(address,uint256)", to, amount)
        );
        if (!success) {
            // Store for alternative claim path (e.g., different address)
            claimable[to] += amount;
            emit WithdrawalFailed(to, amount);
        }
    }
    
    function claimTo(address newRecipient, uint256 amount) external {
        require(claimable[msg.sender] >= amount, "Insufficient claimable");
        claimable[msg.sender] -= amount;
        USDC.transfer(newRecipient, amount); // User provides non-blacklisted address
    }
}
```

---

### Pattern 6: Single Reverting Withdrawal Blocks Entire Queue

**Frequency**: 2/431 reports | **Validation**: Moderate

#### Root Cause

Vault or bridge withdrawal queues are processed in order (FIFO). If any single withdrawal in the queue causes the processing loop to revert (e.g., token transfer fails for a specific user), the entire queue is halted and no user can withdraw.

**Example 6: Queue DoS via Single Reverting Withdrawal** [HIGH]
```solidity
// ❌ VULNERABLE: Process all withdrawals in a loop — any revert blocks queue
function processWithdrawals() external {
    for (uint i = 0; i < withdrawalQueue.length; i++) {
        Withdrawal memory w = withdrawalQueue[i];
        // If this USDC transfer fails (blacklisted user), entire queue halts
        IERC20(w.token).transfer(w.recipient, w.amount); // Can revert!
        // All subsequent withdrawals blocked
    }
    delete withdrawalQueue;
}
```

**Fix:**
```solidity
// ✅ SECURE: Skip failing withdrawals (try/catch) and record for manual resolution
function processWithdrawals() external {
    for (uint i = 0; i < withdrawalQueue.length; i++) {
        Withdrawal memory w = withdrawalQueue[i];
        try IERC20(w.token).transfer(w.recipient, w.amount) {
            emit WithdrawalProcessed(w.recipient, w.token, w.amount);
        } catch {
            // Store failed withdrawal for manual processing
            failedWithdrawals.push(w);
            emit WithdrawalFailed(w.recipient, w.token, w.amount);
        }
    }
    delete withdrawalQueue;
}
```

---

### Impact Analysis

#### Technical Impact
- Bridge accounting corruption → infinite minting of backed tokens
- Token mapping errors → users receive wrong token on destination chain
- Signature replay → same transaction executed on multiple chains simultaneously
- Wrong ERC1155 selector → all bridged NFTs permanently locked

#### Business Impact
- Bridge exploits can drain hundreds of millions in TVL
- Incorrect token routing causes direct financial loss to users
- Queue DoS prevents all users from withdrawing during critical market events
- USDC blacklist scenarios permanently lock user funds

---

### Detection Patterns

```
1. deposit/withdraw functions that make external calls before updating storage (reentrancy)
2. Cross-chain message encoding where token pair arguments are passed in different order on each side
3. Signed message digests without keccak256(chainId, address(this)) in the hash
4. ERC1155 transfer calls using IERC20.transfer.selector instead of IERC1155 interface
5. USDC/USDT transfer calls without checking return value or using try/catch
6. Withdrawal queue processing in a loop without try/catch around each transfer
7. remote_token storage variable that can be updated by owner after deployment
8. bridge adapter functions that don't check USDC blacklist status
```

### Keywords for Search

`token bridge reentrancy`, `bridge accounting corruption`, `wrong token order bridge`, `L1BlastBridge token swap`, `signature replay bridge`, `domain separator missing bridge`, `ERC1155 wrong selector`, `USDC blacklist bridge locked`, `withdrawal queue DoS`, `single reverting withdrawal`, `bridge token mapping error`, `stale inflationary multiplier bridge`, `remote_token manipulation`, `cross-chain replay attack`, `bridge fund theft`, `bridge suspension DoS`, `rate limiter DoS bridge`
