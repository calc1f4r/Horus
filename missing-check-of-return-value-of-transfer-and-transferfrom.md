---
# Core Classification
protocol: Frax Solidity
chain: everychain
category: logic
vulnerability_type: weird_erc20

# Attack Vector Details
attack_type: weird_erc20
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17933
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
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
  - weird_erc20
  - check_return_value
  - data_validation
  - erc20
  - validation

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Samuel Moelius Maximilian Krüger Troy Sargent
---

## Vulnerability Title

Missing check of return value of transfer and transferFrom

### Overview


This bug report focuses on a vulnerability in the TWAMM.sol contract, which is part of the Frax project. The vulnerability occurs when tokens that do not precisely follow the ERC20 specification are used, as they may return false or fail silently instead of reverting. The problem is that the codebase does not consistently use OpenZeppelin's SafeERC20 library, so the return values of calls to transfer and transferFrom are not being checked. This allows an attacker to call provideLiquidity and mint LP tokens for free, as the transferFrom call fails silently or returns false.

In order to fix this issue, the instance mentioned in the report should be fixed, and all instances detected by Slither should be fixed. Additionally, the Token Integration Checklist in Appendix D should be reviewed, and Slither should be integrated into the project’s CI pipeline to prevent regression and catch new instances proactively.

### Original Finding Content

## Frax Solidity Security Assessment

## Difficulty: Medium

## Type: Undefined Behavior

## Target: TWAMM.sol

### Description
Some tokens, such as BAT, do not precisely follow the ERC20 specification and will return
false or fail silently instead of reverting. Because the codebase does not consistently use
OpenZeppelin’s SafeERC20 library, the return values of calls to `transfer` and
`transferFrom` should be checked. However, return value checks are missing from these
calls in many areas of the code, opening the TWAMM contract (the time-weighted automated
market maker) to severe vulnerabilities.

```solidity
function provideLiquidity(uint256 lpTokenAmount) external {
    require(totalSupply() != 0, 'EC3');
    // execute virtual orders
    longTermOrders.executeVirtualOrdersUntilCurrentBlock(reserveMap);
    // the ratio between the number of underlying tokens and the number of lp tokens
    // must remain invariant after mint
    uint256 amountAIn = lpTokenAmount * reserveMap[tokenA] / totalSupply();
    uint256 amountBIn = lpTokenAmount * reserveMap[tokenB] / totalSupply();
    ERC20(tokenA).transferFrom(msg.sender, address(this), amountAIn);
    ERC20(tokenB).transferFrom(msg.sender, address(this), amountBIn);
}
```
*Figure 20.1: contracts/FPI/TWAMM.sol#L125-136*

### Exploit Scenario
Frax deploys the TWAMM contract. Pools are created with tokens that do not revert on
failure, allowing an attacker to call `provideLiquidity` and mint LP tokens for free; the
attacker does not have to deposit funds since the `transferFrom` call fails silently or
returns false.

### Recommendations
- Short term: Fix the instance described above. Then, fix all instances detected by Slither.
  - Detect unchecked-transfer.
  
- Long term: Review the Token Integration Checklist in appendix D and integrate Slither into 
  the project’s CI pipeline to prevent regression and catch new instances proactively.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Solidity |
| Report Date | N/A |
| Finders | Samuel Moelius Maximilian Krüger Troy Sargent |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf

### Keywords for Search

`Weird ERC20, Check Return Value, Data Validation, ERC20, Validation`

