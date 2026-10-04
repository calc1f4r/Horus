---
# Core Classification
protocol: Level  Money
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46585
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/612f3254-f6a6-420d-8d51-fb058e4af022
source_link: https://cdn.cantina.xyz/reports/cantina_level_money_october_2024.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Mario Poneder
  - Delvir0
  - Om Parikh
---

## Vulnerability Title

USDT cannot be withdrawn from AaveV3YieldManager 

### Overview


A bug has been found in the AaveV3YieldManager contract, specifically in the withdraw function. This bug affects the ability to withdraw USDT, a type of cryptocurrency, from the contract. This is due to the implementation of USDT not being fully ERC20-compliant. This means that the contract is not able to handle USDT properly, causing any attempts to withdraw USDT to result in an error. This bug breaks the intended flow of funds in the protocol, and USDT must be manually processed instead. This bug has been fixed in the latest updates to the contract. It is recommended to always use the SafeERC20 library when dealing with ERC20 tokens to avoid similar issues. 

### Original Finding Content

## Issue Report: USDT Withdrawal Limitation in AaveV3YieldManager

## Context
- **File Locations:**
  - `LevelEigenlayerReserveManager.sol#L70`
  - `AaveV3YieldManager.sol#L92`
  - `AaveV3YieldManager.sol#L104`

## Description
USDT can only be deposited into but not withdrawn from the AaveV3YieldManager contract due to the implementation of USDT, which is not fully ERC20-compliant. The AaveV3YieldManager is intended to handle USDC & USDT (with plans for more tokens in the future) for interest accrual by supplying them as collateral to AAVE and wrapping the resulting rebasing & interest-accruing tokens.

However, the `withdraw` method relies on `IERC20.transfer`, which expects a boolean return value. Solidity attempts to decode this return value even though it is not checked, while `USDT.transfer` does not implement a return value. Consequently, any attempt to withdraw USDT using this method will result in a revert.

### Example Function
```solidity
function withdraw(
    address token, // e.g. USDT
    uint256 amount
) external {
    address aTokenAddress = underlyingToaToken[token];
    address wrapper = tokenToWrapper[aTokenAddress];
    IERC20(wrapper).safeTransferFrom(msg.sender, address(this), amount);
    _unwrapToken(wrapper, amount);
    _withdrawFromAave(token, amount);
    IERC20(token).transfer(msg.sender, amount); // IERC20.transfer expects bool return value
}
```

## Impact
USDT cannot be withdrawn from the AaveV3YieldManager contract, breaking the protocol's intended flow of funds. Unwrapping and withdrawal from AAVE must be processed manually instead.

## Likelihood
USDT is fully intended to be used with the AaveV3YieldManager contract.

## Recommendation
It is recommended to always rely on the SafeERC20 library instead of calling `transfer`, `transferFrom`, and `approve` of ERC20 tokens directly. This recommendation applies to all three instances attached to this finding.

## Level
- Fixed in PR 25 and PR 26.

## Cantina Managed
- Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Level  Money |
| Report Date | N/A |
| Finders | Mario Poneder, Delvir0, Om Parikh |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_level_money_october_2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/612f3254-f6a6-420d-8d51-fb058e4af022

### Keywords for Search

`vulnerability`

