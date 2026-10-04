---
# Core Classification
protocol: Apollon Report
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53841
audit_firm: Recon Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Recon Audits/2025-03-22-Apollon_Report.md
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
  - Alex The Entreprenerd
---

## Vulnerability Title

[M-01] `RedemptionOperations` Redemptions should be disabled during Recovery Mode

### Overview


The report discusses an issue with a piece of code called `RedemptionOperations`. The code is supposed to check for a specific condition, but it is currently checking for the wrong thing. This could potentially cause problems with the system's ability to handle certain situations. The report suggests investigating if this issue could lead to additional problems and compares it to how another protocol, Liquity, handles a similar check. 

### Original Finding Content

**Impact**

`RedemptionOperations` checks the `TCR < MCR`, but should most likely check for `TCR < CCR`

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/RedemptionOperations.sol#L101-L103

```solidity
    (, uint TCR, , ) = storagePool.checkRecoveryMode(vars.priceCache); /// @audit High? not checking RM -> Mint for free, Inflate total supply (pay no redemption), redeem at small fee
    if (TCR < MCR) revert LessThanMCR(); /// @audit-ok force to liquidate if all system is insolvent

```

This is because during Recovery Mode, minting fees are voided, meaning that the system may open up to additional arbitrages via Redemptions

Redemptions are generally disabled during RM in favour of liquidations


**Mitigation**

Investigate if additional arbitrages could be detrimental to your protocol due to reduced minting fees

From checking liquity they use a check similar to yours:
https://github.com/liquity/dev/blob/e38edf3dd67e5ca7e38b83bcf32d515f896a7d2f/packages/contracts/contracts/TroveManager.sol#L948-L962

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Recon Audits |
| Protocol | Apollon Report |
| Report Date | N/A |
| Finders | Alex The Entreprenerd |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Recon Audits/2025-03-22-Apollon_Report.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

