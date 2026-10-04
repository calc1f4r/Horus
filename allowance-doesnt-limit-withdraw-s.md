---
# Core Classification
protocol: Gauntlet
chain: everychain
category: uncategorized
vulnerability_type: allowance

# Attack Vector Details
attack_type: allowance
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7089
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - allowance

protocol_categories:
  - dexes
  - cdp
  - yield
  - insurance
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Emanuele Ricci
  - Eric Wang
  - Gerard Persoon
---

## Vulnerability Title

allowance() doesn’t limit withdraw() s

### Overview


This bug report concerns the withdrawal function of the AeraVaultV1.sol code. The allowance() function is meant to limit the amount of funds that can be withdrawn, however, the visibility of the allowance() function is set to view, meaning it can only read and not alter state. This renders the allowance() function ineffective and allows the withdraw() function to be called on demand until the entire Vault/Pool balance has been drained. 

The recommendation is to remove the view keyword from the allowance() template in both IWithdrawalValidator.sol and PermissiveWithdrawalValidator.sol in order to update state in future versions of the allowance() function. Additionally, an additional callback to the Validator is suggested to notify it of actual withdraw amounts, as in cases when allowance is greater than holdings there is no way for the Validator to know how much of its allowance was used.

### Original Finding Content

## High Risk Severity Report

## Context
- **PermissiveWithdrawalValidator.sol**: Lines 17-27
- **IWithdrawalValidator.sol**
- **AeraVaultV1.sol**: Lines 456-514

## Description
The `allowance()` function is meant to limit withdrawal amounts. However, `allowance()` can only read and not alter state because its visibility is set to `view`. Therefore, the `withdraw()` function can be called on demand until the entire Vault/Pool balance has been drained, rendering the `allowance()` function ineffective.

```solidity
function withdraw(uint256[] calldata amounts) ... {
    ...
    uint256[] memory allowances = validator.allowance();
    ...
    for (uint256 i = 0; i < tokens.length; i++) {
        if (amounts[i] > holdings[i] || amounts[i] > allowances[i]) {
            revert Aera__AmountExceedAvailable(... );
        }
    }
}
```

### Note on `allowance()`
```solidity
// can't update state due to view
function allowance() external view override returns (uint256[] memory amounts) {
    amounts = new uint256[](count);
    for (uint256 i = 0; i < count; i++) {
        amounts[i] = ANY_AMOUNT;
    }
}
```

## Recommendation
Remove the `view` keyword from the `allowance()` template, e.g., from both `IWithdrawalValidator.sol` and `PermissiveWithdrawalValidator.sol`, to allow for state updates in future versions of `allowance()`.

## Gauntlet
I would say we need an additional callback to the Validator to notify it of actual withdrawal amounts. In cases where allowance is greater than holdings, there is no way for the Validator to know how much of its allowance was actually used.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Gauntlet |
| Report Date | N/A |
| Finders | Emanuele Ricci, Eric Wang, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review.pdf

### Keywords for Search

`Allowance`

