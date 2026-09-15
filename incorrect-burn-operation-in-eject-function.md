---
# Core Classification
protocol: Auxo Governance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60564
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/auxo-governance/6d7dbf90-5898-41c6-a929-3c7a69e9df28/index.html
source_link: https://certificate.quantstamp.com/full/auxo-governance/6d7dbf90-5898-41c6-a929-3c7a69e9df28/index.html
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
finders_count: 4
finders:
  - Ed Zulkoski
  - Ruben Koch
  - Cameron Biniamow
  - Mostafa Yassin
---

## Vulnerability Title

Incorrect Burn Operation in `eject()` Function

### Overview


The report states that there was a bug in the `eject()` function of the `TokenLocker.sol` file, which is now fixed. The bug caused the wrong account to have their `veTokens` burned, resulting in the loss of their voting power. This also caused ejected accounts to retain their voting power without having any stakes. The recommendation is to change the line of code to ensure that the correct account's `veTokens` are burned. 

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `6daf6a0a70faef0208ca3aa3e16414d6bbee14a7`.

Recommendation implemented.

**File(s) affected:**`TokenLocker.sol`

**Description:** The function `eject()` iterates through a list of accounts removing a given account's stake if its lock has expired. This involves burning each account's `veTokens` and transferring them their corresponding depositTokens. However, the loop instead burns from `msg.sender`:

`veToken.burn(account, veToken.balanceOf(_msgSender()));`

This has the effect of incorrectly clearing the `veToken` balance of the caller, thus removing their voting power, while also not removing the voting power for any of the ejected accounts. As long as these ejected accounts do not create a new lock, they will permanently retain their voting power while having zero stakes.

**Recommendation:** Change the above line to:

`veToken.burn(account, veToken.balanceOf(account));`

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Auxo Governance |
| Report Date | N/A |
| Finders | Ed Zulkoski, Ruben Koch, Cameron Biniamow, Mostafa Yassin |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/auxo-governance/6d7dbf90-5898-41c6-a929-3c7a69e9df28/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/auxo-governance/6d7dbf90-5898-41c6-a929-3c7a69e9df28/index.html

### Keywords for Search

`vulnerability`

