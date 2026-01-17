---
# Core Classification
protocol: Burve 
chain: everychain
category: amm
vulnerability_type: unrestricted_callback

# Attack Vector Details
attack_type: fund_theft
affected_component: uniswap_v3_integration

# Source Information
source: reports/constantproduct/c-04-draining-approved-tokens-by-unrestricted-uniswapv3mintcallback.md
audit_firm: Pashov Audit Group
severity: critical

# Impact Classification
impact: complete_fund_drainage
exploitability: 1.0
financial_impact: critical

# Context Tags
tags:
  - uniswap_v3
  - callback
  - access_control
  - fund_theft
  - approval_exploit

# Version Info
language: solidity
version: all
---

# Burve Protocol - Unrestricted Uniswap V3 Mint Callback Vulnerability

## Unique Protocol Issue

**Protocol**: Burve  
**Audit Firm**: Pashov Audit Group  
**Severity**: CRITICAL  
**Source**: `reports/constantproduct/c-04-draining-approved-tokens-by-unrestricted-uniswapv3mintcallback.md`

## Overview

The Burve protocol implemented a Uniswap V3 integration with a flaw: the `uniswapV3MintCallback` function has no access control. This callback, which is designed to be called only by the Uniswap V3 pool during liquidity minting operations, can be called by anyone with arbitrary data, allowing attackers to drain tokens from any address that has approved the Burve contract.

## Why This Is Unique to Burve

Unlike generic callback vulnerabilities, this specific issue:
1. **Callback-Sourced Address**: The source address for token transfers is decoded from user-controlled `data` parameter
2. **No Pool Verification**: Function doesn't verify `msg.sender` is the legitimate pool
3. **Approval Chain Exploitation**: Exploits the trust model where users approve protocols to spend their tokens

## Vulnerable Code Pattern

```solidity
// ❌ CRITICAL: No access control on callback
function uniswapV3MintCallback(
    uint256 amount0Owed, 
    uint256 amount1Owed, 
    bytes calldata data
) external {
    // DANGER: Anyone can call this function!
    address source = abi.decode(data, (address));
    
    // DANGER: Transfers tokens from arbitrary address!
    TransferHelper.safeTransferFrom(token0, source, address(pool), amount0Owed);
    TransferHelper.safeTransferFrom(token1, source, address(pool), amount1Owed);
}
```

## Attack Scenario

1. **Identify Victims**: Attacker scans for addresses that have approved tokens to Burve contract
2. **Craft Malicious Data**: Attacker encodes victim's address in the `data` parameter
3. **Direct Call**: Attacker calls `uniswapV3MintCallback` directly (not through pool)
4. **Fund Drainage**: Victim's approved tokens are transferred to attacker-controlled address

```solidity
// Attack execution
function attack(address victim) external {
    bytes memory maliciousData = abi.encode(victim);
    uint256 victimBalance0 = IERC20(token0).balanceOf(victim);
    uint256 victimBalance1 = IERC20(token1).balanceOf(victim);
    
    // This should only be callable by the pool, but there's no check!
    BurveContract.uniswapV3MintCallback(victimBalance0, victimBalance1, maliciousData);
    // Victim's tokens now transferred to pool, attacker profits
}
```

## Impact

- **Direct Fund Loss**: Complete drainage of approved tokens from all users
- **Scope**: Affects every address that ever approved the contract
- **Severity**: Critical - immediate fund theft possible
- **No User Action Required**: Victims don't need to interact, just have approval

## Secure Implementation

```solidity
// ✅ SECURE: Callback restricted to pool
function uniswapV3MintCallback(
    uint256 amount0Owed, 
    uint256 amount1Owed, 
    bytes calldata data
) external {
    // CRITICAL: Verify caller is the legitimate pool
    require(msg.sender == address(pool), "Only pool can call callback");
    
    // Now safe to transfer tokens
    IERC20(token0).safeTransfer(address(pool), amount0Owed);
    IERC20(token1).safeTransfer(address(pool), amount1Owed);
}
```

## Detection Patterns

Look for these red flags when auditing Uniswap V3 integrations:

```
- uniswapV3MintCallback without msg.sender check
- uniswapV3SwapCallback without msg.sender check
- Callback functions with user-controlled source addresses
- TransferFrom with decoded address parameters
```

## Lessons for Auditors

1. **All Callbacks Need Access Control**: Uniswap V3 callbacks MUST verify `msg.sender == pool`
2. **Trust Boundaries**: Callbacks create trust boundaries - user data should not determine fund sources
3. **Approval Scans**: During exploits, check on-chain for addresses with approvals
4. **Similar Patterns**: Same vulnerability applies to all Uniswap V3 callback functions

## Related Vulnerabilities

- Uniswap V3 Flash Callback exploits
- ERC-777 reentrancy through callbacks
- General access control missing on privileged functions

## Keywords

`uniswapV3MintCallback`, `callback_access_control`, `approval_exploit`, `transferFrom_arbitrary_source`, `pool_verification`, `burve`, `uniswap_v3_integration`, `fund_drainage`
