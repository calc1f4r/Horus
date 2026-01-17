---
# Core Classification
protocol: Zaros
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34831
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
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
finders_count: 1
finders:
  - Dacian
---

## Vulnerability Title

Users can easily bypass collateral `depositCap` limit using multiple deposits under the limit

### Overview


The report discusses a bug in the Margin collateral system where the `depositCap` configuration, which is supposed to limit the total amount of collateral that can be deposited, is not working correctly. This is because the validation function does not check the total amount of collateral already deposited for a specific type, allowing users to deposit more than the set limit by making multiple transactions. The impact of this bug is that users can deposit more collateral than intended. The recommended solution is to update the validation function to also consider the total amount of collateral already deposited for a specific type. The bug has been fixed in a recent commit and has been verified by a third party.

### Original Finding Content

**Description:** Margin collateral has a `depositCap` configuration to limit the total deposited amount for a particular collateral type.

But validation in `_requireEnoughDepositCap()` reverts when the current amount being deposited is greater than `depositCap`.

```solidity
function _requireEnoughDepositCap(address collateralType, UD60x18 amount, UD60x18 depositCap) internal pure {
    if (amount.gt(depositCap)) {
        revert Errors.DepositCap(collateralType, amount.intoUint256(), depositCap.intoUint256());
    }
}
```

As it doesn't check the total deposited amount for that collateral type, users can deposit as much as they want by using separate transactions each being under `depositCap`.

**Impact:** Users can deposit more margin collateral than `depositCap`.

**Recommended Mitigation:** `_requireEnoughDepositCap` should check if the total deposited amount for that collateral type plus the new deposit is not greater than `depositCap`.

**Zaros:** Fixed in commit [0d37299](https://github.com/zaros-labs/zaros-core/commit/0d37299f6d5037afc9863dc6f0ae3871784ce376).

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Zaros |
| Report Date | N/A |
| Finders | Dacian |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

