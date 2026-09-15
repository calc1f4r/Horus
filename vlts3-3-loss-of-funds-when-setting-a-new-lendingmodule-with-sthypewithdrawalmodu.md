---
# Core Classification
protocol: Valantis
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56684
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-03-17-Valantis.md
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
  - Hexens
---

## Vulnerability Title

[VLTS3-3] Loss of funds when setting a new lendingModule with stHYPEWithdrawalModule::setProposedLendingModule

### Overview


The bug report states that when a new `lendingModule` is set using `stHYPEWithdrawalModule::setProposedLendingModule`, the funds from the current `lendingModule` are transferred to the `stHYPEWithdrawalModule` contract. However, these funds may get stuck in the contract and cannot be transferred to the new `lendingModule` or any other destination. This can happen because the code does not include a way to transfer the withdrawn tokens. To fix this issue, it is recommended to set the withdraw receiver as the SovereignPool and then re-deposit the funds into the new lending module using `supplyToken1ToLendingPool`. This bug has been fixed.

### Original Finding Content

**Severity:** High

**Description:** When a new `lendingModule` is set via `stHYPEWithdrawalModule::setProposedLendingModule` the wrapped native token is transferred from the current `lendingModule` to the `stHYPEWithdrawalModule` contract:
```
if (address(lendingModule) != address(0)) {
    lendingModule.withdraw(lendingModule.assetBalance(), address(this));
}
```
As a consequence, these funds may be stuck in the `stHYPEWithdrawalModule` contract since they are not transferred to the new lending module (`lendingModuleProposal.lendingModule`) and there is also no other way to transfer the withdrawn tokens.
```
function setProposedLendingModule() external onlyOwner {
    if (lendingModuleProposal.startTimestamp > block.timestamp) {
        revert stHYPEWithdrawalModule__setProposedLendingModule_ProposalNotActive();
    }

    if (lendingModuleProposal.startTimestamp == 0) {
        revert stHYPEWithdrawalModule__setProposedLendingModule_InactiveProposal();
    }

    if (address(lendingModule) != address(0)) {
        lendingModule.withdraw(lendingModule.assetBalance(), address(this));
    }

    lendingModule = ILendingModule(lendingModuleProposal.lendingModule);
    delete lendingModuleProposal;
    emit LendingModuleSet(address(lendingModule));
}
```


**Remediation:**  We recommend to set the withdraw receiver as the SovereignPool, such that the withdrawn tokens would simply be counted as reserve. Afterwards, the owner can re-deposit any amount of assets back into the new lending module using `supplyToken1ToLendingPool`.

**Status:**  Fixed


- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Valantis |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-03-17-Valantis.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

