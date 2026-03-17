---
# Core Classification
protocol: Spartan Protocol
chain: bsc
category: amm
vulnerability_type: lp_hijack

# Attack Vector Details
attack_type: pool_hijack
affected_component: liquidity_token

# Source Information
source: reports/constantproduct/h-10-hijack-token-pool-by-burning-liquidity-token.md
audit_firm: Code4rena
severity: high

# Impact Classification
impact: permanent_pool_hijack
exploitability: 1.0
financial_impact: high

# Context Tags
tags:
  - LP_burn
  - pool_hijack
  - rounding_attack
  - totalSupply_manipulation

# Version Info
language: solidity
version: all

# Pattern Identity (Required)
root_cause_family: logic_error
pattern_key: logic_error | liquidity_token | lp_hijack

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - addLiquidity
  - burn
  - calcLiquidityUnits
  - deposit
  - hijackPool
  - mint
  - msg.sender
  - profitFromHijack
  - proveHijack
  - receive
  - removeLiquidity
  - swap
  - totalSupply
  - transferFrom
  - withdraw
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [Spartan Protocol] | reports/constantproduct/h-10-hijack-token-pool-by-burning-liquidity-token.md | HIGH | Code4rena | - |


# Spartan Protocol - LP Token Burn Pool Hijack

## Unique Protocol Issue

**Protocol**: Spartan Protocol  
**Audit Firm**: Code4rena  
**Severity**: HIGH  
**Source**: `reports/constantproduct/h-10-hijack-token-pool-by-burning-liquidity-token.md`

## Overview

Spartan Protocol allowed users to burn LP tokens without withdrawing underlying assets. An attacker could burn their LP tokens down to 1, making `totalSupply = 1`, which causes ALL future LP minting to round down to 0. The attacker becomes the permanent sole owner of the pool's liquidity.



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of logic_error"
- Pattern key: `logic_error | liquidity_token | lp_hijack`
- Interaction scope: `single_contract`
- Primary affected component(s): `liquidity_token`
- High-signal code keywords: `addLiquidity`, `burn`, `calcLiquidityUnits`, `deposit`, `hijackPool`, `mint`, `msg.sender`, `profitFromHijack`
- Typical sink / impact: `permanent_pool_hijack`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `PoolHijacker.function -> SecurePool.function -> SpartanPool.function`
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

## Why This Is Unique to Spartan

Spartan's LP token formula combined with unrestricted burn created a unique exploit:
1. **Unrestricted Burn**: Anyone could burn LP tokens without withdrawing
2. **LP Formula Dependency**: LP tokens calculated as `P * (deposits) / (reserves)` where P = totalSupply
3. **Rounding to Zero**: When P = 1, all calculations round down to 0
4. **Permanent Hijack**: Attacker becomes sole LP, no one else can ever get tokens

## Vulnerable Code Pattern

```solidity
// ❌ VULNERABLE: Burn without withdrawal allowed
contract SpartanPool {
    function burn(uint256 amount) external {
        // Burns LP tokens but does NOT withdraw underlying!
        _burn(msg.sender, amount);
        // Attacker can reduce totalSupply to 1
    }
    
    function addLiquidity(uint256 amountA, uint256 amountB) external returns (uint256 units) {
        // LP calculation from Utils.calcLiquidityUnits
        // units = P * (part1 + part2) / part3
        // where P = totalSupply
        
        // When P = 1:
        // units = 1 * (small_number) / (large_number)
        // units = 0  <-- ALWAYS rounds to zero!
        
        units = Utils.calcLiquidityUnits(amountA, amountB, reserveA, reserveB, totalSupply);
        
        if (units > 0) {  // This check passes, but units = 0!
            _mint(msg.sender, units);  // Nothing minted!
        }
        
        // Tokens transferred but no LP received
        IERC20(tokenA).transferFrom(msg.sender, address(this), amountA);
        IERC20(tokenB).transferFrom(msg.sender, address(this), amountB);
    }
}

// From Utils.sol - LP token calculation
function calcLiquidityUnits(uint b, uint B, uint t, uint T, uint P) public pure returns (uint units) {
    // units = ((P (t B + T b))/(2 T B)) * slipAdjustment
    uint slipAdjustment = getSlipAdustment(b, B, t, T);
    uint part1 = t * B;
    uint part2 = T * b;
    uint part3 = T * B * 2;
    uint _units = (P * (part1 + part2)) / part3;  // P=1 makes this tiny
    return _units * slipAdjustment / 1e18;  // Rounds to 0
}
```

## Attack Scenario

```solidity
contract PoolHijacker {
    SpartanPool pool;
    
    function hijackPool() external {
        // 1. Create new pool as first depositor
        factory.createPool(TOKEN_A, TOKEN_B);
        
        // 2. Add initial liquidity (get some LP tokens)
        uint256 initialLP = pool.addLiquidity(1000 ether, 1000 ether);
        // initialLP = 1000e18 (for example)
        
        // 3. Burn almost all LP tokens (keep just 1)
        pool.burn(initialLP - 1);
        // totalSupply is now 1
        
        // 4. Pool is hijacked! Let's prove it:
    }
    
    function proveHijack() external {
        // Victim tries to deposit 1 million of each token
        // They receive... 0 LP tokens!
        
        // P = 1 (totalSupply)
        // Calculation: 1 * (1M * reserves) / (reserves * reserves * 2)
        // = tiny fraction that rounds to 0
        
        // Victim's tokens are added to reserves
        // But victim gets 0 LP tokens
        // Attacker's 1 LP token now owns all the liquidity!
    }
    
    function profitFromHijack() external {
        // Attacker can withdraw ALL liquidity
        // Including all tokens deposited by victims!
        pool.removeLiquidity(1);  // Their 1 LP = 100% of pool
    }
}
```

## Mathematical Proof

```
Initial State After Hijack:
- totalSupply (P) = 1
- reserveA = 1000 ether
- reserveB = 1000 ether
- Attacker owns 1 LP token (100% of supply)

Victim deposits 1,000,000 of each token:
- b = 1,000,000 ether (tokenA deposit)
- t = 1,000,000 ether (tokenB deposit)
- B = 1000 ether (reserveA)
- T = 1000 ether (reserveB)

LP calculation:
units = P * (t*B + T*b) / (2*T*B)
units = 1 * (1e24 + 1e24) / (2 * 1e6)
units = 1 * 2e24 / 2e6
units = 1e18

But with slippage adjustment (< 1) and integer division:
final_units = 1e18 * slipAdj / 1e18
final_units = 0 (rounds down!)

Result: Victim deposits 1M tokens, receives 0 LP
```

## Impact

- **Permanent Pool Hijack**: Attacker becomes sole owner of all pool liquidity
- **User Fund Theft**: All subsequent deposits go to attacker
- **Irreversible**: Cannot fix without pool migration
- **Factory-Wide Risk**: All permissionlessly created pools vulnerable

## Secure Implementation

```solidity
// ✅ SECURE: Prevent burn without withdrawal / maintain minimum supply
contract SecurePool {
    uint256 public constant MINIMUM_LIQUIDITY = 1000;
    
    // Option 1: No public burn function
    // function burn() - REMOVED
    
    // Option 2: Burn only allowed with withdrawal
    function removeLiquidity(uint256 lpAmount) external returns (uint256 amountA, uint256 amountB) {
        require(lpAmount > 0, "Cannot remove 0");
        
        // Calculate proportional withdrawal
        amountA = lpAmount * reserveA / totalSupply;
        amountB = lpAmount * reserveB / totalSupply;
        
        // Burn LP AND withdraw tokens atomically
        _burn(msg.sender, lpAmount);
        IERC20(tokenA).transfer(msg.sender, amountA);
        IERC20(tokenB).transfer(msg.sender, amountB);
    }
    
    // Option 3: Maintain minimum liquidity (Uniswap V2 style)
    function addLiquidity(uint256 amountA, uint256 amountB) external returns (uint256 liquidity) {
        if (totalSupply == 0) {
            liquidity = sqrt(amountA * amountB) - MINIMUM_LIQUIDITY;
            _mint(address(0), MINIMUM_LIQUIDITY);  // Permanently locked
        } else {
            liquidity = min(
                amountA * totalSupply / reserveA,
                amountB * totalSupply / reserveB
            );
        }
        require(liquidity > 0, "Insufficient liquidity minted");
        _mint(msg.sender, liquidity);
    }
}
```

## Detection Patterns

```solidity
// RED FLAGS:
// 1. Public burn without withdrawal
function burn(uint amount) public { _burn(msg.sender, amount); }

// 2. LP calculation dependent on totalSupply
units = totalSupply * ... / ...

// 3. No minimum liquidity lock
// First depositor can remove all LP

// 4. No minimum LP mint requirement
// Can mint 0 LP tokens
```

## Lessons for Auditors

1. **Minimum Liquidity**: Always lock initial liquidity (Uniswap's 1000 MINIMUM_LIQUIDITY)
2. **Atomic Burn+Withdraw**: Never allow burning LP without proportional withdrawal
3. **Division-First Hazards**: When totalSupply is in numerator, small values cause rounding
4. **Minimum Mint Requirements**: Require non-zero LP mints
5. **Pool Initialization**: First depositor has outsized power - be careful

## Keywords

`LP_burn`, `pool_hijack`, `totalSupply_manipulation`, `rounding_attack`, `liquidity_token`, `spartan`, `first_depositor`, `minimum_liquidity`, `integer_division`

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

`LP_burn`, `addLiquidity`, `amm`, `burn`, `calcLiquidityUnits`, `deposit`, `hijackPool`, `lp_hijack`, `mint`, `msg.sender`, `pool_hijack`, `profitFromHijack`, `proveHijack`, `receive`, `removeLiquidity`, `rounding_attack`, `swap`, `totalSupply`, `totalSupply_manipulation`, `transferFrom`, `withdraw`
