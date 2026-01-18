# LayerZero Bridge - Quick Knowledge Reference

> **Purpose**: Fast lookup reference for the `layerzero-reasoning-agent`. Contains condensed reasoning prompts, checklists, and vulnerability signatures.

---

## Core Security Requirements

| Check | Required | Attack If Missing |
|-------|----------|-------------------|
| NonblockingLzApp | ✓ | Channel blocking |
| minDstGasLookup | ✓ | Gas griefing DoS |
| receive() function | ✓ | Refund reverts |
| forceResumeReceive | ✓ | Permanent DoS |
| Peer validation | ✓ | Malicious messages |

---

## Vulnerability Quick Checklist

### ⚠️ Category 1: Channel Blocking

**One-liner**: Failed lzReceive blocks all subsequent messages from that source chain.

**Quick Checks:**
- [ ] Does contract inherit NonblockingLzApp (not just LzApp)?
- [ ] Are there external calls INSIDE _nonblockingLzReceive?
- [ ] Can those calls drain gas before try-catch?
- [ ] Is forceResumeReceive implemented?
- [ ] Is retryMessage available?

**Exploit Signature:**
```solidity
// ❌ Direct LzApp - any revert blocks channel
contract VulnerableBridge is LzApp {
    function lzReceive(...) external {
        _processPayload(payload);  // Revert = blocked!
    }
}
```

**Reasoning Prompt:**
> "If I send a message designed to revert, what happens to all future messages?"

---

### ⚠️ Category 2: Minimum Gas Validation

**One-liner**: Attacker passes insufficient gas, causing destination revert and channel blocking.

**Quick Checks:**
- [ ] Is minDstGasLookup set per packet type per chain?
- [ ] Are user-supplied adapterParams validated?
- [ ] Is there any way to bypass minimum gas check?

**Exploit Signature:**
```solidity
// ❌ No minimum gas validation
function bridge(bytes calldata _adapterParams) external payable {
    _lzSend(dstChain, payload, payable(msg.sender), address(0), 
            _adapterParams,  // ❌ User controls, no validation!
            msg.value);
}
```

**Secure Check:**
```solidity
// ✅ Validate minimum gas
uint256 gasLimit = _getGasLimit(_adapterParams);
require(gasLimit >= minDstGasLookup[_dstChainId][_packetType], "Gas too low");
```

**Reasoning Prompt:**
> "If I pass 10000 gas but lzReceive needs 200000, what happens?"

---

### ⚠️ Category 3: Gas Estimation & Fee Calculation

**One-liner**: Wrong gas estimation causes failed cross-chain messages or wasted fees.

**Quick Checks:**
- [ ] Are per-chain gas configs set (not single value)?
- [ ] Does quoteLayerZeroFee use the ACTUAL payload?
- [ ] Is native value passed to _lzSend?

**Exploit Signature:**
```solidity
// ❌ Same gas for all destination chains
uint256 constant BASE_GAS = 100000;  // Insufficient for some chains!

// ❌ Wrong payload in fee estimation
function quote() view returns (uint256) {
    bytes memory payload = "";  // ❌ Empty, actual is longer!
    return lzEndpoint.estimateFees(chainId, address(this), payload, ...);
}
```

**Reasoning Prompt:**
> "If Arbitrum needs 200k gas but I estimated with mainnet costs, will it work?"

---

### ⚠️ Category 4: Fee Refund Handling

**One-liner**: Excess fees can't be refunded, causing reverts or lost funds.

**Quick Checks:**
- [ ] Does contract have `receive() external payable {}`?
- [ ] Is refundAddress the user (not the contract)?
- [ ] Can withdrawRefunds() be called?

**Exploit Signature:**
```solidity
// ❌ No receive function - refunds revert the tx
contract VulnerableOFT is OFT {
    // Missing: receive() external payable {}
    
    function _lzReceive(...) internal {
        IOFT(token).send{value: msg.value}(
            ...,
            address(this)  // ❌ Refund here, but no receive()!
        );
    }
}
```

**Secure Pattern:**
```solidity
contract SecureOFT is OFT {
    receive() external payable {}  // ✅ Can receive refunds
    
    function withdrawRefunds() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }
}
```

**Reasoning Prompt:**
> "If LayerZero refunds excess fees and the contract can't receive ETH, what happens?"

---

### ⚠️ Category 5: Payload Size

**One-liner**: Large payload/toAddress can cause unexpected gas costs or DOS.

**Quick Checks:**
- [ ] Are there length limits on user-supplied data?
- [ ] Is toAddress validated (not arbitrary length)?
- [ ] Is payload size reasonable for gas limit?

**Exploit Signature:**
```solidity
// ❌ Unbounded toAddress
function sendFrom(
    address _from,
    uint16 _dstChainId,
    bytes calldata _toAddress,  // ❌ Attacker passes huge value
    ...
) external payable {
    // Gas cost increases with _toAddress length
}
```

**Reasoning Prompt:**
> "If toAddress is 10KB instead of 32 bytes, how much extra gas is needed?"

---

### ⚠️ Category 6: Composed Messages (lzCompose)

**One-liner**: Composed message tokens can be stolen by anyone calling execution.

**Quick Checks:**
- [ ] Is lzCompose wrapped in try-catch?
- [ ] Is there access control on composed message execution?
- [ ] Can tokens be claimed separately from execution?

**Exploit Signature:**
```solidity
// ❌ No try-catch, failure blocks channel
function lzCompose(...) external {
    _executeAction(data);  // If this reverts, funds stuck!
}

// ❌ Anyone can execute with different params
function executeComposed(bytes calldata params) external {
    // No validation that params match original intent
}
```

**Reasoning Prompt:**
> "If composed message arrives with 1000 USDC, can I claim them with different params?"

---

### ⚠️ Category 7: OFT/ONFT Decimal Issues

**One-liner**: Decimal mismatch between chains causes fund loss or reverts.

**Quick Checks:**
- [ ] Is sharedDecimals consistent across all chains?
- [ ] What happens to "dust" from normalization?
- [ ] Is denormalizeAmount handled correctly?

**Exploit Signature:**
```solidity
// Chain A: 18 decimals, Chain B: 6 decimals
// sharedDecimals = 6

// User sends: 1_000_000_000_000_000_001 (18 decimals)
// Normalized:               1_000_001 (6 decimals)  
// Dust lost: 000_000_000_001 wei

// ❌ If local decimals differ and not handled:
function send(...) {
    uint256 normalizedAmount = amount / 10**(localDecimals - sharedDecimals);
    // Dust is lost forever!
}
```

**Reasoning Prompt:**
> "If I send 1 wei + dust from 18-decimal chain, how much arrives on 6-decimal chain?"

---

### ⚠️ Category 8: Peer Configuration

**One-liner**: Malicious peer configuration can steal or block funds.

**Quick Checks:**
- [ ] Is setPeer access controlled?
- [ ] Is peer validated before accepting messages?
- [ ] Can same-chain peer be set (causing infinite loops)?

**Exploit Signature:**
```solidity
// ❌ Anyone can set peer
function setPeer(uint32 _eid, bytes32 _peer) external {
    peers[_eid] = _peer;  // ❌ No access control!
}
```

**Reasoning Prompt:**
> "If I can set peer to my malicious contract, what messages can I inject?"

---

### ⚠️ Category 9: Stargate/sgReceive

**One-liner**: sgReceive runs out of gas, tokens stuck in Stargate.

**Quick Checks:**
- [ ] Is sgReceive gas limit sufficient for all operations?
- [ ] Is dstGasForCall hardcoded or configurable?
- [ ] What happens if sgReceive reverts?

**Exploit Signature:**
```solidity
// ❌ Fixed gas limit too low
uint256 constant DST_GAS = 100000;  // Insufficient for complex operations

function participate(...) external {
    router.swap(..., dstGasForCall: DST_GAS, ...);  // ❌ Hardcoded!
}
```

**Reasoning Prompt:**
> "If sgReceive needs 500k gas but only has 100k, where are my tokens?"

---

### ⚠️ Category 10: Cross-Chain Payload Validation

**One-liner**: Attacker crafts payload to steal tokens or manipulate state.

**Quick Checks:**
- [ ] Are cross-chain parameters validated on destination?
- [ ] Can msg.sender on source be spoofed in payload?
- [ ] Are there separate functions for different payload types?

**Exploit Signature:**
```solidity
// ❌ Trusts payload.from without validation
function _lzReceive(..., bytes memory payload) internal {
    (address from, address to, uint256 amount) = abi.decode(payload, ...);
    token.transferFrom(from, to, amount);  // ❌ 'from' is attacker-controlled!
}
```

**Reasoning Prompt:**
> "If I control the payload, can I make it look like the victim sent tokens?"

---

## NonblockingLzApp Pattern

```solidity
// ✅ SECURE: Proper NonblockingLzApp with recovery
contract SecureBridge is NonblockingLzApp {
    mapping(uint16 => mapping(bytes => mapping(uint64 => bytes32))) public failedMessages;
    
    function _nonblockingLzReceive(
        uint16 _srcChainId,
        bytes memory _srcAddress,
        uint64 _nonce,
        bytes memory _payload
    ) internal override {
        // All dangerous operations in try-catch
        try this.processPayload(_srcChainId, _payload) {
            // Success
        } catch {
            // Store for retry
            failedMessages[_srcChainId][_srcAddress][_nonce] = keccak256(_payload);
            emit MessageFailed(_srcChainId, _srcAddress, _nonce, _payload);
        }
    }
    
    function retryMessage(
        uint16 _srcChainId,
        bytes memory _srcAddress,
        uint64 _nonce,
        bytes memory _payload
    ) external {
        bytes32 payloadHash = failedMessages[_srcChainId][_srcAddress][_nonce];
        require(payloadHash != bytes32(0), "No stored message");
        require(keccak256(_payload) == payloadHash, "Invalid payload");
        
        delete failedMessages[_srcChainId][_srcAddress][_nonce];
        this.processPayload(_srcChainId, _payload);
    }
    
    receive() external payable {}  // Accept refunds
    
    function forceResumeReceive(uint16 _srcChainId, bytes calldata _srcAddress) 
        external onlyOwner 
    {
        lzEndpoint.forceResumeReceive(_srcChainId, _srcAddress);
    }
}
```

---

## Keywords for Code Search

```bash
# Channel blocking patterns
rg -n "LzApp|NonblockingLzApp|lzReceive|storedPayload|forceResumeReceive"

# Gas validation patterns
rg -n "adapterParams|minDstGas|gasLimit|dstGasForCall"

# Refund patterns
rg -n "refundAddress|receive\(\)|payable\(msg.sender\)"

# OFT/ONFT patterns  
rg -n "OFT|ONFT|sharedDecimals|normalizeAmount|removeDust"

# Composed message patterns
rg -n "lzCompose|compose|sgReceive"

# Peer configuration
rg -n "setPeer|trustedRemote|peers\["
```

---

## References

- Full Database: [layerzero-integration-vulnerabilities.md](../../DB/bridge/layerzero/layerzero-integration-vulnerabilities.md)
- Main Agent: [layerzero-reasoning-agent.md](../layerzero-reasoning-agent.md)
- LayerZero V2 Docs: [docs.layerzero.network](https://docs.layerzero.network/v2)
