---
# Core Classification
protocol: Lambo Finance
chain: evm
category: amm
vulnerability_type: deterministic_address_dos

# Attack Vector Details
attack_type: denial_of_service
affected_component: pool_factory

# Source Information
source: reports/constantproduct/h-02-lambofactory-can-be-permanently-dos-ed-due-to-createpair-call-reversal.md
audit_firm: Code4rena
severity: high

# Impact Classification
impact: permanent_dos
exploitability: 1.0
financial_impact: high

# Context Tags
tags:
  - CREATE_opcode
  - deterministic_address
  - factory_dos
  - front_running

# Version Info
language: solidity
version: all

# Pattern Identity (Required)
root_cause_family: logic_error
pattern_key: logic_error | pool_factory | deterministic_address_dos

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - createPair
  - frontRunFactory
  - predictNextAddress
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [Lambo Finance] | reports/constantproduct/h-02-lambofactory-can-be-permanently-dos-ed-due-to-createpair-call-reversal.md | HIGH | Code4rena | - |


# Lambo Finance - Deterministic Address Factory DoS

## Unique Protocol Issue

**Protocol**: Lambo Finance  
**Audit Firm**: Code4rena  
**Severity**: HIGH  
**Source**: `reports/constantproduct/h-02-lambofactory-can-be-permanently-dos-ed-due-to-createpair-call-reversal.md`

## Overview

Lambo Factory uses the `CREATE` opcode to deploy pools, which generates deterministic addresses based on `sender + nonce`. An attacker who deploys a contract at the same address before the factory can PERMANENTLY brick the factory, as the nonce increment is irreversible.



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of logic_error"
- Pattern key: `logic_error | pool_factory | deterministic_address_dos`
- Interaction scope: `single_contract`
- Primary affected component(s): `pool_factory`
- High-signal code keywords: `createPair`, `frontRunFactory`, `predictNextAddress`
- Typical sink / impact: `permanent_dos`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `DefensiveFactory.function -> LamboFactory.function -> SecureFactory.function`
- Trust boundary crossed: `internal`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: State variable updated after external interaction instead of before (CEI violation)
- Signal 2: Withdrawal path produces different accounting than deposit path for same principal
- Signal 3: Reward accrual continues during paused/emergency state
- Signal 4: Edge case in state machine transition allows invalid state

#### False Positive Guards

- Not this bug when: Standard security patterns (access control, reentrancy guards, input validation) are in place
- Safe if: Protocol behavior matches documented specification
- Requires attacker control of: specific conditions per pattern

## Why This Is Unique

Unlike UniswapV2 Factory which uses `CREATE2` with salt-based deterministic addresses:
1. **CREATE Opcode**: Address depends on deployer nonce (incrementing counter)
2. **Irreversible Nonce**: Once a nonce is used, it cannot be reused
3. **Permanent DoS**: Not just temporary - factory is bricked forever
4. **Front-Run Window**: Anyone monitoring mempool can attack

## Vulnerable Architecture

```solidity
// ❌ VULNERABLE: Uses CREATE opcode
contract LamboFactory {
    function createPair(address tokenA, address tokenB) external returns (address pair) {
        // CREATE generates address from: keccak256(rlp([sender, nonce]))[12:]
        // Attacker can precompute this address and deploy there first!
        pair = address(new LamboPair(tokenA, tokenB));  // Uses CREATE
        
        // If address is already occupied, this reverts
        // Factory nonce is now incremented, address is LOST forever
    }
}
```

## Attack Mechanics

### Address Prediction
```solidity
// Attacker's contract to compute factory's next deployment address
function predictNextAddress(address factory) public view returns (address) {
    // Get factory's current nonce (account nonce, not storage)
    uint256 nonce = INonceGetter(factory).nonce();
    // Or use eth_getTransactionCount RPC call
    
    // RLP encode [factory_address, nonce] and hash
    // For nonce < 128: simple encoding
    bytes memory data = abi.encodePacked(
        bytes1(0xd6),  // 0xc0 + 22 (length of following data)
        bytes1(0x94),  // 0x80 + 20 (address length)
        factory,
        uint8(nonce)   // For small nonces
    );
    
    return address(uint160(uint256(keccak256(data))));
}

// Attack execution
function frontRunFactory() external {
    address predictedPair = predictNextAddress(lamboFactory);
    
    // Deploy ANY contract at that address before factory
    // Using CREATE2 with precalculated salt
    bytes32 salt = findSaltForAddress(predictedPair);
    new Occupier{salt: salt}();  // Now occupies the address
    
    // Factory's createPair will now revert permanently for that nonce
}
```

### Permanent Denial
```solidity
// After attack, factory is broken:
// - Factory tried to deploy at address X
// - Address X is occupied
// - CREATE reverts
// - But factory's nonce is STILL incremented (gas was spent)
// - Address X is lost forever
// - Next attempt uses nonce+1, different address
// - Attacker can repeat infinitely
```

## Attack Scenario

1. **Monitor Mempool**: Watch for `createPair` transactions to LamboFactory
2. **Predict Address**: Calculate `keccak256(rlp([factory, nonce]))[12:]`
3. **Front-Run Deploy**: Deploy any contract at predicted address using CREATE2
4. **Factory Reverts**: `createPair` fails, nonce incremented
5. **Repeat**: Each attempt costs attacker ~32k gas, costs factory a nonce slot
6. **Permanent DoS**: Factory can never create pools at occupied addresses

## Impact

- **Permanent Factory DoS**: Factory is irreversibly bricked
- **Protocol Shutdown**: No new pools can be created
- **No Recovery**: Cannot reset nonce, cannot redeploy factory without migration
- **Low Attack Cost**: Only gas costs (~32k per blocked address)
- **High Protocol Cost**: Complete protocol failure

## Secure Implementation

```solidity
// ✅ SECURE: Use CREATE2 with unique salt
contract SecureFactory {
    function createPair(address tokenA, address tokenB) external returns (address pair) {
        // Sort tokens for deterministic salt
        (address token0, address token1) = tokenA < tokenB 
            ? (tokenA, tokenB) 
            : (tokenB, tokenA);
        
        // CREATE2 address = keccak256(0xff ++ factory ++ salt ++ keccak256(bytecode))
        bytes32 salt = keccak256(abi.encodePacked(token0, token1));
        
        // CREATE2 is idempotent - same salt always gives same address
        // Cannot be front-run to different address
        pair = address(new Pair{salt: salt}(token0, token1));
    }
}

// Alternative: Check if address is occupied before CREATE
contract DefensiveFactory {
    function createPair(address tokenA, address tokenB) external returns (address pair) {
        address predicted = computeAddress(tokenA, tokenB);
        
        // Check if address is already occupied
        require(predicted.code.length == 0, "Address occupied");
        require(predicted.balance == 0, "Address has balance");
        
        // Still vulnerable to front-running, but fails gracefully
        pair = address(new LamboPair(tokenA, tokenB));
    }
}
```

## Detection Patterns

```solidity
// RED FLAGS:
// 1. Factory using CREATE (no salt parameter in deployment)
pair = address(new Pair());  // VULNERABLE

// 2. No address existence check before deployment
// 3. Nonce-dependent address generation
// 4. No CREATE2 usage

// SECURE PATTERN:
pair = address(new Pair{salt: salt}());  // Uses CREATE2
```

## Related Vulnerabilities

- **M-04**: Wrong init_code_hash breaking `pairFor` address computation
- **Factory Front-Running**: General pool creation front-running attacks

## Lessons for Auditors

1. **Prefer CREATE2**: Always use CREATE2 for deterministic factory deployments
2. **Salt Design**: Use token pair addresses as salt for uniqueness
3. **Existence Checks**: Verify target address is empty before deployment
4. **Nonce Awareness**: Understand CREATE's nonce dependency
5. **Front-Run Analysis**: Model mempool visibility attacks

## Keywords

`CREATE_opcode`, `deterministic_address`, `factory_dos`, `nonce_manipulation`, `front_running`, `CREATE2`, `permanent_dos`, `lambo_factory`, `pool_creation_attack`

### Detection Patterns

#### Code Patterns to Look For
```
- See vulnerable pattern examples above for specific code smells
- Check for missing validation on critical state-changing operations
- Look for assumptions about external component behavior
```

#### Audit Checklist
- [ ] Verify all state-changing functions have appropriate access controls
- [ ] Check for CEI pattern compliance on external calls
- [ ] Validate arithmetic operations for overflow/underflow/precision loss
- [ ] Confirm oracle data freshness and sanity checks

### Keywords for Search

> These keywords enhance vector search retrieval:

`CREATE_opcode`, `amm`, `createPair`, `deterministic_address`, `deterministic_address_dos`, `factory_dos`, `frontRunFactory`, `front_running`, `predictNextAddress`
