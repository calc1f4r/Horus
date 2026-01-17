---
# Core Classification
protocol: Accountable
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62977
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
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
  - options_vault
  - liquidity_manager
  - insurance
  - uncollateralized_lending

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Immeas
  - Chinmay
  - Alexzoid
---

## Vulnerability Title

InvestmentManager can use `AccountableFixedTerm::coverDefault` to misuse token approvals from anyone

### Overview


The bug report describes an issue in the code for the `coverDefault` function in the `AccountableFixedTerm` contract. This function allows the InvestmentManager of a loan to add additional assets to the system. However, the code also allows the manager to pull assets from a random user's address without their permission, potentially resulting in the loss of their funds. This issue also exists in the `AccountableOpenTerm` contract. The report recommends removing the "provider" address logic and using `msg.sender` instead. The bug has been fixed in the code and verified by Cyfrin.

### Original Finding Content

**Description:** `AccountableFixedTerm::coverDefault` allows InvestmentManager of the loan to add additional assets to the system.

```solidity
    function coverDefault(uint256 assets, address provider) external onlySafetyModuleOrManager whenNotPaused {
        _requireLoanInDefault();

        loanState = LoanState.InDefaultClaims;

        IAccountableVault(vault).lockAssets(assets, provider);

        emit DefaultCovered(safetyModule, provider, assets);
    }
```

And `lockAssets()` pulls assets from the input "provider" address, transferring them to the vault.

This means any user address who had asset token balance, and approved the vault contract (potential pending approvals from the past) is at risk of losing their funds here.

The Manager can pull funds from a random provider address without any permissions, and the "provider" would lose his approved funds without getting anything in return.

**Impact:** Any pending asset approvals from user => vault contract, can be misused to cover loan default.

The same problem also exists in AccountableOpenTerm.

**Recommended Mitigation:** Consider removing the "provider" address logic from `coverDefault()`, and simply pull assets from `msg.sender`.

**Accountable:** Fixed in commit [`014d7fb`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/014d7fb6f11766fada9054a736a264cf1d95c9f6)

**Cyfrin:** Verified. `provider` is removed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Accountable |
| Report Date | N/A |
| Finders | Immeas, Chinmay, Alexzoid |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

