---
# Core Classification
protocol: Ondo RWA Internal
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55266
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Ondo-Spearbit-Security-Review-March-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Ondo-Spearbit-Security-Review-March-2025.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - CarrotSmuggler
  - Anurag Jain
  - Desmond Ho
---

## Vulnerability Title

availableToWithdraw does not check paused state

### Overview

See description below for full details.

### Original Finding Content

## Low Risk Vulnerability Report

## Severity
Low Risk

## Context
- **BuidlUSDCSource.sol**: Lines 202-210
- **PSMSource.sol**: Lines 186-201

## Description
Due to how the `OndoTokenRouter` contract is set up, it expects the result of the `availableToWithdraw` call to be available for withdrawal from all the token sources. If the `availableToWithdraw` function returns a non-zero value but this amount is not actually obtainable by calling the `tokenSource.withdrawToken` function, it can lead to reverts or broken accounting.

```solidity
uint256 amountAvailable = tokenSource.availableToWithdraw(outputToken);
uint256 withdrawAmount = amountAvailable > requestedWithdrawAmount
    ? requestedWithdrawAmount
    : amountAvailable;

// INVARIANT - `TokenSource.withdrawToken` will always withdraw the amount requested
// or revert.
tokenSource.withdrawToken(outputToken, withdrawAmount);
```

Some of the token source contracts are pausable. In case they are paused, the amount reported should be 0, so that the router does not try to extract tokens from it.

The `BuidlUSDCSource` contract reports the available liquidity in the BUIDL settlement contract but doesn't check if the contracts are paused, and thus, if this amount is actually obtainable. If the BUIDL redemption is paused, the `withdrawToken` calls to this token source contract can revert.

Similarly, the `PSMSource` contract uses the USDS PSM module which implements a tin parameter that assigns the paused state. This can be verified at the following address:
- `0xA188EEC8F81263234dA3622A406892F3D630f98c`

Calls to this contract can also revert when it is paused.

## Proof of Concept
Assume the `BuidlUSDCSource` has 100 USDC tokens, 900 BUIDL tokens, and the BUIDL settlement contract has enough liquidity but is paused. The `availableToWithdraw` function will report 1000 USDC. However, the contract can only dispense up to 100 USDC. Any more, and the redeem function will be called on the BUIDL redeemer, which will cause the transaction to revert since it is paused.

## Recommendation
Check the paused state of underlying contracts. If paused, only the current USDC balance in the token source contract is available, and any redemptions/swaps are offline.

## Additional Information
- **Ondo Finance**: Fixed in commit `a876a50b`.
- **Spearbit**: Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Ondo RWA Internal |
| Report Date | N/A |
| Finders | CarrotSmuggler, Anurag Jain, Desmond Ho |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Ondo-Spearbit-Security-Review-March-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Ondo-Spearbit-Security-Review-March-2025.pdf

### Keywords for Search

`vulnerability`

