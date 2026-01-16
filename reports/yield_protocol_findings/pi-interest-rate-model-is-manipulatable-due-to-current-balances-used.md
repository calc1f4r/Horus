---
# Core Classification
protocol: Cod3x lend
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49196
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Cod3x-Spearbit-Security-Review-December-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Cod3x-Spearbit-Security-Review-December-2024.pdf
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

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Saw-mon and Natalie
  - Cergyk
  - Jonatas Martins
---

## Vulnerability Title

Pi interest rate model is manipulatable due to current balances used

### Overview


This bug report is about a medium risk issue in the BasePiReserveRateStrategy.sol file. The problem is that the interest rate is being controlled by the utilization factor, which is calculated using instant values for available liquidity and debt. This allows participants to manipulate the rate in their favor by using flash loans or borrowing. The recommendation is to use previous values for available liquidity and debt to update the rate. The bug has been acknowledged by Cod3x and Spearbit.

### Original Finding Content

## Severity: Medium Risk

## Context
BasePiReserveRateStrategy.sol#L253

## Description
The interest rate is controlled by the utilization factor:

```solidity
function _calculateInterestRates(
    address,
    uint256 availableLiquidity,
    uint256 totalVariableDebt,
    uint256 reserveFactor
) internal returns (uint256, uint256, uint256) {
    uint256 utilizationRate = totalVariableDebt == 0
        ? 0
        : totalVariableDebt.rayDiv(availableLiquidity + totalVariableDebt);
    
    // If no borrowers we reset the strategy
    if (utilizationRate == 0) {
        _errI = 0;
        _lastTimestamp = block.timestamp;
        return (0, 0, 0);
    }
    // PID state update
    int256 err = getNormalizedError(utilizationRate);
    _errI += int256(_ki).rayMulInt(err * int256(block.timestamp - _lastTimestamp)); // <<<
    
    if (_errI < _maxErrIAmp) _errI = _maxErrIAmp; // Limit _errI negative accumulation.
    _lastTimestamp = block.timestamp;
    
    int256 controllerErr = getControllerError(err);
    uint256 currentVariableBorrowRate = transferFunction(controllerErr);
    uint256 currentLiquidityRate = getLiquidityRate(currentVariableBorrowRate, utilizationRate, reserveFactor);
    
    emit PidLog(
        utilizationRate, currentLiquidityRate, currentVariableBorrowRate, err, controllerErr
    );
    
    return (currentLiquidityRate, currentVariableBorrowRate, utilizationRate);
}
```

Unfortunately, since instant values for available liquidity and debt are used (and `_errI` is only updated once per block), it is possible for participants to manipulate the direction of the rate at their advantage by using a flash loan or a borrow:

- **Borrower side:** The borrower can first use a flash loan to deposit into the pool, then withdraw, and finally borrow (_errI won't be updated for the last two operations).
- **Lender side:** The lender can first borrow, increasing _errI, and then repay the same amount (repaying won't change _errI in the same block).

## Recommendation
Use previous `availableLiquidity` and `totalVariableDebt` to update `_errI`.

## Cod3x
Acknowledged.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Cod3x lend |
| Report Date | N/A |
| Finders | Saw-mon and Natalie, Cergyk, Jonatas Martins |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Cod3x-Spearbit-Security-Review-December-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Cod3x-Spearbit-Security-Review-December-2024.pdf

### Keywords for Search

`vulnerability`

