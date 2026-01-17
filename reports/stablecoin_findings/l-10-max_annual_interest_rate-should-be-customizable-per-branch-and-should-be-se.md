---
# Core Classification
protocol: Quill Finance Report
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53933
audit_firm: Recon Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Recon Audits/2025-03-23-Quill_Finance_Report.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

[L-10] `MAX_ANNUAL_INTEREST_RATE` should be customizable per branch and should be set higher due to exotic collaterals

### Overview

See description below for full details.

### Original Finding Content

**Q - Why is this not customizable?**

`MAX_ANNUAL_INTEREST_RATE` is left unchanged from Bold

`uint256 constant MAX_ANNUAL_INTEREST_RATE = _100pct;`

But Quill has collaterals that are more exotic, and also has the ability to update them

See this finding from my original review of Bold

**Lack of premium on redeeming higher interest troves can lead to all troves having the higher interest rate and still be redeemed - Cold Start Problem**

**Impact**

The following is a reasoned discussion around a possibly unsolved issue around CDP Design

In the context of Liquity V2, redemptions have the following aspect:
- Premium is paid to the owner that get's their troved redeemed
- Premium is dynamic like in V1, with the key difference being that Troves are now sorted by interest rate they pay

This creates a scenario, in the most extreme case, in which all Troves are paying the maximum borrow rate, but are still being redeemed against

**Intuition**

Any time levering up costs more than the base redemption fee (brings the price below it), the Trove will get redeemed against

The logic for redeeming is the fee paid

If the fee paid is not influenced by the rate paid by borrowers, then fundamentally there are still scenarios in which redemptions will close Troves in the most extreme scenarios

**Mitigation**

As discussed with the team, it may be necessary to charge a higher max borrow rate

Alternatively, redemptions should pay an additional premium to the Trove, based on the rate that is being paid by the borrower, the fundamental challenge with this is fairly pricing the rate of borrowing LUSD against the "defi risk free rate"

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Recon Audits |
| Protocol | Quill Finance Report |
| Report Date | N/A |
| Finders | Alex The Entreprenerd |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Recon Audits/2025-03-23-Quill_Finance_Report.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

