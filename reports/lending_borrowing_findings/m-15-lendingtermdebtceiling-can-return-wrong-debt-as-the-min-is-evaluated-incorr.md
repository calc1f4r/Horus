---
# Core Classification
protocol: Ethereum Credit Guild
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30235
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-12-ethereumcreditguild
source_link: https://code4rena.com/reports/2023-12-ethereumcreditguild
github_link: https://github.com/code-423n4/2023-12-ethereumcreditguild-findings/issues/708

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
finders_count: 19
finders:
  - 0xStalin
  - mussucal
  - santipu\_
  - neocrao
  - The-Seraphs
---

## Vulnerability Title

[M-15] `LendingTerm::debtCeiling()` can return wrong debt as the `min()` is evaluated incorrectly

### Overview


The bug report discusses an issue with the `LendingTerm::debtCeiling()` function in a code written in Solidity. This function is used to calculate the minimum value out of three variables, but the current logic is flawed and may return an incorrect value. This can impact the `GuildToken::_decrementGaugeWeight()` function as well. To fix this issue, the `min()` logic needs to be updated. The recommended mitigation steps include making changes to the code to ensure that the correct minimum value is returned.

### Original Finding Content


The `LendingTerm::debtCeiling()` function calculates the min of `creditMinterBuffer, _debtCeiling and _hardCap` as shown below:

```solidity
// return min(creditMinterBuffer, hardCap, debtCeiling)
if (creditMinterBuffer < _debtCeiling) {
    return creditMinterBuffer;
}
if (_hardCap < _debtCeiling) {
    return _hardCap;
}
return _debtCeiling;
```

However, the above minimum logic is flawed, as it does not always return the minimum of the 3 values.

### Impact

As the `min()` calculation is not correct, the `LendingTerm::debtCeiling()` might return the incorrect value, and so might return a higher debt ceiling rather than the actual debt ceiling as the function should be returning.

`LendingTerm::debtCeiling()` is used in `GuildToken::_decrementGaugeWeight()`, which will will make this function incorrect as well.

### Proof of concept

If `creditMinterBuffer` was 3, `_debtCeiling` was `5`, and `_hardCap` was 1, then the min of the 3 values should be `_hardCap` which is 1.

But instead, this condition becomes true `creditMinterBuffer < _debtCeiling`, which then returns `creditMinterBuffer`, which is incorrect.

### Recommended Mitigation Steps

Update the `min()` logic to be correct:

```diff
-   if (creditMinterBuffer < _debtCeiling) {
-      return creditMinterBuffer;
-   }
-   if (_hardCap < _debtCeiling) {
-      return _hardCap;
-   }
-   return _debtCeiling;
+   if (creditMinterBuffer < _debtCeiling && creditMinterBuffer < _hardCap) {
+       return creditMinterBuffer;
+   } else if (_debtCeiling < _hardCap) {
+       return _debtCeiling;
+   } else {
+       return _hardCap;
+   }
```

**[eswak (Ethereum Credit Guild) confirmed](https://github.com/code-423n4/2023-12-ethereumcreditguild-findings/issues/708#issuecomment-1887517354)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Ethereum Credit Guild |
| Report Date | N/A |
| Finders | 0xStalin, mussucal, santipu\_, neocrao, The-Seraphs, kaden, Byteblockers, Timenov, mojito\_auditor, Chinmay, rbserver, ether\_sky, TheSchnilch, Aymen0909, Varun\_05, nonseodion, thank\_you, 1, 2 |

### Source Links

- **Source**: https://code4rena.com/reports/2023-12-ethereumcreditguild
- **GitHub**: https://github.com/code-423n4/2023-12-ethereumcreditguild-findings/issues/708
- **Contest**: https://code4rena.com/reports/2023-12-ethereumcreditguild

### Keywords for Search

`vulnerability`

