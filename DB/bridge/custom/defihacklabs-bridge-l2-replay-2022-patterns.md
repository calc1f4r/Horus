---
# Core Classification
protocol: generic
chain: ethereum, optimism, harmony
category: bridge
vulnerability_type: cross_chain_identity_and_custody

# Pattern Identity
root_cause_family: identity_and_custody_assumption
pattern_key: cross_chain_identity_mismatch | deployment_or_custody | deterministic_address_or_threshold | fund_loss

# Interaction Scope
interaction_scope: cross_chain
involved_contracts:
  - ProxyFactory
  - GnosisSafe
  - MultiSigWallet
  - BridgeLocker
  - cTUSD
  - TUSD_Legacy
  - TUSD_Current
path_keys:
  - create_nonce_collision | ProxyFactory.createProxy | ProxyFactory -> GnosisSafe (L2 address claim)
  - low_multisig_threshold | MultiSigWallet.submitTransaction | MultiSigWallet -> BridgeLocker.unlockToken
  - token_proxy_dual_address | cTUSD.sweepToken | cTUSD -> TUSD_Legacy.delegatecall -> TUSD_Current

# Attack Vector Details
attack_type: logical_error
affected_component: cross_chain_deployment, multisig_custody, token_identity

# Technical Primitives
primitives:
  - address_collision
  - create_nonce_determinism
  - create2
  - multisig_threshold
  - key_compromise
  - token_proxy_bypass
  - delegatecall_forwarding
  - sweep_guard

# Grep / Hunt-Card Seeds
code_keywords:
  - createProxy
  - create2
  - CREATE
  - nonce
  - submitTransaction
  - confirmTransaction
  - required
  - threshold
  - sweepToken
  - recoverToken
  - rescueToken
  - underlying
  - delegatecall
  - fallback

# Impact Classification
severity: critical
impact: fund_loss
exploitability: 0.6
financial_impact: critical

# Context Tags
tags:
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
  - DeFiHackLabs

# Version Info
language: solidity
version: ">=0.6.0"
---

## References & Source Reports

| Label | Source | Path / URL | Severity | Loss |
|-------|--------|------------|----------|------|
| [OPT-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-06/Optimism_exp.sol` | CRITICAL | $15M |
| [HAR-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-06/Harmony_multisig_exp.sol` | CRITICAL | $100M |
| [CTUSD-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-03/CompoundTusd_exp.sol` | CRITICAL | Full Market |

---

# Bridge & Cross-Chain Identity / Custody Patterns (2022)

## Overview

Three high-profile exploits from 2022 totaling **$115M+** that share a common theme: cross-chain and cross-contract identity assumptions fail when the mapping between addresses, keys, or token proxies is not consistent across execution contexts. (1) CREATE nonce replay allows claiming a Gnosis Safe address on L2 before the owner deploys (Optimism/Wintermute $15M), (2) a 2-of-5 multisig threshold means compromising 40% of keys grants full bridge control (Harmony $100M), and (3) a token's legacy proxy address bypasses an identity check that only compares against the current address (Compound TUSD — full cTUSD market).

### Agent Quick View

- Root cause statement: "This vulnerability exists because cross-chain deployments rely on CREATE nonce determinism without chain-specific salt (Optimism), bridge multisig thresholds are too low relative to the value secured (Harmony), or token identity checks only compare a single address without accounting for proxy aliases (Compound TUSD)."
- Pattern key: `cross_chain_identity_mismatch | deployment_or_custody | deterministic_address_or_threshold | fund_loss`
- Interaction scope: `cross_chain`
- Primary affected component(s): `proxy factory deployment, multisig custody, token sweep guard`
- Contracts / modules involved: `ProxyFactory, GnosisSafe, MultiSigWallet, BridgeLocker, cTUSD, TUSD_Legacy`
- Path keys: `create_nonce_collision | ProxyFactory.createProxy | ProxyFactory -> GnosisSafe`; `low_multisig_threshold | MultiSigWallet.submitTransaction | MultiSigWallet -> BridgeLocker.unlockToken`; `token_proxy_dual_address | cTUSD.sweepToken | cTUSD -> TUSD_Legacy -> TUSD_Current`
- High-signal code keywords: `createProxy, create2, submitTransaction, confirmTransaction, required, sweepToken, underlying, delegatecall, fallback`
- Typical sink / impact: `L2 deposit theft, complete bridge drain, underlying token sweep`
- Validation strength: `strong`

### Contract / Boundary Map

- Entry surface(s): `ProxyFactory.createProxy()`, `MultiSigWallet.submitTransaction()`, `cTUSD.sweepToken()`
- Contract hop(s): `ProxyFactory -> new proxy (CREATE, increments nonce) -> address match`; `MultiSigWallet.submit -> MultiSigWallet.confirm -> BridgeLocker.unlockToken`; `cTUSD.sweepToken -> TUSD_Legacy.transfer -> delegatecall -> TUSD_Current.transfer`
- Trust boundary crossed: `L1 address assumption → L2 deployment counterfactual`; `multisig threshold → bridge locker`; `token identity check → proxy delegation`
- Shared state or sync assumption: `L1 safe address exists at the same address on L2 upon deployment`; `2 of 5 keys cannot be simultaneously compromised`; `underlying token has exactly one address`

### Valid Bug Signals

- Signal 1: Funds sent to an L2 address where no contract has been deployed yet, and the address is CREATE-deterministic (not CREATE2)
- Signal 2: Bridge multisig threshold is < 60% of total signers and no time delay exists on large transfers
- Signal 3: Token sweep guard compares `token != underlying` using only the current proxy address, but the token has a legacy proxy address that delegates to the same implementation

### False Positive Guards

- Not this bug when: Cross-chain deployments use CREATE2 with chain-specific salt (address is deterministic from salt, not nonce)
- Safe if: Multisig threshold >= 60% of signers AND has mandatory time delay for large operations
- Safe if: Sweep guard checks against ALL known token addresses (current + legacy + aliases) or verifies underlying balance is unchanged post-sweep
- Requires attacker control of: ProxyFactory.createProxy() on L2 (public, Path A), two private keys (Path B), or cTUSD.sweepToken (admin-gated, but was callable — Path C)

---

## Vulnerability Description

### Root Cause

Three vulnerabilities exploiting identity assumptions in cross-chain and cross-contract contexts:

1. **CREATE nonce determinism across chains (Optimism/Wintermute)**: Addresses created via `CREATE` are deterministic: `keccak256(rlp([deployer, nonce]))`. If a Gnosis Safe exists at address X on L1 via a ProxyFactory, the same address can be claimed on L2 by calling `createProxy()` until the factory nonce produces the same address. The attacker then controls the proxy at that L2 address and drains any tokens sent to it.

2. **Insufficient multisig threshold (Harmony)**: The Harmony bridge used a 2-of-5 multisig wallet. Compromising just 2 keys (40%) gave full control to submit and confirm arbitrary token unlock transactions, draining $100M across USDT, ETH, WBTC, USDC, and DAI.

3. **Token proxy dual-address identity confusion (Compound TUSD)**: TUSD uses a proxy pattern where a legacy address (`0x8dd5...`) delegates all calls to the current implementation (`0x0000...`). Compound's `sweepToken` function guards against sweeping the underlying by checking `token != underlying`, but only uses the current address. The legacy address passes this check while any `transfer()` call on it delegates to the real TUSD — effectively sweeping the underlying.

### Attack Scenario / Path Variants

**Path A: Cross-Chain Address Collision via CREATE Nonce Replay (Optimism/Wintermute — $15M)** [CRITICAL]
Path key: `create_nonce_collision | ProxyFactory.createProxy | ProxyFactory -> GnosisSafe (L2 address claim)`
Entry surface: `ProxyFactory.createProxy(address masterCopy, bytes data)` — callable by anyone
Contracts touched: `ProxyFactory -> new GnosisSafeProxy (CREATE)`
Boundary crossed: `L1 address assumption → L2 CREATE nonce race`
pathShape: `iterative-loop`

1. Wintermute receives 20M OP tokens on Optimism to their L1 Gnosis Safe address
2. The Gnosis Safe has NOT been deployed on Optimism yet — funds sit at an uncontrolled address
3. Attacker calls `ProxyFactory.createProxy(masterCopy, "0x")` in a loop on Optimism
4. Each call increments the factory's nonce → deterministic CREATE address shifts
5. When `keccak256(rlp([proxyFactory, current_nonce]))[12:]` matches the target, attacker controls the new proxy
6. Attacker now controls a contract at the target address → calls to drain 20M OP tokens ($15M)

**Path B: Compromised Multisig Keys with Low Threshold (Harmony — $100M)** [CRITICAL]
Path key: `low_multisig_threshold | MultiSigWallet.submitTransaction | MultiSigWallet -> BridgeLocker.unlockToken`
Entry surface: `MultiSigWallet.submitTransaction(address dest, uint value, bytes data)` — callable by owner
Contracts touched: `MultiSigWallet -> BridgeLocker.unlockToken`
Boundary crossed: `multisig threshold → bridge locker custody`
pathShape: `linear-multistep`

1. Harmony bridge uses a 2-of-5 multisig to authorize token unlocks
2. Attacker compromises 2 of 5 private keys (0xf845A7 and 0x812d86)
3. First key calls `submitTransaction(BridgeLocker, 0, unlockToken(USDT, 9.98M, attacker))` — creates pending tx
4. Second key calls `confirmTransaction(txId)` — meets 2-of-5 threshold → auto-executes
5. 9.98M USDT unlocked to attacker
6. Repeat for ETH, WBTC, USDC, DAI → ~$100M total

**Path C: Token Proxy Dual-Address Bypass on Sweep Function (Compound TUSD — Full Market)** [CRITICAL]
Path key: `token_proxy_dual_address | cTUSD.sweepToken | cTUSD -> TUSD_Legacy.delegatecall -> TUSD_Current`
Entry surface: `cTUSD.sweepToken(EIP20NonStandardInterface token)` — admin-callable
Contracts touched: `cTUSD -> TUSD_Legacy (fallback) -> delegatecall -> TUSD_Current.transfer`
Boundary crossed: `token identity check (single address) → proxy delegation (multiple addresses for same token)`
pathShape: `atomic`

1. cTUSD market has `sweepToken()` to recover accidentally-sent tokens
2. Guard: `require(address(token) != underlying)` prevents sweeping TUSD directly
3. TUSD has a legacy address (`0x8dd5...`) that delegates all calls to current TUSD (`0x0000...`)
4. Call `sweepToken(tusdLegacy)` — guard passes: `tusdLegacy != underlying` (different addresses!)
5. But `tusdLegacy.transfer()` → `fallback() { currentTUSDProxy.delegatecall(msg.data) }` → real TUSD transfer
6. Result: ALL TUSD balance drained from the cTUSD market

### Vulnerable Pattern Examples

**Example 1: Optimism — CREATE Nonce Address Collision ($15M)** [Approx Vulnerability: CRITICAL] `@audit` [OPT-POC]

```solidity
// ❌ VULNERABLE: CREATE address is deterministic — attacker replays until match
// address = keccak256(rlp([proxyFactory, nonce]))[12:]

contract OptimismExploit {
    address public childcontract;
    ProxyFactory proxy = ProxyFactory(0x76E2cFc1F5Fa8F6a5b3fC4c8F4788F0116861F9B);

    function testExploit() public {
        // @audit Brute-force proxy creation until address matches Wintermute's L1 safe
        while (childcontract != 0x4f3a120E72C76c22ae802D129F599BFDbc31cb81) {
            childcontract = proxy.createProxy(
                0xE7145dd6287AE53326347f3A6694fCf2954bcD8A, // master copy
                "0x"  // empty initializer
            );
        }
        // @audit childcontract == target → attacker controls the proxy at that address
        // All 20M OP tokens ($15M) sent to this address are now accessible
    }
}
```

**Example 2: Harmony — 2-of-5 Multisig Key Compromise ($100M)** [Approx Vulnerability: CRITICAL] `@audit` [HAR-POC]

```solidity
// ❌ VULNERABLE: 2-of-5 threshold — compromising 40% of keys drains entire bridge

function testExploit() public {
    // Encode bridge unlock: unlockToken(USDT, 9.98M, attacker)
    bytes memory msgP1 = hex"fe7f61ea000000000000000000000000"
                         hex"dac17f958d2ee523a2206206994597c13d831ec7"  // USDT
                         hex"00000000000000000000000000000000000000000000000000000913e1f5a200"
                         hex"000000000000000000000000";
    bytes memory recipient = abi.encodePacked(address(this));
    bytes memory receiptId = hex"d48d952695ede26c0ac11a6028ab1be6059e9d104b55208931a84e99ef5479b6";
    bytes memory _message = bytes.concat(msgP1, recipient, receiptId);

    // @audit First compromised key submits the unlock transaction
    cheat.prank(0xf845A7ee8477AD1FB4446651E548901a2635A915);
    uint256 txId = MultiSigWallet.submitTransaction(
        0x2dCCDB493827E15a5dC8f8b72147E6c4A5620857,  // bridge locker
        0, _message
    );

    // @audit Second compromised key confirms → meets 2/5 threshold → auto-executes
    cheat.prank(0x812d8622C6F3c45959439e7ede3C580dA06f8f25);
    MultiSigWallet.confirmTransaction(txId);
    // 9.98M USDT drained. Repeat for ETH, WBTC, USDC, DAI → ~$100M total
}
```

**Example 3: Compound TUSD — Legacy Proxy Address Bypasses Sweep Guard (Full Market)** [Approx Vulnerability: CRITICAL] `@audit` [CTUSD-POC]

```solidity
// ❌ VULNERABLE: sweepToken guard checks current address only — legacy proxy bypasses it

function testExploit() public {
    address underlying = 0x0000000000085d4780B73119b644AE5ecd22b376;  // Current TUSD
    address tusdLegacy = 0x8dd5fbCe2F6a956C3022bA3663759011Dd51e73E;  // Legacy TUSD

    // @audit Guard: require(address(token) != underlying)
    // tusdLegacy != underlying → PASSES (different addresses!)
    // But tusdLegacy.transfer() → fallback → delegatecall to real TUSD → real transfer
    cTUSD.sweepToken(EIP20NonStandardInterface(tusdLegacy));
    // Result: ALL TUSD drained from cTUSD market
}

// Why this works — Legacy TUSD contract:
// fallback() {
//     (bool success,) = currentTUSDProxy.delegatecall(msg.data);
// }
// Calling tusdLegacy.transfer() delegates to real TUSD → moves real TUSD tokens
```

---

## Impact Analysis

### Technical Impact
- L2 address claims allow draining any tokens sent to undeployed L2 addresses with deterministic L1 counterparts
- Low bridge multisig thresholds turn key compromise into complete bridge drain across all locked tokens
- Token proxy aliases bypass sweep and identity guards, enabling extraction of protocol-held tokens

### Business Impact

| Protocol | Date | Loss | Root Cause |
|----------|------|------|------------|
| Harmony Bridge | Jun 2022 | ~$100M | 2-of-5 multisig key compromise |
| Optimism/Wintermute | Jun 2022 | ~$15M | CREATE nonce address collision on L2 |
| Compound TUSD | Mar 2022 | Full cTUSD market | Legacy proxy address bypasses sweep guard |

**Total: $115M+** from cross-chain identity and custody assumption failures.

### Affected Scenarios
- Any protocol sending tokens to an L2 address where the contract uses CREATE (not CREATE2) for deployment
- Bridge multisig wallets with threshold < 60% of total signers
- Token recovery/sweep functions that compare only one address for the underlying
- Any token using a legacy proxy that delegates to a current implementation
- Protocols integrating tokens without checking for multiple entry points (proxy aliases)

---

## Secure Implementation

**Fix 1: Use CREATE2 with Chain-Specific Salt for Cross-Chain Deployments**
```solidity
// ✅ SECURE: CREATE2 address is deterministic from (factory, salt, initCodeHash)
// Salt includes chain ID → same address can ONLY be created by the same factory with same params
contract SecureProxyFactory {
    function createProxyWithNonce(
        address masterCopy, bytes memory initializer, uint256 saltNonce
    ) public returns (address proxy) {
        bytes32 salt = keccak256(abi.encodePacked(
            keccak256(initializer),
            saltNonce,
            block.chainid  // @audit Chain-specific — prevents cross-chain collision
        ));
        bytes memory deploymentData = abi.encodePacked(proxyCreationCode, uint256(uint160(masterCopy)));
        assembly {
            proxy := create2(0, add(deploymentData, 0x20), mload(deploymentData), salt)
        }
        require(proxy != address(0), "Create2 failed");
    }
}
```

**Fix 2: Higher Multisig Threshold + Time Delays for Bridges**
```solidity
// ✅ SECURE: Higher threshold + time locks for bridge operations
contract SecureBridge {
    uint256 public constant THRESHOLD = 4;  // 4-of-7 minimum
    uint256 public constant UNLOCK_DELAY = 24 hours;
    uint256 public constant MAX_SINGLE_UNLOCK = 1_000_000e18;

    function submitUnlock(address token, uint256 amount, address recipient) external onlySigner {
        require(amount <= MAX_SINGLE_UNLOCK, "Exceeds single unlock limit");
        pendingUnlocks[nextId] = PendingUnlock({
            token: token, amount: amount, recipient: recipient,
            executeAfter: block.timestamp + UNLOCK_DELAY,
            confirmations: 1, executed: false
        });
    }

    function confirmUnlock(uint256 id) external onlySigner {
        PendingUnlock storage unlock = pendingUnlocks[id];
        require(!hasConfirmed[id][msg.sender], "Already confirmed");
        hasConfirmed[id][msg.sender] = true;
        unlock.confirmations++;
        // @audit Requires 4+ confirmations AND time delay
        if (unlock.confirmations >= THRESHOLD && block.timestamp >= unlock.executeAfter) {
            _executeUnlock(unlock);
        }
    }
}
```

**Fix 3: Comprehensive Token Identity Check for Sweep**
```solidity
// ✅ SECURE: Check ALL known addresses for a token, not just current proxy
contract SecureCToken {
    mapping(address => bool) public knownUnderlyingAddresses;

    function initializeUnderlyingAddresses(address[] calldata addresses) external onlyAdmin {
        for (uint i = 0; i < addresses.length; i++) {
            knownUnderlyingAddresses[addresses[i]] = true;
        }
    }

    function sweepToken(IERC20 token) external onlyAdmin {
        require(!knownUnderlyingAddresses[address(token)], "Cannot sweep underlying");
        // @audit Additional check: verify underlying balance unchanged after sweep
        uint256 balBefore = IERC20(underlying).balanceOf(address(this));
        token.transfer(msg.sender, token.balanceOf(address(this)));
        uint256 balAfter = IERC20(underlying).balanceOf(address(this));
        require(balBefore == balAfter, "Swept token IS the underlying via proxy");
    }
}
```

---

## Detection Patterns

### Contract / Call Graph Signals
```
- ProxyFactory using CREATE (sequential nonce) for cross-chain proxy deployment
- Bridge multisig with required < 60% of owners and no time delay on execution
- Token sweep/rescue functions that compare a single address for the underlying
- Tokens with fallback/receive that delegatecall to another contract
```

### High-Signal Grep Seeds
```
- createProxy
- create2
- CREATE
- submitTransaction
- confirmTransaction
- required
- sweepToken
- recoverToken
- rescueToken
- underlying
- delegatecall
- fallback
```

### Code Patterns to Look For
```
- ProxyFactory.createProxy with sequential nonce (not CREATE2 with salt)
- MultiSig.required() returning < 60% of owners list
- require(token != underlying) without checking proxies/aliases
- Token contract with fallback() { delegatecall(currentProxy) }
- Cross-chain fund transfers to addresses without deployed contracts
```

### Audit Checklist
- [ ] Do cross-chain deployments use CREATE2 with chain-specific salt? Or CREATE with replayable nonces?
- [ ] Is the multisig threshold at least 60% of total signers?
- [ ] Are bridge unlock operations subject to mandatory time delays?
- [ ] Does the sweep guard check ALL known addresses for the underlying (current + legacy + aliases)?
- [ ] Does the protocol check if tokens have proxy aliases that delegate to the same implementation?
- [ ] Is there a rate limit on bridge unlock volume?
- [ ] Are bridge signer keys regularly rotated and stored in diverse custody?

---

## Real-World Examples

### Known Exploits
- **Optimism/Wintermute** — CREATE nonce replay claims L2 address before legitimate owner — Jun 2022 — $15M
  - Link: https://rekt.news/wintermute-rekt/
  - Root cause: L1 Gnosis Safe address was CREATE-deterministic; attacker replayed createProxy on L2
- **Harmony Horizon Bridge** — 2-of-5 multisig key compromise → bridge drain — Jun 2022 — $100M
  - Link: https://rekt.news/harmony-rekt/
  - Root cause: Bridge custodied $100M+ with a 2-of-5 threshold — 40% key compromise ≈ full takeover
- **Compound TUSD** — Legacy TUSD proxy bypasses sweepToken guard — Mar 2022 — Full cTUSD market
  - Link: https://medium.com/chainsecurity/trueusd-compound-vulnerability-bc5b696d29e2
  - Root cause: sweepToken checked `token != underlying` — legacy TUSD address passed but delegates to real TUSD

### Related Entries
- [Bridge Access Control Bypass (2021)](defihacklabs-bridge-patterns.md) — Poly Network, Chainswap
- [Bridge Verification Bypass (2022)](defihacklabs-bridge-2022-patterns.md) — Nomad, Qubit, Meter
- [Proxy Vulnerabilities](../../general/proxy/proxy-vulnerabilities.md)
- [Signature Vulnerabilities](../../general/signature/signature-vulnerabilities.md)

---

## Prevention Guidelines

### Development Best Practices
1. Use CREATE2 with chain-specific salt for all cross-chain contract deployments
2. Require multisig threshold >= 60% of total signers for high-value bridges
3. Implement mandatory time delays and rate limiting for bridge unlock operations
4. Check ALL known addresses for tokens (current proxy + legacy + aliases) in identity guards
5. Before any token is integrated, verify whether it has multiple entry points via proxy delegation

### Testing Requirements
- Unit tests for: CREATE2 salt includes chainId, time delay enforcement on unlocks
- Integration tests for: sweep guard with legacy proxy addresses, multisig threshold enforcement
- Invariant tests for: bridge unlock volume bounded per time period, CREATE2 address consistency
