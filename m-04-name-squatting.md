---
# Core Classification
protocol: Aave Lens
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1474
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-02-aave-lens-contest
source_link: https://code4rena.com/reports/2022-02-aave-lens
github_link: https://github.com/code-423n4/2022-02-aave-lens-findings/issues/27

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
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cmichel
---

## Vulnerability Title

[M-04] Name squatting

### Overview


This bug report is about a vulnerability in the code of a project called LensHub. The vulnerability is that creating profiles through the `LensHub/PublishingLogic.createProfile` function does not cost anything, allowing people to "name squat" and take up handles that are in demand, even if they don't need them. This ruins the experience for many high-profile users who can't get their desired handle. The recommended mitigation step is to consider auctioning off handles to the highest bidder or at least taking a fee such that the cost of name squatting is not zero.

### Original Finding Content

_Submitted by cmichel_

[LensHub.sol#L142](https://github.com/code-423n4/2022-02-aave-lens/blob/aaf6c116345f3647e11a35010f28e3b90e7b4862/contracts/core/LensHub.sol#L142)<br>

Creating profiles through `LensHub/PublishingLogic.createProfile` does not cost anything and will therefore result in "name squatting".<br>
A whitelisted profile creator will create many handles that are in demand, even if they don't need them, just to flip them for a profit later.<br>
This ruins the experience for many high-profile users that can't get their desired handle.

### Recommended Mitigation Steps

Consider auctioning off handles to the highest bidder or at least taking a fee such that the cost of name squatting is not zero.

**[donosonaumczuk (Aave Lens) disputed](https://github.com/code-423n4/2022-02-aave-lens-findings/issues/27)**

**[oneski (Aave Lens) commented](https://github.com/code-423n4/2022-02-aave-lens-findings/issues/27#issuecomment-1042215123):**
 > Declined. This is by design. Governance can allow contracts/addresses to mint. If governance allows a malicious actor that is the fault of governance. Governance can also allow contracts that implement auction or other functionality as well to manage the profile minting system.
> 
> The protocol should take no opinion on this by default.

**[0xleastwood (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-02-aave-lens-findings/issues/27#issuecomment-1117274439):**
 > I will mark this as `medium` risk for the same reasons outlined in [M-03 (Issue #26)](https://github.com/code-423n4/2022-02-aave-lens-findings/issues/26#issuecomment-1125814379).



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Aave Lens |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-aave-lens
- **GitHub**: https://github.com/code-423n4/2022-02-aave-lens-findings/issues/27
- **Contest**: https://code4rena.com/contests/2022-02-aave-lens-contest

### Keywords for Search

`vulnerability`

