---
protocol: bridge
chain: ethereum, bsc, polygon, multi-chain
category: bridge_exploit
vulnerability_type: cross_chain_bridge_bypass

attack_type: bridge_logic_flaw
affected_component: cross_chain_messenger, signature_verification

primitives:
  - cross_chain_target_bypass
  - self_referential_signature
  - relay_verification_bypass
  - keeper_privilege_escalation

severity: critical
impact: fund_loss, total_control
exploitability: 0.7
financial_impact: critical

tags:
  - bridge
  - cross_chain
  - signature
  - relay
  - access_control
  - keeper
  - Poly_Network
  - Chainswap
  - real_exploit
  - DeFiHackLabs

source: DeFiHackLabs
total_exploits_analyzed: 3
total_losses: "$617M+"
---

## DeFiHackLabs Bridge Exploit Patterns Compendium

### Overview

Cross-chain bridge exploits represent the highest single-incident losses in DeFi history. This entry catalogs **3 real-world bridge exploits** from 2021 totaling **$617M+ in losses**. The core patterns: (1) insufficient restrictions on cross-chain message targets allow executing arbitrary functions on privileged contracts, and (2) self-referential signature schemes where the signer validates against a list they can modify.

### Root Cause Categories

1. **Cross-Chain Target Restriction Bypass** — Bridge executor can call ANY contract, including privileged ownership/management contracts
2. **Self-Referential Signature Verification** — Signature is verified against a keeper list that the signer themselves can modify

---

### Vulnerable Pattern Examples

#### Category 1: Cross-Chain Target Restriction Bypass [CRITICAL]

**Example 1: Poly Network — Cross-Chain Owner Replacement ($611M, 2021-08)** [CRITICAL]
```solidity
// ❌ VULNERABLE: EthCrossChainManager can execute on ANY target contract
// Including EthCrossChainData which stores the keeper (validator) list

// The bridge cross-chain executor:
contract EthCrossChainManager {
    function verifyHeaderAndExecuteTx(
        bytes memory proof,
        bytes memory rawHeader,
        bytes memory headerProof,
        bytes memory curRawHeader,
        bytes memory headerSig
    ) external returns (bool) {
        // Verify Poly chain header signature...
        // Extract cross-chain message: (toContract, method, args)

        // @audit CRITICAL: No restriction on what `toContract` can be called!
        require(
            _executeCrossChainTx(
                toContract,     // @audit Can be EthCrossChainData!
                toMethod,       // @audit Can be putCurEpochConPubKeyBytes!
                args,           // @audit Can be attacker's public key!
                fromContract,
                fromChainId
            ),
            "Execute tx failed"
        );
    }

    function _executeCrossChainTx(
        address _toContract,
        bytes memory _method,
        bytes memory _args,
        bytes memory _fromContract,
        uint64 _fromChainId
    ) internal returns (bool) {
        // @audit Calls _toContract._method(_args) with NO target whitelist
        (bool success, bytes memory result) = _toContract.call(
            abi.encodePacked(
                bytes4(keccak256(abi.encodePacked(_method, "(bytes,bytes,uint64)"))),
                abi.encode(_args, _fromContract, _fromChainId)
            )
        );
        return success;
    }
}

// The privileged contract that stores keepers:
contract EthCrossChainData {
    // @audit This function changes the keepers (validators) for the bridge
    function putCurEpochConPubKeyBytes(bytes memory curEpochPkBytes) public onlyOwner {
        ConKeepersPkBytes = curEpochPkBytes;
    }
    // @audit Owner of EthCrossChainData IS EthCrossChainManager
    // So cross-chain messages processed by Manager CAN call this!
}

// Attack sequence:
// 1. Craft a cross-chain message on Poly chain:
//    toContract = EthCrossChainData
//    toMethod   = "putCurEpochConPubKeyBytes"
//    args       = [attacker's public key]
//
// 2. EthCrossChainManager processes it — replaces ALL keeper keys with attacker's
//
// 3. Attacker now controls cross-chain message validation
//    Signs arbitrary withdrawal messages → drains $611M across ETH, BSC, Polygon
```
- **PoC**: `DeFiHackLabs/src/test/2021-08/PolyNetwork_exp.sol`
- **Root Cause**: `EthCrossChainManager` was the owner of `EthCrossChainData` (keeper registry). Cross-chain messages could target ANY contract with NO whitelist. Attacker sent a message targeting `EthCrossChainData.putCurEpochConPubKeyBytes()` to replace all validator keys with their own, then signed arbitrary drain messages across 3 chains.

---

#### Category 2: Self-Referential Signature Verification [CRITICAL]

**Example 2: Chainswap v2 — Keeper Signs Own Addition ($4.4M, 2021-07)** [CRITICAL]
```solidity
// ❌ VULNERABLE: Bridge requires signature from ANY registered keeper
// BUT: The receive() function can ADD NEW KEEPERS
// So an attacker who IS a keeper can add more attacker-controlled keepers

contract ChainswapBridgeV2 {
    mapping(address => bool) public keepers;

    // @audit Signature verified against keeper mapping
    function receive(
        uint256[] memory amounts,
        address[] memory tokens,
        address to,
        uint256 nonce,
        uint256 fromChainId,
        bytes memory signature
    ) external {
        bytes32 hash = keccak256(abi.encodePacked(amounts, tokens, to, nonce, fromChainId));
        address signer = hash.toEthSignedMessageHash().recover(signature);
        require(keepers[signer], "not a keeper");  // @audit Only checks IS a keeper

        for (uint256 i = 0; i < tokens.length; i++) {
            IMappableToken(tokens[i]).mint(to, amounts[i]);
            // @audit Mints arbitrary amounts of bridged tokens
        }
    }

    // @audit CRITICAL: Keeper management has insufficient access control
    function addKeeper(address keeper) external onlyKeeper {
        keepers[keeper] = true;
        // @audit A compromised/malicious keeper can add more malicious keepers
    }
}

// Attack:
// 1. Compromise ONE keeper key (or exploit keeper addition flow)
// 2. Add multiple attacker-controlled keeper addresses
// 3. Sign arbitrary mint messages for any bridged token
// 4. Drain $4.4M across multiple token types
```
- **PoC**: `DeFiHackLabs/src/test/2021-07/Chainswap_exp2.sol`

**Example 3: Chainswap v1 — Signature Without Proper Nonce ($0.8M, 2021-07)** [HIGH]
```solidity
// ❌ VULNERABLE: Signature verification doesn't include chain-specific nonce
// Same signature can be replayed or forged with predictable parameters

contract ChainswapBridgeV1 {
    function receive(
        address token,
        address to,
        uint256 amount,
        uint256 nonce,
        bytes memory signature
    ) external {
        bytes32 hash = keccak256(abi.encodePacked(token, to, amount, nonce));
        address signer = hash.recover(signature);
        require(isKeeper[signer], "invalid keeper");

        // @audit Missing: chainId in hash → cross-chain replay
        // @audit Missing: contract address in hash → cross-contract replay
        // @audit Missing: proper nonce management → reuse possible

        IERC20(token).transfer(to, amount);
    }
}

// Attack vectors:
// 1. Replay a valid signature on a different chain
// 2. Reuse signatures with predictable nonce increments
// 3. If keeper key leaked: generate unlimited valid signatures
```
- **PoC**: `DeFiHackLabs/src/test/2021-07/Chainswap_exp1.sol`
- **Root Cause**: Missing `chainId` and `address(this)` in signed hash. Nonce management was weak, allowing signature reuse across chains and contracts.

---

### Impact Analysis

#### Technical Impact
- **Complete bridge takeover**: Replacing keeper keys gives total control over cross-chain validation
- **Multi-chain drain**: Bridge compromises cascade across ALL connected chains simultaneously
- **Unlimited minting**: Self-referential keeper systems allow signing arbitrary mint messages

#### Business Impact
| Protocol | Loss | Bridge Flaw |
|----------|------|-------------|
| Poly Network | $611M | Cross-chain executor targets keeper management contract |
| Chainswap v2 | $4.4M | Keeper can add new keepers + sign arbitrary mints |
| Chainswap v1 | $0.8M | Missing chainId in signature hash + weak nonce |

---

### Secure Implementation

**Fix 1: Whitelist Allowed Cross-Chain Targets**
```solidity
// ✅ SECURE: Restrict which contracts can be called via cross-chain messages
contract SecureCrossChainManager {
    mapping(address => bool) public allowedTargets;

    function executeCrossChainTx(address target, bytes memory data) internal {
        // @audit Only whitelisted contracts can be targeted
        require(allowedTargets[target], "target not whitelisted");
        // @audit NEVER allow targeting the keeper/validator management contract
        require(target != address(crossChainData), "cannot target data contract");

        (bool success,) = target.call(data);
        require(success, "execution failed");
    }
}
```

**Fix 2: Multi-Sig Keeper Operations**
```solidity
// ✅ SECURE: Require M-of-N signatures for bridge operations
contract SecureBridge {
    uint256 public constant REQUIRED_SIGS = 3;
    uint256 public constant TOTAL_KEEPERS = 5;

    function receive(
        address token, address to, uint256 amount,
        uint256 nonce, uint256 fromChainId,
        bytes[] memory signatures  // @audit Multiple signatures required
    ) external {
        require(signatures.length >= REQUIRED_SIGS, "insufficient sigs");

        bytes32 hash = keccak256(abi.encodePacked(
            token, to, amount, nonce, fromChainId,
            block.chainid,          // @audit Include target chainId
            address(this)           // @audit Include contract address
        ));

        address[] memory signers = new address[](signatures.length);
        for (uint i = 0; i < signatures.length; i++) {
            signers[i] = hash.toEthSignedMessageHash().recover(signatures[i]);
            require(keepers[signers[i]], "not a keeper");
            // @audit Check no duplicate signers
            for (uint j = 0; j < i; j++) {
                require(signers[j] != signers[i], "duplicate signer");
            }
        }

        IERC20(token).transfer(to, amount);
    }

    // @audit Keeper management requires governance/timelock, NOT keeper self-addition
    function addKeeper(address keeper) external onlyGovernance {
        keepers[keeper] = true;
    }
}
```

**Fix 3: EIP-712 Typed Signatures for Bridges**
```solidity
// ✅ SECURE: EIP-712 prevents cross-chain and cross-contract replay
bytes32 public immutable DOMAIN_SEPARATOR;

constructor() {
    DOMAIN_SEPARATOR = keccak256(abi.encode(
        keccak256("EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)"),
        keccak256("SecureBridge"),
        keccak256("1"),
        block.chainid,              // @audit Chain-specific
        address(this)               // @audit Contract-specific
    ));
}
```

---

### Detection Patterns

```bash
# Cross-chain executor with unrestricted targets
grep -rn "\.call\|\.delegatecall" --include="*.sol" | \
  grep -i "crosschain\|bridge\|relay\|executor" | \
  xargs grep -L "whitelist\|allowedTarget\|require.*target"

# Keeper self-modification patterns
grep -rn "function addKeeper\|function setKeeper\|function addSigner" --include="*.sol" | \
  xargs grep -i "onlyKeeper\|onlySigner"
# @audit If keepers can add keepers, it's self-referential

# Missing chainId in signature hash
grep -rn "keccak256.*abi.encodePacked" --include="*.sol" | \
  grep -i "signature\|keeper\|bridge\|nonce" | \
  xargs grep -L "chainid\|chainId\|block.chainid"

# Privileged contracts owned by bridge executors
grep -rn "onlyOwner\|owner()" --include="*.sol" | \
  grep -i "keeper\|validator\|pubkey\|epoch"
```

---

### Audit Checklist

1. **Can the cross-chain executor call ANY contract?** — Must have a target whitelist
2. **Is the keeper/validator management contract callable via cross-chain messages?** — NEVER allow this
3. **Can keepers add other keepers?** — Self-referential = single point of failure
4. **Does the signature hash include chainId AND contract address?** — Both required for replay protection
5. **How many signatures are required?** — Single-sig bridges are extremely high risk
6. **What happens if one keeper key is compromised?** — Should not enable full bridge takeover

---

### Keywords

- bridge_exploit
- cross_chain
- keeper_bypass
- signature_replay
- self_referential_signer
- target_whitelist
- validator_replacement
- relay_verification
- multi_sig_bridge
- chainId_replay
- EIP712
- DeFiHackLabs

---

### Related Vulnerabilities

- [LayerZero Bridge Vulnerabilities](../../bridge/layerzero/LAYERZERO_VULNERABILITIES.md)
- [Wormhole Bridge Vulnerabilities](../../bridge/wormhole/WORMHOLE_VULNERABILITIES.md)
- [Hyperlane Bridge Vulnerabilities](../../bridge/hyperlane/HYPERLANE_VULNERABILITIES.md)
- [Signature Vulnerabilities](../../general/signature/signature-vulnerabilities.md)
