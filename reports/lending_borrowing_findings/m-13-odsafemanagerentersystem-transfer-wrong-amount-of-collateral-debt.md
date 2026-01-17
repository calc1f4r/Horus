---
# Core Classification
protocol: Open Dollar
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29361
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-10-opendollar
source_link: https://code4rena.com/reports/2023-10-opendollar
github_link: https://github.com/code-423n4/2023-10-opendollar-findings/issues/159

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
finders_count: 1
finders:
  - klau5
---

## Vulnerability Title

[M-13] ODSafeManager.enterSystem - Transfer wrong amount of collateral, debt

### Overview


This bug report is about the `enterSystem` function in the OpenDollar platform. This function is responsible for sending the `lockedCollateral` and `generatedDebt` of a source address to the safeHandler. However, the function is currently sending the wrong amount of `lockedCollateral` and `generatedDebt` from the safeHandler, instead of from the source address. This is causing the `enterSystem` function to not succeed when the source address has less lockedCollateral and generatedDebt than the safeHandler.

The proof of concept code provided in the report shows how the `enterSystem` function is sending the wrong amounts of `lockedCollateral` and `generatedDebt` from the safeHandler instead of from the source address. The recommended mitigation step is to use `lockedCollateral` and `generatedDebt` of the source address.

The bug was judged to be of medium severity by the warden. The OpenDollar team also agreed that the bug was accurate, as the collateral and debt amounts were being recorded from the wrong address.

### Original Finding Content


If src has less lockedCollateral and generatedDebt than safeHandler, `enterSystem` cannot succeed.

The `enterSystem` function is behaving differently than intended.

### Proof of Concept

The `ODSafeManager.enterSystem` function retrieves the amount of safeHandler's `lockedCollateral` and `generatedDebt` and sends it to safeHandler. The purpose of this function is to send \_src's `lockedCollateral` and `generatedDebt` to safeHandler, so it is sending wrong amounts.

```solidity
  function enterSystem(address _src, uint256 _safe) external handlerAllowed(_src) safeAllowed(_safe) {
    SAFEData memory _sData = _safeData[_safe];
@>  ISAFEEngine.SAFE memory _safeInfo = ISAFEEngine(safeEngine).safes(_sData.collateralType, _sData.safeHandler);
@>  int256 _deltaCollateral = _safeInfo.lockedCollateral.toInt();
@>  int256 _deltaDebt = _safeInfo.generatedDebt.toInt();
    ISAFEEngine(safeEngine).transferSAFECollateralAndDebt(
@>    _sData.collateralType, _src, _sData.safeHandler, _deltaCollateral, _deltaDebt
    );
    emit EnterSystem(msg.sender, _src, _safe);
  }
```

### Recommended Mitigation Steps

Use `lockedCollateral` and `generatedDebt` of \_src.

```diff
function enterSystem(address _src, uint256 _safe) external handlerAllowed(_src) safeAllowed(_safe) {
  SAFEData memory _sData = _safeData[_safe];
+ ISAFEEngine.SAFE memory _safeInfo = ISAFEEngine(safeEngine).safes(_sData.collateralType, _src);
- ISAFEEngine.SAFE memory _safeInfo = ISAFEEngine(safeEngine).safes(_sData.collateralType, _sData.safeHandler);
  int256 _deltaCollateral = _safeInfo.lockedCollateral.toInt();
  int256 _deltaDebt = _safeInfo.generatedDebt.toInt();
  ISAFEEngine(safeEngine).transferSAFECollateralAndDebt(
    _sData.collateralType, _src, _sData.safeHandler, _deltaCollateral, _deltaDebt
  );
  emit EnterSystem(msg.sender, _src, _safe);
}
```

**[MiloTruck (Judge) commented](https://github.com/code-423n4/2023-10-opendollar-findings/issues/159#issuecomment-1791419211):**
 > The warden has demonstrated how `enterSystem()` calls `transferSAFECollateralAndDebt()` with collateral and debt amounts of the wrong safe handler, causing its functionality to be broken. As such, I agree with medium severity.

**[pi0neerpat (OpenDollar) commented](https://github.com/code-423n4/2023-10-opendollar-findings/issues/159#issuecomment-1805212633):**
 > This appears to be accurate, as the collateral and debt amounts are being recorded from the destination address instead of the source address.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Open Dollar |
| Report Date | N/A |
| Finders | klau5 |

### Source Links

- **Source**: https://code4rena.com/reports/2023-10-opendollar
- **GitHub**: https://github.com/code-423n4/2023-10-opendollar-findings/issues/159
- **Contest**: https://code4rena.com/reports/2023-10-opendollar

### Keywords for Search

`vulnerability`

