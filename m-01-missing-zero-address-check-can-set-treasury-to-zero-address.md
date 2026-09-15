---
# Core Classification
protocol: Canto
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25226
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-canto
source_link: https://code4rena.com/reports/2022-06-canto
github_link: https://github.com/code-423n4/2022-06-newblockchain-findings/issues/121

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
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-01] Missing zero address check can set treasury to zero address

### Overview


A bug has been reported in the AccountantDelegate.initialize() function of the lending-market repository on GitHub. The bug is related to the `treasury_` parameter, which could be mistakenly set to the 0 address. A proof of concept has been provided which shows the lack of a zero address check for the `treasury_` parameter. The recommended mitigation step is to add a require() check for zero address for the treasury parameter before changing the treasury address in the initialize function. The bug has been confirmed by nivasan1 (Canto) and Alex the Entreprenerd (judge) has commented that the finding is technically correct and of medium severity due to the risk of loss of funds and the inability to easily fix.

### Original Finding Content

_Submitted by cryptphi_

AccountantDelegate.initialize() is missing a zero address check for `treasury_` parameter, which could maybe allow treasury to be mistakenly set to 0 address.

### Proof of Concept

<https://github.com/Plex-Engineer/lending-market/blob/755424c1f9ab3f9f0408443e6606f94e4f08a990/contracts/Accountant/AccountantDelegate.sol#L20>

### Recommended Mitigation Steps

Add a require() check for zero address for the treasury parameter before changing the treasury address in the initialize function.

**[nivasan1 (Canto) confirmed](https://github.com/code-423n4/2022-06-canto-findings/issues/121)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-06-canto-findings/issues/121#issuecomment-1212623337):**
 > Because:
> - The finding is technically correct
> - The `treasury` variable is only set on the initializer
> - An incorrect setting could cause loss of funds
> 
> I'm going to mark the finding as valid and of Medium severity.
> 
> In mentioning this report in the future, notice that the conditions that caused me to raise the severity weren't simply the lack of a check, but the actual risk of loss of funds, and the inability to easily fix.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Canto |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-canto
- **GitHub**: https://github.com/code-423n4/2022-06-newblockchain-findings/issues/121
- **Contest**: https://code4rena.com/reports/2022-06-canto

### Keywords for Search

`vulnerability`

