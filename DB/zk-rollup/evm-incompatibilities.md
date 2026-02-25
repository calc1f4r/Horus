---
# Core Classification
protocol: generic
chain: zksync|scroll|linea|taiko
category: zk_rollup_evm_compat
vulnerability_type: create2_incompatibility|opcode_divergence|precompile_difference|nonce_handling|address_derivation|msg_sender_preservation|bytecode_compression

# Attack Vector Details
attack_type: deployment_failure|address_collision|authentication_bypass|state_corruption
affected_component: create_opcode|create2_opcode|ecrecover_precompile|extcodehash|nonce_tracker|bytecode_compressor|msg_sender

# Technical Primitives
primitives:
  - CREATE
  - CREATE2
  - CREATE3
  - EXTCODEHASH
  - ecrecover
  - delegatecall
  - nonce
  - deployment_nonce
  - EIP161
  - keccak256_of_initcode
  - address_derivation
  - msg_sender
  - bytecode_compression
  - precompile_addresses
  - max_precompile_address

# Impact Classification
severity: medium
impact: deployment_failure|authentication_bypass|silent_wrong_behavior|state_corruption
exploitability: 0.60
financial_impact: medium

# Context Tags
tags:
  - zk_rollup
  - zksync_era
  - scroll
  - evm_incompatibility
  - CREATE2
  - opcode_difference
  - precompile
  - nonce
  - ecrecover
  - delegatecall
  - bytecode
  - address_derivation

language: solidity
version: all
---

## References & Source Reports

### CREATE / CREATE2 / CREATE3 Incompatibilities

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Factory Deployments Fail on ZKSync (CREATE2 hash differs) | `reports/zk_rollup_findings/factory-deployments-wont-work-correctly-on-the-zksync-chain.md` | MEDIUM | Multiple |
| CREATE Opcode Works Differently on ZKSync | `reports/zk_rollup_findings/m-2-create-opcode-works-differently-in-the-zksync-chain.md` | MEDIUM | Multiple |
| computePoolAddress Won't Work on ZKSync Era | `reports/zk_rollup_findings/m-6-computepooladdress-will-not-work-on-zksync-era.md` | MEDIUM | Sherlock |
| CREATE3 Not Available on ZKSync Era | `reports/zk_rollup_findings/m-15-create3-is-not-available-in-the-zksync-era.md` | MEDIUM | Sherlock |
| Factory create Suspicious of Reorg Attack | `reports/zk_rollup_findings/m-08-factorycreate-is-vulnerable-to-reorg-attacks.md` | MEDIUM | Multiple |
| Multiple create Methods Reorg-Suspicious | `reports/zk_rollup_findings/m-09-create-methods-are-suspicious-of-reorg-attack.md` | MEDIUM | Multiple |

### Opcode and Precompile Divergences

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| ecrecover Discrepancy with delegatecall on ZKSync | `reports/zk_rollup_findings/m-17-discrepancy-in-ecrecover-precompile-when-using-delegatecall.md` | MEDIUM | Spearbit |
| EXTCODEHASH Opcode Divergence on ZKSync | `reports/zk_rollup_findings/m-19-divergences-in-the-simulation-of-the-extcodehash-evm-opcode.md` | MEDIUM | Spearbit |
| Unauthorized Contracts Bypass Precompile Authorization via delegatecall | `reports/zk_rollup_findings/h-01-unauthorized-contracts-can-bypass-precompile-authorization-via-delegatecall.md` | HIGH | Spearbit |
| Incorrect Max Precompile Address | `reports/zk_rollup_findings/m-04-incorrect-max-precompile-address.md` | MEDIUM | Spearbit |
| SessionKeyValidator Not Working on ZKSync Mainnet | `reports/zk_rollup_findings/m-01-sessionkeyvalidator-is-not-working-on-zksync-mainnet.md` | MEDIUM | Multiple |
| Incorrect SAR Implementation | `reports/zk_rollup_findings/incorrect-sarimplementation.md` | HIGH | Multiple |
| Incorrect Byte Implementation | `reports/zk_rollup_findings/incorrect-byte-implementation.md` | HIGH | Multiple |

### Nonce and Account Behavior

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Nonce Behavior Discrepancy: ZKSync vs EIP-161 | `reports/zk_rollup_findings/m-20-nonce-behavior-discrepancy-between-zksync-era-and-eip-161.md` | MEDIUM | Spearbit |
| Deployment Nonce Doesn't Increment for Reverted Child | `reports/zk_rollup_findings/m-21-deployment-nonce-does-not-increment-for-a-reverted-child-contract.md` | MEDIUM | Spearbit |
| Discrepancy in Default Account Behavior | `reports/zk_rollup_findings/m-18-discrepancy-in-default-account-behavior.md` | MEDIUM | Spearbit |
| Nonce Ordering of EOA Can Be Updated via L1 Tx | `reports/zk_rollup_findings/m-06-nonce-ordering-of-eoa-can-be-updated-to-arbitrary-through-an-l1-tx.md` | MEDIUM | Spearbit |

### msg.sender and Context Differences

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Preservation of msg.sender in ZKSync Breaks Trust Assumptions | `reports/zk_rollup_findings/preservation-of-msgsender-in-zksync-could-break-certain-trust-assumption.md` | MEDIUM | Multiple |
| Time-Sensitive Contracts on ZKSync (block.timestamp issues) | `reports/zk_rollup_findings/m-04-time-sensitive-contracts-deployed-on-zksync.md` | MEDIUM | Multiple |
| Use of L1 blockNumber on Arbitrum Incorrect | `reports/zk_rollup_findings/incorrect-use-of-l1-blocknumber-on-arbitrum.md` | MEDIUM | Multiple |
| BLS BN254 Not Available in Certain Chains (hardcoded gas limit) | `reports/zk_rollup_findings/m-6-blsbn254-is-not-available-in-certain-chains-due-to-hardcoded-gas-limit.md` | MEDIUM | Multiple |
| Multisig Incompatible with ERC-4337 on ZKSync | `reports/zk_rollup_findings/scope-1-multisig-is-incompatible-with-erc-4337.md` | MEDIUM | Multiple |

### Bytecode Compression

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Potential Gas Manipulation via Bytecode Compression | `reports/zk_rollup_findings/m-22-potential-gas-manipulation-via-bytecode-compression.md` | MEDIUM | Spearbit |
| Lack of Data Availability of Bytecode | `reports/zk_rollup_findings/lack-of-data-availability-of-bytecode.md` | HIGH | OpenZeppelin |
| CompressRightAfterConvert Bypasses Completeness Checks | `reports/zk_rollup_findings/h-5-compress-right-after-convert-can-bypass-completeness-checks.md` | HIGH | Multiple |

---

## Vulnerability Title

**EVM Incompatibilities on ZK Rollups — CREATE2, Opcodes, Nonce Handling, msg.sender Preservation**

### Overview

ZK rollups (primarily ZKSync Era, Scroll, Taiko) aim for EVM equivalence/compatibility but differ from standard Ethereum in subtle ways. These differences silently break protocols: `CREATE2` derives addresses from different parameters, `ecrecover` behaves differently in `delegatecall` contexts, `EXTCODEHASH` returns 0 for certain accounts, nonces don't increment on reverted child deployments, and `msg.sender` is preserved in system contract calls when it shouldn't be. Protocols ported from Ethereum often fail silently rather than reverting.

---

### Vulnerability Description

#### Root Cause

1. **CREATE2 address derivation**: On ZKSync, `CREATE2` uses `keccak256(bytecode)` while Ethereum uses `keccak256(initcode)`. Protocols computing expected deployment addresses off-chain (via pool address computation, `CREATE3`, etc.) get wrong addresses.
2. **Precompile behavior**: The `ecrecover` precompile behaves differently in `delegatecall` — on Ethereum it accesses the correct context, but on ZKSync the delegatecall context is not preserved, returning wrong results.
3. **Nonce discrepancies**: ZKSync does not follow EIP-161 (nonces don't start at 1 for contracts), and deployment nonces don't always increment on reverted deployments, allowing address re-use.
4. **msg.sender preservation**: System contracts in ZKSync preserve `msg.sender` in certain call contexts, breaking protocols that assume `msg.sender == direct caller`.

---

### Pattern 1: CREATE2 Address Derivation Differs on ZKSync

**Frequency**: 4/431 reports | **Validation**: Strong (multiple Sherlock contests)

#### Attack Scenario

1. Protocol uses `CREATE2` with a factory contract to deploy predictable-address proxies or pool contracts
2. Frontend / off-chain tooling computes the expected deployment address using Ethereum's `CREATE2` formula: `keccak256(0xFF, factory, salt, keccak256(initcode))`
3. On ZKSync Era, `CREATE2` uses `keccak256(ZKSYNC_CREATE2_PREFIX, sender, salt, keccak256(bytecode))` where `bytecode` differs from `initcode`
4. The computed address doesn't match actual deployment address
5. Deposits sent to the pre-computed address are lost; pool lookup by expected address fails

**Example 1: computePoolAddress Fails on ZKSync** [MEDIUM]
```solidity
// ❌ VULNERABLE: Uniswap V3-style pool address computation
// Works on Ethereum/Arbitrum/Optimism but WRONG on ZKSync Era
function computePoolAddress(
    address factory,
    address tokenA,
    address tokenB,
    uint24 fee
) public pure returns (address pool) {
    (address token0, address token1) = tokenA < tokenB 
        ? (tokenA, tokenB) : (tokenB, tokenA);
    
    // ❌ WRONG ON ZKSYNC: Uses Ethereum CREATE2 hash formula
    // ZKSync uses different bytecode hash (keccak256 of COMPILED bytecode, not initcode)
    pool = address(uint160(uint256(keccak256(abi.encodePacked(
        hex'ff',
        factory,
        keccak256(abi.encode(token0, token1, fee)),
        POOL_INIT_CODE_HASH  // This hash is DIFFERENT on ZKSync
    )))));
}
```

**Fix:**
```solidity
// ✅ SECURE: Use ZKSync-specific address derivation when deploying on ZKSync
// The POOL_INIT_CODE_HASH on ZKSync = keccak256(ZKSYNC_BYTECODE) not Ethereum initcode hash
// Option 1: Deploy a factory that stores pool addresses in a mapping
mapping(bytes32 => address) public pools;

// Option 2: Use ZKSync's L2ContractHelper for correct address computation
import {L2ContractHelper} from "@matterlabs/zksync-contracts/l2/system-contracts/libraries/L2ContractHelper.sol";
address pool = L2ContractHelper.computeCreate2Address(factory, salt, bytecodeHash, constructorInputHash);
```

---

### Pattern 2: ecrecover Discrepancy in delegatecall Context on ZKSync

**Frequency**: 1/431 reports | **Validation**: Strong (Spearbit ZKSync audit)

#### Root Cause

On Ethereum, when contract A `delegatecall`s contract B, and B calls the `ecrecover` precompile, the call context (including caller identity) is correctly preserved. On ZKSync Era, `ecrecover` is implemented as a system contract rather than a true precompile. When called via `delegatecall`, the context handling differs, causing `ecrecover` to return a different (incorrect) address.

**Example 2: ecrecover Wrong Result via delegatecall** [MEDIUM]
```solidity
// ❌ VULNERABLE: Library using ecrecover — correct on Ethereum, wrong on ZKSync
library SignatureVerifier {
    function recoverSigner(bytes32 hash, bytes calldata sig) internal pure returns (address) {
        (bytes32 r, bytes32 s, uint8 v) = splitSignature(sig);
        // On ZKSync: when this library is called via delegatecall,
        // ecrecover may return address(0) or wrong signer
        return ecrecover(hash, v, r, s);
    }
}

contract Wallet {
    using SignatureVerifier for bytes32;
    
    function verify(bytes32 hash, bytes calldata sig) external view returns (bool) {
        // Contract calls SignatureVerifier via delegatecall (library usage)
        // On ZKSync: signer != expected → authentication bypass possible
        return hash.recoverSigner(sig) == owner;
    }
}
```

**Fix:**
```solidity
// ✅ SECURE: On ZKSync, call ecrecover directly (not via delegatecall) 
// OR use ZKSync's system contract interface which handles context correctly
function verify(bytes32 hash, bytes calldata sig) external view returns (bool) {
    (bytes32 r, bytes32 s, uint8 v) = splitSignature(sig);
    // Direct call to ecrecover (not via library delegatecall)
    address recovered = ecrecover(hash, v, r, s);
    return recovered != address(0) && recovered == owner;
}
```

---

### Pattern 3: Unauthorized Precompile Authorization Bypass via delegatecall

**Frequency**: 1/431 reports | **Validation**: Strong (ZKSync Spearbit - HIGH)

#### Root Cause

ZKSync system contracts have an authorization mechanism allowing only certain callers to invoke restricted precompile functions. The check verifies `msg.sender` (or `caller` in assembly). However, when accessed via `delegatecall`, the `caller` context is that of the *delegating* contract, not the actual initiating user. An unpermissioned contract can `delegatecall` a permitted system contract, effectively inheriting its authorization.

**Example 3: Precompile Authorization Bypass** [HIGH]
```solidity
// ❌ VULNERABLE: ZKSync precompile checks msg.sender but not tx.origin
// Attacker deploys a contract that delegatecalls an authorized system contract
// Their contract inherits the authorized contract's caller identity

contract MaliciousProxy {
    function bypassPrecompile(address systemContract, bytes calldata data) external {
        // delegatecall inherits caller context (msg.sender = the authorized contract)
        // But in ZKSync, system calls check msg.sender which is THIS contract
        // Due to the discrepancy, authorization check passes
        (bool success,) = systemContract.delegatecall(data);
    }
}
```

---

### Pattern 4: Nonce Doesn't Increment for Reverted Child Deployments

**Frequency**: 1/431 reports | **Validation**: Strong (Spearbit)

#### Root Cause

On Ethereum (post-EIP-161), a contract's deployment nonce is incremented **before** the inner `CREATE` executes, so a reverted deployment still increments the parent's nonce. On ZKSync, the nonce is only incremented when deployment succeeds. This means two failed deployments share the same nonce, potentially allowing a second deployment attempt (with different bytecode) to land at the same address as the failed first attempt.

**Example 4: Nonce Discrepancy Enables Address Re-use** [MEDIUM]
```
// ZKSync vs Ethereum deployment nonce behavior
// 
// Ethereum:
// factory.nonce = N before deploy
// Deploy child (FAILS) → factory.nonce = N+1  ← nonce still incremented
// Deploy another child → uses nonce N+1 → different address
//
// ZKSync:
// factory.nonce = N before deploy
// Deploy child (FAILS) → factory.nonce = N  ← nonce NOT incremented
// Deploy another child → uses nonce N → SAME address as failed attempt!
// 
// Attackers can pre-compute the address of a failed deployment and fund it
// before the (malicious) second deployment lands at that address
```

---

### Pattern 5: block.number Returns L1 Block Number on Arbitrum (Not L2)

**Frequency**: 3/431 reports | **Validation**: Strong (Sherlock/multiple)

#### Root Cause

On Arbitrum, `block.number` returns the **L1 block number** (approximately every 15 seconds), not the L2 block number (which advances with every L2 transaction). Protocols using `block.number` for rate limiting, borrow rate calculations, or time-based logic get wildly different behavior on Arbitrum vs. Ethereum: values are 10-100x sparser.

**Example 5: Incorrect Interest Calculation Using block.number** [MEDIUM]
```solidity
// ❌ VULNERABLE: Protocol uses block.number for interest accrual
// On Ethereum: 1 block ≈ 12 seconds → formula calibrated for this
// On Arbitrum: block.number is L1 block → 1 "block" ≈ 12-15 seconds
// On Optimism: block.number is L2 block → 1 "block" ≈ 2 seconds
// All give different interest rates for same real-world time!

contract LendingPool {
    uint256 constant INTEREST_BLOCKS_PER_YEAR = 2_628_000; // Ethereum ~12s blocks
    
    function accruedInterest(uint256 principal, uint256 depositBlock) 
        public view returns (uint256) 
    {
        // BUG: blocksDelta behaves completely differently on Arbitrum/Optimism
        uint256 blocksDelta = block.number - depositBlock;
        return principal * blocksDelta * RATE / INTEREST_BLOCKS_PER_YEAR;
    }
}
```

**Fix:**
```solidity
// ✅ SECURE: Use block.timestamp for time-based calculations on L2
// block.timestamp is consistent with Wall clock time on all EVM chains
uint256 constant SECONDS_PER_YEAR = 31_536_000;

function accruedInterest(uint256 principal, uint256 depositTimestamp)
    public view returns (uint256)
{
    uint256 secondsDelta = block.timestamp - depositTimestamp;
    return principal * secondsDelta * RATE / SECONDS_PER_YEAR;
}
```

---

### Impact Analysis

#### Technical Impact
- Pool/factory address computation returns wrong address → funds sent to wrong address lost
- ecrecover authentication bypass in delegatecall contexts → signature verification broken
- Precompile authorization bypass → unauthorized system-level operations
- Interest calculations wildly off due to block.number semantics mismatch

#### Business Impact
- Lost funds when users interact with wrong deployment addresses
- Authentication bypasses on ZKSync wallet contracts
- Incorrect fee/interest accrual across entire protocol

#### Affected Scenarios
- Any protocol deployed on ZKSync using Uniswap V3 CREATE2 pool factory patterns
- Multi-chain protocols that copy-paste Ethereum logic to ZKSync/Arbitrum
- Signature verification libraries using ecrecover via delegatecall
- Interest rate models using block.number for rate calculations

---

### Secure Implementation

```solidity
// ✅ DEPLOYMENT CHECKLIST FOR ZK ROLLUPS:
// 1. Never hard-code Ethereum CREATE2 initcode hash — compute ZK-specific hash
// 2. Test ecrecover behavior in both direct call and delegatecall contexts
// 3. Use block.timestamp instead of block.number for time-based logic
// 4. Verify precompile address range (ZKSync has different max precompile address)
// 5. Test that factories correctly account for failed deployment nonces
// 6. Don't assume CREATE3 is available — it requires EIP-3155 which ZKSync may not support

// For cross-chain compatible deployment helpers:
abstract contract ChainAwareFactory {
    function _computeCreate2Address(bytes32 salt, bytes32 bytecodeHash, bytes memory constructorArgs) 
        internal view returns (address) 
    {
        if (block.chainid == 324) { // ZKSync Era
            return L2ContractHelper.computeCreate2Address(address(this), salt, bytecodeHash, keccak256(constructorArgs));
        } else {
            return address(uint160(uint256(keccak256(abi.encodePacked(
                hex'ff', address(this), salt, bytecodeHash
            )))));
        }
    }
}
```

---

### Detection Patterns

```
1. POOL_INIT_CODE_HASH hardcoded in contract — verify this is correct for target chain
2. CREATE2 address computations using keccak256(abi.encodePacked(0xff, ...)) — check if chain-specific
3. ecrecover called inside a library function (which uses delegatecall) — diverges on ZKSync
4. block.number used for interest rate or time-locked calculations on L2
5. CREATE3 factory imports — not available on ZKSync Era
6. Contracts with AggregatorV3Interface checks missing sequencer feed
7. deployment_nonce assumptions (if counting failed deployments on ZKSync)
```

### Keywords for Search

`ZKSync CREATE2 incompatibility`, `computePoolAddress ZKSync`, `CREATE2 bytecode hash different`, `CREATE3 not available ZKSync`, `ecrecover delegatecall ZKSync`, `EXTCODEHASH ZKSync`, `nonce increment reverted deployment`, `block.number Arbitrum L1`, `block.number L2 incorrect`, `ZKSync EVM equivalence`, `precompile address ZKSync`, `system contract authorization bypass`, `bytecode compression ZKSync`, `ZKSync Era opcode difference`, `Scroll EVM compatibility`, `address derivation ZKSync`, `EIP-161 nonce discrepancy`, `msg.sender preservation system call`
