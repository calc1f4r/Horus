---
# Core Classification
protocol: AAVE
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28718
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/AAVE/protocol%20v2/README.md#interest-rate-miscalculation-due-to-stale-debt-values
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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Interest Rate Miscalculation Due to Stale Debt Values

### Overview


This bug report is about the debt reserve interest rates being updated before debt burning takes place in a lending pool collateral manager. This can lead to stale total debt values being used during interest rates calculation. To fix this, the developer is recommended to switch the `updateInterestRates` and the `if` statement.

### Original Finding Content

##### Description

https://github.com/aave/protocol-v2/blob/f435b2fa0ac589852ca3dd6ae2b0fbfbc7079d54/contracts/lendingpool/LendingPoolCollateralManager.sol#L227-L232

```solidity
principalReserve.updateInterestRates(
  principal,
  principalReserve.aTokenAddress,
  vars.actualAmountToLiquidate,
  0
);

if (vars.userVariableDebt >= vars.actualAmountToLiquidate) {
  IVariableDebtToken(principalReserve.variableDebtTokenAddress).burn(
    user,
    vars.actualAmountToLiquidate,
    principalReserve.variableBorrowIndex
  );
} else {
  IVariableDebtToken(principalReserve.variableDebtTokenAddress).burn(
    user,
    vars.userVariableDebt,
    principalReserve.variableBorrowIndex
  );

  IStableDebtToken(principalReserve.stableDebtTokenAddress).burn(
    user,
    vars.actualAmountToLiquidate.sub(vars.userVariableDebt)
  );
}
```

https://github.com/aave/protocol-v2/blob/f435b2fa0ac589852ca3dd6ae2b0fbfbc7079d54/contracts/lendingpool/LendingPoolCollateralManager.sol#L409-L414

```solidity
debtReserve.updateInterestRates(
  principal,
  vars.principalAToken,
  vars.actualAmountToLiquidate,
  0
);
IERC20(principal).safeTransferFrom(receiver, vars.principalAToken, vars.actualAmountToLiquidate);

if (vars.userVariableDebt >= vars.actualAmountToLiquidate) {
  IVariableDebtToken(debtReserve.variableDebtTokenAddress).burn(
    user,
    vars.actualAmountToLiquidate,
    debtReserve.variableBorrowIndex
  );
} else {
  IVariableDebtToken(debtReserve.variableDebtTokenAddress).burn(
    user,
    vars.userVariableDebt,
    debtReserve.variableBorrowIndex
  );
  IStableDebtToken(debtReserve.stableDebtTokenAddress).burn(
    user,
    vars.actualAmountToLiquidate.sub(vars.userVariableDebt)
  );
}
```

Debt reserve interest rates are updated before debt burning takes place.

As a result, stale total debt values are used during interest rates calculation. 

##### Recommendation
We suggest switching `updateInterestRates` and the `if` statement.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | AAVE |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/AAVE/protocol%20v2/README.md#interest-rate-miscalculation-due-to-stale-debt-values
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

