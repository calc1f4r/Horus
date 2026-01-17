---
# Core Classification
protocol: BadgerDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54633
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/e7dac53a-6098-4aa1-aa0f-ea44ee87050e
source_link: https://cdn.cantina.xyz/reports/cantina_badger_august2023.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - hyh
  - StErMi
---

## Vulnerability Title

EIP-3156 requires flashFee() and maxFlashLoan() to accommodate their logic to flashLoansPaused ﬂag 

### Overview


This bug report is about a problem with the `flashFee()` and `maxFlashLoan()` functions in two files, BorrowerOperations.sol and ActivePool.sol. These functions are used for flash loans, which are a type of loan that is borrowed and repaid within the same transaction. According to a standard called ERC-3156, these functions should behave in a certain way when a certain flag is turned on. However, the current code does not follow this standard and can cause issues with other programs that use these functions. The report recommends making changes to the code so that it follows the standard when the flag is turned on. Some organizations have already acknowledged and addressed the issue. 

### Original Finding Content

## Context
- **Files**: BorrowerOperations.sol#L816-L828, ActivePool.sol#L311-L332

## Description
Per ERC-3156, `flashFee()` can revert, while `maxFlashLoan()` can return 0 when `flashLoansPaused == true`:

- The `maxFlashLoan` function **MUST** return the maximum loan possible for token. If a token is not currently supported, `maxFlashLoan` **MUST** return 0, instead of reverting.
- The `flashFee` function **MUST** return the fee charged for a loan of amount token. If the token is not supported, `flashFee` **MUST** revert.

Currently, the flag is ignored in the logic:

```solidity
// BorrowerOperations.sol#L816-L828
function flashFee(address token, uint256 amount) public view override returns (uint256) {
    require(token == address(ebtcToken), "BorrowerOperations: EBTC Only");
    return (amount * feeBps) / MAX_BPS;
}

/// @dev Max flashloan, exclusively in ETH equals to the current balance
function maxFlashLoan(address token) public view override returns (uint256) {
    if (token != address(ebtcToken)) {
        return 0;
    }
    return type(uint112).max;
}
```

On the same grounds as eBTC, `flashFee()` and `maxFlashLoan()` need to change their behavior when `flashLoansPaused == true` for ActivePool's stETH flash loans.

## Impact
In both cases, the flash loan logic does not comply with EIP-3156 when `flashLoansPaused` is on, which can break the integrations.

## Recommendation
- `flashFee()` can revert, while `maxFlashLoan()` can return 0 when `flashLoansPaused == true` in both cases.

## Responses
- **BadgerDao**: Addressed in PR 574.
- **Cantina**: The recommendations have been implemented in PR 574.
- **BadgerDAO**: Acknowledged.
- **Cantina**: Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | BadgerDAO |
| Report Date | N/A |
| Finders | hyh, StErMi |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_badger_august2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/e7dac53a-6098-4aa1-aa0f-ea44ee87050e

### Keywords for Search

`vulnerability`

