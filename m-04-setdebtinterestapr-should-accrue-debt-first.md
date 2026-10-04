---
# Core Classification
protocol: JPEG'd
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 22293
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-04-jpegd
source_link: https://code4rena.com/reports/2022-04-jpegd
github_link: https://github.com/code-423n4/2022-04-jpegd-findings/issues/78

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
  - lending
  - dexes
  - cdp
  - services
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-04] `setDebtInterestApr` should accrue debt first

### Overview


A bug was reported in the NFTVault.sol#L212 contract. The bug was that the `setDebtInterestApr` was changing the debt interest rate without accruing the debt first, which meant that the new debt interest rate was applied retroactively to the unaccrued period on the next `accrue()` call. This could be unfair and wrong as borrowers can incur more debt than they should.

The recommended mitigation step was to call `accrue()` first in `setDebtInterestApr` before setting the new `settings.debtInterestApr`. This bug was confirmed and resolved by spaghettieth (JPEG'd) and the fix was implemented in jpegd/core#4.

### Original Finding Content

_Submitted by cmichel, also found by pedroais_

[NFTVault.sol#L212](https://github.com/code-423n4/2022-04-jpegd/blob/e72861a9ccb707ced9015166fbded5c97c6991b6/contracts/vaults/NFTVault.sol#L212)<br>

The `setDebtInterestApr` changes the debt interest rate without first accruing the debt.<br>
This means that the new debt interest rate is applied retroactively to the unaccrued period on next `accrue()` call.

It should never be applied retroactively to a previous time window as this is unfair & wrong.<br>
Borrowers can incur more debt than they should.

### Recommended Mitigation Steps

Call `accrue()` first in `setDebtInterestApr` before setting the new `settings.debtInterestApr`.

**[spaghettieth (JPEG'd) confirmed](https://github.com/code-423n4/2022-04-jpegd-findings/issues/78)**

**[spaghettieth (JPEG'd) resolved and commented](https://github.com/code-423n4/2022-04-jpegd-findings/issues/78#issuecomment-1099241122):**
 > Fixed in [jpegd/core#4](https://github.com/jpegd/core/pull/4).



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | JPEG'd |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-jpegd
- **GitHub**: https://github.com/code-423n4/2022-04-jpegd-findings/issues/78
- **Contest**: https://code4rena.com/reports/2022-04-jpegd

### Keywords for Search

`vulnerability`

