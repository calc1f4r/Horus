---
# Core Classification
protocol: SKALE
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1608
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-02-skale-contest
source_link: https://code4rena.com/reports/2022-02-skale
github_link: https://github.com/code-423n4/2022-02-skale-findings/issues/50

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
  - dexes
  - cdp
  - yield
  - launchpad
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - IllIllI
  - cmichel
  - gzeon
  - kirk-baird
  - 0x1f8b
---

## Vulnerability Title

[M-09] Not compatible with Rebasing/Deflationary/Inflationary tokens

### Overview


This bug report is about the `DepositBoxERC20` contract, which does not appear to support rebasing/deflationary/inflationary tokens whose balance changes during transfers or over time. The necessary checks include at least verifying the amount of tokens transferred to contracts before and after the actual transfer to infer any fees/interest. To mitigate this issue, it is recommended to add support in contracts for such tokens before accepting user-supplied tokens and consider to check before/after balance on the vault. This bug report is applicable for developers who are working with the `DepositBoxERC20` contract.

### Original Finding Content

_Submitted by 0x1f8b, also found by cmichel, kirk-baird, gzeon, and IllIllI_

The `DepositBoxERC20` contract do not appear to support rebasing/deflationary/inflationary tokens whose balance changes during transfers or over time. The necessary checks include at least verifying the amount of tokens transferred to contracts before and after the actual transfer to infer any fees/interest.

### Recommended Mitigation Steps

Add support in contracts for such tokens before accepting user-supplied tokens
Consider to check before/after balance on the vault.

**[cstrangedk (SKALE) disputed and commented](https://github.com/code-423n4/2022-02-skale-findings/issues/50#issuecomment-1062060382):**
 > Issue is acknowledged and is contingent on SKALE Chain owner configuration and evaluation of compatibile tokens.

**[GalloDaSballo (judge) commented](https://github.com/code-423n4/2022-02-skale-findings/issues/50#issuecomment-1143858483):**
 > Because this is reliant on configuration, I believe the finding to be valid and of medium severity.
> 
> End users can verify if the DepositBoxes are properly handling rebasing tokens at the time they wish to bridge



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | SKALE |
| Report Date | N/A |
| Finders | IllIllI, cmichel, gzeon, kirk-baird, 0x1f8b |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-skale
- **GitHub**: https://github.com/code-423n4/2022-02-skale-findings/issues/50
- **Contest**: https://code4rena.com/contests/2022-02-skale-contest

### Keywords for Search

`vulnerability`

