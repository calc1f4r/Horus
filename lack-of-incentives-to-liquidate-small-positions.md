---
# Core Classification
protocol: Euler Vault Kit (EVK) Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32439
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/euler-vault-kit-evk-audit
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Lack of Incentives to Liquidate Small Positions

### Overview


This bug report discusses an issue where users are able to open positions with collateral that is too small to be profitably liquidated. This can lead to ongoing interest accumulation and potential losses for the user. The report suggests implementing a minimum collateral deposit requirement to address this issue. However, the team has acknowledged the issue but has not yet resolved it. They believe that the current code is prepared to handle the issue and that the impact of these small positions is negligible. They also suggest that the recommended solution can be enforced using hooks and that with debt socialization, the vault's governor may be incentivized to liquidate these small positions. 

### Original Finding Content

There are currently no checks in place to regulate the size of the collateral that users can utilize to open positions. Consequently, users might open positions with collateral that is too small to be profitably liquidated in different vaults. Given the complex architecture and substantial gas costs associated with liquidation, these small positions may never be liquidated, leading to ongoing interest accumulation.


Consider implementing a minimum collateral deposit requirement. This would ensure that the collateral supporting the position maintains sufficient value to incentivize liquidation and overcome the gas cost of such a process.


***Update:** Acknowledged, not resolved. The Euler team stated:*



> *We acknowledge the issue. We acknowledge that there exists a risk of the vault holding small bad debt positions which are not profitable to liquidate. However, we think that the current code is sufficiently prepared to handle the issue.*
> 
> 
> *Firstly, the problem of small positions has been discussed extensively in public, but so far it has not been confirmed to be an issue in practice. Our own experience from V1 confirms this. While we have definitely seen small debt positions which were not picked up by the liquidators, their overall impact on the lending pools was negligible.*
> 
> 
> *Secondly, the recommended solution - minimum collateral deposit - can already be mostly enforced with a use of hooks. In the open EVC-EVK architecture, it would make more sense to enforce a minimum limit on the liability rather than collateral deposited, and it could be achieved by hooking operations which manipulate debt in conjunction with `checkVaultStatus`.*
> 
> 
> *Lastly, with debt socialization, the vault’s governor may be incentivized to liquidate the small positions at a loss in order to take the bad debt off the books for the benefit of the vault and its attractiveness to the users.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Euler Vault Kit (EVK) Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/euler-vault-kit-evk-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

