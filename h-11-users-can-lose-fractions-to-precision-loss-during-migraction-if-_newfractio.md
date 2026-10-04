---
# Core Classification
protocol: Fractional
chain: everychain
category: arithmetic
vulnerability_type: precision_loss

# Attack Vector Details
attack_type: precision_loss
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2992
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-fractional-v2-contest
source_link: https://code4rena.com/reports/2022-07-fractional
github_link: https://github.com/code-423n4/2022-07-fractional-findings/issues/137

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - precision_loss

protocol_categories:
  - dexes
  - bridge
  - yield
  - launchpad
  - synthetics

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - MEP
  - 0x52
  - hansfriese
  - 0x29A
---

## Vulnerability Title

[H-11] Users can lose fractions to precision loss during migraction if _newFractionSupply is set very low

### Overview


This bug report is about a vulnerability in the code of a fractional project, which could cause precision loss and potentially cause complete loss to the vault. The vulnerability is located in the code at https://github.com/code-423n4/2022-07-fractional/blob/8f2697ae727c60c93ea47276f8fa128369abfe51/src/modules/Migration.sol#L72-L99. The impact of this vulnerability is that users could lose value, and in some cases, access to the vault could be lost. The proof of concept is that if the supply of the fraction is set to a certain value, then users with less than that value would receive no shares due to precision loss. Under certain conditions, it could cause the vault to be frozen. To mitigate this vulnerability, it is recommended that when calling propose, the newFractionSupply is greater than some value (i.e. 1E18).

### Original Finding Content

_Submitted by 0x52, also found by 0x29A, hansfriese, and MEP_

Precision loss causing loss of user value and potentially cause complete loss to vault.

### Proof of Concept

<https://github.com/code-423n4/2022-07-fractional/blob/8f2697ae727c60c93ea47276f8fa128369abfe51/src/modules/Migration.sol#L471-L472>

If the supply of the fraction is set to say 10 then any user that uses `migrateFractions` with less than 10% of the contributions will receive no shares at all due to precision loss. Under certain conditions it may even cause complete loss of access to the vault. In this same example, if less than 5 fractions can be redeemed (i.e. not enough people have more than 10% to overcome the precision loss) then the vault would never be able to be bought out and the vault would forever be frozen.

### Recommended Mitigation Steps

When calling propose require that `\_newFractionSupply` is greater than some value (i.e. 1E18).

**[stevennevins (Fractional) confirmed](https://github.com/code-423n4/2022-07-fractional-findings/issues/137)** 

**[HardlyDifficult (judge) commented](https://github.com/code-423n4/2022-07-fractional-findings/issues/137#issuecomment-1208614341):**
 > Rounding can lead to loss of assets. Agree with severity.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Fractional |
| Report Date | N/A |
| Finders | MEP, 0x52, hansfriese, 0x29A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-fractional
- **GitHub**: https://github.com/code-423n4/2022-07-fractional-findings/issues/137
- **Contest**: https://code4rena.com/contests/2022-07-fractional-v2-contest

### Keywords for Search

`Precision Loss`

