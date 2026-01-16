---
# Core Classification
protocol: Filament
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45625
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-08-15-Filament.md
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

VaultFacet contains a rug vector where a rogue team member may be able to cause mass liquidations

### Overview


The report discusses a bug in the VaultFacet portion of the Diamond contract, which is responsible for various functions needed for the protocol to work correctly. One of these functions, updateCollateralizationRatio, sets the minimum collateral required for trading derivatives. The bug allows the contract owner to change this ratio while users are still invested, potentially causing mass liquidations and centralization risks. The recommendation is to update the function in two steps and introduce a grace period to allow users to adjust their positions before any changes take effect. The bug has been resolved.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

The VaultFacet portion of the Diamond contract is responsible for various setters and configuration functions which are required to be called and set in order for the protocol to function properly. One of these functions is the updateCollateralizationRatio which sets the amount of collateral required in order to trade a derivative by setting a value for s.CollateralizationRatio[_indexToken] which the users deposited collateral must be greater than this threshold. The issue lies in the overstepping of privileges whilst users are still invested in the protocol. A malicious owner could update the collateralization ratio for an asset to cause mass liquidations opening users up to a significant centralisation risk.

**Recommendation**:

It’s recommended that the updateCollateralizationRatio is updated through a two step function where we set and notify users of the new updated collateralization ratio into a pending state. After a reasonable period of time, the collateralization ratio can be “confirmed” and set allowing users to do their proper due diligence. In addition to this, a grace period can optionally (in the context of this issue) be introduced (perhaps a 3 or 4 hours) to allow users to bring their positions back to a healthy state or else be liquidated.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Filament |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-08-15-Filament.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

