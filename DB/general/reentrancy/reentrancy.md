---
protocol: generic
vulnerability_class: reentrancy
title: "Reentrancy Vulnerabilities"
category: access_control_state_management
vulnerability_type: reentrancy
attack_type: callback_reentrancy
affected_component: external_call_state_accounting
severity: high
impact: fund_loss
severity_range: "MEDIUM to HIGH"

source_reports:
  - file: "reports/yield_protocol_findings/h-13-balancerpairoracle-can-be-manipulated-using-read-only-reentrancy.md"
    protocol: "Blueberry Update"
    severity: "HIGH"
    auditor: "Sherlock"
  - file: "reports/yield_protocol_findings/reentrancy-in-vault-settlement.md"
    protocol: "Cega (Eth V2)"
    severity: "HIGH"
    auditor: "OtterSec"
  - file: "reports/yield_protocol_findings/attacker-can-bypass-reentrancy-lock-to-double-spend-deposit.md"
    protocol: "Uniswap: The Compact"
    severity: "MEDIUM"
    auditor: "Spearbit"

# Pattern Identity (Required)
root_cause_family: callback_reentrancy
pattern_key: callback_reentrancy | unknown | unknown

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: multi_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - deposit
  - getPrice
  - liquidate
  - msg.sender
  - settleVault
  - swap
  - totalSupply
  - withdraw
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [Blueberry Update] | reports/yield_protocol_findings/h-13-balancerpairoracle-can-be-manipulated-using-read-only-reentrancy.md | HIGH | Sherlock | - |
| [Cega (Eth V2)] | reports/yield_protocol_findings/reentrancy-in-vault-settlement.md | HIGH | OtterSec | - |
| [Uniswap: The Compact] | reports/yield_protocol_findings/attacker-can-bypass-reentrancy-lock-to-double-spend-deposit.md | MEDIUM | Spearbit | - |


# Reentrancy Vulnerabilities

## Overview

Reentrancy vulnerabilities occur when external calls allow attackers to re-enter a function or contract before the initial execution completes, enabling manipulation of state in unexpected ways. This includes classic reentrancy, read-only reentrancy (view functions return stale/manipulated data), and cross-function reentrancy.

**Root Cause Statement**: This vulnerability exists because state updates occur after external calls (violating Checks-Effects-Interactions pattern) or because view functions are called during states that should be considered locked, allowing attackers to manipulate contract state or extract value through recursive calls.

**Observed Frequency**: Common pattern (10+ reports analyzed)
**Consensus Severity**: MEDIUM to HIGH

---



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of callback_reentrancy"
- Pattern key: `callback_reentrancy | unknown | unknown`
- Interaction scope: `multi_contract`
- Primary affected component(s): `unknown`
- High-signal code keywords: `deposit`, `getPrice`, `liquidate`, `msg.sender`, `settleVault`, `swap`, `totalSupply`, `withdraw`
- Typical sink / impact: `fund_loss`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `SecureVault.function -> before.function -> state.function`
- Trust boundary crossed: `callback / external call`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: External call (`.call`, `.transfer`, token transfer) occurs before state variable update
- Signal 2: Token implements callback hooks (ERC-777, ERC-721) and protocol doesn't use `nonReentrant`
- Signal 3: User-supplied token address passed to `transferFrom` without callback protection
- Signal 4: Read-only function's return value consumed cross-contract during an active callback window

#### False Positive Guards

- Not this bug when: Contract uses `ReentrancyGuard` (`nonReentrant`) on all entry points
- Safe if: All state updates complete before any external call (strict CEI)
- Requires attacker control of: specific conditions per pattern

## Vulnerable Code Patterns

### Example 1: Read-Only Reentrancy in Oracle (HIGH - Blueberry)

**Reference**: h-13-balancerpairoracle-can-be-manipulated-using-read-only-reentrancy.md

Oracle queries pool during reentrancy window:

    function getPrice(address token) external view returns (uint256) {
        (tokens, balances, ) = IBalancerVault(vault).getPoolTokens(poolId);
        uint256 totalSupply = IBPool(pool).totalSupply();
        // During joinPool callback, balances updated but supply not yet
        return f(balances) / totalSupply;
    }

**Attack Flow**: Attacker calls joinPool, during callback the oracle returns manipulated price, healthy positions get liquidated unfairly.

### Example 2: Classic Reentrancy in Settlement (HIGH - Cega)

**Reference**: reentrancy-in-vault-settlement.md

State updated AFTER external call:

    function settleVault(address vaultAddress, ITreasury treasury) internal {
        require(!vault.isInDispute, "trade in dispute");
        treasury.withdraw(depositAsset, msg.sender, totalAssets);  // External call
        VaultLogic.setVaultSettlementStatus(vaultAddress, Settled); // State after
    }

### Example 3: Reentrancy Lock Bypass (MEDIUM - Uniswap Compact)

**Reference**: attacker-can-bypass-reentrancy-lock-to-double-spend-deposit.md

Lock bypassed during storage migration from sstore to tstore.

---

## Secure Implementation Patterns

### Fix 1: Checks-Effects-Interactions Pattern

    function settleVault(address vaultAddress, ITreasury treasury) internal {
        require(!vault.isInDispute, "trade in dispute");
        VaultLogic.setVaultSettlementStatus(vaultAddress, Settled); // State first
        treasury.withdraw(depositAsset, msg.sender, totalAssets);   // Call last
    }

### Fix 2: ReentrancyGuard Modifier

    import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
    
    contract SecureVault is ReentrancyGuard {
        function settleVault(address vaultAddress) external nonReentrant {
            treasury.withdraw(depositAsset, msg.sender, totalAssets);
        }
    }

### Fix 3: Read-Only Reentrancy Protection

Check Balancer Vault reentrancy state before querying:

    function liquidate(address user) external {
        VaultReentrancyLib.ensureNotInVaultContext(balancerVault);
        uint256 price = oracle.getPrice(collateralToken);
    }

---

## Impact Analysis

| Scenario | Frequency | Severity |
|----------|-----------|----------|
| ETH transfers with callbacks | Common | HIGH |
| Read-only reentrancy (Balancer) | Common | HIGH |
| ERC777/ERC1155 callbacks | Moderate | HIGH |
| Flash loan callbacks | Common | HIGH |

---

## Detection Checklist

- [ ] All external calls follow Checks-Effects-Interactions pattern
- [ ] Functions with ETH transfers have nonReentrant modifier
- [ ] View functions querying external protocols check reentrancy state
- [ ] Balancer/Curve integrations use reentrancy guards

---

## Real-World Examples

| Protocol | Vulnerability | Severity | Auditor |
|----------|--------------|----------|---------|
| Blueberry | Read-only reentrancy in Balancer oracle | HIGH | Sherlock |
| Cega | Classic reentrancy in vault settlement | HIGH | OtterSec |
| Uniswap Compact | Reentrancy lock bypass | MEDIUM | Spearbit |
| Sentiment | Read-only reentrancy (exploited) | CRITICAL | N/A |

---

## Keywords

reentrancy, reentrant, nonReentrant, read-only reentrancy, CEI pattern, callback, Balancer, Curve, double spend

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

`Access Control/State Management`, `deposit`, `getPrice`, `liquidate`, `msg.sender`, `settleVault`, `swap`, `totalSupply`, `withdraw`
