---
# Core Classification
protocol: Zkdx
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37500
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-18-zkDX.md
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
  - Zokyo
---

## Vulnerability Title

“isLeverageEnabled” is true by default

### Overview


This bug report discusses a mistake in the Vault.sol contract where a boolean called `isLeverageEnabled` is mistakenly left as true instead of false. This allows anyone to directly use the contract to open positions, bypassing important security checks. The recommendation is to explicitly initialize the boolean to false in the contract's constructor to disable leverage-related operations by default and require explicit authorization to enable them.

### Original Finding Content

**Severity** : Medium

**Status** : Resolved

**Description**

In the Vault.sol contract, there's a boolean called `isLeverageEnabled` that should be (false) to start. This ensures only PositionManager.sol can manage positions. But, the boolean is mistakenly left (true) when the contract is first set up. This mistake lets anyone directly use the Vault.sol to open positions right away, skipping important checks in  `_validateIncreaseOrder` (PositionManager.sol).

https://github.com/zkDX-DeFi/Smart_Contracts/blob/35f1d4b887bd5b0fc580b7d9fe951c4b550c9897/contracts/core/Vault.sol#L148

**Recommendation**

it is recommended to explicitly initialize the `isLeverageEnabled` flag to false within the Vault contract's constructor. This change ensures that leverage-related operations are disabled by default, requiring explicit authorization (typically from an admin or through a governance process) to enable such features

```sol
constructor() public {
    gov = msg.sender;
    isLeverageEnabled = false; // Ensure leverage is disabled by default.
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Zkdx |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-18-zkDX.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

